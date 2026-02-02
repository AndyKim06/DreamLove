/* frontend/js/chat-screen.js */

const API_BASE = 'http://localhost:8000';


// 게임 상태
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
    ideal_image_base_path: '',
    negativeFeedbacks: [],
    currentQuestion: '',
    isWaiting: false
};

window.onload = function() {
    // 1. localStorage에서 사용자 데이터 로드
    gameState.userName = localStorage.getItem('user_name') || '사용자';
    gameState.userGender = localStorage.getItem('user_gender') || '남자';
    gameState.concern = localStorage.getItem('user_concern') || '카페에서 소개팅 상대를 처음 만나는데 어떻게 말을 걸어야 할지 모르겠어요';
    
    const personality = localStorage.getItem('ideal_personality') || 'warm';
    gameState.idealPersonality = personality === 'warm' ? '다정한' : '시크한';
    
    // 상대방 성별에 따른 기본 이름 -> '이상형'으로 고정
    gameState.partnerName = '이상형';
    
    // 2. 인트로 텍스트 설정 (초기에는 장소를 모르므로 기본값)
    const introName = document.getElementById('intro-name');
    const introPlace = document.getElementById('intro-place');
    const targetGenderText = document.getElementById('target-gender-text');

    if(introName) introName.innerText = gameState.partnerName;
    if(introPlace) introPlace.innerText = '로딩 중...';
    if(targetGenderText) {
        // 내가 남자면 상대는 여자(그녀), 내가 여자면 상대는 남자(그)
        targetGenderText.innerText = gameState.userGender === '남자' ? '그녀' : '그';
    }
    sendChatRequest('');

    // 3. 인트로 애니메이션 (텍스트 변경 없이 버튼만 표시)
    setTimeout(() => {
        document.getElementById('start-btn').classList.remove('hidden');
    }, 3000);
};


// 타이핑 애니메이션 함수
function typeWriter(element, text, speed = 50) {
    element.innerHTML = ""; // 기존 내용 초기화
    let i = 0;
    
    function type() {
        if (i < text.length) {
            // 줄바꿈 문자(\n)를 <br>로 변환
            if (text.charAt(i) === '\n') {
                element.innerHTML += '<br>';
            } else {
                element.innerHTML += text.charAt(i);
            }
            i++;
            setTimeout(type, speed); // 지정된 속도로 다음 글자 출력
        }
    }
    type();
}

async function startGame() {
    // 1. 인트로 레이어 숨기고 메인 레이어 노출
    document.getElementById('intro-layer').classList.add('hidden');
    
    const mainPhoto = document.getElementById('main-photo');
    mainPhoto.classList.remove('hidden');
    
    // 2. 초기 이미지 설정 (Neutral 표정)
    if (gameState.parsedContext && gameState.parsedContext.location) {
        const basePath = gameState.ideal_image_base_path || "standard_female_1"; 
        const location = gameState.parsedContext.location;
        mainPhoto.src = `./imageCloud/${basePath}_${location}_Neutral.png`;
    }

    // 3. UI 모드 전환 (입력창 활성화, 시작버튼 숨김)
    document.getElementById('user-input-mode').classList.remove('hidden');
    document.getElementById('start-btn').classList.add('hidden');

    // 4. 첫 대사 출력 (타이핑 애니메이션 적용)
    if (gameState.currentQuestion) {
        const charName = document.getElementById('char-name');
        const charMsg = document.getElementById('char-msg');
        
        // 이름 라벨은 즉시 표시
        charName.innerText = gameState.partnerName + " :";
        
        // 대사 텍스트에만 타이핑 효과 적용
        typeWriter(charMsg, gameState.currentQuestion, 50);
    }
}

