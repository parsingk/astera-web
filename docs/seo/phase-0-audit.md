# SEO Phase 0 감사 보고서

- 기준일: 2026-11-25
- 대상: `parsingk/astera-web` `main` (마지막 커밋 `b3c7eae`, 2026-11-02 배포본) + 커밋되지 않은 v1.5.1~v1.5.5 가이드 변경
- 근거 앱 버전: Astera v1.5.5 (`parsingk/Astera` 최신 릴리스, 2026-11-24, `origin/main` `9e6d8aea`)
- 지시서: `astera-run-seo-expansion-implementation.md` v1.0

## 1. 배포 구조

| 항목 | 확인 결과 | 근거 |
|---|---|---|
| 호스팅 | **GitHub Pages** (Cloudflare Pages 아님) | 응답 헤더 `Server: GitHub.com`, Fastly `Via: 1.1 varnish`; `gh api repos/parsingk/astera-web/pages` |
| 빌드 | `build_type: legacy` (Jekyll), `main` 브랜치 `/` | 같은 API 응답 |
| 도메인 | `CNAME` = `astera.run`, HTTPS 강제, 인증서 `astera.run`·`www.astera.run` (만료 2027-02-20) | 같은 API 응답 |
| 배포 시점 | `main`에 push하면 곧바로 운영 반영 | Pages source = `main` |
| 사용자 정의 404 | 없음 (`custom_404: false`) — GitHub 기본 404 페이지 | `/nonexistent-seo-smoke-test` → 404 |
| `_redirects` / `_headers` | 없음. GitHub Pages는 둘 다 지원하지 않음 | 저장소 파일 목록 |
| 빌드 도구 | 없음(정적 HTML). 한국어 페이지만 `tools/build_locales.py`가 `locales/ko.js`로 생성 | `tools/build_locales.py` |
| 테스트 | `design/test_search.py`(7), `design/downloads.test.cjs`(8 시나리오·5 버튼), `build_locales.py --check`, `design/review.html` 브라우저 검사 | README |
| CI | 없음 (`.github/workflows` 없음) | 저장소 파일 목록 |

**지시서와 다른 점**: 지시서는 Cloudflare Pages의 `_redirects`·`_headers`를 전제로 한다. GitHub Pages에서는 다음만 가능하다.

- 영구 리디렉션은 플랫폼이 하는 것뿐이다: `http→https`, `www→apex`(둘 다 301 확인), 디렉터리 `/slug` → `/slug/`.
- 임의 별칭의 301/308, 응답 헤더(`X-Robots-Tag`, CSP, HSTS) 추가는 불가능하다. 별칭 URL을 만들지 않는 것으로 대응한다.
- `404.html`을 루트에 두면 404 상태로 제공된다.

## 2. URL과 응답

| URL | 상태 | 비고 |
|---|---|---|
| `https://astera.run/` | 200 | 정본 |
| `https://astera.run/index.html` | 200 | 중복. canonical이 `/`를 가리킴 |
| `https://astera.run/index.ko.html` | 200 | 정본(한국어) |
| `https://astera.run/index.ko` | 200 | 확장자 없는 중복. canonical로 정리됨 |
| `https://astera.run/guide.html` | 200 | 정본 |
| `https://astera.run/guide` | 200 | 중복. canonical이 `guide.html`을 가리킴 |
| `https://astera.run/guide.ko.html` | 200 | 정본(한국어) |
| `http://astera.run/` | 301 → `https://astera.run/` | |
| `https://www.astera.run/` | 301 → `https://astera.run/` | |
| `https://astera.run/robots.txt` | 200 | `Allow: /`, sitemap 경로 정상 |
| `https://astera.run/sitemap.xml` | 200 | 4개 URL, `lastmod` 모두 2026-09-30 |
| `https://astera.run/design/review.html` | 200 | `noindex,follow` 메타 있음 |
| `https://astera.run/docs/product-positioning.html` | **200, 색인 가능** | Jekyll이 `docs/*.md`를 HTML로 변환해 공개. 제목 "Astera 기능 강조 근거 \| astera-web" |
| `https://astera.run/docs/design-direction.html` | **200, 색인 가능** | 같은 원인 |
| `https://astera.run/README.md`, `docs/*.md`, `tools/*.py`, `design/*.py` | 200 | 원문 파일 그대로 공개 |
| 없는 경로 | 404 | soft 404 없음, 홈 fallback 없음 |

