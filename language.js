const siteI18n = (() => {
  const supported = (value) => value === 'ko' || value === 'en';
  const requested = new URLSearchParams(location.search).get('lang');
  const staticKorean = document.documentElement.dataset.staticLanguage === 'ko';
  let saved;
  try { saved = localStorage.getItem('astera-language'); } catch { /* Storage can be disabled. */ }
  let language = staticKorean ? 'ko' : supported(requested) ? requested : supported(saved) ? saved :
    /^ko(?:-|$)/i.test(navigator.language) ? 'ko' : 'en';

  const copy = [];
  for (const attribute of ['html', 'content', 'aria-label', 'href']) {
    const marker = attribute === 'html' ? 'data-i18n' : `data-i18n-${attribute}`;
    document.querySelectorAll(`[${marker}]`).forEach((element) => {
      copy.push({ element, attribute, key: element.getAttribute(marker),
        english: attribute === 'html' ? element.innerHTML : element.getAttribute(attribute) });
    });
  }

  function apply() {
    document.documentElement.lang = language;
    copy.forEach(({ element, attribute, key, english }) => {
      const value = language === 'ko' ? koreanMessages[key] ?? english : english;
      // Only the bundled translation catalog is inserted as HTML; URL/storage values never are.
      if (attribute === 'html') element.innerHTML = value;
      else element.setAttribute(attribute, value);
    });
    document.querySelectorAll('.language-toggle').forEach((button) => {
      button.textContent = language === 'ko' ? 'English' : '한국어';
      button.lang = language === 'ko' ? 'en' : 'ko';
      button.setAttribute('aria-label', language === 'ko' ? 'View in English' : '한국어로 보기');
      button.title = button.getAttribute('aria-label');
    });
    document.querySelectorAll('[data-theme-link]').forEach((link) => {
      const url = new URL(link.href);
      url.searchParams.set('lang', language);
      link.href = url.href;
    });
  }

  apply();
  document.querySelectorAll('.language-toggle').forEach((button) => {
    button.addEventListener('click', () => {
      const section = [...document.querySelectorAll('main section')].reverse()
        .find((element) => element.getBoundingClientRect().top <= 130);
      const sectionTop = section?.getBoundingClientRect().top;
      if (staticKorean) {
        try { localStorage.setItem('astera-language', 'en'); } catch { /* URL still preserves it. */ }
        const url = new URL(location.href);
        url.pathname = url.pathname.replace(/\.ko\.html$/, '.html');
        url.searchParams.set('lang', 'en');
        if (section && !url.hash) url.hash = section.id;
        location.assign(url.href);
        return;
      }
      language = language === 'ko' ? 'en' : 'ko';
      try { localStorage.setItem('astera-language', language); } catch { /* URL still preserves it. */ }
      const url = new URL(location.href);
      url.searchParams.set('lang', language);
      history.replaceState(null, '', url);
      apply();
      document.dispatchEvent(new Event('languagechange'));
      if (section) window.scrollBy({ top: section.getBoundingClientRect().top - sectionTop, behavior: 'instant' });
    });
  });

  return { text: (english, korean) => language === 'ko' ? korean : english };
})();
