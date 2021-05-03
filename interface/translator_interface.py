import streamlit as st
import requests
import os
ai_port = os.environ.get('AI_PORT', 5003)

def get_translation(sentences, target_lang):
    params = {'sentences': sentences, 'target_lang': target_lang}
    response = requests.post(
        f"http://localhost:{ai_port}/translate",
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
                                   "sus operaciones con Windows después del 14 de enero de 2020;\n"
                                   "根据该组织的官方网站，"
                                   "微软计划在2020年1月14日之后正式终止其Windows运营")
    try:
        sentences = sentences.split(";")
        sentences = list(map(lambda s: s.replace('\n', '').strip(), sentences))
        sentences = [s for s in sentences if s]
        langs = """aav, aed, af, alv, am, ar, art, ase, az, bat, bcl, be,
                bem, ber, bg, bi, bn, bnt, bzs, ca, cau, ccs, ceb, cel, chk,
                cpf, crs, cs, csg, csn, cus, cy, da, de, dra, ee, efi, el, en,
                eo, es, et, eu, euq, fi, fj, fr, fse, ga, gaa, gil, gl, grk, guw,
                gv, ha, he, hi, hil, ho, hr, ht, hu, hy, id, ig, ilo, is, iso, it,
                ja, jap, ka, kab, kg, kj, kl, ko, kqn, kwn, kwy, lg, ln, loz, lt, lu,
                lua, lue, lun, luo, lus, lv, map, mfe, mfs, mg, mh, mk, mkh, ml, mos,
                mr, ms, mt, mul, ng, nic, niu, nl, no, nso, ny, nyk, om, pa, pag, pap,
                phi, pis, pl, pon, poz, pqe, pqw, prl, pt, rn, rnd, ro, roa, ru, run, rw,
                sal, sg, sh, sit, sk, sl, sm, sn, sq, srn, ss, ssp, st, sv, sw, swc, taw,
                tdt, th, ti, tiv, tl, tll, tn, to, toi, tpi, tr, trk, ts, tum, tut, tvl, tw,
                ty, tzo, uk, umb, ur, ve, vi, vsl, wa, wal, war, wls, xh, yap, yo, yua, zai,
                zh, zne"""
        langs = langs.split(',')
        langs = list(map(lambda s: s.replace('\n', '').strip(), langs))
        lang_index = langs.index('en')
        target_lang = st.selectbox("Select a target language", langs, index=lang_index)
    except:
        st.error("Introduce sentences and target language in the correct format")

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