import streamlit as st

# Función para manejar el inicio de sesión utilizando las cuentas predefinidas
def handle_predefined_login(username, password, profile, predefined_users, session_state):
    predefined_user = predefined_users.get(profile, {})
    if username == predefined_user.get("username") and password == predefined_user.get("password"):
        session_state.logged_in = True
        session_state.username = username
        session_state.profile = profile
        st.success("Inicio de sesión exitoso.")
    else:
        st.error("Usuario o contraseña incorrectos.")

# Función para mostrar el formulario de inicio de sesión
def login_form(profile, predefined_users, session_state):
    st.sidebar.header(f"Inicio de Sesión - {profile}")
    predefined_user = predefined_users.get(profile, {})
    user = st.sidebar.text_input("Usuario", value=predefined_user.get("username"), key=f"{profile}_username")
    password = st.sidebar.text_input("Contraseña", type="password", value=predefined_user.get("password"), key=f"{profile}_password")
    if st.sidebar.button("Iniciar Sesión", key=f"{profile}_login"):
        handle_predefined_login(user, password, profile, predefined_users, session_state)

# Función para cerrar sesión
def logout(session_state):
    session_state.logged_in = False
    session_state.username = ""
    session_state.profile = ""
    st.sidebar.success("Sesión cerrada correctamente.")
