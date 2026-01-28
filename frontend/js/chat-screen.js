/* frontend/js/chat-screen.js */

const API_BASE = 'http://localhost:8000';

// 게임 상태
let gameState = {
    partnerName: '이상형',
    userName: '',
    userGender: '',
    concern: '',
    idealPersonality: '',
    stage: 0,
    score: 0,
    parsedContext: null,
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

    // [New] 페이지 로드와 동시에 백엔드 요청 시작 (장소 정보 획득을 위해)
    // 화면에는 아직 intro-layer가 떠 있음
    sendChatRequest('');

    // 3. 인트로 애니메이션 (텍스트 변경 없이 버튼만 표시)
    setTimeout(() => {
        // 기존 텍스트(step-1) 유지, step-2는 사용 안 함
        // document.getElementById('step-1').classList.add('hidden');
        // document.getElementById('step-2').classList.remove('hidden');
        
        document.getElementById('start-btn').classList.remove('hidden');
    }, 3000);
};

// [공략하기] 클릭 - 첫 인사 받기
async function startGame() {
    document.getElementById('intro-layer').classList.add('hidden');
    document.getElementById('game-layer').classList.remove('hidden');
    
    // 이미 window.onload에서 요청을 보냈으므로, 여기서는 UI 전환만 하면 됨
    // 만약 아직 응답이 안 왔다면(isWaiting=true), 로딩 상태 유지됨
    // 응답이 오면 updateUI가 실행되면서 화면이 갱신됨
    
    // 혹시 요청이 실패했거나 해서 다시 보내야 할 경우를 대비해 체크 가능하지만
    // 현재 구조에서는 onload 요청 결과를 기다리는 것이 자연스러움
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
        
        const response = await fetch(`${API_BASE}/chat/simulate`, {
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
                introText.innerHTML = `당신은 <span class="highlight">이상형</span>과 <span class="highlight">${data.parsed_context.dating_place}</span>에 왔습니다.`;
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

// UI 업데이트
function updateUI(data) {
    // 1. 이름 설정
    document.getElementById('char-name').innerText = gameState.partnerName + " :";
    
    // 2. 메시지 표시
    document.getElementById('char-msg').innerHTML = data.bot_message.replace(/\n/g, '<br>');
    
    // 3. 다음 질문 저장 (사용자가 답변할 질문)
    gameState.currentQuestion = data.bot_message;
    
    // 4. Stage 표시
    document.querySelector('.station-text').innerText = `STAGE ${gameState.stage}`;
    
    // 5. 하트 업데이트 (점수에 따라)
    updateHearts();
    
    // 6. 이미지 로드
    const mainPhoto = document.getElementById('main-photo');
    mainPhoto.src = `https://picsum.photos/800/600?random=${gameState.stage}`;
    
    // 7. 입력창 초기화 및 포커스
    const input = document.getElementById('user-input');
    input.value = '';
    input.disabled = false;
    input.focus();
}

// 하트 업데이트 (점수 기반)
function updateHearts() {
    const hearts = document.querySelectorAll('.heart-icon');
    const heartCount = Math.max(0, Math.min(4, Math.floor(gameState.score / 10)));
    
    hearts.forEach((heart, index) => {
        if (index < heartCount) {
            heart.classList.add('active');
        } else {
            heart.classList.remove('active');
        }
    });
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