// 백엔드 API 호출
async function sendChatRequest(userMessage) {
    if (gameState.isWaiting) return;
    gameState.isWaiting = true;
    
    // 로딩 표시 (intro-layer가 떠있을 때는 필요 없음)
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
        
        // parsedContext가 있으면 포함
        if (gameState.parsedContext) {
            requestData.parsed_context = gameState.parsedContext;
        }
        
        console.log('📤 요청:', requestData);
        const userId = localStorage.getItem("userId");
        const response = await fetch(`${API_BASE}/chat/simulate?userId=${userId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '서버 오류');
        }
        
        const data = await response.json();
        console.log('📥 응답:', data);
        
        // 게임 상태 업데이트
        gameState.stage = data.next_stage;
        gameState.score = data.updated_score;
        gameState.negativeFeedbacks = data.negative_feedbacks || [];
        
        // parsedContext 저장 (stage 1에서 받음)
        if (data.parsed_context) {
            gameState.parsedContext = data.parsed_context;
            // 장소 정보 업데이트
            const introText = document.getElementById('intro-text');
            if (introText) {
                introText.innerHTML = `당신은 <span class="highlight">이상형</span>과 <span class="highlight">${data.parsed_context.location}</span>에 왔습니다.`;
            }
        }
        
        // UI 업데이트
        updateUI(data);
        
        // 게임 종료 처리
        if (data.end) {
            showFinalResult(data);
        }
        
    } catch (error) {
        console.error('❌ API 오류:', error);
        alert(`오류가 발생했습니다: ${error.message}\n\n백엔드 서버가 실행 중인지 확인해주세요.`);
    } finally {
        gameState.isWaiting = false;
    }
}


function updateUI(data) {
    const charName = document.getElementById('char-name');
    const charMsg = document.getElementById('char-msg');
    const mainPhoto = document.getElementById('main-photo');

    // 1. 이름 및 메시지 설정
    if (!document.getElementById('intro-layer').classList.contains('hidden')) {
        charName.innerText = "";
        charMsg.innerHTML = "";
    } else {
        charName.innerText = gameState.partnerName + " :";
        charMsg.innerHTML = data.bot_message.replace(/\n/g, '<br>');
    }
    
    // 초기 상태(대답 전)나 점수 변화가 없을 때는 Neutral
    let emotion = 'Neutral'; 
    if (gameState.stage > 1) { // 게임이 진행된 상태라면 점수 변화 체크
        if (gameState.score_change > 0) emotion = 'Smiling';
        else if (gameState.score_change < 0) emotion = 'Disappointed';
    }

    // 백엔드 코드 규칙: {userId_번호}_{장소}_{감정}.png
    if (data.ideal_image_base_path && data.parsed_context) {
        const location = data.parsed_context.location; // 예: cinema
        const basePath = data.ideal_image_base_path;    // 예: standard_female_1
        // 최종 파일명 조립
        const fileName = `${basePath}_${location}_${emotion}.png`;
        mainPhoto.src = `./imageCloud/${fileName}`;
        
        mainPhoto.onerror = () => {
            console.error("이미지 로드 실패:", mainPhoto.src);
            // 로드 실패 시 기본 Neutral 이미지 시도
            mainPhoto.src = `./imageCloud/${basePath}_${location}_Neutral.png`;
        };
    }
    
    // 3. 나머지 상태 업데이트
    gameState.currentQuestion = data.bot_message;
    document.querySelector('.station-text').innerText = `STAGE ${gameState.stage}`;
    
    // 4. 입력창 설정
    const input = document.getElementById('user-input');
    input.value = '';
    input.disabled = false;
    if (document.getElementById('intro-layer').classList.contains('hidden')) {
        input.focus();
    }
}



// 메시지 전송
function sendMessage() {
    const input = document.getElementById('user-input');
    const userAnswer = input.value.trim();
    
    if (!userAnswer) {
        alert('답변을 입력해주세요!');
        return;
    }
    
    if (gameState.isWaiting) {
        alert('응답을 기다리는 중입니다...');
        return;
    }
    
    // 입력창 비활성화 (전송 중 중복 방지)
    input.disabled = true;
    
    // 백엔드에 사용자 답변 전송
    sendChatRequest(userAnswer);
}

// 최종 결과 표시
function showFinalResult(data) {
    const feedback = data.final_feedback || '수고하셨습니다!';
    const finalScore = data.updated_score;
    const negativeFeedbacks = data.negative_feedbacks || [];
    
    // 결과 데이터를 localStorage에 저장
    const resultData = {
        score: finalScore,
        feedback: feedback,
        negativeFeedbacks: negativeFeedbacks,
        couplePhotoUrl: '' // 나중에 실제 생성된 이미지 URL로 대체
    };
    
    localStorage.setItem('chat_result', JSON.stringify(resultData));
    
    // 피드백 페이지로 이동
    setTimeout(() => {
        location.href = '10-feedback.html';
    }, 1000);
}