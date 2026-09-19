





import { API_URL } from "./config";
import AuthManager from "./Auth";

export class HttpError extends Error {
    constructor(public status: number, message: string, public data?: any) {
        super(message);
        this.name = "HttpError";
    }
}

export class NetworkError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "NetworkError";
    }
}

export default class HttpClient {
    private authManager: AuthManager;
    constructor(authManager: AuthManager) {
        this.authManager = authManager;
    }

    async request<T>(path: string, options: RequestInit = {}): Promise<T>{
        const authState = this.authManager.getState();
        if (!authState.isAuthenticated) {
            throw new HttpError(401, "Unauthorized: No valid session");
        }

        const headers = new Headers(options.headers || {});

        const token = this.authManager.getToken();
        if (token) {
            headers.set("Authorization", `Bearer ${token}`);
        }

        let response: Response;

        try {
            response = await fetch(`${API_URL}${path}`, {
                ... options,
                headers: headers
            });
        }catch(error) {
            throw new NetworkError(error instanceof Error ? error.message : "Network failure");
        }
        if (response.status === 401) {
            this.authManager.logout();
            throw new HttpError(401, "Session expired");
        }
            
            if (!response.ok) {
                let errorMessage = `HTTP Error ${response.status}`;
                let errorData = null;

                const contentType = response.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    errorData = await response.json();
                    errorMessage = errorData?.detail || JSON.stringify(errorData);

                    

                }
                throw new HttpError(response.status, errorMessage, errorData);
            }

            if (response.status === 204) {
                return null as unknown as T;
            }
            
            const contentType = response.headers.get("content-type");
              
            if (contentType && contentType.includes("application/json")) {
                return await response.json();
            }

            return await response.text() as unknown as T;
            }
        }