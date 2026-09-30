"""
Calculadora de dinero para jubilación con map()
Hannia Macias Gómez
30 de septiembre de 2026

La función map() se utiliza para generar la proyección anual
del ahorro para la jubilación. En Python 3, map() trabaja de
forma perezosa, produciendo los resultados conforme son
solicitados.

La aplicación utiliza un archivo JSON para almacenar valores
inmutables de configuración.

En este programa se utilizó map() para transformar
cada año de la proyección en un registro que contiene
la edad de la persona y el dinero acumulado.

En Python 3, map() devuelve un iterador, por lo que
trabaja mediante evaluación perezosa: los elementos se
generan conforme son solicitados.

Finalmente se utiliza list() para consumir el iterador,
ya que Streamlit necesita los resultados para presentar
la gráfica y la información al usuario.
"""

import streamlit as st
import json
import os

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Calculadora de Jubilación",
    page_icon="💰",
    layout="wide"
)

# ARCHIVO JSON

ARCHIVO_CONFIG = "config.json"

# Valores inmutables predeterminados
CONFIG_DEFAULT = {
    "nombre_aplicacion": "Calculadora de Jubilación",
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


# Leer configuración
def cargar_configuracion():
    crear_json()

    with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


config = cargar_configuracion()

# FUNCIÓN PARA CALCULAR EL AHORRO

def calcular_ahorro_anual(
    saldo_inicial,
    aportacion_mensual,
    rendimiento_anual,
    anios
):
    """
    Calcula el saldo acumulado año por año.
    """

    saldo = saldo_inicial

    for _ in range(anios):

        for _ in range(12):

            # Primero se agrega la aportación mensual
            saldo += aportacion_mensual

            # Después se aplica rendimiento mensual
            saldo *= 1 + (rendimiento_anual / 100 / 12)

        yield saldo

# TÍTULO

st.title("💰 Calculadora de dinero para jubilación")

st.write(
    "Calcula cuánto dinero podrías acumular para tu jubilación "
    "a partir de tu ahorro actual, tus aportaciones mensuales "
    "y un rendimiento anual estimado."
)

st.divider()

# ENTRADA DE DATOS

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
            "La edad de jubilación debe ser mayor que "
            "la edad actual."
        )

    else:

        anios = edad_jubilacion - edad_actual

        # EVALUACIÓN PEREZOSA

        # Generador que produce el saldo de cada año
        saldos_generador = calcular_ahorro_anual(
            ahorro_inicial,
            aportacion_mensual,
            rendimiento,
            anios
        )

        # map() también devuelve un iterador en Python 3.
        # Los resultados se calculan conforme se consumen.
        proyeccion = map(
            lambda datos: {
                "Edad": datos[0],
                "Ahorro acumulado": datos[1]
            },
            zip(
                range(edad_actual + 1, edad_jubilacion + 1),
                saldos_generador
            )
        )

        # En este punto se consume el iterador para mostrarlo
        # en Streamlit.
        datos_proyeccion = list(proyeccion)

        dinero_final = datos_proyeccion[-1]["Ahorro acumulado"]

        aportado_personalmente = (
            ahorro_inicial +
            aportacion_mensual * 12 * anios
        )

        ganancias = dinero_final - aportado_personalmente

        # RESULTADOS

        st.success(
            f"Proyección calculada para "
            f"{nombre if nombre else 'el usuario'}."
        )

        st.header("📊 Resultado de la jubilación")

        resultado1, resultado2, resultado3 = st.columns(3)

        resultado1.metric(
            "💰 Dinero estimado al jubilarte",
            f"${dinero_final:,.2f} {config['moneda']}"
        )

        resultado2.metric(
            "🏦 Dinero aportado",
            f"${aportado_personalmente:,.2f} {config['moneda']}"
        )

        resultado3.metric(
            "📈 Rendimiento estimado",
            f"${ganancias:,.2f} {config['moneda']}"
        )

        # INFORMACIÓN ADICIONAL

        st.subheader("⏳ Tiempo para tu jubilación")

        st.write(
            f"Te faltan **{anios} años** para llegar "
            f"a los **{edad_jubilacion} años**."
        )

        st.write(
            f"Durante ese periodo realizarías aproximadamente "
            f"**{anios * 12:,} aportaciones mensuales**."
        )

        # GRÁFICA

        st.subheader("📈 Crecimiento estimado del ahorro")

        datos_grafica = {
            registro["Edad"]: registro["Ahorro acumulado"]
            for registro in datos_proyeccion
        }

        st.line_chart(datos_grafica)

        # TABLA

        with st.expander("📋 Ver proyección año por año"):

            for registro in datos_proyeccion:

                st.write(
                    f"**Edad {registro['Edad']}:** "
                    f"${registro['Ahorro acumulado']:,.2f} "
                    f"{config['moneda']}"
                )
st.divider()