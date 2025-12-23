import streamlit as st
import random
import time

# 1. Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate", page_icon="🎮")

# 2. Стилізація (CSS)
st.markdown("""
    <style>
    .stButton > button {
        width: 100% !important;
        height: 4em !important;
        font-size: 22px !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        margin-bottom: 10px !important;
    }
    h1, h2, h3, p, .stMarkdown { text-align: center !important; }
    .word-box { 
        font-size: 40px; text-align: center; font-weight: bold; color: #f9e2af; 
        background-color: #313244; padding: 40px; border-radius: 20px; 
        border: 3px solid #89b4fa; margin: 20px 0; 
    }
    .disclaimer-box {
        text-align: center; background-color: #45475a; padding: 20px;
        border-radius: 15px; border: 2px solid #f38ba8; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Ініціалізація даних
if 'all_words' not in st.session_state:
    st.session_state.all_words = ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Паляниця"]
if 'welcome_done' not in st.session_state:
    st.session_state.welcome_done = False
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'last_added' not in st.session_state:
    st.session_state.last_added = ""

# --- ЕКРАН 1: ДИСКЛЕЙМЕР ---
if not st.session_state.welcome_done:
    st.markdown("## WEZAXES ENTERTAINMENT")
    st.markdown("""
        <div class="disclaimer-box">
            <h2 style='color: #f38ba8;'>УВАГА КОД ПИСАЛА ЖІНКА‼️</h2>
            <p>Це СУПЕР пробна версія. Шанс отримати дибільне слово 70%.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("ЛАДНО ✅"):
        st.session_state.welcome_done = True
        st.rerun()
    st.stop()

# --- ЕКРАН 2: НАЛАШТУВАННЯ ---
if not st.session_state.game_started and not st.session_state.game_over:
    st.title("⚙️ Налаштування")
    
    with st.expander("➕ Додати дебільне слово"):
        st.write("Вписуйте тільки грабельні слова!")
        ex = random.choice(st.session_state.all_words)
        new_w = st.text_input("Введи слово:", placeholder=f"Наприклад: {ex}").strip().capitalize()
        
        if st.button("ДОДАТИ"):
            if new_w:
                if new_w in st.session_state.all_words:
                    st.error("Таке слово вже є, давай придумаємо щось прикольніше")
                else:
                    st.session_state.all_words.append(new_w)
                    st.session_state.last_added = new_w
                    st.success("Вітаю, ви придумали нове прикольне слово, дякую!")
        if st.session_state.last_added:
            st.write(f"Останнє додане: **{st.session_state.last_added}**")

    st.divider()
    n_teams = st.slider("Кількість команд", 2, 4, 2)
    t_names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}") for i in range(n_teams)]
    rounds = st.number_input("Раунди", 1, 10, 3)
    sec = st.slider("Секунди на хід", 10, 120, 60)

    if st.button("🔥 ПОЧАТИ ГРУ"):
        st.session_state.team_names = t_names
        st.session_state.scores = {n: 0 for n in t_names}
        st.session_state.total_rounds = rounds
        st.session_state.round_duration = sec
        st.session_state.current_round = 1
        st.session_state.team_idx = 0
        st.session_state.game_started = True
        st.session_state.game_words = st.session_state.all_words.copy()
        random.shuffle(st.session_state.game_words)
        st.rerun()

# --- ЕКРАН 3: ГРА ---
elif st.session_state.game_started:
    team = st.session_state.team_names[st.session_state.team_idx]
    
    if 'active_turn' not in st.session_state or not st.session_state.active_turn:
        st.title(f"Черга: {team}")
        st.write(f"Раунд {st.session_state.current_round} / {st.session_state.total_rounds}")
        if st.button("Я ГОТОВИЙ(-А)! ▶️"):
            st.session_state.active_turn = True
            st.session_state.start_t = time.time()
            st.session_state.cur_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
    else:
        rem = int(st.session_state.round_duration - (time.time() - st.session_state.start_t))
        
        if rem <= 0:
            st.session_state.active_turn = False
            st.session_state.team_idx += 1
            if st.session_state.team_idx >= len(st.session_state.team_names):
                st.session_state.team_idx = 0
                st.session_state.current_round += 1
            
            if st.session_state.current_round > st.session_state.total_rounds:
                st.session_state.game_started = False
                st.session_state.game_over = True
            st.rerun()
        
        st.subheader(f"⏱ {rem} сек | {team}: {st.session_state.scores[team]} ⭐")
        st.markdown(f'<div class="word-box">{st.session_state.cur_word.upper()}</div>', unsafe_allow_html=True)
        
        if st.button("✅ ВГАДАНО"):
            st.session_state.scores[team] += 1
            st.session_state.cur_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        if st.button("❌ СКІП"):
            st.session_state.scores[team] -= 1
            st.session_state.cur_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        time.sleep(0.1)
        st.rerun()

# --- ЕКРАН 4: ФІНАЛ ---
elif st.session_state.game_over:
    st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in st.session_state.scores.items():
        st.write(f"### {n}: {s} балів")
    if st.button("ЗІГРАТИ ЩЕ РАЗ 🔄"):
        st.session_state.game_over = False
        st.session_state.welcome_done = True
        st.rerun()
