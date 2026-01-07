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
    import streamlit as st
from datetime import date, timedelta
from collections import Counter

ATTIVITA_LIST = [
  "TAGLIO PREZZO + EXTRA DISPLAY",
  "COLLECTION",
  "VOL + EXTRA DISPLAY",
  "TAGLIO PREZZO",
  "VOLANTINO",
]

PRODOTTI_DEMO = {
  "SOFT DRINKS": [
    {"SAP COD": "SAP001", "CODICE SAP": "CSAP001", "FORMATO 1": "33cl"},
    {"SAP COD": "SAP002", "CODICE SAP": "CSAP002", "FORMATO 1": "1L"},
  ],
  "BIRRA": [
    {"SAP COD": "SAP101", "CODICE SAP": "CSAP101", "FORMATO 1": "66cl"},
  ],
  "ENERGY": [
    {"SAP COD": "SAP201", "CODICE SAP": "CSAP201", "FORMATO 1": "25cl"},
  ],
}

CANALI = ["IPER", "SUPER", "SUPERETTE"]

def month_by_max_days(d1: date, d2: date) -> int:
    c = Counter()
    cur = d1
    while cur <= d2:
        c[(cur.year, cur.month)] += 1
        cur += timedelta(days=1)
    best = max(c.items(), key=lambda kv: (kv[1], 1 if kv[0]==(d1.year,d1.month) else 0))[0]
    return best[1]

st.markdown("## Inserimento Promo")

st.markdown("### 1) Sell-Out (definisce il mese)")
so_start = st.date_input("SELL OUT data inizio", value=date(2026,1,1))
so_end   = st.date_input("SELL OUT data fine", value=date(2026,1,7))

if so_end < so_start:
    st.error("Errore: SELL OUT data fine < data inizio")
    st.stop()

mese_so = month_by_max_days(so_start, so_end)
st.success(f"Mese Sell-Out calcolato: **{mese_so}**")

st.markdown("### 2) Categoria")
categoria = st.selectbox("Seleziona categoria", list(PRODOTTI_DEMO.keys()))

st.markdown("### 3) Prodotti della categoria (tick)")
prodotti = PRODOTTI_DEMO[categoria]

selected = []
for p in prodotti:
    label = f'{p["SAP COD"]} | {p["CODICE SAP"]} | {p["FORMATO 1"]}'
    if st.checkbox(label, key=label):
        selected.append(p)

if not selected:
    st.warning("Seleziona almeno un prodotto.")
    st.stop()

st.divider()
st.markdown("### 4) Dettagli promo per prodotto")

for i, p in enumerate(selected, start=1):
    label = f'{p["SAP COD"]} | {p["CODICE SAP"]} | {p["FORMATO 1"]}'
    with st.expander(f"Prodotto {i}: {label}", expanded=True):
        c1, c2 = st.columns(2)
        att = c1.selectbox("ATTIVITA'", ATTIVITA_LIST, key=f"att_{i}")
        clusters = c2.multiselect("Dove attivi la promo (cluster)", CANALI, default=CANALI, key=f"cl_{i}")

        sconto_pos = st.number_input("SCONTO POSIZIONAMENTO (manuale)", min_value=0.0, value=0.0, step=0.1, key=f"sp_{i}")

        st.caption("Opzionali (fillabili manualmente)")
        o1, o2, o3, o4 = st.columns(4)
        o1.number_input("SCONTO A", min_value=0.0, value=0.0, step=0.1, key=f"sa_{i}")
        o2.number_input("SCONTO B", min_value=0.0, value=0.0, step=0.1, key=f"sb_{i}")
        o3.number_input("SC. IN FATT. %", min_value=0.0, value=0.0, step=0.1, key=f"sif_{i}")
        o4.number_input("SCONTO NC %", min_value=0.0, value=0.0, step=0.1, key=f"snc_{i}")

        st.markdown("**SELL IN (selezionabile)**")
        si_start = st.date_input("SELL IN data inizio", value=None, key=f"si_s_{i}")
        si_end   = st.date_input("SELL IN data fine", value=None, key=f"si_e_{i}")

        if not clusters:
            st.error("Seleziona almeno un cluster per questo prodotto.")
            st.stop()

st.success("Schermata inserimento promo OK ✅ (prossimo step: salvataggio + export Excel)")


