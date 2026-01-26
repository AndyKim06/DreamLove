/* frontend/js/feedback.js */

let resultData = {
    score: 0,
    feedback: '',
    negativeFeedbacks: [],
    couplePhotoUrl: ''
};

window.onload = function() {
    // localStorage에서 결과 데이터 로드
    const savedResult = localStorage.getItem('chat_result');
    
    if (!savedResult) {
        alert('결과 데이터를 찾을 수 없습니다.');
        location.href = '01-profile.html';
        return;
    }
    
    try {
        resultData = JSON.parse(savedResult);
        displayResult();
    } catch (error) {
        console.error('데이터 파싱 오류:', error);
        alert('결과 데이터를 불러올 수 없습니다.');
        location.href = '01-profile.html';
    }
};

// 결과 화면 표시
function displayResult() {
    const score = resultData.score || 0;
    const title = document.getElementById('result-title');
    const photoDate = document.getElementById('photo-date');
    
    // 날짜 설정
    if(photoDate) {
        const today = new Date();
        photoDate.innerText = today.toISOString().split('T')[0].replace(/-/g, '.');
    }

    if (score > 0) {
        // 성공
        title.innerText = "Love Ya !! I like you ......";
        showSuccessView();
        document.getElementById('btn-download').classList.remove('hidden');
    } else {
        // 실패
        title.innerText = "Why you are failed this game";
        showFailView();
        document.getElementById('btn-download').classList.add('hidden');
    }
}

// 성공 화면
function showSuccessView() {
    document.getElementById('success-content').classList.remove('hidden');
    document.getElementById('fail-content').classList.add('hidden');
    
    // 커플 사진
    const couplePhoto = document.getElementById('couple-photo');
    if (resultData.couplePhotoUrl) {
        couplePhoto.src = resultData.couplePhotoUrl;
    } else {
        couplePhoto.src = `https://picsum.photos/400/500?random=${Date.now()}`;
    }
}

// 실패 화면
function showFailView() {
    document.getElementById('success-content').classList.add('hidden');
    document.getElementById('fail-content').classList.remove('hidden');
    
    // 피드백 표시
    const feedbackText = document.getElementById('feedback-text');
    // 줄바꿈 처리 및 텍스트 설정
    feedbackText.innerText = resultData.feedback || 'AI가 당신의 대화에서 아쉬운 점을 찾지 못했습니다...\n하지만 왜 실패했을까요?';
}

// 하트 업데이트
function updateHearts(score) {
    const hearts = document.querySelectorAll('.pixel-heart');
    const heartCount = Math.max(0, Math.min(4, Math.floor(score / 10)));
    
    hearts.forEach((heart, index) => {
        if (index < heartCount) {
            heart.style.opacity = '1';
        } else {
            heart.style.opacity = '0.3';
        }
    });
}

// 사진 다운로드 (QR 코드 표시)
function downloadPhoto() {
    const modal = document.getElementById('qr-modal');
    modal.classList.remove('hidden');
    
    // QR 코드 생성 (목업 - 실제 사진 다운로드 URL로 대체 필요)
    const qrImg = document.getElementById('qr-code-img');
    const photoUrl = resultData.couplePhotoUrl || 'https://dreamlove.example.com/photo/download';
    qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(photoUrl)}`;
}

// QR 모달 닫기
function closeQRModal() {
    const modal = document.getElementById('qr-modal');
    modal.classList.add('hidden');
}

// 공유하기
function shareResult() {
    const shareText = `DreamLove에서 데이트 시뮬레이션을 했어요! 최종 점수: ${resultData.score}점 💕`;
    
    if (navigator.share) {
        navigator.share({
            title: 'DreamLove 결과',
            text: shareText,
            url: window.location.href
        }).catch(err => {
            console.log('공유 취소:', err);
        });
    } else {
        // 공유 API 미지원 시 클립보드 복사
        navigator.clipboard.writeText(shareText + '\n' + window.location.origin)
            .then(() => {
                alert('링크가 클립보드에 복사되었습니다! 친구들과 공유해보세요.');
            })
            .catch(err => {
                console.error('복사 실패:', err);
                alert('공유 기능을 사용할 수 없습니다.');
            });
    }
}

// 다시 시작
function restartGame() {
    if (confirm('처음부터 다시 시작하시겠습니까?')) {
        localStorage.clear();
        location.href = '01-profile.html';
    }
}
