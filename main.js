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
    alt: () => siteI18n.text('Actual Astera conversation view with four Claude Code and Codex sessions next to the account and project sidebar.', '계정·프로젝트 사이드바 옆에 Claude Code와 Codex 세션 네 개가 열린 실제 Astera 채팅 화면.')
  },
  terminal: {
    src: 'assets/hero.jpg',
    alt: () => siteI18n.text('Actual Astera terminal view with four sessions running across Claude Code and Codex accounts.', 'Claude Code와 Codex 계정으로 세션 네 개를 실행 중인 실제 Astera 터미널 화면.')
  }
};

const demos = {
  jobs: { src: 'assets/astera-killer-demo.mp4', title: () => siteI18n.text('From parallel work to verified results', '병렬 작업부터 결과 검증까지') },
  rolling: { src: 'assets/astera-demo-rolling.mp4', title: () => siteI18n.text('Account rolling in action', '계정 자동 전환 데모') },
  schedule: { src: 'assets/astera-demo-schedule.mp4', title: () => siteI18n.text('Scheduled sessions in action', '세션 예약 데모') }
};

document.querySelectorAll('[data-view]').forEach((button) => {
  button.addEventListener('click', () => {
    const view = views[button.dataset.view];
    productImage.src = view.src;
    productImage.alt = view.alt();
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
    video.setAttribute('aria-label', demo.title());
    video.addEventListener('error', () => {
      const fallback = document.createElement('p');
      fallback.className = 'video-error';
      fallback.textContent = siteI18n.text('This browser could not play the demo. ', '이 브라우저에서 데모를 재생할 수 없습니다. ');
      const link = document.createElement('a');
      link.href = demo.src;
      link.textContent = siteI18n.text('Open the video file', '영상 파일 열기');
      fallback.append(link);
      mediaContent.replaceChildren(fallback);
    }, { once: true });
    openMedia(demo.title(), video);
    video.play().catch(() => { /* Controls remain available if autoplay is blocked. */ });
  });
});

document.querySelector('.screenshot-button').addEventListener('click', () => {
  const image = document.createElement('img');
  image.src = productImage.src;
  image.alt = productImage.alt;
  openMedia(siteI18n.text('Inside Astera', 'Astera 실제 화면'), image);
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
  menuToggle.setAttribute('aria-label', siteI18n.text('Open menu', '메뉴 열기'));
}

menuToggle.addEventListener('click', () => {
  const opening = mobileNav.hidden;
  mobileNav.hidden = !opening;
  menuToggle.setAttribute('aria-expanded', String(opening));
  menuToggle.setAttribute('aria-label', opening ? siteI18n.text('Close menu', '메뉴 닫기') : siteI18n.text('Open menu', '메뉴 열기'));
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
    button.setAttribute('aria-label', dark ? siteI18n.text('Switch to light theme', '라이트 테마로 전환') : siteI18n.text('Switch to dark theme', '다크 테마로 전환'));
    button.title = button.getAttribute('aria-label');
    button.querySelector('span').textContent = dark ? siteI18n.text('Light theme', '라이트 테마') : siteI18n.text('Dark theme', '다크 테마');
    button.querySelector('use').setAttribute('href', dark ? '#i-sun' : '#i-moon');
  });
  document.querySelector('meta[name="theme-color"]').content = dark ? '#0b1020' : '#f7f8fc';
  document.querySelectorAll('[data-theme-link]').forEach((link) => {
    const url = new URL(link.href);
    url.searchParams.set('theme', dark ? 'dark' : 'light');
    link.href = url.href;
  });
}

function updateInterfaceLanguage() {
  productImage.alt = views[document.querySelector('[data-view].active').dataset.view].alt();
  menuToggle.setAttribute('aria-label', mobileNav.hidden ? siteI18n.text('Open menu', '메뉴 열기') : siteI18n.text('Close menu', '메뉴 닫기'));
  document.querySelectorAll('.brand[aria-label]').forEach((link) => {
    link.setAttribute('aria-label', siteI18n.text('Astera home', 'Astera 홈'));
  });
  setTheme(document.documentElement.dataset.theme === 'dark');
}

updateInterfaceLanguage();
document.addEventListener('languagechange', updateInterfaceLanguage);

themeToggles.forEach((button) => {
  button.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    setTheme(dark);
    const url = new URL(location.href);
    url.searchParams.set('theme', dark ? 'dark' : 'light');
    history.replaceState(null, '', url);
  });
});
