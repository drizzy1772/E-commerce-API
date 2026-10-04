



import { HttpClient, HttpError, NetworkError } from "../api/HttpClient";
import { createElement } from "../ui/dom";
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
    addingProductIds: Set<number>,
    addedProductIds: Set<number>
}

export function ProductCatalogView(
    container: HTMLElement,
    httpClient: HttpClient,
): () => void {

    let isMounted = true;

    const abortController = new AbortController();

    const state: CatalogState = {
        products: [],
        loading: true,
        error: null,
        addingProductIds: new Set(),
        addedProductIds: new Set()
    };

    function updateUI() {
    if (!isMounted) {
        return;
    }

    renderAsyncState(container, state, (cont, validState) => {
            if (validState.products.length === 0) {
                const emptyMsg = document.createElement("div");
                emptyMsg.textContent = "No products available.";
                cont.appendChild(emptyMsg);
                return;
            }

            const productsContainer = createElement('div', {
                class: "products-grid",
            });

            validState.products.forEach(product => {
                const productCard = createProductCard(product, state, updateUI, httpClient);
                productsContainer.appendChild(productCard);
            });

            cont.appendChild(productsContainer);
        });
        }

        async function fetchProducts() {
            try {
                const response = await httpClient.request<PaginatedResponse<Product>>('/products', {
                    signal: abortController.signal 
                });
                state.products = response.items;
            } catch (error: any) {
                if (error instanceof DOMException && error.name === "AbortError") return;


                if (error instanceof HttpError) {
                    state.error = `Server error [${error.status}]: ${error.message}`;
                } else if (error instanceof NetworkError) {
                    state.error = `Network Error: Please check your internet connection`;
                } else {
                    state.error = error.message;
                }
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
        const isAdded = state.addedProductIds.has(product.id);
        const isOutOfStock = product.stock <= 0;

        const title = createElement("h3", {}, [product.name]);

        const description = createElement("p", {}, [product.description]);

        const price = createElement("strong", {}, [`Price: $${product.price}`]);

        const stock = createElement("small", {}, [`Stock: ${product.stock}`]);

        let btnText = "Add to Cart";

        if (isAdding) btnText = "Adding...";

        else if (isAdded) btnText = "Added!";

        else if (isOutOfStock) btnText = "Out of stock";

        const btn = createElement(
            "button",
            {},
            [btnText]
        ) as HTMLButtonElement;

        if (isAdding || isOutOfStock || isAdded) {
            btn.disabled = true;
        }

        if (isAdded) {
            btn.style.color = "green";
        }

        if (!isOutOfStock) {
            btn.addEventListener("click", async () => {
                state.addingProductIds.add(product.id);
                updateUI();
        
                try {
                    await httpClient.request("/cart/items", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            product_id: product.id,
                            quantity: 1,
                        }),
                    });

                    state.addedProductIds.add(product.id);
                    setTimeout(() => {
                        state.addedProductIds.delete(product.id);
                        updateUI();
                    }, 2000);

                    } catch(error: any) {
                        if (error instanceof HttpError) {
                            alert(`Server error [${error.status}]: ${error.message}`);
                        } else if (error instanceof NetworkError)
                        alert(`Network Error: Please check your internet connection`);
                        else {
                            alert(error.message);
                        }
                    } finally {
                        state.addingProductIds.delete(product.id);
                        updateUI();
                        }
                    });
                }

                const card = createElement("div", { class: "product-card" }, [
                    title,
                    description,
                    price,
                    stock, 
                    btn
                ]);

                return card;
            }

