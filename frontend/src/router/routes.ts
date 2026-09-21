




export interface RouteDefinition {
    path: string;

    view: (container: HTMLElement) => void | (() => void);
    requiresAuth: boolean;
    allowedRoles?: string[];
}