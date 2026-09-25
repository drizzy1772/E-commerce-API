


import HttpClient, { HttpError, NetworkError } from "../api/HttpClient";
import Router from "../router/Router";
import { createElement } from "../ui/dom";
import { renderAsyncState } from "../ui/asyncState";


export interface CartItem {
    id: string | number;
    name: string;
    quantity: number;
    price: number;
}

export interface CartViewState {
    items: CartItem[];
    loading: boolean;
    error: string | null;
    deletingItemId: string | number | null;
}

export function CartItemsView (
    container: HTMLElement,
    httpClient: HttpClient,
    router: Router
): () => void {
    const controller = new AbortController();

    const state: CartViewState = {
        items: [],
        loading: true,
        error: null,
        deletingItemId: null,
    };


    const updateUI = () => render(container, state, httpClient, updateUI);

    updateUI();
    fetchCart(httpClient, state, updateUI, controller.signal);

    return () => {
        controller.abort();
    };
}

async function fetchCart(
    httpClient: HttpClient,
    state: CartViewState,
    updateUI: () => void,
    signal: AbortSignal
) {
    try {
        const data = await httpClient.request<CartItem[]>("/api/v1/cart/items", { signal });
        state.items = data;
        state.loading = false;
        updateUI();
    } catch (error: any) {

        if (error instanceof DOMException && error.name === "AbortError") {
            return;
        }

        if (error instanceof HttpError) {
            state.error = `Server error [${error.status}]: ${error.message}`;
    } else if (error instanceof NetworkError) {
        state.error = `Network Error: Please check your internet connection.`;
    } else {
        state.error = error.message;
    }

    state.loading = false;
    updateUI();
    }
}


//logic of deleting Wait-for-response

async function removeItem(
    itemId: string | number,
    httpClient: HttpClient,
    state: CartViewState,
    updateUI: () => void
) {
    state.deletingItemId = itemId;
    updateUI();

    try {
        await httpClient.request(`/api/v1/cart/items/${itemId}`, { method: "DELETE" });
        state.items = state.items.filter(item => item.id !== itemId);
    } catch (error: any) {
        alert(`Failed to delete item ${error.message}`);
    } finally {
        state.deletingItemId = null;
        updateUI();
    }
}


function render(
    container: HTMLElement,
    state: CartViewState,
    httpClient: HttpClient,
    updateUI: () => void
) {
    renderAsyncState(container, state, (cont, validState) => {

        if (validState.items.length === 0) {
            const emptyMsg = createElement("h2", {}, ["Bag is empty"]);
            cont.appendChild(emptyMsg);
            return
        }

        const list = createElement("div", { class: "cart-list" });

        
    for (const item of validState.items) {

        const itemText = `${item.name} | amount: ${item.quantity} | ${item.price * item.quantity} $`;
        const textSpan = createElement("span", {}, [itemText])

        const isDeleting = state.deletingItemId === item.id;

        const deleteBtn = createElement("button",
            isDeleting ? { disabled: "true" } : {},
            [isDeleting ? "Deleting...": "Delete"]
    );

        deleteBtn.onclick = () => {
            removeItem(item.id, httpClient, state, updateUI);
        };
        
        const itemElement = createElement("div", { class: "cart-item", style: "border: 1px solid #ccc; padding: 8px; margin-bottom: 8px; display: flex; justify-content: space-between;"}, [textSpan, deleteBtn]
    );

    list.appendChild(itemElement);
}
    cont.appendChild(list);
    });
}

