/* frontend/js/chat-screen.js */

const API_BASE = 'http://localhost:8000';

// 게임 상태 관리
let gameState = {
    userId: localStorage.getItem('userId') || 'test_user_1', 
    partnerName: '이상형',
    userName: '',
    userGender: '',
    concern: '',
    idealPersonality: '',
    stage: 0,
    score: 0,
    score_change: 0, 
    parsedContext: null,
    ideal_image_base_path: '', // 서버에서 받은 "frontend\\imageCloud\\standard_female_1_cinema" 형태 저장
    negativeFeedbacks: [],
    currentQuestion: '',
    isWaiting: false,
    imageRetryCount: 0
};

window.onload = function() {
    // 1. localStorage에서 사용자 데이터 로드
    gameState.userName = localStorage.getItem('user_name') || '사용자';
    gameState.userGender = localStorage.getItem('user_gender') || '남자';
    gameState.concern = localStorage.getItem('user_concern') || '카페에서 소개팅 상대를 처음 만나는데 어떻게 말을 걸어야 할지 모르겠어요';
    
    const personality = localStorage.getItem('ideal_personality') || 'warm';
    gameState.idealPersonality = personality === 'warm' ? '다정한' : '시크한';
    gameState.partnerName = '이상형';
    
    // 2. 인트로 UI 초기화
    const introName = document.getElementById('intro-name');
    const introPlace = document.getElementById('intro-place');
    const targetGenderText = document.getElementById('target-gender-text');

    if(introName) introName.innerText = gameState.partnerName;
    if(introPlace) introPlace.innerText = '로딩 중...';
    if(targetGenderText) {
        targetGenderText.innerText = gameState.userGender === '남자' ? '그녀' : '그';
    }

    // Stage 0 요청 (인사말 및 이미지 경로 수신 시작)
    sendChatRequest('');

    // 3. 인트로 시작 버튼 활성화
    setTimeout(() => {
        const startBtn = document.getElementById('start-btn');
        if(startBtn) startBtn.classList.remove('hidden');
    }, 3000);
};

// 타이핑 애니메이션 함수
function typeWriter(element, text, speed = 50) {
    element.innerHTML = ""; 
    let i = 0;
    function type() {
        if (i < text.length) {
            if (text.charAt(i) === '\n') {
                element.innerHTML += '<br>';
            } else {
                element.innerHTML += text.charAt(i);
            }
            i++;
            setTimeout(type, speed);
        }
    }
    type();
}

// 게임 시작 버튼 클릭 시 호출
async function startGame() {
    document.getElementById('intro-layer').classList.add('hidden');
    const mainPhoto = document.getElementById('main-photo');
    mainPhoto.classList.remove('hidden');
    
    // 초기 이미지 설정 (Neutral)
    updateCharacterImage('Neutral');

    document.getElementById('user-input-mode').classList.remove('hidden');
    document.getElementById('start-btn').classList.add('hidden');

    if (gameState.currentQuestion) {
        const charName = document.getElementById('char-name');
        const charMsg = document.getElementById('char-msg');
        charName.innerText = gameState.partnerName + " :";
        typeWriter(charMsg, gameState.currentQuestion, 50);
    }
}

