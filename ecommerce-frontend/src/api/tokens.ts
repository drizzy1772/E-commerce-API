// Keeps JWTs in localStorage and exposes them reactively.
import { reactive } from "vue";

function read(key: string): string | null {
  try { return localStorage.getItem(key); } catch { return null; }
}
function write(key: string, value: string | null) {
  try { value === null ? localStorage.removeItem(key) : localStorage.setItem(key, value); } catch { /* storage unavailable */ }
}

const state = reactive({ access: read("access"), refresh: read("refresh") });

export const tokens = {
  get access() { return state.access; },
  get refresh() { return state.refresh; },
  set(access: string, refresh: string | null) {
    state.access = access;
    state.refresh = refresh;
    write("access", access);
    write("refresh", refresh);
  },
  clear() {
    state.access = null;
    state.refresh = null;
    write("access", null);
    write("refresh", null);
  },
};
