/* frontend/js/game-start.js */

// 페이지 로드 시 자동 실행
window.onload = function() {
    // 2초 후 게임화면으로 자동 이동 (로딩 효과)
    setTimeout(() => {
        startGame();
    }, 2000);
};

function startGame() {
    // 깜빡임 멈추고 잠시 멈칫하는 효과
    const text = document.querySelector('.game-start-text');
    if (text) {
        text.style.animation = 'none'; // 깜빡임 중지
        text.style.color = '#808CE7';  // 색상 변경 (활성화 느낌)
    }
    
    // 0.5초 뒤 이동
    setTimeout(() => {
        location.href = '09-chat-screen.html'; 
    }, 500);
}