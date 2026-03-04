/* ============================================================
   atelier CLAIR — main.js
   GSAP + ScrollTrigger Animations & Interactions
   ============================================================ */

(function () {
  "use strict";

  /* ----------------------------------------------------------
     0. WAIT FOR GSAP TO LOAD
     ---------------------------------------------------------- */
  function init() {
    if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
      // Retry after a short delay if GSAP hasn't loaded yet
      setTimeout(init, 100);
      return;
    }

    gsap.registerPlugin(ScrollTrigger);

    // Run all modules
    initHeader();
    initHeroAnimations();
    initScrollAnimations();
    initGalleryFilter();
    initMobileCTA();
    initBotanicalSVGs();
    initSmoothScroll();
  }


  /* ----------------------------------------------------------
     1. HEADER — Scroll & Mobile Menu
     ---------------------------------------------------------- */
  function initHeader() {
    var header = document.getElementById("header");
    var hamburger = document.getElementById("hamburger");
    var nav = document.getElementById("nav");

    if (!header || !hamburger || !nav) return;

    // Scroll effect — add shadow
    var lastScroll = 0;

    function onScroll() {
      var scrollY = window.scrollY || window.pageYOffset;

      if (scrollY > 50) {
        header.classList.add("is-scrolled");
      } else {
        header.classList.remove("is-scrolled");
      }

      lastScroll = scrollY;
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll(); // Initial check

    // Mobile menu toggle
    function toggleMenu() {
      var isOpen = nav.classList.contains("is-open");

      if (isOpen) {
        nav.classList.remove("is-open");
        hamburger.classList.remove("is-active");
        hamburger.setAttribute("aria-expanded", "false");
        document.body.classList.remove("is-menu-open");
      } else {
        nav.classList.add("is-open");
        hamburger.classList.add("is-active");
        hamburger.setAttribute("aria-expanded", "true");
        document.body.classList.add("is-menu-open");
      }
    }

    hamburger.addEventListener("click", toggleMenu);

    // Close menu on nav link click
    var navLinks = nav.querySelectorAll(".header__nav-link, .header__nav-cta");
    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        if (nav.classList.contains("is-open")) {
          toggleMenu();
        }
      });
    });

    // Close on escape key
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) {
        toggleMenu();
      }
    });
  }


  /* ----------------------------------------------------------
     2. HERO ANIMATIONS
     ---------------------------------------------------------- */
  function initHeroAnimations() {
    var heroElements = document.querySelectorAll(".hero .anim-fade-up");
    if (heroElements.length === 0) return;

    // Check for reduced motion preference
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      heroElements.forEach(function (el) {
        el.style.opacity = "1";
        el.style.transform = "none";
      });
      return;
    }

    var tl = gsap.timeline({ delay: 0.3 });

    tl.to(heroElements, {
      opacity: 1,
      y: 0,
      duration: 0.9,
      stagger: 0.15,
      ease: "power3.out",
    });
  }


  /* ----------------------------------------------------------
     3. SCROLL-TRIGGERED ANIMATIONS
     ---------------------------------------------------------- */
  function initScrollAnimations() {
    // Check for reduced motion preference
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      document.querySelectorAll(".anim-fade-up").forEach(function (el) {
        el.style.opacity = "1";
        el.style.transform = "none";
      });
      return;
    }

    // Select all elements with .anim-fade-up that are NOT inside .hero
    var elements = document.querySelectorAll(
      ".section .anim-fade-up, .coupon .anim-fade-up"
    );

    elements.forEach(function (el) {
      gsap.to(el, {
        scrollTrigger: {
          trigger: el,
          start: "top 88%",
          end: "top 60%",
          toggleActions: "play none none none",
          once: true,
        },
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
      });
    });

    // Stagger children in specific containers
    var staggerContainers = [
      ".menu__categories",
      ".stylist__grid",
      ".blog__grid",
    ];

    staggerContainers.forEach(function (selector) {
      var container = document.querySelector(selector);
      if (!container) return;

      var children = container.querySelectorAll(".anim-fade-up");
      if (children.length === 0) return;

      gsap.to(children, {
        scrollTrigger: {
          trigger: container,
          start: "top 85%",
          toggleActions: "play none none none",
          once: true,
        },
        opacity: 1,
        y: 0,
        duration: 0.7,
        stagger: 0.12,
        ease: "power3.out",
      });
    });

    // Flow steps stagger animation
    var flowSteps = document.querySelectorAll(".flow__step, .flow__connector");
    if (flowSteps.length > 0) {
      gsap.to(flowSteps, {
        scrollTrigger: {
          trigger: ".flow",
          start: "top 85%",
          toggleActions: "play none none none",
          once: true,
        },
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger: 0.08,
        ease: "power3.out",
      });
    }

    // Gallery items stagger
    var galleryItems = document.querySelectorAll(".gallery__item");
    if (galleryItems.length > 0) {
      gsap.to(galleryItems, {
        scrollTrigger: {
          trigger: ".gallery__grid",
          start: "top 85%",
          toggleActions: "play none none none",
          once: true,
        },
        opacity: 1,
        y: 0,
        scale: 1,
        duration: 0.6,
        stagger: 0.1,
        ease: "power3.out",
      });

      // Set initial state for gallery items (they don't have .anim-fade-up)
      galleryItems.forEach(function (item) {
        gsap.set(item, { opacity: 0, y: 20, scale: 0.95 });
      });
    }
  }


  /* ----------------------------------------------------------
     4. GALLERY FILTER
     ---------------------------------------------------------- */
  function initGalleryFilter() {
    var filterBtns = document.querySelectorAll(".gallery__filter-btn");
    var galleryItems = document.querySelectorAll(".gallery__item");

    if (filterBtns.length === 0 || galleryItems.length === 0) return;

    filterBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var filter = this.getAttribute("data-filter");

        // Update active button
        filterBtns.forEach(function (b) {
          b.classList.remove("is-active");
        });
        this.classList.add("is-active");

        // Filter items
        galleryItems.forEach(function (item) {
          var category = item.getAttribute("data-category");
          var shouldShow = filter === "all" || category === filter;

          if (shouldShow) {
            item.classList.remove("is-hidden");
            gsap.to(item, {
              opacity: 1,
              scale: 1,
              duration: 0.4,
              ease: "power2.out",
            });
          } else {
            gsap.to(item, {
              opacity: 0,
              scale: 0.95,
              duration: 0.3,
              ease: "power2.in",
              onComplete: function () {
                item.classList.add("is-hidden");
              },
            });
          }
        });
      });
    });
  }


  /* ----------------------------------------------------------
     5. MOBILE STICKY CTA
     ---------------------------------------------------------- */
  function initMobileCTA() {
    var mobileCta = document.getElementById("mobileCta");
    var hero = document.getElementById("hero");

    if (!mobileCta || !hero) return;

    // Show after scrolling past the hero
    ScrollTrigger.create({
      trigger: hero,
      start: "bottom top",
      onEnter: function () {
        mobileCta.classList.add("is-visible");
      },
      onLeaveBack: function () {
        mobileCta.classList.remove("is-visible");
      },
    });
  }


  /* ----------------------------------------------------------
     6. BOTANICAL DECORATIVE SVGs — Fade In
     ---------------------------------------------------------- */
  function initBotanicalSVGs() {
    var svgs = document.querySelectorAll(".deco-svg");
    if (svgs.length === 0) return;

    // Check for reduced motion
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      svgs.forEach(function (svg) {
        svg.classList.add("is-visible");
      });
      return;
    }

    // Stagger their appearance
    setTimeout(function () {
      svgs.forEach(function (svg, i) {
        setTimeout(function () {
          svg.classList.add("is-visible");
        }, i * 400);
      });
    }, 1000);

    // Subtle parallax on desktop
    if (window.innerWidth >= 768) {
      svgs.forEach(function (svg, i) {
        var speed = 0.02 + i * 0.01;
        var direction = i % 2 === 0 ? 1 : -1;

        gsap.to(svg, {
          scrollTrigger: {
            trigger: document.body,
            start: "top top",
            end: "bottom bottom",
            scrub: 1,
          },
          y: function () {
            return direction * window.innerHeight * speed;
          },
          ease: "none",
        });
      });
    }
  }


  /* ----------------------------------------------------------
     7. SMOOTH SCROLL (for anchor links)
     ---------------------------------------------------------- */
  function initSmoothScroll() {
    var anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(function (anchor) {
      anchor.addEventListener("click", function (e) {
        var href = this.getAttribute("href");
        if (href === "#") return;

        var target = document.querySelector(href);
        if (!target) return;

        e.preventDefault();

        var headerHeight =
          document.getElementById("header")?.offsetHeight || 72;
        var targetPosition =
          target.getBoundingClientRect().top + window.scrollY - headerHeight;

        window.scrollTo({
          top: targetPosition,
          behavior: "smooth",
        });
      });
    });
  }


  /* ----------------------------------------------------------
     BOOT
     ---------------------------------------------------------- */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
