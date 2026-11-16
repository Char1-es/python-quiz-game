# python-quiz-game

## 프로젝트 개요

터미널에서 즐기는 Python 콘솔 퀴즈 게임입니다.
메뉴에서 번호를 골라 퀴즈를 풀고, 새 퀴즈를 추가하고, 목록과 최고 점수를 확인할 수 있습니다.
퀴즈와 최고 점수는 `state.json`에 저장되므로 프로그램을 종료했다가 다시 실행해도 유지됩니다.

- 언어: Python 3 (표준 라이브러리만 사용, 별도 설치 불필요)
- 구조: `Quiz`(개별 퀴즈) / `QuizGame`(게임 전체 관리) 두 클래스로 역할 분리

## 퀴즈 주제와 선정 이유

**주제: 일반 상식** (지리, 과학, 경제 등)

- 특별한 배경지식 없이 누구나 풀 수 있어 기능 테스트와 시연에 적합합니다.
- 질문, 선택지 4개, 정답 번호라는 구조가 단순해서 `Quiz` 클래스 설계와 JSON 저장을 연습하기 좋습니다.
- 사용자가 직접 퀴즈를 추가할 수 있어, 원하는 주제로 확장할 수 있습니다.

## 실행 방법

```bash
git clone git@github.com:Char1-es/python-quiz-game.git
cd python-quiz-game
python3 main.py
```

`state.json`은 첫 실행 시 자동으로 생성됩니다.

## 기능 목록

| 메뉴 | 기능 | 설명 |
|---|---|---|
| 1 | 퀴즈 풀기 | 저장된 퀴즈를 순서대로 출제하고 정답/오답을 알려 준 뒤 결과를 표시합니다. 최고 점수보다 높으면 갱신합니다. |
| 2 | 퀴즈 추가 | 질문, 선택지 4개, 정답 번호(1~4)를 입력받아 저장합니다. |
| 3 | 퀴즈 목록 보기 | 등록된 퀴즈의 질문과 선택지를 보여 줍니다. |
| 4 | 최고 점수 보기 | 최고 점수를 보여 줍니다. 아직 풀지 않았다면 안내 메시지를 출력합니다. |
| 0 | 종료 | 저장 후 종료합니다. |

### 입력/예외 처리

- 입력 앞뒤 공백을 제거합니다.
- 빈 입력, 숫자가 아닌 입력, 허용 범위 밖 숫자는 안내 메시지 후 다시 입력받습니다.
- `Ctrl+C`(KeyboardInterrupt)나 입력 스트림 종료(EOFError)가 발생해도 오류 없이 저장 후 안전하게 종료합니다.
- `state.json`이 없으면 기본 퀴즈 5개를 사용하고, 손상되었으면 안내 메시지를 출력한 뒤 기본 데이터로 초기화합니다.

## 파일 구조

```
python-quiz-game/
├── main.py        # 프로그램 진입점
├── quiz.py        # Quiz 클래스 (문제 출력, 정답 확인)
├── quiz_game.py   # QuizGame 클래스 (메뉴, 플레이, 추가, 목록, 점수, 저장/불러오기)
├── state.json     # 실행 중 생성되는 데이터 파일 (Git 제외)
│                  #  └ state.json.corrupt / .tmp: 손상 백업, 저장 임시 파일 (Git 제외)
├── .gitignore
└── README.md
```

## 데이터 파일 설명 (state.json)

- **경로**: 프로젝트 루트의 `state.json`
- **인코딩**: UTF-8
- **역할**: 퀴즈 목록과 최고 점수를 저장합니다. 실행 중 생성되는 데이터라 `.gitignore`로 Git에서 제외했습니다.

```json
{
    "high_score": 3,
    "quizzes": [
        {
            "question": "대한민국의 수도는?",
            "choices": ["부산", "서울", "대전", "인천"],
            "answer": 2
        }
    ]
}
```

| 키 | 타입 | 설명 |
|---|---|---|
| `high_score` | 정수 또는 `null` | 최고 정답 수. 아직 퀴즈를 풀지 않았다면 `null` |
| `quizzes` | 배열 | 퀴즈 목록 |
| `quizzes[].question` | 문자열 | 문제 (비어 있을 수 없음) |
| `quizzes[].choices` | 문자열 4개 배열 | 선택지 |
| `quizzes[].answer` | 정수 (1~4) | 정답 선택지 번호 |

형식이 올바르지 않으면 손상된 파일로 간주하고 기본 퀴즈로 초기화합니다.

## 설계 설명

