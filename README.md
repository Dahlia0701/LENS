# 🛡️ LENS: Local Expert News Sentinel

**LENS (Local Expert News Sentinel)** is a privacy-focused, multi-modal fact-checking system designed to assist users in identifying misinformation in both vernacular and mainstream news content.

Unlike traditional fact-checking tools that require manual searching, LENS operates as a **Chrome Extension**, enabling real-time analysis of selected text and images directly within the browser. It combines Natural Language Processing (NLP) and Computer Vision techniques to provide structured insights into claims, credibility, and supporting evidence.

---

## ✨ Key Features

### 🔍 Multi-Modal Verification
LENS analyzes both textual and visual content:
- **Text Analysis**: Uses semantic similarity via Sentence-Transformers to compare extracted claims against a curated fact dataset.
- **OCR Integration**: Extracts text from screenshots and images using Tesseract OCR for verification.
- **Image–Text Alignment**: Uses OpenAI CLIP to evaluate whether an image contextually matches the associated text.
- **High-Speed News Classification**: Optimized backend capable of processing up to 1000 requests per minute using efficient threading.

### 📊 Real-Time Analytics
- **Truth Accuracy Score**: Percentage of claims matching known facts.
- **Claim Confidence Graph**: Visual representation of confidence per claim (Chart.min.js).
- **Contextual Reasoning**: Explains results based on semantic similarity levels.

### ⚙️ System Design Highlights
- **Browser-Based Workflow**: Chrome Extension (Manifest V3) with side-panel UI.
- **Threaded Execution**: Optimized for high-throughput without the need for external message brokers like Redis.
- **Semantic Matching Pipeline**: Claim extraction → embedding → similarity comparison → scoring.
- **Domain-Based Credibility Scoring**: Heuristic scoring based on URL patterns: **.gov**, **.edu** → higher credibility and **news**, **blog**, others → moderate to lower credibility

---

## 🧠 How It Works (Pipeline)

```
Browser Extension
              ↓
Text Selection / Image Upload
              ↓
  ┌───────────┴───────────┐
  ↓                       ↓
OCR Extraction    CLIP Image-Text Alignment
  ↓                       ↓
Claim Extraction ← (Extracted Text)
          ↓
Embedding Generation (Sentence Transformers)
          ↓
Semantic Similarity Matching (vs fact_db.csv)
          ↓
Fact Verification & Truth Calculation
          ↓
Explanation + Confidence Graph
```
---

## 🧰 Tech Stack

### 🖥️ Frontend
- Chrome Extension (Manifest V3)
- HTML5, CSS3 
- JavaScript
- Chart.js

### ⚙️ Backend
- FastAPI (Python)
- Pydantic (Data Validation)
- Shutil & OS (File Handling)
- Threading (High-performance task execution)
  
### 🤖 AI / ML
- Sentence-Transformers (All-MiniLM-L6-v2)
- PyTorch / TorchVision
- OpenAI CLIP (ViT-B/32)
- Pytesseract (OCR)
  
---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure the following are installed on your system:
* Python 3.10+
* Tesseract OCR (required for image text extraction)
> [!NOTE]
> If Tesseract is not detected, you may need to add it to your system PATH.

### 2. Backend Setup
Clone the repository and install dependencies:
```bash
git clone https://github.com/YourUsername/LENS.git
cd LENS

pip install fastapi uvicorn torch torchvision transformers sentence-transformers pandas pytesseract python-multipart
```
> [!IMPORTANT]
> LENS uses CLIP and Sentence-Transformers. The first run will automatically download the necessary model weights.

### 3. Running the System
Start the FastAPI server:
```bash
uvicorn main:app --reload
```

### 4. Chrome Extension Setup
To see the "LENS" side-panel in your browser:
- Open Chrome and go to:
```
chrome://extensions/
```
2. Enable Developer Mode (top right)
3. Click Load Unpacked
3. Select the **frontend/** folder
4. Pin the LENS extension to your toolbar

---

## 💡 How to Use

### 🔹 Text Verification
1. Highlight text on any webpage
2. It appears in the side panel
3. Click “Verify Facts”
   
### 🔹 Image Verification
1. Upload screenshot via 📸 button
2. OCR extracts text → verification pipeline runs
   
### 🔹 Output
- Truth Accuracy Score
- Claim-wise explanations
- Confidence graph

---

## 📂 Project Structure

```text
LENS/
├── backend/
│   ├── image_verify.py
│   ├── ocr.py
│   ├── pipeline.py
│   ├── task.py
│   └── vector_db.py
├── frontend/
│   ├── icons/
│   ├── background.js
│   ├── chart.min.js
│   ├── content.js
│   ├── manifest.json
│   ├── sidepanel.html
|   ├── sidepanel.css
│   └── sidepanel.js
├── fact.csv
└── main.py
```
---

## ⚠️ Limitations & Future Scope

- **Data Scope**: Currently utilizes a static fact.csv. Future versions aim to integrate live fact-checking APIs.
- **Multilingual Support**: Expanding NLP support for regional/vernacular languages.
- **Advanced Credibility**: Transitioning from domain heuristics to ML-based source credibility models.

---

## 🤝 Contribution: 

Contributions and suggestions are welcome,  do the following steps: 
- Fork repository
- Create feature branch
- Submit pull request

--- 





















  
