


import { HttpClient, HttpError } from "../api/HttpClient";
import { renderAsyncState } from "../ui/asyncState";
import { createElement } from "../ui/dom";


export interface Product {
    id: string,
    name: string,
    price: string,
    stock: number,
}

export interface ProductsViewState{
    products: Product[],
    page: number,
    status: 'loading' | 'success' | 'error' | 'empty';
    error: string | null;
    addingToCardIds: Set<string>
}

export function ProductsView(container: HTMLElement, httpClient: HttpClient, router: any) {
    const state: ProductsViewState = {
        products: [],
        page: 1,
        status: "loading",
        error: null,
        addingToCardIds: new Set()
    };

    let currentController: AbortController | null = null;

    function updateUI() {
        container.replaceChildren();
        render(container, state, updateUI, loadProducts, addToCart);
    };

    async function addToCart(productId: string) {
        if (state.addingToCardIds.has(productId)) {
            return;
        }
        state.addingToCardIds.add(productId);
        updateUI();
        

        try {
            await httpClient.request("/cart/items", {
                method: 'POST',
                body: JSON.stringify({ product_id: productId, quantity: 1 })
            });

            alert("Added to cart!");
        } catch(error: any) {
            alert(error.message);
        } finally {
            state.addingToCardIds.delete(productId);
            updateUI();
        }
    }
    async function loadProducts(pageToFetch: number) {
        if (currentController) {
            currentController.abort();
        }

        currentController = new AbortController();

        state.page = pageToFetch;
        state.status = 'loading';
        updateUI();
        
        
        try {
            const products = await httpClient.request<Product[]>(`/products?page=${pageToFetch}`, {
                signal: currentController.signal
            });

            state.products = products;

            if (products.length === 0) {
                    state.status = 'empty';
                } else {
                    state.status = 'success';
                }
                updateUI();
            } catch(error: any) {
                if (error.name === 'AbortError') {
                    return;
                }

                state.error = error.message || 'An unexpected error occurred';
                state.status = 'error';
                updateUI();
            }
        }

        loadProducts(state.page);
        return () => {
            if (currentController) {
                currentController.abort();
            }
        };
    }

function render(
    container: HTMLElement,
    state: ProductsViewState,
    updateUI: () => void,
    loadProducts: (page: number) => void,
    addToCart: (productId: string) => void
) {
    renderAsyncState(container, state, (cont, validState) => {
        const list = createElement("div", { class: "products-list"  });

        for (const product of validState.products) {

            const nameSpan = createElement('span', {}, [product.name]);
            const priceSpan = createElement('span', {}, [`$${product.price}`]);
            const stockSpan = createElement('span', {}, [`Stock ${product.stock}`]);

            const infoContainer = createElement("div", { class: "product-info" }, [nameSpan, priceSpan, stockSpan]);
            
            const isAdding = state.addingToCardIds.has(product.id);
            const isOutOfStock = product.stock <= 0;

            const button = createElement("button", {
                class: "btn", 
                disabled: (isAdding || isOutOfStock) ? true : undefined
            }, [isAdding ? "Adding.." : isOutOfStock ? "Out of stock" : "Add to Cart"]);                

            button.addEventListener("click", () => {
                addToCart(product.id);
            });

            const rowContainer = createElement("div", { class: "list-row" }, [infoContainer, button]);
            list.appendChild(rowContainer);
        }

            cont.appendChild(list);
        });
    }