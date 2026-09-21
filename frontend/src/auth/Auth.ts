

import type { AuthState } from "./types";
import { decodeJWT } from "./jwt";
import { API_URL } from "../config";

export default class AuthManager {

    private readonly TOKEN_KEY = "access_token";

    private listeners: Array<(state: AuthState) => void> = [];

    async login(email: string, password: string): Promise<void> {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: new URLSearchParams({ username: email, password })
        });

        if (!response.ok) {
            const errorData = await response.json();
            const errorMessage = errorData.detail || "Login failed";
            throw new Error(errorMessage);
        }

        const data = await response.json();
        const token = data.access_token;

        if (typeof token !== "string") {
            throw new Error("Invalid token format")

        }

        localStorage.setItem(this.TOKEN_KEY, token);

        this.notify(this.getState());

    }

    logout(): void {
        const token = this.getToken()
        if (!token) {
            return
        } 

        localStorage.removeItem(this.TOKEN_KEY);
        this.notify({ isAuthenticated: false, token: null, role: null });

    }


    getToken(): string | null {
        return localStorage.getItem(this.TOKEN_KEY)
    }


    getState(): AuthState {
        
        const token = localStorage.getItem(this.TOKEN_KEY);

        if (!token) {
            return { isAuthenticated: false, token: null, role: null};
        }
        
        const payload = decodeJWT(token);
    
        if (!payload) {
            return { isAuthenticated: false, token: null, role: null};
        }

        const currentTime = Date.now() / 1000;

        if (payload.exp < currentTime) {
            this.logout();
            
            return { isAuthenticated: false, token: null, role: null};
        }
        
        return { isAuthenticated: true, token, role: payload.role ?? null};
    }

    onChange(callback: (state: AuthState) => void): void {
        this.listeners.push(callback);
    }
    private notify(state: AuthState): void {
        for (const listener of this.listeners) {
            listener(state);
        }
    }
}
