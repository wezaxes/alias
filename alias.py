import streamlit as st
import random
import time

# Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate Web", page_icon="🎮", layout="centered")

# Стилізація інтерфейсу
st.markdown("""
    <style>
    .stButton>button { width: 100%; height: 3.5em; font-size: 20px; font-weight: bold; border-radius: 12px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); }
    .word-box { font-size: 42px; text-align: center; font-weight: bold; color: #f9e2af; 
                background-color: #313244; padding: 40px; border-radius: 20px; 
                border: 3px solid #89b4fa; box-shadow: 0 10px 20px rgba(0,0,0,0.3); margin: 20px 0; }
    .score-card { background-color: #45475a; padding: 10px; border-radius: 10px; text-align: center; color: white; }
    </style>
""", unsafe_allow_html=True)

# Завантаження слів
@st.cache_data
def load_words():
    try:
        with open("words.txt", "r", encoding="utf-8") as f:
            words = [line.strip().capitalize() for line in f if line.strip()]
        return sorted(list(set(words)))
    except:
        return ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг"]

# Ініціалізація станів (якщо їх ще немає)
if 'init' not in st.session_state:
    st.session_state.all_words = load_words()
    st.session_state.teams = {}
    st.session_state.team_names = []
    st.session_state.current_team_idx = 0
    st.session_state.current_round = 1
    st.session_state.playing = False
    st.session_state.game_over = False
    st.session_state.init = True

# --- ЕКРАН НАЛАШТУВАНЬ ---
if not st.session_state.playing and not st.session_state.game_over:
    st.title("⚙️ Налаштування Alias")
    
    num_teams = st.slider("Скільки команд грає?", 2, 6, 2)
    
    st.write("### Назви команд:")
    temp_names = []
    cols = st.columns(2)
    for i in range(num_teams):
        with cols[i % 2]:
            name = st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"t{i}")
            temp_names.append(name)
    
    st.session_state.total_rounds = st.number_input("Кількість раундів", 1, 20, 3)
    st.session_state.duration = st.slider("Час на хід (сек)", 10, 120, 60)

    if st.button("🔥 ПОЧАТИ ГРУ"):
        st.session_state.team_names = temp_names
        st.session_state.teams = {name: 0 for name in temp_names}
        random.shuffle(st.session_state.all_words)
        st.session_state.playing = True
        st.rerun()

# --- ЕКРАН ГРИ ---
elif st.session_state.playing:
    current_team = st.session_state.team_names[st.session_state.current_team_idx]
    
    # Хід гри (підготовка або активний таймер)
    if 'start_time' not in st.session_state:
        st.title(f"Черга команди: {current_team}")
        st.info(f"Раунд: {st.session_state.current_round} / {st.session_state.total_rounds}")
        if st.button(f"Я ГОТОВИЙ(-А)! ▶️"):
            st.session_state.start_time = time.time()
            st.session_state.current_word = st.session_state.all_words.pop(0) if st.session_state.all_words else "КІНЕЦЬ"
            st.rerun()
    else:
        # Активний раунд з таймером
        elapsed = time.time() - st.session_state.start_time
        time_left = int(st.session_state.duration - elapsed)

        if time_left <= 0:
            st.warning("🔔 ЧАС ВИЙШОВ!")
            del st.session_state.start_time
            
            # Перехід ходу
            if st.session_state.current_team_idx < len(st.session_state.team_names) - 1:
                st.session_state.current_team_idx += 1
            else:
                st.session_state.current_team_idx = 0
                st.session_state.current_round += 1
            
            # Перевірка на кінець гри
            if st.session_state.current_round > st.session_state.total_rounds:
                st.session_state.playing = False
                st.session_state.game_over = True
            st.rerun()
        else:
            st.progress(time_left / st.session_state.duration)
            st.subheader(f"⏱ {time_left} сек | {current_team}: {st.session_state.teams[current_team]} ⭐")
            
            st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ ВГАДАНО"):
                    st.session_state.teams[current_team] += 1
                    st.session_state.current_word = st.session_state.all_words.pop(0) if st.session_state.all_words else "КІНЕЦЬ"
                    st.rerun()
            with c2:
                if st.button("❌ СКІП"):
                    st.session_state.teams[current_team] -= 1
                    st.session_state.current_word = st.session_state.all_words.pop(0) if st.session_state.all_words else "КІНЕЦЬ"
                    st.rerun()
            time.sleep(0.1)
            st.rerun()

# --- ЕКРАН ФІНАЛУ ---
elif st.session_state.game_over:
    st.title("🏆 ФІНАЛЬНИЙ РАХУНОК")
    sorted_scores = sorted(st.session_state.teams.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, score) in enumerate(sorted_scores):
        st.markdown(f"### {i+1}. {name}: {score} балів")
    
    if st.button("ЗІГРАТИ ЩЕ РАЗ 🔄"):
        st.session_state.clear()
        st.rerun()
