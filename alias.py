import streamlit as st
import random
import time
import os

# 1. Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# 2. Стилізація
st.markdown("""
    <style>
    h1, h2, h3, p { text-align: center !important; }
    
    /* Твій фірмовий дизайн плити-кнопки */
    .custom-btn {
        padding: 20px; 
        border-radius: 20px; 
        background: #585b70; 
        border: 3px solid #89b4fa; 
        margin-bottom: 15px;
        transition: 0.3s;
        cursor: pointer;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-decoration: none !important;
        width: 100%;
        min-height: 100px;
    }
    .custom-btn:hover {
        background: #7f849c;
        border-color: #fab387;
        transform: scale(1.02);
    }
    .custom-btn h3 { color: #f9e2af !important; margin: 0 !important; text-transform: uppercase; font-size: 22px; }
    .custom-btn p { color: #cdd6f4 !important; margin: 5px 0 0 0 !important; font-size: 14px; }

    /* Червона плита для СКІПУ або ПЕРЕРВАТИ */
    .btn-danger { border-color: #f38ba8 !important; }
    .btn-danger h3 { color: #f38ba8 !important; }

    /* Зелена плита для ВГАДАНО або ПОЧАТИ */
    .btn-success { border-color: #a6e3a1 !important; }
    .btn-success h3 { color: #a6e3a1 !important; }

    .word-box { 
        font-size: 42px; text-align: center; font-weight: bold; 
        color: #f9e2af; background-color: #313244; padding: 50px; 
        border-radius: 20px; border: 3px solid #89b4fa; margin: 20px 0; 
    }
    .disclaimer-box {
        text-align: center; background-color: #45475a; 
        padding: 25px; border-radius: 15px; border: 2px solid #f38ba8;
    }
    .waiting-screen {
        background-color: #1e1e2e; padding: 50px; border-radius: 25px;
        border: 3px dashed #fab387; color: #fab387; text-align: center;
    }
    .warning-text {
        color: #f38ba8; font-weight: bold; font-size: 28px; 
        border: 2px solid #f38ba8; padding: 10px; border-radius: 10px;
        margin-top: 20px; text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# Логіка обробки кліків через URL
params = st.query_params
if "action" in params:
    action = params["action"]
    if action == "go_to_modes": st.session_state.game_state = "mode_select"
    elif action == "start_setup": st.session_state.game_state = "setup"
    elif action == "start_turn":
        st.session_state.turn_active = True
        st.session_state.start_time = time.time()
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
    elif action == "correct":
        st.session_state.scores[st.session_state.players[st.session_state.current_player_idx]] += 1
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
    elif action == "skip":
        st.session_state.scores[st.session_state.players[st.session_state.current_player_idx]] -= 1
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
    
    st.query_params.clear()
    st.rerun()

# Функції (без змін)
def load_words():
    if os.path.exists("words.txt"):
        with open("words.txt", "r", encoding="utf-8") as f:
            w = [line.strip() for line in f if line.strip()]
            if w: return w
    return ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Wezaxes", "Тілт"]

def append_word_to_file(word):
    with open("words.txt", "a", encoding="utf-8") as f: f.write(word + "\n")

if 'all_words' not in st.session_state: st.session_state.all_words = load_words()
if 'msg_data' not in st.session_state: st.session_state.msg_data = {"text": None, "type": None}
if 'game_state' not in st.session_state: st.session_state.game_state = "welcome"

# --- ЕКРАН 1: ДИСКЛЕЙМЕР ---
if st.session_state.game_state == "welcome":
    st.markdown("<h2 style='color: #fab387;'>ДИСКЛЕЙМЕР</h2>", unsafe_allow_html=True)
    st.markdown("""<div class="disclaimer-box"><h2 style='color: #f38ba8; margin-top: 0;'>УВАГА КОД ПИСАЛА ЖІНКА‼️</h2>
    <p style='font-size: 18px; color: #cdd6f4;'>Це <b>СУПЕР пробна версія</b>.</p></div>""", unsafe_allow_html=True)
    st.markdown('<a href="/?action=go_to_modes" target="_self" class="custom-btn btn-success"><h3>ЛАДНО ✅</h3></a>', unsafe_allow_html=True)
    st.stop()

# --- ЕКРАН 2: ВИБІР РЕЖИМУ ---
elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<a href="/?mode=irl" target="_self" class="custom-btn"><h3>🏠 IRL</h3><p>Вживу</p></a>', unsafe_allow_html=True)
        if st.query_params.get("mode") == "irl":
            st.session_state.game_mode = "irl"; st.session_state.game_state = "setup"; st.query_params.clear(); st.rerun()
    with col2:
        st.markdown('<a href="/?mode=discord" target="_self" class="custom-btn"><h3>🎙️ DISCORD</h3><p>Через демку</p></a>', unsafe_allow_html=True)
        if st.query_params.get("mode") == "discord":
            st.session_state.game_mode = "discord"; st.session_state.game_state = "setup"; st.query_params.clear(); st.rerun()
    st.stop()

# --- ЕКРАН 3: НАЛАШТУВАННЯ ---
elif st.session_state.game_state == "setup":
    st.markdown('<a href="/?action=go_to_modes" target="_self" class="custom-btn btn-danger" style="min-height: 60px;"><h3>⬅️ НАЗАД</h3></a>', unsafe_allow_html=True)
    st.title("⚙️ Налаштування")
    
    with st.expander("➕ Додати слово"):
        new_word = st.text_input("Введи слово:")
        if st.button("ДОДАТИ"):
            word = new_word.strip().capitalize()
            if word and word.lower() not in [w.lower() for w in st.session_state.all_words]:
                st.session_state.all_words.append(word)
                append_word_to_file(word)
                st.success("Додано!")
    
    g_mode = st.session_state.game_mode
    if g_mode == "irl":
        num = st.slider("Кількість команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}") for i in range(num)]
    else:
        names_raw = st.text_area("Імена гравців (через кому):", "Катя, Петя, Маша, Саша")
        names = [n.strip() for n in names_raw.replace('\n', ',').split(',') if n.strip()]

    rounds = st.number_input("Кількість раундів", 1, 20, 3)
    timer = st.slider("Секунди на хід", 10, 120, 60)

    if st.button("🔥 ПОЧАТИ ГРУ"):
        if len(names) >= 2:
            st.session_state.players, st.session_state.scores = names, {n: 0 for n in names}
            st.session_state.total_rounds, st.session_state.duration = rounds, timer
            st.session_state.game_words = st.session_state.all_words.copy()
            random.shuffle(st.session_state.game_words)
            st.session_state.current_player_idx, st.session_state.current_round = 0, 1
            st.session_state.game_state = "waiting" if g_mode == "discord" else "playing"
            st.rerun()

# --- ЕКРАН 4: ОЧІКУВАННЯ ---
elif st.session_state.game_state == "waiting":
    st.markdown('<a href="/?action=go_to_modes" target="_self" class="custom-btn btn-danger" style="min-height: 60px;"><h3>⬅️ НАЗАД</h3></a>', unsafe_allow_html=True)
    idx = st.session_state.current_player_idx
    st.markdown(f'<div class="waiting-screen"><h1>🤫 ТССС!</h1><h2>🎙️ Пояснює: {st.session_state.players[idx]}</h2></div>', unsafe_allow_html=True)
    st.markdown('<a href="/?action=start_turn" target="_self" class="custom-btn btn-success"><h3>ПОЧАТИ РАУНД ▶️</h3></a>', unsafe_allow_html=True)

# --- ЕКРАН 5: ГРА ---
elif st.session_state.game_state == "playing":
    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        st.markdown(f"<h2>Черга: {st.session_state.players[st.session_state.current_player_idx]}</h2>")
        st.markdown('<a href="/?action=start_turn" target="_self" class="custom-btn btn-success"><h3>Я ГОТОВИЙ(-А)! ▶️</h3></a>', unsafe_allow_html=True)
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        if rem <= 0:
            st.session_state.turn_active = False
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.players):
                st.session_state.current_player_idx = 0; st.session_state.current_round += 1
            st.session_state.game_state = "finished" if st.session_state.current_round > st.session_state.total_rounds else "waiting"
            st.rerun()
        
        st.markdown(f"### ⏱ {rem} сек")
        st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1: st.markdown('<a href="/?action=correct" target="_self" class="custom-btn btn-success"><h3>✅ ВГАДАНО</h3></a>', unsafe_allow_html=True)
        with col2: st.markdown('<a href="/?action=skip" target="_self" class="custom-btn btn-danger"><h3>❌ СКІП</h3></a>', unsafe_allow_html=True)
        time.sleep(0.5); st.rerun()

# --- ЕКРАН 6: ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True): st.write(f"### {n}: {s}")
    st.markdown('<a href="/?action=go_to_modes" target="_self" class="custom-btn"><h3>В МЕНЮ 🔄</h3></a>', unsafe_allow_html=True)
