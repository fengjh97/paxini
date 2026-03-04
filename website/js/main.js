/* ================================================
   NexTalent AI — Ultra Premium Interactive JS
   Three.js + GSAP + ScrollTrigger + Particles
   ================================================ */

// Wait for DOM
document.addEventListener('DOMContentLoaded', () => {
    initLoadingScreen();
    initCursorGlow();
    initNavbar();
    initHeroCanvas();
    initAICanvas();
    initScrollAnimations();
    initCounters();
    initMetricBars();
    initCardGlow();
    initParallax();
    initTypingEffect();
});

/* === Loading Screen === */
function initLoadingScreen() {
    window.addEventListener('load', () => {
        setTimeout(() => {
            const loader = document.getElementById('loadingScreen');
            loader.classList.add('hidden');
            // Trigger hero animations after load
            setTimeout(() => {
                document.querySelectorAll('.hero .animate-in').forEach((el, i) => {
                    setTimeout(() => el.classList.add('visible'), i * 200);
                });
                animateHeroStats();
            }, 300);
        }, 1500);
    });
}

/* === Cursor Glow Effect === */
function initCursorGlow() {
    const glow = document.getElementById('cursorGlow');
    if (!glow || window.innerWidth < 768) return;

    let mx = 0, my = 0, cx = 0, cy = 0;
    document.addEventListener('mousemove', (e) => {
        mx = e.clientX;
        my = e.clientY;
    });

    function animate() {
        cx += (mx - cx) * 0.08;
        cy += (my - cy) * 0.08;
        glow.style.left = cx + 'px';
        glow.style.top = cy + 'px';
        requestAnimationFrame(animate);
    }
    animate();
}

/* === Navbar === */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const toggle = document.getElementById('navToggle');
    const links = document.getElementById('navLinks');

    window.addEventListener('scroll', () => {
        navbar.classList.toggle('scrolled', window.scrollY > 50);
    });

    if (toggle && links) {
        toggle.addEventListener('click', () => {
            links.classList.toggle('active');
        });
    }

    // Smooth scroll for nav links
    document.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                if (links) links.classList.remove('active');
            }
        });
    });
}

