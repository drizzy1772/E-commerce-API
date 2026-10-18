<script setup lang="ts">
import { ref } from "vue";
import { useAuth } from "../stores/auth";

const auth = useAuth();
const email = ref("");
const password = ref("");
const error = ref("");
const done = ref(false);
const busy = ref(false);

async function submit() {
  busy.value = true;
  error.value = "";
  try {
    await auth.register(email.value, password.value);
    done.value = true;
  } catch (e) {
    error.value = (e as Error).message;
  } finally {
    busy.value = false;
  }
}
</script>

<template>
  <section v-if="done" class="panel narrow">
    <h1>Check your email</h1>
    <p>We sent a verification link to {{ email }}. Open it, then sign in.</p>
    <RouterLink to="/login" class="btn">Go to sign in</RouterLink>
  </section>
  <form v-else class="panel narrow" @submit.prevent="submit">
    <h1>Create account</h1>
    <label>Email<input v-model="email" type="email" autocomplete="email" required /></label>
    <label>Password<input v-model="password" type="password" autocomplete="new-password" minlength="8" required /></label>
    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <button class="btn" :disabled="busy">{{ busy ? "Creating..." : "Create account" }}</button>
    <p class="muted">Already registered? <RouterLink to="/login">Sign in</RouterLink></p>
  </form>
</template>
