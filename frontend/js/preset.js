/* frontend/js/preset.js */

let selectedType = null;

function goBack() {
    window.history.back();
}

function selectType(type) {
    selectedType = type; // 예: 'type1', 'type2'...
    
    // 1. 모든 윈도우 선택 해제
    document.querySelectorAll('.pixel-window').forEach(win => {
        win.classList.remove('selected');
    });
    
    // 2. 선택한 윈도우 활성화
    const index = type.replace('type', '');
    const targetWindow = document.querySelector(`.window-${index}`);
    
    if (targetWindow) {
        targetWindow.classList.add('selected');
    }
}

async function goNext() {
    if (!selectedType) {
        alert("원하는 이상형 스타일을 선택해주세요!");
        return;
    }
    
    // [수정] 'type4'에서 '4'만 추출하여 숫자로 변환
    const idealTypeNumber = parseInt(selectedType.replace('type', ''));
    const url = `http://localhost:8000/user/idealType?idealType=${idealTypeNumber}`;

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
                // 필요 시 토큰 추가: 'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            // 성공 시 로컬스토리지에는 원본 코드를 저장하거나 숫자만 저장 (선택)
            localStorage.setItem('ideal_type_code', idealTypeNumber);
            location.href = '07-ideal-personality.html';
        } else {
            alert("서버 저장에 실패했습니다.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("네트워크 통신 중 오류가 발생했습니다.");
    }
}