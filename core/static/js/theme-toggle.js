// ================================================
// SISTEMA DE TOGGLE DE TEMA - PSIu
// ================================================

class ThemeManager {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.init();
    }

    init() {
        // Detectar preferência do sistema
        if (!localStorage.getItem('theme')) {
            const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
            this.theme = prefersDark ? 'dark' : 'light';
        }

        // Aplicar tema inicial
        this.applyTheme();

        // Escutar mudanças na preferência do sistema
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.theme = e.matches ? 'dark' : 'light';
                this.applyTheme();
            }
        });

        // Criar botão de toggle
        this.createToggleButton();
    }

    applyTheme() {
        document.documentElement.setAttribute('data-theme', this.theme);
        localStorage.setItem('theme', this.theme);
        this.updateToggleButton();
    }

    toggleTheme() {
        this.theme = this.theme === 'light' ? 'dark' : 'light';
        this.applyTheme();
    }

    createToggleButton() {
        // Criar botão
        const button = document.createElement('button');
        button.className = 'theme-toggle btn btn-outline-light btn-sm me-2';
        button.setAttribute('aria-label', 'Alternar tema');
        button.innerHTML = this.theme === 'light' ? '🌙' : '☀️';

        // Adicionar evento de clique
        button.addEventListener('click', () => this.toggleTheme());

        // Inserir no navbar entre "Olá user" e "Buscar" (para usuários logados)
        const navbarContent = document.querySelector('#navbarContent');
        if (navbarContent) {
            const desktopMenu = navbarContent.querySelector('.d-none.d-lg-flex');
            if (desktopMenu) {
                // Encontrar o span com "Olá user" e inserir o botão depois dele
                const greetingSpan = desktopMenu.querySelector('span.text-white');
                if (greetingSpan) {
                    greetingSpan.insertAdjacentElement('afterend', button);
                } else {
                    desktopMenu.appendChild(button);
                }
            }

            // Para mobile - inserir após a saudação
            const mobileMenu = navbarContent.querySelector('.d-flex.flex-column.d-lg-none');
            if (mobileMenu) {
                const greetingSpan = mobileMenu.querySelector('span.text-white');
                if (greetingSpan) {
                    const toggleMobile = button.cloneNode(true);
                    toggleMobile.addEventListener('click', () => this.toggleTheme());
                    toggleMobile.classList.add('w-100', 'mb-2');
                    greetingSpan.insertAdjacentElement('afterend', toggleMobile);
                }
            }
        }

        // Para usuários não logados, o botão já está no HTML, apenas atualizar
        const existingButton = document.getElementById('theme-toggle');
        if (existingButton) {
            existingButton.innerHTML = this.theme === 'light' ? '🌙' : '☀️';
            existingButton.addEventListener('click', () => this.toggleTheme());
        }
    }

    updateToggleButton() {
        const buttons = document.querySelectorAll('.theme-toggle, #theme-toggle');
        buttons.forEach(button => {
            button.innerHTML = this.theme === 'light' ? '🌙' : '☀️';
            button.setAttribute('aria-label',
                this.theme === 'light' ? 'Mudar para tema escuro' : 'Mudar para tema claro'
            );
        });
    }
}

// Inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    new ThemeManager();
});
