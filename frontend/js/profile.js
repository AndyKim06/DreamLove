/* frontend/js/profile.js */

// 전역 변수
let userProfile = {
    name: '',
    gender: null,
    photo: null
};

// 1. 성별 선택
function selectGender(type) {
    userProfile.gender = type;

    const girlBtn = document.getElementById('btn-girl');
    const boyBtn = document.getElementById('btn-boy');

    girlBtn.classList.remove('selected');
    boyBtn.classList.remove('selected');

    if (type === 'girl') {
        girlBtn.classList.add('selected');
    } else {
        boyBtn.classList.add('selected');
    }
}

// 2. 파일 업로드 트리거
function triggerFileUpload() {
    document.getElementById('file-input').click();
}

// 3. 이미지 미리보기
function previewImage(event) {
    const file = event.target.files[0];
    if (!file) return;

    userProfile.photo = file;

    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('preview-img');
        preview.src = e.target.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

// 뒤로가기
function goBack() {
    window.history.back();
}

// ✅ 핵심: 서버로 전송
async function goNext() {
    const name = document.getElementById('username').value;

    // 유효성 검사
    if (!name) {
        alert("Please enter your name!");
        return;
    }
    if (!userProfile.gender) {
        alert("Please select your gender!");
        return;
    }

    // FormData 생성
    const formData = new FormData();
    formData.append("name", name);
    formData.append(
        "gender",
        userProfile.gender === "girl" ? "여자" : "남자"
    );

    if (userProfile.photo) {
        formData.append("image", userProfile.photo);
    }

    try {
        const res = await fetch("http://localhost:8000/user/info", {
            method: "POST",
            body: formData,
            credentials: "include" // ⭐ 쿠키 받기
        });

        if (!res.ok) {
            throw new Error("Server error");
        }

        location.href = "02-required-info.html";

    } catch (err) {
        console.error(err);
        alert("Failed to save profile 😢");
    }
}
