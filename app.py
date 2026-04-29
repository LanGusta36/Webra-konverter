import streamlit as st
import mammoth

st.set_page_config(page_title="Webra Konvertáló", page_icon="🎓")

st.title("🎓 Webra Okos Konvertáló")
st.write("Használd a `[TÖRZS]` kulcsszót a Wordben a bevezető és a cikktörzs elválasztásához!")

uploaded_file = st.file_uploader("Töltsd fel a .docx fájlt", type="docx")

if uploaded_file is not None:
    # Formázási szabályok: Címsorok -> h3
    style_map = """
    p[style-name='Heading 1'] => h3:fresh
    p[style-name='Heading 2'] => h3:fresh
    p[style-name='Heading 3'] => h3:fresh
    p[style-name='Heading 4'] => h3:fresh
    p[style-name='Title'] => h3:fresh
    """
    
    # Konvertálás HTML-lé
    result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
    full_html = result.value

    # SZÉTVÁLASZTÁS A KULCSSZÓ MENTÉN
    # A Mammoth valószínűleg <p>[TÖRZS]</p> formában fogja látni
    marker = "[TÖRZS]"
    
    if marker in full_html:
        # Kettévágjuk a szöveget a marker mentén
        # Megpróbáljuk elkapni a <p> taggel együtt is, ha a Mammoth belerakta
        if f"<p>{marker}</p>" in full_html:
            parts = full_html.split(f"<p>{marker}</p>", 1)
        else:
            parts = full_html.split(marker, 1)
            
        intro_html = parts[0].strip()
        body_html = parts[1].strip()
        
        st.success("Sikeresen szétválasztva a kulcsszó alapján!")
        
        # KIMENETEK
        st.subheader("Másolható kódok")

        st.write("**1. Bevezető mezőbe:**")
        st.code(intro_html, language="html")

        st.write("**2. Cikktörzs mezőbe:**")
        st.code(body_html, language="html")
        
    else:
        st.error(f"Hiba: Nem találom a `{marker}` kulcsszót a dokumentumban!")
        st.info("Kérlek, írd be a Wordbe a bevezető után egy külön sorba: [TÖRZS]")
        
        with st.expander("Nézd meg a generált teljes kódot"):
            st.code(full_html, language="html")

else:
    st.info("Töltsd fel a Word fájlt a kezdéshez!")
