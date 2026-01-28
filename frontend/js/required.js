/* frontend/js/required.js */

function goBack() {
    window.history.back();
}

function goNext() {
    const worryInput = document.getElementById('user-worry');
    const worryText = worryInput.value.trim();
    
    // 유효성 검사
    if (!worryText) {
        alert("고민 내용을 입력해주세요!");
        worryInput.focus(); 
        return;
    }
    
    // 데이터 저장 (챗봇에서 concern으로 사용)
    localStorage.setItem('user_concern', worryText);
    localStorage.setItem('user_worry', worryText);
    
    // 다음 페이지 이동
    location.href = '03-appearance.html'; 
}