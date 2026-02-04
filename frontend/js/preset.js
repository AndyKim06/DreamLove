/* frontend/js/preset.js */

let selectedType = null;

// 페이지 로드 시 실행
window.onload = function() {
    renderPresetImages();
};

/**
 * 성별에 따른 이미지 렌더링 함수
 */
function renderPresetImages() {
    // 1. localStorage에서 성별 데이터 가져오기 및 디버깅 로그
    const gender = localStorage.getItem("user_gender"); 
    console.log("💾 로드된 성별 데이터:", gender);

    const imagePlaceholders = document.querySelectorAll('.image-placeholder');
    
    /**
     * [성별 판별 로직 개선]
     * 사용자가 'male' 혹은 '남자'인 경우 -> 'basic_girl'(여자) 프리셋 폴더 선택
     * 그 외의 경우(female, 여자 등) -> 'basic_boy'(남자) 프리셋 폴더 선택
     */
    let targetFolder;
    if (gender === "male" || gender === "남자") {
        targetFolder = "basic_girl"; 
    } else {
        targetFolder = "basic_boy"; 
    }

    console.log("📂 설정된 이미지 폴더명:", targetFolder);

    imagePlaceholders.forEach((placeholder, index) => {
        const imgNum = index + 1;
        const img = document.createElement('img');
        
        // 이미지 경로 설정: assets/images/basic/basic_girl_1.png 등
        img.src = `assets/images/basic/${targetFolder}_${imgNum}.png`;
        img.alt = `Type ${imgNum}`;
        
        // 이미지 스타일 설정
        img.style.width = '100%';
        img.style.height = '100%';
        img.style.objectFit = 'cover';

        // 기존 내용을 비우고 이미지 삽입
        placeholder.innerHTML = '';
        placeholder.appendChild(img);
    });
}

/**
 * 타입을 선택하는 함수 (선택만 하고 이동은 하지 않음)
 */
function selectType(type) {
    selectedType = type;
    
    // 1. 모든 윈도우 선택 해제 및 시각적 피드백 부여
    document.querySelectorAll('.pixel-window').forEach(win => {
        win.classList.remove('selected');
    });
    
    const index = type.replace('type', '');
    const targetWindow = document.querySelector(`.window-${index}`);
    if (targetWindow) {
        targetWindow.classList.add('selected');
    }
}

/**
 * 선택된 이상형 타입을 서버에 저장하고 페이지를 이동하는 함수
 */
async function goNext() {
    if (!selectedType) {
        alert("이상형 타입을 선택해주세요.");
        return;
    }
    
    const idealTypeNumber = parseInt(selectedType.replace('type', ''));
    const userId = localStorage.getItem("userId");
    
    const url = `http://localhost:8000/user/idealType?idealType=${idealTypeNumber}&userId=${userId}`;

    try {
        const response = await fetch(url, {
            method: 'PATCH',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            localStorage.setItem('ideal_type_code', idealTypeNumber);
            location.href = '07-ideal-personality.html'; // 다음 페이지 이동
        } else {
            console.error("서버 저장 실패");
            alert("저장에 실패했습니다. 다시 시도해주세요.");
        }
    } catch (error) {
        console.error("통신 오류:", error);
        alert("서버와 통신할 수 없습니다.");
    }
}

function goBack() {
    window.history.back();
}