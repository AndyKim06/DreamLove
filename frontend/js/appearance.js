/* frontend/js/appearance.js */

let selectedAppearance = null;

function goBack() {
    window.history.back();
}

// [수정] 선택 시 바로 이동하게 변경
function selectOption(type) {
    selectedAppearance = type;
    localStorage.setItem('appearance_type', type);
    
    const defBtn = document.getElementById('opt-default');
    const custBtn = document.getElementById('opt-custom');
    
    defBtn.classList.remove('selected');
    custBtn.classList.remove('selected');
    
    if (type === 'default') {
        defBtn.classList.add('selected');
    } else {
        custBtn.classList.add('selected');
    }
}

// 핵심 수정 부분: async 함수로 변경
async function goNext() {
    if (!selectedAppearance) {
        alert("원하는 방식을 선택해주세요!");
        return;
    }

   // 1. 값 결정 (default -> false, custom -> true)
    const isCustom = (selectedAppearance === 'custom');
    const userId = localStorage.getItem("userId");

    const url = `http://localhost:8000/user/customIdeal?customIdeal=${isCustom}&userId=${userId}`;

    try {
        // 2. 서버에 PATCH 요청 전송
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                // 필요하다면 인증 토큰을 여기에 추가하세요
                // 'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        if (response.ok) {
            // 3. 성공 시 로컬 스토리지 저장 및 페이지 이동
            localStorage.setItem('appearance_type', selectedAppearance);

            if (selectedAppearance === 'default') {
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