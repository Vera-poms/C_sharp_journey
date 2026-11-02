import type { CliResult, Lesson, LessonRef, ModuleSummary, RunResult, Stats, WatchTime } from "./types";

async function request<T = unknown>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`${options.method || "GET"} ${path} failed (${res.status})`);
  return (res.status === 204 ? null : res.json()) as Promise<T>;
}

const post = <T>(path: string, body?: unknown) =>
  request<T>(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });

type Id = number | string;

export const api = {
  stats: () => request<Stats>("/stats"),
  modules: () => request<ModuleSummary[]>("/modules"),
  startModule: (id: string) => request<LessonRef>(`/modules/${id}/start`),
  nextLesson: () => request<LessonRef>("/next-lesson"),
  lesson: (id: Id) => request<Lesson>(`/lessons/${id}`),
  complete: (id: Id) => post<unknown>(`/lessons/${id}/complete`),
  uncomplete: (id: Id) => request(`/lessons/${id}/complete`, { method: "DELETE" }),
  watchTime: (id: Id) => request<WatchTime>(`/lessons/${id}/watch`),
  addWatchTime: (id: Id, seconds: number, position: number | null, keepalive = false) =>
    request(`/lessons/${id}/watch`, {
      method: "POST",
      body: JSON.stringify({ seconds, position }),
      keepalive,
    }),
  runCodealong: (id: Id, code: string) => post<RunResult>(`/lessons/${id}/codealong/run`, { code }),
  runScratch: (id: Id, code: string) => post<RunResult>(`/lessons/${id}/scratch/run`, { code }),
  runCli: (id: Id, session: string, command: string) => post<CliResult>(`/lessons/${id}/cli/run`, { session, command }),
  runLab: (id: Id, code: string) => post<RunResult>(`/lessons/${id}/lab/run`, { code }),
  submitLab: (id: Id, code: string) => post<RunResult>(`/lessons/${id}/lab/submit`, { code }),
};