// 백엔드 API 호출 함수
async function sendChatRequest(userMessage) {
    if (gameState.isWaiting) return;
    gameState.isWaiting = true;
    
    if (document.getElementById('intro-layer').classList.contains('hidden')) {
        document.getElementById('char-msg').innerText = '...'; 
    }
    
    try {
        const requestData = {
            user_info: {
                name: gameState.userName,
                gender: gameState.userGender,
                concern: gameState.concern
            },
            ideal_type: {
                personality: gameState.idealPersonality
            },
            user_message: userMessage,
            current_question: gameState.currentQuestion,
            stage: gameState.stage,
            current_score: gameState.score,
            negative_feedbacks: gameState.negativeFeedbacks
        };
        
        if (gameState.parsedContext) {
            requestData.parsed_context = gameState.parsedContext;
        }
        
        const userId = localStorage.getItem("userId") || gameState.userId;
        const response = await fetch(`${API_BASE}/chat/simulate?userId=${userId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '서버 오류');
        }
        
        const data = await response.json();
        
        // 데이터 업데이트
        gameState.stage = data.next_stage;
        gameState.score = data.updated_score;
        gameState.score_change = data.score_change || 0; 
        gameState.negativeFeedbacks = data.negative_feedbacks || [];
        
        // 이미지 경로 저장 (리스트 형태 에러 방지)
        if (data.ideal_image_base_path) {
            gameState.ideal_image_base_path = Array.isArray(data.ideal_image_base_path) 
                ? data.ideal_image_base_path[0] 
                : data.ideal_image_base_path;
        }

        if (data.parsed_context) {
            gameState.parsedContext = data.parsed_context;
            const introPlace = document.getElementById('intro-place');
            if (introPlace) {
                introPlace.innerText = data.parsed_context.location;
            }
        }
        
        updateUI(data);
        
        if (data.end) {
            showFinalResult(data);
        }
        
    } catch (error) {
        console.error('❌ API 오류:', error);
        alert(`오류가 발생했습니다: ${error.message}`);
    } finally {
        gameState.isWaiting = false;
    }
}

// 점수 변화 및 경로 처리에 따른 이미지 교체
function updateCharacterImage(forcedEmotion = null) {
    const mainPhoto = document.getElementById('main-photo');
    if (!gameState.ideal_image_base_path) return;

    let emotion = 'Neutral';
    if (forcedEmotion) {
        emotion = forcedEmotion;
    } else {
        if (gameState.score_change > 0) emotion = 'Smiling';
        else if (gameState.score_change < 0) emotion = 'Disappointed';
    }

    // 경로 보정: "frontend\\imageCloud\\path" -> "imageCloud/path"
    let webPath = gameState.ideal_image_base_path
        .replace(/\\/g, '/')               // 역슬래시를 슬래시로 변경
        .replace(/^frontend\//i, '');      // 앞부분의 frontend/ 제거

    // 파일명 조립 및 확장자 처리
    const basePath = webPath.replace(/\.png$/i, '');
    const expressionPath = `./${basePath}_${emotion}.png`;

    loadExpressionImage(expressionPath);
    console.log(`📸 이미지 업데이트 시도: ${emotion} (${expressionPath})`);
}

function loadExpressionImage(src, maxRetries = 12, delayMs = 1000) {
    const mainPhoto = document.getElementById('main-photo');
    const loadingOverlay = document.getElementById('loading-overlay');

    if (loadingOverlay) {
        loadingOverlay.classList.remove('hidden');
    }

    const tryLoad = () => {
        mainPhoto.onerror = () => {
            if (gameState.imageRetryCount < maxRetries) {
                gameState.imageRetryCount += 1;
                setTimeout(tryLoad, delayMs);
            } else {
                console.error(`❌ 이미지 로딩 실패: ${src}`);
            }
        };

        mainPhoto.onload = () => {
            gameState.imageRetryCount = 0;
            if (loadingOverlay) {
                loadingOverlay.classList.add('hidden');
            }
        };

        mainPhoto.src = src;
    };

    tryLoad();
}

function updateUI(data) {
    const charName = document.getElementById('char-name');
    const charMsg = document.getElementById('char-msg');

    if (document.getElementById('intro-layer').classList.contains('hidden')) {
        charName.innerText = gameState.partnerName + " :";
        charMsg.innerHTML = data.bot_message.replace(/\n/g, '<br>');
        
        // 점수에 따른 이미지 변경 실행
        updateCharacterImage();
    }
    
    gameState.currentQuestion = data.bot_message;
    const stationText = document.querySelector('.station-text');
    if(stationText) stationText.innerText = `STAGE ${gameState.stage}`;
    
    const input = document.getElementById('user-input');
    input.value = '';
    input.disabled = false;
    if (document.getElementById('intro-layer').classList.contains('hidden')) {
        input.focus();
    }
}

function sendMessage() {
    const input = document.getElementById('user-input');
    const userAnswer = input.value.trim();
    
    if (!userAnswer) return;
    if (gameState.isWaiting) return;
    
    input.disabled = true;
    sendChatRequest(userAnswer);
}

function showFinalResult(data) {
    const resultData = {
        score: data.updated_score,
        feedback: data.final_feedback || data.bot_message,
        negativeFeedbacks: data.negative_feedbacks || []
    };
    localStorage.setItem('chat_result', JSON.stringify(resultData));
    setTimeout(() => {
        location.href = '10-feedback.html';
    }, 1500);
}