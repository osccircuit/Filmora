// Обновление данных на карте в реальном времени
document.getElementById('cardNumber').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\s+/g, '');
    if (value.length > 0) {
        value = value.match(/.{1,4}/g).join(' ');
    }
    e.target.value = value;
    document.getElementById('displayCardNumber').textContent = value || '•••• •••• •••• ••••';
});

document.getElementById('cardName').addEventListener('input', function(e) {
    document.getElementById('displayCardName').textContent = e.target.value.toUpperCase() || 'FULL NAME';
});

document.getElementById('expiryDate').addEventListener('input', function(e) {
    let value = e.target.value.replace(/\D/g, '');
    if (value.length >= 3) {
        value = value.slice(0, 2) + '/' + value.slice(2, 4);
    }
    e.target.value = value;
    document.getElementById('displayExpiry').textContent = value || 'MM/YY';
});

document.getElementById('cvv').addEventListener('input', function(e) {
    document.getElementById('displayCvv').textContent = e.target.value.replace(/./g, '•') || '•••';
});

// Функция "оплаты"
function processPayment() {
    alert('Оплата прошла успешно!\n(Это тестовая форма, платеж не выполнен)');
}