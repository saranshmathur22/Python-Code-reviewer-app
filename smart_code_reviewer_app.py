import streamlit as st
import ast
import re
import os
from datetime import datetime
from collections import defaultdict

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Code Reviewer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)
if 'code_changed' not in st.session_state:
    st.session_state.code_changed = False

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1530 50%, #0a0e1a 100%) !important;
}

/* Hide Streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Main container */
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* Hero header */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
    position: relative;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #60a5fa, #a78bfa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1rem;
    color: #64748b;
    margin-top: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
}

/* Textarea */
.stTextArea textarea {
    background: #0f1629 !important;
    border: 1.5px solid #1e2d4a !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82rem !important;
    line-height: 1.6 !important;
    padding: 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59,130,246,0.15) !important;
}

/* File uploader */
[data-testid="stFileUploader"] {
    background: #0f1629 !important;
    border: 1.5px dashed #1e2d4a !important;
    border-radius: 12px !important;
    padding: 1.5rem !important;
}
[data-testid="stFileUploader"] label { color: #94a3b8 !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.7rem 2.5rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    letter-spacing: 0.03em;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(59,130,246,0.35) !important;
}

/* Score card */
.score-card {
    background: linear-gradient(135deg, #0f1629, #1a2744);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    border: 1px solid #1e2d4a;
    position: relative;
    overflow: hidden;
}
.score-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(59,130,246,0.06) 0%, transparent 60%);
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
}
.score-label {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.4rem;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* Stat pills */
.stats-row {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 1.2rem;
}
.stat-pill {
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
}

/* Issue card */
.issue-card {
    background: #0f1629;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    border-left: 4px solid;
    display: flex;
    align-items: flex-start;
    gap: 0.8rem;
    transition: transform 0.15s;
}
.issue-card:hover { transform: translateX(4px); }

.issue-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 2px; }
.issue-body { flex: 1; }
.issue-level {
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.1rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.25rem;
}
.issue-line {
    font-size: 0.72rem;
    color: #475569;
    font-family: 'JetBrains Mono', monospace;
    float: right;
}
.issue-msg {
    font-size: 0.88rem;
    color: #cbd5e1;
    margin-top: 0.15rem;
    line-height: 1.5;
}
.issue-fix {
    margin-top: 0.4rem;
    font-size: 0.8rem;
    color: #34d399;
    font-family: 'JetBrains Mono', monospace;
    background: rgba(52,211,153,0.07);
    padding: 0.3rem 0.6rem;
    border-radius: 6px;
}

/* Section label */
.sec-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.6rem;
    margin-top: 1.4rem;
}

/* Clean code banner */
.clean-banner {
    background: linear-gradient(135deg, rgba(52,211,153,0.1), rgba(16,185,129,0.05));
    border: 1px solid rgba(52,211,153,0.25);
    border-radius: 16px;
    padding: 2.5rem;
    text-align: center;
    font-family: 'Syne', sans-serif;
}
.clean-banner h2 { color: #34d399; font-size: 1.8rem; }
.clean-banner p  { color: #64748b; margin-top: 0.4rem; }

/* Tabs */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: #0f1629 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #1e2d4a !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border-radius: 8px !important;
    border: none !important;
}
[data-testid="stTabs"] [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6) !important;
    color: white !important;
}

