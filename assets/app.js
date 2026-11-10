(() => {
  'use strict';

  function initializeNavigation() {
    const links = Array.from(document.querySelectorAll(".navigation a[href^='#']"));
    const targets = links.map((link) => {
      try {
        const id = decodeURIComponent(link.getAttribute('href').slice(1));
        return { link, section: id ? document.getElementById(id) : null };
      } catch {
        return { link, section: null };
      }
    });
    const sections = Array.from(new Set(targets.map(({ section }) => section)))
      .filter(Boolean);
    let observer;
    let requestedSection = null;
    targets.forEach(({ link, section }) => {
      link.addEventListener('click', () => {
        requestedSection = section;
        window.requestAnimationFrame(updateNavigation);
      });
    });
    window.addEventListener('wheel', () => { requestedSection = null; }, { passive: true });
    window.addEventListener('touchstart', () => { requestedSection = null; }, { passive: true });
    window.addEventListener('keydown', (event) => {
      if (['ArrowUp', 'ArrowDown', 'PageUp', 'PageDown', 'Home', 'End', ' '].includes(event.key)) {
        requestedSection = null;
      }
    });

    function updateNavigation() {
      const anchorLine = Math.round(window.innerHeight * 0.2);
      let current = null;
      let closestTop = -Infinity;
      let first = null;
      let firstTop = Infinity;

      sections.forEach((section) => {
        if (!section.getClientRects().length) return;
        const { top } = section.getBoundingClientRect();
        if (top < firstTop) {
          first = section;
          firstTop = top;
        }
        if (top <= anchorLine && top >= closestTop) {
          current = section;
          closestTop = top;
        }
      });

      current = current || first;
      const atBottom = Math.ceil(window.scrollY + window.innerHeight)
        >= document.documentElement.scrollHeight - 2;
      if (atBottom && window.scrollY > 0) {
        current = requestedSection || sections[sections.length - 1] || current;
      }
      targets.forEach(({ link, section }) => {
        if (current && section === current) {
          link.setAttribute('aria-current', 'location');
        } else {
          link.removeAttribute('aria-current');
        }
      });
    }

    function observeSections() {
      if (observer) observer.disconnect();
      const height = window.innerHeight;
      const bottomMargin = Math.max(0, height - Math.round(height * 0.2));
      // Pixel margins keep the activation band relative to viewport height.
      observer = new window.IntersectionObserver(updateNavigation, {
        rootMargin: `0px 0px -${bottomMargin}px 0px`,
        threshold: 0,
      });
      sections.forEach((section) => observer.observe(section));
      updateNavigation();
    }

    updateNavigation();
    if (!sections.length) return;

    let scrollFrame = 0;
    window.addEventListener('scroll', () => {
      if (scrollFrame) return;
      scrollFrame = window.requestAnimationFrame(() => {
        scrollFrame = 0;
        updateNavigation();
      });
    }, { passive: true });

    if (typeof window.IntersectionObserver === 'function') {
      observeSections();
      window.addEventListener('resize', observeSections, { passive: true });
    } else {
      window.addEventListener('resize', updateNavigation, { passive: true });
    }
    window.addEventListener('hashchange', updateNavigation);
    window.addEventListener('load', updateNavigation, { once: true });
    window.addEventListener('pageshow', updateNavigation);
  }

  function initializeFigures() {
    const dialog = document.querySelector('dialog.figure-dialog');
    if (!dialog || typeof dialog.showModal !== 'function'
      || typeof dialog.close !== 'function') return;

    const image = dialog.querySelector('.figure-image');
    const caption = dialog.querySelector('.figure-caption');
    const closeButton = dialog.querySelector('.close-figure');
    const title = dialog.querySelector('#figure-title');
    if (!image || !caption || !closeButton) return;

    if (title) {
      if (!title.textContent.trim()) title.textContent = 'Figure';
      dialog.setAttribute('aria-labelledby', title.id);
    } else if (!dialog.hasAttribute('aria-label')
      && !dialog.hasAttribute('aria-labelledby')) {
      dialog.setAttribute('aria-label', 'Figure');
    }
    if (!caption.id) {
      let id = 'figure-caption';
      let suffix = 1;
      while (document.getElementById(id)) {
        id = `figure-caption-${suffix++}`;
      }
      caption.id = id;
    }
    dialog.setAttribute('aria-describedby', caption.id);
    if (!closeButton.hasAttribute('aria-label')
      && !closeButton.hasAttribute('aria-labelledby')) {
      closeButton.setAttribute('aria-label', 'Close figure');
    }

    let returnFocus = null;
    let pointerStartedOutside = null;

    function isOutside(event) {
      const rect = dialog.getBoundingClientRect();
      return event.clientX < rect.left || event.clientX > rect.right
        || event.clientY < rect.top || event.clientY > rect.bottom;
    }

    function closeFigure() {
      if (dialog.open) dialog.close();
    }

    image.addEventListener('load', () => {
      if (dialog.open && image.hasAttribute('src')) image.hidden = false;
    });
    image.addEventListener('error', () => {
      image.hidden = true;
      image.removeAttribute('src');
    });

    document.querySelectorAll('.pub-teaser[data-figure][data-caption]')
      .forEach((trigger) => {
        trigger.setAttribute('aria-haspopup', 'dialog');
        if (dialog.id) trigger.setAttribute('aria-controls', dialog.id);

        trigger.addEventListener('click', (event) => {
          const source = trigger.dataset.figure.trim();
          if (!source || dialog.open || !dialog.isConnected) return;
          event.preventDefault();

          returnFocus = trigger;
          pointerStartedOutside = null;
          image.hidden = true;
          image.alt = trigger.dataset.caption;
          caption.textContent = trigger.dataset.caption;
          image.src = source;
          dialog.showModal();
          closeButton.focus({ preventScroll: true });
        });
      });

    closeButton.addEventListener('click', (event) => {
      event.preventDefault();
      closeFigure();
    });
    // Escape uses the native dialog cancellation event and one close path.
    dialog.addEventListener('cancel', (event) => {
      event.preventDefault();
      closeFigure();
    });
    dialog.addEventListener('pointerdown', (event) => {
      pointerStartedOutside = event.target === dialog && isOutside(event);
    });
    dialog.addEventListener('click', (event) => {
      const backdropClick = event.target === dialog && isOutside(event)
        && pointerStartedOutside !== false;
      pointerStartedOutside = null;
      if (backdropClick) closeFigure();
    });
    dialog.addEventListener('close', () => {
      if (dialog.open) return;
      const trigger = returnFocus;
      returnFocus = null;
      pointerStartedOutside = null;
      image.hidden = true;
      image.removeAttribute('src');
      if (trigger && trigger.isConnected) {
        trigger.focus({ preventScroll: true });
      }
    });
  }

  function respectReducedMotion() {
    if (typeof window.matchMedia !== 'function') return;
    const preference = window.matchMedia('(prefers-reduced-motion: reduce)');
    const style = document.documentElement.style;
    const originalValue = style.getPropertyValue('scroll-behavior');
    const originalPriority = style.getPropertyPriority('scroll-behavior');
    let overridden = false;

    function updatePreference() {
      if (preference.matches) {
        style.setProperty('scroll-behavior', 'auto', 'important');
        overridden = true;
      } else if (overridden) {
        if (originalValue) {
          style.setProperty('scroll-behavior', originalValue, originalPriority);
        } else {
          style.removeProperty('scroll-behavior');
        }
        overridden = false;
      }
    }

    updatePreference();
    if (typeof preference.addEventListener === 'function') {
      preference.addEventListener('change', updatePreference);
    } else if (typeof preference.addListener === 'function') {
      preference.addListener(updatePreference);
    }
  }

  function initialize() {
    respectReducedMotion();
    initializeNavigation();
    initializeFigures();
    document.querySelectorAll('footer [data-current-year]').forEach((element) => {
      element.textContent = String(new Date().getFullYear());
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initialize, { once: true });
  } else {
    initialize();
  }
})();
