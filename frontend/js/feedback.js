/* frontend/js/feedback.js */

let resultData = {
    score: 0,
    feedback: '',
    negativeFeedbacks: [],
    couplePhotoUrl: ''
};

window.onload = function() {
    const savedResult = localStorage.getItem('chat_result');
    
    if (savedResult) {
        try {
            resultData = JSON.parse(savedResult);
            console.log('✅ 데이터 연동 성공:', resultData);
        } catch (error) {
            console.error('데이터 파싱 오류:', error);
            setTestData(-10); 
        }
    } else {
        console.warn('⚠️ 데이터가 없어 테스트 모드로 실행합니다.');
        setTestData(10); 
    }
    displayResult();
};

function setTestData(score) {
    resultData = {
        score: score,
        feedback: score > 0 
            ? '축하합니다! 당신의 진심이 닿아\n이상형과 커플이 되었습니다.' 
            : '너무 딱딱한 말투와\n상대에게 차갑게 대한 이유로\n그를 갖지 못하게 되었습니다..',
        negativeFeedbacks: [],
        couplePhotoUrl: 'assets/images/feedback/mask-group-7.png' 
    };
}

/* displayResult 함수 내부 수정 */
function displayResult() {
    const score = resultData.score || 0;
    const titleEl = document.getElementById('ending-title');
    const successContent = document.getElementById('success-content');
    const failContent = document.getElementById('fail-content');
    const couplePhoto = document.getElementById('couple-photo');

    if (score > 0) {
        // [성공 시]
        titleEl.innerHTML = "Love Ya !!<br>I like you .....";
        successContent.classList.remove('hidden');
        failContent.classList.add('hidden');

        if (couplePhoto) {
            couplePhoto.src = resultData.couplePhotoUrl || 'assets/images/feedback/mask-group-7.png';
            couplePhoto.style.display = 'block'; // 성공 시 보임
        }
    } else {
        // [실패 시] 
        titleEl.innerHTML = "Why you<br>are failed this game";
        
        // 1. 성공 콘텐츠(사진 박스)를 확실히 숨김
        successContent.classList.add('hidden');
        // 2. 실패 콘텐츠(텍스트 박스)를 보여줌
        failContent.classList.remove('hidden');

        // 3. [핵심] 실패 시에는 이미지 객체 자체를 숨기고 src를 비움
        if (couplePhoto) {
            couplePhoto.src = ""; 
            couplePhoto.style.display = 'none'; 
        }

        const feedbackText = document.getElementById('feedback-text');
        if (feedbackText) {
            let fullFeedback = resultData.feedback || '아쉽게도 인연이 닿지 않았네요.';
            
            // 종합 결론 문구만 정교하게 추출
            // "데이트 시뮬레이션 결과:" 같은 문구부터 자르고 싶다면 아래처럼 수정
            let summary = fullFeedback.split(/1\.|Q\.|---|실전/)[0].trim();
            
            summary = removeEmojis(summary);
            feedbackText.innerHTML = summary.replace(/\n/g, '<br>');
        }
    }
}
function convertMarkdown(text) {
    return text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
}

function removeEmojis(text) {
    return text.replace(/(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/g, '');
}

window.viewSuccess = () => { setTestData(10); displayResult(); };
window.viewFail = () => { setTestData(-10); displayResult(); };