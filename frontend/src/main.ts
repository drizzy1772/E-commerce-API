





import AuthManager from "./auth/Auth";
import Router from "./router/Router";
import { LoginView } from "./views/LoginView";
import { DashboardView } from "./views/DashboardView";
import { renderNavBar } from "./components/NavBar";
import { OrdersView } from "./views/OrdersView";
import HttpClient from "./api/HttpClient";
import { CartItemsView } from "./views/CartItemsView";
import { UsersView } from "./views/UsersView";
import { ProductCatalogView } from "./views/ProductCatalogView";



const container = document.getElementById('app');

const navContainer = document.getElementById("nav-container");


if (!container || !navContainer) {
  throw new Error("Required DOM elements were not found in index.html");
}

const authManager = new AuthManager();
const router = new Router(authManager, container);
const httpClient = new HttpClient(authManager);


const NAV_LINKS = [
  { path: "/orders", label: "Orders"},
  { path: "/cart", label: "Cart"},
  { path: "/users", label: "Users", allowedRoles: ["admin"]},
  { path: "/products", label: "Catalog" }
]

renderNavBar(navContainer, authManager, NAV_LINKS);

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


router.register({
  path: "/cart",
  requiresAuth: true,
  view: (container: HTMLElement) => CartItemsView(container, httpClient, router)
});


router.register({
  path: "/users",
  requiresAuth: true,
  allowedRoles: ["admin"],
  view: (container: HTMLElement) => UsersView(container, httpClient, router)
});

router.register({
  path: "/products",
  requiresAuth: true,
  view: (container: HTMLElement) => ProductCatalogView(container, httpClient, router)
});

router.start();


