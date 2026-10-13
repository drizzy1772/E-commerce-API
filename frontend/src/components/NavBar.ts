


import AuthManager from '../auth/Auth';

    interface NavLink {
        path: string;
        label: string;
        allowedRoles?: string[];
    }

    const NAV_LINKS: NavLink[] = [
        { path: "/cart", label: "Cart" },
        { path: "/products", label: "Catalog" },
        { path: "/", label: "Dashboard" },
        { path: "/orders", label: "Orders" },
        { path: "/users", label: "Users (Admin)", allowedRoles: ["admin"] },
        { path: "/admin/products", label: "Create Product", allowedRoles: ["admin"] }
    ];

    export function renderNavBar(container: HTMLElement, authManager: AuthManager) {
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
            `;

            NAV_LINKS.forEach(link => {
                if (!link.allowedRoles || (state.role && link.allowedRoles.includes(state.role))) {
                    const extraClass = link.allowedRoles ? ' class="admin-link"' : '';
                    navHtml += `<a href="${link.path}" data-link${extraClass}>${link.label}</a>`;
                }
            });
            
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
                });
            }
        };
        
        updateDOM();

        authManager.onChange(() => {
            updateDOM();
        });
    }