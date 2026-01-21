/* frontend/js/select-type.js */

let selectedRefId = null; // 선택된 레퍼런스 번호 (1~4)
let currentGender = 'girl'; 

window.onload = function() {
    // 1. 피부톤 초기화
    const slider = document.getElementById('skin-slider');
    if(slider) updateSkinColor(slider.value);

    // 2. 성별 정보 가져오기 (01페이지에서 저장됨)
    currentGender = localStorage.getItem('user_gender') || 'girl';

    // 3. 레퍼런스 이미지 로드
    loadReferenceImages();
};

function goBack() {
    window.history.back();
}

// [핵심] 성별에 맞는 레퍼런스 이미지 표시
function loadReferenceImages() {
    // 내가 여자면 -> 남자 사진, 남자면 -> 여자 사진
    const targetGender = currentGender === 'girl' ? 'boy' : 'girl';
    
    // 미리보기 윈도우 4개
    const windows = document.querySelectorAll('.preview-win');
    
    windows.forEach((win, index) => {
        const imgNum = index + 1; // 1 ~ 4
        const winBody = win.querySelector('.window-body');
        
        // 이미지 태그 삽입
        winBody.innerHTML = `
            <img src="assets/images/ref_${targetGender}_${imgNum}.png" 
                 class="ref-img" 
                 alt="Reference ${imgNum}"
                 style="width:100%; height:100%; object-fit:cover; pointer-events:none;">
        `;

        // 클릭 시 선택 처리
        win.onclick = function() {
            selectReference(imgNum);
        };
    });
}

// 레퍼런스 선택 (UI 업데이트)
function selectReference(id) {
    selectedRefId = id;

    // 모든 윈도우 선택 해제
    const allWindows = document.querySelectorAll('.preview-win');
    allWindows.forEach(win => win.classList.remove('selected'));

    // 클릭한 윈도우 강조
    // ID는 1부터 시작하므로 배열 인덱스는 id-1
    if(allWindows[id - 1]) {
        allWindows[id - 1].classList.add('selected');
    }
}

// 피부톤 색상 변경
function updateSkinColor(value) {
    const previewBox = document.getElementById('skin-preview-box');
    const lightness = 95 - (value * 0.5); 
    const color = `hsl(28, 70%, ${lightness}%)`;
    previewBox.style.backgroundColor = color;
}

// [수정됨] 생성하기 버튼 -> 데이터 저장 후 바로 페이지 이동
function generateIdeal() {
    // 1. 레퍼런스 선택 여부 확인
    if (!selectedRefId) {
        alert("왼쪽 창에서 원하는 스타일의 레퍼런스를 선택해주세요!");
        return;
    }

    // 2. DIY 데이터 수집
    const eyelids = document.querySelector('input[name="eyelid"]:checked').value;
    const nose = document.getElementById('nose-shape').value;
    const face = document.getElementById('face-shape').value;
    const atmosphere = document.getElementById('atmosphere').value;
    const hair = document.getElementById('hair-style').value;
    const skinValue = document.getElementById('skin-slider').value;
    
    // 3. 데이터 객체 생성
    const diyData = {
        targetGender: currentGender === 'girl' ? 'boy' : 'girl',
        referenceId: selectedRefId,
        features: { eyelids, nose, face, atmosphere, hair, skinTone: skinValue }
    };
    
    // 4. 로컬 스토리지에 저장 (다음 페이지나 API 전송용)
    localStorage.setItem('final_creation_data', JSON.stringify(diyData));
    
    // 5. [수정됨] 로딩 없이 바로 다음 페이지(06-custom-result.html)로 이동
    // 로딩과 결과 표시는 06페이지에서 진행됨
    location.href = '06-custom-result.html';
}

function goNext() {
    generateIdeal();
}