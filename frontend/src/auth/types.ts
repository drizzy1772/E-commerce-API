


//

export interface JWTPayload {
    sub: string;
    role: string;
    exp: number;
}

//authstate
export interface AuthState {
    isAuthenticated: boolean;
    role: string | null;
}

