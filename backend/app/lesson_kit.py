"""Small constructors for lesson content, so content files stay readable.

Each helper returns the plain dict shape documented in seed_content.py.
"""


def h2(text: str) -> dict:
    return {"type": "h2", "text": text}


def p(text: str) -> dict:
    return {"type": "p", "text": text}


def code(source: str) -> dict:
    return {"type": "code", "code": source.strip("\n")}


def note(text: str) -> dict:
    return {"type": "callout", "kind": "note", "text": text}


def tip(text: str) -> dict:
    return {"type": "callout", "kind": "tip", "text": text}


def warn(text: str) -> dict:
    return {"type": "callout", "kind": "warn", "text": text}


def link(text: str, href: str) -> dict:
    return {"type": "link", "text": text, "href": href}


def step(title: str, body: str, source: str, at: str = "top") -> dict:
    """One code-along step.

    The learner builds a single Program.cs by appending each step's code in order.
    C# requires top-level statements to come before type declarations, so steps that
    declare classes/records/interfaces/enums must use at="bottom" and their body must tell
    the learner to add the code at the *bottom* of the file. verify_content.py assembles
    the program the same way: "top" steps in order, then "bottom" steps in order.
    """
    return {"title": title, "body": body, "code": source.strip("\n"), "at": at}


def codealong(title: str, intro: str, steps: list[dict], filename: str = "Program.cs") -> dict:
    return {"title": title, "intro": intro, "filename": filename, "steps": steps}


def lab(
    title: str,
    difficulty: str,
    description: str,
    requirements: list[str],
    expected_output: str,
    hint: str,
    filename: str = "Lab.cs",
) -> dict:
    return {
        "title": title,
        "difficulty": difficulty,
        "description": description,
        "filename": filename,
        "requirements": requirements,
        "expected_output": expected_output.strip("\n"),
        "hint": hint,
    }


def lesson(subtitle: str, reading: list[dict], codealong: dict | None = None, lab: dict | None = None) -> dict:
    return {"subtitle": subtitle, "reading": reading, "codealong": codealong, "lab": lab}
