const BACKEND_URL = "http://localhost:8000";
const userId = localStorage.getItem("userId");
const statusText = document.getElementById("status-text");
const spinner = document.getElementById("loading-spinner");

window.onload = function() {
    if (!userId) {
        console.error("userId가 로컬 스토리지에 없습니다.");
        statusText.innerText = "Error: User ID not found";
        return;
    }
    checkStatus();
};

// 1. 백엔드 상태 체크 (폴링)
async function checkStatus() {
    const pollInterval = setInterval(async () => {
        try {
            // 변경된 API 엔드포인트 사용
            const res = await fetch(`${BACKEND_URL}/user/checkImage?userId=${userId}`, {
                headers: { 'accept': 'application/json' }
            });
            
            const isReady = await res.json(); // 응답 자체가 true/false임

            // true일 때만 다음 단계로 진행
            if (res.ok && isReady === true) {
                console.log("이미지 생성 완료 확인!");
                clearInterval(pollInterval);
                processFlow(); 
            } else {
                console.log("대기 중... (생성 미완료)");
            }
        } catch (err) {
            console.error("상태 체크 중 오류 발생:", err);
        }
    }, 2000); // 2초 간격 유지
}

// 2. UI 전환 흐름 제어 (기존과 동일)
function processFlow() {
    if (spinner) spinner.style.display = "none"; // visibility 대신 display 추천
    
    statusText.innerText = "Complete!";
    statusText.classList.add("complete-color");
    
    setTimeout(() => {
        statusText.innerText = "Game start";
        statusText.classList.remove("complete-color");
        statusText.classList.add("start-color");

        setTimeout(() => {
            location.href = "08-game-start.html";
        }, 1000);
    }, 1500);
}