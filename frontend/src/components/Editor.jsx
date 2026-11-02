import { useEffect, useMemo, useRef, useState } from "react";
import { EditorState } from "@codemirror/state";
import { EditorView, keymap, lineNumbers, highlightActiveLine, highlightActiveLineGutter, drawSelection } from "@codemirror/view";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { StreamLanguage, HighlightStyle, syntaxHighlighting, indentOnInput, bracketMatching } from "@codemirror/language";
import { closeBrackets, closeBracketsKeymap } from "@codemirror/autocomplete";
import { setDiagnostics } from "@codemirror/lint";
import { csharp } from "@codemirror/legacy-modes/mode/clike";
import { tags as t } from "@lezer/highlight";

const highlightStyle = HighlightStyle.define([
  { tag: [t.keyword, t.modifier, t.operatorKeyword], color: "#c792ea" },
  { tag: [t.typeName, t.className, t.namespace], color: "#ffcb6b" },
  { tag: [t.string, t.special(t.string)], color: "#c3e88d" },
  { tag: [t.number, t.bool, t.null, t.atom], color: "#f78c6c" },
  { tag: [t.lineComment, t.blockComment], color: "#546e7a", fontStyle: "italic" },
  { tag: [t.function(t.variableName), t.function(t.propertyName)], color: "#82aaff" },
  { tag: [t.operator, t.punctuation], color: "#89ddff" },
  { tag: t.meta, color: "#89ddff" },
]);

const theme = EditorView.theme(
  {
    "&": { height: "100%", color: "#e2e8f0", backgroundColor: "transparent", fontSize: "13px" },
    "&.cm-focused": { outline: "none" },
    ".cm-scroller": { fontFamily: "var(--font-mono)", lineHeight: "1.7", overflow: "auto" },
    ".cm-content": { padding: "12px 0", caretColor: "#fff" },
    ".cm-cursor": { borderLeftColor: "#fff" },
    ".cm-gutters": { backgroundColor: "transparent", color: "#546e7a", border: "none" },
    ".cm-lineNumbers .cm-gutterElement": { padding: "0 10px 0 14px", minWidth: "36px" },
    ".cm-activeLine": { backgroundColor: "rgba(255,255,255,.04)" },
    ".cm-activeLineGutter": { backgroundColor: "transparent", color: "#cbd5e1" },
    ".cm-selectionBackground, &.cm-focused .cm-selectionBackground": { backgroundColor: "rgba(99,102,241,.35)" },
    ".cm-matchingBracket": { backgroundColor: "rgba(255,255,255,.15)", outline: "1px solid rgba(255,255,255,.3)" },
    ".cm-lintRange-error": { backgroundImage: "none", textDecoration: "underline wavy #f87171", textUnderlineOffset: "3px" },
    ".cm-tooltip": { backgroundColor: "#1e293b", color: "#e2e8f0", border: "1px solid rgba(255,255,255,.15)" },
  },
  { dark: true }
);

const ERROR_LINE = /^Program\.cs\((\d+),(\d+)\):\s*error\s+(\w+):\s*(.*)$/;

// Split compiler output into structured errors (empty when it isn't a compile failure).
function parseErrors(output) {
  return output
    .split("\n")
    .map((l) => ERROR_LINE.exec(l.trim()))
    .filter(Boolean)
    .map((m) => ({ line: +m[1], col: +m[2], code: m[3], message: m[4] }));
}

function classify(result) {
  if (!result) return null;
  if (result.ok) {
    return result.output.startsWith("✓")
      ? { kind: "ok", label: "All tests passed" }
      : { kind: "ok", label: "Ran successfully" };
  }
  const errors = parseErrors(result.output);
  if (errors.length) return { kind: "err", label: `${errors.length} compile error${errors.length > 1 ? "s" : ""}`, errors };
  if (result.output.startsWith("✗")) {
    const m = /Expected:\n([\s\S]*?)\n\nGot:\n([\s\S]*)$/.exec(result.output);
    return { kind: "warn", label: "Output doesn't match", diff: m && { expected: m[1], got: m[2] } };
  }
  return { kind: "err", label: "Program failed" };
}

