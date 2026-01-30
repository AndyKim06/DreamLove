/* frontend/js/custom-result.js */

let finalSelection = null;
let isGenerated = false;

const POLL_INTERVAL = 2000; 
let pollTimer = null;

// 백엔드 URL을 상수로 관리하여 경로 오류를 방지합니다.
const BACKEND_URL = "http://localhost:8000";

window.onload = function () {
    startPollingImages();
};

function goBack() {
    window.history.back();
}

/* ===============================
   이미지 폴링 (기존 코드 유지)
================================ */
function startPollingImages() {
    const userId = localStorage.getItem("userId");
    if (!userId) {
        console.error("userId 없음");
        return;
    }

    pollTimer = setInterval(async () => {
        try {
            const res = await fetch(`${BACKEND_URL}/imageGen/idealList?userId=${userId}`);

            if (!res.ok) return;

            const data = await res.json();

            if (!data.images || data.images.length < 4) {
                console.log("⏳ 이미지 아직 생성 중...");
                return;
            }

            renderImages(data.images);

            clearInterval(pollTimer);
            pollTimer = null;
            isGenerated = true;

            const headerTitle = document.querySelector(".header-title");
            if (headerTitle) {
                headerTitle.innerText = "마음에 드는 이상형을 선택해주세요!";
            }

        } catch (err) {
            console.error("폴링 에러:", err);
        }
    }, POLL_INTERVAL);
}

/* ===============================
   이미지 렌더링 (로컬 파일 경로 대응)
================================ */
function renderImages(images) {
    for (let i = 1; i <= 4; i++) {
        const container = document.getElementById(`res-${i}`);
        
        if (container && images[i - 1]) {
            // 1. 기존 'Generating...' 오버레이 제거
            container.innerHTML = ""; 

            // 2. 이미지 엘리먼트 생성
            const img = document.createElement("img");
            
            /**
             * 3. 경로 수정 핵심 
             * 응답이 "frontend/imageCloud/..."로 오는데, 
             * 현재 HTML(06-custom-result.html)이 이미 frontend 폴더 안에 있다면
             * 경로에서 "frontend/" 부분을 제거해줘야 브라우저가 올바른 위치를 찾습니다.
             */
            let rawPath = images[i - 1];
            let fixedPath = rawPath.startsWith("frontend/") 
                            ? rawPath.replace("frontend/", "") 
                            : rawPath;

            // 브라우저 보안 정책상 절대 경로보다는 상대 경로로 접근하게 합니다.
            img.src = fixedPath; 
            
            // 4. 스타일 및 속성 설정
            img.alt = `Result ${i}`;
            img.style.width = "100%";
            img.style.height = "100%";
            img.style.objectFit = "cover";
            img.style.display = "block";
            
            // 클릭 시 선택 기능 유지
            img.onclick = (e) => {
                e.stopPropagation(); // 부모 div 클릭 이벤트 중복 방지
                selectFinal(i);
            };
            
            // 5. 박스에 이미지 삽입
            container.appendChild(img);
            
            console.log(`이미지 렌더링 시도: ${img.src}`);
        }
    }
}
/* ===============================
   선택 (클래스 토글링)
================================ */
function selectFinal(num) {
    if (!isGenerated) return;

    finalSelection = num;

    // 모든 윈도우에서 selected 제거
    document.querySelectorAll(".pixel-window").forEach(win => {
        win.classList.remove("selected");
        win.style.border = "none"; // 기본 상태
    });

    // 선택된 윈도우 강조 (CSS selected 클래스가 없다면 인라인으로 추가)
    const target = document.querySelector(`.window-${num}`);
    if (target) {
        target.classList.add("selected");
        target.style.border = "3px solid #7a87f5"; // 선택 표시 예시
    }
}

/* ===============================
   다음 단계 (기존 코드 유지)
================================ */
async function goChat() {
    if (!finalSelection) {
        alert("가장 마음에 드는 이상형을 선택해주세요!");
        return;
    }

    const userId = localStorage.getItem("userId");
    const url = `${BACKEND_URL}/user/idealType?idealType=${finalSelection}&userId=${userId}`;

    try {
        const res = await fetch(url, { method: "PATCH" });

        if (!res.ok) {
            alert("선택 저장 실패");
            return;
        }

        localStorage.setItem("final_custom_ideal_id", finalSelection);
        location.href = "07-ideal-personality.html";

    } catch (err) {
        console.error(err);
        alert("서버 오류");
    }
}