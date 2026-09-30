"""
Estimador de tiempo de viaje tipo Uber
Hannia Macias Gómez
30 de septiembre de 2026

Aplicación desarrollada con Python y Streamlit.

 El recorrido se divide en varios segmentos. Cada segmento
 contiene su distancia y la velocidad promedio estimada.

 La función map() aplica calcular_tiempo_segmento
 a cada segmento.

 En Python 3, map() devuelve un iterador. Esto significa
 que los tiempos no se calculan todos inmediatamente.

 Los resultados se generan conforme son solicitados.
 En este programa, sum() consume el iterador para obtener
 el tiempo total del recorrido.

 Este comportamiento corresponde al concepto de
 **evaluación perezosa (lazy evaluation)**.
"""

import json
from pathlib import Path
import streamlit as st

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Estimador de viaje",
    page_icon="🚗",
    layout="wide"
)

# ---------------------------------------------------------
# CREAR Y CARGAR CONFIG.JSON
# ---------------------------------------------------------

RUTA_CONFIG = Path(__file__).parent / "config.json"

# Valores predeterminados de la aplicación
CONFIG_PREDETERMINADA = {
    "tiempo_espera_conductor": 5,
    "numero_segmentos": 5,

    "tipos_ruta": {
        "🟢 Tráfico ligero": {
            "velocidad_promedio": 55
        },
        "🟡 Tráfico moderado": {
            "velocidad_promedio": 35
        },
        "🔴 Tráfico pesado": {
            "velocidad_promedio": 20
        }
    },

    "tipos_servicio": {
        "UberX": {
            "factor_tiempo": 1.00
        },
        "Uber Comfort": {
            "factor_tiempo": 1.03
        },
        "Uber Black": {
            "factor_tiempo": 1.05
        }
    }
}


