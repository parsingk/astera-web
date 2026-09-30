# Astera 기능 강조 근거

최초 조사·반영일: 2026-09-22. 당시 로컬 앱 `D:\parsingk\astera`의 코드와 문서, 공식 제품 소개를 대조했다. 당시 로컬 앱 버전은 1.3.25였다. 아래 기록은 날짜별 구현을 설명하며, 최신 공개 릴리스에 모든 변경이 들어 있다고 보증하지 않는다.

## 2026-09-30: 최신 develop CLI 설치·사용법 대조

`git fetch origin develop` 후 로컬 `develop`과 `origin/develop`이 모두 `fd48e939f0001fbcdde9bbdddc563d2a46f05a18`임을 확인했다. 기존 Headless CLI 소개와 사용 흐름을 이 커밋의 [README](https://github.com/parsingk/Astera/blob/fd48e939f0001fbcdde9bbdddc563d2a46f05a18/README.md), [CLI 문서](https://github.com/parsingk/Astera/blob/fd48e939f0001fbcdde9bbdddc563d2a46f05a18/docs/cli.md), 소스에 맞췄다. 아래 9월 27일의 설치 메뉴와 9월 22일의 Host 범위는 당시 기록이며, 현재 안내는 이 절을 기준으로 한다.

- **설치 메뉴와 PATH:** `src/renderer/src/App.tsx`의 CLI 탭과 `components/CliSettings.tsx`를 확인했다. 메인과 Guide에 **Settings → CLI**를 안내한다. Windows는 기본으로 켜진 사용자 PATH 체크박스로 설치 폴더를 등록하고 새 터미널부터 사용할 수 있다. macOS·Linux는 필요한 경우 패널의 PATH 명령을 실행한다. 한국어 버튼명은 `src/core/i18n/messages/ko.ts`와 맞췄다.
- **세션과 사람의 응답:** `cliUsage.ts` 및 `command.ts`의 `sessions-create`, `sessions-send`, `chats-answer`, `questions-answer`를 대조했다. 세션 목록, 화면을 읽은 뒤 추가 입력하는 순서, Chat 생성과 권한 요청 처리, Job 질문의 상세 조회를 보강했다. Chat 질문은 앱에서 답하며, 일반 셸의 사용자만 CLI로 Chat 권한 요청에 답할 수 있다.
- **스킬과 실행:** `skills list`·`skills install`은 앱과 Host 없이 계정의 스킬 상태를 확인·설치할 수 있다. 설치 후 새 세션이 필요하다. Job/Run/Session ID는 각각의 생성·실행 응답에서 가져오도록 명시했다. `jobs run`이 Run을 반환하는 처리와 `runs follow`·`runs checks`·`runs wait` 옵션도 대조했다.
- **Host 호환성과 오류:** `src/cli/host.ts`의 `siblingHostError`와 명령 정의를 확인했다. 구형 Host 교체는 `host start --replace` 또는 업데이트한 앱을 여는 방법으로 설명하고, 해당 Host의 세션이 종료됨을 함께 알린다. 종료 코드 3/6/9와 JSON 오류 필드, 변경 명령의 응답 유실 시 재시도 전 상태 확인을 추가했다. 실제 Host 교체나 에이전트 실행은 수행하지 않았다.
- **실행 범위:** `src/host/features.ts`, `src/host/index.ts`, CLI 문서에서 워커·워크트리·검사·리뷰·계정 전환과 Slack 인계 조건을 재확인했다. 컴퓨터가 깨어 있어야 하며 미래 예약만으로 Host가 유지되지 않는 조건도 유지한다.

검증:

- 수정 전후 검색 검사 7개, 다운로드 8개 시나리오와 버튼 5개 검사가 통과했다. 잘못된 설치 메뉴를 확인하는 검사는 수정 전에 실패하고 수정 후 통과했다.
- 네 공개 페이지의 번역 키, 중복 ID, 로컬 앵커 검사 통과. Guide의 영문·한국어 명령 블록 일치와 예제 29개의 명령·옵션 정의 대조를 통과했다. `build_locales.py --check`, 번역 JavaScript 문법 검사와 `git diff --check`도 통과했다.
- Astera Agent browser에서 언어 검사 38개 통과. 메인/Guide × 한·영 × 다크·라이트 × 1440/320px의 16가지 배치를 확인했다. 문서 전체 가로 넘침, 깨진 이미지·앵커, 최종 배치 검사 콘솔·네트워크 오류 없음. Guide 검사기의 `code` 넘침 표시는 `overflow-x: auto`인 명령 블록 내부이며 페이지 폭을 늘리지 않는다.
- 한국어 정적 Guide의 Headless CLI 목차 이동과 화면 캡처를 확인했다. 첫 로드·언어 전환 검사에서 각각 폰트 `ERR_CACHE_MISS`, 이미지 `ERR_FAILED`가 일시 기록됐고, 이후 배치 검사에서는 두 자원 모두 정상 로드됐다. 실제 CLI 세션·Job 실행 검증은 이 문서 작업 범위에 포함하지 않았다.

## 2026-09-27: develop Headless CLI 추가

로컬 `develop`의 CLI 소스와 도움말, Host 구성, 실제 orchestration 명령 처리를 직접 확인했다. 확인 기준 커밋은 `c308069c6f6618801c93dfdc7f2a7eaf30c7ac57`이며, 공개 릴리스에 포함됐다는 뜻은 아니다. 아래의 2026-09-22 조사 기록은 이전 빌드의 동작을 설명하기 위해 보존한다. 특히 기존 Host 항목의 앱 실행 필요 조건은 이 CLI 지원 빌드에는 그대로 적용되지 않는다.

- **사용 가치:** 앱 창 없이 터미널에서 에이전트와 Jobs를 시작하고, 검사·질문·결과를 추적한다. 앱을 다시 열면 같은 세션과 Jobs 그래프를 확인한다. 메인 `#headless-cli`와 Guide `#headless-cli`에 영·한으로 반영했다.
- **설치:** Settings → Agents의 Command line tool에서 설치하는 `astera` 명령이다. 설치된 앱을 Node 모드로 실행하는 진입점이며 별도 npm 패키지가 아니다. Windows는 `%LOCALAPPDATA%\astera\bin`, macOS/Linux는 `~/.local/bin`; 필요한 PATH 설정은 패널 안내를 따른다.
- **Host의 실행 범위:** `spawn`, `worktrees`, `dispatch`, `rolling` 기능을 제공하는 Host는 앱 종료 후에도 워커 실행, 워크트리, 코디네이터 없는 Job의 자동 배분·검사·리뷰·제한된 수정 재시도, 계정 전환을 처리한다. Slack도 지원 Host가 인계할 수 있다. `host status`로 실제 기능을 확인하도록 안내한다.
- **작업 흐름:** `/astera-orchestration` 계획을 기본으로 소개하고, `jobs list` → `jobs run` → 반환된 실행 ID로 `runs follow`/`runs checks`를 설명한다. 직접 `jobs create`와 `tasks add`로 계획하는 방법은 접힌 부가 안내로 둔다. Job ID와 Run ID를 구분한다.
- **자동화 계약:** JSON 기본 출력, `--human`, `--quiet`, `runs follow`의 NDJSON, `runs wait`의 종료 코드 0/7/8/10을 설명한다. 대기 시간 초과나 조회 중단은 Job 취소가 아니다. 계정·앱·프로젝트가 준비된 로컬 CI 실행 환경만을 예로 들고, 설치 없는 원격 실행이나 클라우드 호스팅을 약속하지 않는다.
- **유지 조건:** 컴퓨터가 깨어 있고 Host가 살아 있어야 한다. 클라이언트와 활성 작업이 없는 Host는 약 1분 후 종료한다. 미래 예약만으로 Host가 유지되지 않으므로 예약 시작에는 앱을 켜 두도록 안내한다. 이전 빌드의 앱 실행 필요 조건도 버전을 한정해 유지했다.
- **관련 설정:** develop은 orchestration 스킬을 항상 제공한다. 이전 빌드의 설정 토글 안내에는 버전 조건을 붙였다. 다른 선택 기능의 설정은 변경하지 않았다.

확인한 소스:

- 앱 `src/cli/index.ts`, `src/cli/run.ts`, `src/cli/host.ts`: CLI 진입, 출력 형식, Host 시작·상태·종료.
- 앱 `src/core/orchestration/cliUsage.ts`, `src/core/orchestration/command.ts`: 지원 명령·옵션과 실제 세션/Job/작업/질문/대기 처리.
- 앱 `src/host/index.ts`: `composeHostDriving`, `composeHostRolling`, `composeHostSlack` 구성과 기능 제공 조건.
- 앱 `docs/cli.md`: 설치 경로, 버전 호환성, 예제, Host 수명, 종료 코드 및 사용 제약. 공개 참조: [develop CLI 문서](https://github.com/parsingk/Astera/blob/develop/docs/cli.md).

검증: 기존 검색 검사 7개, 다운로드 8개 시나리오와 버튼 5개 검사, 한국어 정적 페이지 일치 검사, 번역 파일 문법 검사, 네 공개 페이지의 CLI 번역 키·ID·앵커·명령 블록 검사를 통과했다. 실제 CLI 작업은 실행하지 않고 명령 정의와 처리 소스를 대조했다. 이번 세션에서 연결 가능한 브라우저가 없어 화면 배치와 목차 클릭의 브라우저 검증은 남아 있다.

## 2026-09-22 조사: 강조할 가치

**맥락을 이어받고, 여러 에이전트의 작업 관계를 보고, 실제 검사 결과로 다음 단계에 진입하는 작업 공간.**

병렬 실행 자체보다 사용자가 긴 작업을 감독할 때 겪는 네 가지 문제를 앞에 둔다.

| 사용자의 상황 | Astera에서 보여 줄 기능 | 웹사이트 반영 |
| --- | --- | --- |
| 계정 한도 뒤에도 무엇을 하던 중인지 이어받아야 한다 | Smart Resume의 체크포인트와 계정 자동 전환 | 메인 첫 기능, Guide `#smart-resume` |
| 어느 작업이 무엇을 기다리는지 알고 싶다 | Jobs 의존 관계 그래프, 작업 상태, 질문, 검증과 타임라인 | 메인 협업 카드와 실제 Jobs GIF, Guide `#jobs` |
| 작업 분배와 보고 취합을 에이전트에게 맡기고 싶다 | `/astera-orchestration` 스킬, Claude·Codex 코디네이터/워커 흐름 | 메인 Workflow의 요청 예시, Guide `#orchestration` |
| 앱을 다시 열 때 실행 중인 세션에 돌아오고 싶다 | 별도 로컬 Host가 소유하는 프로세스와 재연결 | 메인 Host 섹션, Guide `#host` |

How It Works는 끝난 작업의 요청·변경·이유를 읽는 후속 단계로 유지한다. 선택 기능의 목차와 본문은 사용자 요청대로 ‘Astera로 작업하기’ 그룹으로 이동했다. 기존 `#optional` 링크는 유지한다.

## 다른 제품의 공식 자료

- Orca는 병렬 CLI 에이전트, 독립 워크트리, 터미널·브라우저·CLI 통합을 소개한다. 계정 사용량 확인과 Codex 계정 전환도 공개한다. 따라서 ‘여러 에이전트를 한곳에서 실행’, ‘워크트리’, ‘계정 관리’만으로 독점적인 차별점이라고 표현하지 않는다. [Orca 공식 사이트](https://www.onorca.dev/)
- Conductor는 격리된 클라우드 실행 환경, 여러 제공자의 에이전트와 기존 구독 사용, 공동 작업 공간을 소개한다. 따라서 ‘앱 창을 벗어나 작업을 이어감’ 자체를 Astera만의 기능으로 단정하지 않는다. Astera의 설명은 **사용자의 컴퓨터에서 실행되는 Host와 앱 재연결**이라는 실제 구현 범위에 둔다. [Conductor 공식 사이트](https://www.conductor.build/)

**판단:** 개별 기능의 유일성을 주장하기보다 Astera에서 이 기능들이 어떻게 이어지는지 보여 주는 것이 적합하다. 위 자료에 기능이 적혀 있지 않다는 이유로 경쟁 제품에 그 기능이 없다고 결론 내리지 않는다. 비교 순위나 ‘유일’, ‘최초’, 성능 배수는 추가하지 않았다.

## 구현으로 확인한 내용과 문구의 한계

### Smart Resume

- 일반 세션은 최근 요청 순서, 대화 말미, 작업 폴더·git 상태, 수정 파일과 마지막 명령을 체크포인트로 전달한다. 전체 대화를 그대로 복제하는 방식과 구분한다.
- 계정 한도로 전환할 때 새 대화를 시작하고 체크포인트를 첫 메시지로 전달한다. 체크포인트를 만들지 못하면 기본 resume으로 복귀한다.
- Job 워커는 기록된 목표·작업·선행 작업·보고·결정·검증 상태를 인계 자료로 사용할 수 있다. 관측되지 않은 진행 상태를 완성된 사실처럼 주장하지 않는다.
- 기본 비활성화와 설정 위치를 안내한다. 토큰 절약률, 더 높은 정확도, 맥락의 완전한 보존은 주장하지 않는다.
- 근거: 앱 [README](https://github.com/parsingk/Astera/blob/main/README.md), `src/main/rolling.ts`의 `roll`, `src/core/orchestration/checkpoint.ts`, `src/main/orchestration/resumePacket.ts`.

### 그래프로 보는 오케스트레이션과 완료 검사

- Jobs는 의존 관계, 활성 워커, 질문, 타임라인을 제공한다. 그래프 노드는 검증·리뷰·Gate를 포함한 상태와 검사 칩을 표시하고, 작업을 선택하거나 세션으로 이동할 수 있다.
- 검사가 연결된 작업은 완료 보고만으로 완료가 되지 않는다. 검사와 필요한 리뷰를 통과해야 의존 작업이 풀린다.
- 자동 수정은 설정했을 때 실패한 검사·주요 리뷰 지적을 워커에게 돌려보내는 한도 있는 반복이다. 모든 작업의 무조건적 완료나 무한 재시도를 약속하지 않는다.
- 일반 Job은 결과를 워크트리에 두며 사용자가 병합한다. 예약 회차의 자동 정리·수동 반영 설명도 유지한다.
- 근거: 앱 `src/renderer/src/components/RunDetail.tsx`, [Job 수명 주기](https://github.com/parsingk/Astera/blob/main/docs/jobs.md), [오케스트레이션 CLI 가이드](https://github.com/parsingk/Astera/blob/main/resources/skills/orchestration-guide.md).

### `/astera-orchestration`

- 설정에서 Agent orchestration을 활성화한 후 새 세션을 시작해야 스킬이 전달된다.
- 코디네이터는 작업 생성·워커 배분·보고 수신·판단 요청을 다룬다. 해당 프로젝트의 실행은 Jobs에서 확인할 수 있다.
- 예시는 목표, 제공자별 역할, 의존 순서, 검사·리뷰와 재시도 한도를 포함한 **사용자의 요청**으로 표시한다. 실제 실행 결과나 보장된 자동 동작으로 꾸미지 않는다.
- 단순한 한 번의 작업은 일반 세션으로 충분할 수 있다. 교차 제공자 리뷰에는 상대 제공자의 사용 가능한 계정과 사용량이 필요하다.
- 근거: 앱 README의 `Run it with the astera-orchestration skill`, `resources/skills/orchestration-guide.md`의 supervision loop, review, convergence 설명.

### Host

- Host가 소유하는 Terminal·Chat 세션, 프로젝트 터미널과 Run 프로세스는 일반 앱 종료 때 유지할 수 있다. 재실행 시 지원되는 살아 있는 세션과 출력 버퍼에 다시 연결한다.
- 앱 시작 시 Host가 아직 준비되지 않았거나 사용할 수 없는 경우에는 앱 소유 프로세스가 함께 존재할 수 있다. 따라서 모든 세션이 항상 생존한다고 적지 않는다.
- 일반 종료와 ‘세션 모두 끝내고 종료’를 구분한다. 버전 업데이트 후 재연결도 호환 여부에 따라 달라진다.
- **스케줄러, 계정 자동 전환, Slack, Job 조율까지 앱 종료 후 계속되는 것으로 설명하지 않는다.** 현재 앱 종료 경로에서 관련 앱 서비스가 정지한다. 컴퓨터 종료·잠자기까지 넘어 실행하는 클라우드 서비스로도 설명하지 않는다.
- 근거: 앱 `src/main/host/ptyRouter.ts`, `src/main/host/procRouter.ts`, `src/main/host/reattach.ts`, `src/main/index.ts`의 tray와 `will-quit`, `src/core/i18n/messages/en.ts`의 종료·업데이트 안내.
- `docs/2026-09-22-host-control-plane-design.md`의 전체 제어 기능 이전은 설계 문서다. 그 목표 상태를 현재 제공 기능으로 광고하지 않았다.

## 표현과 구성

- 기존 우주 히어로, Public Sans, 다크·라이트 토큰과 실제 앱 미디어를 유지한다.
- Smart Resume의 인계 내용을 세 줄로 정리하고, 스킬 호출 예시와 Host 재연결 개념도를 기존 설명 옆에 배치한다. 새 의존성이나 애니메이션은 없다.
- 큰 제목과 상단 메뉴는 영어, 본문·사용법·버튼은 한국어/영어로 제공한다. GIF는 실제 계정 전환·Jobs 녹화이며 Smart Resume나 Host의 녹화로 바꾸어 표시하지 않는다.

## 이번 변경의 검증

- 브라우저 언어 검사 38개 통과. 해당 실행에서 콘솔 오류 없음.
- HTML 3개 파일의 로컬 참조·앵커·중복 ID와 JavaScript 문법 검사 통과. 번역 키 331개 중 누락·미사용 0개.
- Guide의 15개 섹션과 목차 순서가 일치하며 `#optional`이 ‘Astera로 작업하기’ 그룹에 포함됨을 확인했다.
- `git diff --check` 통과. 새 패키지나 런타임 의존성 없음.
- 32가지 반응형 조합을 검사하던 중 브라우저 도구가 `waitFor: nothing matched #report[data-status="complete"] within 30000 ms`를 반환했다. 이 실행은 완료 결과를 내지 못했다. 도구 지침에 따라 브라우저 검사를 중단했으며, 이번 변경의 전체 반응형·상호작용 재검사와 최종 시각 캡처는 확인하지 못했다. 기존 캡처는 변경 전 시안이다.
