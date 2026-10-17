

import { HttpClient } from "../api/HttpClient";


//webpage response and type
export type ViewFunction = (container: HTMLElement, httpClient: HttpClient, router: Router) => (() => void) | void;


export class Router {
    private container: HTMLElement;
    private httpClient: HttpClient;
    private routes: Map<string, ViewFunction>;

private currentCleanup: (() => void) | null;


//back and forward pages

constructor(container: HTMLElement, httpClient: HttpClient) {
    this.container = container;
    this.httpClient = httpClient;
    this.routes = new Map();
    this.currentCleanup = null;

    window.addEventListener("popstate", () => {
        this.navigate(window.location.pathname, false);
    });
}

addRoute(path: string, view: ViewFunction) {
    this.routes.set(path, view);
}

//transitions

navigate(path: string, pushHistory = true) {
    const getView = this.routes.get(path);

    if (!getView) {
        console.error("Route not found");
        return;
    }

    if (pushHistory) {
        window.history.pushState({}, "", path);
    }

    if (this.currentCleanup) {
        this.currentCleanup();
    }


    this.currentCleanup = getView(
        this.container,
        this.httpClient,
        this
        ) || null;
    }
}
