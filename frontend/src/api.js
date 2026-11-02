async function request(path, options = {}) {
  const res = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`${options.method || "GET"} ${path} failed (${res.status})`);
  return res.status === 204 ? null : res.json();
}

const post = (path, body) =>
  request(path, { method: "POST", body: body ? JSON.stringify(body) : undefined });

export const api = {
  stats: () => request("/stats"),
  modules: () => request("/modules"),
  startModule: (id) => request(`/modules/${id}/start`),
  nextLesson: () => request("/next-lesson"),
  lesson: (id) => request(`/lessons/${id}`),
  complete: (id) => post(`/lessons/${id}/complete`),
  uncomplete: (id) => request(`/lessons/${id}/complete`, { method: "DELETE" }),
  watchTime: (id) => request(`/lessons/${id}/watch`),
  addWatchTime: (id, seconds, position, keepalive = false) =>
    request(`/lessons/${id}/watch`, {
      method: "POST",
      body: JSON.stringify({ seconds, position }),
      keepalive,
    }),
  runCodealong: (id, code) => post(`/lessons/${id}/codealong/run`, { code }),
  runScratch: (id, code) => post(`/lessons/${id}/scratch/run`, { code }),
  runCli: (id, session, command) => post(`/lessons/${id}/cli/run`, { session, command }),
  runLab:(id, code) => post(`/lessons/${id}/lab/run`, { code }),
  submitLab: (id, code) => post(`/lessons/${id}/lab/submit`, { code }),
};
