import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "./api.js";

const FLUSH_EVERY = 5; // seconds of watching between reports to the server (a refresh loses at most this much)
const FALLBACK_CAP = 2 * 3600; // longest YouTube visit we'll credit when the duration is unknown

// "12:34", "1:02:03" or "12 min" -> seconds; 0 when unparseable.
export function parseDuration(text) {
  if (!text) return 0;
  if (text.includes(":")) return text.split(":").reduce((t, p) => t * 60 + (parseInt(p, 10) || 0), 0);
  const m = text.match(/\d+/);
  return m ? parseInt(m[0], 10) * 60 : 0;
}

export function formatWatched(seconds) {
  const s = Math.floor(seconds);
  if (s < 60) return `${s}s`;
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  return h ? `${h}h ${m}m` : `${m}m ${String(s % 60).padStart(2, "0")}s`;
}

export function formatClock(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = String(seconds % 60).padStart(2, "0");
  return h ? `${h}:${String(m).padStart(2, "0")}:${s}` : `${m}:${s}`;
}

let apiPromise;
function loadYouTubeApi() {
  if (window.YT?.Player) return Promise.resolve(window.YT);
  apiPromise ??= new Promise((resolve, reject) => {
    const prev = window.onYouTubeIframeAPIReady;
    window.onYouTubeIframeAPIReady = () => {
      prev?.();
      resolve(window.YT);
    };
    const s = document.createElement("script");
    s.src = "https://www.youtube.com/iframe_api";
    s.onerror = () => {
      apiPromise = undefined;
      reject(new Error("YouTube API failed to load"));
    };
    document.head.appendChild(s);
  });
  return apiPromise;
}

// Sending the learner to YouTube is remembered in localStorage and settled by a listener that lives
// outside React, so it still counts if they come back while on another lesson tab.
const AWAY_KEY = "watch-away";

function settleAway() {
  if (document.visibilityState === "hidden") return;
  let away;
  try {
    away = JSON.parse(localStorage.getItem(AWAY_KEY));
    localStorage.removeItem(AWAY_KEY);
  } catch {
    return;
  }
  if (!away) return;
  const elapsed = Math.round((Date.now() - away.t) / 1000);
  if (elapsed <= 5) return;
  api
    .addWatchTime(away.lessonId, Math.min(elapsed, away.cap || FALLBACK_CAP), null)
    .then(() => window.dispatchEvent(new Event("watch-updated")))
    .catch(() => {});
}
window.addEventListener("focus", settleAway);
document.addEventListener("visibilitychange", settleAway);

/**
 * Tracks time spent on a lesson's video, and where the embedded player got to.
 *  - Embedded: counts the time the YouTube player reports PLAYING (wall clock, so background tabs are fair).
 *  - On YouTube: YouTube can't tell us what happens in its tab, so we credit the time between
 *    clicking the link and coming back to this site (capped at the video's length).
 * The server is the source of truth: totals and position are fetched whenever the Video tab mounts.
 */
export function useWatchTime({ lessonId, videoId, duration }) {
  const [total, setTotal] = useState(0);
  const [position, setPosition] = useState(0);
  const [ready, setReady] = useState(false);
  const pending = useRef(0);
  const startAt = useRef(0); // where a newly created player starts
  const lastPos = useRef(null); // last known playback position, null = nothing new to save
  const player = useRef(null);
  const cleanup = useRef(null);

  const refresh = useCallback(
    () =>
      api
        .watchTime(lessonId)
        .then((w) => {
          setTotal(w.watched_seconds + pending.current);
          setPosition(w.position_seconds);
          startAt.current = w.position_seconds;
          lastPos.current = null;
          setReady(true);
        })
        .catch(() => setReady(true)),
    [lessonId]
  );

  useEffect(() => {
    setReady(false);
    refresh();
    window.addEventListener("watch-updated", refresh);
    return () => window.removeEventListener("watch-updated", refresh);
  }, [refresh]);

  const flush = useCallback(
    (keepalive = false) => {
      const p = player.current;
      if (p?.getCurrentTime) {
        const t = Math.floor(p.getCurrentTime());
        if (t > 0) lastPos.current = t;
      }
      const seconds = pending.current;
      const pos = lastPos.current;
      if (!seconds && pos === null) return;
      pending.current = 0;
      lastPos.current = null;
      api.addWatchTime(lessonId, seconds, pos, keepalive).catch(() => {
        pending.current += seconds; // retry with the next flush
        lastPos.current ??= pos;
      });
    },
    [lessonId]
  );

  const credit = useCallback(
    (seconds) => {
      pending.current += seconds;
      setTotal((t) => t + seconds);
      if (pending.current >= FLUSH_EVERY) flush();
    },
    [flush]
  );

  // Report leftovers when leaving the lesson, hiding the tab or closing it.
  useEffect(() => {
    const onHide = () => document.visibilityState === "hidden" && flush(true);
    const onPageHide = () => flush(true);
    window.addEventListener("pagehide", onPageHide);
    document.addEventListener("visibilitychange", onHide);
    return () => {
      window.removeEventListener("pagehide", onPageHide);
      document.removeEventListener("visibilitychange", onHide);
      flush(true);
    };
  }, [flush]);

  // Embedded player: credit elapsed wall-clock time while it is playing.
  const mountPlayer = useCallback(
    (host) => {
      cleanup.current?.(); // flushes using the old player's position, so run before destroy
      cleanup.current = null;
      player.current?.destroy?.();
      player.current = null;
      if (!host) return;
      let timer;
      let last = 0;
      let dead = false;
      const tick = () => {
        const whole = Math.floor((Date.now() - last) / 1000);
        if (whole > 0) {
          last += whole * 1000;
          credit(whole);
        }
      };
      const stop = () => {
        if (timer) tick();
        clearInterval(timer);
        timer = undefined;
        flush();
      };
      const target = document.createElement("div");
      host.replaceChildren(target);
      loadYouTubeApi()
        .then((YT) => {
          if (dead) return;
          player.current = new YT.Player(target, {
            videoId,
            playerVars: { rel: 0, autoplay: 1, start: startAt.current },
            events: {
              onStateChange: (e) => {
                if (e.data === YT.PlayerState.PLAYING) {
                  if (!timer) {
                    last = Date.now();
                    timer = setInterval(tick, 1000);
                  }
                } else {
                  stop();
                }
              },
            },
          });
        })
        .catch(() => {});
      cleanup.current = () => {
        dead = true;
        stop();
      };
    },
    [videoId, credit, flush]
  );

  const leftForYouTube = useCallback(() => {
    try {
      if (!localStorage.getItem(AWAY_KEY)) {
        localStorage.setItem(
          AWAY_KEY,
          JSON.stringify({ lessonId, t: Date.now(), cap: parseDuration(duration) })
        );
      }
    } catch {
      /* storage blocked: that visit just isn't counted */
    }
  }, [lessonId, duration]);

  return { total, position, ready, mountPlayer, leftForYouTube };
}