# Si config.json no existe, se crea automáticamente
if not RUTA_CONFIG.exists():

    with open(RUTA_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(
            CONFIG_PREDETERMINADA,
            archivo,
            indent=4,
            ensure_ascii=False
        )

# CREAR Y CARGAR CONFIG.JSON

RUTA_CONFIG = Path(__file__).parent / "config.json"

# Valores predeterminados de la aplicación
CONFIG_PREDETERMINADA = {
    "tiempo_espera_conductor": 5,
    "numero_segmentos": 5,

    "tipos_ruta": {
        "🟢 Tráfico ligero": {
            "velocidad_promedio": 55
        },
        "🟡 Tráfico moderado": {
            "velocidad_promedio": 35
        },
        "🔴 Tráfico pesado": {
            "velocidad_promedio": 20
        }
    },

    "tipos_servicio": {
        "UberX": {
            "factor_tiempo": 1.00
        },
        "Uber Comfort": {
            "factor_tiempo": 1.03
        },
        "Uber Black": {
            "factor_tiempo": 1.05
        }
    }
}


# Si config.json no existe, se crea automáticamente
if not RUTA_CONFIG.exists():

    with open(RUTA_CONFIG, "w", encoding="utf-8") as archivo:
        json.dump(
            CONFIG_PREDETERMINADA,
            archivo,
            indent=4,
            ensure_ascii=False
        )


# Cargar los datos del archivo JSON
try:

    with open(RUTA_CONFIG, "r", encoding="utf-8") as archivo:
        CONFIG = json.load(archivo)

except json.JSONDecodeError:

    st.error("El archivo config.json contiene un formato incorrecto.")
    st.stop()


# Convertir las opciones a tuplas (valores inmutables)

TIPOS_RUTA = tuple(CONFIG["tipos_ruta"].keys())

TIPOS_SERVICIO = tuple(CONFIG["tipos_servicio"].keys())

# FUNCIÓN PARA CALCULAR EL TIEMPO

def calcular_tiempo_segmento(segmento):
    """
    Calcula los minutos necesarios para recorrer
    un segmento del viaje.
    """

    distancia, velocidad = segmento

    horas = distancia / velocidad
    minutos = horas * 60

    return minutos

# FUNCIÓN CON MAP Y EVALUACIÓN PEREZOSA

def calcular_segmentos(segmentos):

    # map NO calcula inmediatamente todos los resultados.
    # Devuelve un iterador.
    # Cada tiempo se calcula cuando el iterador es recorrido.

    tiempos = map(calcular_tiempo_segmento, segmentos)

    return tiempos

# TÍTULO

st.title("🚗 Estimador de tiempo de viaje en Uber")

st.write(
    "Simula el tiempo aproximado de un viaje ingresando "
    "la distancia, condiciones de tránsito y tipo de servicio."
)

st.divider()

# DATOS DEL VIAJE

st.subheader("📍 Información del viaje")

col1, col2 = st.columns(2)

with col1:

    origen = st.text_input(
        "Lugar de origen",
        placeholder="Ejemplo: Centro de Querétaro"
    )

with col2:

    destino = st.text_input(
        "Destino",
        placeholder="Ejemplo: Universidad"
    )


distancia = st.slider(
    "Distancia aproximada del viaje (km)",
    min_value=1.0,
    max_value=100.0,
    value=10.0,
    step=0.5
)

# CONDICIONES DEL VIAJE

st.subheader("⚙️ Condiciones del viaje")

col3, col4 = st.columns(2)

with col3:

    tipo_ruta = st.selectbox(
        "Condición del tránsito",
        TIPOS_RUTA
    )

with col4:

    tipo_servicio = st.selectbox(
        "Tipo de servicio",
        TIPOS_SERVICIO
    )

# INFORMACIÓN OBTENIDA DEL JSON

velocidad = CONFIG["tipos_ruta"][tipo_ruta]["velocidad_promedio"]

factor_servicio = CONFIG["tipos_servicio"][tipo_servicio]["factor_tiempo"]


st.write(
    f"Velocidad promedio estimada: **{velocidad} km/h**"
)

# SIMULACIÓN DEL VIAJE

st.divider()

if st.button(
    "🚘 Calcular tiempo del viaje",
    type="primary",
    use_container_width=True
):

    if not origen or not destino:

        st.warning(
            "Ingresa un lugar de origen y un destino."
        )

    elif origen.strip().lower() == destino.strip().lower():

        st.warning(
            "El origen y el destino deben ser diferentes."
        )

    else:

        # Dividimos el recorrido en segmentos.
        # Esto permite utilizar map() para calcular
        # cada parte del viaje.

        numero_segmentos = CONFIG["numero_segmentos"]

        distancia_segmento = distancia / numero_segmentos

        segmentos = tuple(
            (distancia_segmento, velocidad)
            for _ in range(numero_segmentos)
        )

        # MAP CON EVALUACIÓN PEREZOSA

        tiempos_iterador = calcular_segmentos(segmentos)

        # Hasta este punto map() todavía mantiene
        # los resultados como un iterador.
        # sum() consume el iterador y solicita cada cálculo.

        tiempo_movimiento = sum(tiempos_iterador)


        # Tiempo adicional según el servicio seleccionado

        tiempo_movimiento *= factor_servicio


        # Tiempo de espera del conductor

        tiempo_espera = CONFIG["tiempo_espera_conductor"]


        # Tiempo total

        tiempo_total = tiempo_movimiento + tiempo_espera

        # RESULTADOS

        st.success("✅ Cálculo realizado correctamente")

        st.subheader("📊 Resultado del viaje")

        col5, col6, col7 = st.columns(3)

        with col5:

            st.metric(
                "Distancia",
                f"{distancia:.1f} km"
            )

        with col6:

            st.metric(
                "Tiempo de traslado",
                f"{tiempo_movimiento:.0f} min"
            )

        with col7:

            st.metric(
                "Tiempo total estimado",
                f"{tiempo_total:.0f} min"
            )

        # PROGRESO DEL VIAJE

        st.subheader("🛣️ Simulación del recorrido")

        progreso = st.progress(0)

        for porcentaje in range(0, 101, 10):
            progreso.progress(porcentaje)

        # RESUMEN

        st.subheader("🧾 Resumen")

        st.write(f"**Origen:** {origen}")
        st.write(f"**Destino:** {destino}")
        st.write(f"**Tránsito:** {tipo_ruta}")
        st.write(f"**Servicio:** {tipo_servicio}")
        st.write(f"**Velocidad promedio:** {velocidad} km/h")
        st.write(f"**Espera del conductor:** {tiempo_espera} min")

        st.info(
            f"El viaje de {origen} a {destino} "
            f"tendrá una duración aproximada de "
            f"{tiempo_total:.0f} minutos."
        )

st.divider()