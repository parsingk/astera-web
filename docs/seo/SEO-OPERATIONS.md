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

- 주기: 30~60일. 다음 검토 예정일은 **2027-01-24**(Orca·Paseo, 2026-11-25 확인).
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
curl -sS -D - https://astera.run/robots.txt
curl -sS -D - https://astera.run/sitemap.xml
curl -sS -D - -o /dev/null https://astera.run/nonexistent-seo-smoke-test   # 404, 사이트 404 페이지 기대
curl -sS -o /dev/null -w "%{http_code}\n" https://astera.run/docs/product-positioning.html   # 404 기대
```

GitHub Pages 제약: `_redirects`·`_headers`를 지원하지 않는다. 임의 별칭의 301과 응답 헤더(`X-Robots-Tag`, CSP, HSTS)는 만들 수 없으므로 별칭 URL을 만들지 않는다.

## 5. 소유자 계정이 필요한 작업

아래는 이 저장소 작업으로 할 수 없고 소유자 계정이 필요하다.

1. **Google Search Console**: `astera.run` 도메인 속성이 있는지 먼저 확인한다. 없으면 도메인 속성을 추가하고 DNS TXT 레코드로 소유권을 확인한다. Sitemaps에 `https://astera.run/sitemap.xml`을 제출하고, 처리된 URL 수(배포 시점 20개)를 기록한다. URL 검사로 `/claude-code/`, `/codex/`, `/features/agent-orchestration/`, `/features/smart-resume/`, `/features/github-ci/`, `/guides/claude-code-usage-limit/`, `/alternatives/orca/`, `/alternatives/paseo/`의 크롤링, 렌더링, Google이 고른 canonical을 확인하고 색인 생성을 요청한다.
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
| 4 P1 확장 | 시작 안 함 | — | 계정 전환·원격·MCP·CLI·보안 기능 페이지, 실전 가이드 4개, Conductor·Superset 비교 |
| 5 배포·검색 등록 | 소유자 작업 대기 | — | 병합·push, 위 5절 |
| 6 성과 기반 개선 | 데이터 대기 | — | Search Console 데이터가 쌓인 뒤 |

## 8. Phase 1~3 검증 기록 (2026-11-25)

- 실행한 검사: `validate_seo.py` 통과(22페이지, 공개 대상 20, 내부 링크·앵커 1,499개), 검증기 자체 변이 시험 14종 모두 검출, `build_pages.py --check`, `build_locales.py --check`, 검색 테스트 7개, 다운로드 라우팅 테스트, JS 문법, 공백 검사, 새 페이지의 외부 링크 28개 응답 200.
- 브라우저(Playwright Chromium, 로컬 서버): 모든 페이지를 320·390·768·1440px × 다크·라이트로 열어 콘솔 오류·깨진 이미지·가로 넘침 없음. JS를 끈 상태에서도 새 페이지의 본문, H1, 다운로드 링크가 보임. 300px에서는 헤더가 20px 넘치는데, 기존 홈·가이드도 같은 값이다(변경 전부터 있던 한계).
- 기존 디자인 리뷰: 상호작용·가이드 목차 검사 통과. 언어 검사 38개 중 1개 실패(“guide.html: all marked copy has a Korean translation”). 2026-11-02 커밋 `b3c7eae`부터 가이드 목차의 MCP & Skills, Security & Access, Sandbox, Findings가 한국어에서도 영어 이름을 쓰기 때문이며 이번 작업과 무관하다. 검사 기준을 바꿀지, 번역할지는 소유자 판단이다.
- 한국어 윤문: humanize-korean light 경로 3묶음, 구조 게이트 통과(변경률 0.2%·0.4%·0.2%). 쉼표를 지우면서 길어진 문장 3개는 직접 나눴고, 게이트가 서법 변화를 잡은 문장 1개는 원문으로 되돌렸다. 영어·한국어 본문의 태그 순서와 링크 대응을 비교해 8쌍 모두 일치했다.
- 성능: 변경 전 운영 기준선은 [phase-0-audit.md](phase-0-audit.md) 7절. 새 페이지는 운영 배포 후 같은 방법(모바일 감속 랩 측정)으로 재야 한다. 로컬 서버 수치는 비교 대상이 아니라 기록하지 않았다.
- 소유자 확인이 필요한 문구: 새 페이지 푸터와 제공사 페이지의 “Anthropic·OpenAI가 만들거나 제휴한 제품이 아닌 독립 오픈소스 프로젝트” 문장(지시서의 제휴 없음 명시 요구에 따라 넣음).
