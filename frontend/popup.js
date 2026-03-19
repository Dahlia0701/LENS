document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("verifyBtn").addEventListener("click", verify);
    document.getElementById("imageVerifyBtn").addEventListener("click", verifyImage);
});
let chart;
function renderChart(data) {
    const ctx = document.getElementById("chart").getContext("2d");
    const labels = data.map(d => d.claim.substring(0, 20) + "...");
    const values = data.map(d => d.confidence);
    if (chart) chart.destroy();
    chart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Confidence",
                data: values
            }]
        }
    });
}
async function verify() {
    try {
        const text = document.getElementById("news").value;
        const response = await fetch("http://127.0.0.1:8000/verify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        document.getElementById("score").innerText =
            "Truth Score: " + data.truth_percentage + "%";
        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);
        renderChart(data.confidence_graph);
    } catch (error) {
        document.getElementById("output").innerText =
            "Error: " + error.message;
    }
}
async function verifyImage() {
    try {
        const file = document.getElementById("imageInput").files[0];
        if (!file) {
            alert("Select an image first");
            return;
        }
        const formData = new FormData();
        formData.append("file", file);
        const response = await fetch("http://127.0.0.1:8000/verify-image", {
            method: "POST",
            body: formData
        });
        const data = await response.json();
        document.getElementById("output").innerText =
            JSON.stringify(data, null, 2);
        document.getElementById("score").innerText =
            "Truth Score: " + data.analysis.truth_percentage + "%";
        renderChart(data.analysis.confidence_graph);
    } catch (error) {
        document.getElementById("output").innerText =
            "Error: " + error.message;
    }
}