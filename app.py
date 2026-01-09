import hmac
import streamlit as st
from datetime import date, timedelta
from collections import Counter

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Promo Planner 2026", layout="wide")


# =========================
# AUTH (LOGIN GATE)
# =========================
def require_login():
    # init session
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False
    if "role" not in st.session_state:
        st.session_state.role = "aam"  # default

    # already logged in
    if st.session_state.auth_ok:
        return

    st.title("Accesso riservato")
    st.caption("Inserisci account e password per continuare.")

    user = st.text_input("Account")
    pwd = st.text_input("Password", type="password")

    if st.button("Entra", type="primary"):
        is_aam = (
            user == st.secrets.get("APP_USER", "")
            and hmac.compare_digest(pwd, st.secrets.get("APP_PASS", ""))
        )

        is_admin = (
            user == st.secrets.get("ADMIN_USER", "")
            and hmac.compare_digest(pwd, st.secrets.get("ADMIN_PASS", ""))
        )

        if is_admin:
            st.session_state.auth_ok = True
            st.session_state.role = "admin"
            st.rerun()
        elif is_aam:
            st.session_state.auth_ok = True
            st.session_state.role = "aam"
            st.rerun()
        else:
            st.error("Credenziali non valide")

    st.stop()


require_login()



# =========================
# CONFIG (hardcoded per ora)
# =========================
CLIENTE_DEFAULT = "Esselunga"

LOGO_PATH = "assets/royal.png"  # assicurati che esista in repo

ATTIVITA_LIST = [
    "TAGLIO PREZZO + EXTRA DISPLAY",
    "COLLECTION",
    "VOL + EXTRA DISPLAY",
    "TAGLIO PREZZO",
    "VOLANTINO",
]

CANALI = ["IPER", "SUPER", "SUPERETTE"]

# Prodotti demo (finché non carichiamo la lista vera)
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


def month_by_max_days(d1: date, d2: date) -> int:
    c = Counter()
    cur = d1
    while cur <= d2:
        c[(cur.year, cur.month)] += 1
        cur += timedelta(days=1)
    best = max(
        c.items(),
        key=lambda kv: (kv[1], 1 if kv[0] == (d1.year, d1.month) else 0),
    )[0]
    return best[1]


# =========================
# ROUTING
# =========================
PAGES = {
    "HOME CLIENTE": "home",
    "PIANO PROMO 2025": "piano_2025",
    "INSERIMENTO PROMO": "ins_promo",
    "CONSULTAZIONE PROMO IN BOZZA": "bozze",
    "CONSULTAZIONE PROMO DEF": "def",
}

if "page" not in st.session_state:
    st.session_state.page = PAGES["HOME CLIENTE"]


# =========================
# SIDEBAR (logo + nav + logout)
# =========================
try:
    st.sidebar.image(LOGO_PATH, use_container_width=True)
except Exception:
    st.sidebar.warning("Logo non trovato: controlla assets/royal.png")

st.sidebar.divider()
st.sidebar.caption(f"Cliente: {CLIENTE_DEFAULT} (per ora fisso)")

st.sidebar.markdown("### Navigazione")

if st.sidebar.button("🏠 Home Cliente", use_container_width=True):
    st.session_state.page = PAGES["HOME CLIENTE"]
    st.rerun()

if st.sidebar.button("📅 Piano Promo 2025", use_container_width=True):
    st.session_state.page = PAGES["PIANO PROMO 2025"]
    st.rerun()

if st.sidebar.button("✍️ Inserimento Promo", use_container_width=True):
    st.session_state.page = PAGES["INSERIMENTO PROMO"]
    st.rerun()

if st.sidebar.button("📝 Promo in Bozza", use_container_width=True):
    st.session_state.page = PAGES["CONSULTAZIONE PROMO IN BOZZA"]
    st.rerun()

