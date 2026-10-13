





import { HttpClient, HttpError, NetworkError } from "../api/HttpClient";
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
    status: 'loading' | 'success' | 'error' | 'empty';
    error: string | null;
    deactivatingUserIds: Set<string | number>;
}

//users view    
export function UsersView (
    container: HTMLElement,
    httpClient: HttpClient,
): () => void {
    let isMounted = true;
    const controller = new AbortController();

    const state: UsersViewState = {
        users: [],
        status: "loading",
        error: null,
        deactivatingUserIds: new Set(),
    };

    const updateUI = () => {
        if (!isMounted) return;
        container.replaceChildren();
        render(container, state, httpClient, updateUI);
    };

    updateUI();

    fetchUsers(httpClient, state, updateUI, controller.signal);

    return () => {
        controller.abort();
        isMounted = false;
    };
}


async function fetchUsers(
    httpClient: HttpClient,
    state: UsersViewState,
    updateUI: () => void,
    signal: AbortSignal
) {
    try {
        const users = await httpClient.request<User[]>("/users", { signal });

        state.users = users;

        if (users.length === 0) {
            state.status = 'empty'
        } else {
            state.status = 'success';
    }

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

        state.status = 'error';
        
        updateUI();

    }
}


async function deactivateUser(
    httpClient: HttpClient,
    state: UsersViewState,
    updateUI: () => void,
    userId: string | number,
) {

    if (state.deactivatingUserIds.has(userId)) return;

    state.deactivatingUserIds.add(userId);
    updateUI();
    
    try {
        await httpClient.request(`/users/${userId}/deactivate`, { method: 'PATCH' });

        state.users = state.users.map(user => 
            user.id === userId ? { ...user, isActive: false } : user
        );
    } catch (error: any) {
        if (error instanceof HttpError){
            alert(`Failed to deactivate user: ${error.message}`);
        } else if (error instanceof NetworkError) {
            alert("Network Error: Could not deactivate user. Please check connection.");
        } else {
            alert(error.message);
        }
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
        const list = createElement("div", { class: "users-list" });

        for (const user of validState.users) {
            const nameSpan = createElement("span", {}, [user.name]);
            const emailSpan = createElement("span", {}, [user.email]);
            const statusSpan = createElement("span", {}, [user.isActive ? 'Active' : 'Inactive']);
            const infoContainer = createElement("div", {}, [nameSpan, emailSpan, statusSpan]);

            const isDeactivating = validState.deactivatingUserIds.has(user.id);
            const isAlreadyDeactivated = !user.isActive;
            const isDisabled = isDeactivating || isAlreadyDeactivated;


            const deactivateBtn = createElement("button", {
                class : "btn",
                disabled: isDisabled ? true : undefined
            }, [
                isDeactivating ? "Deactivating..." : isAlreadyDeactivated ? "Deactivated": "Deactivate"
            ]);

            deactivateBtn.addEventListener("click", () => {
                deactivateUser(httpClient, state, updateUI, user.id);
            });

            const userItem = createElement("div", { class: 'list-row' }, [infoContainer, deactivateBtn]);
                list.appendChild(userItem);
            }
            cont.appendChild(list);
        });
    }









