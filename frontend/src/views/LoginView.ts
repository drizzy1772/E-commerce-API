





import AuthManager from "../auth/Auth";
import Router from "../router/Router";

export function LoginView(container: HTMLElement, authManager: AuthManager, router: Router) {
    
    container.innerHTML = "";
    
    const form = document.createElement("form");
    form.innerHTML = `
        <div style="padding: 20px; max-width: 300px; margin: 0 auto;">
            <h2>Enter</h2>
            <input type="email" id="email" placeholder="Email" required style="display:block; margin-bottom:10px; width:100%;" />
            <input type="password" id="password" placeholder="Password" required style="display:block; margin-bottom:10px; width:100%;" />
            <button type="submit" id="submit-btn" style="width:100%;">Login</button>
            <p id="error-msg" style="color: red;"></p>
        </div>
    
    `;

    const emailInput = form.querySelector("#email") as HTMLInputElement;
    const passwordInput = form.querySelector("#password") as HTMLInputElement;
    const submitBtn = form.querySelector("#submit-btn") as HTMLButtonElement;
    const errorMsg = form.querySelector("#error-msg") as HTMLParagraphElement;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        console.log("Button clicked");
        console.log("Email:", emailInput.value);
        console.log("Password", passwordInput.value);

        submitBtn.textContent = "Loading"
        submitBtn.disabled = true;
        errorMsg.textContent = ""

        try {
            await authManager.login(emailInput.value, passwordInput.value);
            router.navigate("/");
        } catch (error: any) {
            errorMsg.textContent = error.message;
        } finally {
            submitBtn.textContent = "Login";
            submitBtn.disabled = false;
        }
    });

    container.appendChild(form);
}