### 클래스와 메서드 책임

| 파일 | 클래스/메서드 | 책임 |
|---|---|---|
| `quiz.py` | `Quiz` | 퀴즈 한 개의 데이터(question, choices, answer)를 표현 |
| | `show_question()` | 문제와 선택지 출력 |
| | `check_answer()` | 정답 여부 판정 |
| `quiz_game.py` | `QuizGame.run()` / `show_menu()` | 메뉴 표시와 선택 분기 (게임 흐름) |
| | `read_text()` / `read_int()` | **입력 검증**: 공백 제거, 빈 입력, 숫자 변환 실패, 범위 검사, Ctrl+C/EOF 처리 |
| | `play_quiz()` / `add_quiz()` / `list_quizzes()` / `show_high_score()` | 각 메뉴 기능 |
| | `load_state()` / `save_state()` / `backup_corrupted_file()` | **데이터 입출력**: JSON 읽기/쓰기, 검증, 손상 파일 백업 |
| | `initialize_quizzes()` | 기본 퀴즈 5개 생성 |
| | `safe_exit()` | 저장 후 안전 종료 |

입력 검증(`read_*`), 데이터 입출력(`*_state`), 화면/흐름(나머지)을 메서드 단위로 나누어 각 기능을 독립적으로 수정할 수 있게 했습니다.

### 클래스(객체지향)를 쓴 이유

- 퀴즈 하나가 가지는 데이터(문제, 선택지, 정답)와 동작(출력, 정답 확인)을 `Quiz`로 묶어, 퀴즈가 늘어나도 같은 방식으로 다룰 수 있습니다.
- 게임 상태(퀴즈 목록, 최고 점수, 저장 파일)를 `QuizGame`이 한곳에서 관리하므로 전역 변수 없이 메서드끼리 상태를 공유합니다.
- 함수만으로 만들면 상태를 인자로 계속 넘기거나 전역 변수를 써야 해서, 이 규모에서는 클래스가 더 읽기 쉽다고 판단했습니다. 대신 파일 수와 코드량이 조금 늘어나는 점이 단점입니다.

### 저장 방식과 안정성

- **JSON을 선택한 이유**: 사람이 직접 읽고 수정할 수 있고, Python 표준 라이브러리(`json`)만으로 다룰 수 있으며, 다른 언어·도구와도 쉽게 주고받을 수 있습니다.
- **필드 구조**: 퀴즈를 `quizzes` 배열의 객체로 묶어, 퀴즈 항목에 필드(예: 카테고리)를 추가해도 기존 구조를 바꾸지 않고 확장할 수 있습니다.
- **원자적 저장**: `state.json.tmp`에 먼저 쓴 뒤 `os.replace`로 교체합니다. 저장 도중 프로그램이 중단돼도 기존 `state.json`은 깨지지 않습니다.
- **손상 복구**: 파일이 손상되었거나 형식이 잘못되었으면 오류 사유를 출력하고, 원본을 `state.json.corrupt`로 보관한 뒤 기본 퀴즈로 초기화합니다. 보관된 파일을 열어 내용을 직접 복구할 수 있습니다.
- **저장 실패**: 쓰기 오류(`OSError`)가 나면 오류 메시지를 출력하고 프로그램은 계속 실행됩니다. 이 경우 변경 내용은 해당 실행 중에만 유지되므로, 디스크 공간/권한을 확인한 뒤 다시 저장(메뉴 진행 또는 종료)하면 됩니다.
- **Ctrl+C / EOF**: 안내 메시지를 출력하고 현재 상태를 저장한 뒤 종료합니다. 퀴즈 추가 도중 중단하면 입력 중이던 퀴즈는 저장하지 않고(롤백), 이미 저장된 퀴즈는 그대로 유지됩니다.
- **오류 발생 시 사용자 행동**: 오류는 화면에 출력되며 별도 로그 파일은 없습니다. 손상 오류가 나면 `state.json.corrupt`를 확인하세요.

### 한계와 확장

- 전체 데이터를 한 번에 읽고 쓰는 방식이라 퀴즈가 수만 개 이상으로 많아지거나 여러 사용자가 동시에 쓰는 환경에는 맞지 않습니다. 이런 경우 SQLite 같은 DB로 전환하는 것이 좋습니다.
- 현재 규모(수십~수백 개 퀴즈, 단일 사용자)에서는 JSON으로 충분합니다.

### 입력 검증 테스트 사례

직접 실행해 확인한 사례입니다.