모든 HTML 응답은 `Cache-Control: max-age=600`. 보안 헤더(CSP·HSTS)는 사이트 페이지에 없다. 약화할 기존 정책이 없고 GitHub Pages에서는 추가할 수도 없다.

## 3. 기존 메타데이터

| 항목 | 홈(en/ko) | 가이드(en/ko) |
|---|---|---|
| `title`·description | 있음, 언어별 고유 | 있음, 언어별 고유 |
| canonical | self, HTTPS 절대 주소 | self, HTTPS 절대 주소 |
| hreflang | en·ko·x-default 상호 참조 | en·ko·x-default 상호 참조 |
| Open Graph / X card | 있음 (`banner.jpg` 1254×625), `og:locale` 언어별 | 있음 |
| `og:image:alt` | 없음 | 없음 |
| JSON-LD | `SoftwareApplication` (`@id` `https://astera.run/#app`, Apache-2.0, 가격 0, OS 범위) | 없음 |
| `WebSite` 엔티티 | 없음 | 없음 |
| H1 | "Step away. Keep building." (제품 범주 문구 없음, 두 언어 모두 영어) | "Get to know Astera." |
| `meta keywords` | 없음 (유지) | 없음 |

JSON-LD의 OS 범위(Windows 10/11, macOS 12+, Ubuntu 22.04+/Debian 12+)와 라이선스는 앱 README·GitHub 라이선스 정보와 일치한다.

## 4. 다국어 동작

- 영어 원문 HTML의 `data-i18n` 키 + `locales/ko.js` 카탈로그. `build_locales.py`가 `index.ko.html`·`guide.ko.html`을 정적으로 생성한다(크롤러가 JS 없이 한국어를 읽음).
- `build_locales.py`의 대상 페이지는 `index.html`·`guide.html` 두 개로 고정돼 있다. 새 페이지를 추가하려면 이 목록을 넓혀야 한다.
- **주의**: 영어 URL(`/`, `/guide.html`)은 저장된 선택이 없고 브라우저 언어가 `ko`이면 같은 URL에서 본문을 한국어로 바꿔 보여 준다. 리디렉션은 아니며 크롤러(영어 환경)는 영어를 본다. 지시서 6.2의 "브라우저 언어로 강제 리디렉션 금지"에는 걸리지 않지만, 같은 URL이 방문자에 따라 다른 언어를 보여 주는 동작이다. 기존 설계(README에 기록됨)이므로 바꾸지 않고 소유자 판단 항목으로 남긴다.
- 언어 전환은 실제 `<a>`가 아니라 버튼(JS)이다. 한국어 정적 페이지에서는 영어 페이지로 이동하고, 영어 페이지에서는 같은 URL에서 바뀐다.

## 5. 분석·검색 등록

| 항목 | 상태 |
|---|---|
| 분석 스크립트 (GA·Plausible·Cloudflare 등) | 없음 |
| Search Console / Bing / 네이버 확인 메타 태그 | 없음. DNS 방식 등록 여부는 **미확인**(소유자 권한 필요) |
| Search Console 데이터 | 미확인 |
| 다운로드 클릭 측정 | 없음. GitHub Releases `download_count`만 가능 |

## 6. 에셋

`assets/` 4.6 MB: `hero.jpg`, `banner.jpg`, `conversation.jpg`, 데모 MP4 3개와 GIF·정지 이미지 3쌍, 폰트(Public Sans) 2개, 아이콘. 모든 `<img>`에 `alt`와 `width`/`height`가 있다(아래 측정). 새 페이지는 이 에셋을 재사용할 수 있다. 앱 저장소에는 `assets/rolling.gif` 등 사이트에 없는 다이어그램이 더 있다.

