import { useEffect, useRef, useState } from "react";
import type { KeyboardEvent } from "react";
import type { CliResult } from "../types";

interface Line {
  kind: "hint" | "cmd" | "out" | "err";
  text: string;
  cwd?: string;
}

const WELCOME = "Sandboxed terminal. Try: dotnet --version, dotnet new console -n hello, cd hello, dotnet run. Type help for more.";

// One persistent session id per browser, so files created by `dotnet new` survive across lessons.
function sessionId() {
  try {
    let id = localStorage.getItem("cli-session");
    if (!id) {
      id = crypto.randomUUID();
      localStorage.setItem("cli-session", id);
    }
    return id;
  } catch {
    return "default";
  }
}

// Minimal terminal. `onRun(session, command)` resolves to {ok, output, cwd}.
export default function Terminal({ onRun }: { onRun: (session: string, command: string) => Promise<CliResult> }) {
  const [lines, setLines] = useState<Line[]>([{ kind: "hint", text: WELCOME }]);
  const [cwd, setCwd] = useState("~");
  const [input, setInput] = useState("");
  const [busy, setBusy] = useState(false);
  const history = useRef<string[]>([]);
  const cursor = useRef(0);
  const session = useRef(sessionId());
  const scroller = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const root = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scroller.current?.scrollTo({ top: scroller.current.scrollHeight });
  }, [lines, busy]);

  // The input keeps focus until the user clicks somewhere outside the terminal.
  const clickedOutside = useRef(false);
  useEffect(() => {
    const onDown = (e: MouseEvent) => {
      clickedOutside.current = !root.current?.contains(e.target as Node);
    };
    document.addEventListener("mousedown", onDown, true);
    return () => document.removeEventListener("mousedown", onDown, true);
  }, []);

  function keepFocus() {
    if (clickedOutside.current || !document.hasFocus()) return;
    if (window.getSelection()?.toString()) return; // don't break selecting output text to copy
    setTimeout(() => {
      // Skip when the terminal is hidden (other tab) or something else took focus.
      if (root.current?.offsetParent && !clickedOutside.current && document.activeElement === document.body)
        inputRef.current?.focus();
    }, 0);
  }

  async function submit() {
    const command = input.trim();
    if (busy || !command) return;
    setInput("");
    history.current.push(command);
    cursor.current = history.current.length;

    if (command === "clear") {
      setLines([]);
      return;
    }
    setLines((l) => [...l, { kind: "cmd", cwd, text: command }]);
    setBusy(true);
    try {
      const res = await onRun(session.current, command);
      setCwd(res.cwd);
      if (res.output) setLines((l) => [...l, { kind: res.ok ? "out" : "err", text: res.output } as Line]);
    } catch (e) {
      setLines((l) => [...l, { kind: "err", text: (e as Error).message }]);
    } finally {
      setBusy(false);
      inputRef.current?.focus();
    }
  }

  function onKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter") {
      e.preventDefault();
      submit();
    } else if (e.key === "ArrowUp" || e.key === "ArrowDown") {
      e.preventDefault();
      const h = history.current;
      cursor.current = Math.max(0, Math.min(h.length, cursor.current + (e.key === "ArrowUp" ? -1 : 1)));
      setInput(h[cursor.current] ?? "");
    } else if (e.key === "l" && e.ctrlKey) {
      e.preventDefault();
      setLines([]);
    }
  }

  return (
    <div className="terminal" ref={root} onClick={() => inputRef.current?.focus()}>
      <div className="terminal-scroll" ref={scroller}>
        {lines.map((l, i) =>
          l.kind === "cmd" ? (
            <div key={i} className="term-line">
              <span className="term-prompt">{l.cwd} $</span> {l.text}
            </div>
          ) : (
            <pre key={i} className={`term-${l.kind}`}>{l.text}</pre>
          )
        )}
        <div className="term-line term-input-row">
          <span className="term-prompt">{cwd} $</span>
          <input
            ref={inputRef}
            value={input}
            readOnly={busy}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={onKeyDown}
            onBlur={keepFocus}
            spellCheck={false}
            autoCapitalize="off"
            autoComplete="off"
            aria-label="Terminal command"
            placeholder={busy ? "Running…" : ""}
          />
        </div>
      </div>
    </div>
  );
}
