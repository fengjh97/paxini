/* ================================================
   炭火焼肉 SUMIRE — Interactive JS

   Skills Used:
   - frontend-design: Motion design, micro-interactions
   - threejs-builder concepts: Particle system (ember canvas)
   - canvas-design concepts: Fire ember particle art
   ================================================ */

document.addEventListener('DOMContentLoaded', () => {
    initCursor();
    initNav();
    initRevealAnimations();
    initEmberParticles();
    initMenuTabs();
    initGalleryDrag();
    initParallax();
});

/* === Custom Cursor === */
function initCursor() {
    const cursor = document.getElementById('cursor');
    const follower = document.getElementById('cursorFollower');
    if (!cursor || !follower || window.innerWidth < 769) return;

    let mx = 0, my = 0, cx = 0, cy = 0, fx = 0, fy = 0;

    document.addEventListener('mousemove', e => {
        mx = e.clientX;
        my = e.clientY;
    });

    (function loop() {
        cx += (mx - cx) * 0.15;
        cy += (my - cy) * 0.15;
        fx += (mx - fx) * 0.08;
        fy += (my - fy) * 0.08;
        cursor.style.left = cx + 'px';
        cursor.style.top = cy + 'px';
        follower.style.left = fx + 'px';
        follower.style.top = fy + 'px';
        requestAnimationFrame(loop);
    })();
}

/* === Navigation === */
function initNav() {
    const nav = document.getElementById('nav');
    const burger = document.getElementById('navBurger');
    const links = document.getElementById('navLinks');

    window.addEventListener('scroll', () => {
        nav.classList.toggle('scrolled', window.scrollY > 80);
    });

    // Smooth scroll
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(a.getAttribute('href'));
            if (target) {
                const offset = nav.offsetHeight + 20;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });
}

/* === Scroll Reveal (GSAP ScrollTrigger) === */
function initRevealAnimations() {
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        // Fallback: Intersection Observer
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) entry.target.classList.add('visible');
            });
        }, { threshold: 0.15 });
        document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    // Reveal elements
    gsap.utils.toArray('.reveal').forEach(el => {
        ScrollTrigger.create({
            trigger: el,
            start: 'top 88%',
            onEnter: () => el.classList.add('visible'),
        });
    });

    // Hero parallax
    const heroImg = document.querySelector('.hero-img');
    if (heroImg) {
        gsap.to(heroImg, {
            yPercent: 15,
            ease: 'none',
            scrollTrigger: {
                trigger: '.hero',
                start: 'top top',
                end: 'bottom top',
                scrub: 1,
            }
        });
    }

    // Gallery horizontal scroll trigger (subtle)
    const galleryTrack = document.querySelector('.gallery-track');
    if (galleryTrack) {
        gsap.to(galleryTrack, {
            x: -100,
            ease: 'none',
            scrollTrigger: {
                trigger: '.section-gallery',
                start: 'top bottom',
                end: 'bottom top',
                scrub: 2,
            }
        });
    }

    // About images stagger
    gsap.utils.toArray('.about-img-main, .about-img-accent').forEach((el, i) => {
        gsap.fromTo(el, { y: 40 + i * 30 }, {
            y: -20 - i * 20,
            ease: 'none',
            scrollTrigger: {
                trigger: el,
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1,
            }
        });
    });
}

