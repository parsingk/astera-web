# SEO 운영 문서

astera.run 검색 페이지를 추가·갱신·배포하는 방법과, 소유자 계정이 필요한 작업의 수동 절차를 정리한다. 현황 감사는 [phase-0-audit.md](phase-0-audit.md)에 있다.

## 1. 구조

| 파일 | 역할 |
|---|---|
| `content/pages.json` | 페이지 레지스트리. 경로, 언어, 번역 그룹, 제목·설명·H1·리드, 근거 URL과 확인일, 관련 페이지, 푸터 그룹 |
| `content/en/*.html`, `content/ko/*.html` | 페이지 본문(헤더·푸터·메타데이터 제외) |
| `tools/build_pages.py` | 본문을 공통 헤더·메타데이터·JSON-LD·푸터로 감싸 `<경로>/index.html`과 `404.html`을 만들고 `sitemap.xml`을 쓴다 |
| `tools/validate_seo.py` | 공개되는 파일 전체를 검사한다(제목·설명 중복, canonical, hreflang 상호 참조, OG, JSON-LD, sitemap, robots, 404, 이미지 속성, 내부 링크와 앵커, 플레이스홀더) |
| `tools/build_locales.py` | 기존 홈·가이드의 한국어 정적 페이지를 `locales/ko.js`로 만든다 |
| `_config.yml` | GitHub Pages(Jekyll)가 `README.md`, `docs/`, `tools/`, `content/`, 테스트 스크립트를 공개하지 않게 한다 |
| `pages.css` | 검색 페이지 전용 스타일(`styles.css`, `guide.css`와 함께 로드) |

URL 규칙: 새 페이지는 `slug/index.html`로 두고 정본은 `https://astera.run/slug/`(끝 슬래시)다. 한국어는 `/ko/slug/`. 기존 `/`, `/guide.html`, `/index.ko.html`, `/guide.ko.html`과 가이드 앵커는 바꾸지 않는다.

목록 페이지: `kind`가 `hub`인 항목(`/features/`, `/alternatives/`와 한국어판)은 같은 언어에서 자기 경로 아래에 있는 공개 페이지를 레지스트리 순서대로 자동으로 나열한다. 그 아래 페이지의 브레드크럼과 `BreadcrumbList`는 목록 페이지로 연결되고, 푸터는 각 묶음 끝에 목록 페이지를 `footerLabel`로 단다. 목록 페이지 본문 파일에는 목록 밖의 안내만 쓴다. `/guides/` 목록은 실전 가이드가 더 생길 때 만든다(지금은 1개뿐이라 빈약한 페이지가 된다).

## 2. 페이지 추가·수정

1. 근거를 먼저 모은다. Astera 기능은 최신 릴리스의 README·`docs/`·앱 문구와 가이드로, 외부 제품·정책은 공식 페이지로만 확인한다.
2. `content/en/<id>.html`에 본문을 쓴다. 기존 페이지 본문의 클래스(`guide-section`, `setup-steps`, `faq-list`, `page-table-wrap` 등)를 그대로 쓴다. 내부 링크는 `/`로 시작하는 루트 경로로 쓴다.
3. `content/pages.json`에 항목을 추가한다. `evidence`에 주장별 근거 URL과 확인일을, `lastVerified`·`verifiedVersion`에 실제로 확인한 날짜와 버전을 적는다. 본문을 실질적으로 바꿨을 때만 `lastContentModified`를 바꾼다(sitemap `lastmod`가 이 값을 쓴다).
4. 한국어 페이지는 같은 `translationGroup`으로 `locale: "ko"` 항목과 `content/ko/<id>.html`을 추가한다. 영어 본문과 태그 구조를 같게 유지하고, humanize-korean으로 다듬는다. 검수가 끝나기 전에는 `status`를 `draft`로 두면 hreflang과 sitemap에서 빠진다.
5. 아래 명령을 실행한다.

