


//

export interface JWTPayload {
    sub: string;
    exp: number;
    role?: string;
}

//authstate
export interface AuthState {
    isAuthenticated: boolean;
    token: string | null;
    role: string | null;
}

