console.log("✅ select-type.js loaded");

let selectedRefId = null;
let myGender = "girl";
let idealGender = "boy";

/* ===============================
   초기화
================================ */
window.onload = function () {
    const rawGender = localStorage.getItem("user_gender");

    myGender = rawGender === "여자" ? "girl" : "boy";
    idealGender = myGender === "girl" ? "boy" : "girl";

    console.log("🙋 내 성별 =", myGender);
    console.log("💖 이상형 성별 =", idealGender);

    updateSkinColor(document.getElementById("skin-slider").value);
    loadReferenceImages();
};

/* ===============================
   네비
================================ */
function goBack() {
    history.back();
}

/* ===============================
   레퍼런스
================================ */
function loadReferenceImages() {
    const windows = document.querySelectorAll(".preview-win");

    windows.forEach((win, i) => {
        win.querySelector(".window-body").innerHTML = `
            <img src="assets/images/ref_${idealGender}_${i + 1}.png"
                 style="width:100%;height:100%;object-fit:cover;">
        `;
        win.onclick = () => selectReference(i + 1);
    });
}

function selectReference(id) {
    selectedRefId = id;
    document.querySelectorAll(".preview-win")
        .forEach(w => w.classList.remove("selected"));
    document.getElementById(`win-${id}`).classList.add("selected");
}

/* ===============================
   피부톤
================================ */
function updateSkinColor(val) {
    document.getElementById("skin-preview-box").style.background =
        `hsl(28, 70%, ${95 - val * 0.5}%)`;
}

/* ===============================
   생성 (비동기 트리거)
================================ */
function generateIdeal() {
    if (!selectedRefId) {
        alert("레퍼런스를 선택해주세요");
        return;
    }

    const animalMap = {
        girl: { 1: "puppy", 2: "cat", 3: "rabbit", 4: "deer" },
        boy:  { 1: "puppy", 2: "fox", 3: "dinosaur", 4: "bear" }
    };

    const animal = animalMap[idealGender][selectedRefId];

    const body = {
        animal_type: animal,
        eyelid: document.querySelector("input[name=eyelid]:checked").value,
        faceShape: document.getElementById("face-shape").value,
        hair: document.getElementById("hair-style").value,
        clothe: document.getElementById("clothe").value,
        makeup: document.getElementById("makeup").value,
        skin: Number(document.getElementById("skin-slider").value)
    };

    const userId = localStorage.getItem("userId");

    console.log("📦 imageGen request =", body);

    // 🔥 결과 기다리지 않고 요청만 보냄
    fetch(`http://localhost:8000/imageGen/idealImage?userId=${userId}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body)
    }).catch(err => {
        console.error("❌ imageGen request error", err);
    });

    // ✅ 즉시 다음 페이지로 이동
    location.href = "06-custom-result.html";
}