/* Labels & text */
label, .stMarkdown p { color: #94a3b8 !important; font-family: 'Syne', sans-serif !important; }
h1,h2,h3 { color: #e2e8f0 !important; font-family: 'Syne', sans-serif !important; }
</style>
""", unsafe_allow_html=True)


# ── Core Reviewer Logic ───────────────────────────────────────────────────────
SECURITY_PATTERNS = [
    (r'\beval\s*\(',       "eval() is dangerous — executes arbitrary code.",           "Use ast.literal_eval() instead."),
    (r'\bexec\s*\(',       "exec() is a security risk.",                               "Use specific function calls instead."),
    (r'os\.system\s*\(',  "os.system() is unsafe for shell commands.",                "Use subprocess.run() with shell=False."),
    (r'pickle\.loads?\s*\(',"pickle is insecure with untrusted data.",                "Use JSON or safe serialization."),
    (r'shell\s*=\s*True',  "subprocess with shell=True is a shell injection risk.",   "Use shell=False and pass args as a list."),
    (r'__import__\s*\(',   "Dynamic __import__() can be dangerous.",                  "Use standard import statements."),
]

class Issue:
    def __init__(self, level, line, message, fix=None):
        self.level   = level
        self.line    = line
        self.message = message
        self.fix     = fix

def review_code(source):
    issues = []
    lines  = source.splitlines()
    tree   = None

    # Syntax check
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        issues.append(Issue("ERROR", e.lineno, f"Syntax Error — {e.msg}",
                            "Fix the syntax error before running further checks."))
        return issues, lines

    # Line length
    for i, line in enumerate(lines, 1):
        if len(line) > 79:
            issues.append(Issue("WARNING", i, f"Line too long ({len(line)} chars, max 79).",
                                "Break using backslash or parentheses."))

    # Trailing whitespace
    for i, line in enumerate(lines, 1):
        if line != line.rstrip():
            issues.append(Issue("INFO", i, "Trailing whitespace.", "Remove trailing spaces."))

    # Tabs
    for i, line in enumerate(lines, 1):
        if "\t" in line:
            issues.append(Issue("WARNING", i, "Tab used for indentation (use 4 spaces per PEP 8).",
                                "Replace tabs with 4 spaces."))

    # Blank lines
    blank = 0
    for i, line in enumerate(lines, 1):
        if line.strip() == "":
            blank += 1
            if blank == 3:
                issues.append(Issue("INFO", i, "3+ consecutive blank lines (PEP 8 max: 2).",
                                    "Reduce to at most 2 consecutive blank lines."))
        else:
            blank = 0

    # Imports
    imported = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.asname or alias.name.split(".")[0]
                imported[name] = node.lineno
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    issues.append(Issue("WARNING", node.lineno,
                                        f"Wildcard import 'from {node.module} import *'.",
                                        "Import only specific names you need."))
                else:
                    name = alias.asname or alias.name
                    imported[name] = node.lineno

    src_no_imp = re.sub(r'^\s*(import|from)\s+.*', '', source, flags=re.MULTILINE)
    for name, lineno in imported.items():
        if not re.search(r'\b' + re.escape(name) + r'\b', src_no_imp):
            issues.append(Issue("WARNING", lineno, f"Unused import '{name}'.",
                                f"Remove 'import {name}' if not needed."))

    # Functions & classes
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Docstring
            if not (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                issues.append(Issue("SUGGESTION", node.lineno,
                                    f"Function '{node.name}' has no docstring.",
                                    f'Add: """Brief description."""'))
            # snake_case
            if not re.match(r'^[a-z_][a-z0-9_]*$', node.name):
                issues.append(Issue("WARNING", node.lineno,
                                    f"Function '{node.name}' is not snake_case.",
                                    f"Rename to snake_case format."))
            # Complexity
            branches = sum(1 for n in ast.walk(node)
                           if isinstance(n, (ast.If, ast.For, ast.While,
                                             ast.ExceptHandler, ast.With)))
            if branches > 10:
                issues.append(Issue("WARNING", node.lineno,
                                    f"Function '{node.name}' is too complex (branches ≈ {branches}).",
                                    "Break into smaller helper functions."))
            # Too many args
            total_args = len(node.args.args) + len(node.args.kwonlyargs)
            if total_args > 6:
                issues.append(Issue("SUGGESTION", node.lineno,
                                    f"Function '{node.name}' has {total_args} parameters (>6).",
                                    "Group params into a config object or dataclass."))
            # Mutable defaults
            for default in node.args.defaults:
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    issues.append(Issue("ERROR", node.lineno,
                                        f"Mutable default argument in '{node.name}'.",
                                        "Use None as default and initialize inside function body."))

        if isinstance(node, ast.ClassDef):
            if not re.match(r'^[A-Z][a-zA-Z0-9]*$', node.name):
                issues.append(Issue("WARNING", node.lineno,
                                    f"Class '{node.name}' is not PascalCase.",
                                    "Rename to PascalCase format."))
            if not (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)):
                issues.append(Issue("SUGGESTION", node.lineno,
                                    f"Class '{node.name}' has no docstring.",
                                    "Add a class-level docstring."))

        if isinstance(node, ast.ExceptHandler) and node.type is None:
            issues.append(Issue("WARNING", node.lineno,
                                "Bare 'except:' catches everything including SystemExit.",
                                "Use 'except Exception as e:' instead."))

        if isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                issues.append(Issue("WARNING", node.lineno,
                                    "Empty except block — silently swallowing exceptions.",
                                    "At minimum: logging.exception(e)."))

        if isinstance(node, ast.Global):
            issues.append(Issue("SUGGESTION", node.lineno,
                                f"Global variable(s): {', '.join(node.names)}.",
                                "Avoid globals — pass as args or use class state."))

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id == "print":
                issues.append(Issue("INFO", node.lineno,
                                    "print() found — use logging in production.",
                                    "import logging; logging.info('msg')"))

        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            if node.value not in (0, 1, -1, True, False):
                issues.append(Issue("SUGGESTION", getattr(node, 'lineno', None),
                                    f"Magic number {node.value}.",
                                    f"Define as a named constant: MY_VALUE = {node.value}"))

    # Security
    for pattern, msg, fix in SECURITY_PATTERNS:
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                issues.append(Issue("WARNING", i, f"Security: {msg}", fix))

    issues.sort(key=lambda x: (x.line or 0,))
    return issues, lines


def compute_score(issues):
    counts = defaultdict(int)
    for iss in issues:
        counts[iss.level] += 1
    score = max(0, 100
                - counts["ERROR"]      * 20
                - counts["WARNING"]    * 5
                - counts["INFO"]       * 1
                - counts["SUGGESTION"] * 1)
    return score, counts


# ── UI Constants ──────────────────────────────────────────────────────────────
LEVEL_CONFIG = {
    "ERROR":      {"icon": "✖", "color": "#ef4444", "bg": "rgba(239,68,68,0.12)",  "badge_bg": "#7f1d1d"},
    "WARNING":    {"icon": "⚠", "color": "#f59e0b", "bg": "rgba(245,158,11,0.10)", "badge_bg": "#78350f"},
    "INFO":       {"icon": "ℹ", "color": "#3b82f6", "bg": "rgba(59,130,246,0.10)", "badge_bg": "#1e3a8a"},
    "SUGGESTION": {"icon": "💡","color": "#a78bfa", "bg": "rgba(167,139,250,0.10)","badge_bg": "#4c1d95"},
}

def render_issue(iss):
    cfg = LEVEL_CONFIG[iss.level]
    line_str = f"Line {iss.line}" if iss.line else ""
    fix_html = f'<div class="issue-fix">💚 Fix: {iss.fix}</div>' if iss.fix else ""
    return f"""
    <div class="issue-card" style="border-color:{cfg['color']};background:{cfg['bg']}">
        <div class="issue-icon">{cfg['icon']}</div>
        <div class="issue-body">
            <span class="issue-line">{line_str}</span>
            <span class="issue-level" style="background:{cfg['badge_bg']};color:{cfg['color']}">{iss.level}</span>
            <div class="issue-msg">{iss.message}</div>
            {fix_html}
        </div>
    </div>"""

def score_color(score):
    if score >= 80: return "#34d399"
    if score >= 50: return "#f59e0b"
    return "#ef4444"

def score_label(score):
    if score >= 80: return "✔ Clean Code"
    if score >= 50: return "⚠ Needs Work"
    return "✖ Poor Quality"


# ── App UI ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-title">Smart Code Reviewer</div>
    <div class="hero-sub">// paste your python · get instant feedback · fix & improve</div>
</div>
""", unsafe_allow_html=True)

# ── Input Section ─────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝  Paste Code", "📂  Upload .py File"])

source_code = ""

with tab1:
    source_code = st.text_area(
        "Your Python code",
        height=320,
        placeholder="# Paste your Python code here...\ndef my_function(x, y):\n    return x + y",
        label_visibility="collapsed"
    )

with tab2:
    uploaded = st.file_uploader("Upload a .py file", type=["py"], label_visibility="collapsed")
    if uploaded:
        source_code = uploaded.read().decode("utf-8")
        st.code(source_code, language="python")

st.markdown("<br>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    run = st.button("🔍  Review My Code", use_container_width=True)

# ── Results ───────────────────────────────────────────────────────────────────
if run:
    if not source_code.strip():
        st.warning("⚠ Please paste some Python code or upload a file first.")
    else:
        with st.spinner("Analysing your code..."):
            issues, lines = review_code(source_code)
            score, counts = compute_score(issues)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")

        # ── Score + Stats Row ──────────────────────────────────────────────
        col_score, col_stats = st.columns([1, 2], gap="large")

        with col_score:
            sc = score_color(score)
            sl = score_label(score)
            st.markdown(f"""
            <div class="score-card">
                <div class="score-number" style="color:{sc}">{score}</div>
                <div style="color:{sc};font-size:0.75rem;font-family:'JetBrains Mono',monospace;
                            font-weight:700;letter-spacing:0.12em;margin-top:0.3rem">/100</div>
                <div class="score-label">{sl}</div>
                <div class="stats-row">
                    <span class="stat-pill" style="background:rgba(239,68,68,0.15);color:#ef4444">
                        ✖ {counts['ERROR']} Errors</span>
                    <span class="stat-pill" style="background:rgba(245,158,11,0.15);color:#f59e0b">
                        ⚠ {counts['WARNING']} Warnings</span>
                    <span class="stat-pill" style="background:rgba(59,130,246,0.15);color:#60a5fa">
                        ℹ {counts['INFO']} Info</span>
                    <span class="stat-pill" style="background:rgba(167,139,250,0.15);color:#a78bfa">
                        💡 {counts['SUGGESTION']} Tips</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_stats:
            st.markdown(f"### 📊 Review Summary")
            st.markdown(f"**{len(lines)} lines** reviewed &nbsp;·&nbsp; **{len(issues)} issues** found &nbsp;·&nbsp; `{datetime.now().strftime('%H:%M:%S')}`")
            st.markdown("<br>", unsafe_allow_html=True)

            # Progress bar per level
            for level, label, color in [
                ("ERROR",      "Errors",      "#ef4444"),
                ("WARNING",    "Warnings",    "#f59e0b"),
                ("INFO",       "Info",        "#60a5fa"),
                ("SUGGESTION", "Suggestions", "#a78bfa"),
            ]:
                count = counts[level]
                pct   = min(count / max(len(issues), 1), 1.0)
                st.markdown(f"""
                <div style="margin-bottom:0.7rem">
                    <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                        <span style="font-size:0.8rem;color:#94a3b8;font-family:'JetBrains Mono',monospace">{label}</span>
                        <span style="font-size:0.8rem;color:{color};font-weight:700">{count}</span>
                    </div>
                    <div style="background:#1e2d4a;border-radius:999px;height:6px;overflow:hidden">
                        <div style="width:{pct*100:.1f}%;background:{color};height:100%;border-radius:999px;
                                    transition:width 0.6s ease"></div>
                    </div>
                </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Issues List ────────────────────────────────────────────────────
        if not issues:
            st.markdown("""
            <div class="clean-banner">
                <h2>✔ Perfect Code!</h2>
                <p>No issues found — your code is clean and well-written.</p>
            </div>""", unsafe_allow_html=True)
        else:
            # Filter tabs
            filter_options = ["All"] + [l for l in ["ERROR","WARNING","INFO","SUGGESTION"] if counts[l] > 0]
            sel = st.radio("Filter by level:", filter_options, horizontal=True, label_visibility="collapsed")

            filtered = issues if sel == "All" else [i for i in issues if i.level == sel]

            st.markdown(f'<div class="sec-label">Showing {len(filtered)} issue(s)</div>', unsafe_allow_html=True)

            for iss in filtered:
                st.markdown(render_issue(iss), unsafe_allow_html=True)

        # ── Download Report ────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        report_lines = [
            "=" * 58,
            "  SMART CODE REVIEWER — Report",
            "=" * 58,
            f"  Date    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Lines   : {len(lines)}",
            f"  Issues  : {len(issues)}",
            f"  Score   : {score}/100  ({score_label(score)})",
            "-" * 58,
        ]
        for iss in issues:
            line_str = f"Line {iss.line:<4}" if iss.line else "      "
            report_lines.append(f"  [{iss.level}]  {line_str}  {iss.message}")
            if iss.fix:
                report_lines.append(f"           Fix: {iss.fix}")
        report_lines += ["-" * 58,
                         f"  Errors: {counts['ERROR']}  Warnings: {counts['WARNING']}  "
                         f"Info: {counts['INFO']}  Suggestions: {counts['SUGGESTION']}",
                         "=" * 58]
        report_txt = "\n".join(report_lines)

        col_dl1, col_dl2, col_dl3 = st.columns([1, 2, 1])
        with col_dl2:
            st.download_button(
                label="⬇️  Download Report (.txt)",
                data=report_txt,
                file_name=f"code_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )