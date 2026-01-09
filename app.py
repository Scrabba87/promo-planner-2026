import hmac
import streamlit as st
from datetime import date, timedelta
from collections import Counter

st.set_page_config(page_title="Promo Planner 2026", layout="wide")

# =========================
# CONFIG
# =========================
CLIENTE_DEFAULT = "Esselunga"
LOGO_PATH = "assets/royal.png"  # opzionale

ATTIVITA_LIST = [
    "TAGLIO PREZZO + EXTRA DISPLAY",
    "COLLECTION",
    "VOL + EXTRA DISPLAY",
    "TAGLIO PREZZO",
    "VOLANTINO",
]
CANALI = ["IPER", "SUPER", "SUPERETTE"]

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
# AUTH (AAM / ADMIN)
# =========================
def require_login():
    if "auth_ok" not in st.session_state:
        st.session_state.auth_ok = False
    if "role" not in st.session_state:
        st.session_state.role = "aam"

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
            st.session_state.page = "admin"
            st.session_state.admin_page = "admin_home"
            st.rerun()

        elif is_aam:
            st.session_state.auth_ok = True
            st.session_state.role = "aam"
            st.session_state.page = "home"
            st.session_state.admin_page = "admin_home"
            st.rerun()

        else:
            st.error("Credenziali non valide")

    st.stop()

require_login()


# =========================
# SESSION STORAGE
# =========================
if "piano2025_df" not in st.session_state:
    st.session_state.piano2025_df = None

if "admin_page" not in st.session_state:
    st.session_state.admin_page = "admin_home"


# =========================
# ROUTING
# =========================
PAGES = {
    "HOME CLIENTE": "home",
    "PIANO PROMO 2025": "piano_2025",
    "INSERIMENTO PROMO": "ins_promo",
    "CONSULTAZIONE PROMO IN BOZZA": "bozze",
    "CONSULTAZIONE PROMO DEF": "def",
    "ADMIN": "admin",
}

if "page" not in st.session_state:
    st.session_state.page = PAGES["HOME CLIENTE"]

def goto(page_key: str):
    st.session_state.page = page_key
    st.rerun()

def goto_admin(admin_key: str):
    st.session_state.page = "admin"
    st.session_state.admin_page = admin_key
    st.rerun()


# =========================
# SIDEBAR
# =========================
try:
    st.sidebar.image(LOGO_PATH, use_container_width=True)
except Exception:
    pass

st.sidebar.divider()

if st.session_state.get("role") == "admin":
    st.sidebar.markdown("### ADMIN — Ambienti")

    if st.sidebar.button("🏠 Admin Home", use_container_width=True):
        goto_admin("admin_home")

    if st.sidebar.button("⬆️ Upload Files", use_container_width=True):
        goto_admin("admin_upload")

    if st.sidebar.button("📚 Consultazione Piani Promo", use_container_width=True):
        goto_admin("admin_piani")

    if st.sidebar.button("🧾 WD Promo Review", use_container_width=True):
        goto_admin("admin_wd")

else:
    st.sidebar.markdown("### Navigazione")

    if st.sidebar.button("🏠 Home Cliente", use_container_width=True):
        goto("home")

    if st.sidebar.button("📅 Piano Promo 2025", use_container_width=True):
        goto("piano_2025")

    if st.sidebar.button("✍️ Inserimento Promo", use_container_width=True):
        goto("ins_promo")

    if st.sidebar.button("📝 Promo in Bozza", use_container_width=True):
        goto("bozze")

    if st.sidebar.button("✅ Promo Definitive", use_container_width=True):
        goto("def")

st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.auth_ok = False
    st.session_state.role = "aam"
    st.session_state.page = "home"
    st.session_state.admin_page = "admin_home"
    st.rerun()


# =========================
# HEADER
# =========================
if st.session_state.get("role") == "admin":
    st.title("Promo Planner 2026 — ADMIN PAGE")
else:
    st.title(f"Promo Planner 2026 — {CLIENTE_DEFAULT}")

page = st.session_state.page


# =========================
# ADMIN ENVIRONMENT
# =========================
if page == "admin":
    st.subheader("Seleziona ambiente di lavoro")

    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("⬆️ Upload Files", use_container_width=True):
            goto_admin("admin_upload")
    with a2:
        if st.button("📚 Consultazione Piani Promo", use_container_width=True):
            goto_admin("admin_piani")
    with a3:
        if st.button("🧾 WD Promo Review", use_container_width=True):
            goto_admin("admin_wd")

    st.divider()

    if st.session_state.admin_page == "admin_home":
        st.info("Seleziona un ambiente Admin.")

    elif st.session_state.admin_page == "admin_upload":
        st.subheader("Upload Files — Piano Promo 2025")

        import pandas as pd
        up = st.file_uploader("Carica Piano Promo 2025 (Excel / CSV)", type=["xlsx", "xls", "csv"])
        if up:
            df = pd.read_excel(up) if not up.name.lower().endswith(".csv") else pd.read_csv(up)
            df.columns = [str(c).strip() for c in df.columns]
            st.session_state.piano2025_df = df
            st.success("Piano Promo 2025 caricato correttamente ✅")

    elif st.session_state.admin_page == "admin_piani":
        st.info("Placeholder consultazione piani promo.")

    elif st.session_state.admin_page == "admin_wd":
        st.info("Placeholder WD Promo Review.")

    st.stop()


# =========================
# AAM ENVIRONMENT
# =========================
if page == "home":
    st.subheader("Seleziona ambiente di lavoro")
    if st.button("Piano Promo 2025"):
        goto("piano_2025")
    st.stop()

elif page == "piano_2025":
    st.subheader("Piano Promo 2025")

    df = st.session_state.piano2025_df
    if df is None:
        st.warning("Nessun piano caricato. Contatta l’Admin.")
        st.stop()

    st.dataframe(df, use_container_width=True, hide_index=True)
