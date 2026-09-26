import math
import os
import re

import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "https://infera-backend-ngqc.onrender.com")
POLL_SECONDS = 1.0

st.set_page_config(page_title="Infera - Document Intelligence Platform", layout="wide")

# --- Visual theme (styling only — no app behavior is changed below) ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');

    :root{
        --cream:#EEEAD7;      /* background / light surfaces */
        --panel:#F8F6EC;
        --maroon:#6D0808;     /* primary / accent */
        --ink:#2D0000;        /* dark text / headers */
        --sage:#757D6F;       /* secondary / muted */
        --sage-tint:rgba(117,125,111,.14);
        --hairline:rgba(45,0,0,.12);
    }

    html, body, [class*="css"]{
        font-family:'DM Sans', sans-serif;
    }
    .stApp{
        background-color:var(--cream);
    }
    .main .block-container{
        max-width:1080px;
        padding:3.25rem 3rem 7rem;
    }
    h1, h2, h3{
        font-family:'DM Sans', sans-serif;
        color:var(--ink);
        font-weight:600;
        letter-spacing:-.025em;
    }
    p, li, label, span{ color:var(--ink); }
    button, .stButton>button, details{ transition:background-color .18s ease, border-color .18s ease; }

    /* ---------- Hero ---------- */
    .hero-card{
        display:flex;
        gap:16px;
        align-items:center;
        background:transparent;
        border:0;
        border-radius:0;
        padding:0 0 30px;
        margin-bottom:38px;
        border-bottom:1px solid var(--hairline);
    }
    .hero-accent{
        width:5px;
        min-width:5px;
        align-self:stretch;
        border-radius:2px;
        background-color:var(--maroon);
    }
    .hero-title{
        font-family:'DM Sans', sans-serif;
        font-weight:700;
        font-size:2rem;
        color:var(--ink);
        letter-spacing:-.04em;
        margin:0 0 9px 0;
        line-height:1.15;
    }
    .hero-desc{
        font-size:.96rem;
        color:var(--sage);
        margin:0;
        max-width:none;
        white-space:nowrap;
        letter-spacing:-.01em;
        line-height:1.45;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"]{
        background-color:var(--cream);
        border-right:1px solid var(--hairline);
    }
    section[data-testid="stSidebar"] .block-container{
        padding:2rem 1.25rem 2rem;
    }
    .brand-row{
        display:flex;
        align-items:center;
        gap:10px;
        margin-bottom:34px;
        padding:0 0 22px;
        border-bottom:1px solid var(--hairline);
    }
    .brand-mark{
        width:18px;
        height:21px;
        border-radius:0;
        background:center / contain no-repeat url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='22' viewBox='0 0 20 22' fill='none' stroke='%236D0808' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 1.8h7l5 5V19a1.2 1.2 0 0 1-1.2 1.2H4A1.2 1.2 0 0 1 2.8 19V3A1.2 1.2 0 0 1 4 1.8Z'/%3E%3Cpath d='M11 2v5h5M6 12h7M6 16h7'/%3E%3C/svg%3E");
        flex-shrink:0;
    }
    .brand-name{
        font-family:'DM Sans', sans-serif;
        font-weight:700;
        font-size:1.15rem;
        color:var(--ink);
        letter-spacing:-.025em;
        line-height:1.2;
    }
    .brand-sub{
        font-size:.82rem;
        color:var(--sage);
        line-height:1.1;
    }
    .sidebar-section-label{
        font-size:.9rem;
        font-weight:600;
        color:var(--ink);
        margin:0 0 14px 0;
        letter-spacing:.01em;
    }
    section[data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"]{
        background:transparent;
        border:0 !important;
        border-radius:0;
        box-shadow:none;
        padding:0;
        margin:0 0 30px;
    }
    section[data-testid="stSidebar"] hr{
        margin:22px 0;
        border-color:var(--hairline);
    }
    /* document rows */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"]{
        border-bottom:0;
        padding:8px 0;
        align-items:center;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{ line-height:1.5; }

    /* ---------- Buttons ---------- */
    .stButton>button{
        background-color:var(--maroon);
        color:var(--cream);
        border:1px solid var(--maroon);
        border-radius:7px;
        font-weight:500;
        padding:.55rem 1rem;
        box-shadow:none;
    }
    .stButton>button:hover:not(:disabled){
        background-color:#2D0000;
        border-color:#2D0000;
    }
    .stButton>button:disabled{
        background-color:var(--sage-tint);
        border-color:var(--sage-tint);
        color:var(--sage);
    }
    /* icon-only delete buttons read as ghost controls, not primary actions */
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton>button{
        background-color:transparent;
        border-color:transparent;
        color:var(--sage);
        padding:.25rem .5rem;
    }
    section[data-testid="stSidebar"] div[data-testid="stHorizontalBlock"] .stButton>button:hover:not(:disabled){
        background-color:var(--sage-tint);
        color:var(--maroon);
        transform:none;
        box-shadow:none;
    }

    /* ---------- Chat ---------- */
    [data-testid="stChatMessage"]{
        background-color:transparent;
        border:0;
        border-radius:0;
        padding:1.1rem 0;
    }
    [data-testid="stChatInput"]{
        border-radius:8px;
        border:1px solid rgba(45,0,0,.18);
        background:var(--panel);
    }
    .empty-state{
        text-align:center;
        padding:72px 30px 80px;
        color:var(--sage);
        border:0;
        border-radius:0;
        background:transparent;
        margin:56px 0 0;
    }
    .empty-state h3{
        font-family:'DM Sans', sans-serif;
        font-weight:600;
        letter-spacing:-.025em;
        line-height:1.3;
        margin:0 0 10px 0;
        font-size:1.55rem;
        color:var(--ink);
    }
    .empty-state p{
        margin:0 auto;
        max-width:58ch;
        line-height:1.7;
        color:var(--sage);
    }

    /* Badge pills for the answer meta-row (grounded / cached / degraded) */
    .badge-row{ margin:.35rem 0 .1rem 0; }
    .badge{
        display:inline-block;
        font-size:.8rem;
        font-weight:500;
        padding:3px 10px;
        border-radius:4px;
        margin:0 6px 6px 0;
    }
    .badge-primary{ background-color:var(--maroon); color:var(--cream); }
    .badge-muted{ background-color:var(--sage-tint); color:var(--ink); }
    .badge-outline{ background-color:transparent; border:1px solid var(--sage); color:var(--sage); }

    /* ---------- Expanders (sources / trace) ---------- */
    details{
        background:transparent;
        border:0 !important;
        border-top:1px solid var(--hairline) !important;
        border-radius:0;
        padding:.35rem 0;
    }
    summary{
        color:var(--ink) !important;
        font-weight:500;
    }

    /* ---------- Progress bar ---------- */
    .stProgress > div > div > div{
        background-color:var(--maroon);
    }

    /* ---------- Captions / muted text ---------- */
    [data-testid="stCaptionContainer"], .stCaption{
        color:var(--sage) !important;
    }

    hr{
        border-color:var(--hairline);
    }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"]{
        background-color:rgba(117,125,111,.06);
        border:1px dashed rgba(117,125,111,.55);
        border-radius:7px;
        min-height:178px;
        position:relative;
        cursor:pointer;
        padding:22px 16px;
    }
    [data-testid="stFileUploaderDropzone"] button{
        display:none !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"]{
        display:flex;
        flex-direction:column;
        align-items:center;
        justify-content:center;
        gap:8px;
        width:100%;
        text-align:center;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] span,
    [data-testid="stFileUploaderDropzoneInstructions"] small{
        opacity:0 !important;
        height:0 !important;
        margin:0 !important;
        padding:0 !important;
        overflow:hidden !important;
        font-size:0 !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] > *{
        opacity:0 !important;
        height:0 !important;
        min-height:0 !important;
        margin:0 !important;
        padding:0 !important;
        overflow:hidden !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"]::before{
        content:"";
        display:block;
        width:30px;
        height:30px;
        margin-bottom:3px;
        background:center / contain no-repeat url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='30' height='30' viewBox='0 0 24 24' fill='none' stroke='%236D0808' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M12 16V4m0 0L7.5 8.5M12 4l4.5 4.5'/%3E%3Cpath d='M5 14v4.5A1.5 1.5 0 0 0 6.5 20h11a1.5 1.5 0 0 0 1.5-1.5V14'/%3E%3C/svg%3E");
    }
    [data-testid="stFileUploaderDropzoneInstructions"]::after{
        content:"Drag & drop your file here\\A PDF, TXT, MD • Max 200MB";
        display:block;
        white-space:pre-line;
        color:var(--sage);
        font-size:.82rem;
        font-weight:400;
        line-height:1.8;
        text-align:center;
    }

    /* ---------- Select box ---------- */
    [data-baseweb="select"] > div{
        border-color:var(--hairline) !important;
        border-radius:7px !important;
        background-color:var(--panel) !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] small{ color:var(--sage); }
    [data-testid="stCaptionContainer"], .stCaption, .brand-sub,
    .hero-desc, .empty-state p{ color:var(--sage) !important; }
    @media (max-width: 1050px){
        .hero-desc{ white-space:normal; }
    }
    @media (max-width: 800px){
        .main .block-container{ padding:2rem 1.2rem 6rem; }
        .hero-card{ margin-bottom:24px; }
        .empty-state{ margin-top:28px; padding:48px 8px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <div class="hero-accent"></div>
        <div>
            <h1 class="hero-title">Infera</h1>
            <p class="hero-desc">Document intelligence &amp; retrieval — grounded, citation-backed Q&amp;A
            over your PDF, TXT, and Markdown files, powered by Gemini.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Compiled once at import time (compiling validates the graph's shape) and reused for every request.
_MD_INLINE = re.compile(r"([\\`*_\[\]<>])")
_MD_BLOCK_START = re.compile(r"^(\s*)([#>|=+\-]|\d+[.)])", flags=re.MULTILINE)


def escape_markdown(text: str) -> str:
    """Show source text literally instead of letting it style itself."""
    return _MD_BLOCK_START.sub(r"\1\\\2", _MD_INLINE.sub(r"\\\1", text))


def shorten(text: str, limit: int = 700) -> tuple[str, bool]:
    """Trim to `limit` characters on a word boundary. Returns (text, was_cut)."""
    if len(text) <= limit:
        return text, False
    cut = text[:limit]
    spaced = cut.rsplit(" ", 1)[0]
    return (spaced if len(spaced) > limit * 0.6 else cut).rstrip(" ,;:-") + "…", True


def relevance_percent(score: float) -> int:
    # Turn a raw score into a 0-100 reading a human can glance at.
    return round(100 / (1 + math.exp(-max(-30.0, min(30.0, score)))))

def render_citation(index: int, citation: dict) -> None:
    percent = relevance_percent(citation["score"])
    body, truncated = shorten(citation["text"])

    with st.container(border=True):
        header, badge = st.columns([4, 1])
        header.markdown(f"**{index}. {citation['filename']}** (chunk {citation['chunk_index']})")
        badge.markdown(
            f"<div style='text-align:right;color:#6D0808;font-weight:600;'>{percent}% match</div>",
            unsafe_allow_html=True,
        )
        for paragraph in (p for p in body.split("\n") if p.strip()):
            st.markdown(escape_markdown(paragraph))
        if truncated:
            st.caption("Snippet truncated — this is part of a longer chunk.")
            

# Upload flow
st.session_state.setdefault("ingest_job_id", None)
st.session_state.setdefault("upload_banner", None)
st.session_state.setdefault("uploader_round", 0)
st.session_state.setdefault("history", [])


def start_ingestion(file) -> None:
    """POST the file and remember the job id; the polling fragment takes it from here."""
    try:
        resp = requests.post(
            f"{BACKEND_URL}/ingest",
            files={"file": (file.name, file.getvalue())},
            timeout=120,
        )
    except requests.RequestException as exc:
        st.session_state.upload_banner = ("error", f"Could not reach the backend: {exc}")
        return

    if resp.status_code != 202:
        try:
            detail = resp.json().get("detail", resp.text)
        except ValueError:
            detail = resp.text
        st.session_state.upload_banner = ("error", f"Upload failed: {detail}")
        return

    st.session_state.ingest_job_id = resp.json()["job_id"]
    st.session_state.upload_banner = None


def finish_ingestion(banner: tuple[str, str]) -> None:
    """Clear the job, show the outcome, and reset the uploader widget."""
    st.session_state.ingest_job_id = None
    st.session_state.upload_banner = banner
    # Increment a counter so the uploader widget re-renders and clears its file selection.
    st.session_state.uploader_round += 1


@st.fragment(run_every=POLL_SECONDS)
def ingestion_progress() -> None:
    """Poll the job and draw its progress bar.

    Being a FRAGMENT (not plain code) matters: it re-runs on its own timer
    instead of blocking the whole page in a sleep loop, so everything else
    stays responsive while the bar keeps moving on its own.
    """
    job_id = st.session_state.ingest_job_id
    if not job_id:
        return

    try:
        resp = requests.get(f"{BACKEND_URL}/jobs/{job_id}", timeout=10)
    except requests.RequestException as exc:
        st.warning(f"Lost contact with the backend, retrying… ({exc})")
        return

    if resp.status_code == 404:
        finish_ingestion(("error", "That upload job is no longer on the server. Please try again."))
        st.rerun(scope="app")
        return
    if resp.status_code != 200:
        st.warning("Waiting for the backend…")
        return

    job = resp.json()
    status = job.get("status", "processing")
    percent = int(job.get("progress") or 0)
    stage = job.get("stage") or "Processing"
    name = job.get("filename") or "file"

    if status == "complete":
        finish_ingestion(("success", f"✅ **{name}** ingested and ready to query."))
        st.rerun(scope="app")   # refresh the document list in the sidebar
        return
    if status == "failed":
        finish_ingestion(("error", f"❌ Ingestion failed: {job.get('error') or 'unknown error'}"))
        st.rerun(scope="app")
        return

    st.progress(percent / 100, text=f"{stage} — {percent}%")
    st.caption(f"Processing **{name}**… you can keep reading while this finishes.")
    
# Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="brand-row">
            <span class="brand-mark"></span>
            <div>
                <div class="brand-name">Infera</div>
                <div class="brand-sub">Document intelligence</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<p class="sidebar-section-label">Upload a document</p>', unsafe_allow_html=True)

        is_busy = st.session_state.ingest_job_id is not None
        uploaded_file = st.file_uploader(
            "PDF, TXT, or Markdown",
            type=["pdf", "txt", "md"],
            key=f"uploader_{st.session_state.uploader_round}",
            disabled=is_busy,
            label_visibility="collapsed",
        )
        if st.button("Processing…" if is_busy else "Ingest file", disabled=is_busy or uploaded_file is None, use_container_width=True):
            start_ingestion(uploaded_file)
            st.rerun()

        if is_busy:
            ingestion_progress()

        if st.session_state.upload_banner:
            kind, message = st.session_state.upload_banner
            (st.success if kind == "success" else st.error)(message)

    with st.container(border=True):
        st.markdown('<p class="sidebar-section-label">Your documents</p>', unsafe_allow_html=True)

        try:
            docs_resp = requests.get(f"{BACKEND_URL}/documents", timeout=10)
            documents = docs_resp.json() if docs_resp.status_code == 200 else []
        except requests.RequestException:
            documents = []
            st.error(f"Backend unreachable — is it running on {BACKEND_URL}?")

        if not documents:
            st.caption("No documents ingested yet — upload one above to get started.")

        for doc in documents:
            col_name, col_delete = st.columns([5, 1])
            col_name.write(f"**{doc['filename']}** — {doc['num_chunks']} chunks")
            if col_delete.button("🗑️", key=f"delete_{doc['id']}", help=f"Delete {doc['filename']}"):
                del_resp = requests.delete(f"{BACKEND_URL}/documents/{doc['id']}", timeout=10)
                if del_resp.status_code == 204:
                    st.rerun()
                else:
                    st.error(f"Could not delete: {del_resp.text}")

        st.divider()
        doc_options = {"All documents": []}
        for doc in documents:
            doc_options[doc["filename"]] = [doc["id"]]
        selected_label = st.selectbox("Search scope", list(doc_options.keys()))
        selected_document_ids = doc_options[selected_label] or None   # [] -> None means "search everything"

# Main panel
question = st.chat_input("Ask a question about your documents...")

if not st.session_state.history and not question:
    st.markdown(
        """
        <div class="empty-state">
            <h3>Ask your first question</h3>
            <p>Upload a document in the sidebar, then ask anything about it — every answer comes with sources.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for turn in st.session_state.history:
        with st.chat_message("user"):
            st.write(turn["question"])
        with st.chat_message("assistant"):
            st.write(turn["answer"])

if question:
    with st.chat_message("user"):
        st.write(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            payload = {"question": question, "document_ids": selected_document_ids}
            try:
                resp = requests.post(f"{BACKEND_URL}/query", json=payload, timeout=60)
            except requests.RequestException as exc:
                resp = None
                st.error(f"Could not reach the backend: {exc}")

        if resp is not None:
            if resp.status_code != 200:
                try:
                    detail = resp.json().get("detail", resp.text)
                except ValueError:
                    detail = resp.text
                st.error(f"Query failed: {detail}")
            else:
                data = resp.json()
                st.write(data["answer"])

                badges = []
                if data["is_grounded"] is True:
                    badges.append(("badge-primary", "✅ Grounded"))
                elif data["is_grounded"] is False:
                    badges.append(("badge-outline", "⚠️ Not fully grounded"))
                else:
                    badges.append(("badge-muted", "❔ Groundedness unknown"))
                if data["retrieval_degraded"]:
                    badges.append(("badge-outline", "⚠️ Reranker unavailable — showing hybrid search results"))
                if data["cached"]:
                    badges.append(("badge-muted", "⚡ Cached"))

                st.markdown(
                    '<div class="badge-row">'
                    + "".join(f'<span class="badge {cls}">{label}</span>' for cls, label in badges)
                    + "</div>",
                    unsafe_allow_html=True,
                )

                citations = data["citations"]
                with st.expander(f"📎 Sources / citations ({len(citations)})"):
                    if not citations:
                        st.caption("No matching chunks were found.")
                    for i, citation in enumerate(citations, start=1):
                        render_citation(i, citation)

                with st.expander("🔍 Pipeline trace (observability)"):
                    st.write(f"Search query used: `{data['search_query']}`")
                    st.json(data["trace"])

                st.session_state.history.append({"question": question, "answer": data["answer"]})
