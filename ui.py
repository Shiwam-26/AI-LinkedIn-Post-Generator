
import streamlit as st
import html
import runpy
import builtins
import io
from pathlib import Path
from contextlib import redirect_stdout

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0B1120;
    color: #F1F5F9;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background: #111B2E;
    border-right: 1px solid #26354C;
}

[data-testid="stSidebar"] .stRadio label {
    color: #CBD5E1;
    font-weight: 500;
}

/* SIDEBAR BRAND */

.brand {
    font-size: 25px;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.8px;
}

.brand-subtitle {
    color: #60A5FA;
    font-size: 15px;
    font-weight: 700;
    margin-top: 3px;
}

.muted {
    color: #94A3B8;
    font-size: 13px;
    line-height: 1.7;
}

/* HERO */

.hero {
    background: linear-gradient(120deg, #172E53, #202344);
    border: 1px solid #34496D;
    padding: 32px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero-tag {
    color: #93C5FD;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 12px;
}

.hero-description {
    color: #B8C7DD;
    font-size: 14px;
    line-height: 1.8;
    max-width: 750px;
    margin-top: 8px;
}

/* CARDS */

.panel {
    background: #131F33;
    border: 1px solid #293B55;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

.stat {
    background: #16263E;
    border: 1px solid #30445F;
    padding: 20px;
    border-radius: 14px;
    min-height: 120px;
}

.stat-icon {
    font-size: 23px;
    margin-bottom: 10px;
}

.stat-label {
    color: #94A3B8;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
}

.stat-description {
    color: #CBD5E1;
    font-size: 12px;
    margin-top: 6px;
}

/* WORKFLOW */

.step-number {
    color: #60A5FA;
    font-size: 13px;
    font-weight: 800;
}

.step-title {
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 700;
}

.step-description {
    color: #94A3B8;
    font-size: 12px;
    margin-top: 8px;
}

/* POST PREVIEW */

.post {
    background: #FFFFFF;
    color: #1E293B;
    padding: 25px;
    border-radius: 13px;
    line-height: 1.8;
    white-space: pre-wrap;
    overflow-wrap: anywhere;
    font-size: 14px;
}

.post-heading {
    color: #0F172A;
    font-size: 17px;
    font-weight: 800;
}

.post-subheading {
    color: #64748B;
    font-size: 11px;
}

/* INPUTS */

.stTextArea textarea,
.stTextInput input {
    background: #18263D !important;
    color: #FFFFFF !important;
    border: 1px solid #354966 !important;
    border-radius: 10px !important;
}

.stSelectbox div[data-baseweb="select"] > div {
    background: #18263D;
    border-color: #354966;
    color: white;
}

[data-testid="stSlider"] {
    color: #60A5FA;
}

/* BUTTONS */

.stButton button {
    background: linear-gradient(90deg, #2563EB, #0A66C2);
    color: white;
    border: none;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton button:hover {
    color: white;
    border: 1px solid #93C5FD;
    background: #1D4ED8;
}

.stDownloadButton button {
    border-radius: 9px;
    font-weight: 600;
    min-height: 42px;
}

/* DIVIDER */

hr {
    border-color: #293B55;
}

/* EXPANDER */

[data-testid="stExpander"] {
    background: #131F33;
    border: 1px solid #293B55;
    border-radius: 12px;
}

/* RESPONSIVE */

@media (max-width: 768px) {
    .hero {
        padding: 22px;
    }

    .stat {
        margin-bottom: 10px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "topic": "",
    "generated_post": "",
    "review_feedback": "",
    "is_approved": False,
    "attempt": 0,
    "drafts": [],
    "generation_error": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# BACKEND CONNECTION
# =====================================================

def generate_linkedin_post(topic):

    backend_path = Path(__file__).resolve().with_name(
        "iterative_Tools.py"
    )

    if not backend_path.is_file():
        raise FileNotFoundError(
            f"Backend file not found: {backend_path}\n"
            "Keep ui.py and iterative_Tools.py in the same folder."
        )

    captured_output = io.StringIO()
    original_input = builtins.input

    try:

        builtins.input = lambda prompt="": topic

        with redirect_stdout(captured_output):

            namespace = runpy.run_path(
                str(backend_path),
                run_name="__main__"
            )

        final_state = namespace.get("final_state")

        if not isinstance(final_state, dict):
            output = captured_output.getvalue()

            raise RuntimeError(
                "Backend executed, but a dictionary named "
                "'final_state' was not found.\n\n"
                "Check how the final LangGraph result is stored "
                "inside iterative_Tools.py.\n\n"
                f"Captured backend output:\n{output[-1500:]}"
            )

        return final_state

    finally:
        builtins.input = original_input


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("""
    <div class="brand">💼 LinkedIn</div>
    <div class="brand-subtitle">Post Generator</div>
    <p class="muted">AI-Powered Content Creation Studio</p>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🧭 Navigation")

    page = st.radio(
        "Navigation",
        [
            "✍️ Create Post",
            "📁 My Drafts",
            "📊 AI Insights",
            "⚙️ Settings"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### 🤖 AI WORKFLOW")

    st.markdown("""
    <div class="muted">
        ✍️ Writer Agent<br><br>
        🔍 Research Agent<br><br>
        🛡️ Reviewer Agent<br><br>
        🔄 Iterative Refinement
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("""
    <div class="muted">
        💼 LinkedIn Post Generator<br>
        Version 2.0
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-tag">AI CONTENT CREATION STUDIO</div>
    <div class="hero-description">
        Create engaging professional content with intelligent writing,
        web research and AI-powered quality review.
    </div>
</div>
""", unsafe_allow_html=True)

# Native Streamlit heading: HTML tags will not appear as text.
st.title("💼 LinkedIn Post Generator")

st.caption(
    "Transform your ideas into engaging professional LinkedIn posts."
)


# =====================================================
# DASHBOARD METRICS
# =====================================================

columns = st.columns(4)

metrics = [
    ("✍️", "AI WRITER", "Intelligent content creation"),
    ("🔍", "WEB RESEARCH", "Relevant information gathering"),
    ("🛡️", "AI REVIEWER", "Content quality assurance"),
    ("🔄", "ITERATIONS", "Continuous refinement")
]

for col, metric in zip(columns, metrics):

    with col:
        st.markdown(f"""
        <div class="stat">
            <div class="stat-icon">{metric[0]}</div>
            <div class="stat-label">{metric[1]}</div>
            <div class="stat-description">{metric[2]}</div>
        </div>
        """, unsafe_allow_html=True)

st.write("")


# =====================================================
# CREATE POST
# =====================================================

if page == "✍️ Create Post":

    left, right = st.columns([1.05, 0.95], gap="large")

    # LEFT SECTION

    with left:

        st.markdown("### ✍️ Create Your LinkedIn Post")

        st.markdown(
            '<p class="muted">Share your idea and customize your content.</p>',
            unsafe_allow_html=True
        )

        topic = st.text_area(
            "Post Topic",
            placeholder=(
                "Example: How Generative AI is transforming "
                "Data Analytics..."
            ),
            height=140,
            key="topic_input"
        )

        audience = st.selectbox(
            "👥 Target Audience",
            [
                "Professionals",
                "Students",
                "Recruiters",
                "Tech Enthusiasts",
                "Business Leaders"
            ]
        )

        tone = st.selectbox(
            "🎯 Writing Tone",
            [
                "Professional",
                "Conversational",
                "Storytelling",
                "Educational",
                "Thought Leadership"
            ]
        )

        length = st.select_slider(
            "📝 Post Length",
            options=["Short", "Medium", "Long"],
            value="Medium"
        )

        if st.button(
            "🚀 Generate LinkedIn Post",
            use_container_width=True
        ):

            if not topic.strip():

                st.warning("Please enter a topic first.")

            else:

                st.session_state.topic = topic.strip()
                st.session_state.generated_post = ""
                st.session_state.review_feedback = ""
                st.session_state.generation_error = ""

                try:

                    with st.spinner(
                        "🤖 AI Writer and Reviewer are working..."
                    ):

                        result = generate_linkedin_post(
                            topic.strip()
                        )

                        st.session_state.generated_post = result.get(
                            "draft", ""
                        )

                        st.session_state.review_feedback = result.get(
                            "review_feedback", ""
                        )

                        st.session_state.is_approved = result.get(
                            "is_approved", False
                        )

                        st.session_state.attempt = result.get(
                            "attempt", 0
                        )

                    if st.session_state.generated_post:
                        st.success(
                            "LinkedIn post generated successfully!"
                        )
                    else:
                        st.warning(
                            "Backend completed, but no draft was generated."
                        )

                except Exception as e:

                    st.session_state.generation_error = str(e)

                    st.error("Post generation failed.")

                    st.exception(e)

        st.caption(
            "💡 Your content deserves a professional voice."
        )

    # RIGHT SECTION

    with right:

        st.markdown("### ⚡ How It Works")

        steps = [
            (
                "01",
                "Topic Understanding",
                "Analyze the given topic and context."
            ),
            (
                "02",
                "Web Research",
                "Gather relevant information using web search."
            ),
            (
                "03",
                "AI Content Writing",
                "Generate an engaging LinkedIn post."
            ),
            (
                "04",
                "Quality Review",
                "Evaluate the draft against quality criteria."
            ),
            (
                "05",
                "Final Post",
                "Prepare a polished LinkedIn post."
            )
        ]

        for number, title, description in steps:

            st.markdown(f"""
            <div class="panel">
                <span class="step-number">{number}</span>
                <span class="step-title" style="margin-left:10px;">
                    {title}
                </span>
                <div class="step-description" style="margin-left:32px;">
                    {description}
                </div>
            </div>
            """, unsafe_allow_html=True)


    # =================================================
    # LINKEDIN POST PREVIEW
    # =================================================

    st.divider()

    st.markdown("### 👀 LinkedIn Post Preview")

    if st.session_state.generated_post:

        safe_post = html.escape(
            str(st.session_state.generated_post)
        )

        st.markdown(f"""
        <div class="post">
            <div class="post-heading">💼 LinkedIn Post</div>
            <div class="post-subheading">
                Generated by your AI Writer Agent
            </div>
            <br>
            {safe_post}
        </div>
        """, unsafe_allow_html=True)

        st.write("")

        if st.session_state.is_approved:
            st.success("🛡️ AI Reviewer: APPROVED")
        else:
            st.warning("🛡️ AI Reviewer: NOT APPROVED")

        st.info(
            f"🔄 Total Attempts: {st.session_state.attempt}"
        )

        with st.expander("📝 Reviewer Feedback"):
            st.write(
                st.session_state.review_feedback
                or "No reviewer feedback available."
            )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "💾 Save to My Drafts",
                use_container_width=True
            ):

                draft = {
                    "topic": st.session_state.topic,
                    "post": st.session_state.generated_post,
                    "approved": st.session_state.is_approved,
                    "attempts": st.session_state.attempt
                }

                if not any(
                    d["post"] == draft["post"]
                    for d in st.session_state.drafts
                ):

                    st.session_state.drafts.append(draft)

                    st.success("Post saved to My Drafts!")

                else:
                    st.info("This post is already saved.")

        with col2:

            st.download_button(
                label="📥 Download Post",
                data=st.session_state.generated_post,
                file_name="linkedin_post.txt",
                mime="text/plain",
                use_container_width=True
            )

        st.caption(
            "Select and copy the post text from the preview above."
        )

    else:

        st.info(
            "✨ Your AI-generated LinkedIn post will appear here "
            "after generation."
        )


# =====================================================
# MY DRAFTS
# =====================================================

elif page == "📁 My Drafts":

    st.markdown("## 📁 My Drafts")

    drafts = st.session_state.drafts

    if drafts:

        st.caption(f"Total saved posts: {len(drafts)}")

        for index, draft in enumerate(reversed(drafts)):

            with st.expander(
                f"📝 {draft['topic']}",
                expanded=False
            ):

                st.write(draft["post"])

                if draft["approved"]:
                    st.success("AI Reviewer: Approved")
                else:
                    st.warning("AI Reviewer: Not Approved")

                st.caption(
                    f"Total Attempts: {draft['attempts']}"
                )

                st.download_button(
                    "📥 Download Draft",
                    data=draft["post"],
                    file_name=f"linkedin_draft_{index + 1}.txt",
                    mime="text/plain",
                    key=f"download_{index}"
                )

    else:

        st.markdown("""
        <div class="panel">
            <h3>📝 Your saved posts</h3>
            <p class="muted">
                Your generated and saved LinkedIn drafts
                will appear here.
            </p>
        </div>
        """, unsafe_allow_html=True)


# =====================================================
# AI INSIGHTS
# =====================================================

elif page == "📊 AI Insights":

    st.markdown("## 📊 AI Insights")

    st.caption(
        "Track your saved content and AI review performance."
    )

    drafts = st.session_state.drafts

    total_posts = len(drafts)

    approved_posts = sum(
        1 for draft in drafts
        if draft["approved"]
    )

    average_attempts = (
        sum(draft["attempts"] for draft in drafts) / total_posts
        if total_posts else 0
    )

    cols = st.columns(3)

    insights = [
        (str(total_posts), "TOTAL POSTS"),
        (str(approved_posts), "APPROVED POSTS"),
        (f"{average_attempts:.1f}", "AVERAGE ATTEMPTS")
    ]

    for col, item in zip(cols, insights):

        with col:

            st.markdown(f"""
            <div class="stat">
                <div class="stat-label">{item[1]}</div>
                <h2 style="color:#60A5FA;font-size:28px;">
                    {item[0]}
                </h2>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    if total_posts:

        approval_rate = (
            approved_posts / total_posts
        ) * 100

        st.markdown("### 📈 Approval Rate")

        st.progress(int(approval_rate))

        st.caption(
            f"{approval_rate:.1f}% of your saved posts are approved."
        )

    else:

        st.info(
            "Generate and save posts to view your AI insights."
        )


# =====================================================
# SETTINGS
# =====================================================

elif page == "⚙️ Settings":

    st.markdown("## ⚙️ Settings")

    st.caption(
        "Manage your default content preferences."
    )

    st.markdown("### 🧠 Content Preferences")

    st.selectbox(
        "Default Writing Tone",
        [
            "Professional",
            "Conversational",
            "Educational"
        ]
    )

    st.selectbox(
        "Default Post Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    st.selectbox(
        "Default Audience",
        [
            "Professionals",
            "Students",
            "Recruiters"
        ]
    )

    st.info(
        "These preferences are currently visual settings only. "
        "They are not passed to the backend agent."
    )

    st.divider()

    st.markdown("### 💼 About")

    st.write("LinkedIn Post Generator")

    st.caption(
        "AI-Powered Content Creation & Review Assistant | Version 2.0"
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div style="
    text-align:center;
    color:#64748B;
    font-size:12px;
    padding:10px;
">
    💼 LinkedIn Post Generator<br>
    AI-Powered Content Creation & Review Assistant
</div>
""", unsafe_allow_html=True)