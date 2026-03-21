console.log("Fact-Checker: Content Script is ACTIVE on this page.");
document.addEventListener('mouseup', () => {
    const selection = window.getSelection().toString().trim();
    if (selection.length > 0) {
        console.warn("DEBUG: Attempting to send text:", selection.substring(0, 20) + "...");
        chrome.runtime.sendMessage({
            action: "UPDATE_TEXT",
            data: selection
        }, (response) => {
            if (chrome.runtime.lastError) {
                console.error("DEBUG: Send failed. Is the Side Panel open?", chrome.runtime.lastError.message);
            } else {
                console.log("DEBUG: Text sent successfully!");
            }
        });
    }
});