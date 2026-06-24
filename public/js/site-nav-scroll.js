document.addEventListener('DOMContentLoaded', function () {
  var header = document.querySelector('.site-header');
  if (!header || typeof Observer === 'undefined') return;

  gsap.registerPlugin(Observer);

  var threshold = 40;

  function setScrolled(scrolled) {
    header.classList.toggle('is-scrolled', scrolled);
  }

  setScrolled(window.scrollY >= threshold);

  Observer.create({
    type: 'wheel,touch,scroll,pointer',
    onChange: function () {
      setScrolled(window.scrollY >= threshold);
    }
  });
});
