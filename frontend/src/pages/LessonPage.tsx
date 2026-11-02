import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useLocation, useNavigate, useParams, useSearchParams } from "react-router-dom";
import { api } from "../api";
import { addBookmark, locateBookmark, useBookmarks, removeBookmark, selectionToPosition } from "../bookmarks";
import Editor from "../components/Editor";
import Terminal from "../components/Terminal";
import { Block, CodeBlock, Highlight, Inline } from "../components/Rich";
import { formatClock, formatWatched, useWatchTime } from "../watchTime";
import type { Bookmark, Lesson, Resource } from "../types";
import type { CSSProperties, PointerEvent as ReactPointerEvent } from "react";

function Reading({ lesson }: { lesson: Lesson }) {
  const ca = lesson.codealong;
  const ref = useRef<HTMLDivElement>(null);
  const [pending, setPending] = useState<ReturnType<typeof selectionToPosition>>(null);

  // Offer a bookmark button next to a freshly selected word (double-click or drag).
  function onSelect() {
    // Wait a tick so the selection has settled.
    setTimeout(() => {
      const pos = ref.current && selectionToPosition(ref.current);
      setPending(pos);
    }, 0);
  }

  function save() {
    addBookmark({
      lessonId: lesson.id,
      block: pending!.block,
      offset: pending!.offset,
      word: pending!.word,
      title: lesson.title,
      moduleNumber: lesson.module.number,
    });
    window.getSelection()?.removeAllRanges();
    setPending(null);
  }

  return (
    <div className="lesson-content reading" ref={ref} onMouseUp={onSelect} onKeyUp={onSelect}>
      <h1 data-b="title">{lesson.title}</h1>
      {lesson.subtitle && <p className="lesson-subtitle" data-b="subtitle">{lesson.subtitle}</p>}
      {lesson.reading.map((block, i) => (
        <div className="block" data-b={`r${i}`} key={i}><Block block={block} /></div>
      ))}
      {ca && (
        <section className="reading-exercises">
          <h2 data-b="ca-title">{ca.title}</h2>
          <p data-b="ca-intro">{ca.intro}</p>
          <p className="exercise-hint">Type each step into the Practice panel and run it.</p>
          {ca.steps.map((step, i) => (
            <div className="step" data-step={i + 1} key={i}>
              <h4 data-b={`s${i}-t`}>{step.title}</h4>
              <p data-b={`s${i}-b`}><Inline text={step.body} /></p>
              <div className="step-code" data-b={`s${i}-c`}><Highlight code={step.code} /></div>
            </div>
          ))}
        </section>
      )}
      {pending && (
        <button
          type="button"
          className="bookmark-pop"
          style={{ top: pending.rect.top - 38, left: pending.rect.left + pending.rect.width / 2 }}
          onMouseDown={(e) => e.preventDefault()}
          onClick={save}
        >
          🔖 Bookmark “{pending.word}”
        </button>
      )}
    </div>
  );
}

function ResourceList({ resources }: { resources: Resource[] }) {
  const groups: { source: string; items: Resource[] }[] = [];
  for (const r of resources) {
    let g = groups.find((x) => x.source === r.source);
    if (!g) groups.push((g = { source: r.source, items: [] }));
    g.items.push(r);
  }
  return groups.map((g) => (
    <div className="resource-group" key={g.source}>
      <h3>{g.source}</h3>
      {g.items.map((r) => (
        <a key={r.href} href={r.href} target="_blank" rel="noopener noreferrer" className="ms-link">↗ {r.text}</a>
      ))}
    </div>
  ));
}

function Video({ lesson }: { lesson: Lesson }) {
  const v = lesson.video!;
  const [playing, setPlaying] = useState(false);
  useEffect(() => setPlaying(false), [v.youtube_id]);
  const { total, position, ready, mountPlayer, leftForYouTube } = useWatchTime({
    lessonId: lesson.id,
    videoId: v.youtube_id,
    duration: v.duration,
  });
  return (
    <div className="lesson-content">
      <h1 className="tab-title">Video: {v.title}</h1>
      <p className="tab-intro">Watch the walkthrough, then practice in the other tabs.</p>
      <div className="video-container">
        <div className="video-frame">
          {playing ? (
            <div className="video-player" ref={mountPlayer} />
          ) : (
            <div
              className="video-poster"
              style={{ backgroundImage: `url(https://i.ytimg.com/vi/${v.youtube_id}/hqdefault.jpg)` }}
            >
              <div className="video-poster-actions">
                <a className="btn-primary" href={v.url} target="_blank" rel="noopener noreferrer" onClick={leftForYouTube}>
                  ▶ Watch on YouTube
                </a>
                <button type="button" className="btn-secondary" disabled={!ready} onClick={() => setPlaying(true)}>
                  {position > 5 ? `Resume here from ${formatClock(position)}` : "Play here"}
                </button>
              </div>
            </div>
          )}
        </div>
        <div className="video-meta">
          <div className="video-meta-item">🕑 {v.duration}</div>
          <div className="video-meta-item">🎓 {v.provider}</div>
          <div className="video-meta-item" title="Time spent watching, here or on YouTube">⏱ Watched {formatWatched(total)}</div>
          <div className="video-meta-item">
            <a href={v.url} target="_blank" rel="noopener noreferrer" onClick={leftForYouTube}>Watch on YouTube ↗</a>
          </div>
        </div>
      </div>
    </div>
  );
}

