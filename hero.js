const hero = document.querySelector('.hero');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)');
let heroFrame = 0;
let spaceX = 0;
let spaceY = 0;

function resetSpace() {
  cancelAnimationFrame(heroFrame);
  heroFrame = 0;
  hero.style.removeProperty('--space-x');
  hero.style.removeProperty('--space-y');
}

function moveSpace(event) {
  if (event.pointerType === 'touch' || reducedMotion.matches || !finePointer.matches) return;
  const bounds = hero.getBoundingClientRect();
  const clamp = (value) => Math.max(-.5, Math.min(.5, value));
  spaceX = clamp((event.clientX - bounds.left) / bounds.width - .5) * 48;
  spaceY = clamp((event.clientY - bounds.top) / Math.min(bounds.height, 800) - .5) * 36;
  if (heroFrame) return;
  heroFrame = requestAnimationFrame(() => {
    hero.style.setProperty('--space-x', `${spaceX}px`);
    hero.style.setProperty('--space-y', `${spaceY}px`);
    heroFrame = 0;
  });
}

hero.addEventListener('pointermove', moveSpace, { passive: true });
hero.addEventListener('pointerleave', resetSpace);
hero.addEventListener('pointercancel', resetSpace);
reducedMotion.addEventListener('change', resetSpace);
finePointer.addEventListener('change', resetSpace);
document.addEventListener('visibilitychange', () => {
  if (document.hidden) resetSpace();
});
