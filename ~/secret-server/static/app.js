// API Base URL
const API_BASE = '';

// State
let currentUser = null;
let loginPassphrase = null;

// DOM Elements
const authScreen = document.getElementById('auth-screen');
const dashboardScreen = document.getElementById('dashboard-screen');
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const tabBtns = document.querySelectorAll('.tab-btn');
const usernameDisplay = document.getElementById('username-display');
const logoutBtn = document.getElementById('logout-btn');
const newSecretBtn = document.getElementById('new-secret-btn');
const appsGrid = document.getElementById('apps-grid');
const emptyState = document.getElementById('empty-state');

// Modals
const storeModal = document.getElementById('store-modal');
const retrieveModal = document.getElementById('retrieve-modal');
const updateModal = document.getElementById('update-modal');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    checkAuthStatus();
    setupEventListeners();
});

// Check if user is already authenticated
async function checkAuthStatus() {
    try {
        const response = await fetch(`${API_BASE}/api/auth/check`);
        const data = await response.json();

        if (data.authenticated) {
            currentUser = data.username;
            loginPassphrase = data.password;
            showDashboard();
        }
    } catch (error) {
        console.error('Auth check failed:', error);
    }
}

// Event Listeners
function setupEventListeners() {
    // Tab switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tab = btn.dataset.tab;
            switchTab(tab);
        });
    });

    // Forms
    loginForm.addEventListener('submit', handleLogin);
    registerForm.addEventListener('submit', handleRegister);
    document.getElementById('store-form').addEventListener('submit', handleStore);
    document.getElementById('retrieve-form').addEventListener('submit', handleRetrieve);
    document.getElementById('update-form').addEventListener('submit', handleUpdate);
    document.getElementById('unlock-edit-btn').addEventListener('click', handleUnlockEdit);

    // Buttons
    logoutBtn.addEventListener('click', handleLogout);
    newSecretBtn.addEventListener('click', () => openModal('store-modal'));

    // Visibility toggles
    document.querySelectorAll('.password-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.dataset.target;
            const input = document.getElementById(targetId);
            if (input.type === 'password') {
                input.type = 'text';
                btn.textContent = '🙈';
            } else {
                input.type = 'password';
                btn.textContent = '👁️';
            }
        });
    });

    document.getElementById('toggle-result-visibility').addEventListener('click', toggleResultVisibility);

    // Modal close buttons
    document.querySelectorAll('[data-modal]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            closeModal(btn.dataset.modal);
        });
    });

    // Copy button
    document.getElementById('copy-secret-btn').addEventListener('click', copySecret);

    // Close modal on background click
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModal(modal.id);
            }
        });
    });
}

// Tab Switching
function switchTab(tab) {
    tabBtns.forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');

    loginForm.classList.remove('active');
    registerForm.classList.remove('active');

    if (tab === 'login') {
        loginForm.classList.add('active');
    } else {
        registerForm.classList.add('active');
    }
}

// Authentication Handlers
async function handleLogin(e) {
    e.preventDefault();

    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorEl = document.getElementById('login-error');

    try {
        const response = await fetch(`${API_BASE}/api/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.username;
            loginPassphrase = data.password;
            showDashboard();
        } else {
            showError(errorEl, data.error || 'Login failed');
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
    }
}

async function handleRegister(e) {
    e.preventDefault();

    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirmPassword = document.getElementById('register-password-confirm').value;
    const errorEl = document.getElementById('register-error');

    if (password !== confirmPassword) {
        showError(errorEl, 'Passwords do not match');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.username;
            loginPassphrase = data.password;
            showDashboard();
        } else {
            showError(errorEl, data.error || 'Registration failed');
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
    }
}

async function handleLogout() {
    try {
        await fetch(`${API_BASE}/api/auth/logout`, { method: 'POST' });
        currentUser = null;
        showAuth();
    } catch (error) {
        console.error('Logout failed:', error);
    }
}

// Screen Management
function showDashboard() {
    authScreen.classList.remove('active');
    dashboardScreen.classList.add('active');
    usernameDisplay.textContent = currentUser;
    loadApps();
}

function showAuth() {
    dashboardScreen.classList.remove('active');
    authScreen.classList.add('active');
    loginForm.reset();
    registerForm.reset();
}

// Load Apps
async function loadApps() {
    try {
        const response = await fetch(`${API_BASE}/api/apps`);
        const data = await response.json();

        if (data.apps && data.apps.length > 0) {
            renderApps(data.apps);
            emptyState.classList.remove('show');
        } else {
            appsGrid.innerHTML = '';
            emptyState.classList.add('show');
        }
    } catch (error) {
        console.error('Failed to load apps:', error);
    }
}

function renderApps(apps) {
    appsGrid.innerHTML = apps.map(app => `
        <div class="app-card">
            <div class="app-card-header">
                <div class="app-icon">🔑</div>
                <div class="app-actions">
                    <button class="icon-btn" onclick="openRetrieveModal('${app.name}')" title="View Secret">👁️</button>
                    <button class="icon-btn" onclick="openUpdateModal('${app.name}')" title="Update Secret">✏️</button>
                </div>
            </div>
            <div class="app-name">${escapeHtml(app.name)}</div>
            <div class="app-meta">
                Updated: ${new Date(app.modified * 1000).toLocaleDateString()}
            </div>
        </div>
    `).join('');
}

// Secret Operations
async function handleStore(e) {
    e.preventDefault();

    const appName = document.getElementById('store-app-name').value;
    const appUsername = document.getElementById('store-app-username').value;
    const secretText = document.getElementById('store-secret').value;
    const passphrase = document.getElementById('store-passphrase').value;
    const errorEl = document.getElementById('store-error');

    try {
        const response = await fetch(`${API_BASE}/api/secrets/store`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                app_name: appName,
                app_username: appUsername,
                secret_text: secretText,
                passphrase: passphrase
            })
        });

        const data = await response.json();

        if (response.ok) {
            closeModal('store-modal');
            document.getElementById('store-form').reset();
            loadApps();
        } else {
            showError(errorEl, data.error || 'Failed to store secret');
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
    }
}

async function handleRetrieve(e) {
    e.preventDefault();

    const appName = document.getElementById('retrieve-app-name').value;
    const passphrase = document.getElementById('retrieve-passphrase').value;
    const errorEl = document.getElementById('retrieve-error');
    const resultEl = document.getElementById('retrieve-result');

    try {
        const response = await fetch(`${API_BASE}/api/secrets/retrieve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                app_name: appName,
                passphrase: passphrase
            })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('result-username').textContent = data.app_username;
            document.getElementById('result-timestamp').textContent = data.timestamp;
            document.getElementById('result-secret').textContent = data.secret;
            resultEl.style.display = 'block';
            errorEl.classList.remove('show');
        } else {
            showError(errorEl, data.error || 'Failed to retrieve secret');
            resultEl.style.display = 'none';
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
        resultEl.style.display = 'none';
    }
}

