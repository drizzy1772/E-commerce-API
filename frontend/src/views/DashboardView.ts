



import Router from "../router/Router";

export function DashboardView(container: HTMLElement, router: Router) {
    container.innerHTML = `
        <div style="padding: 20px;">
            <h2>Main panel</h2>
            <p>Welcome in system!</p>
            <button id="logout-btn">Exit</button>
        </div>
    `;


    const logoutBtn = container.querySelector("#logout-btn");
    logoutBtn?.addEventListener("click", () => {
        router.navigate("/login");
    });
}
