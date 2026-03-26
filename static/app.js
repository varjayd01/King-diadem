const API_URL = "https://king-diadem.onrender.com/decision"; // ใส่ลิงก์พี่

async function send() {
    const input = document.getElementById("input").value;

    const res = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ input })
    });

    const data = await res.json();

    document.getElementById("output").innerText = data.result;
}