| 입력 | 위치 | 결과 |
|---|---|---|
| ` 1 ` (앞뒤 공백) | 메뉴 | 공백 제거 후 정상 처리 |
| `abc` | 메뉴/정답 | "숫자를 입력해 줘" 후 재입력 |
| (빈 입력) | 메뉴/정답/질문/선택지 | 안내 메시지 후 재입력 |
| `9`, `0`(정답) | 메뉴/정답 | 범위 안내 후 재입력 |
| `²` (특수 숫자 문자) | 정답 | 오류 없이 "숫자를 입력해 줘" |
| Ctrl+C, EOF | 모든 입력 | 저장 후 안전 종료 |
| `{bad` (손상된 state.json) | 시작 시 | 안내, `state.json.corrupt`로 보관, 기본 퀴즈로 시작 |
| state.json 없음 | 시작 시 | 기본 퀴즈 5개로 시작 |

## 개발 환경

터미널에서 직접 실행한 결과입니다. (macOS 26.2)

```
$ python3 --version
Python 3.15.2
$ git --version
git version 2.56.0
$ git config user.name
Char1-es
$ git remote -v
origin	git@github.com:Char1-es/python-quiz-game.git (fetch)
origin	git@github.com:Char1-es/python-quiz-game.git (push)
$ git branch -a
  feature/quiz-play
* main
  remotes/origin/HEAD -> origin/main
  remotes/origin/feature/quiz-play
  remotes/origin/main
```

## 실행 결과

실제로 `python3 main.py`를 실행한 결과입니다. `<입력>` 표시는 사용자가 입력한 값입니다.

### 최고 점수 확인 (퀴즈를 풀기 전)

```
메뉴를 선택해 줘: <4>
아직 퀴즈를 풀지 않았어. 퀴즈를 풀고 점수를 남겨 봐!
```

### 퀴즈 추가

기본 퀴즈 5개에 아래 퀴즈를 직접 입력해 추가한 예시입니다. 이후 목록과 풀기 결과에 6문제가 나오는 이유입니다.

```
===== 퀴즈 추가 =====
질문을 입력해 줘: <대한민국의 국기 이름은?>
1번 선택지를 입력해 줘: <태극기>
2번 선택지를 입력해 줘: <무궁화기>
3번 선택지를 입력해 줘: <한반도기>
4번 선택지를 입력해 줘: <오륙기>
정답 번호를 입력해 줘 (1~4): <1>
퀴즈가 추가됐어!
```

### 퀴즈 목록

```
===== 퀴즈 목록 =====

[1] 대한민국의 수도는?
  1. 부산
  2. 서울
  3. 대전
  4. 인천

... (2~5번 생략) ...

[6] 대한민국의 국기 이름은?
  1. 태극기
  2. 무궁화기
  3. 한반도기
  4. 오륙기
```

### 퀴즈 풀기

```
===== 문제 1 =====
대한민국의 수도는?
1. 부산
2. 서울
3. 대전
4. 인천
정답 번호를 입력해 줘: <2>
정답이야!

... (문제 2~5 생략) ...

===== 문제 6 =====
대한민국의 국기 이름은?
1. 태극기
2. 무궁화기
3. 한반도기
4. 오륙기
정답 번호를 입력해 줘: <1>
정답이야!

===== 퀴즈 결과 =====
총 문제 수: 6
정답 수: 6
점수: 6점
최고 점수를 갱신했어!
```

### 최고 점수 확인 (플레이 후, 프로그램 재실행 뒤에도 유지)

```
메뉴를 선택해 줘: <4>
현재 최고 점수: 6점
```

### 잘못된 입력 처리

```
메뉴를 선택해 줘: <abc>
숫자를 입력해 줘. 다시 선택해 줘.
메뉴를 선택해 줘: <(빈 입력)>
메뉴 번호를 입력해 줘.
정답 번호를 입력해 줘 (1~4): <9>
1부터 4 사이의 숫자를 입력해 줘.
```

### Git 이력 (`git log --oneline --graph`)

```
* e325fa5 docs: clone 실습 내용 README에 추가
* 30c3858 docs: README 작성 (개요, 실행 방법, 기능, 파일 구조, state.json 스키마)
*   24910ad merge: feature/quiz-play 브랜치 병합
|\
| * 6c7344e refactor: 공통 입력 처리 분리 및 점수 미기록 처리
| * d8a4215 chore: exclude runtime state file from git
| * a2913cb fix: validate saved quiz data
| * b4a8032 fix: handle interruption during quiz creation
| * bb97149 feat: add application entry point
| * 385f38b feat: add quiz listing feature
| * 5e1780e feat: add quiz creation
| * 9e3da01 feat: add quiz play and score tracking
|/
* 67996b2 feat: Quiz 클래스 구현
* 5873040 Initial commit
```

