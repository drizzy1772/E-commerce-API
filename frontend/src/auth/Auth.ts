

import { AuthState } from "./types";
import { decodeJWT } from "./jwt";
import { API_URL } from "./config";

export default class AuthManager {

    private readonly TOKEN_KEY = "access_token";

    private listeners: Array<(state: AuthState) => void> = [];

    async login(email: string, password: string): Promise<void> {
        const response = await fetch(`${API_URL}/login`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ email, password})
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
        this.notify({ isAuthenticated: false, role: null });

    }


    getToken(): string | null {
        return localStorage.getItem(this.TOKEN_KEY)
    }


    getState(): AuthState {
        
        const token = localStorage.getItem(this.TOKEN_KEY);

        if (!token) {
            return { isAuthenticated: false, role: null};
        }
        
        const payload = decodeJWT(token);
    
        if (!payload) {
            return { isAuthenticated: false, role: null};
        }

        const currentTime = Date.now() / 1000;

        if (payload.exp < currentTime) {
            this.logout();
            
            return { isAuthenticated: false, role: null};
        }
        
        return { isAuthenticated: true, role: payload.role};
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

