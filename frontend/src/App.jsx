import { useEffect } from "react";
import { Link, NavLink, Route, Routes, useNavigate, useParams } from "react-router-dom";
import { api } from "./api.js";
import Dashboard from "./pages/Dashboard.jsx";
import LessonPage from "./pages/LessonPage.jsx";

// Resolves a module/playground link to the first unfinished lesson.
function Redirect({ load }) {
  const navigate = useNavigate();
  const { moduleId } = useParams();
  useEffect(() => {
    load(moduleId)
      .then(({ lesson_id }) => navigate(`/lessons/${lesson_id}`, { replace: true }))
      .catch(() => navigate("/", { replace: true }));
  }, [load, moduleId, navigate]);
  return null;
}

export default function App() {
  return (
    <>
      <nav className="topnav">
        <Link to="/" className="logo">
          <span className="dot" />
          C# Journey
        </Link>
        <div className="nav-links">
          <NavLink to="/" end>Modules</NavLink>
          <NavLink to="/playground">Playground</NavLink>
        </div>
      </nav>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/modules/:moduleId" element={<Redirect load={api.startModule} />} />
        <Route path="/playground" element={<Redirect load={api.nextLesson} />} />
        <Route path="/lessons/:lessonId" element={<LessonPage />} />
        <Route path="*" element={<Dashboard />} />
      </Routes>
    </>
  );
}