```powershell
python tools/build_pages.py
python tools/build_locales.py
python tools/validate_seo.py
python tools/build_pages.py --check
python tools/build_locales.py --check
python -m unittest discover -s design -p "test_search.py"
node design/downloads.test.cjs
```

6. `python -m http.server 5173 --bind 127.0.0.1`로 띄워 320·390·768·1440px, 다크·라이트, JS 끔 상태를 확인한다.

## 3. 비교 페이지 재검증

- 주기: 30~60일. 다음 검토 예정일은 **2027-01-24**(Orca·Paseo·Paradev, 2026-11-25 확인). **Conductor는 2026-12-25**로 앞당긴다. 2026-11-04 변경 내역은 Meta에 합류한다고 했다가 11-13에 서비스를 종료하지 않는다고 밝혔고, 사이트 푸터는 “Conductor from Meta”, 약관은 Melty Labs, Inc.로 서로 다르다. 클라우드 작업 공간의 존속 여부도 공식 페이지에 명확히 나오지 않는다. 페이지는 두 공지를 날짜와 함께 적고 현재 상태는 Conductor 사이트에서 확인하라고 안내한다.
- Superset은 2026-10-26에 Paradev로 이름을 바꿨다(superset.sh → paradev.com 308, GitHub `superset-sh/superset` → `ParadevAI/Paradev`). 지시서의 `/alternatives/superset` 대신 `/alternatives/paradev/`로 발행하고 제목·H1·본문에 “formerly Superset”과 Apache Superset과의 구분을 적었다. Paradev 저장소 README에는 Conductor가 신규 사용자를 받지 않는다는 문장이 있지만 Conductor 공식 페이지에서는 확인되지 않아 쓰지 않았다.
- 경쟁 제품의 플랫폼·가격·주요 기능이 바뀌거나 새 릴리스가 크게 나오면 바로 확인한다.
- 각 행은 공식 출처로만 판정한다. 찾지 못한 기능은 “Not documented”로 두고 “Not supported”는 명시적 근거가 있을 때만 쓴다.
- 확인을 마치면 표 캡션의 날짜·버전, 출처 목록, 레지스트리의 `lastVerified`·`evidence.checkedAt`을 함께 바꾼다.
- 별점, 사용자 수, Star 수, 근거 없는 성능 비교는 쓰지 않는다.

사용량 한도 가이드도 같은 주기로 Anthropic·OpenAI 공식 페이지를 다시 확인한다. 2026-11-25 기준 Anthropic 도움말은 사용량 확인 명령으로 `/status`를, Claude Code 문서는 `/usage`를 안내하고 있어 페이지는 `/usage`를 쓴다.

## 4. 배포와 롤백

- 이 저장소는 GitHub Pages가 `main` 브랜치 루트를 그대로 배포한다. **`main`에 push하면 곧바로 운영에 반영된다.** 작업은 브랜치에서 하고, 위 검사를 통과한 뒤 소유자가 병합·push한다.
- 롤백: 문제 커밋을 `git revert`한 뒤 `main`에 push한다. 캐시는 `max-age=600`이라 최대 10분 걸린다.
- 배포 후 확인(운영):

```bash
curl -sS -D - -o /dev/null https://astera.run/
curl -sS -D - -o /dev/null https://astera.run/claude-code/
curl -sS -D - -o /dev/null https://astera.run/claude-code          # 301 → /claude-code/ 기대
curl -sS -D - -o /dev/null https://astera.run/ko/claude-code/
curl -sS -D - -o /dev/null https://astera.run/features/
curl -sS -D - -o /dev/null https://astera.run/alternatives            # 301 → /alternatives/ 기대
curl -sS -D - -o /dev/null https://astera.run/ko/alternatives/paradev/
curl -sS -D - https://astera.run/robots.txt
curl -sS -D - https://astera.run/sitemap.xml
curl -sS -D - -o /dev/null https://astera.run/nonexistent-seo-smoke-test   # 404, 사이트 404 페이지 기대
curl -sS -o /dev/null -w "%{http_code}\n" https://astera.run/docs/product-positioning.html   # 404 기대
```

