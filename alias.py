import streamlit as st
import random
import time
import os
import json
import string
from google.cloud import firestore
from google.oauth2 import service_account

# 1. Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# 2. Стилізація
st.markdown("""
    <style>
    .stButton { display: flex; justify-content: center; }
    .stButton>button { 
        width: 100%;  height: 4.5em; 
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
    
    /* Дизайн плит */
    .mode-selection {
        padding: 30px; 
        border-radius: 20px; 
        background: #585b70; 
        border: 3px solid #89b4fa; 
        margin-bottom: 20px;
        transition: 0.3s;
        cursor: pointer;
        display: block;
        width: 100%;
        text-decoration: none !important;
    }
    .mode-selection:hover {
        background: #7f849c;
        border-color: #fab387;
        transform: scale(1.02);
    }
    .mode-selection h3 { color: #f9e2af !important; margin-top: 0; }
    .mode-selection p { color: #cdd6f4 !important; }

    /* Стиль для кнопки фідбеку */
    .feedback-btn {
        background-color: #38bdf8 !important;
        border: none !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    div[data-testid="stVerticalBlock"] > div.stElementContainer {
        width: 100%;
        margin-bottom: 10px;
    }
    div.stButton {
        width: 100%;
        display: flex;  
        justify-content: center;
    }
    div.stButton > button {
        width: 100%;
    }     
    </style>
""", unsafe_allow_html=True)

# --- ДОПОМІЖНІ ФУНКЦІЇ ---
def generate_room_code():
    letters = ''.join(random.choices(string.ascii_uppercase, k=4))
    digits = ''.join(random.choices(string.digits, k=2))
    code_list = list(letters + digits)
    random.shuffle(code_list)
    return ''.join(code_list)

@st.cache_resource
def get_db():
    try:
        key_dict = json.loads(st.secrets["textkey"])
        creds = service_account.Credentials.from_service_account_info(key_dict)
        return firestore.Client(credentials=creds)
    except:
        return None

db = get_db()

def load_words():
    filename = "words.txt"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            words = [line.strip() for line in f if line.strip()]
            if words: return words
    return ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Wezaxes", "Тільт"]

def append_word_to_file(word):
    try:
        with open("words.txt", "a", encoding="utf-8") as f:
            f.write(word + "\n")
    except: pass

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

# Сайдбар
with st.sidebar:
    st.markdown("---")
    st.markdown("### 💡 Маєш ідею або щось зламалось?")
    st.link_button("ЗАПРОПОНУВАТИ ФІЧУ/НАЯБІДНІЧАТЬ ✈️", "https://t.me/wezaxes", use_container_width=True)
    st.markdown("---")

# Перевірка параметрів URL
params = st.query_params
if "mode" in params:
    st.session_state.game_mode = params["mode"]
    st.session_state.game_state = "setup"
    st.query_params.clear()
    st.rerun()

# --- ЕКРАНИ ---

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
        st.session_state.game_state = "tutorial"
        st.rerun()

elif st.session_state.game_state == "tutorial":
    st.title("📖 Куди жмать? (методичка)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏠 Режим IRL\n**Для тих, хто в одній кімнаті:**\n* Один телефон на всіх.\n* Передаєте мобілу тому, чия черга.\n* Тиснете **'Я готовий'** і вперед!")
    with col2:
        st.markdown("### 🎙️ DISCORD\n**Для гри на відстані:**\n* Кожен заходить зі свого девайсу.\n* Один створює кімнату (Начальнік), інші вводять код.\n* Система сама каже, хто пояснює.")
    
    st.info("💡 **Головне правило:** Пояснюй як хочеш, але не називай саме слово або спільнокореневі.")
    st.write("➕ У налаштуваннях можна додати свої слова! p.s: при натисканні вас флешне, будьте готові)))")
    if st.button("ЗРОЗУМІВ, ПОГНАЛИ! 🚀"):
        st.session_state.game_state = "mode_select"
        st.rerun()

elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<a href="/?mode=irl" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🏠 IRL</h3><p>Командна гра вживу</p></div></a>', unsafe_allow_html=True)
    with col2:
        st.markdown('<a href="/?mode=discord" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🎙️ DISCORD</h3><p>Грайте разом онлайн</p></div></a>', unsafe_allow_html=True)
    
    st.divider()
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        if st.button("❓ Я ЗАБУВ ЯК РУЛИТЬ", use_container_width=True):
            st.session_state.game_state = "tutorial"; st.rerun()

