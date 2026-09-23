import streamlit as st
from utils.utils import *

def check_info_corso(corso_dict):
    for key, value in corso_dict.items():
        if value == '':
            return False, "Tutti i campi testuali devono essere riempiti."
    if not str(corso_dict['CodC']).startswith("CT"):
        return False, "Il Codice Corso deve iniziare con la sigla 'CT'."
    return True, ""

def insert_corso(corso_dict):
    valid, msg = check_info_corso(corso_dict)
    if valid:
        attributi = ", ".join(corso_dict.keys())
        # Formattazione valori stringa per SQL
        valori = f"('{corso_dict['CodC']}', '{corso_dict['Nome']}', '{corso_dict['Tipo']}', {corso_dict['Livello']})"
        query = f"INSERT INTO CORSO ({attributi}) VALUES {valori};"
        
        try:
            execute_query(st.session_state["connection"], query)
            st.session_state["connection"].commit()
            return True, ""
        except Exception as e:
            if "Duplicate entry" in str(e):
                return False, "Codice Corso già esistente nel database."
            return False, str(e)
    else:
        return False, msg

if __name__ == "__main__":
    st.title("➕ Inserisci Nuovo Corso")
    
    if check_connection():
        with st.form("form_corso"):
            st.header(":blue[Dettagli Corso]")
            
            code = st.text_input("Codice Corso (es. CT004)")
            nome = st.text_input("Nome")
            tipo = st.text_input("Tipo")
            livello = st.number_input("Livello", min_value=1, max_value=4, value=1)

            insert_dict = {"CodC": code, "Nome": nome, "Tipo": tipo, "Livello": livello}
            submitted = st.form_submit_button("Inserisci Corso", type='primary')
        
        if submitted:
            success, error_msg = insert_corso(insert_dict)
            if success:
                st.success("Inserimento completato con successo!", icon='✅')
                st.write(insert_dict)
            else:
                st.error(f"Errore: {error_msg}", icon='⚠️')