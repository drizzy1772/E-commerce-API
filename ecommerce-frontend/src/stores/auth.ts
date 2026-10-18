




import { computed } from "vue";
import { defineStore } from "pinia";
import { request } from "../api/http";
import { tokens } from "../api/tokens";

interface TokenPair { access_token: string; refresh_token?: string }

export const useAuth = defineStore("auth", () => {
  const isLoggedIn = computed(() => !!tokens.access);

  async function login(email: string, password: string) {
    const data = await request<TokenPair>("/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: new URLSearchParams({ username: email, password }),
      
    });
    tokens.set(data.access_token, data.refresh_token ?? null);
  }


  async function register(email: string, password: string) {
    await request("/auth/register", { method: "POST", body: JSON.stringify({ email, password }) });
  }

  function logout() {
    tokens.clear();
  }

  return { isLoggedIn, login, register, logout };
});
