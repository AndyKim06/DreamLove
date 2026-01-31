/* frontend/js/feedback.js */

/**
 * DreamLove 최종 피드백 페이지 JavaScript
 * - 백엔드에서 받은 결과 데이터를 표시
 * - 성공/실패 UI 전환
 * - 공유 및 재시작 기능
 */

let resultData = {
    score: 0,
    feedback: '',
    negativeFeedbacks: [],
    couplePhotoUrl: ''
};

/**
 * 페이지 로드 시 초기화
 */
window.onload = function() {
    // localStorage에서 결과 데이터 로드
    const savedResult = localStorage.getItem('chat_result');
    
    if (!savedResult) {
        console.warn('결과 데이터를 찾을 수 없습니다. 테스트 모드로 실행합니다.');
        // 테스트용 기본 데이터 (개발 시 사용)
        resultData = {
            score: -10,
            feedback: '너무 딱딱한 말투와\n섬세한 상대에게 차갑게\n대한 이유로 그를 갖지\n못하게 되었습니다..',
            negativeFeedbacks: [],
            couplePhotoUrl: ''
        };
        displayResult();
        return;
    }
    
    try {
        resultData = JSON.parse(savedResult);
        console.log('결과 데이터 로드 성공:', resultData);
        displayResult();
    } catch (error) {
        console.error('데이터 파싱 오류:', error);
        alert('결과 데이터를 불러올 수 없습니다.');
        location.href = '01-profile.html';
    }
};

/**
 * 결과에 따라 적절한 UI 표시
 */
function displayResult() {
    const score = resultData.score || 0;
    
    console.log('최종 점수:', score);
    
    if (score > 0) {
        // 성공 UI 표시
        showSuccessView();
    } else {
        // 실패 UI 표시
        showFailView();
    }
}

/**
 * 성공 화면 표시 (점수 > 0)
 */
function showSuccessView() {
    // UI 전환
    document.getElementById('success-view').classList.remove('hidden');
    document.getElementById('fail-view').classList.add('hidden');
    
    // 커플 사진 설정
    const couplePhoto = document.getElementById('couple-photo');
    if (couplePhoto) {
        if (resultData.couplePhotoUrl) {
            couplePhoto.src = resultData.couplePhotoUrl;
        } else {
            // 기본 이미지 유지
            couplePhoto.src = 'assets/images/feedback/mask-group-7.png';
        }
    }
    
    console.log('성공 화면 표시 완료');
}

/**
 * 실패 화면 표시 (점수 <= 0)
 */
function showFailView() {
    // UI 전환
    document.getElementById('success-view').classList.add('hidden');
    document.getElementById('fail-view').classList.remove('hidden');
    
    // 피드백 텍스트 설정
    const feedbackText = document.getElementById('feedback-text');
    if (feedbackText) {
        // 백엔드에서 받은 피드백에서 간단한 요약만 추출
        let feedback = resultData.feedback || '아쉽게도 이번 데이트는\n잘 되지 않았어요.\n다시 도전해보세요!';
        
        // 이모티콘 제거
        feedback = removeEmojis(feedback);
        
        // 간단한 피드백만 추출 (첫 번째 단락 또는 "---" 이전 부분)
        let simpleFeedback = extractSimpleFeedback(feedback);
        
        // 마크다운 변환 후 줄바꿈을 <br>로 변환
        simpleFeedback = convertMarkdown(simpleFeedback);
        feedbackText.innerHTML = simpleFeedback.replace(/\n/g, '<br>');
        
        // 상세 피드백 저장
        resultData.detailFeedback = extractDetailFeedback(feedback);
    }
    
    console.log('실패 화면 표시 완료');
}

/**
 * 이모티콘 제거 함수
 */