elif st.session_state.game_state == "setup":
    if st.button("⬅️ НАЗАД"):
        st.session_state.game_state = "mode_select"; st.rerun()
    st.title("⚙️ Налаштування")
    
    # --- ТВОЄ ОРИГІНАЛЬНЕ ДОДАВАННЯ СЛІВ ---
    with st.expander("➕ Додати своє слово"):
        st.info(f"Зараз у словнику слів: {len(st.session_state.all_words)}")
        new_word_raw = st.text_input("Введи слово:", key="input_field")

        if st.button("ДОДАТИ В СЛОВНИК"):
            word = new_word_raw.strip().capitalize()
            low_word = word.lower()
            existing_low = [w.lower() for w in st.session_state.all_words]

            if word != "":
                if low_word in existing_low:
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
    
    # --- ЛОГІКА DISCORD (Оновлена з генератором та валідацією коду) ---
    if st.session_state.game_mode == "discord":
        my_name = st.text_input("Твій нікнейм:")
        
        c_h, c_j = st.columns(2)
        with c_h:
            st.write("Ти хост?")
            if st.button("СТВОРИТИ КІМНАТУ ✨"):
                if my_name:
                    r_id = generate_room_code()
                    st.session_state.room_id = r_id
                    st.session_state.my_name = my_name
                    if db:
                        db.collection("rooms").document(r_id).set({
                            "host": my_name, "players": [my_name], "scores": {my_name: 0},
                            "state": "lobby", "total_rounds": 3, "duration": 60, "current_round": 1,
                            "explainer": "", "listener": "", "word": ""
                        })
                        st.session_state.game_state = "sync_lobby"; st.rerun()
                else: st.error("Введи нікнейм!")

        with c_j:
            st.write("Маєш код?")
            enter_code = st.text_input("Введи код:", key="join_input").upper().strip()
            if st.button("УВІЙТИ 🚪"):
                if not my_name or not enter_code:
                    st.error("Введи дані!")
                else:
                    if db:
                        ref = db.collection("rooms").document(enter_code)
                        doc = ref.get()
                        if doc.exists:
                            data = doc.to_dict()
                            st.session_state.room_id = enter_code
                            st.session_state.my_name = my_name
                            if my_name not in data["players"]:
                                data["players"].append(my_name)
                                data["scores"][my_name] = 0
                                ref.update({"players": data["players"], "scores": data["scores"]})
                            st.session_state.game_state = "sync_lobby"; st.rerun()
                        else:
                            st.error("❌ Кімнату з таким кодом не знайдено!")

    # --- ЛОГІКА IRL ---
    elif st.session_state.game_mode == "irl":
        num = st.slider("Кількість команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}") for i in range(num)]
        rounds = st.number_input("Кількість раундів", 1, 20, 3)
        timer = st.slider("Секунди на хід", 10, 120, 60)
        
        if st.button("🔥 ПОЧАТИ ГРУ"):
            if len(names) < 2: st.error("Для гри треба хоча б двоє!")
            else:
                st.session_state.players = names; st.session_state.scores = {n: 0 for n in names}
                st.session_state.total_rounds = rounds; st.session_state.duration = timer
                st.session_state.current_player_idx = 0; st.session_state.current_round = 1
                st.session_state.game_state = "playing_irl"; st.rerun()

# --- СИНХРОНІЗОВАНЕ ЛОББІ (DISCORD) ---
elif st.session_state.game_state == "sync_lobby":
    st.title(f"🏠 Кімната: {st.session_state.room_id}")
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()
    if not doc.exists:
        st.error("Кімнату не знайдено!"); st.session_state.game_state = "setup"; st.rerun()
    
    data = doc.to_dict()
    if data.get("state") == "playing":
        st.session_state.game_state = "playing_sync"; st.rerun()

    st.write("### Гравці в лобі:")
    cols = st.columns(3)
    for i, p in enumerate(data["players"]):
        cols[i % 3].button(f"👤 {p}", disabled=True, key=f"p_{i}")
    
    st.divider()
    is_host = (data.get("host") == st.session_state.my_name)
    
    if is_host:
        st.subheader("👑 Ви Хост (Адмін)")
        h_rounds = st.number_input("Кількість раундів", 1, 20, data.get("total_rounds", 3))
        h_timer = st.slider("Секунди на хід", 10, 120, data.get("duration", 60))
        if h_rounds != data.get("total_rounds") or h_timer != data.get("duration"):
            ref.update({"total_rounds": h_rounds, "duration": h_timer})
        
        if st.button("ПОЧАТИ ГРУ ДЛЯ ВСІХ 🔥"):
            ref.update({"state": "playing", "current_round": 1, "explainer": "", "listener": ""})
            st.rerun()
    else:
        st.warning("🕒 Очікуємо, поки хост розбереться в кнопках...")
        st.info(f"📊 Раундів: {data.get('total_rounds', 3)} | ⏱ Час: {data.get('duration', 60)}с")

    if st.button("🚪 ПОКИНУТИ КІМНАТУ"):
        st.session_state.game_state = "setup"; st.rerun()
    
    time.sleep(2); st.rerun()

