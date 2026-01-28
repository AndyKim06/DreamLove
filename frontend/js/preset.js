/* frontend/js/preset.js */

let selectedType = null;

function goBack() {
    window.history.back();
}

function selectType(type) {
    selectedType = type;
    
    // 1. 모든 윈도우 선택 해제
    document.querySelectorAll('.pixel-window').forEach(win => {
        win.classList.remove('selected');
    });
    
    // 2. 선택한 윈도우 활성화
    // type1 -> window-1 클래스 매핑
    const index = type.replace('type', '');
    const targetWindow = document.querySelector(`.window-${index}`);
    
    if (targetWindow) {
        targetWindow.classList.add('selected');
    }
}

function goNext() {
    if (!selectedType) {
        alert("원하는 이상형 스타일을 선택해주세요!");
        return;
    }
    
    // 데이터 저장
    localStorage.setItem('ideal_type_code', selectedType);
    
    // 다음 페이지로 이동 (내적 이상형 선택 페이지)
    location.href = '07-ideal-personality.html';
}