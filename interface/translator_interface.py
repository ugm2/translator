from numpy import isin
import streamlit as st
import requests
import json

def get_translation(sentences, target_lang):
    params = {'sentences': sentences, 'target_lang': target_lang}
    response = requests.post(
        "http://localhost:5001/translate",
        json=params
    )
    try:
        result = response.json()['translations']
    except:
        result = response.json()
    return result

def interface():
    st.header("Multilingual Translator")

    sentences = st.text_area("Input sentences separated by ';'",
                             value="Según el portal oficial de la organización, "
                                   "Microsoft tiene la intención de terminar formalmente "
                                   "sus operaciones contra Windows después del 14 de enero"
                                   " de 2020;\n"
                                   "根据该组织的官方门户网站，"
                                   "微软公司打算在2020年1月14日之后正式终止对Windows ")
    try:
        sentences = sentences.split(";")
        sentences = list(map(lambda s: s.replace('\n', '').strip(), sentences))
        target_lang = st.text_input("Input target language", value="en")
    except:
        st.error("Introduce sentences in the correct format")

    if st.button("Translate"):
        if len(sentences) > 0:
            with st.spinner("Sending request..."):
                translation = get_translation(sentences, target_lang)
            
            if translation:
                if isinstance(translation, list):
                    for s, tr in zip(sentences, translation):
                        st.write(f"### Original: \n{s}")
                        st.write(f"### Translation to '{target_lang}': \n{tr}")
                else:
                    st.error("Error: ", translation)
        else:
            st.warning("Empty sentences")

interface()