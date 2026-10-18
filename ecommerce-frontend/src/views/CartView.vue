<script setup lang="ts">
import { ref } from "vue";
import { useCart } from "../stores/cart";

const cart = useCart();
const busy = ref(false);
const error = ref("");
const placedId = ref<number | string | null>(null);

async function checkout() {
  busy.value = true;
  error.value = "";
  try {
    const order = await cart.checkout();
    placedId.value = order.id;
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <h1>Cart</h1>

  <div v-if="placedId !== null" class="panel">
    <h2>Order placed</h2>
    <p>Your order number is {{ placedId }}. We'll email you when its status changes.</p>
    <RouterLink to="/" class="btn">Keep shopping</RouterLink>
  </div>

  <p v-else-if="!cart.lines.length" class="muted">
    Your cart is empty. <RouterLink to="/">Browse products</RouterLink>
  </p>

  <template v-else>
    <ul class="list">
      <li v-for="l in cart.lines" :key="l.productId" class="row card">
        <span>{{ l.name }} <span class="muted">x {{ l.quantity }}</span></span>
        <span class="row">
          <strong>${{ (l.price * l.quantity).toFixed(2) }}</strong>
          <button class="btn btn--danger btn--small" @click="cart.remove(l.productId)">Remove</button>
        </span>
      </li>
    </ul>
    <div class="row total">
      <strong>Total ${{ cart.total.toFixed(2) }}</strong>
      <button class="btn" :disabled="busy" @click="checkout">{{ busy ? "Placing order..." : "Place order" }}</button>
    </div>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
  </template>
</template>
