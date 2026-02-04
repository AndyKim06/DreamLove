/* frontend/js/loading.js */

const BACKEND_URL = "http://localhost:8000";
const userId = localStorage.getItem("userId");
const statusText = document.getElementById("status-text");
const spinner = document.getElementById("loading-spinner");

window.onload = function() {
    checkStatus();
};

// 1. 백엔드 상태 체크 (폴링)
async function checkStatus() {
    const pollInterval = setInterval(async () => {
        try {
            const res = await fetch(`${BACKEND_URL}/imageGen/idealList?userId=${userId}`);
            const data = await res.json();

            // 이미지 생성이 완료되었는지 확인 (4개 이상)
            if (res.ok && data.images && data.images.length >= 4) {
                clearInterval(pollInterval);
                processFlow(); 
            }
        } catch (err) {
            console.error("체크 중 오류:", err);
        }
    }, 2000);
}

// 2. Wait -> Complete -> Game Start 흐름 제어
function processFlow() {
    // [단계 1] 생성 완료: 스피너 숨기고 텍스트 변경
    if (spinner) spinner.style.visibility = "hidden";
    statusText.innerText = "Complete!";
    statusText.classList.add("complete-color");
    
    // [단계 2] 1.5초 후 Game Start로 문구 변경
    setTimeout(() => {
        statusText.innerText = "Game start";
        statusText.classList.remove("complete-color");
        statusText.classList.add("start-color");

        // [단계 3] 1초 후 다음 페이지로 이동
        setTimeout(() => {
            location.href = "08-game-start.html";
        }, 1000);
    }, 1500);
}