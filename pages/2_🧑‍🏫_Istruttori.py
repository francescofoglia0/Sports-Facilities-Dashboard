import streamlit as st
from utils.utils import *
import pandas as pd
import datetime

if __name__ == "__main__":
    st.title("🧑‍🏫 Team Istruttori")

    if check_connection():
        col1, col2 = st.columns(2)
        cognome_ricerca = col1.text_input("Filtra per cognome:")
        
        # recupero date
        date_res = execute_query(st.session_state["connection"], "SELECT MIN(DataNascita) as min_d, MAX(DataNascita) as max_d FROM ISTRUTTORE").mappings().first()
        min_date = date_res['min_d'] if date_res['min_d'] else datetime.date(1950, 1, 1)
        max_date = date_res['max_d'] if date_res['max_d'] else datetime.date.today()

        # divido il col2 in due mini-colonne per avere due date separate
        scol1, scol2 = col2.columns(2)
        data_inizio = scol1.date_input("Nato dal:", value=min_date, min_value=min_date, max_value=max_date)
        data_fine = scol2.date_input("Nato fino al:", value=max_date, min_value=min_date, max_value=max_date)

        query = "SELECT * FROM ISTRUTTORE WHERE 1=1"
        
        if cognome_ricerca:
            query += f" AND Cognome LIKE '%{cognome_ricerca}%'"
        
        # uso le due date singole
        if data_inizio and data_fine:
            query += f" AND DataNascita >= '{data_inizio}' AND DataNascita <= '{data_fine}'"

        istr_res = execute_query(st.session_state["connection"], query)
        df_istr = pd.DataFrame(istr_res)

        if df_istr.empty:
            st.warning("Nessun istruttore trovato.", icon='⚠️')
        else:
            # iterrows e non tabella generale
            for index, row in df_istr.iterrows():
                c_icon, c_dati = st.columns([1, 8])
                c_icon.markdown("<h1>🏃</h1>", unsafe_allow_html=True)
                c_dati.markdown(f"**{row['Nome']} {row['Cognome']}**")
                c_dati.markdown(f"📧 `{row['Email']}` | 🎂 Data di Nascita: {row['DataNascita']}")
                st.divider()