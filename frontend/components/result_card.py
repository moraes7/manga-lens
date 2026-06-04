import streamlit as st


def show_result(uploaded_file, trace_result):
    cover_url = trace_result.get("cover_url")

    st.markdown(
        """
        <style>
            .result-card {
                background-color: #111827;
                border-radius: 24px;
                padding: 32px 32px;
                text-align: center;
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.25);
                margin-bottom: 16px;
                margin-top: 16px;
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

            .cover-placeholder {
                width: 150px;
                min-height: 220px;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px auto;
                padding: 20px;
                border: 1px dashed #4B5563;
                border-radius: 12px;
                color: #9CA3AF;
                font-size: 14px;
                text-align: center;
            }

            .result-info {
                color: #E5E7EB;
                font-size: 18px;
                margin: 10px 0;
            }

            div.stButton > button {
                width: auto;
                padding: 6px 16px;
                border-radius: 10px;
                background-color: transparent;
                color: #60A5FA;
                border: 1px solid #60A5FA;
                font-weight: 700;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    button_col_left, button_col_center, button_col_right = st.columns([2, 1, 2])

    with button_col_center:
        new_analysis = st.button("Nova análise")

        result_html = f"""
            <div class="result-card">
            <div class="result-status">Análise concluída</div>
            <div class="result-title">{trace_result["anime"]}</div>
            {f'<img class="cover-image" src="{cover_url}" />' if cover_url else '<div class="cover-placeholder">Capa indisponível</div>'}
            <div class="result-info">Similaridade: {trace_result["similarity"]}%</div>
            <div class="result-info">Episódio: {trace_result["episode"]}</div>
            <div class="result-info">Minutagem: {trace_result["timestamp"]}</div>
            </div>
        """

    st.markdown(result_html, unsafe_allow_html=True)

    return new_analysis