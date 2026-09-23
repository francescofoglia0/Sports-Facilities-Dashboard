import streamlit as st
from utils.utils import *
import pandas as pd

if __name__ == "__main__":
    st.title("📚 Catalogo Corsi")

    if check_connection():
        query_tipi = "SELECT DISTINCT Tipo FROM CORSO"
        tipi_res = execute_query(st.session_state["connection"], query_tipi)
        lista_tipi = [row['Tipo'] for row in tipi_res.mappings()]

        col1, col2 = st.columns(2)
        tipi_sel = col1.multiselect("Filtra per Tipo:", options=lista_tipi)
        livello_range = col2.slider("Filtra per Livello:", 1, 4, (1, 4))

        query = f"SELECT * FROM CORSO WHERE Livello >= {livello_range[0]} AND Livello <= {livello_range[1]}"
        if tipi_sel:
            if len(tipi_sel) == 1:
                query += f" AND Tipo = '{tipi_sel[0]}'"
            else:
                query += f" AND Tipo IN {tuple(tipi_sel)}"
        
        corsi_res = execute_query(st.session_state["connection"], query)
        df_corsi = pd.DataFrame(corsi_res)

        if df_corsi.empty:
            st.warning("Nessun corso corrispondente.", icon='⚠️')
        else:
            met1, met2 = st.columns(2)
            met1.metric(label="Corsi Totali", value=len(df_corsi))
            met2.metric(label="Tipi Distinti", value=df_corsi['Tipo'].nunique())
            
            st.dataframe(df_corsi, use_container_width=True, hide_index=True)

            with st.expander("Programmi dettagliati", expanded=False):
                codici = tuple(df_corsi['CodC'].tolist())
                if codici:
                    # gestisco stringa per la tupla SQL
                    if len(codici) == 1:
                        query_det = f"SELECT P.Giorno, P.OrarioInizio, P.Durata, P.Sala, C.Nome as NomeCorso, CONCAT(I.Nome, ' ', I.Cognome) as Istruttore, I.Email FROM PROGRAMMA P JOIN CORSO C ON P.CodC = C.CodC JOIN ISTRUTTORE I ON P.CodFisc = I.CodFisc WHERE P.CodC = '{codici[0]}'"
                    else:
                        query_det = f"SELECT P.Giorno, P.OrarioInizio, P.Durata, P.Sala, C.Nome as NomeCorso, CONCAT(I.Nome, ' ', I.Cognome) as Istruttore, I.Email FROM PROGRAMMA P JOIN CORSO C ON P.CodC = C.CodC JOIN ISTRUTTORE I ON P.CodFisc = I.CodFisc WHERE P.CodC IN {codici}"
                    
                    det_res = execute_query(st.session_state["connection"], query_det)
                    df_det = pd.DataFrame(det_res)
                    
                    if df_det.empty:
                        st.info("Programmazione non ancora disponibile per i corsi selezionati.")
                    else:
                        st.dataframe(df_det, use_container_width=True, hide_index=True)