GitHub Pages 제약: `_redirects`·`_headers`를 지원하지 않는다. 임의 별칭의 301과 응답 헤더(`X-Robots-Tag`, CSP, HSTS)는 만들 수 없으므로 별칭 URL을 만들지 않는다.

## 5. 소유자 계정이 필요한 작업

아래는 이 저장소 작업으로 할 수 없고 소유자 계정이 필요하다.

1. **Google Search Console**: `astera.run` 도메인 속성이 있는지 먼저 확인한다. 없으면 도메인 속성을 추가하고 DNS TXT 레코드로 소유권을 확인한다. Sitemaps에 `https://astera.run/sitemap.xml`을 제출하고, 처리된 URL 수(Phase 4 1차 포함 시 36개)를 기록한다. URL 검사로 `/claude-code/`, `/codex/`, `/features/`와 그 아래 기능 페이지 7개, `/guides/claude-code-usage-limit/`, `/alternatives/`와 그 아래 비교 페이지 4개의 크롤링, 렌더링, Google이 고른 canonical을 확인하고 색인 생성을 요청한다.
2. **Bing Webmaster Tools**: Search Console에서 가져오기로 등록하고 같은 sitemap을 제출한다.
3. **네이버 서치어드바이저**(선택): 한국어 페이지 유입을 보려면 사이트를 등록한다. HTML 확인 파일이나 메타 태그가 필요하면 그 파일을 이 저장소에 추가하는 작업을 요청한다.
4. **분석**: 사이트에는 분석 스크립트가 없다. 추가할지는 소유자가 정한다. 추가한다면 개인 정보(프롬프트, 경로, 이메일, 계정 ID, 쿼리 문자열)를 이벤트에 넣지 않는다.

## 6. 모니터링

| 주기 | 볼 것 |
|---|---|
| 배포 후 1~2주 | 색인된 URL 수, 색인 제외 사유, 크롤링 오류, 선택된 canonical |
| 매월 | 페이지별 노출·클릭·CTR·검색어(비브랜드 검색어 비중), Core Web Vitals(필드 데이터가 생기면), GitHub Releases 다운로드 누적 |
| 30~60일 | 비교 페이지와 사용량 한도 가이드 재검증 |

다운로드 클릭과 `download_count`는 설치 성공이나 사용자 수가 아니다. 트래픽이 적을 때는 증가율보다 절대 수치와 실제 검색어를 본다.

## 7. Phase 진행 상황

| Phase | 상태 | 커밋 | 비고 |
|---|---|---|---|
| 0 감사 | 완료 | `9872bea` | [phase-0-audit.md](phase-0-audit.md) |
| 1 공통 기반 | 완료 | `41f0e9a` | 생성기, 검증기, `_config.yml`, 404, 기존 페이지 메타 보강 |
| 2 영어 P0 8개 | 완료 | `f1d96b5` | 홈·가이드 푸터 링크, 가이드의 Smart Resume 설정 경로 수정 |
| 3 한국어 P0 8개 | 완료 | `1b123f0` | `/ko/...`, hreflang 상호 참조, humanize-korean 윤문 |
| 4 P1 확장 (1차) | 완료 | `64c43d9`(영어), `ca37cb5`(한국어) | 기능 4개(헤드리스 CLI, MCP, Remote Runtime, 감사 기록과 Sandbox), 비교 2개(Conductor, Paradev), 목록 페이지 2개(`/features/`, `/alternatives/`) |
| 4 P1 확장 (2차) | 대기 | — | 계정 전환 기능 페이지(문구 수위 결정 필요), 실전 가이드 5개(실제 재현 환경 필요), `/guides/` 목록 |
| 5 배포·검색 등록 | Google·Bing 완료, 네이버 미정 | `66c919e`, `d014442` | 2026-11-25 `main`에 fast-forward 병합·push, Search Console·Bing 제출(아래 10절). 네이버 서치어드바이저는 선택 |
| 6 성과 기반 개선 | 데이터 대기 | — | Search Console 데이터가 쌓인 뒤 |

