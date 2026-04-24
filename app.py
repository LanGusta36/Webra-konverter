import streamlit as st

st.set_page_config(page_title="Webra Szöveg Formázó", page_icon="📝")

st.title("📝 Webra Szöveg Formázó")
st.write("Másold be a szövegeket a megfelelő helyre, és az app legenerálja a Webra-kompatibilis kódokat.")

# --- BEVITEL ---
title_input = st.text_input("1. Cikk címe", placeholder="Ide másold a főcímet...")

intro_input = st.text_area("2. Bevezető (Alcím)", placeholder="Ide másold a rövid bevezető szöveget...", height=100)

body_input = st.text_area("3. Cikktörzs szövege", 
    placeholder="Ide jöhet a cikk teljes szövege. A címsorokat hagyd meg külön sorban!", 
    height=300)

st.divider()

# --- FELDOLGOZÁS ---

def clean_body_conversion(text):
    if not text:
        return ""
    
    lines = text.split('\n')
    html_output = []
    
    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        
        # Logika: Ha a sor kérdőjellel végződik vagy viszonylag rövid, legyen H3
        # Ezt bármikor módosíthatjuk, ha más szabályt szeretnél
        if clean_line.endswith('?') or len(clean_line) < 60:
            html_output.append(f"<h3>{clean_line}</h3>")
        else:
            html_output.append(f"<p>{clean_line}</p>")
            
    return "\n".join(html_output)

# --- MEGJELENÍTÉS / KIMENET ---

if title_input or intro_input or body_input:
    st.subheader("Másolható kódok")

    # CÍM
    st.write("**Cikk címe (Csak szöveg):**")
    st.code(title_input)

    # BEVEZETŐ
    if intro_input:
        st.write("**Bevezető mező:**")
        st.code(f"<p>{intro_input}</p>", language="html")

    # CIKKTÖRZS
    if body_input:
        st.write("**Cikktörzs mező:**")
        body_html = clean_body_conversion(body_input)
        st.code(body_html, language="html")

    st.success("Tipp: Kattints a kódblokkok jobb felső sarkában lévő ikonra a másoláshoz!")
else:
    st.info("Várom a szövegeket...")

# A requirements.txt-ből most már ki is veheted a 'mammoth' sort, 
# de ha benne marad, az sem okoz hibát.
