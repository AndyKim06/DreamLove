/* frontend/js/ideal-personality.js */

let selectedPersonality = null; // 'warm' or 'chic'

function goBack() {
    window.history.back();
}

function selectPersonality(type) {
    selectedPersonality = type;

    // 1. 초기화
    const items = document.querySelectorAll('.option-item');
    items.forEach(item => item.classList.remove('selected'));

    // 2. 선택 표시
    if (type === 'warm') {
        document.querySelector('.option-left').classList.add('selected');
    } else if (type === 'chic') {
        document.querySelector('.option-right').classList.add('selected');
    }
}

function goNext() {
    if (!selectedPersonality) {
        alert("원하는 성격을 선택해주세요!");
        return;
    }

    // 데이터 저장
    localStorage.setItem('ideal_personality', selectedPersonality);

    // 다음 페이지 이동 (예: 08-game-start.html)
    // alert("성격 선택 완료! 다음으로 넘어갑니다.");
    location.href = 'loading.html';
}