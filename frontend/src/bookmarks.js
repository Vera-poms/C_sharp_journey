import { useSyncExternalStore } from "react";

// One bookmark per lesson, kept in localStorage. A bookmark points at a word:
// the block it sits in (data-b) and the character offset inside that block.
const KEY = "bookmarks";
const listeners = new Set();
let cache = null;

function read() {
  if (cache) return cache;
  try {
    cache = JSON.parse(localStorage.getItem(KEY)) ?? [];
  } catch {
    cache = [];
  }
  return cache;
}

function write(list) {
  cache = list;
  try {
    localStorage.setItem(KEY, JSON.stringify(list));
  } catch {
    // Storage unavailable: bookmarks still work for this session.
  }
  listeners.forEach((l) => l());
}

export function addBookmark(bm) {
  write([...read().filter((b) => b.lessonId !== bm.lessonId), bm]);
}

export function removeBookmark(lessonId) {
  write(read().filter((b) => b.lessonId !== lessonId));
}

export function useBookmarks() {
  return useSyncExternalStore(
    (cb) => (listeners.add(cb), () => listeners.delete(cb)),
    read
  );
}

// Turns the current text selection into a bookmark position, or null if it isn't a word in a block.
export function selectionToPosition(root) {
  const sel = window.getSelection();
  if (!sel || sel.isCollapsed || sel.rangeCount === 0) return null;
  const word = sel.toString().trim();
  if (!word || word.length > 40 || /\s/.test(word)) return null;
  const range = sel.getRangeAt(0);
  const el = (range.startContainer.nodeType === 1 ? range.startContainer : range.startContainer.parentElement)?.closest("[data-b]");
  if (!el || !root.contains(el)) return null;
  const pre = document.createRange();
  pre.selectNodeContents(el);
  pre.setEnd(range.startContainer, range.startOffset);
  const raw = sel.toString();
  const offset = pre.toString().length + (raw.length - raw.trimStart().length);
  return { block: el.dataset.b, offset, word, rect: range.getBoundingClientRect() };
}

// Selects the bookmarked word and scrolls to it. Returns false if it can't be found.
export function locateBookmark(root, bm) {
  const el = root.querySelector(`[data-b="${bm.block}"]`);
  if (!el) return false;
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let seen = 0;
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const len = node.nodeValue.length;
    if (bm.offset < seen + len) {
      const start = bm.offset - seen;
      const range = document.createRange();
      range.setStart(node, start);
      range.setEnd(node, Math.min(start + bm.word.length, len));
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      (node.parentElement ?? el).scrollIntoView({ block: "center", behavior: "smooth" });
      return true;
    }
    seen += len;
  }
  el.scrollIntoView({ block: "center", behavior: "smooth" });
  return true;
}
