"""
Hannia Macias Gómez
30 de septiembre de 2026
Simulador bancario con Streamlit

Se utilizó la función filter() para seleccionar los movimientos correspondientes a una 
cuenta bancaria. En Python, filter() devuelve un iterador y no genera inmediatamente una 
nueva lista con todos los resultados. Los elementos son evaluados conforme el iterador 
es consumido. Esto permite aplicar el concepto de evaluación perezosa y evita crear 
estructuras intermedias innecesarias.
"""

import streamlit as st
import json
import random
import hashlib
from pathlib import Path
from datetime import datetime

# CONFIGURACIÓN

st.set_page_config(
    page_title="Hannia Banco",
    page_icon="🏦",
    layout="wide"
)

ARCHIVO_JSON = Path("banco.json")

# ARCHIVO JSON

def guardar_datos(datos):
    """Guarda los datos en el archivo JSON."""

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(
            datos,
            archivo,
            indent=4,
            ensure_ascii=False
        )


def cargar_datos():
    """Carga la información almacenada en banco.json."""

    if not ARCHIVO_JSON.exists():

        datos_iniciales = {
            "cuentas": [],
            "movimientos": []
        }

        guardar_datos(datos_iniciales)

    try:

        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    except (json.JSONDecodeError, FileNotFoundError):

        datos_iniciales = {
            "cuentas": [],
            "movimientos": []
        }

        guardar_datos(datos_iniciales)

        return datos_iniciales

# CONTRASEÑAS

