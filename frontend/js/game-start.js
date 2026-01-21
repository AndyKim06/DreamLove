/* frontend/js/game-start.js */

// 화면 클릭 시 게임 시작
function startGame() {
    // 효과음이 있다면 여기서 재생 가능
    
    // 깜빡임 멈추고 잠시 멈칫하는 효과 (선택사항)
    const text = document.querySelector('.game-start-text');
    text.style.animation = 'none'; // 깜빡임 중지
    text.style.color = '#808CE7';  // 색상 변경 (활성화 느낌)
    
    // 0.3초 뒤 이동 (클릭 피드백)
    setTimeout(() => {
        // 다음 페이지: 실제 채팅 시뮬레이션 화면
        // 파일명은 추후 만들 페이지에 맞춰 수정하세요 
        location.href = '09-chat-screen.html'; 
    }, 300);
}

// (옵션) 키보드 엔터키 눌러도 시작
window.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
        startGame();
    }
});