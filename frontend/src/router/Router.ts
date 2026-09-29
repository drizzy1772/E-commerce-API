


import AuthManager from "../auth/Auth";

import type { RouteDefinition } from "./routes";

export default class Router{
    private routes: RouteDefinition[] = [];
    private authManager: AuthManager;
    private container: HTMLElement;

    private currentUnmount: (() => void ) | void = undefined;

    constructor(authManager: AuthManager, container: HTMLElement) {
        this.authManager = authManager;
        this.container = container;

        window.addEventListener('popstate', () => {
            this.navigate(window.location.pathname, true);
        });

        this.authManager.onChange((state) => {
            const currentRoute = this.resolve(window.location.pathname);
            if (currentRoute && currentRoute.requiresAuth && !state.isAuthenticated){
                this.navigate("/login");
            }
        });

        document.body.addEventListener('click', (e: MouseEvent) => {
            const target = e.target as Element;
            const link = target.closest("a[data-link]") as HTMLAnchorElement;

            if (link &&!e.ctrlKey  && !e.metaKey && e.button === 0) {
                e.preventDefault();
                this.navigate(link.pathname);
            }
        })
    }

        register(route: RouteDefinition): void {
            this.routes.push(route);
        }

        private resolve(path: string): RouteDefinition | undefined {
            const normalizedPath = path.endsWith("/") && path !== "/" ? path.slice(0, -1) : path;
            return this.routes.find(route => route.path === normalizedPath);
        }

        navigate(path: string, skipPushState = false, replaceState = false): void {
            const route = this.resolve(path);
            const authState = this.authManager.getState();

            if (route && route.requiresAuth && !authState.isAuthenticated) {
                this.navigate("/login", false, true);
                return;
            }

            // 404 error work
            if (route && route.allowedRoles) {
                if (!authState.role || !route.allowedRoles.includes(authState.role)) {
                    console.warn("403 Forbidden");

                    this.navigate("/", false, true);
                    return;
                }  
            }

            if (!route) {
                if (this.currentUnmount) {
                    this.currentUnmount();
                    this.currentUnmount = undefined;
                }
                this.container.innerHTML = "<h2>Error 404 - Page not found</h2>";
                return;
            }

            if (!skipPushState && path !== window.location.pathname) {
                if (replaceState === true) {
                    window.history.replaceState({}, "", path);
                } else {
                    window.history.pushState({}, "", path);
                }
            }

            if (this.currentUnmount) {
                this.currentUnmount();
            }

            this.container.innerHTML = "";

            this.currentUnmount = route.view(this.container);
        }

        start(): void {
            this.navigate(window.location.pathname);
        }
    }
