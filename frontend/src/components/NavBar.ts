


import AuthManager from '../auth/Auth';

export function renderNavBar(container: HTMLElement, authManager: AuthManager, _links: any = []) {
    const updateDOM = () => {
        const state = authManager.getState();
    
    if (!state.isAuthenticated) {
        container.innerHTML = `
            <nav class="navbar">
                    <strong>E-Commerce API</strong>
                    <div class="nav-links">
                        <a href="/login" data-link>Login</a>
                    </div>
            </nav>
        `;
        return;
    }
    
    let navHtml = `
        <nav class="navbar">
                <strong>E-Commerce API</strong>
                <div class="nav-links">
                    <a href="/cart" data-link>Cart</a>
                    <a href="/products" data-link>Catalog</a>
                    <a href="/" data-link>Dashboard</a>
                    <a href="/orders" data-link>Orders</a>
    `;

    if (state.role === "admin") {
        navHtml += `
                <a href="/users" data-link class="admin-link">
                    Users (Admin)
                </a>
                <a href="/admin/products" data-link class="admin-link">
                    Create Product
                </a>
        `;
    }

    navHtml += `
            </div>
            <div class="user-controls">
                <span class="user-email">Profile</span>
                <button id="logout-btn">Logout</button>
            </div>
        </nav>
    `;

    container.innerHTML = navHtml;

    const logoutBtn =  container.querySelector('#logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            authManager.logout();
        })
    }
};

updateDOM();

authManager.onChange(() => {
    updateDOM();
});
}
