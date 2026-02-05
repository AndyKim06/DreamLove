/* frontend/js/feedback.js */

let resultData = {
    score: 0,
    feedback: '',
    negativeFeedbacks: [],
    couplePhotoUrl: ''
};

// 상세 피드백 저장용 변수
let detailFeedback = '';

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
            : '**데이트 시뮬레이션 결과: 개선 필요** (점수: -10점)\n\n아쉬운 결과지만 괜찮아요! 다음에는 더 잘할 수 있을 거예요.\n\n---\n\n### **대화별 상세 피드백**\n\nQ. 운동할 때 어떤 기분이 제일 좋아요?\nA. 몰라요 [-5점]\n-> 좀 더 구체적으로 자신의 감정을 표현해보세요.\n\n### **실전 종합 팁**\n\n상대방에게 관심을 보이고, 질문에 성의있게 답변해보세요.',
        negativeFeedbacks: [],
        couplePhotoUrl: 'assets/images/feedback/mask-group-7.png' 
    };
}

/* 피드백을 요약/상세로 분리하는 함수 */
function parseFeedback(fullFeedback) {
    console.log('🔍 파싱 시작:', fullFeedback);
    
    // "대화별 상세 피드백" 을 기준으로 분리
    const detailPatterns = [
        '### **대화별 상세 피드백**',
        '### 대화별 상세 피드백',
        '**대화별 상세 피드백**',
        '대화별 상세 피드백'
    ];
    
    for (let pattern of detailPatterns) {
        const idx = fullFeedback.indexOf(pattern);
        if (idx > 0) {
            let summary = fullFeedback.substring(0, idx).trim();
            let detail = fullFeedback.substring(idx).trim();
            
            // 요약에서 "---" 구분자 제거
            summary = summary.replace(/---/g, '').trim();
            
            console.log('✂️ 분리 완료 - 요약:', summary);
            console.log('✂️ 분리 완료 - 상세:', detail);
            
            return { summary, detail };
        }
    }
    
    // 구분자가 없으면 전체를 요약으로
    console.log('⚠️ 구분자 없음, 전체를 요약으로 처리');
    return { summary: fullFeedback, detail: '' };
}

