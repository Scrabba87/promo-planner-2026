import streamlit as st

st.set_page_config(page_title="Promo Planner 2026", layout="wide")

st.title("Promo Planner 2026")
st.subheader("Cliente: Esselunga")

st.markdown("### Seleziona cosa vuoi fare")
choice = st.radio(
    "Scegli una sezione",
    ["LAST YEAR VIEW", "INSERIMENTO PROMO"],
    horizontal=True
)

if choice == "LAST YEAR VIEW":
    st.info("Qui vedrai cosa è stato promozionato lo scorso anno (placeholder)")
else:
    st.success("Qui inserirai una nuova promo (step successivo)")

