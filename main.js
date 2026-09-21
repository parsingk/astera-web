const productImage = document.querySelector('#product-image');
const dialog = document.querySelector('#media-dialog');
const mediaContent = document.querySelector('#media-content');
const mediaTitle = document.querySelector('#media-title');
const menuToggle = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('#mobile-nav');
const themeToggles = document.querySelectorAll('.theme-toggle');

const views = {
  conversation: {
    src: 'assets/conversation.jpg',
    alt: 'Actual Astera conversation view with four Claude Code and Codex sessions next to the account and project sidebar.'
  },
  terminal: {
    src: 'assets/hero.jpg',
    alt: 'Actual Astera terminal view with four sessions running across Claude Code and Codex accounts.'
  }
};

const demos = {
  jobs: { src: 'assets/astera-killer-demo.mp4', title: 'From parallel work to verified results' },
  rolling: { src: 'assets/astera-demo-rolling.mp4', title: 'Account rolling in action' },
  schedule: { src: 'assets/astera-demo-schedule.mp4', title: 'Scheduled sessions in action' }
};

document.querySelectorAll('[data-view]').forEach((button) => {
  button.addEventListener('click', () => {
    const view = views[button.dataset.view];
    productImage.src = view.src;
    productImage.alt = view.alt;
    document.querySelectorAll('[data-view]').forEach((item) => {
      const selected = item === button;
      item.classList.toggle('active', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
  });
});

function openMedia(title, element) {
  mediaTitle.textContent = title;
  mediaContent.replaceChildren(element);
  dialog.showModal();
  document.body.classList.add('dialog-open');
}

document.querySelectorAll('[data-demo]').forEach((button) => {
  button.addEventListener('click', () => {
    const demo = demos[button.dataset.demo];
    const video = document.createElement('video');
    video.controls = true;
    video.playsInline = true;
    video.preload = 'metadata';
    video.src = demo.src;
    video.setAttribute('aria-label', demo.title);
    video.addEventListener('error', () => {
      const fallback = document.createElement('p');
      fallback.className = 'video-error';
      fallback.textContent = 'This browser could not play the demo. ';
      const link = document.createElement('a');
      link.href = demo.src;
      link.textContent = 'Open the video file';
      fallback.append(link);
      mediaContent.replaceChildren(fallback);
    }, { once: true });
    openMedia(demo.title, video);
  });
});

document.querySelector('.screenshot-button').addEventListener('click', () => {
  const image = document.createElement('img');
  image.src = productImage.src;
  image.alt = productImage.alt;
  openMedia('Inside Astera', image);
});

function closeMedia() {
  const video = mediaContent.querySelector('video');
  if (video) video.pause();
  mediaContent.replaceChildren();
  document.body.classList.remove('dialog-open');
  dialog.close();
}

document.querySelector('.dialog-close').addEventListener('click', closeMedia);
dialog.addEventListener('click', (event) => {
  if (event.target !== dialog) return;
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right ||
      event.clientY < bounds.top || event.clientY > bounds.bottom) closeMedia();
});
dialog.addEventListener('cancel', (event) => {
  event.preventDefault();
  closeMedia();
});

function closeMenu() {
  mobileNav.hidden = true;
  menuToggle.setAttribute('aria-expanded', 'false');
  menuToggle.setAttribute('aria-label', 'Open menu');
}

menuToggle.addEventListener('click', () => {
  const opening = mobileNav.hidden;
  mobileNav.hidden = !opening;
  menuToggle.setAttribute('aria-expanded', String(opening));
  menuToggle.setAttribute('aria-label', opening ? 'Close menu' : 'Open menu');
});
mobileNav.querySelectorAll('a').forEach((link) => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape' && !mobileNav.hidden) {
    closeMenu();
    menuToggle.focus();
  }
});
window.matchMedia('(min-width: 761px)').addEventListener('change', (event) => {
  if (event.matches) closeMenu();
});

function setTheme(dark) {
  document.documentElement.dataset.theme = dark ? 'dark' : 'light';
  themeToggles.forEach((button) => {
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', dark ? 'Switch to light theme' : 'Switch to dark theme');
    button.title = dark ? 'Switch to light theme' : 'Switch to dark theme';
    button.querySelector('span').textContent = dark ? 'Light theme' : 'Dark theme';
    button.querySelector('use').setAttribute('href', dark ? '#i-sun' : '#i-moon');
  });
  document.querySelector('meta[name="theme-color"]').content = dark ? '#0b1020' : '#f7f8fc';
}

setTheme(document.documentElement.dataset.theme === 'dark');

themeToggles.forEach((button) => {
  button.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    setTheme(dark);
    const url = new URL(location.href);
    url.searchParams.set('theme', dark ? 'dark' : 'light');
    history.replaceState(null, '', url);
  });
});