// Editor + run button + output. `onRun(code)` resolves to {ok, output}.
// With `storageKey`, the code is kept in localStorage so it survives reloads.
export default function Editor({ filename, onRun, minHeight, footer, storageKey }) {
  const host = useRef(null);
  const view = useRef(null);
  const runRef = useRef(null);
  const [code, setCode] = useState(() => {
    try {
      return (storageKey && localStorage.getItem(storageKey)) || "";
    } catch {
      return "";
    }
  });
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [elapsed, setElapsed] = useState(null);

  async function run() {
    if (busy) return;
    setBusy(true);
    const started = performance.now();
    try {
      setResult(await onRun(view.current.state.doc.toString()));
    } catch (e) {
      setResult({ ok: false, output: e.message });
    } finally {
      setElapsed((performance.now() - started) / 1000);
      setBusy(false);
    }
  }
  runRef.current = run;

  useEffect(() => {
    const state = EditorState.create({
      doc: code,
      extensions: [
        lineNumbers(),
        highlightActiveLineGutter(),
        highlightActiveLine(),
        drawSelection(),
        history(),
        indentOnInput(),
        bracketMatching(),
        closeBrackets(),
        StreamLanguage.define(csharp),
        syntaxHighlighting(highlightStyle),
        EditorState.tabSize.of(4),
        keymap.of([
          { key: "Shift-Enter", run: () => (runRef.current(), true) },
          { key: "Mod-Enter", run: () => (runRef.current(), true) },
          ...closeBracketsKeymap,
          ...defaultKeymap,
          ...historyKeymap,
          indentWithTab,
        ]),
        theme,
        EditorView.updateListener.of((u) => {
          if (!u.docChanged) return;
          const text = u.state.doc.toString();
          setCode(text);
          u.view.dispatch(setDiagnostics(u.state, [])); // markers are stale once code changes
          try {
            if (storageKey) localStorage.setItem(storageKey, text);
          } catch {
            /* storage unavailable; keep in memory only */
          }
        }),
      ],
    });
    view.current = new EditorView({ state, parent: host.current });
    return () => view.current.destroy();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const status = useMemo(() => classify(result), [result]);

  // Underline compile errors in the editor.
  useEffect(() => {
    const v = view.current;
    if (!v || !status?.errors) return;
    const doc = v.state.doc;
    const diagnostics = status.errors
      .filter((e) => e.line >= 1 && e.line <= doc.lines)
      .map((e) => {
        const line = doc.line(e.line);
        const from = Math.min(line.from + Math.max(e.col - 1, 0), line.to);
        const to = Math.min(Math.max(from + 1, line.from + line.text.trimEnd().length), line.to);
        return { from, to: Math.max(to, from), severity: "error", message: `${e.code}: ${e.message}` };
      });
    v.dispatch(setDiagnostics(v.state, diagnostics));
  }, [status]);

  function jumpTo(err) {
    const v = view.current;
    if (!v || err.line > v.state.doc.lines) return;
    const line = v.state.doc.line(err.line);
    v.dispatch({
      selection: { anchor: Math.min(line.from + Math.max(err.col - 1, 0), line.to) },
      scrollIntoView: true,
    });
    v.focus();
  }

  return (
    <div className="codealong-editor" style={{ minHeight }}>
      <div className="editor-toolbar">
        <span className="editor-filename">{filename}</span>
        <button className="run-btn" onClick={run} disabled={busy} title="Run (Shift+Enter or Ctrl+Enter)">
          {busy ? "Running…" : "▶ Run"}
        </button>
      </div>
      <div className="editor-host" ref={host} />
      <div className={`output-panel${status ? ` is-${status.kind}` : ""}`}>
        <div className="output-head">
          <span className="output-label">Output</span>
          {busy && <span className="out-badge busy"><span className="spinner" /> Compiling &amp; running…</span>}
          {!busy && status && (
            <span className={`out-badge ${status.kind}`}>
              {status.kind === "ok" ? "✓" : "✕"} {status.label}
              {elapsed != null && <span className="out-time"> · {elapsed.toFixed(1)}s</span>}
            </span>
          )}
          {!busy && !status && <span className="out-hint">Shift + Enter to run</span>}
        </div>
        {status?.errors ? (
          <ul className="error-list">
            {status.errors.map((e, i) => (
              <li key={i} onClick={() => jumpTo(e)}>
                <span className="err-loc">Line {e.line}:{e.col}</span>
                <span className="err-code">{e.code}</span>
                <span className="err-msg">{e.message}</span>
              </li>
            ))}
          </ul>
        ) : status?.diff ? (
          <div className="diff-cols">
            <div>
              <div className="diff-title">Expected</div>
              <pre className="out-ok">{status.diff.expected}</pre>
            </div>
            <div>
              <div className="diff-title">Your output</div>
              <pre className="out-err">{status.diff.got}</pre>
            </div>
          </div>
        ) : (
          <pre className={result ? (status.kind === "ok" ? "out-ok" : "out-err") : "out-idle"}>
            {result ? result.output : "Run your code to see output here."}
          </pre>
        )}
      </div>
      {footer && footer({ code, setResult })}
    </div>
  );
}
