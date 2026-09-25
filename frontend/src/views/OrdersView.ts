




import HttpClient, { HttpError, NetworkError } from "../api/HttpClient";
import Router from "../router/Router";
import { renderAsyncState } from "../ui/asyncState";
import { createElement } from "../ui/dom";

//my first order
interface Order {
    id: number | string;
    user_id: string;
    total_amount: number;
    status: string;
    created_at: string;

}

//stats of order
interface OrdersViewState {
    orders: Order[];
    loading: boolean;
    error: string | null;
}

//point of enter in /orders
export function OrdersView(
    container: HTMLElement,
    httpClient: HttpClient,
    router: Router
): () => void {

    const controller = new AbortController();
    
    const state: OrdersViewState = {
        orders: [],
        loading: true,
        error: null,
    };

    const updateUI = () => render(container, state);

    updateUI();


    fetchOrders(httpClient, state, updateUI, controller.signal);

    //exit from page
    return () => {
        controller.abort();
    };
}

//walk on server and changing stats
    async function fetchOrders(
        httpClient: HttpClient,
        state: OrdersViewState,
        updateUI: () => void,
        signal: AbortSignal
    ) {
        try {
            const data = await httpClient.request<Order[]>("/api/v1/orders/", { signal });

        
            state.orders = data;

            state.loading = false;

            updateUI();


        } catch (error: any) {
            if (error instanceof DOMException && error.name === "AbortError") {
                return;
            }

            if (error instanceof HttpError) {
                state.error = `Server Error [${error.status}]: ${error.message}`;
            } else if (error instanceof NetworkError) {
                state.error = "Network Error: Please check your internet connection.";
            } else {
                state.error = error.message;
            }

            state.loading = false;
            updateUI();
        }
    }

function createOrderCard(order: Order): HTMLElement {

    const cardText = `Order: ${order.id} | Status: ${order.status} | Total: ${order.total_amount} USD`

    return createElement("div", { class: "order-card", style: "border: 1px solid #ccc; padding: 8px; margin-bottom: 8px;" }, [cardText])

}

//watch for a state and give an HTML
function render(container: HTMLElement, state: OrdersViewState) {
    renderAsyncState(container, state, (cont, validState) => {
        if (validState.orders.length === 0) {
            const createOrders = createElement("h2", {}, [`You didn't have orders right now`]);
            cont.appendChild(createOrders);
            return;
        }

        const list = createElement("div", { class: { "orders-list" } })

        for (const order of validState.orders) {
            const card = createOrderCard(order);
            list.appendChild(card);

        }
        cont.appendChild(list);
    });
    }