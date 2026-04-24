import streamlit as st
import mammoth

st.set_page_config(page_title="Webra Okos Konvertáló", page_icon="🎓")

st.title("🎓 Webra Mind-az-egyben Konvertáló")
st.write("Töltsd fel az egyetlen Word fájlt, amiben egy vízszintes vonallal választottad el a bevezetőt a törzstől.")

uploaded_file = st.file_uploader("Válaszd ki a .docx fájlt", type="docx")

if uploaded_file is not None:
    # Stílusok beállítása (Címsorok -> h3)
    style_map = """
    p[style-name='Heading 1'] => h3:fresh
    p[style-name='Heading 2'] => h3:fresh
    p[style-name='Heading 3'] => h3:fresh
    p[style-name='Heading 4'] => h3:fresh
    p[style-name='Title'] => h3:fresh
    """
    
    # Teljes konvertálás
    result = mammoth.convert_to_html(uploaded_file, style_map=style_map)
    full_html = result.value

    # SZÉTVÁLASZTÁS A VONAL MENTÉN
    # A Mammoth a vízszintes vonalat <hr /> taggé alakítja
    if "<hr />" in full_html:
        parts = full_html.split("<hr />", 1)
        intro_html = parts[0].strip()
        body_html = parts[1].strip()
        
        st.success("Sikeresen szétválasztva!")
        
        st.subheader("Másolható kódok")

        # 1. Doboz: Bevezető
        st.write("**1. Bevezető mezőbe (HTML nézetbe):**")
        st.code(intro_html, language="html")

        # 2. Doboz: Cikktörzs
        st.write("**2. Cikktörzs mezőbe (HTML nézetbe):**")
        st.code(body_html, language="html")
        
    else:
        # Ha nem talál vonalat, mindent a törzsbe tesz, és figyelmeztet
        st.warning("Nem találtam vízszintes elválasztó vonalat a Wordben! Itt a teljes szöveg egyben:")
        st.write("**Cikktörzs (teljes):**")
        st.code(full_html, language="html")

else:
    st.info("Húzz egy vízszintes vonalat a Wordben a bevezető után, majd töltsd fel ide!")
