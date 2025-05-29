import streamlit as st
from datetime import datetime
import pandas as pd
import altair as alt

# Configuración de página para usar todo el ancho
st.set_page_config(layout="wide")

# --------------------------
# DEFINICIONES DE CLASES (deben estar en el ámbito global)
# --------------------------
# Interfaz del Observador
class Observer:
    def update(self, temperature):
        pass

# Sujeto: Sensor de Temperatura
class TemperatureSensor:
    def __init__(self):
        self._observers = []  # Lista de observadores registrados
        self._temperature = 0  # Temperatura actual

    def attach(self, observer):
        self._observers.append(observer)  # Agrega un observador

    def detach(self, observer):
        self._observers.remove(observer)  # Elimina un observador

    def notify(self):
        # Notifica a todos los observadores del cambio de temperatura
        for observer in self._observers:
            observer.update(self._temperature)

    def set_temperature(self, new_temperature):
        # Actualiza la temperatura y notifica a los observadores
        self._temperature = new_temperature
        st.success(f"[Sensor] Temperatura actualizada a: {new_temperature}°C")
        self.notify()

# Observadores concretos

# Muestra la temperatura en pantalla
class ScreenDisplay(Observer):
    def update(self, temperature):
        st.info(f"[Pantalla] Temperatura mostrada: {temperature}°C")

# Registra el historial de temperaturas
class DataLogger(Observer):
    def __init__(self):
        self.logs = []  # Almacena tuplas (timestamp, temperatura)
    # Inicializa el logger con una lista vacía
    def update(self, temperature):
        timestamp = datetime.now().isoformat(timespec='seconds')
        self.logs.append((timestamp, temperature))

    def show_logs(self):
        # Muestra el historial de temperaturas
        for timestamp, temperature in self.logs:
            st.write(f"[Logger] {timestamp} - {temperature}°C")

    def get_dataframe(self):
        # Devuelve los logs como un DataFrame de pandas
        return pd.DataFrame(self.logs, columns=["Timestamp", "Temperatura"]).set_index("Timestamp").reset_index()

# Sistema de alerta si la temperatura es alta
class AlarmSystem(Observer):
    def update(self, temperature):
        if temperature > 30:
            st.error("[Alarma] ¡Temperatura elevada!")



# --------------------------
# INTERFAZ DE 3 COLUMNAS
# --------------------------

col1, col2, col3 = st.columns([1, 1, 1])

# Columna 1: Código fuente
with col1:
    st.header("📄 Código Fuente")
    with st.expander("Ver código completo", expanded=True):
        st.code("""
# Definición de la interfaz Observer
# Interfaz del Observador
class Observer:
    def update(self, temperature):
        pass

# Implementación del Sensor Sujeto: Sensor de Temperatura
class TemperatureSensor:
    def __init__(self):
        self._observers = [] # Lista de observadores registrados
        self._temperature = 0 # Temperatura actual

    def attach(self, observer): # Agrega un observador
        self._observers.append(observer)

    def detach(self, observer): # Elimina un observador
        self._observers.remove(observer)

    def notify(self):
        # Notifica a todos los observadores del cambio de temperatura
        for observer in self._observers:
            observer.update(self._temperature)

    def set_temperature(self, new_temp):
        # Actualiza la temperatura y notifica a los observadores
        self._temperature = new_temp
        st.success(f"Temp actualizada: {new_temp}°C")
        self.notify()
                
# Observadores concretos

# Muestra la temperatura en pantalla
# Implementación de observadores
class ScreenDisplay(Observer):
    def update(self, temperature):
        st.info(f"Mostrando: {temperature}°C")
# Registra el historial de temperaturas
class DataLogger(Observer):
    def __init__(self):
        self.logs = []
    # Inicializa el logger con una lista vacía
    def update(self, temperature):
        timestamp = datetime.now()
        self.logs.append((timestamp, temperature))
    
    def show_logs(self):
        # Muestra el historial de temperaturas
        for ts, temp in self.logs:
            st.write(f"{ts} - {temp}°C")

# Sistema de alerta si la temperatura es alta
class AlarmSystem(Observer):
    def update(self, temperature):
        if temperature > 30:
            st.error("¡Temperatura elevada!")

# Nota:
# La clase Observer se define como interfaz base para los
# observadores concretos (ScreenDisplay, DataLogger, AlarmSystem).
# No se instancia ni se usa directamente, solo sirve como referencia
# para asegurar que los observadores implementen el método update.

""", language='python')










# Columna 2: Aplicación funcional
with col2:
    # Interfaz gráfica con Streamlit
    st.title("🌡️ Simulación del Patrón Observer - Sensor de Temperatura")

    # Inicialización de objetos en sesión
    if "sensor" not in st.session_state:
        st.session_state.sensor = TemperatureSensor()
        st.session_state.logger = DataLogger()
        st.session_state.sensor.attach(ScreenDisplay())
        st.session_state.sensor.attach(st.session_state.logger)
        st.session_state.sensor.attach(AlarmSystem())

    # Entrada de temperatura por el usuario
    temp_input = st.number_input("Ingrese nueva temperatura:", min_value=-50.0, max_value=100.0, value=25.0)

    if st.button("Actualizar Temperatura"):
        st.session_state.sensor.set_temperature(temp_input)

    # Mostrar registros de temperatura
    with st.expander("📋 Ver historial de temperaturas"):
        st.session_state.logger.show_logs()

    # Mostrar gráfica de la evolución de la temperatura
    with st.expander("📈 Ver gráfica en tiempo real"):
        df = st.session_state.logger.get_dataframe()
        if not df.empty:
            chart = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X("Timestamp:T", title="Hora"),
                y=alt.Y("Temperatura:Q", title="°C"),
                tooltip=["Timestamp", "Temperatura"]
            ).properties(
                title="Evolución de la Temperatura",
                width=700,
                height=400
            ).interactive()
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Aún no hay datos para graficar.")

    #Explicación del sistema
    st.info("""
    ### ¿Cómo funciona este sistema?
    Este sistema simula el **Patrón de Diseño Observer** en un contexto de sensores de temperatura.

    - El **Sensor de Temperatura** es el sujeto que detecta los cambios.
    - Los **observadores** (Pantalla, Registrador de Datos, Alarma) reaccionan automáticamente cuando la temperatura cambia.
    - Puedes ingresar una nueva temperatura y ver cómo:
      - Se muestra en pantalla,
      - Se registra con fecha y hora,
      - Y se activa una alarma si supera los 30 °C.

    ### ¿Cómo usarlo?
    1. Ingresa un valor en el campo de temperatura.
    2. Haz clic en "Actualizar Temperatura".
    3. Revisa el historial y la gráfica en tiempo real.
    """)
# Nota:
# La clase Observer se define como interfaz base para los observadores concretos (ScreenDisplay, DataLogger, AlarmSystem).
# No se instancia ni se usa directamente, solo sirve como referencia para asegurar que los observadores implementen el método update.





# Columna 3: Diagrama UML
with col3:
    st.header("📌 Diagrama UML")
    st.image("img/sensor.png", caption="Diagrama UML del sistema", use_container_width=True)  # Parámetro actualizado