def convertir_password(password):
    """
    Convierte la contraseña en un hash SHA-256.

    La contraseña original no se almacena directamente
    en el archivo JSON.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()

# CUENTAS

def generar_numero_cuenta(datos):
    """Genera un número de cuenta único de 8 dígitos."""

    existentes = {
        cuenta["numero"]
        for cuenta in datos["cuentas"]
    }

    while True:

        numero = str(
            random.randint(10000000, 99999999)
        )

        if numero not in existentes:
            return numero


def buscar_cuenta(datos, numero):
    """Busca una cuenta mediante su número."""

    for cuenta in datos["cuentas"]:

        if cuenta["numero"] == numero:
            return cuenta

    return None


def buscar_por_correo(datos, correo):
    """Busca una cuenta mediante el correo electrónico."""

    for cuenta in datos["cuentas"]:

        if cuenta["correo"].lower() == correo.lower():
            return cuenta

    return None


def crear_cuenta(
    datos,
    nombre,
    apellidos,
    correo,
    password,
    tipo,
    deposito_inicial
):
    """Registra una nueva cuenta bancaria."""

    if buscar_por_correo(datos, correo):
        return False, "Este correo ya está registrado.", None

    numero = generar_numero_cuenta(datos)

    nueva_cuenta = {
        "numero": numero,
        "nombre": nombre,
        "apellidos": apellidos,
        "correo": correo,
        "password": convertir_password(password),
        "tipo": tipo,
        "saldo": round(deposito_inicial, 2),
        "fecha_creacion": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    }

    datos["cuentas"].append(nueva_cuenta)

    if deposito_inicial > 0:

        registrar_movimiento(
            datos,
            numero,
            "Depósito inicial",
            deposito_inicial,
            "Apertura de cuenta"
        )

    guardar_datos(datos)

    return True, "Cuenta creada correctamente.", numero

# INICIO DE SESIÓN

def iniciar_sesion(datos, correo, password):
    """Comprueba las credenciales del usuario."""

    cuenta = buscar_por_correo(
        datos,
        correo
    )

    if cuenta is None:
        return None

    password_hash = convertir_password(password)

    if cuenta["password"] == password_hash:
        return cuenta

    return None

# MOVIMIENTOS

def registrar_movimiento(
    datos,
    numero,
    tipo,
    monto,
    descripcion
):
    """Registra una operación bancaria."""

    movimiento = {
        "cuenta": numero,
        "tipo": tipo,
        "monto": round(monto, 2),
        "descripcion": descripcion,
        "fecha": datetime.now().strftime(
            "%d/%m/%Y %H:%M:%S"
        )
    }

    datos["movimientos"].append(movimiento)

# OPERACIONES

def depositar(datos, numero, monto):

    cuenta = buscar_cuenta(datos, numero)

    if monto <= 0:
        return False, "El monto debe ser mayor que cero."

    cuenta["saldo"] += monto

    registrar_movimiento(
        datos,
        numero,
        "Depósito",
        monto,
        "Depósito realizado"
    )

    guardar_datos(datos)

    return True, "Depósito realizado correctamente."


def retirar(datos, numero, monto):

    cuenta = buscar_cuenta(datos, numero)

    if monto <= 0:
        return False, "El monto debe ser mayor que cero."

    if monto > cuenta["saldo"]:
        return False, "Saldo insuficiente."

    cuenta["saldo"] -= monto

    registrar_movimiento(
        datos,
        numero,
        "Retiro",
        monto,
        "Retiro realizado"
    )

    guardar_datos(datos)

    return True, "Retiro realizado correctamente."


def transferir(datos, origen, destino, monto):

    cuenta_origen = buscar_cuenta(datos, origen)
    cuenta_destino = buscar_cuenta(datos, destino)

    if cuenta_destino is None:
        return False, "La cuenta de destino no existe."

    if origen == destino:
        return False, "No puedes transferirte a ti mismo."

    if monto <= 0:
        return False, "El monto debe ser mayor que cero."

    if monto > cuenta_origen["saldo"]:
        return False, "Saldo insuficiente."

    cuenta_origen["saldo"] -= monto
    cuenta_destino["saldo"] += monto

    registrar_movimiento(
        datos,
        origen,
        "Transferencia enviada",
        monto,
        f"Transferencia hacia {destino}"
    )

    registrar_movimiento(
        datos,
        destino,
        "Transferencia recibida",
        monto,
        f"Transferencia recibida de {origen}"
    )

    guardar_datos(datos)

    return True, "Transferencia realizada correctamente."

# EVALUACIÓN PEREZOSA

def obtener_movimientos_cuenta(datos, numero):
    """
    filter() devuelve un iterador.

    Los elementos se procesan conforme son solicitados,
    por lo que se utiliza evaluación perezosa.
    """

    return filter(
        lambda movimiento:
            movimiento["cuenta"] == numero,
        datos["movimientos"]
    )

# ESTADO DE SESIÓN

if "usuario" not in st.session_state:
    st.session_state.usuario = None

datos = cargar_datos()

# ENCABEZADO

st.title("🏦 Hannia Banco")
st.caption("Tu banco digital")
st.divider()

# USUARIO SIN SESIÓN

if st.session_state.usuario is None:

    st.sidebar.title("🏦 Hannia Bank")

    opcion = st.sidebar.radio(
        "Selecciona una opción:",
        [
            "Inicio",
            "Iniciar sesión",
            "Crear cuenta"
        ]
    )

    # INICIO

    if opcion == "Inicio":

        st.header("Bienvenido a Hannia Banco 👋")

        st.write(
            """
            Administra tu cuenta desde nuestra plataforma
            bancaria.
            """
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "🔐",
            "Acceso seguro"
        )

        col2.metric(
            "💳",
            "Cuenta digital"
        )

        col3.metric(
            "⚡",
            "Operaciones rápidas"
        )

        st.info(
            "Si ya tienes una cuenta, selecciona "
            "'Iniciar sesión'."
        )

        st.success(
            "Si eres nuevo, selecciona 'Crear cuenta'."
        )
        
    # CREAR CUENTA

    elif opcion == "Crear cuenta":

        st.header("👤 Crear cuenta")

        st.write(
            "Completa tus datos para registrarte."
        )

        with st.form("registro"):

            col1, col2 = st.columns(2)

            with col1:

                nombre = st.text_input(
                    "Nombre"
                )

            with col2:

                apellidos = st.text_input(
                    "Apellidos"
                )

            correo = st.text_input(
                "Correo electrónico"
            )

            col3, col4 = st.columns(2)

            with col3:

                password = st.text_input(
                    "Contraseña",
                    type="password"
                )

            with col4:

                confirmar = st.text_input(
                    "Confirmar contraseña",
                    type="password"
                )

            tipo = st.selectbox(
                "Tipo de cuenta",
                [
                    "Cuenta de débito",
                    "Cuenta de ahorro"
                ]
            )

            deposito = st.number_input(
                "Depósito inicial",
                min_value=0.0,
                step=100.0,
                format="%.2f"
            )

            aceptar = st.checkbox(
                "Confirmo que los datos son correctos."
            )

            boton = st.form_submit_button(
                "Crear mi cuenta",
                type="primary",
                use_container_width=True
            )

        if boton:

            if not nombre.strip():

                st.error(
                    "Ingresa tu nombre."
                )

            elif not apellidos.strip():

                st.error(
                    "Ingresa tus apellidos."
                )

            elif not correo.strip() or "@" not in correo:

                st.error(
                    "Ingresa un correo válido."
                )

            elif len(password) < 6:

                st.error(
                    "La contraseña debe contener "
                    "al menos 6 caracteres."
                )

            elif password != confirmar:

                st.error(
                    "Las contraseñas no coinciden."
                )

            elif not aceptar:

                st.warning(
                    "Debes confirmar tus datos."
                )

            else:

                correcto, mensaje, numero = crear_cuenta(
                    datos,
                    nombre.strip(),
                    apellidos.strip(),
                    correo.strip(),
                    password,
                    tipo,
                    deposito
                )

                if correcto:

                    st.success(
                        "🎉 ¡Cuenta creada correctamente!"
                    )

                    st.balloons()

                    st.subheader(
                        "Tu número de cuenta"
                    )

                    st.code(numero)

                    st.info(
                        "Guarda este número. Lo necesitarás "
                        "para recibir transferencias."
                    )

                else:

                    st.error(mensaje)

    # INICIAR SESIÓN

    elif opcion == "Iniciar sesión":

        st.header("🔐 Iniciar sesión")

        with st.form("login"):

            correo = st.text_input(
                "Correo electrónico"
            )

            password = st.text_input(
                "Contraseña",
                type="password"
            )

            boton_login = st.form_submit_button(
                "Iniciar sesión",
                type="primary",
                use_container_width=True
            )

        if boton_login:

            cuenta = iniciar_sesion(
                datos,
                correo,
                password
            )

            if cuenta:

                st.session_state.usuario = cuenta["numero"]

                st.success(
                    "Inicio de sesión correcto."
                )

                st.rerun()

            else:

                st.error(
                    "Correo o contraseña incorrectos."
                )

# USUARIO CON SESIÓN INICIADA

else:

    numero_usuario = st.session_state.usuario

    cuenta = buscar_cuenta(
        datos,
        numero_usuario
    )

    # Si la cuenta deja de existir
    if cuenta is None:

        st.session_state.usuario = None
        st.rerun()

    st.sidebar.write(
        f"👤 **{cuenta['nombre']} {cuenta['apellidos']}**"
    )

    st.sidebar.caption(
        f"Cuenta: {cuenta['numero']}"
    )

    st.sidebar.divider()

    opcion = st.sidebar.radio(
        "Menú",
        [
            "Mi cuenta",
            "Depositar",
            "Retirar",
            "Transferir",
            "Movimientos"
        ]
    )

    st.sidebar.divider()

    if st.sidebar.button(
        "🚪 Cerrar sesión",
        use_container_width=True
    ):

        st.session_state.usuario = None
        st.rerun()

    # MI CUENTA

    if opcion == "Mi cuenta":

        st.header(
            f"Hola, {cuenta['nombre']} 👋"
        )

        st.write(
            "Aquí puedes consultar la información "
            "de tu cuenta."
        )

        st.divider()

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Saldo disponible",
            f"${cuenta['saldo']:,.2f}"
        )

        col2.metric(
            "💳 Número de cuenta",
            cuenta["numero"]
        )

        col3.metric(
            "🏦 Tipo",
            cuenta["tipo"]
        )

        st.divider()

        st.subheader(
            "Información del titular"
        )

        col4, col5 = st.columns(2)

        with col4:

            st.write(
                f"**Nombre:** "
                f"{cuenta['nombre']} {cuenta['apellidos']}"
            )

            st.write(
                f"**Correo:** {cuenta['correo']}"
            )

        with col5:

            st.write(
                f"**Fecha de apertura:** "
                f"{cuenta['fecha_creacion']}"
            )

            st.write(
                f"**Número de cuenta:** "
                f"{cuenta['numero']}"
            )

    # DEPOSITAR

    elif opcion == "Depositar":

        st.header("💵 Depositar dinero")

        st.metric(
            "Saldo actual",
            f"${cuenta['saldo']:,.2f}"
        )

        monto = st.number_input(
            "Cantidad a depositar:",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button(
            "Depositar",
            type="primary",
            use_container_width=True
        ):

            correcto, mensaje = depositar(
                datos,
                numero_usuario,
                monto
            )

            if correcto:

                st.success(mensaje)
                st.balloons()
                st.rerun()

            else:

                st.error(mensaje)

    # RETIRAR

    elif opcion == "Retirar":

        st.header("💸 Retirar dinero")

        st.metric(
            "Saldo disponible",
            f"${cuenta['saldo']:,.2f}"
        )

        monto = st.number_input(
            "Cantidad a retirar:",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button(
            "Retirar",
            type="primary",
            use_container_width=True
        ):

            correcto, mensaje = retirar(
                datos,
                numero_usuario,
                monto
            )

            if correcto:

                st.success(mensaje)
                st.rerun()

            else:

                st.error(mensaje)

    # TRANSFERIR

    elif opcion == "Transferir":

        st.header("🔄 Transferir dinero")

        st.metric(
            "Saldo disponible",
            f"${cuenta['saldo']:,.2f}"
        )

        st.write(
            "Ingresa el número de cuenta de la "
            "persona a la que deseas transferir."
        )

        destino = st.text_input(
            "Número de cuenta destino"
        )

        monto = st.number_input(
            "Cantidad a transferir:",
            min_value=0.0,
            step=100.0,
            format="%.2f"
        )

        if st.button(
            "Realizar transferencia",
            type="primary",
            use_container_width=True
        ):

            correcto, mensaje = transferir(
                datos,
                numero_usuario,
                destino.strip(),
                monto
            )

            if correcto:

                st.success(mensaje)
                st.balloons()
                st.rerun()

            else:

                st.error(mensaje)

    # MOVIMIENTOS

    elif opcion == "Movimientos":

        st.header("📊 Mis movimientos")

        # filter() devuelve un iterador.
        movimientos_filtrados = obtener_movimientos_cuenta(
            datos,
            numero_usuario
        )

        # El iterador se consume aquí.
        movimientos = list(
            movimientos_filtrados
        )

        if movimientos:

            st.write(
                f"Tienes **{len(movimientos)} movimientos**."
            )

            for movimiento in reversed(movimientos):

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [2, 2, 1]
                    )

                    with col1:

                        st.write(
                            f"**{movimiento['tipo']}**"
                        )

                        st.caption(
                            movimiento["descripcion"]
                        )

                    with col2:

                        st.write(
                            f"🕒 {movimiento['fecha']}"
                        )

                    with col3:

                        st.write(
                            f"**${movimiento['monto']:,.2f}**"
                        )

        else:

            st.info(
                "Todavía no tienes movimientos."
            )