// ========================================
// Lastic Productions - Landing Page Script
// ========================================

// Splash screen messages
const SPLASH_MESSAGES = [
    "Tired of tools that never work?",
    "No more ads.",
    "No more struggling.",
    "Download your YouTube videos.",
    "Download MP3s.",
    "Everything in one place.",
    "Lastic Productions."
];

document.addEventListener('DOMContentLoaded', () => {
    // Mark body as splash-active to hide main content
    document.body.classList.add('splash-active');

    initSplashScreen();
    initTabs();
    initNavbar();
    initSmoothScroll();
});

/* ---------- Splash Screen Loader ---------- */
function initSplashScreen() {
    const splash = document.getElementById('splash-screen');
    const messageEl = document.getElementById('splash-message');
    const loaderFill = document.getElementById('loader-fill');
    const loaderText = document.getElementById('loader-text');
    const hintEl = document.querySelector('.splash-hint');

    let msgIndex = 0;

    // Cycle messages every 900ms
    const msgInterval = setInterval(() => {
        msgIndex = (msgIndex + 1) % SPLASH_MESSAGES.length;
        messageEl.style.opacity = 0;
        setTimeout(() => {
            messageEl.textContent = SPLASH_MESSAGES[msgIndex];
            messageEl.style.opacity = 1;
        }, 250);
    }, 900);

    // Random loader text updates
    const loaderTexts = ["Initializing...", "Loading engine...", "Preparing download core...", "Almost ready...", "Launching..."];
    let ltIndex = 0;
    const ltInterval = setInterval(() => {
        ltIndex = (ltIndex + 1) % loaderTexts.length;
        loaderText.textContent = loaderTexts[ltIndex];
    }, 1200);

    const hideSplash = () => {
        clearInterval(msgInterval);
        clearInterval(ltInterval);
        splash.classList.add('fade-out');
        document.body.classList.remove('splash-active');

        // Fully remove from DOM after transition
        setTimeout(() => {
            splash.style.display = 'none';
        }, 900);
    };

    // Auto hide after loader animation (5s)
    setTimeout(hideSplash, 5000);

    // Click to skip
    splash.addEventListener('click', (e) => {
        if (e.target === splash || e.target.closest('.splash-hint') || e.target.closest('.splash-content')) {
            hideSplash();
        }
    });

    // Keyboard skip
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === 'Escape' || e.key === ' ') {
            hideSplash();
        }
    }, { once: true });
}

/* ---------- Tab Switching ---------- */
function initTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabPanels = document.querySelectorAll('.tab-panel');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetTab = btn.getAttribute('data-tab');

            // Update buttons
            tabBtns.forEach(b => {
                b.classList.remove('active');
                b.setAttribute('aria-selected', 'false');
            });
            btn.classList.add('active');
            btn.setAttribute('aria-selected', 'true');

            // Update panels
            tabPanels.forEach(panel => {
                if (panel.id === `tab-${targetTab}`) {
                    panel.classList.add('active');
                } else {
                    panel.classList.remove('active');
                }
            });
        });
    });
}

/* ---------- Navbar Scroll Effect ---------- */
function initNavbar() {
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 60) {
            navbar.style.padding = '12px 0';
            navbar.style.background = 'rgba(5, 5, 7, 0.95)';
        } else {
            navbar.style.padding = '20px 0';
            navbar.style.background = 'linear-gradient(180deg, rgba(5,5,7,0.9), transparent)';
        }
    });
}

/* ---------- Smooth Scroll for Anchor Links ---------- */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                const offset = 80;
                const targetPosition = target.getBoundingClientRect().top + window.pageYOffset - offset;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/* ---------- Console Easter Egg ---------- */
console.log('%c Lastic Productions %c', 'background: #00d4ff; color: #000; padding: 4px 10px; font-family: Orbitron; font-weight: 900; font-size: 14px;', 'color: #00d4ff; font-family: Rajdhani; font-size: 14px;');
console.log('%c Studio Cyber - Multi-Platform Video Downloader %c https://github.com/kinkysweetfeet90-ship-it/lastic-productions-YT', 'color: #7b2cbf; font-family: Rajdhani; font-weight: 700;', 'color: #8b8ca3;');