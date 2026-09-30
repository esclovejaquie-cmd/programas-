"""
Estimador de tiempo de viaje tipo Uber utilizando Lambda
Hannia Macias Gómez
30 de septiembre de 2026

  La función lambda se utiliza para calcular el tiempo
  necesario para recorrer cada segmento del viaje.

  Recibe como parámetros la distancia del segmento y
  la velocidad promedio. Posteriormente divide la
  distancia entre la velocidad y convierte el resultado
  de horas a minutos.

  Se utilizó lambda porque permite realizar este cálculo
  sencillo mediante una función anónima escrita en una
  sola expresión.
"""

import json
from pathlib import Path
import streamlit as st

# CONFIGURACIÓN DE LA PÁGINA

st.set_page_config(
    page_title="Estimador de viaje en Uber con Lambda",
    page_icon="🚗",
    layout="wide"
)

# CREAR Y CARGAR CONFIG.JSON

RUTA_CONFIG = Path(__file__).parent / "config.json"

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


# Cargar información del JSON
try:

    with open(RUTA_CONFIG, "r", encoding="utf-8") as archivo:
        CONFIG = json.load(archivo)

except json.JSONDecodeError:

    st.error("El archivo config.json contiene un formato incorrecto.")
    st.stop()

# VALORES INMUTABLES
# Se utilizan tuplas porque son estructuras inmutables.

TIPOS_RUTA = tuple(CONFIG["tipos_ruta"].keys())

TIPOS_SERVICIO = tuple(CONFIG["tipos_servicio"].keys())

# FUNCIÓN LAMBDA

# Recibe la distancia y velocidad de un segmento.
# Devuelve el tiempo del recorrido en minutos.

calcular_tiempo = lambda distancia, velocidad: (
    distancia / velocidad
) * 60

# TÍTULO

st.title("🚗 Estimador de tiempo de viaje en Uber con Lambda")

st.write(
    "Ingresa los datos de tu recorrido para obtener una "
    "estimación del tiempo total del viaje."
)

st.divider()

# INFORMACIÓN DEL VIAJE

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
    
# OBTENER VALORES DEL JSON

velocidad = CONFIG["tipos_ruta"][tipo_ruta]["velocidad_promedio"]

factor_servicio = CONFIG["tipos_servicio"][tipo_servicio]["factor_tiempo"]

st.write(
    f"Velocidad promedio estimada: **{velocidad} km/h**"
)

# BOTÓN PARA CALCULAR

st.divider()

if st.button(
    "🚘 Calcular tiempo del viaje",
    type="primary",
    use_container_width=True
):

    # Validar campos
    if not origen or not destino:

        st.warning(
            "Ingresa un lugar de origen y un destino."
        )

    elif origen.strip().lower() == destino.strip().lower():

        st.warning(
            "El origen y el destino deben ser diferentes."
        )

    else:

        # DIVIDIR EL RECORRIDO EN SEGMENTOS

        numero_segmentos = CONFIG["numero_segmentos"]

        distancia_segmento = distancia / numero_segmentos

        # UTILIZACIÓN DE LA FUNCIÓN LAMBDA

        tiempos_segmentos = []

        for _ in range(numero_segmentos):

            tiempo = calcular_tiempo(
                distancia_segmento,
                velocidad
            )

            tiempos_segmentos.append(tiempo)


        # Sumar los tiempos de todos los segmentos

        tiempo_movimiento = sum(tiempos_segmentos)


        # Aplicar el factor del tipo de servicio

        tiempo_movimiento *= factor_servicio


        # Tiempo que tarda en llegar el conductor

        tiempo_espera = CONFIG["tiempo_espera_conductor"]


        # Tiempo total estimado

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

        # SIMULACIÓN DEL RECORRIDO

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