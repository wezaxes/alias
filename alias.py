import streamlit as st
import random
import time

# Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# Стилізація інтерфейсу
st.markdown("""
    <style>
    .stButton>button { 
        width: 100%; 
        height: 4.5em; 
        font-size: 24px !important; 
        font-weight: bold; 
        border-radius: 15px; 
        transition: 0.3s; 
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .stButton>button:hover { transform: scale(1.02); }
    
    .word-box { 
        font-size: 42px; 
        text-align: center; 
        font-weight: bold; 
        color: #f9e2af; 
        background-color: #313244; 
        padding: 50px; 
        border-radius: 20px; 
        border: 3px solid #89b4fa; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.3); 
        margin: 20px 0; 
    }
    
    .disclaimer-box {
        text-align: center;
        background-color: #45475a;
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #f38ba8;
    }
    </style>
""", unsafe_allow_html=True)

# Завантаження слів
@st.cache_data
def load_initial_words():
    # Початковий набір слів, якщо файлу немає
    return ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Wezaxes", "Тілт"]

# Ініціалізація станів
if 'init_done' not in st.session_state:
    st.session_state.all_words = load_initial_words()
    st.session_state.teams = {}
    st.session_state.team_names = []
    st.session_state.current_team_idx = 0
    st.session_state.current_round = 1
    st.session_state.playing = False
    st.session_state.game_over = False
    st.session_state.welcome_done = False
    st.session_state.init_done = True

# --- 1. ЕКРАН ДИСКЛЕЙМЕРА ---
if not st.session_state.welcome_done:
    st.markdown("<h2 style='text-align: center; color: #fab387;'>ДИСКЛЕЙМЕР</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer-box">
            <h2 style='color: #f38ba8; margin-top: 0;'>УВАГА КОД ПИСАЛА ЖІНКА‼️</h2>
            <p style='font-size: 18px; color: #cdd6f4;'>
                Це <b>СУПЕР пробна версія</b>, все ще буде допрацьовуватись.<br>
                Шанс отримати дибільне слово <b>70%</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("ЛАДНО ✅"):
        st.session_state.welcome_done = True
        st.rerun()
    st.stop()

# --- 2. ЕКРАН НАЛАШТУВАНЬ ---
if not st.session_state.playing and not st.session_state.game_over:
    st.title("⚙️ Налаштування Alias")
    
    # СЕКЦІЯ ДОДАВАННЯ СЛІВ
    with st.expander("➕ Додати своє дебільне слово"):
        new_word = st.text_input("Введи слово:", placeholder="Наприклад: Солевар").strip().capitalize()
        if st.button("ДОДАТИ В СЛОВНИК"):
            if new_word:
                if new_word in st.session_state.all_words:
                    st.error("Таке слово вже є, давай придумаємо щось прикольніше")
                else:
                    st.session_state.all_words.append(new_word)
                    st.success(f"Слово '{new_word}' додано! Тепер їх {len(st.session_state.all_words)}")
            else:
                st.warning("Ну введи хоч щось...")

    st.divider()
    
    num_teams = st.slider("Скільки команд грає?", 2, 6, 2)
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
        # Робимо копію слів для гри, щоб перемішати їх
        st.session_state.game_words = st.session_state.all_words.copy()
        random.shuffle(st.session_state.game_words)
        st.session_state.playing = True
        st.rerun()

# --- 3. ЕКРАН ГРИ ---
elif st.session_state.playing:
    current_team = st.session_state.team_names[st.session_state.current_team_idx]
    
    if 'start_time' not in st.session_state:
        st.title(f"Черга: {current_team}")
        st.info(f"Раунд: {st.session_state.current_round} / {st.session_state.total_rounds}")
        if st.button(f"Я ГОТОВИЙ(-А)! ▶️"):
            st.session_state.start_time = time.time()
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "СЛОВА СКІНЧИЛИСЬ"
            st.rerun()
    else:
        elapsed = time.time() - st.session_state.start_time
        time_left = int(st.session_state.duration - elapsed)

        if time_left <= 0:
            st.warning("🔔 ЧАС ВИЙШОВ!")
            del st.session_state.start_time
            if st.session_state.current_team_idx < len(st.session_state.team_names) - 1:
                st.session_state.current_team_idx += 1
            else:
                st.session_state.current_team_idx = 0
                st.session_state.current_round += 1
            
            if st.session_state.current_round > st.session_state.total_rounds:
                st.session_state.playing = False
                st.session_state.game_over = True
            st.rerun()
        else:
            st.progress(max(0.0, min(time_left / st.session_state.duration, 1.0)))
            st.subheader(f"⏱ {time_left} сек | {current_team}: {st.session_state.teams[current_team]} ⭐")
            
            st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
            
            if st.button("✅ ВГАДАНО"):
                st.session_state.teams[current_team] += 1
                st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
                st.rerun()
            
            if st.button("❌ СКІП"):
                st.session_state.teams[current_team] -= 1
                st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
                st.rerun()
                
            time.sleep(0.1)
            st.rerun()

# --- 4. ЕКРАН ФІНАЛУ ---
elif st.session_state.game_over:
    st.title("🏆 ФІНАЛЬНИЙ РАХУНОК")
    sorted_scores = sorted(st.session_state.teams.items(), key=lambda x: x[1], reverse=True)
    
    for i, (name, score) in enumerate(sorted_scores):
        st.markdown(f"### {i+1}. {name}: {score} балів")
    
    if st.button("ЗІГРАТИ ЩЕ РАЗ 🔄"):
        # Очищаємо все, крім загального списку слів
        words_backup = st.session_state.all_words
        st.session_state.clear()
        st.session_state.all_words = words_backup
        st.session_state.init_done = True
        st.session_state.welcome_done = True # Щоб не бачити дисклеймер знову
        st.rerun()
