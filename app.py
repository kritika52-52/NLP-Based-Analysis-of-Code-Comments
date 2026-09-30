import pandas as pd
import streamlit as st
from textwrap import dedent

from nlp_pipeline import CommentClassifier, extract_comments, preprocess


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="CodeSense AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# HTML HELPER
# Prevents Streamlit from displaying indented HTML as code.
# ============================================================

def render_html(html):
    st.markdown(dedent(html).strip(), unsafe_allow_html=True)


# ============================================================
# CUSTOM CSS
# ============================================================

render_html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg: #070a12;
    --panel: #0d1220;
    --panel2: #111827;
    --border: rgba(148,163,184,.14);
    --purple: #8b5cf6;
    --purple2: #a78bfa;
    --cyan: #22d3ee;
    --text: #f8fafc;
    --muted: #94a3b8;
    --muted2: #64748b;
}

.stApp {
    background:
        radial-gradient(circle at 8% 8%, rgba(124,58,237,.18), transparent 28%),
        radial-gradient(circle at 92% 12%, rgba(6,182,212,.10), transparent 25%),
        var(--bg);
    color: var(--text);
}

html, body, [class*="css"] {
    font-family: "Inter", sans-serif;
}

[data-testid="stSidebar"] {
    background: #070a12;
    border-right: 1px solid rgba(139,92,246,.18);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 34px 38px;
    margin: 8px 0 24px 0;
    border: 1px solid rgba(139,92,246,.28);
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(17,24,39,.96), rgba(8,12,23,.96));
    box-shadow: 0 20px 60px rgba(0,0,0,.35);
}

.hero:before {
    content: "";
    position: absolute;
    width: 280px;
    height: 280px;
    right: -110px;
    top: -150px;
    border-radius: 50%;
    background: rgba(139,92,246,.25);
    filter: blur(70px);
}

.hero:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    left: -120px;
    bottom: -150px;
    border-radius: 50%;
    background: rgba(34,211,238,.12);
    filter: blur(70px);
}

.hero-content {
    position: relative;
    z-index: 1;
}

.hero-kicker {
    color: var(--purple2);
    font-family: "JetBrains Mono", monospace;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.hero-title {
    margin: 0;
    font-size: 40px;
    line-height: 1.15;
    font-weight: 800;
    letter-spacing: -1.5px;
    background: linear-gradient(90deg, #fff, #c4b5fd, #67e8f9);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    margin-top: 10px;
    color: var(--muted);
    font-size: 14px;
    max-width: 760px;
}

.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
    padding: 14px;
    margin-bottom: 24px;
    border: 1px solid var(--border);
    border-radius: 16px;
    background: rgba(15,23,42,.55);
}

.pipeline-step {
    padding: 8px 13px;
    border-radius: 9px;
    border: 1px solid rgba(139,92,246,.28);
    background: rgba(124,58,237,.10);
    color: #c4b5fd;
    font: 600 11px "JetBrains Mono", monospace;
}

.pipeline-arrow {
    color: #475569;
}

.section-title {
    color: var(--text);
    font-size: 22px;
    font-weight: 750;
    margin-top: 5px;
}

.section-subtitle {
    color: var(--muted2);
    font-size: 13px;
    margin: 4px 0 18px 0;
}

.glass-card {
    padding: 20px;
    border-radius: 18px;
    border: 1px solid var(--border);
    background: linear-gradient(145deg, rgba(17,24,39,.92), rgba(9,13,24,.92));
    box-shadow: 0 12px 38px rgba(0,0,0,.20);
}

.metric-card {
    min-height: 108px;
    padding: 17px;
    border-radius: 16px;
    border: 1px solid rgba(139,92,246,.16);
    background: linear-gradient(145deg, rgba(17,24,39,.95), rgba(9,13,24,.95));
}

.metric-icon {
    font-size: 20px;
}

.metric-label {
    margin-top: 5px;
    color: var(--muted2);
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: .8px;
}

.metric-value {
    margin-top: 3px;
    color: #c4b5fd;
    font-size: 25px;
    font-weight: 800;
}

.code-header {
    display: flex;
    align-items: center;
    gap: 7px;
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-bottom: 0;
    border-radius: 12px 12px 0 0;
    background: #0b1020;
    color: var(--muted2);
    font: 12px "JetBrains Mono", monospace;
}

.code-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #475569;
}