# --- ГРА (DISCORD SYNC) ---
elif st.session_state.game_state == "playing_sync":
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()
    if not doc.exists:
        st.session_state.game_state = "mode_select"; st.rerun()
    
    data = doc.to_dict()
    my_name = st.session_state.my_name

    with st.sidebar:
        st.write(f"👤 Ти: **{my_name}**")
        st.write(f"🏠 Кімната: **{st.session_state.room_id}**")
        st.divider()
        st.write("👥 **Гравці в мережі:**")
        for p in data.get("players", []):
            st.caption(f"• {p} {'(ти)' if p == my_name else ''}")
        if st.button("🔴 ВИЙТИ"):
            st.session_state.game_state = "setup"; st.rerun()

    total_rounds = data.get("total_rounds", 3)
    if data.get("current_round", 1) > total_rounds:
        st.session_state.scores = data["scores"]; st.session_state.game_state = "finished"; st.rerun()

    if not data.get("explainer"):
        st.title(f"Раунд {data.get('current_round', 1)} з {total_rounds}")
        quotes = [
            "💡 Порада: якщо не знаєш як пояснити — махай руками!",
            "💅 Факт: цей код писала жінка, тому він такий гарний.",
            "⏳ Очікуємо... Тим часом придумай, як пояснити слово 'Бебра'.",
            "🚀 Шанс випадіння тупого слова сьогодні — 99%.",
            "🎮 Ви вже намагались написати сюди слово хуй?"
        ]
        st.info(random.choice(quotes)) 
        if st.button("ЗГЕНЕРУВАТИ ПАРУ 🎲"):
            players = data["players"]
            if len(players) >= 2:
                p1, p2 = random.sample(players, 2)
                ref.update({
                    "explainer": p1, "listener": p2, 
                    "word": random.choice(st.session_state.all_words), 
                    "t_end": time.time() + data.get("duration", 60)
                })
                st.rerun()
    else:
        rem = int(data["t_end"] - time.time())
        if rem <= 0:
            st.warning("Час вийшов!")
            if st.button("Наступна пара"):
                ref.update({"explainer": "", "listener": "", "word": "", "current_round": data.get("current_round", 1) + 1})
                st.rerun()
        else:
            st.subheader(f"⏱ {rem} сек | {data['explainer']} ➜ {data['listener']}")
            if my_name == data["explainer"]:
                st.success("ТИ ПОЯСНЮЄШ!")
                st.markdown(f'<div class="word-box">{data["word"].upper()}</div>', unsafe_allow_html=True)
                c1, c2 = st.columns(2)
                if c1.button("✅ ВГАДАНО"):
                    data["scores"][my_name] = data["scores"].get(my_name, 0) + 1
                    ref.update({"scores": data["scores"], "word": random.choice(st.session_state.all_words)})
                    st.rerun()
                if c2.button("❌ СКІП"):
                    ref.update({"word": random.choice(st.session_state.all_words)}); st.rerun()
            elif my_name == data["listener"]:
                st.warning("ТИ ВІДГАДУЄШ!"); st.markdown('<div class="word-box">???</div>', unsafe_allow_html=True)
            else: st.info(f"Грають {data['explainer']} та {data['listener']}")
        time.sleep(1); st.rerun()

# --- IRL РЕЖИМ ---
elif st.session_state.game_state == "playing_irl":
    active = st.session_state.players[st.session_state.current_player_idx]
    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        st.title(f"Раунд {st.session_state.current_round} з {st.session_state.total_rounds}")
        st.subheader(f"Черга: {active}")
        if st.button("Я ГОТОВИЙ! ▶️"):
            st.session_state.turn_active = True
            st.session_state.start_time = time.time()
            st.session_state.current_word = random.choice(st.session_state.all_words); st.rerun()
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        if rem <= 0:
            st.session_state.turn_active = False
            st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(st.session_state.players)
            if st.session_state.current_player_idx == 0: st.session_state.current_round += 1
            st.rerun()
        st.subheader(f"⏱ {rem} сек | {active}")
        st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ ВГАДАНО"):
            st.session_state.scores[active] += 1; st.session_state.current_word = random.choice(st.session_state.all_words); st.rerun()
        if c2.button("❌ СКІП"):
            st.session_state.current_word = random.choice(st.session_state.all_words); st.rerun()
        time.sleep(0.1); st.rerun()

# --- ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.balloons(); st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"### {n}: {s} балів")
    if st.button("В ГОЛОВНЕ МЕНЮ 🔄"):
        st.session_state.game_state = "mode_select"; st.rerun()
