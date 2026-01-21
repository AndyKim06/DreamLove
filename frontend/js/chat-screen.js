/* frontend/js/chat-screen.js */

let partnerName = '노애정';

window.onload = function() {
    // 1. 데이터 로드
    partnerName = localStorage.getItem('partner_name') || '노애정';
    const situation = localStorage.getItem('user_situation') || '영화관'; 
    
    // 2. 인트로 텍스트 설정
    const introName = document.getElementById('intro-name');
    const introPlace = document.getElementById('intro-place');
    if(introName) introName.innerText = partnerName;
    if(introPlace) introPlace.innerText = situation;

    // 3. 인트로 애니메이션
    setTimeout(() => {
        document.getElementById('step-1').classList.add('hidden');
        document.getElementById('step-2').classList.remove('hidden');
        document.getElementById('start-btn').classList.remove('hidden');
    }, 3000);
};

// [공략하기] 클릭
function startGame() {
    document.getElementById('intro-layer').classList.add('hidden');
    document.getElementById('game-layer').classList.remove('hidden');
    initGame();
}

function initGame() {
    // 1. 이름 설정
    document.getElementById('char-name').innerText = partnerName + " :";

    // 2. 이미지 로드 (임시 랜덤)
    // 실제로는 백엔드 연동 필요
    const mainPhoto = document.getElementById('main-photo');
    mainPhoto.src = `https://picsum.photos/800/600?random=1`;
}

function nextDialogue() {
    alert("다음 대화로 넘어갑니다!");
}