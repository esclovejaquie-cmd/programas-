"""
Cálculo de días vividos
Hannia Macias Gómez
30 de septiembre de 2026

La función map() se utilizó para aplicar automáticamente
la función calcular_dias() a todas las fechas de nacimiento
ingresadas por el usuario.
"""

import streamlit as st
import json
from datetime import date

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Calculadora de días vividos - Hannia",
    page_icon="📅",
    layout="wide"
)

# FUNCIONES

def calcular_dias(fecha_nacimiento):
    """
    Calcula los días transcurridos desde la fecha de nacimiento
    hasta la fecha actual.
    """
    hoy = date.today()
    return (hoy - fecha_nacimiento).days


def calcular_edad_aproximada(dias):
    """Convierte los días vividos a años aproximados."""
    return dias / 365.2425

# ARCHIVO JSON

ARCHIVO_JSON = "DiasVividos.json"

def guardar_json(resultados):
    datos = []

    for fecha, dias in resultados:
        datos.append({
            "fecha_nacimiento": fecha.isoformat(),
            "dias_vividos": dias
        })

    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4)


def cargar_json():
    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)

        # Convertir los datos del JSON en una tupla
        resultados = tuple(
            (
                date.fromisoformat(persona["fecha_nacimiento"]),
                persona["dias_vividos"]
            )
            for persona in datos
        )

        return resultados

    except FileNotFoundError:
        return ()

# TÍTULO

st.title("📅 Calculadora de días vividos")

st.write(
    "Ingresa una o varias fechas de nacimiento para calcular "
    "cuántos días han transcurrido hasta la fecha actual."
)

st.divider()

# ESTADO DE LA APLICACIÓN

if "cantidad_fechas" not in st.session_state:
    st.session_state.cantidad_fechas = 1

# Al iniciar, cargar los datos almacenados en el JSON
if "resultados" not in st.session_state:
    st.session_state.resultados = cargar_json()

# BOTONES PARA AGREGAR O ELIMINAR FECHAS

col1, col2 = st.columns(2)

with col1:
    if st.button("➕ Agregar fecha", use_container_width=True):
        st.session_state.cantidad_fechas += 1


with col2:
    if st.button(
        "➖ Eliminar fecha",
        use_container_width=True,
        disabled=st.session_state.cantidad_fechas <= 1
    ):
        # Reducir la cantidad de campos
        st.session_state.cantidad_fechas -= 1

        # Como resultados es una TUPLA, eliminamos el último
        # elemento creando una nueva tupla
        if st.session_state.resultados:
            st.session_state.resultados = (
                st.session_state.resultados[:-1]
            )

            # Actualizar también el JSON
            guardar_json(st.session_state.resultados)

# CAPTURA DE FECHAS
st.subheader("Fechas de nacimiento")

fechas = []

for i in range(st.session_state.cantidad_fechas):

    fecha = st.date_input(
    f"Persona {i + 1}",
    value=date(2000, 1, 1),
    min_value=date(1900, 1, 1),
    max_value=date.today(),
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

    # MAP utiliza evaluación perezosa
    dias_vividos = map(calcular_dias, fechas)

    # MAP se consume al crear la tupla
    resultados = tuple(
        zip(fechas, dias_vividos)
    )

    # Guardar los resultados en el JSON
    guardar_json(resultados)

    # Guardar también en session_state
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

            st.markdown(f"### 👤 Persona {numero}")

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

    st.success("✅ Cálculo realizado correctamente.")