function Resources({ lesson }: { lesson: Lesson }) {
  return (
    <div className="lesson-content">
      <h1 className="tab-title">Resources</h1>
      <p className="tab-intro">Keep learning with official docs, W3Schools tutorials, and videos.</p>
      <div className="resources">
        <ResourceList resources={lesson.resources} />
      </div>
    </div>
  );
}

function Lab({ lesson, onSubmitted }: { lesson: Lesson; onSubmitted: () => void }) {
  const lab = lesson.lab!;
  const [showHint, setShowHint] = useState(false);
  return (
    <div className="lesson-content reading">
      <div className="lab-header">
        <h2>{lab.title}</h2>
        <span className="lab-diff">{lab.difficulty}</span>
      </div>
      <p className="lab-description">{lab.description}</p>

      <div className="lab-requirements">
        <h4>Requirements</h4>
        <ol>
          {lab.requirements.map((r, i) => <li key={i}><Inline text={r} /></li>)}
        </ol>
      </div>

      <div className="expected-label">Expected output:</div>
      <div className="code-block expected"><code>{lab.expected_output}</code></div>

      <div className="lab-editor-wrap">
        <Editor
          filename={lab.filename}
          minHeight={520}
          storageKey={`lab:${lesson.id}`}
          onRun={(code) => api.runLab(lesson.id, code)}
          footer={({ code, setResult }) => (
            <>
              {showHint && <pre className="hint-box">{lab.hint}</pre>}
              <div className="submit-bar">
                <button className="hint-btn" onClick={() => setShowHint((s) => !s)}>
                  {showHint ? "Hide Hint" : "Show Hint"}
                </button>
                <button
                  className="submit-btn"
                  onClick={async () => {
                    try {
                      setResult(await api.submitLab(lesson.id, code));
                      onSubmitted();
                    } catch (e) {
                      setResult({ ok: false, output: (e as Error).message });
                    }
                  }}
                >
                  Submit Solution
                </button>
              </div>
            </>
          )}
        />
      </div>
    </div>
  );
}

// Saved reading positions. Clicking one jumps to the word and removes the bookmark.
function Bookmarks() {
  const bookmarks = useBookmarks();
  const navigate = useNavigate();
  return (
    <div className="sidebar-bookmarks">
      <h3>Bookmarks</h3>
      {bookmarks.length === 0 && (
        <p className="bookmark-empty">Select a word in the reading, then click “Bookmark” to mark your place.</p>
      )}
      {bookmarks.map((b) => (
        <button
          key={b.lessonId}
          type="button"
          className="bookmark-chip"
          title={`Module ${b.moduleNumber} · ${b.title}`}
          onClick={() => navigate(`/lessons/${b.lessonId}`, { state: { bookmark: b } })}
        >
          <span className="bookmark-word">🔖 {b.word}</span>
          <span className="bookmark-where">{b.title}</span>
        </button>
      ))}
    </div>
  );
}

const DEFAULT_PRACTICE = 460;
const MIN_PRACTICE = 320;

