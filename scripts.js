document.getElementById('strategy-form').addEventListener('submit', function (e) {
    e.preventDefault();
    const symbol = document.getElementById('symbol').value;
    const quantity = document.getElementById('quantity').value;

    fetch('/trade', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol, quantity }),
    })
    .then(response => response.json())
    .then(data => {
        alert(`Trade Signal: ${data.signal === 1 ? 'BUY' : 'SELL'}\nResult: ${data.result}`);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
