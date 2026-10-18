// The API has no "get cart" route yet, so the visible cart lives here
// (saved in localStorage). Adding an item still calls POST /cart/items.
import { computed, ref, watch } from "vue";
import { defineStore } from "pinia";
import { request } from "../api/http";
import type { Product } from "../api/products";

export interface CartLine {
  productId: number | string;
  name: string;
  price: number;
  quantity: number;
}

function load(): CartLine[] {
  try { return JSON.parse(localStorage.getItem("cart") ?? "[]"); } catch { return []; }
}

export const useCart = defineStore("cart", () => {
  const lines = ref<CartLine[]>(load());
  const count = computed(() => lines.value.reduce((n, l) => n + l.quantity, 0));
  const total = computed(() => lines.value.reduce((s, l) => s + l.price * l.quantity, 0));

  watch(lines, (v) => {
    try { localStorage.setItem("cart", JSON.stringify(v)); } catch { /* ignore */ }
  }, { deep: true });

  async function add(p: Product) {
    await request("/cart/items", {
      method: "POST",
      body: JSON.stringify({ product_id: p.id, quantity: 1 }),
    });
    const line = lines.value.find((l) => l.productId === p.id);
    if (line) line.quantity++;
    else lines.value.push({ productId: p.id, name: p.name, price: p.price, quantity: 1 });
  }

  function remove(productId: number | string) {
    lines.value = lines.value.filter((l) => l.productId !== productId);
  }

  async function checkout() {
    const order = await request<{ id: number | string }>("/orders", { method: "POST" });
    lines.value = [];
    return order;
  }

  return { lines, count, total, add, remove, checkout };
});
