





import HttpClient, { HttpError, NetworkError } from "../api/HttpClient";
import Router from "../router/Router";
import { createElement } from "../ui/dom";
import { renderAsyncState } from "../ui/asyncState";


export interface User {
    id: string | number;
    name: string;
    email: string;
    isActive: boolean;
}


export interface UsersViewState {
    users: User[];
    loading: boolean;
    error: string | null;
    deactivatingUserIds: Set<string | number>;
}

//users view
export function UsersView (
    container: HTMLElement,
    httpClient: HttpClient,
    router: Router
): () => void {
    const controller = new AbortController();

    const state: UsersViewState = {
        users: [],
        loading: true,
        error: null,
        deactivatingUserIds: new Set(),
    }

    const updateUI = () => render(container, state, httpClient, updateUI);

    updateUI();

    fetchUsers(httpClient, state, updateUI, controller.signal);

    return () => {
        controller.abort();
    };
}


async function fetchUsers(
    httpClient: HttpClient,
    state: UsersViewState,
    updateUI: () => void,
    signal: AbortSignal
) {
    try {
        const users = await httpClient.request<User[]>("/api/v1/users", { signal });

        state.users = users;

        state.loading = false;

        updateUI();

    } catch(error: any) {
        if (error instanceof DOMException && error.name === "AbortError") {
            return;
        }

        if (error instanceof HttpError) {
            state.error = `Error server (${error.status}): (${error.message})`;
        
        } else if (error instanceof NetworkError) {
            state.error = `Network error: Please check your internet connection`
        } else {
            state.error = error.message;
        }

        state.loading = false;

        updateUI();

    }
}


async function deactivateUser(
    userId: string | number,
    httpClient: HttpClient,
    state: UsersViewState,
    updateUI: () => void
) {

    state.deactivatingUserIds.add(userId);
    updateUI();
    
    try {
    await httpClient.request(`/api/v1/users/${userId}/deactivate`, { method: 'PATCH' });

        const user = state.users.find(u => u.id === userId)
        if (user) { 
            user.isActive = false;
        }
    } catch (error: any) {
            alert(`Failed to deactivate user: ${error.message}`);
        } finally {
            state.deactivatingUserIds.delete(userId);
            updateUI();
        }
    }

function render(
    container: HTMLElement,
    state: UsersViewState,
    httpClient: HttpClient,
    updateUI: () => void
) {
    renderAsyncState(container, state, (cont, validState) => {
        if (validState.users.length === 0) {
            const emptyMsg = createElement("h2", {}, ["No users found"]);
            cont.appendChild(emptyMsg);
            return;
        }

        const list = createElement("div", { class: "users-list" });

        for (const user of validState.users) {

            const textContent = `Name: ${user.name} | Email: ${user.email} | Status: ${user.isActive ? 'Active' : 'Inactive'}`;
            const textSpan = createElement("span", {}, [textContent]);

            const isButtonDeactivated = state.deactivatingUserIds.has(user.id);
            const isAlreadyDeactivated = !user.isActive;
            const isDisabled = isButtonDeactivated || isAlreadyDeactivated;

            let buttonText = "Deactivate";
            if (isDisabled) {
                buttonText = isAlreadyDeactivated ? 'Deactivated' : 'Deactivating...';
            }

            const btnAttrs: any = {};
            if (isDisabled) {
                btnAttrs.disabled = true;
            } else {
                btnAttrs.onclick = () => deactivateUser(user.id, httpClient, state, updateUI);
            }
            
            const deactivateBtn = createElement("button", btnAttrs, [buttonText]);

                const userItem = createElement(
                    "div",
                    {
                        class: 'user-item',
                        style: 'border: 1px solid #ccc; padding: 8px; margin-bottom: 8px; display: flex; justify-content: space-between;'
                    },
                    [textSpan, deactivateBtn]
                );

                list.appendChild(userItem);
            
            }
            cont.appendChild(list);

        });
    }   