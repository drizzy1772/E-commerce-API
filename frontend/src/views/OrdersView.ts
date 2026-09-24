




import HttpClient, { HttpError, NetworkError } from "../api/HttpClient";
import Router from "../router/Router";
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

//watch for a state and give an HTML
function render(container: HTMLElement, state: OrdersViewState) {
    container.replaceChildren();

    if (state.loading === true) {
        const loadingText = createElement("h2", {}, ["Orders loading..."])
            container.appendChild(loadingText);
            return;
    }

    if (state.error !== null) {
        const errorText = createElement("h2", { style: "color: red;" }, [`Error: ${state.error}`]);
        container.appendChild(errorText);
        return;
    }
    
   
    if (state.orders.length === 0) {
        const emptyText = createElement("h2", {}, ["You didnt have orders right now"]);
        container.appendChild(emptyText);
        return;
    }

        const list = createElement("div", { class: "orders-list" })

        for (const order of state.orders) {
            const orderText = `Order: ${order.id} | Status: ${order.status} | Total: $${order.total_amount}`;

            const card = createElement("div", { style: "border: 1px solid #ccc; padding: 8px;" }, [orderText]);

            list.appendChild(card);

        }
        container.appendChild(list);
    }