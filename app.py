import streamlit as st
import mammoth
import pypandoc
import os
import re

st.set_page_config(page_title="Webra Konvertáló Pro", page_icon="🎓")

st.title("🎓 Webra Okos Konvertáló")

uploaded_file = st.file_uploader("Töltsd fel a Word fájlt (.doc vagy .docx)", type=["doc", "docx"])

if uploaded_file is not None:
    file_details = uploaded_file.name.split('.')
    extension = file_details[-1].lower()
    
    html_content = ""

    if extension == "docx":
        # Mammoth-szal kezdünk, de megkérjük, hogy ne törölje az üres részeket
        style_map = "p[style-name='Heading 1'] => h3:fresh \n p[style-name='Heading 2'] => h3:fresh \n p[style-name='Heading 3'] => h3:fresh"
        result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
        html_content = result.value
    else:
        with st.spinner("Régi .doc feldolgozása..."):
            with open("temp.doc", "wb") as f:
                f.write(uploaded_file.getbuffer())
            html_content = pypandoc.convert_file("temp.doc", 'html5')
            os.remove("temp.doc")

    # --- SPECIÁLIS FORMÁZÁS JAVÍTÁSA (VERSHEZ) ---
    # 1. Tabulátorok cseréje szóközökre (hogy a web is lássa)
    html_content = html_content.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # 2. CSS hozzáadása a bekezdésekhez, hogy tisztelje a szóközöket
    # Ezzel a trükkel a Webra kénytelen lesz megjeleníteni a behúzásokat
    html_content = html_content.replace("<p>", '<p style="white-space: pre-wrap; margin-bottom: 0.5em;">')

    # SZÉTVÁLASZTÁS [TÖRZS] ALAPJÁN
    marker = "[TÖRZS]"
    
    if marker in html_content:
        parts = html_content.split(marker, 1)
        intro_html = parts[0].strip()
        body_html = parts[1].strip()
        
        # Tisztítás a vágás után
        if intro_html.endswith('<p style="white-space: pre-wrap; margin-bottom: 0.5em;">'): 
            intro_html = intro_html.rsplit('<p', 1)[0]
        if body_html.startswith("</p>"): body_html = body_html[4:]

        st.success("Feldolgozva! A behúzások megmaradtak.")
        
        st.write("**1. Bevezető mezőbe:**")
        st.code(intro_html, language="html")

        st.write("**2. Cikktörzs mezőbe:**")
        st.code(body_html, language="html")
    else:
        st.warning("Nem találtam [TÖRZS] kulcsszót, íme a teljes kód:")
        st.code(html_content, language="html")

most így néz ki a kód, kiegészítenéd csak a tabulátoros résszel, semmilyen titlet ne változtass légyszi
