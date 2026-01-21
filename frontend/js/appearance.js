/* frontend/js/appearance.js */

let selectedAppearance = null;

function goBack() {
    window.history.back();
}

function selectOption(type) {
    selectedAppearance = type;
    
    const defBtn = document.getElementById('opt-default');
    const custBtn = document.getElementById('opt-custom');
    
    // 초기화
    defBtn.classList.remove('selected');
    custBtn.classList.remove('selected');
    
    // 선택 표시
    if (type === 'default') {
        defBtn.classList.add('selected');
    } else {
        custBtn.classList.add('selected');
    }
}

function goNext() {
    if (!selectedAppearance) {
        alert("원하는 방식을 선택해주세요!");
        return;
    }
    
    localStorage.setItem('appearance_type', selectedAppearance);
    
    if (selectedAppearance === 'default') {
        location.href = '04-preset.html'; 
    } else {
        location.href = '05-select-type.html'; 
    }
}