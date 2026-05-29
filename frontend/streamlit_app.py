import streamlit as st
import requests
from services.api import analyze_image
from components.result_card import show_result


ALLOWED_IMAGE_TYPES = [
    "image/jpeg",
    "image/png",
    "image/webp"
]


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
    st.write("Envie uma imagem para tentar identificar o anime.")

    uploaded_file = st.file_uploader(
        "Escolha uma imagem",
        type=["jpg", "jpeg", "png", "webp"]
    )

    if uploaded_file is not None:

        if uploaded_file.type not in ALLOWED_IMAGE_TYPES:
            st.error("Tipo de arquivo inválido. Envie uma imagem JPG, PNG ou WEBP.")

        else:
            if st.button("Analisar imagem"):

                status_message = st.empty()

                progress_bar = st.progress(0)

                try:
                    status_message.info("Preparando imagem...")
                    progress_bar.progress(25)

                    status_message.info("Analisando imagem...")
                    progress_bar.progress(50)

                    result = analyze_image(uploaded_file)

                    status_message.info("Processando resposta...")
                    progress_bar.progress(75)

                    progress_bar.progress(100)
                    status_message.empty()

                    if result["success"]:
                        trace_result = result["anime_result"]["data"]

                        st.session_state["uploaded_file"] = uploaded_file

                        st.session_state["trace_result"] = trace_result

                        st.session_state["tela"] = "resultado"

                        st.rerun()

                    else:
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
    show_result(
        st.session_state["uploaded_file"],
        st.session_state["trace_result"]
    )