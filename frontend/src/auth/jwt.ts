

import { JWTPayload } from "./types";


export function decodeJWT(token: string): JWTPayload | null {
    try {
        const base64Url = token.split(".")[1];
        
        let base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");

        while (base64.length % 4 !== 0) {
            base64 = base64 + "=";
        }
        
        const jsonString = decodeURIComponent(
            atob(base64)
                .split('')
                .map(function(c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                })
                .join("")

        );

        const payload = JSON.parse(jsonString);

        return payload;

    } catch (e) {
        return null;
    }
}   