## 8. Phase 1~3 검증 기록 (2026-11-25)

- 실행한 검사: `validate_seo.py` 통과(22페이지, 공개 대상 20, 내부 링크·앵커 1,499개), 검증기 자체 변이 시험 14종 모두 검출, `build_pages.py --check`, `build_locales.py --check`, 검색 테스트 7개, 다운로드 라우팅 테스트, JS 문법, 공백 검사, 새 페이지의 외부 링크 28개 응답 200.
- 브라우저(Playwright Chromium, 로컬 서버): 모든 페이지를 320·390·768·1440px × 다크·라이트로 열어 콘솔 오류·깨진 이미지·가로 넘침 없음. JS를 끈 상태에서도 새 페이지의 본문, H1, 다운로드 링크가 보임. 300px에서는 헤더가 20px 넘치는데, 기존 홈·가이드도 같은 값이다(변경 전부터 있던 한계).
- 기존 디자인 리뷰: 상호작용·가이드 목차 검사 통과. 언어 검사 38개 중 1개 실패(“guide.html: all marked copy has a Korean translation”). 2026-11-02 커밋 `b3c7eae`부터 가이드 목차의 MCP & Skills, Security & Access, Sandbox, Findings가 한국어에서도 영어 이름을 쓰기 때문이며 이번 작업과 무관하다. 검사 기준을 바꿀지, 번역할지는 소유자 판단이다.
- 한국어 윤문: humanize-korean light 경로 3묶음, 구조 게이트 통과(변경률 0.2%·0.4%·0.2%). 쉼표를 지우면서 길어진 문장 3개는 직접 나눴고, 게이트가 서법 변화를 잡은 문장 1개는 원문으로 되돌렸다. 영어·한국어 본문의 태그 순서와 링크 대응을 비교해 8쌍 모두 일치했다.
- 성능: 변경 전 운영 기준선은 [phase-0-audit.md](phase-0-audit.md) 7절. 새 페이지는 운영 배포 후 같은 방법(모바일 감속 랩 측정)으로 재야 한다. 로컬 서버 수치는 비교 대상이 아니라 기록하지 않았다. 배포 후 측정은 10절.
- 소유자 확인이 필요한 문구: 새 페이지 푸터와 제공사 페이지의 “Anthropic·OpenAI가 만들거나 제휴한 제품이 아닌 독립 오픈소스 프로젝트” 문장(지시서의 제휴 없음 명시 요구에 따라 넣음).

## 9. Phase 4 1차 검증 기록 (2026-11-25)