async function handleUpdate(e) {
    e.preventDefault();

    const appName = document.getElementById('update-app-name').value;
    const passphrase = document.getElementById('update-passphrase').value;
    const value = document.getElementById('update-value').value;
    const errorEl = document.getElementById('update-error');

    try {
        const response = await fetch(`${API_BASE}/api/secrets/update`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                app_name: appName,
                passphrase: passphrase,
                key_path: "", // Send empty to trigger full overwrite
                value: value
            })
        });

        const data = await response.json();

        if (response.ok) {
            closeModal('update-modal');
            loadApps(); // Refresh the list
        } else {
            showError(errorEl, data.error || 'Failed to update secret');
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
    }
}

async function handleUnlockEdit() {
    const appName = document.getElementById('update-app-name').value;
    const passphrase = document.getElementById('update-passphrase').value;
    const errorEl = document.getElementById('update-error');
    const unlockSection = document.getElementById('update-unlock-section');
    const editorSection = document.getElementById('update-editor-section');
    const textarea = document.getElementById('update-value');

    if (!passphrase) {
        showError(errorEl, 'Passphrase required to unlock');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/api/secrets/retrieve`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                app_name: appName,
                passphrase: passphrase
            })
        });

        const data = await response.json();

        if (response.ok) {
            textarea.value = data.secret;
            unlockSection.style.display = 'none';
            editorSection.style.display = 'block';
            errorEl.classList.remove('show');
        } else {
            showError(errorEl, data.error || 'Failed to unlock secret');
        }
    } catch (error) {
        showError(errorEl, 'Network error. Please try again.');
    }
}

// Modal Management
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('active');

    // Reset result displays
    if (modalId === 'retrieve-modal') {
        document.getElementById('retrieve-result').style.display = 'none';
        document.getElementById('retrieve-form').reset();
    } else if (modalId === 'update-modal') {
        document.getElementById('update-result').style.display = 'none';
        document.getElementById('update-form').reset();
    }

    // Pre-fill passphrase if available
    if (loginPassphrase) {
        if (modalId === 'store-modal') {
            document.getElementById('store-passphrase').value = loginPassphrase;
        } else if (modalId === 'retrieve-modal') {
            document.getElementById('retrieve-passphrase').value = loginPassphrase;
        } else if (modalId === 'update-modal') {
            document.getElementById('update-passphrase').value = loginPassphrase;
        }
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
}

function openRetrieveModal(appName) {
    document.getElementById('retrieve-app-name').value = appName;
    openModal('retrieve-modal');
}

function openUpdateModal(appName) {
    document.getElementById('update-app-name').value = appName;
    document.getElementById('update-value').value = '';
    document.getElementById('update-unlock-section').style.display = 'block';
    document.getElementById('update-editor-section').style.display = 'none';
    openModal('update-modal');
}

// Copy Secret
function copySecret() {
    const secretText = document.getElementById('result-secret').textContent;
    navigator.clipboard.writeText(secretText).then(() => {
        const btn = document.getElementById('copy-secret-btn');
        btn.textContent = 'Copied!';
        setTimeout(() => {
            btn.textContent = 'Copy';
        }, 2000);
    });
}

function toggleResultVisibility() {
    const secretEl = document.getElementById('result-secret');
    const toggleBtn = document.getElementById('toggle-result-visibility');

    if (secretEl.classList.contains('blurred-content')) {
        secretEl.classList.remove('blurred-content');
        toggleBtn.textContent = 'Hide';
    } else {
        secretEl.classList.add('blurred-content');
        toggleBtn.textContent = 'Show';
    }
}

// Utility Functions
function showError(element, message) {
    element.textContent = message;
    element.classList.add('show');
    setTimeout(() => {
        element.classList.remove('show');
    }, 5000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
