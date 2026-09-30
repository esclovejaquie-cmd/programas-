"""
Cálculo de días vividos utilizando lambda
Hannia Macias Gómez
30 de septiembre de 2026

La función lambda se utilizó para calcular los días vividos
de cada persona de manera breve, sin necesidad de definir
una función tradicional con def.

Los resultados se almacenan en un fichero JSON y se procesan
como tuplas para trabajar con valores inmutables.

La aplicación está preparada para desplegarse mediante
GitHub y Streamlit Community Cloud.
"""

import streamlit as st
import json
from datetime import date

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Calculadora de días vividos - Lambda",
    page_icon="📅",
    layout="wide"
)

# FUNCIÓN LAMBDA

# Calcula los días transcurridos entre una fecha y el día actual
calcular_dias = lambda fecha: (date.today() - fecha).days

# ARCHIVO JSON

ARCHIVO_JSON = "DiasVividosLambda.json"


def guardar_json(resultados):
    """
    Guarda los resultados en el fichero JSON.
    """

    datos = []

    for fecha, dias in resultados:
        datos.append({
            "fecha_nacimiento": fecha.isoformat(),
            "dias_vividos": dias
        })

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def cargar_json():
    """
    Recupera los datos almacenados en el fichero JSON
    y los convierte en una tupla.
    """

    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Los resultados se convierten en una tupla.
        # Las tuplas son estructuras inmutables en Python.
        resultados = tuple(
            (
                date.fromisoformat(persona["fecha_nacimiento"]),
                persona["dias_vividos"]
            )
            for persona in datos
        )

        return resultados

    except (FileNotFoundError, json.JSONDecodeError):
        return ()

# TÍTULO

st.title("📅 Calculadora de días vividos con Lambda")

st.write(
    "Ingresa una o varias fechas de nacimiento para calcular "
    "cuántos días han transcurrido hasta la fecha actual."
)

st.divider()

# ESTADO DE LA APLICACIÓN

if "cantidad_fechas" not in st.session_state:
    st.session_state.cantidad_fechas = 1

# Recuperar los resultados almacenados en el JSON
if "resultados" not in st.session_state:
    st.session_state.resultados = cargar_json()

# BOTONES PARA AGREGAR O ELIMINAR FECHAS

col1, col2 = st.columns(2)


with col1:

    if st.button(
        "➕ Agregar fecha",
        use_container_width=True
    ):
        st.session_state.cantidad_fechas += 1


with col2:

    if st.button(
        "➖ Eliminar fecha",
        use_container_width=True,
        disabled=st.session_state.cantidad_fechas <= 1
    ):

        # Eliminar el último campo de fecha
        st.session_state.cantidad_fechas -= 1

        # Como los resultados son una tupla, no usamos pop().
        # Creamos una nueva tupla sin el último elemento.
        if st.session_state.resultados:

            st.session_state.resultados = (
                st.session_state.resultados[:-1]
            )

            # Actualizar también el fichero JSON
            guardar_json(st.session_state.resultados)

# CAPTURA DE FECHAS

st.subheader("Fechas de nacimiento")

fechas = []

for i in range(st.session_state.cantidad_fechas):

    fecha = st.date_input(
        f"Persona {i + 1}",

        # Fecha que aparece inicialmente
        value=date(2000, 1, 1),

        # Permite seleccionar fechas antiguas
        min_value=date(1900, 1, 1),

        # No permite fechas futuras
        max_value=date.today(),

        # Formato día/mes/año
        format="DD/MM/YYYY",

        key=f"fecha_{i}"
    )

    fechas.append(fecha)

# CÁLCULO

if st.button(
    "🧮 Calcular días vividos",
    type="primary",
    use_container_width=True
):

    # MAP aplica la función lambda a cada fecha.
    # map() genera los resultados de forma perezosa.
    dias_vividos = map(calcular_dias, fechas)

    # Convertimos los resultados en una tupla inmutable.
    # En este momento se consumen los valores de map().
    resultados = tuple(
        zip(fechas, dias_vividos)
    )

    # Guardar resultados en el fichero JSON
    guardar_json(resultados)

    # Guardar resultados durante la sesión de Streamlit
    st.session_state.resultados = resultados

# MOSTRAR RESULTADOS

if st.session_state.resultados:

    st.divider()

    st.subheader("📋 Lista de personas")

    for numero, (fecha, dias) in enumerate(
        st.session_state.resultados,
        start=1
    ):

        with st.container(border=True):

            st.markdown(
                f"### 👤 Persona {numero}"
            )

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Fecha de nacimiento",
                    fecha.strftime("%d/%m/%Y")
                )

            with col2:

                st.metric(
                    "Días vividos",
                    f"{dias:,}"
                )

    st.success(
        "✅ Cálculo realizado correctamente."
    )