- 범위: 기능 페이지 4개(`/features/headless-cli/`, `/features/mcp/`, `/features/remote-runtime/`, `/features/agent-security/`), 비교 페이지 2개(`/alternatives/conductor/`, `/alternatives/paradev/`), 목록 페이지 2개(`/features/`, `/alternatives/`)와 각각의 한국어판. 공개 대상은 36개가 됐다.
- 중복 의도 검사: 새 기능 페이지는 기존 페이지와 검색 의도가 겹치지 않는다. 에이전트 오케스트레이션 페이지는 Job 흐름을, 헤드리스 CLI 페이지는 셸·스크립트·종료 코드를 다룬다. Codex 페이지의 MCP와 Sandbox 소단락은 요약으로 두고 자세한 내용은 새 페이지가 맡는다. Remote Runtime 기능 페이지의 설정 절차는 4단계로 줄였다. 문제 해결까지 다루는 단계별 절차는 실전 가이드 `/guides/remote-coding-agent-setup`(2차)에서 다룬다. 계정 전환 기능 페이지는 사용량 한도 가이드와 목적이 겹치고 문구 결정이 필요해서 2차로 미뤘다.
- 근거: Astera 기능은 v1.5.5 가이드와 `docs/remote-runtime.md`, `docs/cli.md`, `docs/mcp.md`(릴리스 태그 기준)로 확인했다. 페이지의 `astera` 명령과 옵션은 설치된 1.5.4의 `--help`로 이름이 있는지만 확인했고, Job을 만들거나 계정을 쓰는 명령은 실행하지 않았다. 비교 페이지는 각 제품의 공식 사이트·문서·변경 내역·저장소만 썼다. 핵심 사실(Paradev 라이선스·릴리스·리디렉션, Conductor 플랫폼·로컬 세션 종료·0.99.0)은 직접 다시 확인했다.
- 이미지: 헤드리스 CLI 페이지에만 기존 Jobs 데모 캡처를 다시 썼다. MCP, Remote Runtime, 보안 화면은 저장소에 실제 캡처가 없어 넣지 않았다. 지시서 4.1의 “실제 제품 캡처 1개 이상”을 채우려면 소유자가 해당 설정 화면을 캡처해야 한다.
- 실행한 검사: `validate_seo.py` 통과(38페이지, 공개 대상 36, 내부 링크·앵커 2,723개), `build_pages.py --check`, `build_locales.py --check`, 검색 테스트 7개, 다운로드 라우팅 테스트, JS 문법, 공백 검사. 새 페이지의 외부 링크 30개가 모두 200으로 응답했고, 한국어 페이지의 외부 링크도 같은 30개 안에 든다.
- 브라우저(Playwright Chromium, 로컬 서버): sitemap의 모든 페이지와 404를 320·390·768·1440px로, 한국어 새 페이지는 라이트 테마로도 열었다(188회). 콘솔 오류, 가로 넘침, 설정 단계 번호와 제목이 겹치는 경우가 없었다. JS를 끈 상태에서도 새 페이지 16개 모두 H1, 본문, 목록 링크, 다운로드 링크가 보인다. 언어 링크, 브레드크럼, hreflang, 푸터가 각 언어의 페이지로 연결된다.
- 함께 고친 것: Phase 2에서 넣은 `pages.css`의 본문 목록 규칙이 설정 단계(`.setup-steps`)의 여백을 덮어써서, 단계 번호가 제목 앞부분을 가렸다(Claude Code·Codex·GitHub 페이지, 모든 폭). 목록 규칙에서 `.setup-steps`를 빼서 가이드와 같은 모양으로 되돌렸다.
- 한국어 윤문: humanize-korean light 경로 3묶음, 구조 게이트 통과(변경률 0.4%·0.6%·0.5%). 같은 표현 두 곳(“사용량 한도에서 …”)과 제목 하나는 손으로 맞췄다. 영어·한국어 본문의 태그 순서와 링크 대응을 18쌍 모두 비교해 일치했다.
- 남은 일: 계정 전환 기능 페이지(문구 수위 결정), 실전 가이드 5개(테스트 저장소와 계정 사용량을 쓰는 실제 재현), `/guides/` 목록, 새 기능 페이지의 실제 화면 캡처, Conductor 재확인(2026-12-25).

## 10. 운영 배포 기록 (2026-11-25)

