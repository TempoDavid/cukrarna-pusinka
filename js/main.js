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

  initMenu();
  initHeaderShadow();
  initReveal();
  initToday();
  initFab();
})();
