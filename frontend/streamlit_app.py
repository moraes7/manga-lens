import streamlit as st
import requests
import time
from services.api import analyze_image
from components.result_card import show_result


ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
]

def animate_progress(progress_bar, status_message):
    status_message.info("🔍 Analisando imagem...")
    for progress in range(0, 31, 5):
        progress_bar.progress(progress)
        time.sleep(0.18)

    status_message.info("📚 Buscando obra...")
    for progress in range(35, 61, 5):
        progress_bar.progress(progress)
        time.sleep(0.08)


st.set_page_config(
    page_title="Mangalens",
    page_icon="🔍",
    layout="centered"
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)


if "tela" not in st.session_state:
    st.session_state["tela"] = "upload"


if st.session_state["tela"] == "upload":

    st.title("🔍 Mangalens")
    st.write("Envie uma imagem para tentar identificar o anime ou mangá.")

    uploaded_file = st.file_uploader(
        "Escolha uma imagem",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, width=150) 

    if uploaded_file is not None:

        if uploaded_file.type not in ALLOWED_IMAGE_TYPES:
            st.error("Tipo de arquivo inválido. Envie uma imagem JPG, PNG ou WEBP.")

        else:
            if st.button("Analisar imagem"):
                status_message = st.empty()

                progress_bar = st.progress(0)

                try:
                    animate_progress(progress_bar, status_message)

                    result = analyze_image(uploaded_file)

                    if result["success"]:
                        status_message.info("📝 Preparando resultado...")
                        for progress in range(35, 61, 5):
                            progress_bar.progress(progress)
                            time.sleep(0.18)
                        
                        time.sleep(0.05)    
                        
                        status_message.empty()
                        progress_bar.empty()

                        trace_result = result["anime_result"]["data"]

                        st.session_state["uploaded_file"] = uploaded_file

                        st.session_state["trace_result"] = trace_result

                        st.session_state["tela"] = "resultado"

                        st.rerun()

                    else:
                        progress_bar.empty()
                        status_message.empty()
                        st.error(result["message"])

                except requests.exceptions.ConnectionError:
                    progress_bar.empty()
                    status_message.empty()
                    st.error("Não foi possível conectar ao servidor.")

                except requests.exceptions.Timeout:
                    progress_bar.empty()
                    status_message.empty()
                    st.error("A análise demorou muito para responder.")

                except Exception as error:
                    progress_bar.empty()
                    status_message.empty()
                    st.error("Erro inesperado ao analisar a imagem.")
                    st.exception(error)


elif st.session_state["tela"] == "resultado":
    new_analysis = show_result(
        st.session_state["uploaded_file"],
        st.session_state["trace_result"]
    )

    if new_analysis:
        st.session_state.pop("uploaded_file", None)

        st.session_state.pop("trace_result", None)

        st.session_state["tela"] = "upload"

        st.rerun()