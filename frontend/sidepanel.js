const newsInput = document.getElementById('news-input');
const verifyBtn = document.getElementById('verify-btn');
const accuracyValue = document.getElementById('accuracy-value');
const statusText = document.getElementById('status-text');
const explanationText = document.getElementById('explanation-text');
const imageUpload = document.getElementById('image-upload');
let confidenceChart = null;
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "UPDATE_TEXT") {
        newsInput.value = message.data;
        sendResponse({ status: "OK" });
    }
    return true;
});
function renderConfidenceGraph(data) {
    const ctx = document.getElementById('claimGraph').getContext('2d');
    if (confidenceChart) {
        confidenceChart.destroy();
    }
    confidenceChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map((_, i) => `Claim ${i + 1}`),
            datasets: [{
                label: 'Confidence %',
                data: data
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });
}
verifyBtn.addEventListener('click', async () => {
    const text = newsInput.value.trim();
    if (!text) {
        alert("Enter or select news text!");
        return;
    }
    verifyBtn.innerText = "Analyzing...";
    verifyBtn.disabled = true;
    try {
        const res = await fetch("http://127.0.0.1:8000/verify-async", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text })
        });
        const { job_id } = await res.json();
        let result = null;
        while (true) {
            const r = await fetch(`http://127.0.0.1:8000/result/${job_id}`);
            const data = await r.json();
            if (data.status === "finished") {
                result = data.result;
                break;
            }
            if (data.status === "failed") {
                throw new Error("Processing failed");
            }
            await new Promise(r => setTimeout(r, 1000));
        }
        const score = result.truth_percentage;
        accuracyValue.innerText = `${score}%`;
        if (score >= 70) {
            accuracyValue.className = "status-true";
            statusText.innerText = "Credible News";
        } else if (score >= 40) {
            accuracyValue.className = "status-neutral";
            statusText.innerText = "Partially True / Misleading";
        } else {
            accuracyValue.className = "status-false";
            statusText.innerText = "Likely Misinformation";
        }
        explanationText.innerText = result.claims.map(c => `
• ${c.claim}
Status: ${c.status}
Confidence: ${c.confidence}%
Reason: ${c.reason}
Correct Fact: ${c.correct_fact}
Source: ${c.source}
        `).join("\n");
        const graphData = result.confidence_graph.map(c => c.confidence);
        renderConfidenceGraph(graphData);
    } catch (err) {
        console.error(err);
        statusText.innerText = "Error occurred";
    }
    verifyBtn.innerText = "Verify Facts";
    verifyBtn.disabled = false;
});
imageUpload.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    explanationText.innerText = "Processing image...";
    const formData = new FormData();
    formData.append("file", file);
    try {
        const res = await fetch("http://127.0.0.1:8000/verify-image", {
            method: "POST",
            body: formData
        });
        const data = await res.json();
        const score = data.analysis.truth_percentage;
        accuracyValue.innerText = `${score}%`;
        renderConfidenceGraph(
            data.analysis.confidence_graph.map(c => c.confidence)
        );
        explanationText.innerText =
            "Image Analysis:\n" +
            JSON.stringify(data.image_verification, null, 2);

    } catch {
        explanationText.innerText = "Image verification failed.";
    }
});