.result-label {
    color: var(--cyan);
    font: 600 11px "JetBrains Mono", monospace;
    letter-spacing: 1px;
}

.result-value {
    margin: 6px 0 10px 0;
    color: white;
    font-size: 29px;
    font-weight: 800;
}

.badge {
    display: inline-block;
    padding: 5px 11px;
    border-radius: 999px;
    border: 1px solid rgba(34,211,238,.25);
    background: rgba(34,211,238,.08);
    color: #67e8f9;
    font: 11px "JetBrains Mono", monospace;
}

.sidebar-brand {
    text-align: center;
    padding: 5px 0 20px 0;
}

.sidebar-icon {
    font-size: 40px;
}

.sidebar-name {
    margin-top: 4px;
    color: white;
    font-size: 20px;
    font-weight: 800;
}

.sidebar-tag {
    margin-top: 4px;
    color: var(--muted2);
    font: 9px "JetBrains Mono", monospace;
    letter-spacing: 1px;
}

.footer {
    margin-top: 45px;
    padding: 22px 10px;
    border-top: 1px solid rgba(148,163,184,.08);
    text-align: center;
    color: #475569;
    font-size: 11px;
}

.footer-highlight {
    color: #8b5cf6;
}

.stButton > button {
    width: 100%;
    min-height: 44px;
    border-radius: 11px;
    border: 1px solid rgba(139,92,246,.45);
    background: linear-gradient(135deg, #7c3aed, #4f46e5);
    color: white;
    font-weight: 700;
    transition: .2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 10px 28px rgba(124,58,237,.30);
}

.stDownloadButton > button {
    width: 100%;
    border-radius: 11px;
    border: 1px solid rgba(34,211,238,.30);
    background: rgba(34,211,238,.08);
    color: #67e8f9;
    font-weight: 700;
}

[data-baseweb="textarea"] {
    border-radius: 12px !important;
    background: #0b1020 !important;
}

textarea {
    font-family: "JetBrains Mono", monospace !important;
}

[data-testid="stFileUploader"] {
    padding: 8px;
    border: 1px dashed rgba(139,92,246,.32);
    border-radius: 14px;
    background: rgba(15,23,42,.45);
}

div[data-testid="stMetric"] {
    background: rgba(17,24,39,.80);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px;
}

button[data-baseweb="tab"] {
    font-weight: 600;
}

@media (max-width: 768px) {
    .hero {
        padding: 25px;
    }

    .hero-title {
        font-size: 29px;
    }

    .pipeline {
        justify-content: flex-start;
    }
}
</style>
""")


# ============================================================
# MODEL
# ============================================================

@st.cache_resource
def get_model():
    return CommentClassifier()


try:
    clf = get_model()
    model_ready = True
except Exception as exc:
    clf = None
    model_ready = False
    st.error(f"Could not load the NLP model: {exc}")
    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    render_html("""
    <div class="sidebar-brand">
        <div class="sidebar-icon">🧠</div>
        <div class="sidebar-name">CodeSense AI</div>
        <div class="sidebar-tag">JAVA COMMENT INTELLIGENCE</div>
    </div>
    """)

    st.divider()

    st.markdown("### ⚡ System Status")
    st.success("NLP Engine Online")

    render_html("""
    <div class="glass-card">
        <div style="color:#64748b;font-size:10px;letter-spacing:1px;">
            NLP PIPELINE
        </div>
        <div style="color:#c4b5fd;font-family:'JetBrains Mono';font-size:12px;line-height:2;margin-top:8px;">
            ▸ Tokenization<br>
            ▸ Normalization<br>
            ▸ Stopword Removal<br>
            ▸ Stemming<br>
            ▸ Classification
        </div>
    </div>
    """)

    st.markdown("### 🛠 Technology")

    for item in [
        "Python",
        "Streamlit",
        "Natural Language Processing",
        "Machine Learning",
        "Java",
        "Pandas",
    ]:
        st.markdown(f"▸ {item}")


# ============================================================
# HERO
# ============================================================

render_html("""
<div class="hero">
    <div class="hero-content">
        <div class="hero-kicker">◈ CODESENSE / NLP ENGINE</div>
        <h1 class="hero-title">Java Comment Intelligence</h1>
        <div class="hero-subtitle">
            Analyze, preprocess and classify natural-language comments
            hidden inside Java source code.
        </div>
    </div>
</div>
""")

render_html("""
<div class="pipeline">
    <div class="pipeline-step">01 Tokenize</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">02 Normalize</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">03 Stopwords</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">04 Stem</div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">05 Classify</div>
</div>
""")


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🔎 Single Comment",
    "📂 Java Code Analyzer",
    "📊 Model Report",
])


# ============================================================
# TAB 1: SINGLE COMMENT
# ============================================================

with tab1:
    st.markdown("## Comment Analyzer")
    st.caption(
        "Enter a Java comment and inspect the complete NLP processing pipeline."
    )

    left, right = st.columns([1.25, .75], gap="large")

    with left:
        render_html("""
        <div class="code-header">
            <span class="code-dot"></span>
            <span class="code-dot"></span>
            <span class="code-dot"></span>
            <span style="margin-left:8px;">comment.java</span>
        </div>
        """)

        comment_text = st.text_area(
            "Comment",
            value="TODO: fix the NullPointerException in getUserName()",
            height=145,
            label_visibility="collapsed",
        )

    with right:
        render_html("""
        <div class="glass-card">
            <div style="color:#64748b;font-size:10px;letter-spacing:1px;">
                ANALYSIS ENGINE
            </div>
            <div style="font-size:17px;font-weight:700;margin-top:8px;">
                NLP-powered classification
            </div>
            <div style="color:#94a3b8;font-size:13px;line-height:1.7;margin-top:10px;">
                The comment is processed through tokenization,
                normalization, stopword removal, stemming and classification.
            </div>
        </div>
        """)

    analyze_single = st.button(
        "⚡ Analyze Comment",
        key="analyze_single",
        type="primary",
    )

    if analyze_single:
        if not comment_text.strip():
            st.warning("Please enter a comment.")
        else:
            try:
                steps = preprocess(comment_text, detail=True)
                label, probs = clf.predict(comment_text)

                # Support both dict and Series-like probability outputs.
                if hasattr(probs, "items"):
                    prob_dict = dict(probs.items())
                else:
                    prob_dict = dict(probs)

                confidence = float(prob_dict.get(label, 0.0))

                st.divider()

                m1, m2, m3, m4 = st.columns(4)

                metrics = [
                    ("🔤", "Tokens", len(steps["tokens"])),
                    ("🧹", "Clean Tokens", len(steps["no_stopwords"])),
                    ("🌱", "Stems", len(steps["stems"])),
                    ("🎯", "Confidence", f"{confidence:.1%}"),
                ]

                for column, (icon, name, value) in zip(
                    [m1, m2, m3, m4],
                    metrics,
                ):
                    with column:
                        render_html(f"""
                        <div class="metric-card">
                            <div class="metric-icon">{icon}</div>
                            <div class="metric-label">{name}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                        """)

                st.markdown("")

                result_col, probability_col = st.columns(
                    [.9, 1.1],
                    gap="large",
                )

                with result_col:
                    render_html(f"""
                    <div class="glass-card">
                        <div class="result-label">PREDICTED CLASS</div>
                        <div class="result-value">{label}</div>
                        <span class="badge">AI CLASSIFICATION</span>
                    </div>
                    """)

                    st.markdown("### 🧩 NLP Pipeline Output")

                    st.markdown("**Normalized Text**")
                    st.code(str(steps["normalized"]), language="text")

                    st.markdown("**Tokens**")
                    st.code(
                        "  ".join(map(str, steps["tokens"])),
                        language="text",
                    )

                    st.markdown("**After Stopword Removal**")
                    st.code(
                        "  ".join(map(str, steps["no_stopwords"])),
                        language="text",
                    )

                    st.markdown("**Stemmed Tokens**")
                    st.code(
                        "  ".join(map(str, steps["stems"])),
                        language="text",
                    )

                with probability_col:
                    render_html("""
                    <div class="glass-card">
                        <div style="font-size:18px;font-weight:700;">
                            📈 Class Probability
                        </div>
                        <div style="color:#64748b;font-size:12px;margin-top:5px;">
                            Model confidence across categories
                        </div>
                    </div>
                    """)

                    probability_df = pd.DataFrame(
                        {
                            "Class": list(prob_dict.keys()),
                            "Probability": [
                                float(v) for v in prob_dict.values()
                            ],
                        }
                    ).sort_values("Probability", ascending=True)

                    if not probability_df.empty:
                        st.bar_chart(
                            probability_df.set_index("Class"),
                            height=330,
                        )

            except Exception as exc:
                st.error(f"Analysis failed: {exc}")


# ============================================================
# TAB 2: JAVA CODE ANALYZER
# ============================================================

with tab2:
    st.markdown("## Java Source Analyzer")
    st.caption(
        "Upload Java source files or paste Java code to automatically "
        "extract and classify comments."
    )

    upload_col, paste_col = st.columns(2, gap="large")

    with upload_col:
        render_html("""
        <div class="glass-card">
            <div style="font-size:18px;font-weight:700;">
                📁 Upload Java Files
            </div>
            <div style="color:#64748b;font-size:12px;margin-top:5px;">
                Select one or multiple .java files.
            </div>
        </div>
        """)

        uploaded_files = st.file_uploader(
            "Upload Java files",
            type=["java"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

    with paste_col:
        render_html("""
        <div class="glass-card">
            <div style="font-size:18px;font-weight:700;">
                💻 Paste Java Code
            </div>
            <div style="color:#64748b;font-size:12px;margin-top:5px;">
                Analyze source code directly.
            </div>
        </div>
        """)

        java_code = st.text_area(
            "Java code",
            height=150,
            placeholder=(
                "// TODO: improve authentication\n\n"
                "public class User {\n"
                "    // Validate user input\n"
                "}"
            ),
            label_visibility="collapsed",
        )

    sources = {}

    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                sources[uploaded_file.name] = uploaded_file.read().decode(
                    "utf-8",
                    "ignore",
                )
            except Exception as exc:
                st.warning(
                    f"Could not read {uploaded_file.name}: {exc}"
                )

    if java_code.strip():
        sources["pasted.java"] = java_code

    analyze_java = st.button(
        "🚀 Run Java Comment Analysis",
        key="analyze_java",
        type="primary",
    )

    if analyze_java:
        if not sources:
            st.warning(
                "Please upload a Java file or paste Java code first."
            )
        else:
            rows = []
            progress = st.progress(0, text="Analyzing Java source...")

            source_items = list(sources.items())
            total = len(source_items)

            try:
                for file_index, (file_name, source) in enumerate(source_items):
                    comments = extract_comments(source)

                    for comment in comments:
                        text = comment.get("text", "")

                        if not str(text).strip():
                            continue

                        label, probs = clf.predict(text)

                        if hasattr(probs, "items"):
                            prob_dict = dict(probs.items())
                        else:
                            prob_dict = dict(probs)

                        confidence = float(prob_dict.get(label, 0.0))

                        rows.append({
                            "File": file_name,
                            "Line": comment.get("line", ""),
                            "Type": comment.get("type", ""),
                            "Comment": text,
                            "Stems": preprocess(text),
                            "Class": label,
                            "Confidence": round(confidence, 4),
                        })

                    progress.progress(
                        int(((file_index + 1) / total) * 100),
                        text=f"Processed {file_name}",
                    )

                progress.empty()

            except Exception as exc:
                progress.empty()
                st.error(f"Java analysis failed: {exc}")
                rows = []

            if rows:
                df = pd.DataFrame(rows)

                st.success(
                    f"✓ Analysis complete — {len(df)} comments detected."
                )

                total_comments = len(df)
                total_files = df["File"].nunique()
                avg_confidence = float(df["Confidence"].mean())
                class_count = df["Class"].nunique()

                m1, m2, m3, m4 = st.columns(4)

                metrics = [
                    ("💬", "Comments", total_comments),
                    ("📁", "Files", total_files),
                    ("🎯", "Avg Confidence", f"{avg_confidence:.1%}"),
                    ("🏷️", "Classes", class_count),
                ]

                for column, (icon, name, value) in zip(
                    [m1, m2, m3, m4],
                    metrics,
                ):
                    with column:
                        render_html(f"""
                        <div class="metric-card">
                            <div class="metric-icon">{icon}</div>
                            <div class="metric-label">{name}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                        """)

                st.markdown("")

                results_col, chart_col = st.columns(
                    [1.6, .7],
                    gap="large",
                )

                with results_col:
                    st.markdown("### 📋 Classification Results")
                    st.caption(
                        "Extracted comments and predicted categories."
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        height=420,
                        hide_index=True,
                    )

                with chart_col:
                    st.markdown("### 📊 Distribution")
                    st.caption("Predicted comment categories.")

                    class_counts = df["Class"].value_counts()

                    st.bar_chart(
                        class_counts,
                        height=300,
                    )

                    st.download_button(
                        "⬇️ Download CSV",
                        data=df.to_csv(index=False),
                        file_name="comments_analysis.csv",
                        mime="text/csv",
                    )

                st.divider()

                st.markdown("### 🔬 Comment Explorer")
                st.caption(
                    "Expand a comment to inspect its classification details."
                )

                for index, row in df.iterrows():
                    title = (
                        f"#{index + 1} • {row['File']} • "
                        f"Line {row['Line']} • {row['Class']}"
                    )

                    with st.expander(title):
                        st.code(
                            str(row["Comment"]),
                            language="java",
                        )

                        c1, c2, c3 = st.columns(3)

                        with c1:
                            st.metric(
                                "Comment Type",
                                str(row["Type"]),
                            )

                        with c2:
                            st.metric(
                                "Predicted Class",
                                str(row["Class"]),
                            )

                        with c3:
                            st.metric(
                                "Confidence",
                                f"{float(row['Confidence']):.1%}",
                            )

                        st.caption(
                            f"Stemmed representation: {row['Stems']}"
                        )

            else:
                st.warning(
                    "No comments were found in the provided Java source."
                )


# ============================================================
# TAB 3: MODEL REPORT
# ============================================================

with tab3:
    st.markdown("## Model Performance")
    st.caption(
        "Evaluation metrics for the built-in comment classification model."
    )

    try:
        report = clf.report
        report_df = pd.DataFrame(report).T.round(2)

        if not report_df.empty:
            metric_cols = st.columns(3)

            with metric_cols[0]:
                st.metric("🤖 Model", "NLP Classifier")

            with metric_cols[1]:
                st.metric("📚 Evaluation", "25% Hold-out")

            with metric_cols[2]:
                st.metric("🧠 Task", "Comment Classification")

            st.markdown("### 📊 Classification Report")

            st.dataframe(
                report_df,
                use_container_width=True,
                height=350,
            )

            st.info(
                "The model is evaluated on a 25% hold-out of the built-in "
                "seed dataset. Adding more labelled examples to dataset.py "
                "can improve generalization."
            )
        else:
            st.warning("The model report is empty.")

    except Exception as exc:
        st.error(f"Could not display the model report: {exc}")


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
    <div>
        <span class="footer-highlight">◈ CodeSense AI</span>
        &nbsp; • &nbsp;
        NLP-Based Java Comment Intelligence
    </div>
    <div style="margin-top:6px;">
        Tokenize • Normalize • Stem • Classify
    </div>
</div>
""")
