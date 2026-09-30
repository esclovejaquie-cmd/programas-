"""
Calculadora de consumo de gasolina con Streamlit
Hannia Macias Gómez
30 de septiembre de 2026

La función map() se utiliza para calcular el consumo de gasolina
de varios recorridos. En Python 3, map() devuelve un iterador,
por lo que utiliza evaluación perezosa: los valores se calculan
solamente cuando son solicitados o recorridos.

La función map() aplica calcular_consumo() a cada recorrido. En Python 3, 
map() devuelve un iterador, por lo que utiliza evaluación perezosa: los resultados
no se calculan todos inmediatamente, sino conforme se solicitan al recorrer el iterador.
"""

import streamlit as st
import json
import os

# ARCHIVO JSON

ARCHIVO_JSON = "configuracion.json"

# Valores inmutables predeterminados
CONFIGURACION_PREDETERMINADA = {
    "unidad_distancia": "km",
    "unidad_combustible": "litros",
    "moneda": "MXN",
    "titulo": "Calculadora de consumo de gasolina",
    "version": "1.0"
}

# Crear automáticamente el JSON si no existe
if not os.path.exists(ARCHIVO_JSON):
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(
            CONFIGURACION_PREDETERMINADA,
            archivo,
            indent=4,
            ensure_ascii=False
        )

# Leer los valores inmutables del JSON
with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
    configuracion = json.load(archivo)

# Convertir algunos valores a tupla para trabajar
# con una estructura inmutable
UNIDADES = (
    configuracion["unidad_distancia"],
    configuracion["unidad_combustible"],
    configuracion["moneda"]
)

# CONFIGURACIÓN DE STREAMLIT

st.set_page_config(
    page_title=configuracion["titulo"],
    page_icon="⛽",
    layout="wide"
)

# FUNCIONES

def calcular_consumo(datos):
    """
    Recibe una tupla:
    (distancia, litros)

    Retorna:
    km por litro y litros por cada 100 km.
    """
    distancia, litros = datos

    km_litro = distancia / litros
    litros_100km = (litros / distancia) * 100

    return km_litro, litros_100km

# ENCABEZADO

st.title("⛽ Calculadora de consumo de gasolina")

st.write(
    "Calcula el rendimiento de combustible de tu vehículo "
    "y estima cuánto cuesta realizar un recorrido."
)

st.divider()

# PESTAÑAS

tab1, tab2 = st.tabs([
    "🚗 Calcular recorrido",
    "📊 Varios recorridos"
])

# TAB 1 - UN RECORRIDO

with tab1:

    st.subheader("Datos del recorrido")

    col1, col2, col3 = st.columns(3)

    with col1:
        distancia = st.number_input(
            "Distancia recorrida (km)",
            min_value=0.1,
            value=100.0,
            step=1.0
        )

    with col2:
        litros = st.number_input(
            "Gasolina consumida (L)",
            min_value=0.1,
            value=10.0,
            step=0.5
        )

    with col3:
        precio_litro = st.number_input(
            "Precio por litro ($)",
            min_value=0.0,
            value=24.00,
            step=0.10
        )

    if st.button(
        "⛽ Calcular consumo",
        type="primary",
        use_container_width=True
    ):

        km_litro = distancia / litros
        litros_100km = (litros / distancia) * 100
        costo = litros * precio_litro
        costo_km = costo / distancia

        st.success("Cálculo realizado correctamente.")

        st.subheader("Resultados")

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric(
                "Rendimiento",
                f"{km_litro:.2f} km/L"
            )

        with r2:
            st.metric(
                "Consumo",
                f"{litros_100km:.2f} L/100 km"
            )

        with r3:
            st.metric(
                "Costo del recorrido",
                f"${costo:.2f} MXN"
            )

        with r4:
            st.metric(
                "Costo por km",
                f"${costo_km:.2f}"
            )

        st.divider()

        st.subheader("Interpretación")

        st.write(
            f"Tu vehículo recorrió **{km_litro:.2f} kilómetros "
            f"por cada litro de gasolina**."
        )

        st.write(
            f"Para recorrer 100 km consumiría aproximadamente "
            f"**{litros_100km:.2f} litros**."
        )

        st.write(
            f"El costo total del recorrido fue de aproximadamente "
            f"**${costo:.2f} MXN**."
        )

# TAB 2 - VARIOS RECORRIDOS

with tab2:

    st.subheader("Comparar varios recorridos")

    st.write(
        "Selecciona cuántos recorridos deseas comparar. "
        "Esta sección utiliza `map()` con evaluación perezosa."
    )

    cantidad = st.slider(
        "Número de recorridos",
        min_value=2,
        max_value=5,
        value=3
    )

    recorridos = []

    for i in range(cantidad):

        st.markdown(f"#### Recorrido {i + 1}")

        col1, col2 = st.columns(2)

        with col1:
            distancia_recorrido = st.number_input(
                f"Distancia del recorrido {i + 1} (km)",
                min_value=0.1,
                value=100.0,
                key=f"distancia_{i}"
            )

        with col2:
            litros_recorrido = st.number_input(
                f"Litros consumidos en recorrido {i + 1}",
                min_value=0.1,
                value=10.0,
                key=f"litros_{i}"
            )

        # Se almacena como tupla (estructura inmutable)
        recorridos.append(
            (distancia_recorrido, litros_recorrido)
        )

    if st.button(
        "📊 Comparar recorridos",
        use_container_width=True
    ):

        # MAP() + EVALUACIÓN PEREZOSA
        # map NO calcula inmediatamente todos los valores.
        # Devuelve un iterador que produce cada resultado
        # conforme se va recorriendo.
        resultados_perezosos = map(
            calcular_consumo,
            recorridos
        )

        st.subheader("Resultados")

        tabla_resultados = []

        # Aquí se consumen los valores del iterador map
        for numero, resultado in enumerate(
            resultados_perezosos,
            start=1
        ):
            km_litro, litros_100km = resultado

            tabla_resultados.append({
                "Recorrido": numero,
                "Distancia (km)": recorridos[numero - 1][0],
                "Gasolina (L)": recorridos[numero - 1][1],
                "Rendimiento (km/L)": round(km_litro, 2),
                "Consumo (L/100 km)": round(litros_100km, 2)
            })

        st.dataframe(
            tabla_resultados,
            use_container_width=True,
            hide_index=True
        )

# INFORMACIÓN DEL PROGRAMA

st.divider()