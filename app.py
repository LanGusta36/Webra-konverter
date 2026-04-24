import streamlit as st
import mammoth

st.set_page_config(page_title="Webra Formázó v2", page_icon="🎓")

st.title("🎓 Webra Cikk Formázó")
st.write("Ez a verzió a Word stílusok alapján (Címsor 1, 2, 3) generál HTML-t.")

# 1. MEZŐ: Cikk címe (Sima szöveg)
title_input = st.text_input("1. Cikk címe", placeholder="Másold ide a címet a Wordből...")

# 2. MEZŐ: Bevezető (Alcím)
intro_input = st.text_area("2. Bevezető (Alcím) - Ez <p> tagbe kerül", placeholder="Ide jön a rövid bevezető...", height=100)

st.divider()

# 3. MEZŐ: Cikktörzs (Fájlfeltöltés a formázás megőrzése miatt)
st.subheader("3. Cikktörzs generálása")
st.info("Töltsd fel a Word fájlt, hogy a program felismerje a címsorokat!")
uploaded_file = st.file_uploader("Válaszd ki a .docx fájlt", type="docx")

if uploaded_file is not None:
    # Itt mondjuk meg, hogy minden Word címsorból (H1, H2, H3) legyen <h3>
    style_map = """
    p[style-name='Heading 1'] => h3:fresh
    p[style-name='Heading 2'] => h3:fresh
    p[style-name='Heading 3'] => h3:fresh
    p[style-name='Heading 4'] => h3:fresh
    p[style-name='Title'] => h3:fresh
    """
    
    # Konvertálás (képek nélkül)
    result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
    body_html = result.value

    # Megjelenítés
    st.success("HTML generálva!")
    
    # Kimenetek
    st.write("### Másolható kódok a Webrához:")
    
    st.write("**Cikk címe:**")
    st.code(title_input)

    st.write("**Bevezető mezőbe:**")
    st.code(f"<p>{intro_input}</p>", language="html")

    st.write("**Cikktörzs mezőbe:**")
    st.code(body_html, language="html")
    
else:
    st.warning("A cikktörzs generálásához töltsd fel a Word fájlt!")
