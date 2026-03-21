# 🛡️ LENS: Local Expert News Sentinel

**LENS (Local Expert News Sentinel)** is a privacy-focused, multi-modal fact-checking system designed to assist users in identifying misinformation in both vernacular and mainstream news content.

Unlike traditional fact-checking tools that require manual searching, LENS operates as a **Chrome Extension**, enabling real-time analysis of selected text and images directly within the browser. It combines Natural Language Processing (NLP) and Computer Vision techniques to provide structured insights into claims, credibility, and supporting evidence.

---

## ✨ Key Features

### 🔍 Multi-Modal Verification
LENS analyzes both textual and visual content:
- **Text Analysis**: Uses semantic similarity via Sentence-Transformers to compare extracted claims against a curated fact dataset.
- **OCR Integration**: Extracts text from screenshots and images using Tesseract OCR for verification.
- **Image–Text Alignment**: Uses CLIP to evaluate whether an image contextually matches the associated text.
- **Image Authenticity (Prototype)**: Uses a pretrained ResNet18 model for basic classification-based heuristics.
> [!NOTE]
> This is not a specialized deepfake detection model.

### 📊 Real-Time Analytics
- **Truth Accuracy Score**: Percentage of claims matching known facts.
- **Claim Confidence Graph**: Visual representation of confidence per claim (Chart.min.js).
- **Contextual Reasoning**: Explains results based on semantic similarity levels.

### ⚙️ System Design Highlights
- **Browser-Based Workflow**: Chrome Extension (Manifest V3) with side-panel UI.
- **Asynchronous Processing**: Redis + RQ used for background task execution.
- **Semantic Matching Pipeline**: Claim extraction → embedding → similarity comparison → scoring.
- **Domain-Based Credibility Scoring**: Heuristic scoring based on URL patterns **.gov**, **.edu** → higher credibility and **news**, **blog**, others → moderate to lower credibility
- **Vector Search Module (Experimental)**: FAISS-based similarity search implemented but not currently used in the main pipeline.

---

## 🧠 How It Works (Pipeline)

```
Browser Extension
        ↓
Text Selection / Image Upload
        ↓
OCR (if image input)
        ↓
Claim Extraction
        ↓
Embedding Generation (Sentence Transformers)
        ↓
Semantic Similarity Matching
        ↓
Fact Verification
        ↓
Truth Percentage Calculation
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
- Pydantic
  
### 🤖 AI / ML
- Sentence-Transformers
- PyTorch
- OpenAI CLIP
- ResNet18 (pretrained, prototype use)
  
### 🗄️ Data & Processing
- Pandas
- FAISS (experimental)
  
### ⚡ Task Queue
- Redis
- RQ (Redis Queue)

---

## 🚀 Installation & Setup

### 1. Prerequisites
Ensure the following are installed on your system:
* Python 3.10+
* Redis Server (running on localhost:6379)
* Tesseract OCR (required for image text extraction)
> [!NOTE]
> If Tesseract is not detected, you may need to add it to your system PATH.

### 2. Backend Setup
Clone the repository and install dependencies:
```bash
git clone https://github.com/YourUsername/LENS.git
cd LENS

pip install fastapi uvicorn torch torchvision transformers sentence-transformers pandas pytesseract redis rq faiss-cpu
```
> [!IMPORTANT]
> LENS uses large AI models (CLIP and Sentence-Transformers).
> The first run may take a few minutes as model weights are downloaded.

### 3. Running the System
Make sure Redis server is running, then start both services:

#### ▶️ Terminal 1 – Start Redis Worker
```bash
python worker.py
```

#### ▶️ Terminal 2 – Start FastAPI Server
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
│   ├── deepfake_detection.py
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
├── main.py
└── worker.py
```
---

## ⚠️ Limitations

- Uses a static fact dataset, not live fact-checking APIs
- Image authenticity detection is prototype-level only
- Credibility scoring is domain-based heuristic
- FAISS is not integrated into the main pipeline

---

## 🌱 Future Improvements

- Real-time fact-checking APIs
- Dedicated deepfake detection models
- Multilingual NLP support
- ML-based credibility scoring
- Full FAISS integration

--- 

## 🤝 Contribution: 

Contributions and suggestions are welcome,  do the following steps: 
- Fork repository
- Create feature branch
- Submit pull request

--- 





















  