/* === Hero Three.js Particle Canvas === */
function initHeroCanvas() {
    const canvas = document.getElementById('heroCanvas');
    if (!canvas || typeof THREE === 'undefined') return;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Particles
    const particleCount = 2000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    const color1 = new THREE.Color(0x418fde); // blue
    const color2 = new THREE.Color(0xe8a838); // gold
    const color3 = new THREE.Color(0x1b4d89); // dark blue

    for (let i = 0; i < particleCount; i++) {
        positions[i * 3] = (Math.random() - 0.5) * 20;
        positions[i * 3 + 1] = (Math.random() - 0.5) * 20;
        positions[i * 3 + 2] = (Math.random() - 0.5) * 20;

        const t = Math.random();
        const c = t < 0.4 ? color1 : t < 0.7 ? color2 : color3;
        colors[i * 3] = c.r;
        colors[i * 3 + 1] = c.g;
        colors[i * 3 + 2] = c.b;

        sizes[i] = Math.random() * 3 + 1;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));
    geometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    // Create circular texture for particles
    const particleCanvas = document.createElement('canvas');
    particleCanvas.width = 64;
    particleCanvas.height = 64;
    const pCtx = particleCanvas.getContext('2d');
    const gradient = pCtx.createRadialGradient(32, 32, 0, 32, 32, 32);
    gradient.addColorStop(0, 'rgba(255,255,255,1)');
    gradient.addColorStop(0.3, 'rgba(255,255,255,0.8)');
    gradient.addColorStop(1, 'rgba(255,255,255,0)');
    pCtx.fillStyle = gradient;
    pCtx.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(particleCanvas);

    const material = new THREE.PointsMaterial({
        size: 0.08,
        vertexColors: true,
        transparent: true,
        opacity: 0.8,
        map: texture,
        blending: THREE.AdditiveBlending,
        depthWrite: false,
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    // Connection lines
    const lineGeometry = new THREE.BufferGeometry();
    const linePositions = new Float32Array(particleCount * 6);
    lineGeometry.setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
    const lineMaterial = new THREE.LineBasicMaterial({
        color: 0x418fde,
        transparent: true,
        opacity: 0.06,
        blending: THREE.AdditiveBlending,
    });
    const lines = new THREE.LineSegments(lineGeometry, lineMaterial);
    scene.add(lines);

    camera.position.z = 8;

    let mouseX = 0, mouseY = 0;
    document.addEventListener('mousemove', (e) => {
        mouseX = (e.clientX / window.innerWidth) * 2 - 1;
        mouseY = -(e.clientY / window.innerHeight) * 2 + 1;
    });

    function animate() {
        requestAnimationFrame(animate);

        const time = Date.now() * 0.0003;
        particles.rotation.y = time * 0.3 + mouseX * 0.1;
        particles.rotation.x = time * 0.2 + mouseY * 0.1;

        // Animate positions slightly
        const pos = particles.geometry.attributes.position.array;
        for (let i = 0; i < particleCount; i++) {
            const idx = i * 3;
            pos[idx + 1] += Math.sin(time + i * 0.1) * 0.002;
        }
        particles.geometry.attributes.position.needsUpdate = true;

        // Update connection lines (connect nearby particles)
        const lp = lines.geometry.attributes.position.array;
        let lineIdx = 0;
        const maxConnections = 200;
        for (let i = 0; i < Math.min(100, particleCount) && lineIdx < maxConnections * 6; i++) {
            for (let j = i + 1; j < Math.min(100, particleCount) && lineIdx < maxConnections * 6; j++) {
                const dx = pos[i * 3] - pos[j * 3];
                const dy = pos[i * 3 + 1] - pos[j * 3 + 1];
                const dz = pos[i * 3 + 2] - pos[j * 3 + 2];
                const dist = Math.sqrt(dx * dx + dy * dy + dz * dz);

                if (dist < 2) {
                    lp[lineIdx++] = pos[i * 3];
                    lp[lineIdx++] = pos[i * 3 + 1];
                    lp[lineIdx++] = pos[i * 3 + 2];
                    lp[lineIdx++] = pos[j * 3];
                    lp[lineIdx++] = pos[j * 3 + 1];
                    lp[lineIdx++] = pos[j * 3 + 2];
                }
            }
        }
        // Zero out remaining
        for (let i = lineIdx; i < lp.length; i++) lp[i] = 0;
        lines.geometry.attributes.position.needsUpdate = true;

        renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
}

/* === AI Section Neural Network Canvas === */
function initAICanvas() {
    const canvas = document.getElementById('aiCanvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let w, h;

    function resize() {
        const section = canvas.parentElement;
        w = canvas.width = section.offsetWidth;
        h = canvas.height = section.offsetHeight;
    }
    resize();

    const nodes = [];
    const nodeCount = 50;
    for (let i = 0; i < nodeCount; i++) {
        nodes.push({
            x: Math.random() * w,
            y: Math.random() * h,
            vx: (Math.random() - 0.5) * 0.5,
            vy: (Math.random() - 0.5) * 0.5,
            r: Math.random() * 3 + 1,
        });
    }

    function draw() {
        ctx.clearRect(0, 0, w, h);

        // Draw connections
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dx = nodes[i].x - nodes[j].x;
                const dy = nodes[i].y - nodes[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 150) {
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.strokeStyle = `rgba(65, 143, 222, ${0.15 * (1 - dist / 150)})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        }

        // Draw nodes
        nodes.forEach(n => {
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(65, 143, 222, 0.5)';
            ctx.fill();

            // Glow
            ctx.beginPath();
            ctx.arc(n.x, n.y, n.r * 3, 0, Math.PI * 2);
            const grd = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 3);
            grd.addColorStop(0, 'rgba(65, 143, 222, 0.2)');
            grd.addColorStop(1, 'rgba(65, 143, 222, 0)');
            ctx.fillStyle = grd;
            ctx.fill();

            // Move
            n.x += n.vx;
            n.y += n.vy;
            if (n.x < 0 || n.x > w) n.vx *= -1;
            if (n.y < 0 || n.y > h) n.vy *= -1;
        });

        requestAnimationFrame(draw);
    }
    draw();

    window.addEventListener('resize', resize);
}

/* === Scroll Animations (GSAP + Intersection Observer fallback) === */
function initScrollAnimations() {
    // Use GSAP ScrollTrigger if available
    if (typeof gsap !== 'undefined' && typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);

        // Animate sections
        gsap.utils.toArray('.animate-in').forEach((el) => {
            // Skip hero elements (handled separately)
            if (el.closest('.hero')) return;

            ScrollTrigger.create({
                trigger: el,
                start: 'top 85%',
                onEnter: () => el.classList.add('visible'),
            });
        });

        // Table rows
        gsap.utils.toArray('.table-row-animate').forEach((row) => {
            ScrollTrigger.create({
                trigger: row,
                start: 'top 90%',
                onEnter: () => row.classList.add('visible'),
            });
        });

        // Parallax images
        gsap.utils.toArray('.image-reveal img').forEach(img => {
            gsap.fromTo(img, { yPercent: 10 }, {
                yPercent: -10,
                ease: 'none',
                scrollTrigger: {
                    trigger: img,
                    start: 'top bottom',
                    end: 'bottom top',
                    scrub: 1,
                }
            });
        });

        // Timeline line animation
        const timelineLine = document.querySelector('.timeline-line');
        if (timelineLine) {
            gsap.fromTo(timelineLine,
                { scaleY: 0, transformOrigin: 'top' },
                {
                    scaleY: 1,
                    ease: 'none',
                    scrollTrigger: {
                        trigger: '.timeline',
                        start: 'top 80%',
                        end: 'bottom 60%',
                        scrub: 1,
                    }
                }
            );
        }

        // Savings banner parallax
        const banner = document.querySelector('.savings-banner');
        if (banner) {
            gsap.fromTo(banner,
                { scale: 0.95, opacity: 0 },
                {
                    scale: 1,
                    opacity: 1,
                    scrollTrigger: {
                        trigger: banner,
                        start: 'top 85%',
                        end: 'top 50%',
                        scrub: 1,
                    }
                }
            );
        }
    } else {
        // Fallback: Intersection Observer
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.animate-in, .table-row-animate').forEach(el => {
            if (!el.closest('.hero')) observer.observe(el);
        });
    }
}

/* === Counter Animation === */
function initCounters() {
    const counters = document.querySelectorAll('.counter');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.dataset.counted) {
                entry.target.dataset.counted = 'true';
                animateCounter(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

function animateCounter(el) {
    const target = parseInt(el.dataset.target);
    const duration = 2000;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const ease = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.floor(target * ease);

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            el.textContent = target;
        }
    }
    requestAnimationFrame(update);
}

/* === Hero Stats Animation === */
function animateHeroStats() {
    document.querySelectorAll('.stat-number').forEach(el => {
        const target = parseInt(el.dataset.target);
        const duration = 2500;
        const start = performance.now();

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            el.textContent = Math.floor(target * ease);
            if (progress < 1) requestAnimationFrame(update);
            else el.textContent = target;
        }
        requestAnimationFrame(update);
    });
}

/* === Metric Bars Animation === */
function initMetricBars() {
    const bars = document.querySelectorAll('.metric-bar');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const bar = entry.target;
                const width = bar.dataset.width || 50;
                bar.style.setProperty('--bar-width', width + '%');
                bar.classList.add('animated');
            }
        });
    }, { threshold: 0.5 });

    bars.forEach(b => observer.observe(b));
}

/* === Card Glow Follow Mouse === */
function initCardGlow() {
    document.querySelectorAll('.glass-card').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = ((e.clientX - rect.left) / rect.width) * 100;
            const y = ((e.clientY - rect.top) / rect.height) * 100;
            card.style.setProperty('--mouse-x', x + '%');
            card.style.setProperty('--mouse-y', y + '%');
        });
    });
}

/* === Parallax on Scroll === */
function initParallax() {
    const heroBg = document.querySelector('.hero-bg-image');
    if (!heroBg) return;

    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY;
        heroBg.style.transform = `translateY(${scrollY * 0.3}px)`;
    });
}

/* === Typing Effect for Hero Subtitle === */
function initTypingEffect() {
    // Optional: Add a blinking cursor to subtitle
    const subtitle = document.querySelector('.hero-subtitle');
    if (!subtitle) return;

    const style = document.createElement('style');
    style.textContent = `
        .hero-subtitle::after {
            content: '|';
            animation: blink 1s step-end infinite;
            color: var(--accent);
            font-weight: 300;
        }
        @keyframes blink {
            50% { opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    // Remove cursor after 3 seconds
    setTimeout(() => {
        style.textContent = '';
    }, 5000);
}
