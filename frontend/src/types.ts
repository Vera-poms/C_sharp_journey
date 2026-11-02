export interface Stats {
  lessons_completed: number;
  lessons_total: number;
  modules_started: number;
  modules_total: number;
  labs_passed: number;
  watch_seconds: number;
}

export interface ModuleSummary {
  id: number | string;
  number: number;
  title: string;
  description: string;
  lesson_count: number;
  completed_count: number;
}

export interface LessonRef {
  lesson_id: number | string;
}

export interface ReadingBlock {
  type: "h2" | "p" | "code" | "callout" | "link";
  text?: string;
  code?: string;
  kind?: "note" | "tip" | "warn";
  href?: string;
}

export interface CodealongStep {
  title: string;
  body: string;
  code: string;
}

export interface Codealong {
  title: string;
  intro: string;
  steps: CodealongStep[];
}

export interface Video {
  youtube_id: string;
  title: string;
  url: string;
  duration: string;
  provider: string;
}

export interface Lab {
  title: string;
  difficulty: string;
  description: string;
  requirements: string[];
  expected_output: string;
  filename: string;
  hint: string;
}

export interface Resource {
  source: string;
  href: string;
  text: string;
}

export interface SidebarLesson {
  id: number | string;
  label: string;
  title: string;
  completed: boolean;
}

export interface Lesson {
  id: number | string;
  title: string;
  subtitle?: string;
  completed: boolean;
  module: { number: number; title: string; lessons: SidebarLesson[] };
  reading: ReadingBlock[];
  codealong?: Codealong | null;
  video?: Video | null;
  lab?: Lab | null;
  resources: Resource[];
}

export interface WatchTime {
  watched_seconds: number;
  position_seconds: number;
}

export interface RunResult {
  ok: boolean;
  output: string;
}

export interface CliResult extends RunResult {
  cwd: string;
}

export interface Bookmark {
  lessonId: number | string;
  block: string;
  offset: number;
  word: string;
  title: string;
  moduleNumber: number;
}
