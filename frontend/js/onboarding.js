document.addEventListener('DOMContentLoaded', () => {
    const logo = document.getElementById('step-logo');
    const onScreen = document.getElementById('step-on-screen');
    const startBtn = document.getElementById('start-btn');

    // 1. 1초 뒤: 로고 등장
    setTimeout(() => {
        logo.classList.remove('hidden');
    }, 1000);

    // 2. 3.5초 뒤: 로고 사라지고 TV 화면 켜짐 + 버튼 등장
    setTimeout(() => {
        logo.style.display = 'none'; // 로고 제거
        
        onScreen.classList.remove('hidden'); // TV 화면 켜짐
        
        // 화면이 켜지고 0.5초 뒤 버튼 등장
        setTimeout(() => {
            startBtn.classList.remove('hidden');
        }, 500);
    }, 3500);

    // 3. 버튼 클릭 시 이동
    startBtn.addEventListener('click', () => {
        window.location.href = '01-profile.html';
    });
});