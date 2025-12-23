import streamlit as st
import random
import time
import os

# 1. Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# 2. Стилізація (ОНОВЛЕНО)
st.markdown("""
    <style>
    .stButton { display: flex; justify-content: center; }
    
    /* ПЕРЕТВОРЮЄМО ВСІ КНОПКИ НА КРАСИВІ ПЛИТИ */
    .stButton>button { 
        width: 100%; 
        max-width: 500px; 
        min-height: 4.5em; 
        font-size: 24px !important; 
        font-weight: bold; 
        border-radius: 20px; 
        margin-bottom: 10px; 
        text-transform: uppercase;
        background: #585b70 !important;
        border: 3px solid #89b4fa !important;
        color: #f9e2af !important;
        transition: 0.3s !important;
    }
    
    .stButton>button:hover {
        background: #7f849c !important;
        border-color: #fab387 !important;
        transform: scale(1.02);
    }

    h1, h2, h3, p { text-align: center !important; }
    
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
    
    /* Дизайн плит для вибору режиму (залишаємо як було) */
    .mode-selection {
        padding: 30px; border-radius: 20px; background: #585b70; 
        border: 3px solid #89b4fa; margin-bottom: 20px; transition: 0.3s;
        cursor: pointer; display: block; width: 100%; text-decoration: none !important;
    }
    .mode-selection:hover { background: #7f849c; border-color: #fab387; transform: scale(1.02); }
    .mode-selection h3 { color: #f9e2af !important; margin-top: 0; }
    .mode-selection p { color: #cdd6f4 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. РОБОТА З ФАЙЛОМ ---
def load_words():
    filename = "words.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
            if words: return words
    return ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Wezaxes", "Тілт"]

def append_word_to_file(word):
    try:
        with open("words.txt", "a", encoding="utf-8") as f:
            f.write(word + "\n")
    except: pass

# Ініціалізація станів
if 'all_words' not in st.session_state: st.session_state.all_words = load_words()
if 'msg_data' not in st.session_state: st.session_state.msg_data = {"text": None, "type": None}
if 'game_state' not in st.session_state:
    st.session_state.game_state = "welcome"
    st.session_state.game_mode = None
    st.session_state.players = []
    st.session_state.scores = {}
    st.session_state.current_player_idx = 0
    st.session_state.current_round = 1

# --- ЕКРАН 1: ДИСКЛЕЙМЕР ---
if st.session_state.game_state == "welcome":
    st.markdown("<h2 style='color: #fab387;'>ДИСКЛЕЙМЕР</h2>", unsafe_allow_html=True)
    st.markdown("""<div class="disclaimer-box"><h2 style='color: #f38ba8; margin-top: 0;'>УВАГА КОД ПИСАЛА ЖІНКА‼️</h2>
    <p style='font-size: 18px; color: #cdd6f4;'>Це <b>СУПЕР пробна версія</b>.</p></div>""", unsafe_allow_html=True)
    if st.button("ЛАДНО ✅"):
        st.session_state.game_state = "mode_select"
        st.rerun()
    st.stop()

# --- ЕКРАН 2: ВИБІР РЕЖИМУ ---
elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    params = st.query_params
    if "mode" in params:
        st.session_state.game_mode = params["mode"]
        st.session_state.game_state = "setup"
        st.query_params.clear()
        st.rerun()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<a href="/?mode=irl" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🏠 IRL</h3><p>Вживу</p></div></a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="/?mode=discord" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🎙️ DISCORD</h3><p>Через демку</p></div></a>', unsafe_allow_html=True)
    st.stop()

# --- ЕКРАН 3: НАЛАШТУВАННЯ ---
elif st.session_state.game_state == "setup":
    if st.button("⬅️ НАЗАД"):
        st.session_state.game_state = "mode_select"
        st.rerun()

    st.title("⚙️ Налаштування Alias")
    with st.expander("➕ Додати слово"):
        new_word = st.text_input("Введи слово:")
        if st.button("ДОДАТИ"):
            word = new_word.strip().capitalize()
            if word and word.lower() not in [w.lower() for w in st.session_state.all_words]:
                st.session_state.all_words.append(word)
                append_word_to_file(word)
                st.success("Додано!")
            st.rerun()

    g_mode = st.session_state.game_mode
    if g_mode == "irl":
        num = st.slider("Кількість команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}") for i in range(num)]
    else:
        names_raw = st.text_area("Імена гравців:", "Катя, Петя, Маша, Саша")
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
    if st.button("⬅️ НАЗАД"):
        st.session_state.game_state = "mode_select"; st.rerun()
    idx = st.session_state.current_player_idx
    st.markdown(f'<div class="waiting-screen"><h1>🤫 ТССС!</h1><h2>🎙️ Пояснює: {st.session_state.players[idx]}</h2></div>', unsafe_allow_html=True)
    if st.button("ПОЧАТИ РАУНД ▶️"):
        st.session_state.turn_active, st.session_state.start_time = True, time.time()
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
        st.session_state.game_state = "playing"; st.rerun()

# --- ЕКРАН 5: ГРА ---
elif st.session_state.game_state == "playing":
    if st.button("⬅️ ПЕРЕРВАТИ"):
        st.session_state.game_state = "mode_select"; st.rerun()
    
    active_name = st.session_state.players[st.session_state.current_player_idx]
    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        if st.button(f"Я ГОТОВИЙ(-А) {active_name}! ▶️"):
            st.session_state.turn_active, st.session_state.start_time = True, time.time()
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
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
        c1, c2 = st.columns(2)
        if c1.button("✅ ВГАДАНО"):
            st.session_state.scores[active_name] += 1
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        if c2.button("❌ СКІП"):
            st.session_state.scores[active_name] -= 1
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        time.sleep(0.1); st.rerun()

# --- ЕКРАН 6: ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True): st.write(f"### {n}: {s}")
    if st.button("В МЕНЮ 🔄"):
        st.session_state.game_state = "mode_select"; st.rerun()
