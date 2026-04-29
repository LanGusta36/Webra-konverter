import streamlit as st
import mammoth
import pypandoc
import os
import re

st.set_page_config(page_title="Webra Konvertáló", page_icon="🎓")

st.title("🎓 Webra Okos Konvertáló")

uploaded_file = st.file_uploader("Töltsd fel a Word fájlt (.doc vagy .docx)", type=["doc", "docx"])

if uploaded_file is not None:
    file_details = uploaded_file.name.split('.')
    extension = file_details[-1].lower()
    
    html_content = ""

    if extension == "docx":
        # Mammoth konvertálás
        style_map = "p[style-name='Heading 1'] => h3:fresh \n p[style-name='Heading 2'] => h3:fresh \n p[style-name='Heading 3'] => h3:fresh"
        result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
        html_content = result.value
    else:
        with st.spinner("Régi .doc feldolgozása..."):
            with open("temp.doc", "wb") as f:
                f.write(uploaded_file.getbuffer())
            html_content = pypandoc.convert_file("temp.doc", 'html5')
            os.remove("temp.doc")

    # --- SPECIÁLIS FORMÁZÁS JAVÍTÁSA (TABULÁTOROK FIXÁLÁSA) ---
    
    # 1. A tabulátorokat 4 kemény szóközre cseréljük
    html_content = html_content.replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
    
    # 2. A sor eleji és egymás melletti szóközök "keményítése"
    # Regex: Csak a tageken ( < > ) kívüli szóközöket bántjuk
    def hard_space_fix(text):
        # Minden két vagy több szóközt kicserélünk kemény szóközökre
        text = re.sub(r' {2,}', lambda m: "&nbsp;" * len(m.group(0)), text)
        # A bekezdések elején lévő szóközöket is keményítjük (ha maradt ilyen)
        text = text.replace("> ", ">&nbsp;")
        return text

    html_content = hard_space_fix(html_content)
    
    # 3. Biztonsági tartalék: white-space stílus (ha a Webra mégis átengedné)
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

        st.success("Feldolgozva! A behúzások most már 'kőbe vannak vésve'.")
        
        st.write("**1. Bevezető mezőbe:**")
        st.code(intro_html, language="html")

        st.write("**2. Cikktörzs mezőbe:**")
        st.code(body_html, language="html")
    else:
        st.warning("Nem találtam [TÖRZS] kulcsszót, íme a teljes kód:")
        st.code(html_content, language="html")
