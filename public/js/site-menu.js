document.addEventListener('DOMContentLoaded', function () {
  var menu = document.getElementById('site-menu');
  var openButton = document.querySelector('[data-site-menu-open]');
  var closeButton = document.querySelector('[data-site-menu-close]');

  if (!menu || !openButton || !closeButton) return;

  function getFocusableElements() {
    return Array.prototype.slice.call(
      menu.querySelectorAll('a[href], button:not([disabled])')
    );
  }

  function openMenu() {
    menu.hidden = false;
    menu.setAttribute('aria-hidden', 'false');
    openButton.setAttribute('aria-expanded', 'true');
    document.body.classList.add('site-menu-is-open');
    closeButton.focus();
  }

  function closeMenu() {
    menu.hidden = true;
    menu.setAttribute('aria-hidden', 'true');
    openButton.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('site-menu-is-open');
    openButton.focus();
  }

  openButton.addEventListener('click', openMenu);
  closeButton.addEventListener('click', closeMenu);

  document.addEventListener('keydown', function (event) {
    if (event.key === 'Escape' && !menu.hidden) {
      closeMenu();
    }

    if (event.key === 'Tab' && !menu.hidden) {
      var focusableElements = getFocusableElements();
      var firstElement = focusableElements[0];
      var lastElement = focusableElements[focusableElements.length - 1];

      if (!firstElement || !lastElement) return;

      if (event.shiftKey && document.activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      } else if (!event.shiftKey && document.activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  });
});