if st.sidebar.button("✅ Promo Definitive", use_container_width=True):
    st.session_state.page = PAGES["CONSULTAZIONE PROMO DEF"]
    st.rerun()

st.sidebar.divider()

if st.session_state.get("role") == "admin":
    if st.sidebar.button("🛠️ Admin", use_container_width=True):
        st.session_state.page = "admin"
        st.rerun()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.auth_ok = False
    st.session_state.role = "aam"
    st.rerun()



# =========================
# HEADER
# =========================
st.title(f"Promo Planner 2026 — {CLIENTE_DEFAULT}")

page = st.session_state.page


# =========================
# HOME CLIENTE
# =========================
if page == "home":
    st.subheader("Seleziona ambiente di lavoro")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("1) Piano Promo 2025", use_container_width=True):
            st.session_state.page = PAGES["PIANO PROMO 2025"]
            st.rerun()
        if st.button("3) Consultazione promo in bozza", use_container_width=True):
            st.session_state.page = PAGES["CONSULTAZIONE PROMO IN BOZZA"]
            st.rerun()

    with c2:
        if st.button("2) Inserimento promo", type="primary", use_container_width=True):
            st.session_state.page = PAGES["INSERIMENTO PROMO"]
            st.rerun()
        if st.button("4) Consultazione promo definitive", use_container_width=True):
            st.session_state.page = PAGES["CONSULTAZIONE PROMO DEF"]
            st.rerun()

    st.info("Login AAM e scelta cliente verranno aggiunti successivamente.")
    st.stop()


# =========================
# PAGES
# =========================
if page == "piano_2025":
    st.subheader("Piano Promo 2025")
    st.info("Placeholder: qui mostreremo la Last Year View (per categoria e quando).")

elif page == "bozze":
    st.subheader("Consultazione Promo in bozza")
    st.info("Placeholder: qui vedremo le promo salvate in bozza (da DB).")

elif page == "def":
    st.subheader("Consultazione Promo definitive")
    st.info("Placeholder: qui vedremo le promo definitive / approvate (da DB).")

elif page == "ins_promo":
    st.subheader("Inserimento Promo")

    st.markdown("### 1) Sell-Out (definisce il mese)")
    so_start = st.date_input("SELL OUT data inizio", value=date(2026, 1, 1))
    so_end = st.date_input("SELL OUT data fine", value=date(2026, 1, 7))

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
        if st.checkbox(label, key=f"prod_{label}"):
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
            c1.selectbox("ATTIVITA'", ATTIVITA_LIST, key=f"att_{i}")
            clusters = c2.multiselect(
                "Dove attivi la promo (cluster)",
                CANALI,
                default=CANALI,
                key=f"cl_{i}",
            )

            st.number_input(
                "SCONTO POSIZIONAMENTO (manuale)",
                min_value=0.0,
                value=0.0,
                step=0.1,
                key=f"sp_{i}",
            )

            st.caption("Opzionali (fillabili manualmente)")
            o1, o2, o3, o4 = st.columns(4)
            o1.number_input("SCONTO A", min_value=0.0, value=0.0, step=0.1, key=f"sa_{i}")
            o2.number_input("SCONTO B", min_value=0.0, value=0.0, step=0.1, key=f"sb_{i}")
            o3.number_input("SC. IN FATT. %", min_value=0.0, value=0.0, step=0.1, key=f"sif_{i}")
            o4.number_input("SCONTO NC %", min_value=0.0, value=0.0, step=0.1, key=f"snc_{i}")

            st.markdown("**SELL IN (selezionabile)**")
            st.date_input("SELL IN data inizio", value=None, key=f"si_s_{i}")
            st.date_input("SELL IN data fine", value=None, key=f"si_e_{i}")

            if not clusters:
                st.error("Seleziona almeno un cluster per questo prodotto.")
                st.stop()

    st.success("Inserimento promo OK ✅ (prossimo step: salvataggio + export Excel)")





