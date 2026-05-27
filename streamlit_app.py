import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/upload"

st.set_page_config(
    page_title="Mangalens",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 Mangalens")
st.write("Envie uma imagem para tentar identificar o anime.")

uploaded_file = st.file_uploader(
    "Escolha uma imagem",
    type=["jpg", "jpeg", "png", "webp"]
)


if uploaded_file is not None:
    st.image(
        uploaded_file,
        caption="Imagem enviada",
        use_container_width=True
    )

    if st.button("Analisar imagem"):

        status_message = st.empty()

        progress_bar = st.progress(0)

        try:
            status_message.info("Preparando imagem...")
            progress_bar.progress(25)

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            status_message.info("Analisando imagem...")
            progress_bar.progress(50)

            response = requests.post(
                API_URL,
                files=files,
                timeout=30
            )

            status_message.info("Processando resposta...")
            progress_bar.progress(75)

            result = response.json()

            progress_bar.progress(100)
            status_message.empty()

            if result["success"]:
                trace_result = result["trace_moe_result"]["data"]

                st.success("Anime encontrado!")

                st.subheader(trace_result["anime"])

                st.write(f"**Episódio:** {trace_result['episode']}")
                st.write(f"**Similaridade:** {trace_result['similarity']}%")
                st.write(f"**Minutagem no episódio:** {trace_result['timestamp']}")

                if trace_result.get("preview"):
                    st.image(
                        trace_result["preview"],
                        caption="Frame encontrado pela API",
                        use_container_width=True
                    )

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

        except Exception:
            progress_bar.empty()
            status_message.empty()
            st.error("Erro inesperado ao analisar a imagem.")