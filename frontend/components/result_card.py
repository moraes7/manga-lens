import streamlit as st


def show_result(uploaded_file, trace_result):
    cover_url = trace_result.get("cover_url")

    st.markdown(
        """
        <style>
            .result-card {
                background-color: #111827;
                border-radius: 24px;
                padding: 40px 32px;
                text-align: center;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
                margin-bottom: 0;
                margin-top: 45px;
            }

            .result-status {
                display: inline-block;
                color: #22C55E; 
                border: 1px solid #22C55E;
                border-radius: 999px; 
                padding: 6px 14px; 
                font-size: 12px;
                font-weight: 700;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                margin-bottom: 20px;
            }

            .result-title {
                color: #F9FAFB;
                font-size: 36px;
                font-weight: 700;
                margin-bottom: 28px;
            }

            .cover-image {
                width: 150px;
            }

            .result-info {
                color: #E5E7EB;
                font-size: 18px;
                margin: 10px 0;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-status">Análise concluída</div>
            <div class="result-title">{trace_result["anime"]}</div>
            {f'<img class="cover-image" src="{cover_url}" />' if cover_url else ''}
            <div class="result-info">Similaridade: {trace_result["similarity"]}%</div>
            <div class="result-info">Episódio: {trace_result["episode"]}</div>
            <div class="result-info">Minutagem: {trace_result["timestamp"]}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    

    '''col1, col2 = st.columns(2)

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
            )'''