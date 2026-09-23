import streamlit as st
from utils.utils import *
import pandas as pd

def check_conflitti_e_vincoli(lez_dict):
    if lez_dict['Durata'] > 60:
        return False, "La durata non può superare i 60 minuti."
    if lez_dict['Giorno'] in ["Sabato", "Domenica"]:
        return False, "Le lezioni si tengono solo dal Lunedì al Venerdì."
    if lez_dict['Sala'] == '':
        return False, "Il campo Sala è obbligatorio."
    
    # faccio check su database per eventuali conflitti
    q_check = f"SELECT * FROM PROGRAMMA WHERE CodC = '{lez_dict['CodC']}' AND Giorno = '{lez_dict['Giorno']}';"
    res_check = execute_query(st.session_state["connection"], q_check)
    if not pd.DataFrame(res_check).empty:
        return False, "Conflitto: Esiste già una lezione per questo corso in questo giorno."
        
    return True, ""

def insert_lezione(lez_dict):
    valid, msg = check_conflitti_e_vincoli(lez_dict)
    if valid:
        attributi = ", ".join(lez_dict.keys())
        valori = f"('{lez_dict['CodFisc']}', '{lez_dict['Giorno']}', '{lez_dict['OrarioInizio']}', {lez_dict['Durata']}, '{lez_dict['CodC']}', '{lez_dict['Sala']}')"
        query = f"INSERT INTO PROGRAMMA ({attributi}) VALUES {valori};"
        
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
            return True, ""
        except Exception as e:
            return False, str(e)
    else:
        return False, msg

if __name__ == "__main__":
    st.title("📅 Programmazione Lezioni")
    
    if check_connection():
        istr_res = execute_query(st.session_state["connection"], "SELECT CodFisc FROM ISTRUTTORE")
        lista_istr = [row['CodFisc'] for row in istr_res.mappings()]
        
        corsi_res = execute_query(st.session_state["connection"], "SELECT CodC FROM CORSO")
        lista_corsi = [row['CodC'] for row in corsi_res.mappings()]
        
        if not lista_istr or not lista_corsi:
            st.error("Errore: Assicurati di aver inserito almeno un corso e un istruttore prima di programmare una lezione.")
        else:
            with st.form("form_lezione"):
                st.header(":blue[Dettagli Lezione]")
                col1, col2 = st.columns(2)
                
                fisc = col1.selectbox("Codice Fiscale Istruttore", lista_istr)
                corso = col1.selectbox("Codice Corso", lista_corsi)
                sala = col1.text_input("Sala")
                
                giorno = col2.selectbox("Giorno", ["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì"])
                orario = col2.time_input("Orario Inizio")
                durata = col2.slider("Durata (minuti)", 5, 60, 30, 1)
                
                orario_str = orario.strftime("%H:%M:%S")
                insert_dict = {"CodFisc": fisc, "Giorno": giorno, "OrarioInizio": orario_str, "Durata": durata, "CodC": corso, "Sala": sala}
                
                submitted = st.form_submit_button("Inserisci in Programma", type='primary')
                
            if submitted:
                success, error_msg = insert_lezione(insert_dict)
                if success:
                    st.success("Lezione inserita correttamente nel palinsesto!", icon='✅')
                    st.write(insert_dict)
                else:
                    st.error(f"Operazione fallita. {error_msg}", icon='⚠️')