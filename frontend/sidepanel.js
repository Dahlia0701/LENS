const newsInput = document.getElementById('news-input');
const verifyBtn = document.getElementById('verify-btn');
const accuracyValue = document.getElementById('accuracy-value');
const statusText = document.getElementById('status-text');
const explanationText = document.getElementById('explanation-text');
const imageUpload = document.getElementById('image-upload');
let confidenceChart = null; 
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "UPDATE_TEXT") {
        newsInput.scrollTop = 0;
        newsInput.value = message.data;
        newsInput.style.borderColor = "#414B9E"; 
        setTimeout(() => { newsInput.style.borderColor = "#9792CB"; }, 200);
        sendResponse({ status: "Text received in Side Panel" });
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
                data: data,
                backgroundColor: '#414B9E',
                borderRadius: 8
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
    const textToVerify = newsInput.value.trim();
    if (!textToVerify) {
        alert("Please highlight or type news text first!");
        return;
    }
    verifyBtn.innerText = "Sending to AI Pipeline...";
    verifyBtn.disabled = true;
    try {
        const response = await fetch("http://127.0.0.1:8000/verify-async", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: textToVerify })
        });
        const data = await response.json();
        const jobId = data.job_id;
        verifyBtn.innerText = "Processing...";
        let result = null;
        while (true) {
            const res = await fetch(`http://127.0.0.1:8000/result/${jobId}`);
            const jobData = await res.json();
            if (jobData.status === "finished") {
                result = jobData.result;
                break;
            }
            await new Promise(r => setTimeout(r, 1000)); 
        }
        const score = result.truth_percentage;
        accuracyValue.innerText = `${score}%`;
        if (score > 50) {
            accuracyValue.className = 'status-true';
            statusText.innerText = "Verified Credible News";
        } else {
            accuracyValue.className = 'status-false';
            statusText.innerText = "Misinformation Alert!";
        }
        explanationText.innerText =
            result.claims.map(c =>
                `• ${c.claim}\n→ ${c.reason}`
            ).join("\n\n");
        const graphData = result.confidence_graph.map(c => c.confidence * 100);
        renderConfidenceGraph(graphData);
        verifyBtn.innerText = "Verify Facts";
        verifyBtn.disabled = false;
    } catch (error) {
        console.error(error);
        verifyBtn.innerText = "Error - Try Again";
        verifyBtn.disabled = false;
    }
});
imageUpload.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    explanationText.innerText = "Processing image with OCR + AI...";
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
            data.analysis.confidence_graph.map(c => c.confidence * 100)
        );
        explanationText.innerText =
            "Image Analysis:\n" +
            JSON.stringify(data.image_verification, null, 2);
    } catch (err) {
        explanationText.innerText = "Image processing failed.";
    }
});