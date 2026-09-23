import streamlit as st
from utils.utils import *
import pandas as pd


if __name__ == "__main__":
    
    # configurazione della pagina con i menu del dipartimento
    st.set_page_config(
        page_title="Dashboard Palestra",
        layout="wide",
        page_icon="🏠",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://dbdmg.polito.it/',
            'Report a bug': "https://dbdmg.polito.it/",
            'About': "# Laboratorio di *Basi di Dati*"
        }
    )

    # layout dell'header con titolo e credenziali
    col1, col2 = st.columns([3, 2])
    with col1:
        st.title(":red[Dashboard] Centro sportivo")
        st.markdown("## Corso di :blue[Basi di dati]")
        st.markdown("#### Studente: Francesco Foglia")
        
        st.markdown("""
        **Specifiche del progetto:**
        * Laboratorio: sviluppo di una dashboard multi-pagina interfacciata con DBMS MySQL.
        * Obiettivo: visualizzazione, filtraggio, inserimento e verifica di nuovi dati nelle tabelle del DB.
        """)
    with col2:
        st.image("images/polito.png")
        
    # controllo session state per la connessione
    if "connection" not in st.session_state.keys():
        st.session_state["connection"] = False

    # se siamo connessi mostriamo l'analisi grafica
    if check_connection():
        st.divider()
        st.subheader("📊 Analisi Lezioni")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("#### Distribuzione Oraria")
            query_orari = "SELECT OrarioInizio as Orario_Inizio, COUNT(*) as Numero_Lezioni FROM PROGRAMMA GROUP BY OrarioInizio ORDER BY OrarioInizio"
            orari_result = execute_query(st.session_state["connection"], query_orari)
            df_orari = pd.DataFrame(orari_result)
            
            if df_orari.empty:
                st.info("Nessuna lezione in programma.")
            else:
                # converti in stringa
                df_orari['Orario_Inizio'] = df_orari['Orario_Inizio'].astype(str)
                
                # se avevo (e.g. "0 days 11:00:00") viene pulito e
                # mantiene solo la parte dell'orario (hh:mm:ss)
                df_orari['Orario_Inizio'] = df_orari['Orario_Inizio'].apply(lambda x: str(x).split()[-1])
                
                st.area_chart(df_orari, x="Orario_Inizio", y="Numero_Lezioni")
        with c2:
            st.markdown("#### Lezioni Settimanali")
            
            # query per il conteggio delle lezioni per giorno della settimana
            query_giorni = """
                SELECT Giorno, COUNT(*) as Numero_Lezioni 
                FROM PROGRAMMA 
                GROUP BY Giorno;
            """
            giorni_result = execute_query(st.session_state["connection"], query_giorni)
            df_giorni = pd.DataFrame(giorni_result)
            
            if df_giorni.empty:
                st.info("Nessuna lezione in programma al momento.")
            else:
                st.bar_chart(df_giorni, x="Giorno", y="Numero_Lezioni")