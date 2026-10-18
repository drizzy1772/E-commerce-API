<script setup lang="ts">
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { listProducts, type Product } from "../api/products";
import { useAuth } from "../stores/auth";
import { useCart } from "../stores/cart";

const SIZE = 12;
const auth = useAuth();
const cart = useCart();
const router = useRouter();

const items = ref<Product[]>([]);
const total = ref<number | undefined>();
const search = ref("");
const page = ref(1);
const loading = ref(true);
const error = ref("");
const pending = ref<(number | string)[]>([]); // products being added right now
const addError = ref("");

let timer: ReturnType<typeof setTimeout>;

async function load() {
  loading.value = true;
  error.value = "";
  try {
    const data = await listProducts({ search: search.value, page: page.value, size: SIZE });
    items.value = data.items;
    total.value = data.total;
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    loading.value = false;
  }
}

async function addToCart(p: Product) {
  if (!auth.isLoggedIn) return router.push({ path: "/login", query: { next: "/" } });
  pending.value.push(p.id);
  addError.value = "";
  try {
    await cart.add(p);
  } catch (e) {
    addError.value = `Couldn't add "${p.name}": ${(e as Error).message}`;
  } finally {
    pending.value = pending.value.filter((id) => id !== p.id);
  }
}

watch(search, () => {
  clearTimeout(timer);
  timer = setTimeout(() => { page.value = 1; load(); }, 300);
});
watch(page, load);
load();

const hasNext = () => (total.value !== undefined ? page.value * SIZE < total.value : items.value.length === SIZE);
</script>

<template>
  <div class="head">
    <h1>Products</h1>
    <input v-model="search" type="search" placeholder="Search products" aria-label="Search products" />
  </div>

  <p v-if="addError" class="error" role="alert">{{ addError }}</p>
  <p v-if="loading" class="muted">Loading products...</p>
  <div v-else-if="error" class="panel">
    <p class="error" role="alert">{{ error }}</p>
    <button class="btn btn--small" @click="load">Try again</button>
  </div>
  <p v-else-if="!items.length" class="muted">No products match your search.</p>

  <ul v-else class="grid">
    <li v-for="p in items" :key="p.id" class="card">
      <h2>{{ p.name }}</h2>
      <p v-if="p.description" class="muted clamp">{{ p.description }}</p>
      <div class="row">
        <strong>${{ Number(p.price).toFixed(2) }}</strong>
        <button class="btn btn--small" :disabled="pending.includes(p.id)" @click="addToCart(p)">
          {{ pending.includes(p.id) ? "Adding..." : "Add to cart" }}
        </button>
      </div>
    </li>
  </ul>

  <div v-if="!loading && !error && items.length" class="pager">
    <button class="btn btn--ghost btn--small" :disabled="page === 1" @click="page--">Previous</button>
    <span class="muted">Page {{ page }}</span>
    <button class="btn btn--ghost btn--small" :disabled="!hasNext()" @click="page++">Next</button>
  </div>
</template>
