# 🔍 Smart Code Reviewer

> **Paste your Python code. Get instant, actionable feedback. Fix & improve.**

A sleek, dark-themed **Python static analysis tool** built with [Streamlit](https://streamlit.io/). It inspects your code for style violations, security risks, complexity issues, and best-practice suggestions — all in your browser, with zero setup beyond Python.

---

## ✨ Features

| Category | What it checks |
|---|---|
| 🔴 **Errors** | Syntax errors, mutable default arguments |
| ⚠️ **Warnings** | Long lines, tabs, wildcard imports, unused imports, bare `except`, shell injection risks, non-snake_case functions, non-PascalCase classes |
| ℹ️ **Info** | Trailing whitespace, excessive blank lines, `print()` statements |
| 💡 **Suggestions** | Missing docstrings, too many parameters, magic numbers, global variables |
| 🔒 **Security** | `eval()`, `exec()`, `os.system()`, `pickle`, `shell=True`, dynamic `__import__` |

### Additional Highlights
- 📊 **Quality Score** — 0–100 rating based on weighted issue counts  
- 📁 **File Upload** — Paste code or upload a `.py` file directly  
- 🎯 **Filter by Level** — View All / Errors / Warnings / Info / Suggestions  
- ⬇️ **Download Report** — Export a full `.txt` review report  
- ⚡ **Instant Analysis** — Pure static analysis using Python's `ast` module (no external linters needed)

---

## 📸 Preview

```
┌─────────────────────────────────────────────────┐
│          Smart Code Reviewer                    │
│    // paste your python · get instant feedback  │
├─────────┬───────────────────────────────────────┤
│  Score  │  📊 Review Summary                   │
│   72    │  ████░░░░  Errors      2              │
│  /100   │  ██████░░  Warnings    6              │
│ ⚠ Needs │  ██░░░░░░  Info        1              │
│  Work   │  ████░░░░  Suggestions 4              │
└─────────┴───────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8+**
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/smart-code-reviewer.git
cd smart-code-reviewer

# 2. (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 📦 Dependencies

```txt
streamlit
```

> All analysis is powered by Python's built-in `ast` and `re` modules — no external linters (pylint, flake8, etc.) are required.

Create a `requirements.txt` with:

```
streamlit>=1.30.0
```

---

## 🏗️ Project Structure

```
smart-code-reviewer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🧠 How It Works

The reviewer uses Python's built-in **`ast` (Abstract Syntax Tree)** module to parse and walk your code without executing it.

```
Your Code (str)
      │
      ▼
 ast.parse()  ──► SyntaxError? → Report immediately
      │
      ▼
 ast.walk()   ──► Visit every node (functions, classes, imports, calls…)
      │
      ▼
 re.search()  ──► Line-by-line regex checks (security patterns, whitespace…)
      │
      ▼
 Issue List   ──► Scored, sorted, and rendered as styled cards
```

### Scoring Formula

```
Score = 100
      − (Errors      × 20)
      − (Warnings    × 5)
      − (Info        × 1)
      − (Suggestions × 1)

Minimum score: 0
```

| Score | Label |
|---|---|
| 80 – 100 | ✔ Clean Code |
| 50 – 79  | ⚠ Needs Work |
| 0 – 49   | ✖ Poor Quality |

---

## 🔒 Security Checks Reference

| Pattern | Risk | Recommendation |
|---|---|---|
| `eval()` | Arbitrary code execution | Use `ast.literal_eval()` |
| `exec()` | Arbitrary code execution | Use explicit function calls |
| `os.system()` | Shell injection | Use `subprocess.run(shell=False)` |
| `pickle.load()` | Unsafe deserialization | Use JSON or safe serialization |
| `shell=True` | Shell injection via subprocess | Pass args as a list |
| `__import__()` | Dynamic import abuse | Use standard `import` statements |

---

## 🛠️ Customization

### Add your own checks

The `review_code()` function in `app.py` is modular. You can add new checks by:

1. **AST-based check** — Add a new `isinstance(node, ...)` branch inside the `ast.walk(tree)` loop.
2. **Regex-based check** — Append a tuple to `SECURITY_PATTERNS`:
   ```python
   (r'your_pattern', "Description of the risk.", "How to fix it.")
   ```

### Change severity weights

Update the `compute_score()` function:
```python
score = max(0, 100
            - counts["ERROR"]      * 20   # ← adjust multipliers
            - counts["WARNING"]    * 5
            - counts["INFO"]       * 1
            - counts["SUGGESTION"] * 1)
```

---

## 📄 Sample Report Output

```
==========================================================
  SMART CODE REVIEWER — Report
==========================================================
  Date    : 2026-04-26 15:00:00
  Lines   : 42
  Issues  : 7
  Score   : 72/100  (⚠ Needs Work)
----------------------------------------------------------
  [ERROR]   Line 14    Mutable default argument in 'process'.
             Fix: Use None as default and initialize inside function body.
  [WARNING] Line 3     Unused import 'os'.
             Fix: Remove 'import os' if not needed.
  [WARNING] Line 21    Security: eval() is dangerous — executes arbitrary code.
             Fix: Use ast.literal_eval() instead.
----------------------------------------------------------
  Errors: 1  Warnings: 2  Info: 1  Suggestions: 3
==========================================================
```

---

## 🤝 Contributing

Contributions are welcome! To add a new rule, improve the UI, or fix a bug:

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-new-check`
3. Commit your changes: `git commit -m "feat: add check for X"`
4. Push and open a Pull Request

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  Made with ❤️ and Python · Powered by Streamlit
</div>
