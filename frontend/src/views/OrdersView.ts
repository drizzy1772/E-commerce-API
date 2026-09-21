




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
    };

    if (state.error !== null) {
        container.innerHTML = `<h2 style="color: red;">Error: ${state.error}</h2>`
        return;
    }
    
    if (state.loading === false) {
        container.innerHTML = "<h2>Stats loaded!</h2>";
    };
}
    







////



interface Product {
    id: string | number,
    title: string,
    price: number,
    inStock: boolean;
}

interface ProductsViewState {
    products: Product[],
    loading: boolean,
    error: string | null
}

export function ProductsView(
    container: HTMLElement,
    httpClient: HTTPClient
): () => void {

    

    const state : ProductsViewState = {
        products: [],
        loading: true,
        error: null
    };

    const updateUI = () => render(container, state);

    updateUI();

    fetchProducts(httpClient, state, updateUI);
}

async function fetchProducts(
        httpClient: HTTPClient,
        state: ProductsViewState,
        updateUI: () => void
    ) {
        try{
            const data = await httpClient.request<Product[]>("/api/v1/products");
            state.products = data;
            state.loading = false;
            updateUI();
        } catch(error: any) {
            state.error = error.message;
            state.loading = false;
            updateUI();
        }
    }
    function render(
        container: HTMLElement,
        state: ProductsViewState
    ) {
           if (state.loading === true) {
        container.innerHTML = "<h2>Products loading...</h2>";
        return;
    };

    if (state.error !== null) {
        container.innerHTML = `<h2 style="color: red;">Error: ${state.error}</h2>`
        return;
    }
    
    if (state.loading === false) {
        const productsHTML = state.products.map(product => {
            return `
                <div>
                    <h3>${product.title}</h3>
                    <p>Price: ${product.price} UAH</p>
                    <p>${product.inStock ? "In stock" : "Out of stock"}</p>
                </div>
            `;
        }).join("");
        container.innerHTML = productsHTML
    };
}