/* displayResult 함수 */
function displayResult() {
    const score = resultData.score || 0;
    const titleEl = document.getElementById('ending-title');
    const successContent = document.getElementById('success-content');
    const failContent = document.getElementById('fail-content');
    const couplePhoto = document.getElementById('couple-photo');
    const detailBtn = document.getElementById('detail-btn');
    const userId = localStorage.getItem('userId');
    const generatedCouplePhotoUrl = userId ? `imageCloud/user/${userId}_success_result.png` : '';

    if (score > 0) {
        // [성공 시]
        titleEl.innerHTML = "Love Ya !!<br>I like you .....";
        successContent.classList.remove('hidden');
        failContent.classList.add('hidden');
        if (detailBtn) {
            detailBtn.style.display = 'none';
        }

        if (couplePhoto) {
            couplePhoto.src = resultData.couplePhotoUrl || generatedCouplePhotoUrl;
            couplePhoto.style.display = 'block';
        }
    } else {
        // [실패 시] 
        titleEl.innerHTML = "Why you<br>are failed this game";
        
        successContent.classList.add('hidden');
        failContent.classList.remove('hidden');
        if (detailBtn) {
            detailBtn.style.display = 'inline-flex';
        }

        if (couplePhoto) {
            couplePhoto.src = ""; 
            couplePhoto.style.display = 'none'; 
        }

        const feedbackText = document.getElementById('feedback-text');
        if (feedbackText) {
            let fullFeedback = resultData.feedback || '아쉽게도 인연이 닿지 않았네요.';
            
            console.log('📝 원본 피드백:', fullFeedback);
            
            // 이모지 제거
            fullFeedback = removeEmojis(fullFeedback);
            
            // 피드백을 요약과 상세로 분리
            const { summary, detail } = parseFeedback(fullFeedback);
            
            console.log('📋 요약:', summary);
            console.log('📖 상세:', detail);
            
            // 요약 텍스트 정리
            let displaySummary = summary;
            
            // 1. 불필요한 텍스트 및 마크다운 잔재 제거
            displaySummary = displaySummary.replace(/간단한 요약 피드백/g, '');
            displaySummary = displaySummary.replace(/^\d+\.\s*/gm, ''); // "1. " 같은 숫자 목록 제거
            displaySummary = displaySummary.replace(/\*{4,}/g, '');     // "****" 같은 연속 별표 제거
            
            // 2. 점수 포맷 변환
            displaySummary = displaySummary.replace(/\*?\*?데이트 시뮬레이션 결과[:\s]*[^\(]*\(점수[:\s]*([+-]?\d+)점\)\*?\*?/g, '최종점수: $1점');
            
            // 3. 공백 및 줄바꿈 정리
            displaySummary = displaySummary.trim();
            
            // 3개 이상의 연속 줄바꿈을 2개로 축소
            displaySummary = displaySummary.replace(/\n\s*\n\s*\n+/g, '\n\n');
            
            // "최종점수: XX점" 바로 아래의 공백을 확실하게 조정 (한 줄 띄우기)
            displaySummary = displaySummary.replace(/(최종점수: [+-]?\d+점)\s*\n+/g, '$1\n\n');

            displaySummary = convertMarkdownSummary(displaySummary);
            feedbackText.innerHTML = displaySummary.replace(/\n/g, '<br>');
            
            // 상세 피드백 저장 (버튼 클릭 시 사용)
            detailFeedback = detail;
            
            // 상세 피드백이 있으면 버튼 표시, 없으면 숨김
            if (detailBtn) {
                if (detail && detail.length > 0) {
                    detailBtn.classList.remove('hidden');
                } else {
                    detailBtn.classList.add('hidden');
                }
            }
        }
    }
}

/* 상세 피드백 모달 열기 */
function showDetailFeedback() {
    const modal = document.getElementById('detail-modal');
    const contentEl = document.getElementById('detail-feedback-content');
    
    console.log('🔍 원본 상세 피드백:', detailFeedback);
    
    if (modal && contentEl) {
        let formattedDetail = convertMarkdownForDetail(detailFeedback);
        console.log('✨ 변환된 HTML:', formattedDetail);
        contentEl.innerHTML = formattedDetail;
        modal.classList.remove('hidden');
    }
}

/* 상세 피드백 모달 닫기 */
function closeDetailModal() {
    const modal = document.getElementById('detail-modal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

/* 게임 재시작 */
function restartGame() {
    // 로컬 스토리지의 게임 데이터 초기화 (필요한 경우)
    localStorage.removeItem('chat_result');
    // 필요한 다른 항목들도 초기화할 수 있음 (예: user_info 등은 유지할지 여부에 따라 결정)
    
    // 처음 화면으로 이동
    location.href = '00-onboarding.html';
}

function convertMarkdownSummary(text) {
    let result = text;
    // ### 헤더 처리 (요약에서는 기본 헤더만 적용)
    result = result.replace(/###\s*(.+)/g, '<h3>$1</h3>');
    // **볼드** 처리
    result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    // --- 구분선 처리
    result = result.replace(/^---+$/gm, '<hr>');
    return result;
}

function convertMarkdownDetail(text) {
    let result = text;
    
    // **볼드** 처리 (먼저 처리)
    result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // "Q." 또는 "Q. "로 시작하는 질문 찾기
    result = result.replace(/(?:^|\n)Q\.\s*([^\n]+)/g, '\n<div class="feedback-question"><span class="q-label">Q.</span> $1</div>');
    
    // "A." 또는 "A. "로 시작하는 답변 찾기 (점수 포함 가능)
    result = result.replace(/(?:^|\n)A\.\s*([^\n]+?)\s*(?:\[([+-]?\d+)점\])?(?=\n|$)/g, function(match, answer, score) {
        if (score) {
            const scoreClass = parseInt(score) < 0 ? 'negative' : 'positive';
            return `\n<div class="feedback-answer"><span class="a-label">A.</span> ${answer} <span class="score-badge ${scoreClass}">${score}점</span></div>`;
        }
        return `\n<div class="feedback-answer"><span class="a-label">A.</span> ${answer}</div>`;
    });
    
    // "->" 또는 "→" 로 시작하는 조언 찾기
    result = result.replace(/(?:^|\n)(?:->|→)\s*([^\n]+)/g, '\n<div class="feedback-advice"><span class="arrow">→</span> $1</div>');
    
    // --- 구분선 처리
    result = result.replace(/^---+$/gm, '<hr class="feedback-divider">');
    
    // ### 실전 종합 팁 섹션을 특별 박스로 처리
    result = result.replace(/#{2,3}\s*(?:<strong>)?실전 종합 팁(?:<\/strong>)?\s*([\s\S]*?)$/gm, function(match, content) {
        return `<div class="tip-box">
            <div class="tip-header"><span class="tip-icon">💡</span> 실전 종합 팁</div>
            <div class="tip-content">${content.trim()}</div>
        </div>`;
    });
    
    // ### 대화별 상세 피드백 헤더 처리
    result = result.replace(/#{2,3}\s*(?:<strong>)?대화별 상세 피드백(?:<\/strong>)?/g, '<h3 class="feedback-section-title">📝 대화별 상세 피드백</h3>');
    
    // 나머지 ### 헤더 처리
    result = result.replace(/#{2,3}\s*(.+)/g, '<h3 class="feedback-section-title">$1</h3>');
    
    // 연속된 Q, A, → 를 그룹으로 묶기
    result = groupFeedbackItems(result);
    
    return result;
}

// Q, A, → 아이템들을 그룹으로 묶는 함수
function groupFeedbackItems(html) {
    // 각 질문-답변-조언 블록을 feedback-item-group으로 감싸기
    let lines = html.split('\n');
    let result = [];
    let currentGroup = [];
    let inGroup = false;
    
    for (let line of lines) {
        const isQuestion = line.includes('feedback-question');
        const isAnswer = line.includes('feedback-answer');
        const isAdvice = line.includes('feedback-advice');
        const isHeader = line.includes('feedback-section-title');
        
        if (isQuestion) {
            // 이전 그룹이 있으면 닫기
            if (inGroup && currentGroup.length > 0) {
                result.push('<div class="feedback-item-group">');
                result.push(...currentGroup);
                result.push('</div>');
                currentGroup = [];
            }
            currentGroup.push(line);
            inGroup = true;
        } else if ((isAnswer || isAdvice) && inGroup) {
            currentGroup.push(line);
        } else {
            // 그룹 외의 요소
            if (inGroup && currentGroup.length > 0) {
                result.push('<div class="feedback-item-group">');
                result.push(...currentGroup);
                result.push('</div>');
                currentGroup = [];
                inGroup = false;
            }
            result.push(line);
        }
    }
    
    // 마지막 그룹 처리
    if (inGroup && currentGroup.length > 0) {
        result.push('<div class="feedback-item-group">');
        result.push(...currentGroup);
        result.push('</div>');
    }
    
    return result.join('\n');
}

function convertMarkdownForDetail(text) {
    // 텍스트 전처리: 줄바꿈이 없는 경우 Q., A., ->, ### 앞에 줄바꿈 추가
    let cleaned = text.trim();
    
    // Q. A. -> ### --- 앞에 줄바꿈 추가 (이미 줄바꿈이 있으면 중복 방지)
    cleaned = cleaned.replace(/(?<!\n)\s*(###\s)/g, '\n\n$1');
    cleaned = cleaned.replace(/(?<!\n)\s*(Q\.)\s/g, '\n$1 ');
    cleaned = cleaned.replace(/(?<!\n)\s*(A\.)\s/g, '\n$1 ');
    cleaned = cleaned.replace(/(?<!\n)\s*(->|→)\s/g, '\n$1 ');
    cleaned = cleaned.replace(/(?<!\n)\s*(---)/g, '\n$1');
    
    console.log('🔧 전처리된 텍스트:', cleaned);
    
    // 마크다운 변환 적용
    let result = convertMarkdownDetail(cleaned);
    
    // 빈 줄 정리 (연속 줄바꿈을 하나로)
    result = result.replace(/\n{3,}/g, '\n\n');
    
    // HTML 태그가 아닌 일반 텍스트 줄은 p 태그로 감싸기
    let lines = result.split('\n');
    let finalLines = [];
    
    for (let line of lines) {
        let trimmed = line.trim();
        if (trimmed === '') continue;
        
        // 이미 HTML 태그로 감싸져 있으면 그대로
        if (trimmed.startsWith('<')) {
            finalLines.push(trimmed);
        } else {
            // 일반 텍스트는 p 태그로 감싸기
            finalLines.push('<p class="feedback-paragraph">' + trimmed + '</p>');
        }
    }
    
    return finalLines.join('');
}

function removeEmojis(text) {
    return text.replace(/(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/g, '');
}

window.viewSuccess = () => { setTestData(10); displayResult(); };
window.viewFail = () => { setTestData(-10); displayResult(); };