function removeEmojis(text) {
    return text.replace(/(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/g, '');
}

/**
 * 마크다운을 HTML로 변환하는 함수
 * - **텍스트** -> <strong>텍스트</strong>
 * - ### 텍스트 -> <span class="md-heading">텍스트</span>
 * - -> (arrow) -> <span class="md-arrow">-></span>
 */
function convertMarkdown(text) {
    // **텍스트** -> <strong>텍스트</strong>
    text = text.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // ### 텍스트 (line start) -> <span class="md-heading">
    text = text.replace(/^### (.+)$/gm, '<span class="md-heading">$1</span>');
    text = text.replace(/\n### (.+)/g, '<br><span class="md-heading">$1</span>');
    
    // -> (arrow) -> <span class="md-arrow">
    text = text.replace(/->\s*/g, '<span class="md-arrow">➜ </span>');
    
    return text;
}

/**
 * 간단한 피드백 추출 (첫 문단 또는 "---" 이전 부분)
 */
function extractSimpleFeedback(feedback) {
    // "---" 구분자가 있으면 그 전 부분만
    if (feedback.includes('---')) {
        return feedback.split('---')[0].trim();
    }
    
    // "대화별 상세 피드백" 이전 부분만
    if (feedback.includes('대화별 상세 피드백')) {
        return feedback.split('대화별 상세 피드백')[0].trim();
    }
    
    // "Q." 이전 부분만 (상세 피드백 시작 전)
    if (feedback.includes('Q.')) {
        return feedback.split('Q.')[0].trim();
    }
    
    // 그렇지 않으면 전체 텍스트의 앞부분만 (300자 제한)
    if (feedback.length > 300) {
        return feedback.substring(0, 300) + '...';
    }
    
    return feedback;
}

/**
 * 상세 피드백 추출 ("---" 이후 또는 "Q." 부분부터)
 */
function extractDetailFeedback(feedback) {
    // "---" 구분자가 있으면 그 후 부분
    if (feedback.includes('---')) {
        const parts = feedback.split('---');
        if (parts.length > 1) {
            return parts.slice(1).join('---').trim();
        }
    }
    
    // "대화별 상세 피드백" 이후 부분
    if (feedback.includes('대화별 상세 피드백')) {
        const idx = feedback.indexOf('대화별 상세 피드백');
        return feedback.substring(idx).trim();
    }
    
    // "Q." 부터 시작하는 부분
    if (feedback.includes('Q.')) {
        const idx = feedback.indexOf('Q.');
        return feedback.substring(idx).trim();
    }
    
    return '';
}

/**
 * 상세 피드백 토글
 */
function toggleDetailFeedback() {
    const detailBox = document.getElementById('detail-feedback');
    const detailContent = document.getElementById('detail-feedback-content');
    const btn = document.getElementById('show-detail-btn');
    
    if (detailBox.classList.contains('hidden')) {
        // 상세 피드백 표시
        if (resultData.detailFeedback) {
            let detail = convertMarkdown(resultData.detailFeedback);
            detailContent.innerHTML = detail.replace(/\n/g, '<br>');
        } else {
            detailContent.innerHTML = '상세 피드백이 없습니다.';
        }
        detailBox.classList.remove('hidden');
        btn.innerText = '상세 피드백 닫기';
    } else {
        // 상세 피드백 숨기기
        detailBox.classList.add('hidden');
        btn.innerText = '📝 상세 피드백 보기';
    }
}

// 상세 피드백 토글 함수를 전역으로 노출
window.toggleDetailFeedback = toggleDetailFeedback;

/**
 * 사진 다운로드 (QR 코드 모달 표시)
 */
function downloadPhoto() {
    const modal = document.getElementById('qr-modal');
    if (!modal) {
        console.error('QR 모달을 찾을 수 없습니다.');
        return;
    }
    
    modal.classList.remove('hidden');
    
    // QR 코드 생성
    const qrImg = document.getElementById('qr-code-img');
    if (qrImg) {
        const photoUrl = resultData.couplePhotoUrl || window.location.href;
        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(photoUrl)}`;
    }
    
    console.log('QR 모달 표시');
}

/**
 * QR 모달 닫기
 */
function closeQRModal() {
    const modal = document.getElementById('qr-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/**
 * 결과 공유하기
 */
function shareResult() {
    const score = resultData.score || 0;
    const shareText = `💕 DreamLove에서 데이트 시뮬레이션을 했어요!\n최종 점수: ${score}점\n${score > 0 ? '성공! 💖' : '아쉬워요.. 다시 도전! 💪'}`;
    
    // Web Share API 지원 확인
    if (navigator.share) {
        navigator.share({
            title: 'DreamLove 결과',
            text: shareText,
            url: window.location.origin
        }).then(() => {
            console.log('공유 성공');
        }).catch((err) => {
            console.log('공유 취소:', err);
        });
    } else {
        // Web Share API 미지원 시 클립보드 복사
        const fullText = shareText + '\n' + window.location.origin;
        
        navigator.clipboard.writeText(fullText)
            .then(() => {
                alert('📋 결과가 클립보드에 복사되었습니다!\n친구들과 공유해보세요.');
            })
            .catch((err) => {
                console.error('클립보드 복사 실패:', err);
                prompt('아래 텍스트를 복사해서 공유하세요:', fullText);
            });
    }
}

/**
 * 게임 재시작
 */
function restartGame() {
    if (confirm('처음부터 다시 시작하시겠습니까?')) {
        // localStorage 초기화
        localStorage.removeItem('chat_result');
        localStorage.removeItem('user_name');
        localStorage.removeItem('user_gender');
        localStorage.removeItem('user_concern');
        localStorage.removeItem('ideal_personality');
        
        // 프로필 페이지로 이동
        location.href = '01-profile.html';
    }
}

/**
 * 개발/테스트용: 콘솔에서 결과 시뮬레이션
 * 사용법: setTestResult(10) 또는 setTestResult(-5)
 */
function setTestResult(score) {
    const testData = {
        score: score,
        feedback: score > 0 
            ? '축하합니다! 멋진 데이트였어요!' 
            : '너무 딱딱한 말투와\n섬세한 상대에게 차갑게\n대한 이유로 그를 갖지\n못하게 되었습니다..',
        negativeFeedbacks: [],
        couplePhotoUrl: ''
    };
    
    localStorage.setItem('chat_result', JSON.stringify(testData));
    console.log('테스트 데이터 설정 완료. 새로고침하세요.');
    location.reload();
}

// 개발용 함수를 전역에 노출
window.setTestResult = setTestResult;
