# ai-resume-screener
AI-powered resume screener: structured extraction, semantic matching, and hybrid scoring
---

## ✨ Features

- 📥 Upload a resume in **PDF or DOCX** format
- 🧠 Converts the resume into **structured JSON** using an LLM with a JSON schema
- 🎯 Extracts concrete, verifiable requirements from the job description (soft skills and employer benefits are excluded)
- 📊 **Hybrid scoring**: semantic matching by the LLM + deterministic overlap percentage + contextual adjustment
- 💡 Clear output: strengths, gaps, and a recommendation
- 🖥️ Simple web interface built with **Streamlit**

---

## 🔍 How It Works

```
Resume (PDF/DOCX)  ──►  Text extraction  ──►  Structured JSON (LLM)
                                                        │
Job description  ──►  Requirement extraction (LLM)      │
                                   │                    │
                                   └───────►  Semantic matching (LLM)
                                                        │
                                          Overlap % (computed in code)
                                                        │
                                       Contextual analysis (LLM)
                                                        │
                           Final score + strengths + gaps + recommendation
```

1. **Text extraction** with PyPDF2 and python-docx.
2. **Structured extraction**: the resume text becomes JSON (skills, experience, education, certifications).
3. **Requirement extraction**: only what the candidate must have, based on the job description.
4. **Semantic matching**: each requirement is classified as matched or missing, treating synonyms as equal (e.g. NLP = Natural Language Processing).
5. **Hybrid score**: the overlap percentage is calculated in code, then adjusted by the LLM using context to produce the final score.

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Language | Python |
| Interface | Streamlit |
| LLM | Groq API (`openai/gpt-oss-120b`) via the OpenAI-compatible SDK |
| Document parsing | PyPDF2, python-docx |
| Reliability | tenacity (retry on transient API errors) |

---

## 📁 Project Structure

```
ai-resume-screener/
├── app.py              # Streamlit interface
├── extractor.py        # Resume text extraction + structured JSON
├── comparator.py       # Requirement extraction, matching, scoring
├── llm.py              # LLM client and JSON generation with retries
├── requirements.txt
└── README.md
```

---

## 🚀 Run Locally

**1. Download the project**

Click the green **Code** button at the top of this page, choose **Download ZIP**, and extract it.
Then open a terminal inside the extracted folder.

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set your Groq API key** (free key from [console.groq.com](https://console.groq.com/keys))

Windows (PowerShell):
```powershell
$env:GROQ_API_KEY="your_key_here"
```

macOS / Linux:
```bash
export GROQ_API_KEY="your_key_here"
```

**4. Start the app**
```bash
streamlit run app.py
```

---

## 🖼️ Examples

### 🏦 Graduate banking program
![Banking program example]
<img width="2500" height="1303" alt="bank-program1" src="https://github.com/user-attachments/assets/0ab34211-401d-430b-a2de-a2b71e85dc10" />
<img width="2503" height="1208" alt="bank-program2" src="https://github.com/user-attachments/assets/7a009ace-c9d6-4fc3-b936-01d1c990f498" />
<img width="2522" height="785" alt="bank-program3" src="https://github.com/user-attachments/assets/80008b57-7762-48a2-b3fe-774d336014c6" />

### 🧾 Accounting role (outside the candidate's background)
![Accounting role example]
<img width="2529" height="1304" alt="accounting-role1" src="https://github.com/user-attachments/assets/f8a5f608-6677-4360-90e5-27925debee3e" />
<img width="2518" height="1204" alt="accounting-role2" src="https://github.com/user-attachments/assets/4fc8704d-c589-481d-ad33-73ee07cbbfd9" />
<img width="2507" height="1175" alt="accounting-role3" src="https://github.com/user-attachments/assets/cba31d93-cb1a-42ea-9e38-2fafa665e7ec" />

---

## ⚠️ Limitations

- Scores can vary slightly between runs because requirement extraction and matching use an LLM.
- Abstract requirements (e.g. "strategic thinking") may be matched generously; concrete, tool-based requirements are matched more reliably.
- Scanned (image-based) PDFs are not supported.
- Uses a free-tier API, so heavy use may hit rate limits.
- Built as a decision-support demo, not an automated hiring tool.

---

## 🔮 Future Improvements

- Support multiple resumes and ranking between candidates
- OCR for scanned resumes
- Export the analysis as a PDF report

---

## 👩‍💻 Author

**Layal Al-Sharif**
B.Sc. in Artificial Intelligence, Umm Al-Qura University

🔗 📧 layalalsharef@gmail.com
