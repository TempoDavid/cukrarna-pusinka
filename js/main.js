/* Cukrárna Pusinka — vanilla JS: menu, header, reveals (GSAP pass v initMotion, T8) */
(function () {
  'use strict';

  /* Mobilní menu — clip-path circle, aria, Esc, scroll-lock */
  function initMenu() {
    var burger = document.querySelector('.burger');
    var menu = document.getElementById('m-menu');
    if (!burger || !menu) return;

    function setOpen(open) {
      burger.setAttribute('aria-expanded', String(open));
      burger.setAttribute('aria-label', open ? 'Zavřít menu' : 'Otevřít menu');
      menu.classList.toggle('open', open);
      document.body.style.overflow = open ? 'hidden' : '';
    }

    burger.addEventListener('click', function () {
      setOpen(burger.getAttribute('aria-expanded') !== 'true');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') setOpen(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) {
        setOpen(false);
        burger.focus();
      }
    });
  }

  /* Tvrdý stín headeru po odscrollování */
  function initHeaderShadow() {
    var header = document.querySelector('.site-header');
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle('scrolled', window.scrollY > 10);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* Scroll reveal — IO fallback; GSAP pass (initMotion) ho v T8 přebije */
  function initReveal() {
    var els = document.querySelectorAll('.rev');
    if (!('IntersectionObserver' in window)) {
      els.forEach(function (el) { el.classList.add('in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: .15, rootMargin: '0px 0px -40px' });
    els.forEach(function (el) { io.observe(el); });
  }

  /* Zvýraznění dnešního dne v otevírací době */
  function initToday() {
    var today = new Date().getDay();
    var row = document.querySelector('#hours li[data-day="' + today + '"]');
    if (row) row.classList.add('today');
  }

  /* Mobilní FAB — ukáže se po odscrollování hera */
  function initFab() {
    var fab = document.getElementById('fab');
    var hero = document.getElementById('uvod');
    if (!fab || !hero || !('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (entries) {
      fab.classList.toggle('show', !entries[0].isIntersecting);
    }, { threshold: 0 });
    io.observe(hero);
  }

  /* GSAP motion pass — reveals přes ScrollTrigger.batch + hero parallax */
  function initMotion() {
    gsap.registerPlugin(ScrollTrigger);

    ScrollTrigger.batch('.rev', {
      start: 'top 88%',
      once: true,
      onEnter: function (batch) {
        batch.forEach(function (el) { el.classList.add('in'); });
      }
    });

    /* hero parallax: text a scéna se rozjíždějí různou rychlostí */
    gsap.to('.hero-copy', {
      y: 60,
      opacity: .35,
      ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });
    gsap.to('.hero-stage', {
      y: -70,
      ease: 'none',
      scrollTrigger: { trigger: '.hero', start: 'top top', end: 'bottom top', scrub: true }
    });

    /* barevné sekce najíždějí zespodu jako vrstvy dortu */
    ['#bestsellery', '#sluzby', '#recenze', '#kontakt'].forEach(function (sel) {
      var sec = document.querySelector(sel);
      if (!sec) return;
      gsap.from(sec, {
        yPercent: 6,
        scale: .97,
        ease: 'none',
        scrollTrigger: { trigger: sec, start: 'top bottom', end: 'top 55%', scrub: .6 }
      });
    });

    /* zdobící linky se samy nakreslí (stroke draw-in) */
    document.querySelectorAll('.sq-path').forEach(function (path) {
      var len = path.getTotalLength();
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      gsap.to(path, {
        strokeDashoffset: 0,
        duration: 1.1,
        ease: 'power2.out',
        scrollTrigger: { trigger: path, start: 'top 88%', once: true }
      });
    });

    /* plovoucí dekorace — každá jinou rychlostí, ať to žije */
    document.querySelectorAll('.float-deco').forEach(function (el, i) {
      gsap.to(el, {
        y: 8 + (i % 3) * 4,
        rotation: (i % 2 ? '+=4' : '-=4'),
        duration: 3.6 + (i % 4) * .9,
        ease: 'sine.inOut',
        yoyo: true,
        repeat: -1
      });
    });

    /* dekorace v sekcích lehce parallaxují proti scrollu */
    ['.story-gingerbread', '.best-cupcake', '.best-sprinkles', '.rev-pusinka'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el) return;
      gsap.to(el, {
        y: -34,
        ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });

    /* fotky v příběhu se při scrollu lehce rozestoupí */
    gsap.to('.lace-frame', {
      y: -22,
      ease: 'none',
      scrollTrigger: { trigger: '.story', start: 'top bottom', end: 'bottom top', scrub: true }
    });
    gsap.to('.inset-frame', {
      y: 26,
      ease: 'none',
      scrollTrigger: { trigger: '.story', start: 'top bottom', end: 'bottom top', scrub: true }
    });
  }

  var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  initMenu();
  initHeaderShadow();
  initToday();
  initFab();

  if (!reducedMotion && window.gsap && window.ScrollTrigger) {
    initMotion();
  } else {
    initReveal();
  }
})();
