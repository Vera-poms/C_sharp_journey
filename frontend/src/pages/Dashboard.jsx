import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api.js";
import { formatWatched } from "../watchTime.js";

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [modules, setModules] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    Promise.all([api.stats(), api.modules()])
      .then(([s, m]) => {
        setStats(s);
        setModules(m);
      })
      .catch((e) => setError(e.message));
  }, []);

  if (error) return <div className="dashboard"><p className="status-msg">Could not load courses: {error}</p></div>;
  if (!stats || !modules) return <div className="dashboard"><p className="status-msg">Loading…</p></div>;

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Your C# Journey</h1>
        <p>From your first line of code to building desktop applications. Learn with in-depth reading, guided code-along exercises, videos, and hands-on labs.</p>
      </div>

      <div className="progress-overview">
        <div className="stat-card">
          <div className="stat-value accent">{stats.lessons_completed} / {stats.lessons_total}</div>
          <div className="stat-label">Lessons completed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value amber">{stats.modules_started} / {stats.modules_total}</div>
          <div className="stat-label">Modules started</div>
        </div>
        <div className="stat-card">
          <div className="stat-value green">{stats.labs_passed}</div>
          <div className="stat-label">Labs passed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value accent">{formatWatched(stats.watch_seconds)}</div>
          <div className="stat-label">Video time watched</div>
        </div>
      </div>

      <div className="modules-heading">All Modules</div>

      {modules.map((m) => (
        <Link key={m.id} to={`/modules/${m.id}`} className="module-card">
          <div className="module-num">{m.number}</div>
          <div className="module-info">
            <h3>{m.title}</h3>
            <p>{m.description}</p>
          </div>
          <div className="module-meta">
            <div className="lessons-count">{m.lesson_count} lessons</div>
            <div className="module-progress-bar">
              <div className="fill" style={{ width: `${(m.completed_count / m.lesson_count) * 100}%` }} />
            </div>
          </div>
        </Link>
      ))}
    </div>
  );
}
