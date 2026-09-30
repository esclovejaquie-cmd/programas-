"""
Calculadora de consumo de gasolina utilizando lambda
Hannia Macias Gómez
30 de septiembre de 2026

La función lambda se utiliza para calcular el rendimiento
del vehículo en km/L y el consumo en L/100 km de forma
breve, sin necesidad de definir una función tradicional
con def.
"""

import streamlit as st
import json
import os

# ARCHIVO JSON

ARCHIVO_JSON = "configuracion.json"

# Valores predeterminados de configuración
CONFIGURACION_PREDETERMINADA = {
    "unidad_distancia": "km",
    "unidad_combustible": "litros",
    "moneda": "MXN",
    "titulo": "Calculadora de consumo de gasolina con Lambda",
    "version": "2.0"
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

# Leer configuración del JSON
with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
    configuracion = json.load(archivo)

# VALORES INMUTABLES

# Tupla: estructura inmutable
UNIDADES = (
    configuracion["unidad_distancia"],
    configuracion["unidad_combustible"],
    configuracion["moneda"]
)

# FUNCIONES LAMBDA

# Calcula kilómetros recorridos por cada litro de gasolina
calcular_rendimiento = lambda distancia, litros: distancia / litros

# Calcula litros consumidos por cada 100 kilómetros
calcular_consumo = lambda distancia, litros: (litros / distancia) * 100

# Calcula el costo total de la gasolina utilizada
calcular_costo = lambda litros, precio: litros * precio

# Calcula el costo por kilómetro
calcular_costo_km = lambda costo, distancia: costo / distancia

# CONFIGURACIÓN DE STREAMLIT

st.set_page_config(
    page_title=configuracion["titulo"],
    page_icon="⛽",
    layout="wide"
)

# ENCABEZADO

st.title("⛽ Calculadora de consumo de gasolina con Lambda")

st.write(
    "Ingresa los datos de tu recorrido para calcular el "
    "rendimiento del vehículo, consumo de gasolina y costo "
    "del viaje."
)

st.divider()

# PESTAÑAS

tab1, tab2 = st.tabs([
    "🚗 Calcular consumo",
    "📊 Comparar recorridos"
])

# TAB 1 - CALCULAR UN RECORRIDO

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

        # Se utilizan las funciones lambda
        rendimiento = calcular_rendimiento(
            distancia,
            litros
        )

        consumo_100km = calcular_consumo(
            distancia,
            litros
        )

        costo_total = calcular_costo(
            litros,
            precio_litro
        )

        costo_por_km = calcular_costo_km(
            costo_total,
            distancia
        )

        st.success("Cálculo realizado correctamente.")

        st.subheader("Resultados")

        r1, r2, r3, r4 = st.columns(4)

        with r1:
            st.metric(
                "Rendimiento",
                f"{rendimiento:.2f} km/L"
            )

        with r2:
            st.metric(
                "Consumo",
                f"{consumo_100km:.2f} L/100 km"
            )

        with r3:
            st.metric(
                "Costo del recorrido",
                f"${costo_total:.2f} MXN"
            )

        with r4:
            st.metric(
                "Costo por km",
                f"${costo_por_km:.2f} MXN"
            )

        st.divider()

        st.subheader("Interpretación")

        st.write(
            f"🚗 El vehículo recorrió aproximadamente "
            f"**{rendimiento:.2f} km por cada litro de gasolina**."
        )

        st.write(
            f"⛽ Para recorrer 100 km consumiría aproximadamente "
            f"**{consumo_100km:.2f} litros**."
        )

        st.write(
            f"💰 El costo del recorrido fue de aproximadamente "
            f"**${costo_total:.2f} MXN**."
        )

# TAB 2 - COMPARAR RECORRIDOS

with tab2:

    st.subheader("Comparar varios recorridos")

    st.write(
        "Ingresa los datos de varios recorridos para comparar "
        "el rendimiento de gasolina."
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
                f"Gasolina consumida en recorrido {i + 1} (L)",
                min_value=0.1,
                value=10.0,
                key=f"litros_{i}"
            )

        # Cada recorrido se guarda como una tupla
        recorridos.append(
            (distancia_recorrido, litros_recorrido)
        )

    if st.button(
        "📊 Comparar recorridos",
        use_container_width=True
    ):

        resultados = []

        for numero, recorrido in enumerate(
            recorridos,
            start=1
        ):

            distancia_r = recorrido[0]
            litros_r = recorrido[1]

            # Uso de funciones lambda
            rendimiento_r = calcular_rendimiento(
                distancia_r,
                litros_r
            )

            consumo_r = calcular_consumo(
                distancia_r,
                litros_r
            )

            resultados.append({
                "Recorrido": numero,
                "Distancia (km)": distancia_r,
                "Gasolina (L)": litros_r,
                "Rendimiento (km/L)": round(rendimiento_r, 2),
                "Consumo (L/100 km)": round(consumo_r, 2)
            })

        st.subheader("Resultados")

        st.dataframe(
            resultados,
            use_container_width=True,
            hide_index=True
        )