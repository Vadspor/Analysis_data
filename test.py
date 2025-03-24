import streamlit as st

# Значення за замовчуванням
DEFAULT_SLIDER1 = 25
DEFAULT_SLIDER2 = 50

# Ініціалізація значень при першому запуску
if 'slider1' not in st.session_state:
    st.session_state.slider1 = DEFAULT_SLIDER1
if 'slider2' not in st.session_state:
    st.session_state.slider2 = DEFAULT_SLIDER2

# Функція скидання, яка повертає слайдери до значень за замовчуванням
def reset_sliders():
    st.session_state.slider1 = DEFAULT_SLIDER1
    st.session_state.slider2 = DEFAULT_SLIDER2

# Інтерфейс
st.title("Демонстрація скидання слайдерів")

# Кнопка скидання значень
st.button("Скинути значення слайдерів", on_click=reset_sliders)

# Слайдери з прив'язкою до session_state через key
col1, col2 = st.columns(2)
with col1:
    slider1_val = st.slider("Слайдер 1", 0, 100, key="slider1")
    st.write(f"Значення: {slider1_val}")
with col2:
    slider2_val = st.slider("Слайдер 2", 0, 100, key="slider2")
    st.write(f"Значення: {slider2_val}")

# Додаткова інформація для демонстрації
st.info(f"Стандартні значення: Слайдер 1 = {DEFAULT_SLIDER1}, Слайдер 2 = {DEFAULT_SLIDER2}")