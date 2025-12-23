import streamlit as st
import random
import time

# Налаштування сторінки
st.set_page_config(page_title="Alias Pro Max", page_icon="🎮")

# Стиль кнопок та інтерфейсу
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3em; font-size: 20px; font-weight: bold; border-radius: 10px; }
    .word-box { font-size: 40px; text-align: center; font-weight: bold; color: #f9e2af; 
                background-color: #313244; padding: 30px; border-radius: 15px; border: 2px solid #89b4fa; }
    </style>
""", unsafe_allow_html=True)

# Завантаження слів з твого файлу words.txt
@st.cache_data
def load_words():
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except:
        return ["Помилка файлу words.txt", "Перевірте назву"]

# Ініціалізація гри
if 'words_list' not in st.session_state:
    st.session_state.words_list = load_words()
    random.shuffle(st.session_state.words_list)
if 'score' not in st.session_state: st.session_state.score = 0
if 'playing' not in st.session_state: st.session_state.playing = False
if 'current_word' not in st.session_state: st.session_state.current_word = ""

def next_word():
    if st.session_state.words_list:
        st.session_state.current_word = st.session_state.words_list.pop(0)
    else:
        st.session_state.current_word = "СЛОВА ЗАКІНЧИЛИСЯ"

# ЕКРАН ГРИ
st.title("🎮 Alias Pro Max")

if not st.session_state.playing:
    st.write(f"Готово до гри! У базі: **{len(st.session_state.words_list)}** слів.")
    duration = st.number_input("Час раунду (сек)", min_value=10, max_value=300, value=60)
    if st.button("ПОЧАТИ РАУНД"):
        st.session_state.playing = True
        st.session_state.start_time = time.time()
        st.session_state.duration = duration
        next_word()
        st.rerun()
else:
    time_left = int(st.session_state.duration - (time.time() - st.session_state.start_time))
    
    if time_left <= 0:
        st.error("⏰ ЧАС ВИЙШОВ!")
        st.metric("Результат", f"{st.session_state.score} балів")
        if st.button("ГРАТИ ЗНОВУ"):
            st.session_state.playing = False
            st.session_state.score = 0
            st.rerun()
    else:
        st.subheader(f"⏱ Час: {time_left} сек | ⭐ Бали: {st.session_state.score}")
        st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ ВГАДАНО"):
                st.session_state.score += 1
                next_word()
                st.rerun()
        with col2:
            if st.button("❌ СКІП"):
                st.session_state.score -= 1
                next_word()
                st.rerun()
        
        time.sleep(0.1)
        st.rerun()
