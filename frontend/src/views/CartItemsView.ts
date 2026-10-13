


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
    let isMounted = true;
    const controller = new AbortController();

    const state: CartViewState = {
        items: [],
        loading: true,
        error: null,
        isCheckingOut: false,
        deletingItemIds: new Set(),
    };

    const updateUI = () => {
        if (!isMounted) return;
        render(container, state, httpClient, updateUI, router);
    };

    updateUI();
    fetchCart(httpClient, state, updateUI, controller.signal);

    return () => {
        isMounted = false;
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
    httpClient: HttpClient,
    state: CartViewState,
    updateUI: () => void,
    itemId: string | number,
) {
    state.deletingItemIds.add(itemId);

    updateUI();

    try {
        await httpClient.request(`/cart/items/${itemId}`, { method: "DELETE" });
        state.items = state.items.filter(item => item.id !== itemId);
    } catch (error: any) {
        if (error instanceof HttpError) {
            alert(`Failed to remove item [${error.status}]: ${error.message}`);
        } else if (error instanceof NetworkError) {
                alert("Network Error: Could not remove item. Please check connection.");
        } else {
            alert(error.message);
        }
    } finally {
        state.deletingItemIds.delete(itemId);
        updateUI();
    }
}

async function checkout(
    httpClient: HttpClient,
    state: CartViewState,
    updateUI: () => void,
    router: Router,
) {
    if (state.isCheckingOut || state.items.length === 0) {
        return;
    }

    state.isCheckingOut = true;
    updateUI();

    try {
        const idempotencyKey = crypto.randomUUID();
        await httpClient.request("/orders/", {
            method: "POST",
            headers: { "Idempotency-Key": idempotencyKey }
        });

        router.navigate("/orders");
    } catch (error: any) {
        state.isCheckingOut = false;    

        if (error instanceof HttpError) {
            alert(`Checkout failed [${error.status}]: ${error.message}`);
        } else if (error instanceof NetworkError) {
            alert("Network Error: Checkout failed. Please check connection.");
        } else {
            alert(error.message);
        }

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
    renderAsyncState(container, state, (cont, validState) => {
        if (validState.items.length === 0) {
            const emptyMsg = createElement("h2", {}, ["Cart is empty"]);
            cont.appendChild(emptyMsg);
            return
        }

        const list = createElement("div", { class: "cart-list" });
        let totalAmount = 0;

        
        for (const item of validState.items) {
            totalAmount += item.price * item.quantity;

        const nameSpan = createElement("span", {}, [`${item.name} (x${item.quantity})`]);
        const priceSpan = createElement("span", {}, [`$${item.price * item.quantity}`]);
        const infoContainer = createElement("div", {}, [nameSpan, priceSpan]);

        const isDeleting = validState.deletingItemIds.has(item.id);
        const removeBtn = createElement("button", {
            class: "btn",
            disabled: isDeleting || validState.isCheckingOut ? true : undefined
        }, [isDeleting ? "Removing..." : "Remove"]);

        removeBtn.addEventListener('click', () => {
            removeItem(httpClient, validState, updateUI, item.id);
        });

        const itemRow = createElement("div", { class: 'list-row' }, [infoContainer, removeBtn]);
        list.appendChild(itemRow);
    }

    const totalHeader = createElement("h3", {}, [`Total: $${totalAmount}`]);

    const checkoutBtn = createElement("button", {
        class: "btn btn-primary",
        disabled: validState.isCheckingOut ? true : undefined
    }, [validState.isCheckingOut ? "Processing..." : "Checkout"]);

    
    checkoutBtn.addEventListener("click", () => {
        checkout(httpClient, validState, updateUI, router);
    });

    cont.appendChild(list);
    cont.appendChild(totalHeader);
    cont.appendChild(checkoutBtn);
    });
}