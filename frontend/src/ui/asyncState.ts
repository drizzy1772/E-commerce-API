



import { createElement } from "./dom";


export interface AsyncState{
    loading: boolean;
    error: string | null;
}

export function renderAsyncState<T extends AsyncState>(
    container: HTMLElement,
    state: T,
    renderSuccess: (container: HTMLElement, state: T) => void
): void {
    container.replaceChildren();

    if (state.loading) {
        const loadingHeader = createElement("h2", {}, ["Loading..."]);
        container.appendChild(loadingHeader);
        return;
    }

    if (state.error !== null) {
    const errorHead = createElement("h2", { "style": "color: red;" }, [`Error: ${state.error}`]);
    
    container.appendChild(errorHead);
    return;
    }
    renderSuccess(container, state);
}