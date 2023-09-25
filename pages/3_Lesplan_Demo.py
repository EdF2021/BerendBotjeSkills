import os 
import streamlit as st
from streamlit import sidebar
from core import ui
from ui import (
    wrap_doc_in_html,
    is_query_valid,
    is_file_valid,
    is_open_ai_key_valid,
    display_file_read_error,
)

from core.caching import bootstrap_caching
from core.parsing import read_file
from core.chunking import chunk_file
from core.embedding import embed_files
from core.utils import get_llm
from core.qa import query_folder
import tiktoken


EMBEDDING = "openai"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]


# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="Berend-Botje Skills", page_icon="📖", )
st.header("📖Berend-Botje Skills" )
st.subheader("- De Lesplanner - Waarom zou je moeilijk doen ....?")

st.markdown("###### De Lesplanner ondersteunt docenten bij het maken van een lesplan.")
st.markdown(
            "###### Hoe werkt De Lesplanner?\n"
            "1. Upload een pdf, docx, of txt file📄\n"
            "2. Stel je vraag over het document 💬\n"
            "3. Laat Berend je lesplan maken\n"
        )


# Enable caching for expensive functions
bootstrap_caching()

# sidebar()

sleutel = os.getenv("OPENAI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

st.session_state.get("OPENAI_API_KEY")


if not openai_api_key:
    st.warning(
        "Je hebt een geldig OpenAI API key nodig!"
        " https://platform.openai.com/account/api-keys."
    )


uploaded_file = st.file_uploader(
    "Upload een pdf, docx, or txt file",
    type=["pdf", "docx", "txt"],
    help="Gescande documenten worden nog niet ondersteund!",
)

model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")


if not uploaded_file:
    st.stop()

try:
    
    file = read_file(uploaded_file)
except Exception as e:
    display_file_read_error(e, file_name=uploaded_file.name)

chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

if not is_file_valid(file):
    st.stop()


if not is_open_ai_key_valid(openai_api_key, model):
    st.stop()


with st.spinner("Indexeren van het document... Dit kan even duren⏳"):
    folder_index = embed_files(
        files=[chunked_file],
        embedding=EMBEDDING if model != "debug" else "debug",
        vector_store=VECTOR_STORE if model != "debug" else "debug",
        openai_api_key=openai_api_key,
    )

with st.form(key="qa_form"):
    query = st.text_area("Stel hier je vraag.")
    submit = st.form_submit_button("Versturen")
    


if show_full_doc:
    with st.expander("Document"):
        # Hack to get around st.markdown rendering LaTeX
        st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


if submit:
    if not is_query_valid(query):
        st.stop()

    # Output Columns
    answer_col, sources_col = st.columns(2)

    llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
    result = query_folder(
        folder_index=folder_index,
        query=query,
        return_all=return_all_chunks,
        llm=llm,
    )

    with answer_col:
        st.markdown("#### Lesplan")
        st.markdown("> by ['Berend-Botje Skills']('https://berend-botje.online')")
        st.markdown(result.answer)

    with sources_col:
        st.markdown("#### Gebruikte bronnen")
        for source in result.sources:
            st.markdown(source.page_content)
            st.markdown(source.metadata["source"])
            st.markdown("---")
