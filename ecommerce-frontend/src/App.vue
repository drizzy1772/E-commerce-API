<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuth } from "./stores/auth";
import { useCart } from "./stores/cart";

const auth = useAuth();
const cart = useCart();
const router = useRouter();

function logout() {
  auth.logout();
  router.push("/login");
}
</script>

<template>
  <header class="bar">
    <RouterLink to="/" class="brand">Store</RouterLink>
    <nav>
      <RouterLink to="/">Products</RouterLink>
      <RouterLink to="/cart">Cart<span v-if="cart.count" class="badge">{{ cart.count }}</span></RouterLink>
      <template v-if="auth.isLoggedIn">
        <button class="link" @click="logout">Sign out</button>
      </template>
      <template v-else>
        <RouterLink to="/login">Sign in</RouterLink>
        <RouterLink to="/register" class="btn btn--small">Create account</RouterLink>
      </template>
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
</template>
