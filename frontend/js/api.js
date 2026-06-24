const API_BASE_URL = "http://127.0.0.1:5000/api";

function getToken() {
    return localStorage.getItem("fintrack_token");
}

function setAuth(token, user) {
    localStorage.setItem("fintrack_token", token);
    localStorage.setItem("fintrack_user", JSON.stringify(user));
}

function getUser() {
    const raw = localStorage.getItem("fintrack_user");
    return raw ? JSON.parse(raw) : null;
}

function clearAuth() {
    localStorage.removeItem("fintrack_token");
    localStorage.removeItem("fintrack_user");
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

function logout() {
    clearAuth();
    window.location.href = "login.html";
}

async function apiRequest(path, options = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(options.headers || {})
    };

    const token = getToken();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
        ...options,
        headers
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.message || "Request failed");
    }

    return data;
}