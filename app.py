import streamlit as st
import time
import logging
import requests
from typing import Dict, Optional
from datetime import datetime

# Import agent chains
from agents import build_reader_agent, build_Search_agent, writer_chain, critic_chain

# ── Logging Setup ────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ── Page Configuration ───────────────────────────────────────────────────────
def configure_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="ResearchMind · AI Research Agent",
        page_icon="🔬",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


# ── Custom CSS ───────────────────────────────────────────────────────────────
def load_custom_css():
    """Load and inject custom CSS styling."""
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

    /* ── Reset & base ── */
    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        color: #e8e4dc;
    }

    .stApp {
        background: #0a0a0f;
        background-image:
            radial-gradient(ellipse 80% 50% at 20% -10%, rgba(255,140,50,0.12) 0%, transparent 60%),
            radial-gradient(ellipse 60% 40% at 80% 110%, rgba(255,80,30,0.08) 0%, transparent 55%);
    }

    /* ── Hide default streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding: 2rem 3rem 4rem; max-width: 1200px; }

    /* ── Hero header ── */
    .hero {
        text-align: center;
        padding: 3.5rem 0 2.5rem;
        position: relative;
    }
    .hero-eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.25em;
        text-transform: uppercase;
        color: #ff8c32;
        margin-bottom: 1rem;
        opacity: 0.9;
    }
    .hero h1 {
        font-family: 'Syne', sans-serif;
        font-size: clamp(2.8rem, 6vw, 5rem);
        font-weight: 800;
        line-height: 1.0;
        letter-spacing: -0.03em;
        color: #f0ebe0;
        margin: 0 0 1rem;
    }
    .hero h1 span {
        color: #ff8c32;
    }
    .hero-sub {
        font-size: 1.05rem;
        font-weight: 300;
        color: #a09890;
        max-width: 520px;
        margin: 0 auto;
        line-height: 1.65;
    }

    /* ── Divider ── */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,140,50,0.3), transparent);
        margin: 2rem 0;
    }

    /* ── Input card ── */
    .input-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,140,50,0.15);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(8px);
    }

    /* ── Streamlit input overrides ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,140,50,0.25) !important;
        border-radius: 10px !important;
        color: #f0ebe0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 1rem !important;
        padding: 0.75rem 1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff8c32 !important;
        box-shadow: 0 0 0 3px rgba(255,140,50,0.12) !important;
    }
    .stTextInput > label {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.15em !important;
        text-transform: uppercase !important;
        color: #ff8c32 !important;
        font-weight: 500 !important;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #ff8c32 0%, #ff5a1a 100%) !important;
        color: #0a0a0f !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.04em !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 2.2rem !important;
        cursor: pointer !important;
        transition: transform 0.15s, box-shadow 0.15s, opacity 0.15s !important;
        box-shadow: 0 4px 20px rgba(255,140,50,0.3) !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(255,140,50,0.4) !important;
        opacity: 0.95 !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Pipeline step cards ── */
    .step-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
        transition: border-color 0.3s;
    }
    .step-card.active {
        border-color: rgba(255,140,50,0.4);
        background: rgba(255,140,50,0.04);
    }
    .step-card.done {
        border-color: rgba(80,200,120,0.3);
        background: rgba(80,200,120,0.03);
    }
    .step-card::before {
        content: '';
        position: absolute;
        left: 0; top: 0; bottom: 0;
        width: 3px;
        border-radius: 14px 0 0 14px;
        background: rgba(255,255,255,0.05);
        transition: background 0.3s;
    }
    .step-card.active::before { background: #ff8c32; }
    .step-card.done::before   { background: #50c878; }

    .step-header {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.3rem;
    }
    .step-num {
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        font-weight: 500;
        letter-spacing: 0.15em;
        color: #ff8c32;
        opacity: 0.7;
    }
    .step-title {
        font-family: 'Syne', sans-serif;
        font-size: 0.95rem;
        font-weight: 700;
        color: #f0ebe0;
    }
    .step-status {
        margin-left: auto;
        font-family: 'DM Mono', monospace;
        font-size: 0.68rem;
        letter-spacing: 0.1em;
    }
    .status-waiting  { color: #555; }
    .status-running  { color: #ff8c32; }
    .status-done     { color: #50c878; }

    /* ── Result panels ── */
    .result-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .result-panel-title {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #ff8c32;
        margin-bottom: 1rem;
        padding-bottom: 0.7rem;
        border-bottom: 1px solid rgba(255,140,50,0.15);
    }
    .result-content {
        font-size: 0.92rem;
        line-height: 1.8;
        color: #cdc8bf;
        white-space: pre-wrap;
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Report & feedback panels ── */
    .report-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(255,140,50,0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
    }
    .feedback-panel {
        background: rgba(255,255,255,0.025);
        border: 1px solid rgba(80,200,120,0.2);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
    }
    .panel-label {
        font-family: 'DM Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        padding-bottom: 0.7rem;
    }
    .panel-label.orange {
        color: #ff8c32;
        border-bottom: 1px solid rgba(255,140,50,0.15);
    }
    .panel-label.green {
        color: #50c878;
        border-bottom: 1px solid rgba(80,200,120,0.15);
    }

    /* ── Progress text ── */
    .stSpinner > div { color: #ff8c32 !important; }

    /* ── Expander ── */
    details summary {
        font-family: 'DM Mono', monospace !important;
        font-size: 0.75rem !important;
        color: #a09890 !important;
        letter-spacing: 0.1em !important;
        cursor: pointer;
    }

    /* ── Section heading ── */
    .section-heading {
        font-family: 'Syne', sans-serif;
        font-size: 1.3rem;
        font-weight: 700;
        color: #f0ebe0;
        margin: 2rem 0 1rem;
    }

    /* ── Toast-style notice ── */
    .notice {
        font-family: 'DM Mono', monospace;
        font-size: 0.72rem;
        color: #605850;
        text-align: center;
        margin-top: 3rem;
        letter-spacing: 0.08em;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ── UI Component: Step Card ──────────────────────────────────────────────────
def render_step_card(num: str, title: str, state: str, desc: str = "") -> None:
    """
    Render a pipeline step card with status indicator.
    
    Args:
        num: Step number (e.g., "01")
        title: Step title
        state: "waiting", "running", or "done"
        desc: Optional description text
    """
    status_map = {
        "waiting": ("WAITING", "status-waiting"),
        "running": ("● RUNNING", "status-running"),
        "done": ("✓ DONE", "status-done"),
    }
    label, cls = status_map.get(state, ("", ""))
    card_cls = {"running": "active", "done": "done"}.get(state, "")
    
    desc_html = (
        f"<div style='font-size:0.82rem;color:#706860;margin-top:0.3rem;'>{desc}</div>"
        if desc else ""
    )
    
    st.markdown(f"""
    <div class="step-card {card_cls}">
        <div class="step-header">
            <span class="step-num">{num}</span>
            <span class="step-title">{title}</span>
            <span class="step-status {cls}">{label}</span>
        </div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


# ── UI Component: Hero Section ───────────────────────────────────────────────
def render_hero() -> None:
    """Render the hero header section."""
    st.markdown("""
    <div class="hero">
        <div class="hero-eyebrow">Multi-Agent AI System</div>
        <h1>Research<span>Mind</span></h1>
        <p class="hero-sub">
            Four specialized AI agents collaborate — searching, scraping, writing,
            and critiquing — to deliver a polished research report on any topic.
        </p>
    </div>
    <div class="divider"></div>
    """, unsafe_allow_html=True)


# ── UI Component: Example Chips ──────────────────────────────────────────────
def render_example_chips(examples: list) -> None:
    """Render example topic chips."""
    st.markdown("""
    <div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1.5rem;">
        <span style="font-family:'DM Mono',monospace;font-size:0.68rem;color:#605850;letter-spacing:0.1em;">TRY →</span>
    """, unsafe_allow_html=True)
    
    for ex in examples:
        st.markdown(f"""
        <span style="
            background:rgba(255,255,255,0.04);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:6px;
            padding:0.25rem 0.7rem;
            font-size:0.75rem;
            color:#a09890;
            font-family:'DM Sans',sans-serif;
            cursor:default;
        ">{ex}</span>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)


# ── Session State Management ─────────────────────────────────────────────────
def initialize_session_state() -> None:
    """Initialize or reset session state variables."""
    state_vars = {
        "results": {},
        "running": False,
        "done": False,
        "current_step": None,
        "error_message": None,
        "start_time": None,
    }
    
    for key, default_value in state_vars.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


# ── Pipeline Step Status ─────────────────────────────────────────────────────
def get_step_status(step: str) -> str:
    """
    Determine the current status of a pipeline step.
    
    Args:
        step: Step name ("search", "reader", "writer", "critic")
    
    Returns:
        Status: "waiting", "running", or "done"
    """
    r = st.session_state.results
    steps = ["search", "reader", "writer", "critic"]
    
    if not r:
        return "waiting"
    
    if step in r:
        return "done"
    
    if st.session_state.running:
        for k in steps:
            if k not in r:
                return "running" if k == step else "waiting"
    
    return "waiting"


# ── Pipeline Execution ───────────────────────────────────────────────────────
def execute_pipeline(topic: str) -> Dict[str, str]:
    """
    Send the research request to the FastAPI backend.
    """

    try:
        logger.info(f"Sending research request to FastAPI: {topic}")

        st.session_state.current_step = "search"

        response = requests.post(
            "http://localhost:8000/research",
            json={"topic": topic},
            timeout=300
        )

        # Check if FastAPI returned an error
        response.raise_for_status()

        # Get JSON response
        data = response.json()

        # Get pipeline results
        results = data["result"]

        # Save results to Streamlit state
        st.session_state.results = results

        logger.info("Research completed successfully")

        return results

    except requests.exceptions.ConnectionError:
        error = "Could not connect to ResearchMind API. Make sure FastAPI is running on port 8000."

        logger.error(error)
        st.session_state.error_message = error
        raise Exception(error)

    except requests.exceptions.Timeout:
        error = "Research request timed out."

        logger.error(error)
        st.session_state.error_message = error
        raise Exception(error)

    except Exception as e:
        logger.error(
            f"Pipeline request failed: {str(e)}",
            exc_info=True
        )

        st.session_state.error_message = str(e)
        raise

# ── Results Display ──────────────────────────────────────────────────────────
def display_results(results: Dict[str, str]) -> None:
    """Display the pipeline results."""
    if not results:
        return
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-heading">Results</div>', unsafe_allow_html=True)
    
    # Search Results (expandable)
    if "search" in results:
        with st.expander("🔍 Search Results (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Search Agent Output</div>'
                f'<div class="result-content">{results["search"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    # Reader Results (expandable)
    if "reader" in results:
        with st.expander("📄 Scraped Content (raw)", expanded=False):
            st.markdown(
                f'<div class="result-panel">'
                f'<div class="result-panel-title">Reader Agent Output</div>'
                f'<div class="result-content">{results["reader"]}</div>'
                f'</div>',
                unsafe_allow_html=True
            )
    
    # Final Report
    if "writer" in results:
        st.markdown(
            '<div class="report-panel">'
            '<div class="panel-label orange">📝 Final Research Report</div>',
            unsafe_allow_html=True
        )
        st.markdown(results["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download Button
        st.download_button(
            label="⬇  Download Report (.md)",
            data=results["writer"],
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )
    
    # Critic Feedback
    if "critic" in results:
        st.markdown(
            '<div class="feedback-panel">'
            '<div class="panel-label green">🧐 Critic Feedback</div>',
            unsafe_allow_html=True
        )
        st.markdown(results["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────────────────────
def render_footer() -> None:
    """Render the footer."""
    st.markdown("""
    <div class="notice">
        ResearchMind · Powered by LangChain multi-agent pipeline · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


# ── Main Application ─────────────────────────────────────────────────────────
def main() -> None:
    """Main application entry point."""
    # Initialize
    configure_page()
    load_custom_css()
    initialize_session_state()
    
    # Render Hero
    render_hero()
    
    # Layout: Input left, Pipeline right
    col_input, col_spacer, col_pipeline = st.columns([5, 0.5, 4])
    
    with col_input:
        st.markdown('<div class="input-card">', unsafe_allow_html=True)
        
        # Text Input
        topic = st.text_input(
            "Research Topic",
            placeholder="e.g. Quantum computing breakthroughs in 2025",
            key="topic_input",
            label_visibility="visible",
        )
        
        # Run Button
        run_btn = st.button("⚡  Run Research Pipeline", use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example Chips
        examples = ["LLM agents 2025", "CRISPR gene editing", "Fusion energy progress"]
        render_example_chips(examples)
    
    with col_pipeline:
        st.markdown('<div class="section-heading">Pipeline</div>', unsafe_allow_html=True)
        
        render_step_card("01", "Search Agent", get_step_status("search"), "Gathers recent web information")
        render_step_card("02", "Reader Agent", get_step_status("reader"), "Scrapes & extracts deep content")
        render_step_card("03", "Writer Chain", get_step_status("writer"), "Drafts the full research report")
        render_step_card("04", "Critic Chain", get_step_status("critic"), "Reviews & scores the report")
    
    # Handle Run Button
    if run_btn:
        if not topic.strip():
            st.error("❌ Please enter a research topic first.")
            logger.warning("Run button clicked with empty topic")
        else:
            # Reset state and execute pipeline
            st.session_state.results = {}
            st.session_state.running = True
            st.session_state.done = False
            st.session_state.error_message = None
            st.session_state.start_time = datetime.now()
            st.rerun()
    
    # Execute Pipeline
    if st.session_state.running and not st.session_state.done:
        topic_val = st.session_state.topic_input
        try:
            execute_pipeline(topic_val)
            st.session_state.running = False
            st.session_state.done = True
            st.rerun()
        except Exception as e:
            st.error(f"❌ Pipeline failed: {str(e)}")
            logger.error(f"Pipeline error: {str(e)}", exc_info=True)
            st.session_state.running = False
    
    # Display Results
    if st.session_state.results:
        display_results(st.session_state.results)
    
    # Render Footer
    render_footer()


# ── Entry Point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
    