## 7. 기준선 (변경 전, 운영 사이트, 2026-11-25 측정)

Playwright Chromium 랩 측정. 필드 데이터(CrUX)는 트래픽 규모상 **미측정**이며 아래 수치는 실제 사용자 Core Web Vitals가 아니다. INP는 랩에서 측정하지 않았다.

모바일(390×844, DPR 3, 지연 150 ms·1.6 Mbps, CPU 4배 감속, 캐시 끔):

| 페이지 | LCP | CLS | 요청 | 전송량 | LCP 요소 | 가로 넘침 | 콘솔 오류 |
|---|---|---|---|---|---|---|---|
| `/` | 1,636 ms | 0 | 15 | 670 KB | `div.space-stars` | 없음 | 0 |
| `/index.ko.html` | 1,992 ms | 0 | 15 | 671 KB | `div.space-stars` | 없음 | 0 |
| `/guide.html` | 1,288 ms | 0 | 13 | 195 KB | `a` | 없음 | 0 |
| `/guide.ko.html` | 1,744 ms | 0 | 13 | 198 KB | `a` | 없음 | 0 |

데스크톱(1440×900, 감속 없음): LCP 228~332 ms, CLS 0, 가로 넘침 없음, 콘솔 오류 0.

JS 끔(390 px): 네 페이지 모두 본문·링크(홈 41개, 가이드 115개)·다운로드 링크(`releases/latest`)를 읽을 수 있고 가로 넘침이 없다. 이미지 `alt` 누락 0, 크기 누락 0.

Lighthouse는 저장소에 없고 새 의존성을 추가하지 않았으므로 실행하지 않았다.

## 8. 외부에서 들어오는 링크

- 앱 저장소(`parsingk/Astera` `origin/main`)는 `https://astera.run` 루트만 9곳에서 링크한다. 가이드 앵커로 들어오는 링크는 없다.
- 홈 → 가이드 앵커 링크 16종, 가이드 섹션 31개(`#quickstart`~`#faq`). 이 앵커는 모두 보존 대상이다.
- 그 밖의 외부 링크(블로그, 커뮤니티)는 **미확인**.

## 9. 기능 근거 매트릭스 (P0 대상)

모든 기능은 v1.5.5에 출시돼 있다. 가이드 해당 섹션은 이전 업데이트에서 앱 소스와 대조됐다(`docs/product-positioning.md`의 날짜별 기록).

| P0 페이지 | 주 근거(앱 저장소 `origin/main`) | 가이드 앵커 | 반드시 함께 쓸 조건 |
|---|---|---|---|
| `/claude-code` | `README.md` What it does, `docs/usage-guide.md` | `#quickstart` `#sessions` `#accounts` | Claude Code CLI 설치·로그인 필요, Astera는 Anthropic과 무관한 독립 프로젝트, AI 사용료는 별도 |
| `/codex` | `README.md`, `docs/usage-guide.md` | `#quickstart` `#sessions` | Codex CLI 필요, OpenAI 공식 Codex 앱과 별개 |
| `/features/agent-orchestration` | `docs/jobs.md`, `docs/cli.md` | `#jobs` `#orchestration` `#completion-plugins` `#reviewers` | Host 필요, 검토자·체크는 설정 필요 |
| `/features/smart-resume` | `README.md` Smart Resume, `docs/usage-guide.md` | `#smart-resume` | 기본 꺼짐, 체크포인트 범위·비밀값 가림, 일반 resume과 차이 |
| `/features/github-ci` | `docs/jobs.md`, 릴리스 노트 v1.4.15~v1.5.3 | `#job-sources` `#github-lifecycle` | `gh` 로그인, draft PR, 병합은 사람, head 변경 시 상태 철회 |
| `/guides/claude-code-usage-limit` | `README.md` Accounts, Smart Resume | `#accounts` `#smart-resume` `#scheduling` | 제공사 정책 공식 링크, 한도 우회·무제한 사용 표현 금지 (조사 중) |
| `/alternatives/orca` | 경쟁 제품 공식 자료 | — | 공식 근거만, 미확인은 "Not documented" (조사 중) |
| `/alternatives/paseo` | 경쟁 제품 공식 자료 | — | 위와 같음 (조사 중) |

