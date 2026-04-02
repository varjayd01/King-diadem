async function run() {
    const input = document.getElementById('cmd');
    const term = document.getElementById('term');
    const val = input.value;
    if(!val) return;

    term.innerHTML += `<div style="color:white;">> COMMAND: ${val}</div>`;
    input.value = '';

    try {
        const res = await fetch('/api/execute', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({prompt: val})
        });
        const data = await res.json();
        term.innerHTML += `<div>> [KERNEL]: ${data.message}</div>`;
    } catch (e) {
        term.innerHTML += `<div style="color:red;">> [ALERT]: API RATE LIMIT EXCEEDED!</div>`;
    }
    term.scrollTop = term.scrollHeight;
}
