/* frontend/js/custom-result.js */

let finalSelection = null;  // 사용자가 최종 선택한 번호 (1~4)
let isGenerated = false;    // 생성이 완료되었는지 여부

window.onload = function() {
    // 페이지 로드 후 3초 뒤에 결과 보여주기
    setTimeout(() => {
        revealResults();
    }, 3000);
};

// 뒤로가기 (유지)
function goBack() {
    window.history.back();
}

// 결과를 화면에 표시하는 함수
function revealResults() {
    const bodies = [
        document.getElementById('res-1'),
        document.getElementById('res-2'),
        document.getElementById('res-3'),
        document.getElementById('res-4')
    ];

    bodies.forEach((body, idx) => {
        // 랜덤 숫자를 사용하여 매번 다른 이미지가 뜨게 함
        const randomId = Math.floor(Math.random() * 1000) + idx;
        const imgUrl = `https://picsum.photos/300/300?random=${randomId}`; 
        
        // 이미지 태그 삽입
        body.innerHTML = `<img src="${imgUrl}" class="result-img" alt="Custom Result ${idx+1}">`;
    });
    
    isGenerated = true; // 생성 완료 플래그
    
    // 헤더 텍스트 변경
    const headerTitle = document.querySelector('.header-title');
    if(headerTitle) {
        headerTitle.innerText = "마음에 드는 이상형을 선택해주세요!";
    }
}

// [핵심 수정] 윈도우 클릭 시 선택 처리 + 바로 이동
function selectFinal(num) {
    // 생성이 안 끝났으면 선택 불가
    if (!isGenerated) return;

    finalSelection = num;

    // 1. UI 시각적 피드백 (선택된 박스 강조)
    document.querySelectorAll('.pixel-window').forEach(win => {
        win.classList.remove('selected');
    });
    const target = document.querySelector(`.window-${num}`);
    if (target) {
        target.classList.add('selected');
    }

    // 2. 선택한 이상형 정보 저장
    localStorage.setItem('final_custom_ideal_id', finalSelection);

    // 3. [페이지 바로 이동] 
    // 클릭 효과를 눈으로 확인할 수 있게 0.2초(200ms)만 기다렸다가 이동합니다.
    setTimeout(() => {
        location.href = '07-ideal-personality.html';
    }, 200);
}

// 화살표 버튼 클릭 시 (혹시 누를 경우를 대비해 경로 수정)
function goChat() {
    if (!finalSelection) {
        alert("가장 마음에 드는 이상형을 선택해주세요!");
        return;
    }
    
    localStorage.setItem('final_custom_ideal_id', finalSelection);
    location.href = '07-ideal-personality.html';
}