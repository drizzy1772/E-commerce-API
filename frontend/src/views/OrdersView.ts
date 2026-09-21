




import HTTPClient from "../api/HttpClient";
import HttpClient from "../HttpClient";
import Router from "../router/Router";

//my first order
interface Order {
    id: number | string;
    status: string;
    total: number;
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
    httpClient: HTTPClient,
    router: Router
): () => void {
    
    const state: OrdersViewState = {
        orders: [],
        loading: true,
        error: null,
    };

    const updateUI = () => render(container, state);

    updateUI();

    fetchOrders(httpClient, state, updateUI);

    //exit from page
    return () => {
        container.innerHTML = "";
    };
}

//walk on server and changing stats
    async function fetchOrders(
        httpClient: HTTPClient,
        state: OrdersViewState,
        updateUI: () => void
    ) {
        try {
            const data = await httpClient.request<Order[]>("/api/v1/orders");


        
            state.orders = data;

            state.loading = false;

            updateUI();


        } catch (error: any) {
            state.error = error.message;
            state.loading = false;
            updateUI();
        }
    }

//watch for a state and give an HTML
function render(container: HTMLElement, state: OrdersViewState) {
    if (state.loading === true) {
        container.innerHTML = "<h2>Orders loading...</h2>";
        return;
    }

    if (state.error !== null) {
        container.innerHTML = `<h2 style="color: red;">Error: ${state.error}</h2>`
        return;
    }
    
   
    if (state.orders.length === 0) {
    container.innerHTML = "<h2>You didnt have orders right now</h2>"
    return;
    }

    const tableRows = state.orders.map(order => {
        return `<tr>
            <td style="border: 1px solid #ccc; padding: 8px;">${order.id}</td>
               <td style="border: 1px solid #ccc; padding: 8px;">${order.status}</td>
               <td style="border: 1px solid #ccc; padding: 8px;">$${order.total}</td>
           </tr>`;
        }).join("");

    container.innerHTML = `
        <h2>Your orders</h2>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
               <thead style="background: #f4f4f4;">
                   <tr>
                       <th style="border: 1px solid #ccc; padding: 8px;">ID</th>
                       <th style="border: 1px solid #ccc; padding: 8px;">Stats</th>
                       <th style="border: 1px solid #ccc; padding: 8px;">Total</th>
                   </tr>
               </thead>
               <tbody>
                   ${tableRows}
               </tbody>
           </table>
       `;
    }
