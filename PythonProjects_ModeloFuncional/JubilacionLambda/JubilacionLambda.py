"""
Calculadora de dinero para jubilación utilizando lambda
Hannia Macias Gómez
30 de septiembre de 2026

La función lambda se utiliza para calcular el dinero estimado
que una persona tendrá al momento de jubilarse considerando
su ahorro inicial, aportaciones mensuales y rendimiento anual.

En este programa se utilizó una función lambda
para calcular el dinero estimado que tendrá una
persona al momento de jubilarse.

La función recibe cuatro datos:

- ahorro inicial
- aportación mensual
- tasa de rendimiento
- cantidad de meses

Con estos valores calcula el crecimiento del ahorro
mediante interés compuesto y las aportaciones
realizadas durante el periodo.

Se utilizó lambda porque permite realizar este
cálculo mediante una función anónima y compacta,
sin necesidad de definir una función tradicional
con def.
"""

import streamlit as st
import json
import os

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Calculadora de Jubilación con Lambda",
    page_icon="💰",
    layout="wide"
)

# ARCHIVO JSON

ARCHIVO_CONFIG = "config_lambda.json"

# Valores inmutables de configuración
CONFIG_DEFAULT = {
    "nombre_aplicacion": "Calculadora de Jubilación con Lambda",
    "moneda": "MXN",
    "rendimiento_predeterminado": 6.0,
    "edad_minima": 18,
    "edad_maxima": 100
}


# Crear automáticamente el JSON si no existe
def crear_json():
    if not os.path.exists(ARCHIVO_CONFIG):
        with open(ARCHIVO_CONFIG, "w", encoding="utf-8") as archivo:
            json.dump(
                CONFIG_DEFAULT,
                archivo,
                indent=4,
                ensure_ascii=False
            )


# Cargar configuración
def cargar_configuracion():
    crear_json()

    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


config = cargar_configuracion()

# FUNCIÓN LAMBDA

# Calcula el monto futuro considerando:
# ahorro inicial + aportaciones mensuales + rendimiento
calcular_jubilacion = lambda ahorro, aportacion, tasa, meses: (
    ahorro * (1 + tasa / 12) ** meses
    +
    (
        aportacion * (
            ((1 + tasa / 12) ** meses - 1)
            / (tasa / 12)
        )
        if tasa > 0
        else aportacion * meses
    )
)

# TÍTULO

st.title("💰 Calculadora de Jubilación con Lambda")

st.write(
    "Calcula cuánto dinero podrías acumular para tu jubilación "
    "considerando tu ahorro actual, aportaciones mensuales "
    "y un rendimiento anual estimado."
)

st.divider()

# DATOS DEL USUARIO

st.header("👤 Datos personales y financieros")

col1, col2 = st.columns(2)


with col1:

    nombre = st.text_input(
        "Nombre",
        placeholder="Ingresa tu nombre"
    )

    edad_actual = st.number_input(
        "Edad actual",
        min_value=config["edad_minima"],
        max_value=config["edad_maxima"],
        value=25,
        step=1
    )

    edad_jubilacion = st.number_input(
        "Edad deseada para jubilarte",
        min_value=config["edad_minima"],
        max_value=config["edad_maxima"],
        value=65,
        step=1
    )


with col2:

    ahorro_inicial = st.number_input(
        "Ahorro actual ($)",
        min_value=0.0,
        value=50000.0,
        step=1000.0
    )

    aportacion_mensual = st.number_input(
        "Aportación mensual ($)",
        min_value=0.0,
        value=3000.0,
        step=500.0
    )

    rendimiento = st.slider(
        "Rendimiento anual estimado (%)",
        min_value=0.0,
        max_value=15.0,
        value=float(config["rendimiento_predeterminado"]),
        step=0.5
    )

# CÁLCULO

st.divider()

if st.button(
    "💰 Calcular jubilación",
    type="primary",
    use_container_width=True
):

    if edad_jubilacion <= edad_actual:

        st.error(
            "La edad de jubilación debe ser mayor "
            "que la edad actual."
        )

    else:

        # Años restantes
        anios = edad_jubilacion - edad_actual

        # Meses restantes
        meses = anios * 12

        # Convertir porcentaje anual a decimal
        tasa_anual = rendimiento / 100

        # USO DE LA FUNCIÓN LAMBDA

        dinero_final = calcular_jubilacion(
            ahorro_inicial,
            aportacion_mensual,
            tasa_anual,
            meses
        )
        
        # OTROS CÁLCULOS

        total_aportado = (
            ahorro_inicial +
            aportacion_mensual * meses
        )

        ganancias = dinero_final - total_aportado

        # RESULTADOS

        st.success(
            f"Proyección calculada para "
            f"{nombre if nombre else 'el usuario'}."
        )

        st.header("📊 Resultado de la jubilación")

        col_resultado1, col_resultado2, col_resultado3 = st.columns(3)


        with col_resultado1:

            st.metric(
                "💰 Dinero estimado al jubilarte",
                f"${dinero_final:,.2f} {config['moneda']}"
            )


        with col_resultado2:

            st.metric(
                "🏦 Dinero aportado",
                f"${total_aportado:,.2f} {config['moneda']}"
            )


        with col_resultado3:

            st.metric(
                "📈 Rendimiento estimado",
                f"${ganancias:,.2f} {config['moneda']}"
            )

        # INFORMACIÓN DEL TIEMPO

        st.subheader("⏳ Tiempo para tu jubilación")

        st.write(
            f"Actualmente tienes **{edad_actual} años** "
            f"y deseas jubilarte a los "
            f"**{edad_jubilacion} años**."
        )

        st.write(
            f"Te quedan **{anios} años**, equivalentes "
            f"a **{meses:,} meses**, para ahorrar."
        )

        # PROYECCIÓN PARA LA GRÁFICA

        st.subheader("📈 Crecimiento estimado de tus ahorros")

        datos_grafica = {}

        for anio in range(0, anios + 1):

            meses_transcurridos = anio * 12

            saldo_anual = calcular_jubilacion(
                ahorro_inicial,
                aportacion_mensual,
                tasa_anual,
                meses_transcurridos
            )

            edad = edad_actual + anio

            datos_grafica[edad] = saldo_anual


        st.line_chart(datos_grafica)

        # TABLA DE PROYECCIÓN

        with st.expander("📋 Ver proyección año por año"):

            for edad, saldo in datos_grafica.items():

                st.write(
                    f"**Edad {edad}:** "
                    f"${saldo:,.2f} {config['moneda']}"
                )

st.divider()