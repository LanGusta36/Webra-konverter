import streamlit as st
import mammoth
import io

st.set_page_config(page_title="Webra Cikk Konvertáló", page_icon="📝")

st.title("📝 Word -> Webra HTML Konvertáló")
st.write("Töltsd fel a Word dokumentumot, és másold ki a tiszta HTML kódot!")

uploaded_file = st.file_uploader("Válassz ki egy .docx fájlt", type="docx")

if uploaded_file is not None:
    # A fájl beolvasása
    bytes_data = uploaded_file.getvalue()
    docx_file = io.BytesIO(bytes_data)
    
    # Konvertálás Mammoth-tal
    style_map = """
    p[style-name='Title'] => h1:fresh
    p[style-name='Heading 1'] => h1:fresh
    p[style-name='Heading 2'] => h2:fresh
    p[style-name='Heading 3'] => h3:fresh
    """
    
    result = mammoth.convert_to_html(docx_file, style_map=style_map)
    html_code = result.value

    # Megjelenítés
    st.subheader("Generált HTML kód")
    st.code(html_code, language='html')
    
    st.success("Másold ki a fenti kódot, és illeszd be a Webra HTML nézetébe!")
    
    # Letöltési opció (ha fájlként kellene)
    st.download_button(
        label="HTML fájl letöltése",
        data=html_code,
        file_name="cikk.html",
        mime="text/html"
    )