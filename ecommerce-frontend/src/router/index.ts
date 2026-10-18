import { createRouter, createWebHistory } from "vue-router";
import { useAuth } from "../stores/auth";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: "/", component: () => import("../views/ProductsView.vue") },
    { path: "/login", component: () => import("../views/LoginView.vue") },
    { path: "/register", component: () => import("../views/RegisterView.vue") },
    { path: "/cart", component: () => import("../views/CartView.vue"), meta: { requiresAuth: true } },
  ],
});

router.beforeEach((to) => {
  if (to.meta.requiresAuth && !useAuth().isLoggedIn) {
    return { path: "/login", query: { next: to.fullPath } };
  }
});

export default router;
