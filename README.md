# 💌 DreamLove (AI Dating Simulation Backend)

**Solar API**를 활용한 연애 시뮬레이션 AI 챗봇 백엔드 서비스입니다. 사용자의 연애 고민을 분석하여 가상의 데이트 상대와 대화하며 연애 능력을 진단하고 피드백을 제공합니다.

## ✨ 주요 기능

*   **💘 연애 시뮬레이션**: 사용자의 성별, 고민, 이상형(다정한/시크한)을 반영한 1:1 롤플레잉
*   **🧩 상황 자동 분석**: 사용자의 고민 텍스트에서 '데이트 장소'와 '상대와의 관계'를 자동 추출
*   **📊 실시간 평가 시스템**: 사용자의 답변을 AI가 분석하여 점수 부여 (+10, +5, -5, -10)
*   **📝 맞춤형 피드백**: 대화 종료 후 점수와 대화 내용을 바탕으로 구체적인 조언 제공
*   **🔄 6단계 대화 흐름**: 인사(Stage 0)부터 최종 평가(Stage 6)까지 체계적인 시나리오 진행

## 🛠 기술 스택

*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **AI Model**: Solar API (Large Language Model)
*   **Libraries**: Uvicorn, Pydantic, Httpx

## 🚀 설치 및 실행

### 1. 가상환경 설정 및 활성화 (필수)
프로젝트의 의존성 라이브러리를 격리된 환경에서 관리하기 위해 가상환경을 사용합니다.

**Windows (PowerShell)**
```powershell
# 가상환경 생성 (최초 1회)
python -m venv venv

# 가상환경 활성화
.\venv\Scripts\activate
```

**Linux / macOS / WSL2**
```bash
# 가상환경 생성 (최초 1회)
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate
```

### 2. 환경 변수 설정
1. `env.example` 파일을 복사하여 `.env` 파일을 생성합니다.
   ```bash
   # Windows
   copy env.example .env

   # Mac / Linux
   cp env.example .env
   ```
2. 발급받은 Solar API 키를 `.env` 파일에 입력합니다.
```env
SOLAR_API_KEY=your_solar_api_key_here
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. 서버 실행 
먼저 백엔드 서버를 실행해야 합니다. 
```bash
python -m uvicorn app.main:app --reload
```
`Application startup complete.` 메시지가 뜨면 실행 성공입니다.

### 5. 서비스 테스트 (CLI)
터미널에서 직접 대화해보며 서비스를 테스트할 수 있습니다.
**새 터미널**을 열고(서버 실행 중인 터미널 유지), 가상환경을 활성화한 뒤 실행하세요.
```bash
python interactive_cli.py
```

### 6. API 문서 확인 (Swagger UI)
서버가 실행 중일 때 브라우저에서 아래 주소로 접속하면 API 문서를 볼 수 있습니다.
- [http://localhost:8000/docs](http://localhost:8000/docs)

## 📂 프로젝트 구조

```
DreamLove/
├── app/
│   ├── core/       # 설정 (config.py)
│   ├── models/     # 데이터 모델 (schemas.py)
│   ├── routers/    # API 라우터 (chat.py)
│   ├── services/   # 비즈니스 로직
│   │   ├── chat_flow.py      # 대화 흐름 및 평가
│   │   ├── concern_parser.py # 고민 분석
│   │   └── solar_client.py   # Solar API 통신
│   └── main.py     # 앱 진입점
├── interactive_cli.py # CLI 테스트 도구
└── requirements.txt
```
