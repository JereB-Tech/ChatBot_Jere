# python -m streamlit run chatbot.py
import streamlit as st
import groq


# st.title("BIENVENIDOS A TALENTO TECH TEENS, COPADOS")
#Tener modelos de IA
Modelos = ["llama3-8b-8192", "llama3-70b-8192"]

#Configurar la página
def configurar_pagina():
    st.set_page_config(page_title="ChatBotDeJere", page_icon="👑") #Cambia el nombre de la ventana del navegador.
    st.title("Pregunta lo que necesites, estoy acá para ayudarte.")

#Mostrar el sidebar con los modelos
def mostrar_sidebar():
    st.sidebar.title("Eleji tu modelo de IA favorito")
    modelo = st.sidebar.selectbox("¿Cuál elegís?", Modelos, index=2) #Con el "index" elegimos lo que queremos mostrar primero.
    st.write(f"**Elegiste el modelo:**  {modelo}")
    return modelo

#Crear un cliente Groq, que me permita usar su API
def crear_cliente_Groq():
    Groq_API_Key = st.secrets["GROQ_API_KEY"] #Almacena la API Key de Groq.
    return groq.Groq(api_key = Groq_API_Key)

#Inicializar el estado de los mensajes.
def inicialización_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

#Historial del chat
def mostrar_historial_chat(): #Recorre los mensajes
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje ["role"]): #generar un contexto temporal "context manager". Guarda quien lo envía.
            st.markdown(mensaje["content"]) #MarkDown simula visualmente una "cajita" para que salga el contenido. Guarda qué envía.

#Obtener mensaje de usuario
def obtener_mensaje_usuario():
    return st.chat_input("Envía un mensaje.")

#Agregar mensajes al estado
def agregar_mensaje_al_historial(role, content): #Recibe quien lo envia y que envia.
    st.session_state.mensajes.append({"role":role, "content":content}) #lo incrusto en la lista de inicialización.

#Mostrar mensajes en pantalla
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

#Llamar al modelo de Groq
def obtener_respuesta_modelo(cliente, modelo, mensajes):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensajes,
        stream = False
    )
    return respuesta.choices[0].message.content





#Flujo de la aplicación
def ejecutar_app():
    configurar_pagina()
    modelo = mostrar_sidebar()
    cliente = crear_cliente_Groq()
    inicialización_estado_chat()
    mostrar_historial_chat()
    mensaje_usuario = obtener_mensaje_usuario()

    if mensaje_usuario:
        agregar_mensaje_al_historial("user", mensaje_usuario)
        mostrar_mensaje("user", mensaje_usuario)

        mensaje_modelo = obtener_respuesta_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensaje_al_historial("assisant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)


#El condicional que la define como app, tiene que estar SI O SI al final.
if __name__ == "__main__": #solo se puede ejecutar el codigo en ESTE archivo y no se puede importar ninguna funcion en otro archivo
    ejecutar_app() #toma como referencia el archivo en el que estoy, sin importar el nombre, aun que SI O SI debe tener el __ antes y despues.

