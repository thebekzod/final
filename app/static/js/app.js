const API_BASE = "";

function getToken() {
  return localStorage.getItem("token");
}

function setToken(token) {
  localStorage.setItem("token", token);
}

function clearToken() {
  localStorage.removeItem("token");
}

function getRole() {
  return localStorage.getItem("role");
}

function setRole(role) {
  localStorage.setItem("role", role);
}

function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = "/";
  }
}

async function fetchJSON(url, options = {}) {
  const headers = options.headers || {};
  const token = getToken();
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  const response = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...headers,
    },
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Request failed" }));
    throw new Error(error.detail || "Request failed");
  }
  return response.json();
}

function getLang() {
  return localStorage.getItem("lang") || "en";
}

function setLang(lang) {
  localStorage.setItem("lang", lang);
}

function applyTranslations(dict) {
  const lang = getLang();
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[lang] && dict[lang][key]) {
      el.textContent = dict[lang][key];
    }
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[lang] && dict[lang][key]) {
      el.setAttribute("placeholder", dict[lang][key]);
    }
  });
}

function bindLangToggle(dict) {
  const toggle = document.querySelector("[data-lang-toggle]");
  if (!toggle) return;
  toggle.addEventListener("click", () => {
    const next = getLang() === "en" ? "ru" : "en";
    setLang(next);
    applyTranslations(dict);
  });
  applyTranslations(dict);
}

function setActiveNav(id) {
  document.querySelectorAll("[data-nav]").forEach((el) => {
    el.classList.toggle("text-cyan-300", el.dataset.nav === id);
  });
}