/* === Ember Particles (canvas-design: fire ember art) === */
function initEmberParticles() {
    const canvas = document.getElementById('emberCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let w, h;
    const embers = [];
    const EMBER_COUNT = 60;

    function resize() {
        const hero = canvas.parentElement;
        w = canvas.width = hero.offsetWidth;
        h = canvas.height = hero.offsetHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Ember class
    class Ember {
        constructor() {
            this.reset();
        }
        reset() {
            this.x = Math.random() * w;
            this.y = h + Math.random() * 100;
            this.size = Math.random() * 3 + 1;
            this.speedY = -(Math.random() * 1.5 + 0.3);
            this.speedX = (Math.random() - 0.5) * 0.8;
            this.opacity = Math.random() * 0.8 + 0.2;
            this.decay = Math.random() * 0.003 + 0.001;
            this.wobble = Math.random() * Math.PI * 2;
            this.wobbleSpeed = Math.random() * 0.02 + 0.01;
            // Color: warm orange to red
            const t = Math.random();
            this.r = 200 + Math.floor(t * 55);
            this.g = 100 + Math.floor(t * 65);
            this.b = 20 + Math.floor(t * 30);
        }
        update() {
            this.wobble += this.wobbleSpeed;
            this.x += this.speedX + Math.sin(this.wobble) * 0.3;
            this.y += this.speedY;
            this.opacity -= this.decay;
            if (this.opacity <= 0 || this.y < -20) this.reset();
        }
        draw() {
            ctx.save();
            ctx.globalAlpha = this.opacity;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = `rgb(${this.r}, ${this.g}, ${this.b})`;
            ctx.fill();
            // Glow
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 4, 0, Math.PI * 2);
            const grd = ctx.createRadialGradient(this.x, this.y, 0, this.x, this.y, this.size * 4);
            grd.addColorStop(0, `rgba(${this.r}, ${this.g}, ${this.b}, ${this.opacity * 0.3})`);
            grd.addColorStop(1, 'rgba(0, 0, 0, 0)');
            ctx.fillStyle = grd;
            ctx.fill();
            ctx.restore();
        }
    }

    for (let i = 0; i < EMBER_COUNT; i++) {
        const e = new Ember();
        e.y = Math.random() * h; // Spread initially
        embers.push(e);
    }

    function animate() {
        ctx.clearRect(0, 0, w, h);
        embers.forEach(e => {
            e.update();
            e.draw();
        });
        requestAnimationFrame(animate);
    }
    animate();
}

/* === Menu Tabs === */
function initMenuTabs() {
    const tabs = document.querySelectorAll('.menu-tab');
    const panels = document.querySelectorAll('.menu-panel');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const target = tab.dataset.tab;

            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            panels.forEach(p => {
                p.classList.remove('active');
                if (p.id === 'panel-' + target) {
                    p.classList.add('active');
                    // Re-trigger reveal for items inside
                    p.querySelectorAll('.reveal:not(.visible)').forEach(el => {
                        el.classList.add('visible');
                    });
                }
            });
        });
    });
}

/* === Gallery Drag Scroll === */
function initGalleryDrag() {
    const scroll = document.querySelector('.gallery-scroll');
    if (!scroll) return;

    let isDown = false, startX, scrollLeft;

    scroll.addEventListener('mousedown', e => {
        isDown = true;
        startX = e.pageX - scroll.offsetLeft;
        scrollLeft = scroll.scrollLeft;
    });

    scroll.addEventListener('mouseleave', () => isDown = false);
    scroll.addEventListener('mouseup', () => isDown = false);

    scroll.addEventListener('mousemove', e => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - scroll.offsetLeft;
        const walk = (x - startX) * 2;
        scroll.scrollLeft = scrollLeft - walk;
    });

    // Touch support
    let touchStartX, touchScrollLeft;
    scroll.addEventListener('touchstart', e => {
        touchStartX = e.touches[0].pageX;
        touchScrollLeft = scroll.scrollLeft;
    });

    scroll.addEventListener('touchmove', e => {
        const x = e.touches[0].pageX;
        const walk = (touchStartX - x) * 1.5;
        scroll.scrollLeft = touchScrollLeft + walk;
    });
}

/* === Parallax for reserve bg === */
function initParallax() {
    const reserveBg = document.querySelector('.reserve-bg img');
    if (!reserveBg) return;

    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.to(reserveBg, {
            yPercent: 20,
            ease: 'none',
            scrollTrigger: {
                trigger: '.section-reserve',
                start: 'top bottom',
                end: 'bottom top',
                scrub: 1,
            }
        });
    }
}
