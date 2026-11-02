"""Compile and run every code-along and lab solution with the local .NET SDK.

Usage (from backend/):   python verify_content.py [module numbers...]

Checks, per lesson in app/content_m<N>.py (exports LESSONS and SOLUTIONS):
  * structure: block types, non-empty reading, lab has requirements + hint
  * code-along: the steps assembled into one Program.cs compile and exit 0
  * lab: SOLUTIONS[(m, l)] compiles, exits 0, and prints exactly lab["expected_output"]
Mirrors the runner (runner/template: net10.0, implicit usings, en-US culture).
"""
import importlib
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE.parent / "runner" / "template"
BLOCKS = {"h2", "p", "code", "callout", "link"}


def run_program(source: str) -> tuple[bool, str]:
    work = Path(tempfile.mkdtemp(prefix="csj_"))
    try:
        for f in TEMPLATE.glob("*.c*"):
            shutil.copy(f, work / f.name)
        (work / "Program.cs").write_text(source, encoding="utf-8")
        b = subprocess.run(
            ["dotnet", "build", "-nologo", "-v", "q", "-clp:NoSummary", "-o", "out"],
            cwd=work, capture_output=True, text=True, timeout=180,
        )
        if b.returncode != 0:
            errs = sorted({l.strip() for l in b.stdout.splitlines() if "error " in l})
            return False, "COMPILE ERROR\n" + "\n".join(errs[:8])
        r = subprocess.run(
            ["dotnet", "out/app.dll"], cwd=work, capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL,
        )
        return r.returncode == 0, (r.stdout + r.stderr).rstrip()
    except subprocess.TimeoutExpired:
        return False, "TIMEOUT"
    finally:
        shutil.rmtree(work, ignore_errors=True)


def assemble(steps: list[dict]) -> str:
    top = [s["code"] for s in steps if s.get("at", "top") != "bottom"]
    bottom = [s["code"] for s in steps if s.get("at") == "bottom"]
    return "\n\n".join(top + bottom) + "\n"


def lines(text: str) -> list[str]:
    return [l.rstrip() for l in text.strip().splitlines()]


def check_structure(key, lesson) -> list[str]:
    problems = []
    if not lesson.get("subtitle"):
        problems.append("missing subtitle")
    reading = lesson.get("reading") or []
    if len(reading) < 6:
        problems.append(f"reading too thin ({len(reading)} blocks)")
    for b in reading:
        if b.get("type") not in BLOCKS:
            problems.append(f"bad block type {b.get('type')!r}")
        if "coming soon" in str(b).lower():
            problems.append("contains 'coming soon'")
    ca, lab = lesson.get("codealong"), lesson.get("lab")
    if ca and len(ca["steps"]) < 3:
        problems.append("code-along needs >= 3 steps")
    if lab:
        if len(lab["requirements"]) < 3:
            problems.append("lab needs >= 3 requirements")
        if not lab.get("hint") or not lab.get("expected_output"):
            problems.append("lab missing hint/expected_output")
    return problems


def verify_lesson(key, lesson, solutions) -> list[str]:
    problems = check_structure(key, lesson)
    ca, lab = lesson.get("codealong"), lesson.get("lab")
    if ca:
        ok, out = run_program(assemble(ca["steps"]))
        if not ok:
            problems.append("code-along failed:\n" + out)
    if lab:
        sol = solutions.get(key)
        if sol is None:
            problems.append("lab has no entry in SOLUTIONS")
        else:
            ok, out = run_program(sol)
            if not ok:
                problems.append("lab solution failed:\n" + out)
            elif lines(out) != lines(lab["expected_output"]):
                problems.append(
                    "lab solution output != expected_output\n--- expected\n"
                    + lab["expected_output"] + "\n--- got\n" + out
                )
    return problems


def main(modules: list[int]) -> int:
    sys.path.insert(0, str(HERE))
    jobs = []
    for m in modules:
        try:
            mod = importlib.import_module(f"app.content_m{m}")
        except ModuleNotFoundError:
            print(f"module {m}: app/content_m{m}.py not found")
            return 1
        for key, lesson in sorted(mod.LESSONS.items()):
            jobs.append((key, lesson, mod.SOLUTIONS))
    failed = 0
    with ThreadPoolExecutor(max_workers=3) as pool:
        for (key, _, _), problems in zip(jobs, pool.map(lambda j: verify_lesson(*j), jobs)):
            label = f"{key[0]}.{key[1]}"
            if problems:
                failed += 1
                print(f"FAIL {label}")
                for pr in problems:
                    print("   ", pr.replace("\n", "\n    "))
            else:
                print(f"ok   {label}")
    print(f"\n{len(jobs) - failed}/{len(jobs)} lessons verified")
    return 1 if failed else 0


if __name__ == "__main__":
    mods = [int(a) for a in sys.argv[1:]] or list(range(1, 9))
    sys.exit(main(mods))
