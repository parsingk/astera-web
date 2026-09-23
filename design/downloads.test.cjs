const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..');
const releasePage = 'https://github.com/parsingk/Astera/releases/latest';
const assets = ['astera-1.3.25-setup.exe', 'astera-1.3.25-universal.dmg', 'astera-1.3.25-x86_64.AppImage']
  .map((name) => ({ name, browser_download_url: `https://github.com/parsingk/Astera/releases/download/v1.3.25/${name}` }));
const script = fs.readFileSync(path.join(root, 'downloads.js'), 'utf8');

function makeLink() {
  return {
    href: releasePage,
    target: '_blank',
    removeAttribute(name) { delete this[name]; },
    addEventListener(name, handler) { this[name] = handler; }
  };
}

async function check(platform, expected, options = {}) {
  const links = Array.from({ length: 5 }, makeLink);
  let assigned = null;
  const release = { tag_name: 'v1.3.25', assets: options.assets ?? assets };
  vm.runInNewContext(script, {
    navigator: { platform, userAgent: options.userAgent ?? `${platform} x86_64` },
    document: { querySelectorAll: () => links },
    fetch: async () => ({ ok: !options.failure, json: async () => release }),
    location: { assign: (url) => { assigned = url; } },
    Promise
  });
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert(links.every((link) => link.href === expected));
  if (expected !== releasePage) assert(links.every((link) => !('target' in link)));
  let prevented = false;
  links[0].click({ preventDefault() { prevented = true; } });
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.equal(assigned, null);
  assert.equal(prevented, false);
}

async function checkEarlyClick() {
  const links = [makeLink()];
  let assigned = null;
  let finish;
  vm.runInNewContext(script, {
    navigator: { platform: 'Win32', userAgent: 'Win32 x86_64' },
    document: { querySelectorAll: () => links },
    fetch: () => new Promise((resolve) => { finish = resolve; }),
    location: { assign: (url) => { assigned = url; } },
    Promise
  });
  let prevented = false;
  links[0].click({ preventDefault() { prevented = true; } });
  assert.equal(prevented, true);
  assert.equal(assigned, null);
  finish({ ok: true, json: async () => ({ tag_name: 'v1.3.25', assets }) });
  await new Promise((resolve) => setTimeout(resolve, 0));
  assert.equal(assigned, assets[0].browser_download_url);
}

(async () => {
  await check('Win32', assets[0].browser_download_url);
  await check('MacIntel', assets[1].browser_download_url);
  await check('Linux x86_64', assets[2].browser_download_url);
  await check('Linux aarch64', releasePage, { userAgent: 'Linux aarch64' });
  await check('Android', releasePage, { userAgent: 'Android Mobile' });
  await check('Win32', releasePage, { failure: true });
  await check('Win32', releasePage, { assets: [] });
  await checkEarlyClick();
  assert.equal((fs.readFileSync(path.join(root, 'index.html'), 'utf8').match(/data-download/g) ?? []).length, 3);
  assert.equal((fs.readFileSync(path.join(root, 'guide.html'), 'utf8').match(/data-download/g) ?? []).length, 2);
  console.log('Download routing: 8 scenarios and 5 website buttons passed.');
})().catch((error) => { console.error(error); process.exitCode = 1; });
