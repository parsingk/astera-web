const releasePage = 'https://github.com/parsingk/Astera/releases/latest';
const downloadLinks = document.querySelectorAll('[data-download]');
const userAgent = navigator.userAgent;
const platform = navigator.userAgentData?.platform ?? navigator.platform ?? userAgent;
const mobile = /Android|iPad|iPhone|iPod|Mobile/i.test(userAgent);
const os = mobile ? null : /Win/i.test(platform) ? 'windows' :
  /Mac/i.test(platform) ? 'mac' :
  /Linux|X11/i.test(platform) && !/aarch64|arm64|armv/i.test(`${platform} ${userAgent}`) ? 'linux' : null;
const installerSuffix = { windows: 'setup.exe', mac: 'universal.dmg', linux: 'x86_64.AppImage' };
let pending = Boolean(os);

const installer = os ? fetch('https://api.github.com/repos/parsingk/Astera/releases/latest')
  .then((response) => response.ok ? response.json() : null)
  .then((release) => {
    const version = /^v?(\d+\.\d+\.\d+)$/.exec(release?.tag_name)?.[1];
    if (!version) return null;
    const name = `astera-${version}-${installerSuffix[os]}`;
    const url = release.assets?.find((asset) => asset.name === name)?.browser_download_url;
    return url?.startsWith('https://github.com/parsingk/Astera/releases/download/') ? url : null;
  })
  .catch(() => null) : Promise.resolve(null);

installer.then((url) => {
  if (url) {
    downloadLinks.forEach((link) => {
      link.href = url;
      link.removeAttribute('target');
    });
  }
  pending = false;
});

downloadLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    if (!pending) return;
    event.preventDefault();
    installer.then((url) => location.assign(url ?? releasePage));
  });
});
