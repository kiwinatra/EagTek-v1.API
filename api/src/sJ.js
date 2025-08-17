  hljs.highlightAll();

        const themeToggle = document.getElementById('themeToggle');
        themeToggle.addEventListener('click', function() {
            document.documentElement.classList.toggle('dark');
            localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
        });

        if (localStorage.getItem('theme') === 'dark' || 
            (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        }

        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.querySelector('aside');
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('hidden');
        });

        document.querySelectorAll('[data-tab]').forEach(tab => {
            tab.addEventListener('click', function() {
                const tabId = this.getAttribute('data-tab');

                document.querySelectorAll('.response-tab-content').forEach(content => {
                    content.classList.add('hidden');
                });

                document.querySelectorAll('.tab-button, .response-tab-button').forEach(btn => {
                    btn.classList.remove('active');
                });

                document.getElementById(`${tabId}-tab`).classList.remove('hidden');

                this.classList.add('active');
            });
        });

        document.querySelectorAll('pre').forEach(pre => {
            const copyBtn = pre.querySelector('.copy-btn');
            if (copyBtn) {
                copyBtn.addEventListener('click', function() {
                    const code = pre.querySelector('code').textContent;
                    navigator.clipboard.writeText(code).then(() => {
                        const originalInnerHTML = this.innerHTML;
                        this.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
                        setTimeout(() => {
                            this.innerHTML = originalInnerHTML;
                        }, 2000);
                    });
                });
            }
        });

        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function(e) {
                e.preventDefault();

                const targetId = this.getAttribute('href');
                const targetElement = document.querySelector(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });

                    history.pushState(null, null, targetId);

                    if (!sidebar.classList.contains('hidden')) {
                        sidebar.classList.add('hidden');
                    }
                }
            });
        });

        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                const id = entry.target.getAttribute('id');
                if (entry.intersectionRatio > 0.2) {
                    document.querySelectorAll(`a[href="#${id}"]`).forEach(link => {
                        link.classList.add('active');
                    });
                } else {
                    document.querySelectorAll(`a[href="#${id}"]`).forEach(link => {
                        link.classList.remove('active');
                    });
                }
            });
        }, { threshold: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1] });

        document.querySelectorAll('section[id]').forEach(section => {
            observer.observe(section);
        });

        const backToTopBtn = document.getElementById('backToTop');
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.remove('opacity-0', 'invisible', 'translate-y-2');
                backToTopBtn.classList.add('opacity-100', 'visible', 'translate-y-0');
            } else {
                backToTopBtn.classList.add('opacity-0', 'invisible', 'translate-y-2');
                backToTopBtn.classList.remove('opacity-100', 'visible', 'translate-y-0');
            }
        });

        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        document.documentElement.style.scrollPaddingTop = '80px';