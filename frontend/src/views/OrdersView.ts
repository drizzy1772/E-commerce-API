



import HttpClient, { HttpError, NetworkError } from "../api/HttpClient";
import { createElement } from "../ui/dom";
import { renderAsyncState } from "../ui/asyncState";

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
): () => void {

    let isMounted = true;
    const controller = new AbortController();
    
    const state: OrdersViewState = {
        orders: [],
        loading: true,
        error: null,
    };

    const updateUI = () => {
        if (!isMounted) return;
        render(container, state);
    };

    updateUI();


    fetchOrders(httpClient, state, updateUI, controller.signal);

    //exit from page
    return () => {
        isMounted = false;
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
            const data = await httpClient.request<Order[]>("/orders", { signal });

        
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
function render(
    container: HTMLElement,
    state: OrdersViewState,

) {
    renderAsyncState(container, state, (cont, validState) => {
        if (validState.orders.length === 0) {
            const createOrders = createElement("h2", {}, [`No orders`]);
            cont.appendChild(createOrders);
            return;
        }

        const list = createElement("div", { class: "orders-list" });

        for (const order of validState.orders) {
            const idText = `Order #${order.id}`;
            const idSpan = createElement("span", { class: "order-id" }, [idText]);


            const totalText = `$${order.total_amount}`;
            const totalSpan = createElement("span", { class: "order-total" }, [totalText]);

            const rowChildren = [idSpan, totalSpan];

            if (order.status) {
                const statusStamp = createElement("span", { class: "status-stamp" }, [order.status]);
                rowChildren.push(statusStamp); 
            }
            
            const orderRow = createElement(
                "div",
                { class: 'list-row' },
                rowChildren
            );

            list.appendChild(orderRow);
        }
        cont.appendChild(list);
    });
    }
