/* frontend/js/custom-result.js */

let finalSelection = null;  // 사용자가 최종 선택한 번호 (1~4)
let isGenerated = false;    // 생성이 완료되었는지 여부

window.onload = function() {
    setTimeout(() => {
        revealResults();
    }, 3000);
};

function goBack() {
    window.history.back();
}

function revealResults() {
    const bodies = [
        document.getElementById('res-1'),
        document.getElementById('res-2'),
        document.getElementById('res-3'),
        document.getElementById('res-4')
    ];

    bodies.forEach((body, idx) => {
        const randomId = Math.floor(Math.random() * 1000) + idx;
        const imgUrl = `https://picsum.photos/300/300?random=${randomId}`; 
        body.innerHTML = `<img src="${imgUrl}" class="result-img" alt="Custom Result ${idx+1}">`;
    });
    
    isGenerated = true;
    
    const headerTitle = document.querySelector('.header-title');
    if(headerTitle) {
        headerTitle.innerText = "마음에 드는 이상형을 선택해주세요!";
    }
}

// 1. 이미지 클릭 시: 선택 표시만 함
function selectFinal(num) {
    if (!isGenerated) return;

    finalSelection = num; // 선택한 번호 저장

    // UI 시각적 피드백 (선택된 박스 강조)
    document.querySelectorAll('.pixel-window').forEach(win => {
        win.classList.remove('selected');
    });
    
    const target = document.querySelector(`.window-${num}`);
    if (target) {
        target.classList.add('selected');
    }
}

// 2. >> 버튼 클릭 시: 서버 전송 및 페이지 이동
async function goChat() {
    // 선택을 안 하고 버튼을 눌렀을 경우 체크
    if (!finalSelection) {
        alert("가장 마음에 드는 이상형을 선택해주세요!");
        return;
    }

    const idealTypeNumber = parseInt(finalSelection);
    const url = `http://localhost:8000/user/idealType?idealType=${idealTypeNumber}`;

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include' // 쿠키 전송을 위해 반드시 포함
        });

        if (response.ok) {
            localStorage.setItem('final_custom_ideal_id', finalSelection);
            location.href = '07-ideal-personality.html';
        } else {
            const errorData = await response.json().catch(() => ({}));
            console.error("Server Error:", errorData);
            alert("선택 저장에 실패했습니다. 다시 시도해주세요.");
        }
    } catch (error) {
        console.error("Network Error:", error);
        alert("서버와 통신할 수 없습니다.");
    }
}