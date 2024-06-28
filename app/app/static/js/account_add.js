document.getElementById('account-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const account_name = document.getElementById('account_name').value;
    const account_type = document.getElementById('account_type').value;
    
    if (account_name && account_type) {
        alert(`계좌명이 ${account_name}인 ${account_type} 계좌가 생성되었습니다`);
    } else {
        alert('모든 필드를 채워주세요.');
    }
});