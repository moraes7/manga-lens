import streamlit as st


def show_result(uploaded_file, trace_result):
    st.success("Anime encontrado!")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            uploaded_file,
            caption="Imagem enviada",
            use_container_width=True
        )

    with col2:
        if trace_result.get("preview"):
            st.image(
                trace_result["preview"],
                caption="Frame encontrado",
                use_container_width=True
            )

    st.divider()

    st.subheader(trace_result["anime"])

    st.write(f"**Episódio:** {trace_result['episode']}")
    st.write(f"**Similaridade:** {trace_result['similarity']}%")
    st.write(f"**Minutagem do episódio:** {trace_result['timestamp']}")