



import { HttpClient } from "../api/HttpClient";
import Router from "../router/Router";
import { createElement } from "../ui/dom"
import { renderAsyncState } from "../ui/asyncState";


export interface Product {
    id: number,
    name: string,
    description: string,
    price: number,
    stock: number,
    is_active: boolean,
    category_id: number,
    created_at: string
}

export interface PaginatedResponse<T> {
    items: T[];
    total: number;
    has_next: boolean;
}

export interface CatalogState {
    products: Product[],
    loading: boolean,
    error: string | null,
    addingProductIds: Set<number>
}

export function ProductCatalogView(
    container: HTMLElement,
    httpClient: HttpClient,
    router: Router
): () => void {

    let isMounted = true;

    const abortController = new AbortController();

    const state: CatalogState = {
    products: [],
    loading: true,
    error: null,
    addingProductIds: new Set()
    };

    function updateUI() {
    if (!isMounted) {
        return;
    }

    renderAsyncState(container, state, () => {
            if (state.products.length === 0) {
                const emptyMsg = document.createElement("div");
                emptyMsg.textContent = "No products available.";
                container.appendChild(emptyMsg);
                return;
            }

            const productsContainer = createElement('div', { class: "products-grid "});

            state.products.forEach(product => {
                const productCard = createProductCard(product, state, updateUI, httpClient);
                productsContainer.appendChild(productCard);
            });

            container.appendChild(productsContainer);
        });
        }

        async function fetchProducts() {
            try {
                const response = await httpClient.request<PaginatedResponse<Product>>('/api/v1/products/', {
                    signal: abortController.signal 
                });
                
                state.products = response.items;
            } catch (err: any) {
                if (err.name === "AbortError") {
                    return;
                }

                state.error = err.message || "Failed to load products";
                } finally {
                    state.loading = false;
                    updateUI();
                }
            }

            fetchProducts();

            return () => {
                isMounted = false;
                abortController.abort();
            }
        }
    
    function createProductCard(
        product: Product,
        state: CatalogState,
        updateUI: () => void,
        httpClient: HttpClient
    ): HTMLElement {
        
        const isAdding = state.addingProductIds.has(product.id);
        const isOutOfStock = product.stock <= 0;

        const card = createElement("div", { class: "product-card" });

        const title = document.createElement("h3");
        title.textContent = product.name;
        card.appendChild(title);

        const description = document.createElement("p");
        description.textContent = product.description;
        card.appendChild(description);

        const price = document.createElement("strong");
        price.textContent = `Price: $${product.price}`;
        card.appendChild(price);

        const stock = document.createElement("small");
        stock.textContent = `Stock: ${product.stock}`;
        card.appendChild(stock);

        let btnText = "Add to Cart";

        if (isAdding) btnText = "Adding...";

        if (isOutOfStock) btnText = "Out of stock";

        const btn = document.createElement("button");
        btn.textContent = btnText;

        if (isAdding || isOutOfStock) {
            btn.disabled = true
        }

        if (!isOutOfStock) {
            btn.addEventListener("click", async () => {
                state.addingProductIds.add(product.id);
                updateUI();
        
                try {
                    await httpClient.request("/api/v1/cart/items", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ product_id: product.id, quantity: 1})
                    })

                        btn.textContent = "Added!";
                        btn.style.color = "green";
                        setTimeout(() => updateUI(), 2000);
                    } catch(error: any) {
                        alert(error.message || "Failed to add to cart");
                    } finally {
                        state.addingProductIds.delete(product.id);
                        updateUI();
                        }
                    });
                }
                card.appendChild(btn);
                return card;
            }