export default function LessonPage() {
  const { lessonId } = useParams();
  const [params, setParams] = useSearchParams();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showPractice, setShowPractice] = useState(true);
  const [mode, setMode] = useState("code");
  const [practiceWidth, setPracticeWidth] = useState(() => {
    try {
      const w = Number(localStorage.getItem("practice-width"));
      return w >= MIN_PRACTICE ? w : DEFAULT_PRACTICE;
    } catch {
      return DEFAULT_PRACTICE;
    }
  });

  // Drag the panel's left edge; the panel is on the right, so moving left widens it.
  function startResize(e: ReactPointerEvent) {
    e.preventDefault();
    const startX = e.clientX;
    const startW = practiceWidth;
    const max = Math.max(MIN_PRACTICE, window.innerWidth - 360);
    let width = startW;
    const onMove = (ev: PointerEvent) => {
      width = Math.round(Math.min(max, Math.max(MIN_PRACTICE, startW + startX - ev.clientX)));
      setPracticeWidth(width);
    };
    const onUp = () => {
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      document.body.classList.remove("resizing");
      try {
        localStorage.setItem("practice-width", String(width));
      } catch {
        /* not persisted */
      }
    };
    document.body.classList.add("resizing");
    window.addEventListener("pointermove", onMove);
    window.addEventListener("pointerup", onUp);
  }

  const load = useCallback(
    () => api.lesson(lessonId!).then(setLesson).catch((e) => setError(e.message)),
    [lessonId]
  );

  useEffect(() => {
    // Keep the previous lesson on screen while the next one loads; clearing it flashed "Loading…".
    setError(null);
    load();
  }, [load]);

  // Arriving from a nav-bar bookmark: jump to the word, then drop the bookmark to free its slot.
  const location = useLocation();
  const bookmark = location.state?.bookmark as Bookmark | undefined;
  const onReading = !params.get("tab") || params.get("tab") === "reading";
  useEffect(() => {
    if (!bookmark || !lesson || lesson.id !== bookmark.lessonId || !onReading) return;
    const root = document.querySelector<HTMLElement>(".lesson-content.reading");
    if (!root) return;
    locateBookmark(root, bookmark);
    removeBookmark(bookmark.lessonId);
    navigate(`${location.pathname}${location.search}`, { replace: true, state: null });
  }, [bookmark, lesson, onReading, location.pathname, location.search, navigate]);

  if (error) return <p className="status-msg">Could not load lesson: {error}</p>;
  if (!lesson) return <p className="status-msg">Loading…</p>;

  const tabs = [
    { id: "reading", label: "Reading", show: true },
    { id: "video", label: "Video", show: !!lesson.video },
    { id: "lab", label: "Lab", show: !!lesson.lab },
    { id: "resources", label: "Resources", show: lesson.resources.length > 0 },
  ].filter((t) => t.show);
  const tab = tabs.find((t) => t.id === params.get("tab"))?.id ?? "reading";

  async function toggleComplete() {
    if (!lesson) return;
    await (lesson.completed ? api.uncomplete(lesson.id) : api.complete(lesson.id));
    load();
  }

  return (
    <div className="lesson-view">
      <aside className="sidebar">
        <div className="sidebar-header">
          <Link to="/" className="sidebar-back">← All Modules</Link>
          <h2>Module {lesson.module.number}: {lesson.module.title}</h2>
        </div>
        <div className="sidebar-lessons">
          {lesson.module.lessons.map((l) => (
            <div
              key={l.id}
              className={`sidebar-lesson${l.id === lesson.id ? " active" : ""}`}
              onClick={() => navigate(`/lessons/${l.id}`)}
            >
              <div className={`check${l.completed ? " done" : ""}`}>{l.completed && "✓"}</div>
              <span>{l.label} {l.title}</span>
            </div>
          ))}
        </div>
        <Bookmarks />
      </aside>

      <main className="lesson-main" key={lesson.id}>
        <div className="lesson-topbar">
          {tabs.map((t) => (
            <div
              key={t.id}
              className={`tab${t.id === tab ? " active" : ""}`}
              onClick={() => setParams(t.id === "reading" ? {} : { tab: t.id })}
            >
              {t.label}
            </div>
          ))}
          <button className={`complete-btn${lesson.completed ? " done" : ""}`} onClick={toggleComplete}>
            {lesson.completed ? "✓ Completed" : "Mark complete"}
          </button>
        </div>

        {/* Stays mounted (just hidden) on other tabs so the editor isn't rebuilt, which made the page blink. */}
        <div
          className={`lesson-split${showPractice ? "" : " no-practice"}`}
          style={
            tab === "reading" || tab === "video"
              ? ({ "--practice-width": `${practiceWidth}px` } as CSSProperties)
              : { display: "none" }
          }
        >
          <div className="lesson-split-main">
            {tab === "reading" && <Reading lesson={lesson} />}
            {tab === "video" && <Video lesson={lesson} />}
          </div>
          {showPractice ? (
            <aside className="practice-panel">
              <div
                className="practice-resizer"
                role="separator"
                aria-orientation="vertical"
                aria-label="Resize practice panel"
                onPointerDown={startResize}
                onDoubleClick={() => setPracticeWidth(DEFAULT_PRACTICE)}
              />
              <div className="practice-header">
                <span>Practice — code while you {tab === "video" ? "watch" : "read"}</span>
                <button type="button" className="practice-toggle" onClick={() => setShowPractice(false)}>
                  Hide
                </button>
              </div>
              <div className="practice-modes">
                {[["code", "C# Editor"], ["cli", "Terminal"]].map(([id, label]) => (
                  <button
                    key={id}
                    type="button"
                    className={`practice-mode${mode === id ? " active" : ""}`}
                    onClick={() => setMode(id)}
                  >
                    {label}
                  </button>
                ))}
              </div>
              {/* Both stay mounted so switching keeps the code and the terminal history. */}
              <div className="practice-body" style={mode === "code" ? undefined : { display: "none" }}>
                <Editor
                  filename="Scratch.cs"
                  storageKey={`practice:${lesson.id}`}
                  onRun={(code) => api.runScratch(lesson.id, code)}
                />
              </div>
              <div className="practice-body" style={mode === "cli" ? undefined : { display: "none" }}>
                <Terminal onRun={(session, cmd) => api.runCli(lesson.id, session, cmd)} />
              </div>
            </aside>
          ) : (
            <button type="button" className="practice-open" onClick={() => setShowPractice(true)}>
              {"</>"} Practice
            </button>
          )}
        </div>
        {tab === "lab" && <Lab lesson={lesson} onSubmitted={load} />}
        {tab === "resources" && <Resources lesson={lesson} />}
      </main>
    </div>
  );
}
