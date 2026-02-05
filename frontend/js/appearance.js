/* frontend/js/appearance.js */

function goBack() {
    window.history.back();
}

// 옵션을 클릭하자마자 실행되는 함수
async function selectOption(type) {
    const userId = localStorage.getItem("userId");
    const isCustom = (type === 'custom');

    // 1. 시각적 피드백 (선택된 버튼 강조)
    const defBtn = document.getElementById('opt-default');
    const custBtn = document.getElementById('opt-custom');
    
    defBtn.classList.remove('selected');
    custBtn.classList.remove('selected');
    
    if (type === 'default') {
        defBtn.classList.add('selected');
    } else {
        custBtn.classList.add('selected');
    }

    // 2. 서버 통신 시작 (goNext의 로직을 여기로 가져옴)
    const url = `http://localhost:8000/user/customIdeal?customIdeal=${isCustom}&userId=${userId}`;

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            // 3. 성공 시 로컬 스토리지 저장 및 즉시 페이지 이동
            localStorage.setItem('appearance_type', type);

            if (type === 'default') {
                location.href = '04-preset.html'; 
            } else {
                location.href = '05-select-type.html'; 
            }
        } else {
            alert("서버 업데이트에 실패했습니다. 다시 시도해주세요.");
        }
    } catch (error) {
        console.error("Error updating appearance:", error);
        alert("네트워크 오류가 발생했습니다.");
    }
}

