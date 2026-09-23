const contents = document.querySelector('.guide-contents');
const compactGuide = window.matchMedia('(max-width: 900px)');
const contentsLinks = contents.querySelectorAll('nav a');

function setContentsLayout() {
  contents.open = !compactGuide.matches;
}

function highlightSection(link) {
  contentsLinks.forEach((item) => {
    if (item === link) item.setAttribute('aria-current', 'location');
    else item.removeAttribute('aria-current');
  });
}

setContentsLayout();
compactGuide.addEventListener('change', setContentsLayout);
contentsLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    history.pushState(null, '', link.hash);
    document.getElementById(link.hash.slice(1)).scrollIntoView({ behavior: 'instant' });
    highlightSection(link);
    if (compactGuide.matches) contents.open = false;
  });
});

const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    const link = [...contentsLinks].find((item) => item.hash === `#${entry.target.id}`);
    if (link) highlightSection(link);
  });
}, { rootMargin: '-15% 0px -65% 0px' });

document.querySelectorAll('.guide-section').forEach((section) => sectionObserver.observe(section));