## 10. 키워드 충돌·중복

- `/features/*`와 가이드 섹션이 같은 기능을 다룬다. 기능 페이지는 "무엇을 해결하는지·언제 쓰는지·조건과 한계·FAQ"를 맡고, 단계별 조작은 가이드 앵커로 보낸다. 가이드 문단을 복사하지 않는다.
- `/features/account-rolling`(P1)과 `/guides/claude-code-usage-limit`(P0)는 의도가 겹친다. P0 가이드가 먼저 나가고, P1에서 분리할지 다시 판단한다.
- `/features`·`/guides` 허브는 기존 홈 섹션·가이드와 겹친다. P0 단계에서는 별도 허브를 만들지 않고 홈과 푸터에서 직접 링크한다(3클릭 이내 충족).
- 홈 `title`이 이미 "Claude Code & Codex Desktop Workspace"를 쓴다. `/claude-code` 제목은 "Claude Code Desktop Workspace"를 쓰므로 홈과 겹친다. 두 페이지의 의도(홈: 제품 전체, `/claude-code`: Claude Code 사용자의 설정·한계)를 본문으로 구분해야 한다.

## 11. 발견 사항과 조치 제안

| # | 발견 | 영향 | 제안 | 결정 |
|---|---|---|---|---|
| F1 | 호스팅이 GitHub Pages | `_redirects`·`_headers` 불가 | 별칭 URL을 만들지 않는다. 새 페이지는 `slug/index.html`(정본 `/slug/`)로 두면 `/slug` → `/slug/` 301을 플랫폼이 처리 | 기술 기본값 |
| F2 | `docs/*.md`가 HTML 페이지로 공개·색인 가능 | 내부 메모가 검색에 노출, 얇은 중복 페이지 | `_config.yml`의 `exclude`로 `docs/`, `tools/`, `README.md`와 `design/`의 테스트 스크립트를 사이트에서 뺀다 | **소유자 확인 필요**(공개 URL 제거) |
| F3 | 사용자 정의 404 없음 | 사이트 이탈 | 루트 `404.html` 추가 (`noindex`) | 기술 기본값 |
| F4 | sitemap `lastmod`가 모두 2026-09-30 | 실제 변경일과 다름 | 생성 스크립트가 git 기록에서 콘텐츠 변경일을 읽어 만든다 | 기술 기본값 |
| F5 | 홈 H1에 제품 범주 문구 없음 | 범주 검색 약함 | H1은 두고 바로 아래 본문 또는 kicker에 "desktop workspace for Claude Code and Codex"를 넣는다(지시서 4.4) | Phase 2 |
| F6 | `WebSite` JSON-LD·`og:image:alt` 없음, 가이드 JSON-LD 없음 | 경미 | 홈에 `WebSite` 추가, 기존 `@id` `#app` 유지(바꾸지 않음) | Phase 1 |
| F7 | 영어 URL이 브라우저 언어로 본문을 바꿈 | 경미(리디렉션 아님) | 유지, 소유자 판단 항목 | 소유자 판단 |
| F8 | CI 없음 | 회귀 검사 수동 | 검증 스크립트를 Python 표준 라이브러리로 만들고, CI 추가는 선택 사항으로 둔다 | Phase 1 |
| F9 | 커밋 안 된 v1.5.x 가이드 변경 7파일 | Phase 커밋과 섞임 | SEO 작업 전에 별도 커밋 | **소유자 확인 필요** |

## 12. 미확인 항목

- Search Console·Bing 등록 여부와 색인 현황 (소유자 계정 필요)
- 실사용자 Core Web Vitals (필드 데이터 없음)
- GitHub Pages에서 새 디렉터리 페이지의 `/slug` → `/slug/` 301 (배포 후 확인)
- 경쟁 제품(Orca·Paseo) 사실, AI 제공사 사용량 정책 (공식 자료 조사 중)
- 사이트로 들어오는 외부 링크 목록
