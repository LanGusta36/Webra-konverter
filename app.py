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

    # Ideiglenes mentés a Pandoc számára
    temp_filename = f"temp.{extension}"
    with open(temp_filename, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        with st.spinner("Dokumentum elemzése..."):
            # A Pandoc-ot használjuk mindenre, mert az jobban kezeli a margókat
            # 'html5' formátum, de stílusok nélkül, hogy ne legyen 'szemetes'
            html_content = pypandoc.convert_file(temp_filename, 'html5', extra_args=['--body-only'])
            os.remove(temp_filename)
    except Exception as e:
        st.error(f"Hiba a konvertálás során: {e}")
        # Tartalék megoldás Mammoth-szal, ha a Pandoc elakadna
        if extension == "docx":
            result = mammoth.convert_to_html(uploaded_file)
            html_content = result.value

    # --- SPECIÁLIS VERS-FORMÁZÓ LOGIKA ---
    
    def fix_indentation(html):
        # 1. Keressük meg a tabulátorokat és alakítsuk át fix pixel alapú behúzássá
        # Egy tabulátor kb. 40px behúzásnak felel meg
        html = html.replace("\t", '<span style="display:inline-block; width:40px;"></span>')
        
        # 2. Ha sor eleji szóközöket találunk, alakítsuk át padding-re
        lines = html.split('\n')
        fixed_lines = []
        for line in lines:
            if line.startswith('<p> '):
                # Megszámoljuk a sor eleji szóközöket
                spaces = len(line) - len(line.lstrip('<p> '))
                padding = spaces * 10 # 1 szóköz kb 10px
                line = line.replace('<p>', f'<p style="padding-left: {padding}px; margin-bottom: 0;">')
            fixed_lines.append(line)
        
        return "\n".join(fixed_lines)

    html_content = fix_indentation(html_content)

    # SZÉTVÁLASZTÁS [TÖRZS] ALAPJÁN
    marker = "[TÖRZS]"
    
    if marker in html_content:
        parts = html_content.split(marker, 1)
        intro_html = parts[0].strip()
        body_html = parts[1].strip()
        
        # Tisztítás a kódvégeknél
        if intro_html.endswith('<p>'): intro_html = intro_html.rsplit('<p', 1)[0]
        if body_html.startswith("</p>"): body_html = body_html[4:]

        st.success("Feldolgozva! Próbáld meg ezt beilleszteni a forráskódba.")
        
        st.write("**1. Bevezető mezőbe:**")
        st.code(intro_html, language="html")

        st.write("**2. Cikktörzs mezőbe:**")
        st.code(body_html, language="html")
    else:
        st.warning("Nem találtam [TÖRZS] kulcsszót, íme a teljes kód:")
        st.code(html_content, language="html")