- 배포: `seo-expansion`을 `main`에 fast-forward 병합해 push했다(`b3c7eae..66c919e`, 9커밋, Phase 0~4 1차와 1.5.1~1.5.5 가이드). GitHub Pages 빌드는 2026-11-25 00:25 UTC에 `built`로 끝났다. 되돌릴 때 기준점은 `b3c7eae`다. 배포 전 2절 검사를 다시 돌려 모두 통과했다.
- 운영 확인(4절 명령과 같은 내용): sitemap URL 36개가 모두 200이고, 각 페이지의 canonical이 자기 URL과 같다. `/claude-code`, `/features`, `/alternatives`, `/ko/features`, `/guides/claude-code-usage-limit`은 끝에 `/`를 붙인 주소로 301. 없는 주소, `/docs/…`, `/content/pages.json`, `/tools/…`, `/README.md`는 404이고 사이트 404 페이지가 나온다. robots.txt가 sitemap을 가리킨다. 배포된 `pages.css?v=20261125-5`, `locales/ko.js?v=20261125-3`.
- 운영 브라우저 확인(Playwright Chromium): 홈·가이드(영어·한국어)와 새 페이지 7개를 390·1440px로 열어 콘솔 오류와 가로 넘침이 없다. 홈 푸터는 브라우저 언어가 영어면 영어 페이지로, 한국어면 `/ko/` 페이지로 연결된다. 사이트 스크립트가 내부 링크에 `?lang=…&theme=…`를 붙이는 동작은 2026-09부터 있던 것이고 canonical이 원래 주소를 가리킨다.
- 성능(운영, Phase 0 감사 7절과 같은 랩 조건, 모바일은 3회 중앙값):

| 페이지 | 모바일 LCP | 기준선(변경 전) | CLS | 요청 | 전송량 | LCP 요소 |
|---|---|---|---|---|---|---|
| `/` | 1,424 ms | 1,636 ms | 0 | 15 | 677 KB | `div.space-stars` |
| `/index.ko.html` | 1,672 ms | 1,992 ms | 0 | 15 | 678 KB | `div.space-stars` |
| `/guide.html` | 1,064 ms | 1,288 ms | 0(아래 참고) | 13 | 206 KB | `a` |
| `/guide.ko.html` | 1,768 ms | 1,744 ms | 0 | 13 | 210 KB | `a` |
| `/claude-code/` | 3,328 ms | — | 0 | 13 | 558 KB | `img`(hero.jpg) |
| `/features/` | 892 ms | — | 0 | 12 | 134 KB | `h1` |
| `/features/mcp/` | 1,272 ms | — | 0 | 12 | 136 KB | `h1` |
| `/ko/features/headless-cli/` | 2,256 ms | — | 0 | 13 | 246 KB | `img` |
| `/alternatives/paradev/` | 1,288 ms | — | 0 | 12 | 136 KB | `p` |
| `/guides/claude-code-usage-limit/` | 1,296 ms | — | 0 | 12 | 136 KB | `h1` |

  데스크톱(1440px, 감속 없음)은 LCP 432~900 ms, CLS 0.019 이하. 랩 측정 한 번의 차이는 수백 ms까지 흔들리므로 기준선과의 차이를 개선으로 읽지 않는다.
