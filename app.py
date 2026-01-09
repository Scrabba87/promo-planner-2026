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
        st.session_state.role = "aam"  # default

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
# SESSION STORAGE (per ora in memoria)
# =========================
if "piano2025_df" not in st.session_state:
    st.session_state.piano2025_df = None

# stato navigazione admin
if "admin_page" not in st.session_state:
    st.session_state.admin_page = "admin_home"  # admin_home, admin_upload, admin_piani, admin_wd


# =========================
# ROUTING (AAM)
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
    st.session_state.page = PAGES["ADMIN"]
    st.session_state.admin_page = admin_key
    st.rerun()


# =========================
# SIDEBAR
# =========================
try:
    st.sidebar.image(LOGO_PATH, use_container_width=True)
except Exception:
    pass

st.sidebar.caption(f"Cliente: {CLIENTE_DEFAULT}")

st.sidebar.divider()

# Sidebar diversa per ruolo
if st.session_state.get("role") == "admin":
    st.sidebar.markdown("### Admin — Ambienti")

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
        goto(PAGES["HOME CLIENTE"])

    if st.sidebar.button("📅 Piano Promo 2025", use_container_width=True):
        goto(PAGES["PIANO PROMO 2025"])

    if st.sidebar.button("✍️ Inserimento Promo", use_container_width=True):
        goto(PAGES["INSERIMENTO PROMO"])

    if st.sidebar.button("📝 Promo in Bozza", use_container_width=True):
        goto(PAGES["CONSULTAZIONE PROMO IN BOZZA"])

    if st.sidebar.button("✅ Promo Definitive", use_container_width=True):
        goto(PAGES["CONSULTAZIONE PROMO DEF"])

st.sidebar.divider()

if st.sidebar.button("🚪 Logout", use_container_width=True):
    st.session_state.auth_ok = False
    st.session_state.role = "aam"
    st.session_state.page = PAGES["HOME CLIENTE"]
    st.session_state.admin_page = "admin_home"
    st.rerun()


# =========================
# HEADER (diverso per ruolo)
# =========================
if st.session_state.get("role") == "admin":
    st.title("Promo Planner 2026 — ADMIN PAGE")
else:
    st.title(f"Promo Planner 2026 — {CLIENTE_DEFAULT}")

page = st.session_state.page


# =========================
# ADMIN PAGES (ambiente separato)
# =========================
if page == "admin":
    if st.session_state.get("role") != "admin":
        st.error("Accesso non autorizzato.")
        st.stop()

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

    admin_page = st.session_state.admin_page

    if admin_page == "admin_home":
        st.info("Seleziona un ambiente (Upload Files / Consultazione Piani Promo / WD Promo Review).")

    elif admin_page == "admin_upload":
        st.subheader("Upload Files")
        st.caption("Qui carichiamo i file che alimentano le viste AAM. (Per ora: Piano Promo 2025)")

        import pandas as pd

        up = st.file_uploader("Carica Piano Promo 2025 (Excel o CSV)", type=["xlsx", "xls", "csv"])
        if up is not None:
            try:
                if up.name.lower().endswith(".csv"):
                    df = pd.read_csv(up)
                else:
                    df = pd.read_excel(up, sheet_name=0)
            except Exception as e:
                st.error(f"Errore lettura file: {e}")
                st.stop()

            df.columns = [str(c).strip() for c in df.columns]
            st.session_state.piano2025_df = df
            st.success(f"Piano Promo 2025 caricato ✅ Righe: {len(df):,} | Colonne: {len(df.columns)}")

        if st.session_state.piano2025_df is not None:
            with st.expander("Preview (prime 20 righe)"):
                st.dataframe(st.session_state.piano2025_df.head(20), use_container_width=True, hide_index=True)

        st.divider()
        st.info("Prossimi file (placeholder): Lista Prodotti, WD Cliente, Mapping cluster, ecc.")

    elif admin_page == "admin_piani":
        st.subheader("Consultazione Piani Promo")
        st.info("Placeholder: qui metteremo la consultazione piani per cliente/anno/versione.")

    elif admin_page == "admin_wd":
        st.subheader("WD Promo Review")
        st.info("Placeholder: qui metteremo il controllo WD / coerenza promo / match con piani.")

    st.stop()


