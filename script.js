const revealObserver = new IntersectionObserver(
  (entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    }
  },
  { threshold: 0.12 }
);

const revealItems = document.querySelectorAll('[data-reveal]');
revealItems.forEach((element) => {
  revealObserver.observe(element);
});

window.setTimeout(() => {
  revealItems.forEach((element) => element.classList.add('is-visible'));
}, 120);

const screenshotOffset = new URLSearchParams(window.location.search).get('shotY');
if (screenshotOffset !== null) {
  revealItems.forEach((element) => element.classList.add('is-visible'));
  requestAnimationFrame(() => {
    window.scrollTo(0, Number(screenshotOffset) || 0);
  });
}