- `/guide.html` 모바일 측정 중 한 번 CLS 0.829가 나왔다. 같은 조건(새 브라우저, 홈을 먼저 연 브라우저, 영어·한국어 언어 설정)으로 23번 더 쟀을 때는 모두 0이어서 원인을 찾지 못했다. Search Console의 Core Web Vitals에 필드 데이터가 생기면 다시 본다.
- `/claude-code/`(영어·한국어)는 첫 화면의 가장 큰 요소가 `hero.jpg`(432 KB)인데 `loading="lazy"`로 넣어서 다운로드가 늦게 시작됐다. `fetchpriority="high"`로 바꾸고 로컬에서 같은 조건으로 재니 3,808 → 3,352 ms(영어), 3,872 → 3,352 ms(한국어)였다. 이 수정은 `c76f9d3`으로 배포했다. 남은 시간 대부분이 이미지 다운로드여서, 소유자 승인을 받아 Pillow로 작은 사본 `assets/hero-640.jpg`(61 KB), `hero-960.jpg`(124 KB), `hero-1280.jpg`(192 KB)를 만들었다(LANCZOS 축소, JPEG 품질 78, progressive). 2배 확대 비교에서 원본 축소본과 구분되지 않았다. Claude Code 페이지의 이미지에 `srcset`과 `sizes="(max-width: 880px) 90vw, 820px"`를 달았다. 브라우저는 390px 3배 화면에서 1280, 390px 2배와 1440px 1배에서 960, 320px 2배에서 640, 768px 2배와 1440px 2배에서 원본을 고른다. 로컬 모바일 랩에서 LCP 3,352 → 2,196 ms(영어), 3,352 → 2,208 ms(한국어), 전송량 558 → 388 KB였다. 홈과 가이드의 같은 이미지는 스크립트가 원본 주소로 바꿔 끼우고, 첫 화면의 가장 큰 요소도 이미지가 아니라서 그대로 두었다. Codex·오케스트레이션·헤드리스 CLI 페이지는 첫 화면의 가장 큰 요소가 글이라 그대로 두었다. 운영 배포(`d014442`) 후 같은 조건에서 LCP 2,024 ms(영어), 2,052 ms(한국어), 전송량 328 KB였다.
- 검색 등록(2026-11-25, 소유자가 로그인한 브라우저에서 진행):
  - Google Search Console: 도메인 속성 `sc-domain:astera.run`은 이미 있었다(DNS TXT `google-site-verification` 확인). 2026-09-23에 제출한 `https://astera.run/sitemap.xml`은 11-19에 마지막으로 읽혀 발견 페이지가 4개였다. 다시 제출하자 바로 읽혀 상태 성공, 발견 페이지 36개가 됐다. URL 검사 결과 `guide.html`만 색인돼 있었고, 나머지는 “발견됨 - 현재 색인이 생성되지 않음” 또는 “Google에 아직 알려지지 않은 URL”이었다. 색인 생성 요청 10건(하루 한도)을 보냈다: `/claude-code/`, `/codex/`, `/guides/claude-code-usage-limit/`, `/features/`, `/features/agent-orchestration/`, `/alternatives/`, `/ko/claude-code/`, `/features/smart-resume/`, `/alternatives/conductor/`, `/guide.html`. 나머지는 sitemap으로 처리되기를 기다리고, 1~2주 뒤 색인 수를 보고 남은 주요 페이지(헤드리스 CLI, MCP, Remote Runtime, 보안, GitHub, 비교 페이지, 한국어판)를 요청한다.
  - Bing Webmaster Tools: 사이트 `https://astera.run/`는 이미 있었고 sitemap은 없었다. sitemap을 제출했고(처리 중), URL 제출 도구(하루 100개)로 sitemap의 36개 URL을 모두 제출해 성공했다.
  - 네이버 서치어드바이저: 아직 하지 않았다. 사이트 소유 확인 파일이나 메타 태그를 배포해야 한다.
- 본문 폭(`dbebdfb`): 새 페이지의 본문이 820 px, 문단이 68ch로 묶여 넓은 화면의 오른쪽이 비어 있었다. 소유자 요청으로 본문·소개 문장·문단·목록이 헤더와 푸터 구분선 폭(최대 1160 px)까지 차게 했다. 운영에서 32페이지 × 1440·390 px로 본문과 글의 오른쪽 끝이 구분선 끝과 같고 가로 넘침이 없음을 확인했다.
- 이미지 비율: Phase 2부터 본문 그림이 HTML의 `height` 값(예: 1248 px)으로 고정돼, 폭이 줄어든 만큼 세로로 늘어나 보였다(1440 px의 Claude Code 이미지가 1160×1248, 390 px에서 335×1248). `.page-article figure img`에 `height: auto`를 넣어 고쳤다. 생성 페이지 32개의 그림 8개를 1440·1024·390·320 px에서 재서 표시 비율이 파일 비율과 0.01 안에서 같음을 확인했다. 그동안의 브라우저 검사는 깨진 이미지와 가로 넘침만 봤고 비율은 보지 않아 놓쳤다. 이제 그림이 있는 페이지는 표시 비율도 확인한다.
