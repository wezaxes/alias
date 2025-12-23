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
    .mode-selection {
        padding: 20px; border-radius: 15px; background: #45475a; border: 2px solid #89b4fa; margin-bottom: 20px;
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
    st.session_state.game_mode = None # 'irl' або 'discord'
    st.session_state.teams = {}
    st.session_state.team_names = []
    st.session_state.current_team_idx = 0
    st.session_state.current_round = 1
    st.session_state.welcome_done = False

# --- ЕКРАН 1: ДИСКЛЕЙМЕР ---
if not st.session_state.welcome_done:
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
        st.session_state.welcome_done = True
        st.session_state.game_state = "mode_select"
        st.rerun()
    st.stop()

# --- ЕКРАН 2: ВИБІР РЕЖИМУ ---
if st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='mode-selection'><h3>🏠 IRL (Вживу)</h3><p>Передавайте телефон один одному по колу</p></div>", unsafe_allow_html=True)
        if st.button("РЕЖИМ IRL"):
            st.session_state.game_mode = "irl"
            st.session_state.game_state = "setup"
            st.rerun()
            
    with col2:
        st.markdown("<div class='mode-selection'><h3>🎙️ DISCORD</h3><p>Для гри через демку з рандомними парами</p></div>", unsafe_allow_html=True)
        if st.button("РЕЖИМ DISCORD"):
            st.session_state.game_mode = "discord"
            st.session_state.game_state = "setup"
            st.rerun()
    st.stop()

# --- ЕКРАН 3: НАЛАШТУВАННЯ ---
if st.session_state.game_state == "setup":
    st.title(f"⚙️ Налаштування ({st.session_state.game_mode.upper()})")
    
    with st.expander("➕ Додати своє дебільне слово"):
        st.info(f"Зараз у словнику слів: {len(st.session_state.all_words)}")
        new_word_raw = st.text_input("Введи слово:", key="input_field")

        if st.button("ДОДАТИ В СЛОВНИК"):
            word = new_word_raw.strip().capitalize()
            low_word = word.lower()
            existing_low = [w.lower() for w in st.session_state.all_words]

            if word:
                if low_word in existing_low:
                    st.session_state.msg_data = {"text": "Таке слово вже є!", "type": "error"}
                else:
                    st.session_state.all_words.append(word)
                    st.session_state.last_added_word = word
                    append_word_to_file(word)
                    st.session_state.msg_data = {"text": "Вітаємо у словнику! ✅", "type": "success"}
                st.rerun()

        if st.session_state.msg_data["text"]:
            st.success(st.session_state.msg_data["text"]) if st.session_state.msg_data["type"] == "success" else st.error(st.session_state.msg_data["text"])

    st.divider()
    
    if st.session_state.game_mode == "irl":
        num_teams = st.slider("Скільки команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"name_{i}") for i in range(num_teams)]
    else:
        names_input = st.text_area("Введіть імена всіх гравців через кому:", placeholder="Олег, Маша, Андрій...")
        names = [n.strip() for n in names_input.replace('\n', ',').split(',') if n.strip()]

    rounds = st.number_input("Кількість раундів", 1, 15, 3)
    timer = st.slider("Секунди на хід", 10, 120, 60)

    if st.button("🔥 ПОЧАТИ ГРУ"):
        if len(names) < 2:
            st.error("Потрібно хоча б 2 гравці/команди!")
        else:
            st.session_state.team_names = names
            st.session_state.teams = {n: 0 for n in names}
            st.session_state.total_rounds = rounds
            st.session_state.duration = timer
            st.session_state.game_words = st.session_state.all_words.copy()
            random.shuffle(st.session_state.game_words)
            st.session_state.game_state = "waiting" if st.session_state.game_mode == "discord" else "playing"
            st.session_state.msg_data = {"text": None, "type": None}
            st.rerun()

# --- ЕКРАН 4: ГРА ---
elif st.session_state.game_state == "waiting":
    # Тільки для Discord: вибір пари та екран очікування
    st.session_state.explainer = random.choice(st.session_state.team_names)
    st.session_state.listener = random.choice([p for p in st.session_state.team_names if p != st.session_state.explainer])
    
    st.markdown(f"""
        <div class="waiting-screen">
            <h1>🤫 ТССС, ЧЕКАЄМО...</h1>
            <p>Ведучий готує наступний раунд</p>
            <hr style="border: 1px solid #45475a;">
            <h2 style="color: #a6e3a1;">🎙️ Пояснює: {st.session_state.explainer}</h2>
            <h2 style="color: #89b4fa;">👂 Відгадує: {st.session_state.listener}</h2>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button(f"Я ГОТОВИЙ, ПОКАЗУЙ СЛОВО! ▶️"):
        st.session_state.game_state = "playing"
        st.session_state.turn_active = True
        st.session_state.start_time = time.time()
        st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
        st.rerun()

elif st.session_state.game_state == "playing":
    # Визначаємо хто ходить
    if st.session_state.game_mode == "irl":
        team = st.session_state.team_names[st.session_state.current_team_idx]
    else:
        team = st.session_state.explainer

    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        st.title(f"Черга: {team}")
        st.write(f"Раунд: {st.session_state.current_round} / {st.session_state.total_rounds}")
        if st.button("Я ГОТОВИЙ(-А)! ▶️"):
            st.session_state.turn_active = True
            st.session_state.start_time = time.time()
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        
        if rem <= 0:
            st.session_state.turn_active = False
            if st.session_state.game_mode == "irl":
                st.session_state.current_team_idx += 1
                if st.session_state.current_team_idx >= len(st.session_state.team_names):
                    st.session_state.current_team_idx = 0
                    st.session_state.current_round += 1
                st.session_state.game_state = "playing"
            else:
                st.session_state.current_round += 1
                st.session_state.game_state = "waiting"

            if st.session_state.current_round > st.session_state.total_rounds:
                st.session_state.game_state = "finished"
            st.rerun()
        
        st.subheader(f"⏱ {rem} сек | {team}: {st.session_state.teams[team]} ⭐")
        st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ ВГАДАНО"):
            st.session_state.teams[team] += 1
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        if c2.button("❌ СКІП"):
            st.session_state.teams[team] -= 1
            st.session_state.current_word = st.session_state.game_words.pop(0) if st.session_state.game_words else "КІНЕЦЬ"
            st.rerun()
        time.sleep(0.1)
        st.rerun()

# --- ЕКРАН 5: ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in sorted(st.session_state.teams.items(), key=lambda x: x[1], reverse=True):
        st.write(f"### {n}: {s} балів")
    
    if st.button("ЗІГРАТИ ЩЕ РАЗ 🔄"):
        st.session_state.game_state = "mode_select"
        st.session_state.current_team_idx = 0
        st.session_state.current_round = 1
        st.session_state.last_added_word = ""
        st.rerun()
