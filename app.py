import streamlit as st
import mammoth

st.set_page_config(page_title="Webra Formázó", page_icon="🎓")

st.title("🎓 Webra Tartalom Formázó")
st.write("Csak a kódolást igénylő mezőkhöz:")

# 1. MEZŐ: Bevezető (Alcím)
intro_input = st.text_area("1. Bevezető (Alcím) szövege", 
    placeholder="Ide másold a bevezetőt a Wordből...", 
    height=100)

st.divider()

# 2. MEZŐ: Cikktörzs (Fájlfeltöltés)
st.subheader("2. Cikktörzs generálása Wordből")
uploaded_file = st.file_uploader("Töltsd fel a .docx fájlt", type="docx")

if intro_input or uploaded_file:
    st.subheader("Másolható HTML kódok")

    # BEVEZETŐ KIMENET
    if intro_input:
        st.write("**Bevezető mezőbe:**")
        # Automatikusan körberakjuk <p> taggel a Webra miatt
        st.code(f"<p>{intro_input}</p>", language="html")

    # CIKKTÖRZS KIMENET
    if uploaded_file:
        # A Word címsorokat (Heading 1-4) h3-ra alakítjuk
        style_map = """
        p[style-name='Heading 1'] => h3:fresh
        p[style-name='Heading 2'] => h3:fresh
        p[style-name='Heading 3'] => h3:fresh
        p[style-name='Heading 4'] => h3:fresh
        p[style-name='Title'] => h3:fresh
        """
        
        result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
        body_html = result.value

        st.write("**Cikktörzs mezőbe:**")
        st.code(body_html, language="html")
        st.success("Kész! Csak másold ki a kódot.")
else:
    st.info("Várom a bevezetőt vagy a Word fájlt...")
