import { Fragment } from "react";

// Inline markup used in lesson text: `code` and **bold**.
export function Inline({ text }) {
  return text.split(/(`[^`]+`|\*\*[^*]+\*\*)/g).map((part, i) => {
    if (part.startsWith("`")) return <code key={i}>{part.slice(1, -1)}</code>;
    if (part.startsWith("**")) return <strong key={i}>{part.slice(2, -2)}</strong>;
    return <Fragment key={i}>{part}</Fragment>;
  });
}

const KEYWORDS = new Set([
  "int", "long", "short", "byte", "sbyte", "uint", "ulong", "ushort", "double", "float", "decimal",
  "string", "char", "bool", "object", "dynamic", "void", "var", "true", "false", "null",
  "new", "if", "else", "for", "foreach", "in", "while", "do", "switch", "case", "default", "break",
  "continue", "return", "goto", "try", "catch", "finally", "throw", "when",
  "class", "struct", "record", "interface", "enum", "namespace", "using", "global",
  "public", "private", "protected", "internal", "static", "readonly", "const", "sealed", "abstract",
  "virtual", "override", "partial", "required", "init", "get", "set", "this", "base",
  "is", "as", "not", "and", "or", "with", "async", "await", "yield", "out", "ref", "params",
  "delegate", "event", "where", "lock", "typeof", "nameof", "operator", "implicit", "explicit",
  "from", "select", "orderby", "group", "by", "into", "join", "let",
]);
const TOKEN = /(\/\/.*|\$?"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*'|\b\d[\d_]*(?:\.\d+)?[fm]?\b|\b[A-Za-z_]\w*\b)/g;

// Small C# highlighter, enough for lesson snippets.
export function Highlight({ code }) {
  return code.split(TOKEN).map((tok, i) => {
    if (tok.startsWith("//")) return <span key={i} className="cm">{tok}</span>;
    if (/^\$?["']/.test(tok)) return <span key={i} className="str">{tok}</span>;
    if (/^\d/.test(tok)) return <span key={i} className="num">{tok}</span>;
    if (KEYWORDS.has(tok)) return <span key={i} className="kw">{tok}</span>;
    return <Fragment key={i}>{tok}</Fragment>;
  });
}

export function CodeBlock({ code }) {
  return (
    <div className="code-block">
      <span className="lang-tag">C#</span>
      <code><Highlight code={code} /></code>
    </div>
  );
}

const CALLOUT_ICONS = { note: "ⓘ", tip: "💡", warn: "⚠" };

export function Block({ block }) {
  switch (block.type) {
    case "h2":
      return <h2><Inline text={block.text} /></h2>;
    case "p":
      return <p><Inline text={block.text} /></p>;
    case "code":
      return <CodeBlock code={block.code} />;
    case "callout":
      return (
        <div className={`callout callout-${block.kind}`}>
          <span className="callout-icon">{CALLOUT_ICONS[block.kind]}</span>
          <div><Inline text={block.text} /></div>
        </div>
      );
    case "link":
      return (
        <a href={block.href} target="_blank" rel="noopener noreferrer" className="ms-link">
          ↗ <Inline text={block.text} />
        </a>
      );
    default:
      return null;
  }
}
