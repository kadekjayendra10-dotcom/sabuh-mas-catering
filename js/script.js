(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#main-nav');
  const panels = [...document.querySelectorAll('[data-view]')];
  const routeLinks = [...document.querySelectorAll('[data-route]')];
  const routes = new Set(panels.map((panel) => panel.dataset.view));

  const closeMenu = () => {
    if (!menuButton || !navigation) return;
    menuButton.setAttribute('aria-expanded', 'false');
    menuButton.setAttribute('aria-label', 'Buka navigasi');
    navigation.classList.remove('is-open');
  };

  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Buka navigasi' : 'Tutup navigasi');
      navigation.classList.toggle('is-open', !isOpen);
    });
    document.addEventListener('click', (event) => {
      if (menuButton.getAttribute('aria-expanded') === 'true' && !navigation.contains(event.target) && !menuButton.contains(event.target)) closeMenu();
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu();
        menuButton.focus();
      }
    });
  }

  const activateRoute = (requestedRoute, writeHistory = false) => {
    const route = routes.has(requestedRoute) ? requestedRoute : 'beranda';
    panels.forEach((panel) => {
      const active = panel.dataset.view === route;
      panel.classList.toggle('is-active', active);
      panel.hidden = !active;
      panel.setAttribute('aria-hidden', String(!active));
    });
    navigation?.querySelectorAll('[data-route]').forEach((link) => {
      if (link.dataset.route === route) link.setAttribute('aria-current', 'page');
      else link.removeAttribute('aria-current');
    });
    closeMenu();
    if (writeHistory && window.location.hash !== `#${route}`) window.history.pushState({}, '', `#${route}`);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  routeLinks.forEach((link) => link.addEventListener('click', (event) => {
    const route = link.dataset.route;
    if (!routes.has(route)) return;
    event.preventDefault();
    activateRoute(route, true);
  }));
  window.addEventListener('hashchange', () => activateRoute(window.location.hash.slice(1)));
  window.addEventListener('popstate', () => activateRoute(window.location.hash.slice(1)));
  activateRoute(window.location.hash.slice(1));

  const yearElement = document.querySelector('#year');
  if (yearElement) yearElement.textContent = new Date().getFullYear();

  const galleryImages = [...document.querySelectorAll('[data-gallery-image]')];
  const lightbox = document.querySelector('[data-lightbox]');
  const lightboxImage = lightbox?.querySelector('[data-lightbox-image]');
  const lightboxCaption = lightbox?.querySelector('[data-lightbox-caption]');
  let galleryIndex = 0;

  const closeLightbox = () => {
    if (!lightbox) return;
    lightbox.hidden = true;
    document.body.classList.remove('lightbox-open');
  };
  const renderLightbox = (nextIndex) => {
    if (!galleryImages.length || !lightboxImage) return;
    galleryIndex = (nextIndex + galleryImages.length) % galleryImages.length;
    const source = galleryImages[galleryIndex];
    lightboxImage.src = source.src;
    lightboxImage.alt = source.alt;
    if (lightboxCaption) lightboxCaption.textContent = source.alt;
  };
  const openLightbox = (imageIndex) => {
    if (!lightbox) return;
    renderLightbox(imageIndex);
    lightbox.hidden = false;
    document.body.classList.add('lightbox-open');
    lightbox.querySelector('[data-lightbox-close]')?.focus();
  };
  galleryImages.forEach((image, imageIndex) => image.addEventListener('click', () => openLightbox(imageIndex)));
  lightbox?.querySelector('[data-lightbox-close]')?.addEventListener('click', closeLightbox);
  lightbox?.querySelector('[data-lightbox-prev]')?.addEventListener('click', () => renderLightbox(galleryIndex - 1));
  lightbox?.querySelector('[data-lightbox-next]')?.addEventListener('click', () => renderLightbox(galleryIndex + 1));
  lightbox?.addEventListener('click', (event) => { if (event.target === lightbox) closeLightbox(); });
  document.addEventListener('keydown', (event) => {
    if (!lightbox || lightbox.hidden) return;
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft') renderLightbox(galleryIndex - 1);
    if (event.key === 'ArrowRight') renderLightbox(galleryIndex + 1);
  });
})();
