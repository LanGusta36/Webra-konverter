import streamlit as st
import mammoth
import io
from datetime import datetime

st.set_page_config(page_title="Webra Publikáló Segéd", page_icon="🎓")

# --- SEGÉDFÜGGVÉNYEK ---
def get_webra_path():
    now = datetime.now()
    # Példa: site/upload/2026/04/
    return f"site/upload/{now.year}/{now.strftime('%m')}/"

def generate_img_tag(filename, is_cover=True):
    path = get_webra_path()
    if is_cover:
        # A te példád alapján a borítókép kódja
        return f'<img id="img_gen_{datetime.now().strftime("%S%f")}" name="{path}{filename}" src="{path}{filename}" alt="{filename}" title="{filename}" width="900" height="506" style=""/>'
    else:
        # Cikktörzsbe szánt középre zárt kép
        return f'<p><img id="img_gen_{datetime.now().strftime("%S%f")}" name="{path}{filename}" src="{path}{filename}" alt="{filename}" title="{filename}" width="450" height="330" style="display: block; margin-left: auto; margin-right: auto;"/></p>'

# --- UI ---
st.title("🎓 SZTE Alma Mater - Webra Formázó")

col1, col2 = st.columns(2)

with col1:
    title = st.text_input("1. Cikk címe (Főcím)", placeholder="Másold ide a címet...")
    intro = st.text_area("2. Bevezető (Alcím)", placeholder="Ide jön a rövid kedvcsináló...")

with col2:
    cover_name = st.text_input("3. Borítókép fájlneve", placeholder="pl. boritokep.jpg")
    st.info(f"Várható útvonal: {get_webra_path()}")

st.divider()

uploaded_file = st.file_uploader("4. Cikktörzs feltöltése (Word dokumentum)", type="docx")

if st.button("HTML Kódok Generálása") or uploaded_file:
    if uploaded_file:
        # Cikktörzs konvertálása
        style_map = """
        p[style-name='Heading 1'] => h3:fresh
        p[style-name='Heading 2'] => h3:fresh
        p[style-name='Heading 3'] => h3:fresh
        """
        result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
        body_html = result.value
        
        # Eredmények megjelenítése boxokban
        st.subheader("Másold ki a kódokat a Webrába:")

        # CÍM (Sima szöveg, de legyen meg)
        st.write("**Cikk címe:**")
        st.code(title)

        # BEVEZETŐ
        st.write("**Bevezető mezőbe:**")
        st.code(f"<p>{intro}</p>")

        # KÉP (Rövid bevezető mező)
        if cover_name:
            st.write("**Rövid bevezetőhöz (Kép kód):**")
            st.code(generate_img_tag(cover_name, is_cover=True))

        # CIKKTÖRZS
        st.write("**Cikktörzs mezőbe:**")
        st.code(body_html, language="html")

        # EXTRA: Kép beszúró segéd a cikktörzshöz
        st.divider()
        st.subheader("Képkód generátor a cikktörzshöz")
        extra_img = st.text_input("Belső kép fájlneve (ha van)", key="inner_img")
        if extra_img:
            st.code(generate_img_tag(extra_img, is_cover=False))