## Git 작업 방식

- **저장소**: https://github.com/Char1-es/python-quiz-game (`origin`, SSH)
- **커밋 수**: main 기준 19개 (병합 커밋 2개 포함)

### 커밋 메시지 규칙

`종류: 변경 내용 요약` 형식으로 쓰고, 기능/수정 단위로 커밋합니다.

| 종류 | 용도 | 예시 |
|---|---|---|
| `feat` | 기능 추가 | `feat: add quiz creation` |
| `fix` | 버그/검증 수정 | `fix: validate saved quiz data` |
| `refactor` | 동작 변경 없는 구조 개선 | `refactor: 공통 입력 처리 분리 및 점수 미기록 처리` |
| `docs` | 문서 | `docs: README 작성` |
| `chore` | 설정/기타 | `chore: exclude runtime state file from git` |

### 브랜치 전략

- `main`: 항상 실행 가능한 상태를 유지하는 기준 브랜치입니다.
- `feature/quiz-play`: 퀴즈 풀기·추가·목록·점수 등 게임 기능을 개발한 브랜치입니다.
- `feature/safe-storage`: 원자적 저장과 손상 파일 백업 기능을 추가한 브랜치입니다. (병합 사유: 평가에서 지적된 저장 안정성 보완)
- 기능 개발은 `main`에서 feature 브랜치를 분기해 진행하고, 기능이 동작하는 것을 확인한 뒤 `git merge --no-ff`로 `main`에 병합합니다. `--no-ff`를 써서 어떤 기능이 언제 합쳐졌는지 그래프에 남깁니다. (병합 커밋: `24910ad`)
- README 같은 문서 수정은 `main`에 바로 커밋했습니다.

### clone / pull 실습 기록

별도 폴더에 clone한 뒤 README를 수정해 push하고, 원래 작업 폴더에서 pull로 가져왔습니다. 실제 터미널 출력이며 중간 줄은 생략했습니다.

```
# 1) clone (별도 폴더)
$ git clone git@github.com:Char1-es/python-quiz-game.git python-quiz-game-clone
Cloning into 'python-quiz-game-clone'...

# 2) clone한 저장소에서 README 수정 후 commit, push
$ git add README.md
$ git commit -m "docs: clone 실습 내용 README에 추가"
$ git push origin main
   30c3858..e325fa5  main -> main

# 3) 원래 작업 폴더에서 pull
$ git pull origin main
 * branch            main       -> FETCH_HEAD
   30c3858..e325fa5  main       -> origin/main
Updating 30c3858..e325fa5
Fast-forward
 README.md | 4 ++++
 1 file changed, 4 insertions(+)

# 4) 반영 확인
$ git log --oneline -3
e325fa5 docs: clone 실습 내용 README에 추가
30c3858 docs: README 작성 (개요, 실행 방법, 기능, 파일 구조, state.json 스키마)
24910ad merge: feature/quiz-play 브랜치 병합
```

## 요구사항 변경 시 수정 대상 (영향 범위)

| 변경 요구 | 수정 파일 / 메서드 | 영향 범위 |
|---|---|---|
| 선택지 개수 변경 (4개 → N개) | `quiz_game.py`: `add_quiz`, `load_state`(길이 검증), `read_int` 범위 인자, `play_quiz` | 저장 데이터 검증, 입력 범위, 기존 `state.json` 호환 |
| 점수 계산 방식 변경 | `quiz_game.py`: `play_quiz`, `show_high_score` | `high_score` 의미 변경 시 `state.json` 호환 확인 |
| 퀴즈 필드 추가 (예: 카테고리) | `quiz.py`: `Quiz`; `quiz_game.py`: `load_state`, `save_state`, `list_quizzes` | state.json 스키마와 README 스키마 표 |
| 메뉴 추가 | `quiz_game.py`: `show_menu`, `run` + 새 메서드 | 메뉴 번호 안내 |
| 저장소를 DB로 변경 | `quiz_game.py`: `load_state`, `save_state`, `backup_corrupted_file` | 입출력 메서드에 격리되어 있어 게임 로직 영향 적음 |
| 기본 퀴즈/주제 변경 | `quiz_game.py`: `initialize_quizzes` | 이미 만들어진 `state.json`에는 반영되지 않음 |

