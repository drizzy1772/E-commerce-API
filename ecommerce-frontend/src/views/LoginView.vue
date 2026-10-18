<script setup lang="ts">
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useAuth } from "../stores/auth";

const auth = useAuth();
const router = useRouter();
const route = useRoute();
const email = ref("");
const password = ref("");
const error = ref("");
const busy = ref(false);

async function submit() {
  busy.value = true;
  error.value = "";
  try {
    await auth.login(email.value, password.value);
    router.push((route.query.next as string) || "/");
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <form class="panel narrow" @submit.prevent="submit">
    <h1>Sign in</h1>
    <label>Email<input v-model="email" type="email" autocomplete="email" required /></label>
    <label>Password<input v-model="password" type="password" autocomplete="current-password" required /></label>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <button class="btn" :disabled="busy">{{ busy ? "Signing in..." : "Sign in" }}</button>
    <p class="muted">New here? <RouterLink to="/register">Create an account</RouterLink></p>
  </form>
</template>
