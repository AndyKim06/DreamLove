/* frontend/js/required.js */

function goBack() {
    window.history.back();
}

async function goNext() {
    const worryInput = document.getElementById('user-worry');
    const worryText = worryInput.value.trim();

    // 유효성 검사
    if (!worryText) {
        alert("고민 내용을 입력해주세요!");
        worryInput.focus();
        return;
    }

    // 로컬 저장 (유지)
    localStorage.setItem('user_concern', worryText);
    localStorage.setItem('user_worry', worryText);

    try {
        const userId = localStorage.getItem("userId");

        const response = await fetch(
            `http://localhost:8000/user/concern?userId=${userId}`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    concern: worryText
                })
            }
        );

        if (response.ok) {
            const data = await response.json();
            // 서버에서 분석한 결과(장소 등)가 있으면 저장해둠 (선택사항)
            if (data.parsed_context) {
                console.log('분석된 정보:', data.parsed_context);
                localStorage.setItem('parsed_context', JSON.stringify(data.parsed_context));
            }
        }
        } catch (e) {
            console.error("서버 통신 오류 (백그라운드 처리하므로 진행은 계속함):", e);
        }

        // 성공 시 다음 페이지 이동
        location.href = "03-appearance.html";

    } catch (error) {
        console.error(error);
        alert("서버에 고민을 저장하는데 실패했어요 😥");
    }
}

