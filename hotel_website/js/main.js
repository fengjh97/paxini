/* ============================================================
   旅亭 花月 KAGETSU — Main JavaScript
   GSAP + ScrollTrigger animations, custom cursor,
   drag gallery, mobile nav, header scroll behaviour
   ============================================================ */

(function () {
  "use strict";

  /* ── Wait for GSAP to be ready ────────────────────── */
  function init() {
    if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
      // Retry until GSAP is loaded (deferred scripts)
      setTimeout(init, 50);
      return;
    }

    gsap.registerPlugin(ScrollTrigger);

    initCustomCursor();
    initHeaderScroll();
    initMobileNav();
    initHeroAnimations();
    initScrollReveal();
    initParallax();
    initGalleryDrag();
    initSmoothAnchors();
  }

  /* ── Custom Cursor ────────────────────────────────── */
  function initCustomCursor() {
    // Skip on touch devices
    if (window.matchMedia("(hover: none) and (pointer: coarse)").matches) return;

    const cursor = document.querySelector(".cursor");
    const follower = document.querySelector(".cursor-follower");
    if (!cursor || !follower) return;

    let mouseX = -100;
    let mouseY = -100;
    let followerX = -100;
    let followerY = -100;

    document.addEventListener("mousemove", function (e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
      // Instant position for the dot
      cursor.style.left = mouseX + "px";
      cursor.style.top = mouseY + "px";
    });

    // Smooth follower via requestAnimationFrame
    function updateFollower() {
      followerX += (mouseX - followerX) * 0.12;
      followerY += (mouseY - followerY) * 0.12;
      follower.style.left = followerX + "px";
      follower.style.top = followerY + "px";
      requestAnimationFrame(updateFollower);
    }
    requestAnimationFrame(updateFollower);

    // Hover states
    const hoverElements = document.querySelectorAll(
      'a, button, [role="button"], .room-card, .gallery__item, .seasonal__card'
    );

    hoverElements.forEach(function (el) {
      el.addEventListener("mouseenter", function () {
        cursor.classList.add("cursor--hover");
        follower.classList.add("cursor-follower--hover");
      });
      el.addEventListener("mouseleave", function () {
        cursor.classList.remove("cursor--hover");
        follower.classList.remove("cursor-follower--hover");
      });
    });

    // Hide cursor when leaving window
    document.addEventListener("mouseleave", function () {
      cursor.style.opacity = "0";
      follower.style.opacity = "0";
    });
    document.addEventListener("mouseenter", function () {
      cursor.style.opacity = "1";
      follower.style.opacity = "0.5";
    });
  }

  /* ── Header Scroll Behaviour ──────────────────────── */
  function initHeaderScroll() {
    var header = document.getElementById("siteHeader");
    if (!header) return;

    ScrollTrigger.create({
      start: "top -80",
      onUpdate: function (self) {
        if (self.scroll() > 80) {
          header.classList.add("site-header--scrolled");
        } else {
          header.classList.remove("site-header--scrolled");
        }
      },
    });
  }

  /* ── Mobile Nav ───────────────────────────────────── */
  function initMobileNav() {
    var toggle = document.getElementById("navToggle");
    var mobileNav = document.getElementById("mobileNav");
    if (!toggle || !mobileNav) return;

    var isOpen = false;

    function openNav() {
      isOpen = true;
      toggle.classList.add("nav__toggle--open");
      toggle.setAttribute("aria-expanded", "true");
      mobileNav.classList.add("mobile-nav--open");
      mobileNav.setAttribute("aria-hidden", "false");
      document.body.style.overflow = "hidden";
    }

    function closeNav() {
      isOpen = false;
      toggle.classList.remove("nav__toggle--open");
      toggle.setAttribute("aria-expanded", "false");
      mobileNav.classList.remove("mobile-nav--open");
      mobileNav.setAttribute("aria-hidden", "true");
      document.body.style.overflow = "";
    }

    toggle.addEventListener("click", function () {
      if (isOpen) {
        closeNav();
      } else {
        openNav();
      }
    });

    // Close on link click
    var navLinks = mobileNav.querySelectorAll("a");
    navLinks.forEach(function (link) {
      link.addEventListener("click", function () {
        closeNav();
      });
    });

    // Close on Escape
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && isOpen) {
        closeNav();
      }
    });
  }

  /* ── Hero Animations ──────────────────────────────── */
  function initHeroAnimations() {
    var tl = gsap.timeline({ delay: 0.3 });

    // Parallax on hero image
    gsap.to(".hero__image", {
      yPercent: 20,
      ease: "none",
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "bottom top",
        scrub: true,
      },
    });

    // Vertical characters
    tl.to(".hero__vertical-char", {
      opacity: 1,
      y: 0,
      duration: 0.8,
      stagger: 0.15,
      ease: "power3.out",
      clearProps: "transform",
    });

    tl.to(
      ".hero__vertical-divider",
      {
        opacity: 0.6,
        scaleY: 1,
        duration: 0.6,
        ease: "power2.out",
      },
      "-=0.3"
    );

    // Main text
    tl.to(
      ".hero__tagline-jp",
      {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
      },
      "-=0.2"
    );

    tl.to(
      ".hero__title-jp",
      {
        opacity: 1,
        y: 0,
        duration: 1,
        ease: "power3.out",
      },
      "-=0.5"
    );

    tl.to(
      ".hero__title-en",
      {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
      },
      "-=0.6"
    );

    tl.to(
      ".hero__subtitle",
      {
        opacity: 1,
        y: 0,
        duration: 0.8,
        ease: "power3.out",
      },
      "-=0.5"
    );

    // Scroll indicator
    tl.fromTo(
      ".hero__scroll-indicator",
      { opacity: 0, y: 20 },
      { opacity: 1, y: 0, duration: 0.8, ease: "power2.out" },
      "-=0.2"
    );

    // Fade scroll indicator on scroll
    gsap.to(".hero__scroll-indicator", {
      opacity: 0,
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "20% top",
        scrub: true,
      },
    });
  }

  /* ── Scroll Reveal ────────────────────────────────── */
  function initScrollReveal() {
    // Check for reduced motion preference
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      // Immediately show all elements
      document.querySelectorAll(".reveal-up").forEach(function (el) {
        el.style.opacity = "1";
        el.style.transform = "none";
      });
      return;
    }

    // Reveal-up elements
    var revealElements = document.querySelectorAll(".reveal-up");
    revealElements.forEach(function (el) {
      gsap.to(el, {
        opacity: 1,
        y: 0,
        duration: 0.9,
        ease: "power3.out",
        scrollTrigger: {
          trigger: el,
          start: "top 85%",
          once: true,
        },
      });
    });

    // Section divider animations
    var dividers = document.querySelectorAll(".section__divider");
    dividers.forEach(function (divider) {
      gsap.fromTo(
        divider,
        { scaleX: 0 },
        {
          scaleX: 1,
          duration: 0.8,
          ease: "power2.inOut",
          scrollTrigger: {
            trigger: divider,
            start: "top 90%",
            once: true,
          },
        }
      );
    });

    // Experience timeline line
    var timelineLine = document.querySelector(".experience__line");
    if (timelineLine) {
      gsap.fromTo(
        timelineLine,
        { scaleY: 0, transformOrigin: "top" },
        {
          scaleY: 1,
          duration: 1.5,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ".experience__timeline",
            start: "top 80%",
            end: "bottom 60%",
            scrub: 1,
          },
        }
      );
    }

    // Experience dots
    var dots = document.querySelectorAll(".experience__dot");
    dots.forEach(function (dot) {
      gsap.fromTo(
        dot,
        { scale: 0 },
        {
          scale: 1,
          duration: 0.4,
          ease: "back.out(2)",
          scrollTrigger: {
            trigger: dot,
            start: "top 80%",
            once: true,
          },
        }
      );
    });

    // Room cards stagger
    var roomCards = document.querySelectorAll(".room-card");
    if (roomCards.length > 0) {
      gsap.to(roomCards, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.15,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ".rooms__grid",
          start: "top 80%",
          once: true,
        },
      });
    }

    // Seasonal cards stagger
    var seasonCards = document.querySelectorAll(".seasonal__card");
    if (seasonCards.length > 0) {
      gsap.to(seasonCards, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.12,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ".seasonal__grid",
          start: "top 80%",
          once: true,
        },
      });
    }

    // Onsen panels
    var onsenPanels = document.querySelectorAll(".onsen__panel");
    if (onsenPanels.length > 0) {
      gsap.to(onsenPanels, {
        opacity: 1,
        y: 0,
        duration: 1,
        stagger: 0.2,
        ease: "power3.out",
        scrollTrigger: {
          trigger: ".onsen__split",
          start: "top 80%",
          once: true,
        },
      });
    }

    // Gallery items stagger on scroll
    var galleryItems = document.querySelectorAll(".gallery__item");
    if (galleryItems.length > 0) {
      gsap.fromTo(
        galleryItems,
        { opacity: 0, x: 60 },
        {
          opacity: 1,
          x: 0,
          duration: 0.8,
          stagger: 0.08,
          ease: "power3.out",
          scrollTrigger: {
            trigger: ".gallery__track",
            start: "top 85%",
            once: true,
          },
        }
      );
    }
  }

  /* ── Parallax Effects ─────────────────────────────── */
  function initParallax() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

    // Concept images parallax
    var conceptPrimary = document.querySelector(".concept__image-primary img");
    if (conceptPrimary) {
      gsap.to(conceptPrimary, {
        yPercent: -8,
        ease: "none",
        scrollTrigger: {
          trigger: ".concept",
          start: "top bottom",
          end: "bottom top",
          scrub: 1,
        },
      });
    }

    // Onsen images parallax
    var onsenImages = document.querySelectorAll(".onsen__image-wrap img");
    onsenImages.forEach(function (img) {
      gsap.to(img, {
        yPercent: -6,
        ease: "none",
        scrollTrigger: {
          trigger: img.closest(".onsen__panel"),
          start: "top bottom",
          end: "bottom top",
          scrub: 1,
        },
      });
    });

    // Dining images parallax
    var diningImages = document.querySelectorAll(".dining__feature-image img");
    diningImages.forEach(function (img) {
      gsap.to(img, {
        yPercent: -5,
        ease: "none",
        scrollTrigger: {
          trigger: img.closest(".dining__feature"),
          start: "top bottom",
          end: "bottom top",
          scrub: 1,
        },
      });
    });
  }

  /* ── Gallery Drag ─────────────────────────────────── */
  function initGalleryDrag() {
    var track = document.getElementById("galleryTrack");
    if (!track) return;

    var isDragging = false;
    var startX = 0;
    var scrollLeft = 0;
    var velocity = 0;
    var lastX = 0;
    var lastTime = 0;
    var rafId = null;

    function getPageX(e) {
      return e.touches ? e.touches[0].pageX : e.pageX;
    }

    function onDragStart(e) {
      isDragging = true;
      startX = getPageX(e) - track.offsetLeft;
      scrollLeft = track.scrollLeft;
      lastX = startX;
      lastTime = Date.now();
      velocity = 0;
      track.classList.add("is-dragging");
      if (rafId) cancelAnimationFrame(rafId);
    }

    function onDragMove(e) {
      if (!isDragging) return;
      e.preventDefault();
      var x = getPageX(e) - track.offsetLeft;
      var walk = (x - startX) * 1.5;
      track.scrollLeft = scrollLeft - walk;

      // Calculate velocity for momentum
      var now = Date.now();
      var dt = now - lastTime;
      if (dt > 0) {
        velocity = (x - lastX) / dt;
      }
      lastX = x;
      lastTime = now;
    }

    function onDragEnd() {
      if (!isDragging) return;
      isDragging = false;
      track.classList.remove("is-dragging");

      // Momentum scrolling
      var momentum = velocity * 300;
      var targetScroll = track.scrollLeft - momentum;

      gsap.to(track, {
        scrollLeft: targetScroll,
        duration: 0.8,
        ease: "power3.out",
      });
    }

    // Mouse events
    track.addEventListener("mousedown", onDragStart);
    track.addEventListener("mousemove", onDragMove);
    track.addEventListener("mouseup", onDragEnd);
    track.addEventListener("mouseleave", onDragEnd);

    // Touch events
    track.addEventListener("touchstart", onDragStart, { passive: true });
    track.addEventListener("touchmove", onDragMove, { passive: false });
    track.addEventListener("touchend", onDragEnd);

    // Prevent image dragging
    track.querySelectorAll("img").forEach(function (img) {
      img.addEventListener("dragstart", function (e) {
        e.preventDefault();
      });
    });

    // Allow mouse wheel horizontal scroll
    track.addEventListener("wheel", function (e) {
      if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
      e.preventDefault();
      track.scrollLeft += e.deltaY * 2;
    }, { passive: false });
  }

  /* ── Smooth Anchor Scrolling ──────────────────────── */
  function initSmoothAnchors() {
    var anchors = document.querySelectorAll('a[href^="#"]');

    anchors.forEach(function (anchor) {
      anchor.addEventListener("click", function (e) {
        var targetId = this.getAttribute("href");
        if (targetId === "#") return;

        var target = document.querySelector(targetId);
        if (!target) return;

        e.preventDefault();

        var headerHeight = document.getElementById("siteHeader")
          ? document.getElementById("siteHeader").offsetHeight
          : 0;

        var targetPosition =
          target.getBoundingClientRect().top + window.pageYOffset - headerHeight;

        gsap.to(window, {
          scrollTo: { y: targetPosition, autoKill: true },
          duration: 1.2,
          ease: "power3.inOut",
        });
      });
    });

    // Load GSAP ScrollTo plugin for smooth scrolling if available
    if (typeof gsap !== "undefined" && !gsap.plugins?.scrollTo) {
      // Fallback: use native smooth scroll if ScrollTo plugin is not available
      anchors.forEach(function (anchor) {
        anchor.addEventListener("click", function (e) {
          var targetId = this.getAttribute("href");
          if (targetId === "#") return;

          var target = document.querySelector(targetId);
          if (!target) return;

          e.preventDefault();
          target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
      });
    }
  }

  /* ── Initialize on DOM Ready ──────────────────────── */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
