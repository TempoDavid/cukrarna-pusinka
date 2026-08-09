/* Cukrárna Pusinka — vanilla JS: menu, header, animace */
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

  /* Fallback bez GSAP — prosté odkrytí */
  function initReveal() {
    var els = document.querySelectorAll('.rev, .anim-head, .anim-img, .anim-card, .anim-chip');
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
    }, { threshold: .12, rootMargin: '0px 0px -40px' });
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

  /* ---------------------------------------------------------------
     Rozsekání nadpisu na slova — každé slovo do masky, ať může
     vyjet zespodu. Zachovává <br> i vnořené <span> (outline-word).
     --------------------------------------------------------------- */
  function splitWords(el) {
    if (el.dataset.split === '1') return el.querySelectorAll('.wi');
    var frag = document.createDocumentFragment();

    function walk(node, target) {
      Array.prototype.slice.call(node.childNodes).forEach(function (child) {
        if (child.nodeType === 3) {
          var parts = child.textContent.split(/(\s+)/);
          parts.forEach(function (part) {
            if (!part) return;
            if (/^\s+$/.test(part)) {
              target.appendChild(document.createTextNode(' '));
              return;
            }
            var mask = document.createElement('span');
            mask.className = 'w';
            var inner = document.createElement('span');
            inner.className = 'wi';
            inner.textContent = part;
            mask.appendChild(inner);
            target.appendChild(mask);
          });
        } else if (child.nodeName === 'BR') {
          target.appendChild(document.createElement('br'));
        } else if (child.nodeType === 1) {
          var clone = child.cloneNode(false);
          target.appendChild(clone);
          walk(child, clone);
        }
      });
    }

    walk(el, frag);
    el.innerHTML = '';
    el.appendChild(frag);
    el.dataset.split = '1';
    return el.querySelectorAll('.wi');
  }

  /* Počítadlo čísel (4,2 / 321 / 1992) */
  function countUp(el, done) {
    var raw = el.dataset.count;
    var decimals = (raw.split('.')[1] || '').length;
    var target = parseFloat(raw);
    var obj = { v: 0 };
    gsap.to(obj, {
      v: target,
      duration: 1.4,
      ease: 'power2.out',
      onUpdate: function () {
        el.textContent = obj.v.toFixed(decimals).replace('.', ',');
      },
      onComplete: done
    });
  }

  /* ---------------------------------------------------------------
     Hlavní animační pass
     --------------------------------------------------------------- */
  function initMotion() {
    gsap.registerPlugin(ScrollTrigger);

    /* --- 1. Nadpisy: slova vyjedou zespodu z masky --- */
    document.querySelectorAll('.anim-head').forEach(function (head) {
      var words = splitWords(head);
      gsap.set(words, { yPercent: 118, rotate: 4 });
      gsap.to(words, {
        yPercent: 0,
        rotate: 0,
        duration: .85,
        ease: 'power3.out',
        stagger: .055,
        scrollTrigger: { trigger: head, start: 'top 88%', once: true }
      });
    });

    /* --- 2. Odstavce a drobné prvky: jemný nájezd --- */
    document.querySelectorAll('.anim-up').forEach(function (el) {
      gsap.fromTo(el,
        { y: 26, opacity: 0 },
        {
          y: 0,
          opacity: 1,
          duration: .7,
          ease: 'power2.out',
          delay: parseFloat(el.dataset.delay || 0),
          scrollTrigger: { trigger: el, start: 'top 90%', once: true }
        }
      );
    });

    /* --- 3. Obrázky: odkryjí se stěrkou zdola nahoru --- */
    document.querySelectorAll('.anim-img').forEach(function (el) {
      gsap.fromTo(el,
        { clipPath: 'inset(100% 0% 0% 0%)', scale: 1.08 },
        {
          clipPath: 'inset(0% 0% 0% 0%)',
          scale: 1,
          duration: 1.05,
          ease: 'power3.out',
          scrollTrigger: { trigger: el, start: 'top 88%', once: true }
        }
      );
    });

    /* --- 4. Karty: naskáčou postupně s lehkým pootočením --- */
    document.querySelectorAll('[data-stagger]').forEach(function (group) {
      var items = group.querySelectorAll(group.dataset.stagger);
      if (!items.length) return;
      gsap.fromTo(items,
        { y: 46, opacity: 0, scale: .94 },
        {
          y: 0,
          opacity: 1,
          scale: 1,
          duration: .7,
          ease: 'back.out(1.4)',
          stagger: { each: .07, from: 'start' },
          clearProps: 'transform',
          scrollTrigger: { trigger: group, start: 'top 85%', once: true }
        }
      );
    });

    /* --- 5. Chipy / odrážky: popnou jeden po druhém --- */
    document.querySelectorAll('[data-pop]').forEach(function (group) {
      var items = group.querySelectorAll(group.dataset.pop);
      if (!items.length) return;
      gsap.fromTo(items,
        { scale: .3, opacity: 0 },
        {
          scale: 1,
          opacity: 1,
          duration: .5,
          ease: 'back.out(2.2)',
          stagger: .06,
          clearProps: 'transform',
          scrollTrigger: { trigger: group, start: 'top 90%', once: true }
        }
      );
    });

    /* --- 6. Čísla se načítají --- */
    document.querySelectorAll('[data-count]').forEach(function (el) {
      ScrollTrigger.create({
        trigger: el,
        start: 'top 92%',
        once: true,
        onEnter: function () { countUp(el); }
      });
    });

    /* --- 7. Pečeť 1992 přiletí a doskočí --- */
    var seal = document.querySelector('.seal');
    if (seal) {
      gsap.fromTo(seal,
        { scale: 0, rotate: -140 },
        {
          scale: 1,
          rotate: 0,
          duration: .8,
          ease: 'back.out(1.7)',
          clearProps: 'transform',
          scrollTrigger: { trigger: seal, start: 'top 92%', once: true }
        }
      );
    }

    /* --- 8. Hero intro po načtení --- */
    var heroWords = document.querySelector('.hero h1');
    var tl = gsap.timeline({ defaults: { ease: 'power3.out' } });
    if (heroWords) {
      var hw = splitWords(heroWords);
      gsap.set(hw, { yPercent: 118, rotate: 5 });
      tl.to(hw, { yPercent: 0, rotate: 0, duration: .95, stagger: .075 }, .15);
    }
    tl.fromTo('.hero-sub', { y: 24, opacity: 0 }, { y: 0, opacity: 1, duration: .7 }, '-=.5')
      .fromTo('.hero-ctas .btn',
        { y: 20, opacity: 0, scale: .92 },
        { y: 0, opacity: 1, scale: 1, duration: .55, stagger: .1, ease: 'back.out(1.6)', clearProps: 'transform' }, '-=.35')
      .fromTo('.trust-chip', { y: 16, opacity: 0 }, { y: 0, opacity: 1, duration: .5, clearProps: 'transform' }, '-=.3')
      .fromTo('.hero-frame',
        { y: 60, rotate: -9, opacity: 0 },
        { y: 0, rotate: -1.8, opacity: 1, duration: 1, ease: 'back.out(1.2)', clearProps: 'transform' }, .3)
      .fromTo('.hero-stage .deco',
        { scale: 0, opacity: 0 },
        { scale: 1, opacity: 1, duration: .6, stagger: .12, ease: 'back.out(2)' }, '-=.4');

    /* --- 9. Hero parallax --- */
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

    /* --- 10. Zdobící linky se samy nakreslí --- */
    document.querySelectorAll('.sq-path').forEach(function (path) {
      var len = path.getTotalLength();
      path.style.strokeDasharray = len;
      path.style.strokeDashoffset = len;
      gsap.to(path, {
        strokeDashoffset: 0,
        duration: 1.1,
        ease: 'power2.out',
        scrollTrigger: { trigger: path, start: 'top 90%', once: true }
      });
    });

    /* --- 11. Plovoucí dekorace --- */
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

    /* --- 12. Parallax dekorací a fotek v příběhu --- */
    ['.story-gingerbread', '.best-cupcake', '.best-sprinkles', '.rev-pusinka'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el) return;
      gsap.to(el, {
        y: -34,
        ease: 'none',
        scrollTrigger: { trigger: el, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });
    gsap.to('.inset-frame', {
      y: 26,
      ease: 'none',
      scrollTrigger: { trigger: '.story', start: 'top bottom', end: 'bottom top', scrub: true }
    });

    /* --- 13. Vlnky mezi sekcemi se lehce vlní --- */
    document.querySelectorAll('.divider svg').forEach(function (svg, i) {
      gsap.to(svg, {
        xPercent: i % 2 ? 2.5 : -2.5,
        ease: 'none',
        scrollTrigger: { trigger: svg, start: 'top bottom', end: 'bottom top', scrub: true }
      });
    });

    /* zbytek .rev prvků (bez vlastní animace) prostě odkryjeme */
    ScrollTrigger.batch('.rev', {
      start: 'top 90%',
      once: true,
      onEnter: function (batch) {
        batch.forEach(function (el) { el.classList.add('in'); });
      }
    });

    /* --- Pojistky: dopočítat pozice, až doběhne layout a obrázky --- */
    var refreshTimer;
    function scheduleRefresh() {
      clearTimeout(refreshTimer);
      refreshTimer = setTimeout(function () { ScrollTrigger.refresh(); }, 120);
    }
    document.querySelectorAll('img').forEach(function (img) {
      if (!img.complete) img.addEventListener('load', scheduleRefresh, { once: true });
    });
    window.addEventListener('load', scheduleRefresh);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(scheduleRefresh);
    ScrollTrigger.refresh();
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
    document.querySelectorAll('[data-count]').forEach(function (el) {
      el.textContent = el.dataset.count.replace('.', ',');
    });
  }
})();
