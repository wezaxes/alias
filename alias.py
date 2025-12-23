import streamlit as st
import random
import time
import os

# 1. Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# 2. Стилізація
st.markdown("""
    <style>
    .stButton { display: flex; justify-content: center; }
    .stButton>button { 
        width: 100%; max-width: 500px; height: 4.5em; 
        font-size: 24px !important; font-weight: bold; 
        border-radius: 15px; margin-bottom: 10px; text-transform: uppercase;
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
    .mode-selection {
        padding: 30px; 
        border-radius: 20px; 
        /* Змінив фон на світліший сіро-блакитний */
        background: #585b70; 
        /* Змінив рамку на яскраву білу або світло-блакитну */
        border: 3px solid #89b4fa; 
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .mode-selection:hover {
        /* Ефект підсвічування при наведенні */
        background: #7f849c;
        border-color: #fab387;
        transform: scale(1.02);
    }
    .mode-selection h3 {
        color: #f9e2af !important; /* Робимо заголовок золотистим */
        margin-top: 0;
    }
    .mode-selection p {
        color: #cdd6f4 !important; /* Світлий текст опису */
    }
        /* Робимо контейнер відносним, щоб кнопка всередині не вилітала за межі */
    .mode-container { position: relative; }

    /* Ховаємо кнопку, але розтягуємо її на всю площу картки */
    div.stButton > button[key*="overlay_"] {
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important;
        z-index: 10;
        cursor: pointer;
    }
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
    except:
        pass

# Ініціалізація станів
if 'all_words' not in st.session_state:
    st.session_state.all_words = load_words()

if 'msg_data' not in st.session_state:
    st.session_state.msg_data = {"text": None, "type": None}

if 'last_added_word' not in st.session_state:
    st.session_state.last_added_word = ""

if 'game_state' not in st.session_state:
    st.session_state.game_state = "welcome"
    st.session_state.game_mode = None
    st.session_state.players = []
    st.session_state.scores = {}
    st.session_state.current_player_idx = 0
    st.session_state.current_round = 1
    st.session_state.welcome_done = False

# --- ЕКРАН 1: ДИСКЛЕЙМЕР ---
if st.session_state.game_state == "welcome":
    st.markdown("<h2 style='color: #fab387;'>ДИСКЛЕЙМЕР</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="disclaimer-box">
            <h2 style='color: #f38ba8; margin-top: 0;'>УВАГА КОД ПИСАЛА ЖІНКА‼️</h2>
            <p style='font-size: 18px; color: #cdd6f4;'>
                Це <b>СУПЕР пробна версія</b>. Шанс отримати дибільне слово <b>70%</b>.
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("ЛАДНО ✅"):
        st.session_state.game_state = "mode_select"
        st.rerun()
    st.stop()

# --- ЕКРАН 2: ВИБІР РЕЖИМУ ---
elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Створюємо візуальну картку
        st.markdown("""
            <div class="mode-card">
                <h2 style='margin:0;'>🏠</h2>
                <h3 style='color:#f9e2af; margin:10px 0;'>РЕЖИМ IRL</h3>
                <p style='color:#cdd6f4; font-size:14px;'>Командна гра вживу</p>
            </div>
        """, unsafe_allow_html=True)
        # Накладаємо невидиму кнопку зверху
        if st.button("overlay_irl", key="overlay_irl"):
            st.session_state.game_mode = "irl"
            st.session_state.game_state = "setup"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class="mode-card">
                <h2 style='margin:0;'>🎙️</h2>
                <h3 style='color:#f9e2af; margin:10px 0;'>DISCORD</h3>
                <p style='color:#cdd6f4; font-size:14px;'>Кругова гра через демку</p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("overlay_discord", key="overlay_discord"):
            st.session_state.game_mode = "discord"
            st.session_state.game_state = "setup"
            st.rerun()
    st.stop()


# --- ЕКРАН 3: НАЛАШТУВАННЯ ---
elif st.session_state.game_state == "setup":
    st.title("⚙️ Налаштування Alias")
    
    with st.expander("➕ Додати своє дебільне слово"):
        st.info(f"Зараз у словнику слів: {len(st.session_state.all_words)}")
        new_word_raw = st.text_input("Введи слово:", key="input_field")

        if st.button("ДОДАТИ В СЛОВНИК"):
            word = new_word_raw.strip().capitalize()
            low_word = word.lower()
            existing_low = [w.lower() for w in st.session_state.all_words]

            if word == "":
                pass
            elif low_word in existing_low:
                st.session_state.msg_data = {"text": "Таке слово вже є, давай придумаємо щось прикольніше", "type": "error"}
            else:
                st.session_state.all_words.append(word)
                st.session_state.last_added_word = word
                st.session_state.msg_data = {"text": "Вітаю, ви придумали нове прикольне слово, дякую!", "type": "success"}
                append_word_to_file(word)
            st.rerun()

        if st.session_state.msg_data["text"]:
            if st.session_state.msg_data["type"] == "success":
                st.success(st.session_state.msg_data["text"])
            else:
                st.error(st.session_state.msg_data["text"])
        
        if st.session_state.last_added_word:
            st.markdown(f"✅ Останнє додане: **{st.session_state.last_added_word}**")

    st.divider()
    
    g_mode = st.session_state.game_mode
    if g_mode == "irl":
        num = st.slider("Кількість команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}") for i in range(num)]
    else:
        st.write("Введи імена гравців (через кому):")
        names_raw = st.text_area("Імена:", "Катя, Петя, Маша, Саша")
        names = [n.strip() for n in names_raw.replace('\n', ',').split(',') if n.strip()]

    rounds = st.number_input("Кількість раундів", 1, 20, 3)
    timer = st.slider("Секунди на хід", 10, 120, 60)

    if st.button("🔥 ПОЧАТИ ГРУ"):
        if len(names) < 2:
            st.error("Для гри треба хоча б двоє!")
        else:
            st.session_state.players = names
            st.session_state.scores = {n: 0 for n in names}
            st.session_state.total_rounds = rounds
            st.session_state.duration = timer
            st.session_state.game_words = st.session_state.all_words.copy()
            random.shuffle(st.session_state.game_words)
            st.session_state.current_player_idx = 0
            st.session_state.current_round = 1
            st.session_state.game_state = "waiting" if g_mode == "discord" else "playing"
            st.rerun()

# --- ЕКРАН 4: ОЧІКУВАННЯ (DISCORD) ---
elif st.session_state.game_state == "waiting":
    idx = st.session_state.current_player_idx
    explainer = st.session_state.players[idx]
    listener = st.session_state.players[(idx + 1) % len(st.session_state.players)]
    
    st.markdown(f"""
        <div class="waiting-screen">
            <h1 style="margin-bottom:0;">🤫 ТССС, ГОТУЄМОСЬ!</h1>
            <p style="font-size:18px;">Коло {st.session_state.current_round} з {st.session_state.total_rounds}</p>
            <hr style="border: 1px solid #45475a;">
            <h2 style="color: #a6e3a1; margin-bottom:5px;">🎙️ Пояснює: {explainer}</h2>
            <h2 style="color: #89b4fa;">👂 Відгадує: {listener}</h2>
            <div class="warning-text">🙈 {listener.upper()}, ВИЙДИ ЗІ СТРІМУ!</div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("ВІДГАДУВАЧ ПІШОВ — ПОЧИНАЄМО! ▶️"):
        st.session_state.turn_active = True
        st.session_state.start_time = time.time()
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
        st.session_state.game_state = "playing"
        st.rerun()

# --- ЕКРАН 5: ГРА ---
elif st.session_state.game_state == "playing":
    active_name = st.session_state.players[st.session_state.current_player_idx]

    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        st.title(f"Черга: {active_name}")
        if st.button("Я ГОТОВИЙ(-А)! ▶️"):
            st.session_state.turn_active = True
            st.session_state.start_time = time.time()
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        if rem <= 0:
            st.session_state.turn_active = False
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.players):
                st.session_state.current_player_idx = 0
                st.session_state.current_round += 1
            
            if st.session_state.current_round > st.session_state.total_rounds:
                st.session_state.game_state = "finished"
            else:
                st.session_state.game_state = "waiting" if st.session_state.game_mode == "discord" else "playing"
            st.rerun()
        
        st.subheader(f"⏱ {rem} сек | {active_name}: {st.session_state.scores[active_name]} ⭐")
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
        time.sleep(0.1)
        st.rerun()

# --- ЕКРАН 6: ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.title("🏆 ТАБЛИЦЯ РЕЗУЛЬТАТІВ")
    for n, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"### {n}: {s} балів")
    if st.button("В МЕНЮ 🔄"):
        st.session_state.game_state = "mode_select"
        st.session_state.current_player_idx = 0
        st.session_state.current_round = 1
        st.rerun()
