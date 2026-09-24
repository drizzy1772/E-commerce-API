





import AuthManager from "./auth/Auth";
import Router from "./router/Router";
import { LoginView } from "./views/LoginView";
import { DashboardView } from "./views/DashboardView";
import { renderNavBar } from "./components/NavBar";
import { OrdersView } from "./views/OrdersView";
import { HttpClient } from "./api/HttpClient";


const container = document.getElementById('app')!;

const navContainer = document.getElementById("nav-container");


if (!container || !navContainer) {
  throw new Error("Required DOM elements were not found in index.html");
}

const authManager = new AuthManager();
const router = new Router(authManager, container);
const httpClient = new HttpClient(authManager);


renderNavBar(navContainer, authManager);

router.register({
  path: "/login",
  requiresAuth: false,
  view: (container: HTMLElement) => LoginView(container, authManager, router)
});

router.register({
  path: "/",
  requiresAuth: true,
  view: (container: HTMLElement) => DashboardView(container, router)
});


router.register({
  path: "/orders",
  requiresAuth: true,
  view: (container: HTMLElement) => OrdersView(container, httpClient, router)
});

router.start();