# =========================
# AAM PAGES (come ora)
# =========================
if page == "home":
    st.subheader("Seleziona ambiente di lavoro")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("1) Piano Promo 2025", use_container_width=True):
            goto(PAGES["PIANO PROMO 2025"])
        if st.button("3) Consultazione promo in bozza", use_container_width=True):
            goto(PAGES["CONSULTAZIONE PROMO IN BOZZA"])

    with c2:
        if st.button("2) Inserimento promo", type="primary", use_container_width=True):
            goto(PAGES["INSERIMENTO PROMO"])
        if st.button("4) Consultazione promo definitive", use_container_width=True):
            goto(PAGES["CONSULTAZIONE PROMO DEF"])

    st.info("Login AAM e scelta cliente verranno aggiunti successivamente.")
    st.stop()


elif page == "piano_2025":
    st.subheader("Piano Promo 2025 (Consultazione)")

    df = st.session_state.piano2025_df
    if df is None:
        st.warning("Nessun Piano Promo 2025 caricato. Chiedi all’Admin di caricarlo nella pagina Admin > Upload Files.")
        st.stop()

    st.success(f"Dati disponibili ✅ Righe: {len(df):,} | Colonne: {len(df.columns)}")

    with st.expander("Vedi elenco colonne"):
        st.write([str(c) for c in df.columns])

    df_f = df.copy()
    df_f.columns = [str(c).strip() for c in df_f.columns]

    def pick_col(options):
        for c in df_f.columns:
            if c.lower() in options:
                return c
        return None

    cat_col = pick_col({"categoria", "category"})
    act_col = pick_col({"attivita", "attività", "attivita'", "activity"})
    clu_col = pick_col({"cluster", "canale", "channel"})

    st.markdown("### Filtri")
    f1, f2, f3 = st.columns(3)

    if cat_col:
        cats = sorted(df_f[cat_col].dropna().astype(str).str.strip().unique().tolist())
        sel = f1.multiselect("Categoria", cats, default=[])
        if sel:
            df_f = df_f[df_f[cat_col].astype(str).str.strip().isin(sel)]
    else:
        f1.caption("Categoria: colonna non trovata (la mappiamo dopo)")

    if act_col:
        acts = sorted(df_f[act_col].dropna().astype(str).str.strip().unique().tolist())
        sel = f2.multiselect("Attività", acts, default=[])
        if sel:
            df_f = df_f[df_f[act_col].astype(str).str.strip().isin(sel)]
    else:
        f2.caption("Attività: colonna non trovata (la mappiamo dopo)")

    if clu_col:
        clus = sorted(df_f[clu_col].dropna().astype(str).str.strip().unique().tolist())
        sel = f3.multiselect("Cluster/Canale", clus, default=[])
        if sel:
            df_f = df_f[df_f[clu_col].astype(str).str.strip().isin(sel)]
    else:
        f3.caption("Cluster/Canale: colonna non trovata (la mappiamo dopo)")

    st.markdown("### Tabella")
    st.dataframe(df_f, use_container_width=True, hide_index=True)

    st.download_button(
        "Scarica vista filtrata (CSV)",
        data=df_f.to_csv(index=False).encode("utf-8"),
        file_name="piano_promo_2025_filtrato.csv",
        mime="text/csv",
    )


elif page == "bozze":
    st.subheader("Consultazione Promo in bozza")
    st.info("Placeholder: qui vedremo le promo salvate in bozza.")


elif page == "def":
    st.subheader("Consultazione Promo definitive")
    st.info("Placeholder: qui vedremo le promo definitive / approvate.")


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
