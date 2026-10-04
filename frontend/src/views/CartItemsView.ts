


import { HttpClient, HttpError, NetworkError } from "../api/HttpClient";
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
    isCheckingOut: boolean;
    deletingItemIds: Set<string | number>;
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
        isCheckingOut: false,
        deletingItemIds: new Set(),
    };

    const updateUI = () => render(container, state, httpClient, updateUI, router);

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
        const data = await httpClient.request<CartItem[]>("/cart", { signal });
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
    updateUI: () => void,
) {
    state.deletingItemIds.add(itemId);

    updateUI();

    try {
        await httpClient.request(`/cart/items/${itemId}`, { method: "DELETE" });
        state.items = state.items.filter(item => item.id !== itemId);
    } catch (error: any) {
            alert(`Failed to delete item ${error.message}`);
    } finally {
        state.deletingItemIds.delete(itemId);

        updateUI();
    }
}

async function checkout(
    httpClient: HttpClient,
    state: CartViewState,
    router: Router,
    updateUI: () => void,
) {
    if (state.isCheckingOut || state.items.length === 0) {
        return;
    }

    state.isCheckingOut = true;
    updateUI();

    try {
    const idempotencyKey = crypto.randomUUID();
    await httpClient.request("/orders/",{ 
        method: "POST",
        headers: { "Idempotency-Key": idempotencyKey }
    });

    router.navigate("/orders");
} catch (error: any) {
        if (error instanceof HttpError) {
            alert(`Server error [${error.status}]: ${error.message}`);
        } else if (error instanceof NetworkError) {
            alert(`Network Error: Please check your internet connection`);
        } else {
            alert(error.message);
        }

        state.isCheckingOut = false;
        updateUI();
    }
}



function render(
    container: HTMLElement,
    state: CartViewState,
    httpClient: HttpClient,
    updateUI: () => void,
    router: Router,
) {
    renderAsyncState(container, state, (cont: HTMLElement, validState: CartViewState) => {
        
        if (validState.items.length === 0) {
            const emptyMsg = createElement("h2", {}, ["Bag is empty"]);
            cont.appendChild(emptyMsg);
            return
        }

        const list = createElement("div", { class: "cart-list" });

        
    for (const item of validState.items) {

        const itemText = `${item.name} | amount: ${item.quantity} | $${item.price * item.quantity}`;
        const textSpan = createElement("span", {}, [itemText])

        const isDeleting = state.deletingItemIds.has(item.id);

        const btnAttrs: any = {};
        if (isDeleting) {
            btnAttrs.disabled = true;
        } else {
            btnAttrs.onclick = () => removeItem(item.id, httpClient, state, updateUI);
        }
        const deleteBtn = createElement(
            "button",
            btnAttrs,
            [isDeleting ? "Deleting..." : "Delete"]
        );

        const itemElement = createElement(
            "div",
            { class: "cart-item",
              style: "border: 1px solid #ccc; padding: 8px; margin-bottom: 8px; display: flex; justify-content: space-between;"
            },
            [textSpan, deleteBtn]
        );

        list.appendChild(itemElement);
    }
    cont.appendChild(list);


    const checkoutBtnAttrs: any = { 
        style: "margin-top: 20px; padding: 10px 20px; font-weight: bold; cursor: pointer;"
    };

    if (validState.isCheckingOut) {
        checkoutBtnAttrs.disabled = true;
    } else {
        checkoutBtnAttrs.onclick = () => checkout(httpClient, state, router, updateUI);
    }

    const checkoutBtn = createElement(
        "button",
        checkoutBtnAttrs,
        [validState.isCheckingOut ? "Processing..." : "Checkout"]);

    cont.appendChild(checkoutBtn);
    });
}