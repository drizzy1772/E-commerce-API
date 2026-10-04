



import type { HttpClient } from "../api/HttpClient";
import { createElement } from "../ui/dom";







export function AdminProductCreateView(
    container: HTMLElement,
    httpClient: HttpClient
): () => void {
    const form = createElement("form", {
        "class": "admin-product-form",
    });
    const title = createElement("h1", {}, ["Create Product"]);

    form.append(title);

    const nameInput = createElement("input", {
        name: "name",
        type: "text",
        placeholder: "Product name",
        required: true,
    }) as HTMLInputElement;

    form.append(nameInput);

    const description = createElement("textarea", {
        name: "description",
        placeholder: "Product description",
        required: true,
    }) as HTMLTextAreaElement;

    form.append(description);

    const priceInput = createElement("input", {
        name: "price",
        type: "number",
        min: "0.01",
        step: "0.01",
        placeholder: "Price",
        required: true,
    }) as HTMLInputElement;

    form.append(priceInput);

    const stockInput = createElement("input", {
        name: "stock",
        type: "number",
        min: "0",
        step: "1",
        placeholder: "Stock",
        required: true,
    }) as HTMLInputElement;

    form.append(stockInput);

    const categoryInput = createElement("input", {
        name: "category_id",
        type: "number",
        min: "1",
        placeholder: "Category ID",
        required: true,
    }) as HTMLInputElement;

    form.append(categoryInput);

    const submitButton = createElement( 
        "button",
        { type: "submit"},
        ["Create Product"]
    ) as HTMLButtonElement;

    form.append(submitButton);

    const message = createElement("p", {
        class: "form-message",
    });

    form.append(message);

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = nameInput.value.trim();
        const productDescription = description.value.trim();
        const price = Number(priceInput.value);
        const stock = Number(stockInput.value);
        const categoryId = Number(categoryInput.value);
        
        if (!name || name.trim() === "") {
            message.textContent = "The name is empty";
            return;
        } else if (productDescription === "") {
            message.textContent = "The productDescription is empty";
            return;
        } else if (Number.isNaN(price) || price <= 0) {
            message.textContent = "the price is none";
            return;
        } else if (Number.isNaN(stock) || stock < 0) {
            message.textContent = "the stock is none";
            return;
        } else if (Number.isNaN(categoryId) || categoryId < 1) {
            message.textContent = "categoryId is empty";
            return;
        } 
        try {
            await httpClient.request("/products/", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    description: productDescription,
                    price: price,
                    stock: stock,
                    category_id: categoryId,
                })
            });

        
        message.textContent = "Product created successfully!";
        } catch (error) {
            message.textContent = "Could not create product.";
        }

    });


    container.replaceChildren(form);

    return () => {
        form.remove();
    };

}