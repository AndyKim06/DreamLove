console.log("✅ select-type.js loaded");

let selectedRefId = null;
let currentGender = "girl";

/* ===============================
   초기화
================================ */
window.onload = function () {
    // 성별 정규화 ⭐⭐⭐ 핵심
    const rawGender = localStorage.getItem("user_gender");
    currentGender =
        rawGender === "male" ? "boy" :
        rawGender === "female" ? "girl" :
        rawGender || "girl";

    console.log("gender =", currentGender);

    // 피부톤 미리보기
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
    const targetGender = currentGender === "girl" ? "boy" : "girl";
    const windows = document.querySelectorAll(".preview-win");

    windows.forEach((win, i) => {
        win.querySelector(".window-body").innerHTML = `
            <img src="assets/images/ref_${targetGender}_${i + 1}.png"
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
        `hsl(28,70%,${95 - val * 0.5}%)`;
}

/* ===============================
   생성
================================ */
function generateIdeal() {
    console.log("🔥 generateIdeal called");

    if (!selectedRefId) {
        alert("레퍼런스를 선택해주세요");
        return;
    }

    const animalMap = {
        girl: { 1: "puppy", 2: "cat", 3: "rabbit", 4: "deer" },
        boy:  { 1: "puppy", 2: "fox", 3: "dinosaur", 4: "bear" }
    };

    const animal = animalMap[currentGender]?.[selectedRefId];
    if (!animal) {
        alert("성별 정보 오류");
        return;
    }

    const body = {
        animal_type: animal,
        eyelid: document.querySelector("input[name=eyelid]:checked").value,
        faceShape: document.getElementById("face-shape").value,
        hair: document.getElementById("hair-style").value,
        clothe: document.getElementById("clothe-style").value,
        makeup: document.getElementById("makeup-style").value,
        skin: Number(document.getElementById("skin-slider").value)
    };
    
    console.log("📦 request body", body);

    fetch("http://localhost:8000/imageGen/idealImage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify(body)
    })
    .then(res => {
        console.log("📡 status", res.status);
    })
    .catch(err => console.error(err));

    // 바로 이동
    location.href = "06-custom-result.html";
}
