import streamlit as st
from pickle import load
import numpy as np
from gtts import gTTS

# Cargar el modelo
model = load(open("./models/randomforest_classifier__boot-Fal_criterion-entr_max_depth-None_max_feat-sqrt_max_nod-10_min_samples-1_min_split-10_n_est-100_42.sav", "rb"))

# Definir opciones de idioma
languages = {"Español": "es", "Inglés": "en"}
outcome = {"0": "Negativo", "1": "Positivo"}

# Configuración en una barra lateral
with st.sidebar:
    st.title("Configuración")
    language = st.selectbox("Seleccione un idioma:", list(languages.keys()))
    font_size = st.slider("Tamaño del texto", min_value=12, max_value=32, value=16)

# Texto dinámico según el idioma seleccionado
if language == "Español":
    text_labels = {
        "title": "Test de diabetes - Diagnóstico",
        "instructions": """
            ### Instrucciones:
            1. Ingrese sus datos en los cuadros proporcionados.
            2. Ajuste los parámetros según sea necesario.
            3. Presione el botón "Predecir" para ver el resultado.
        """,
        "glucose": "Concentración de glucosa (2 horas antes del test)",
        "pressure": "Presión arterial (mm Hg)",
        "insulin": "Nivel de insulina (µU/mL)",
        "thickness": "Grosor del pliegue cutáneo del tríceps (mm)",
        "bmi": "Índice de masa corporal (BMI)",
        "age": "Edad",
        "pedigree": "Pedigrí de diabetes",
        "pregnancies": "Número de embarazos (0 = No embarazo)",
        "predict": "Predecir",
        "success": "Datos ingresados correctamente. Procesando predicción...",
        "positive": "Positivo: Es posible que tenga diabetes.",
        "negative": "Negativo: Es poco probable que tenga diabetes.",
        "caption": "La salud es para todos",
    }
else:  # Inglés
    text_labels = {
        "title": "Diabetes Test - Diagnosis",
        "instructions": """
            ### Instructions:
            1. Enter your data in the fields provided.
            2. Adjust the parameters as needed.
            3. Press the "Predict" button to see the result.
        """,
        "glucose": "Glucose concentration (2 hours before the test)",
        "pressure": "Blood pressure (mm Hg)",
        "insulin": "Insulin level (µU/mL)",
        "thickness": "Skin thickness of the triceps (mm)",
        "bmi": "Body Mass Index (BMI)",
        "age": "Age",
        "pedigree": "Diabetes pedigree",
        "pregnancies": "Number of pregnancies (0 = No pregnancies)",
        "predict": "Predict",
        "success": "Data successfully entered. Processing prediction...",
        "positive": "Positive: You may have diabetes.",
        "negative": "Negative: You are unlikely to have diabetes.",
        "caption": "Health is for everyone",
    }

# Aplicar el tamaño de fuente global
st.markdown(
    f"""
    <style>
    body, label, input, button, h1, h2, h3, p {{
        font-size: {font_size}px !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Mostrar título
st.image("https://www.ccomsuam.org/wp-content/uploads/2017/11/hospital-links-logo.png", width=400)
st.title(text_labels["title"])

# Mostrar instrucciones
st.markdown(text_labels["instructions"])

# Botones de audio al lado de cada texto
def play_audio(text, lang):
    tts = gTTS(text, lang=lang)
    audio_file = f"{text[:10].replace(' ', '_')}.mp3"
    tts.save(audio_file)
    return audio_file

# Columnas de entrada con audio
left, right = st.columns(2)
with left:
    Glucose = st.text_input(text_labels["glucose"])
    st.audio(play_audio(text_labels["glucose"], languages[language]))
    BloodPressure = st.text_input(text_labels["pressure"])
    st.audio(play_audio(text_labels["pressure"], languages[language]))
    Insulin = st.text_input(text_labels["insulin"])
    st.audio(play_audio(text_labels["insulin"], languages[language]))
    SkinThickness = st.text_input(text_labels["thickness"])
    st.audio(play_audio(text_labels["thickness"], languages[language]))
with right:
    BMI = st.text_input(text_labels["bmi"])
    st.audio(play_audio(text_labels["bmi"], languages[language]))
    Age = st.text_input(text_labels["age"])
    st.audio(play_audio(text_labels["age"], languages[language]))
    DiabetesPedigreeFunction = st.text_input(text_labels["pedigree"])
    st.audio(play_audio(text_labels["pedigree"], languages[language]))
    Pregnancies = st.slider(text_labels["pregnancies"], min_value=0, max_value=10, step=1)

# Botón para predecir
if st.button(text_labels["predict"]):
    if not Glucose or not BloodPressure or not Insulin or not BMI or not Age or not DiabetesPedigreeFunction or not SkinThickness:
        st.error("Por favor, complete todos los campos antes de continuar." if language == "Español" else "Please complete all fields before proceeding.")
    else:
        # Procesamos los datos
        Glucose = float(Glucose)
        BloodPressure = float(BloodPressure)
        Insulin = float(Insulin)
        BMI = float(BMI)
        Age = float(Age)
        SkinThickness = float(SkinThickness)
        DiabetesPedigreeFunction = float(DiabetesPedigreeFunction)
        Pregnancies = float(Pregnancies)
        
        # Predicción
        data = np.array([[Glucose, BloodPressure, Insulin, SkinThickness, BMI, Age, DiabetesPedigreeFunction, Pregnancies]])
        st.info(text_labels["success"])
        prediction = str(model.predict(data)[0])
        result = text_labels["positive"] if prediction == "1" else text_labels["negative"]
        
        # Mostrar resultado
        st.success(result)

# Imagen inclusiva al final
st.image(
    "https://escueladepacientestuc.gob.ar/wp-content/uploads/2023/10/test-de-riesgo-1024x683.jpg",
    use_container_width=True
)