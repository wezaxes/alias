import streamlit as st
import random
import time
import os
import json
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
    
    /* Твій дизайн плит */
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
    </style>
""", unsafe_allow_html=True)
# Отдельный код по кнпки
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
# --- 3. БАЗА ДАНИХ ТА ФАЙЛИ ---
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
        st.session_state.game_state = "mode_select"
        st.rerun()

elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <a href="/?mode=irl" target="_self" style="text-decoration: none;">
                <div class="mode-selection">
                    <h3>🏠 IRL</h3>
                    <p>Командна гра вживу</p>
                </div>
            </a>
        """, unsafe_allow_html=True)
            
    with col2:
        st.markdown(f"""
            <a href="/?mode=discord" target="_self" style="text-decoration: none;">
                <div class="mode-selection">
                    <h3>🎙️ DISCORD</h3>
                    <p>Грайте разом онлайн</p>
                </div>
            </a>
        """, unsafe_allow_html=True)

elif st.session_state.game_state == "setup":
    if st.button("⬅️ НАЗАД"):
        st.session_state.game_state = "mode_select"
        st.rerun()
    
    st.title("⚙️ Налаштування")
    
    # --- ДОДАВАННЯ СЛІВ ---
    with st.expander("➕ Додати своє дебільне слово"):
        st.info(f"Зараз у словнику слів: {len(st.session_state.all_words)}")
        new_word_raw = st.text_input("Введи слово:", key="input_field")

        if st.button("ДОДАТИ В СЛОВНИК"):
            word = new_word_raw.strip().capitalize()
            low_word = word.lower()
            existing_low = [w.lower() for w in st.session_state.all_words]

            if word != "":
                if low_word in existing_low:
                    st.session_state.msg_data = {"text": "Таке слово вже є!", "type": "error"}
                else:
                    st.session_state.all_words.append(word)
                    st.session_state.last_added_word = word
                    st.session_state.msg_data = {"text": "Додано успішно!", "type": "success"}
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
    
    # --- ЛОГІКА DISCORD ---
    if st.session_state.game_mode == "discord":
        room_id = st.text_input("Код кімнати (наприклад: 7777):", value=" ").upper()
        my_name = st.text_input("Твій нікнейм:")
        
        if st.button("ВХІД У КІМНАТУ 🔥"):
            if not room_id or not my_name:
                st.error("Введи код і нік!")
            else:
                st.session_state.room_id = room_id
                st.session_state.my_name = my_name
                if db:
                    ref = db.collection("rooms").document(room_id)
                    doc = ref.get()
                    
                    # Якщо кімнати немає або завершена — створюємо (ЯК ХОСТ)
                    if not doc.exists or doc.to_dict().get("state") == "finished":
                        ref.set({
                            "host": my_name,
                            "players": [my_name],
                            "scores": {my_name: 0},
                            "state": "lobby",
                            "total_rounds": 3,
                            "duration": 60,
                            "current_round": 1,
                            "explainer": "", "listener": "", "word": ""
                        })
                    else:
                        # Заходимо як звичайний гравець
                        data = doc.to_dict()
                        if my_name not in data["players"]:
                            data["players"].append(my_name)
                            data["scores"][my_name] = 0
                            ref.update({"players": data["players"], "scores": data["scores"]})
                    
                    st.session_state.game_state = "sync_lobby"
                    st.rerun()

    # --- ЛОГІКА IRL (залишаємо як було) ---
    elif st.session_state.game_mode == "irl":
        num = st.slider("Кількість команд?", 2, 4, 2)
        names = [st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}") for i in range(num)]
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
                st.session_state.current_player_idx = 0
                st.session_state.current_round = 1
                st.session_state.game_state = "playing_irl"
                st.rerun()

# --- СИНХРОНІЗОВАНЕ ЛОББІ (DISCORD) ---
elif st.session_state.game_state == "sync_lobby":
    st.title(f"🏠 Кімната: {st.session_state.room_id}")
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()
    
    if not doc.exists:
        st.error("Кімнату не знайдено!")
        st.session_state.game_state = "setup"; st.rerun()
        
    data = doc.to_dict()
    
    # Якщо гра вже запущена хостом — перекидаємо всіх у гру
    if data.get("state") == "playing":
        st.session_state.game_state = "playing_sync"
        st.rerun()

    st.write("### Гравці в лобі:")
    # Малюємо список гравців кнопками (просто для краси)
    cols = st.columns(3)
    for i, p in enumerate(data["players"]):
        cols[i % 3].button(f"👤 {p}", disabled=True, key=f"p_{i}")
    
    st.divider()
    
    # ПЕРЕВІРКА НА ХОСТА
    is_host = (data.get("host") == st.session_state.my_name)
    
    if is_host:
        st.subheader("👑 Ви Хост (Адмін)")
        st.write("Тільки ви бачите ці налаштування:")
        
        # Хост виставляє параметри, які запишуться в базу для ВСІХ
        h_rounds = st.number_input("Кількість раундів", 1, 20, data.get("total_rounds", 3))
        h_timer = st.slider("Секунди на хід", 10, 120, data.get("duration", 60))
        
        if st.button("ПОЧАТИ ГРУ ДЛЯ ВСІХ 🔥"):
            ref.update({
                "state": "playing",
                "total_rounds": h_rounds,
                "duration": h_timer,
                "current_round": 1,
                "explainer": "", # Очищуємо старі пари
                "listener": ""
            })
            st.rerun()
    else:
        st.warning("🕒 Очікуємо, поки хост запустить гру...")
        
        # Витягуємо актуальні дані з бази, які міг змінити хост
        current_r = data.get('total_rounds', 3)
        current_t = data.get('duration', 60)
        
        st.markdown(f"""
            <div style="background-color: #313244; padding: 20px; border-radius: 15px; border: 1px solid #fab387;">
                <p style="margin: 0; color: #cdd6f4;">Налаштування від хоста:</p>
                <h3 style="margin: 10px 0; color: #fab387;">📊 Раундів: {current_r} | ⏱ Час: {current_t}с</h3>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🚪 ПОКИНУТИ КІМНАТУ"):
        # Можна додати логіку видалення гравця зі списку, але поки просто вихід
        st.session_state.game_state = "setup"
        st.rerun()
    
    # Автооновлення лобі кожні 2 секунди
    time.sleep(2)
    st.rerun()

# --- ГРА (DISCORD SYNC) ---
elif st.session_state.game_state == "playing_sync":
    # --- БІЧНА ПАНЕЛЬ ДЛЯ ВИХОДУ ---
    with st.sidebar:
        st.write(f"👤 Гравець: **{st.session_state.my_name}**")
        st.write(f"🏠 Кімната: **{st.session_state.room_id}**")
        st.divider()
        if st.button("🔴 ВИЙТИ ДО НАЛАШТУВАНЬ"):
            st.session_state.game_state = "setup"
            st.session_state.game_mode = "discord"
            st.rerun()

    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()
    
    if not doc.exists:
        st.error("Кімнату втрачено!")
        st.session_state.game_state = "mode_select"
        st.rerun()
    
    data = doc.to_dict()
    my_name = st.session_state.my_name

    total_rounds = data.get("total_rounds", st.session_state.get("total_rounds", 3))
    turn_duration = data.get("duration", st.session_state.get("duration", 60))

    if data.get("current_round", 1) > total_rounds:
        st.session_state.scores = data["scores"]
        st.session_state.game_state = "finished"
        st.rerun()

    if not data.get("explainer"):
        st.title(f"Раунд {data.get('current_round', 1)} з {total_rounds}")
        quotes = [
            "💡 Порада: якщо не знаєш як пояснити — махай руками!",
            "💅 Факт: цей код писала жінка, тому він такий гарний.",
            "⏳ Очікуємо... Тим часом придумай, як пояснити слово 'Бебра'.",
            "🚀 Шанс випадіння тупого слова сьогодні — 99%.",
            "🦖 Обережно: занадто довге думання викликає тільт у тіммейтів.",
            "🎮 Wezaxes Edition: грай, поки не згорить монітор."
        ]
        st.info(random.choice(quotes)) 
        
        if st.button("ЗГЕНЕРУВАТИ ПАРУ 🎲"):
            players = data["players"]
            if len(players) < 2:
                st.error("Треба мінімум 2 гравці!")
            else:
                # ЛОГІКА РОТАЦІЇ (БЕЗПЕЧНА)
                last_explainer = data.get("explainer", "")
                
                # Якщо гравців рівно 2
                if len(players) == 2:
                    # Перевіряємо, чи останній пояснювач все ще в кімнаті
                    if last_explainer in players:
                        p1 = [p for p in players if p != last_explainer][0]
                        p2 = [p for p in players if p == last_explainer][0]
                    else:
                        # Якщо хтось вийшов/зайшов новий — просто рандом
                        p1, p2 = random.sample(players, 2)
                else:
                    # Якщо більше двох гравців — завжди рандом
                    p1, p2 = random.sample(players, 2)
                
                ref.update({
                    "explainer": p1, 
                    "listener": p2, 
                    "word": random.choice(st.session_state.all_words), 
                    "t_end": time.time() + turn_duration,
                    "total_rounds": total_rounds,
                    "duration": turn_duration
                })
                st.rerun()
    else:
        rem = int(data["t_end"] - time.time())
        if rem <= 0:
            st.warning("Час вийшов!")
            if st.button("Наступний раунд/пара"):
                new_round = data.get("current_round", 1) + 1
                ref.update({"explainer": "", "listener": "", "word": "", "current_round": new_round})
                st.rerun()
        else:
            st.subheader(f"⏱ {rem} сек | {data['explainer']} ➜ {data['listener']}")
            if my_name == data["explainer"]:
                st.success("ТИ ПОЯСНЮЄШ!")
                word_to_show = data["word"].upper()
                diff_emoji = "🔴" if len(word_to_show) > 8 else "🟢"
                st.markdown(f'<div class="word-box">{diff_emoji} {word_to_show}</div>', unsafe_allow_html=True)
                
                c1, c2 = st.columns(2)
                if c1.button("✅ ВГАДАНО"):
                    data["scores"][my_name] = data["scores"].get(my_name, 0) + 1
                    ref.update({"scores": data["scores"], "word": random.choice(st.session_state.all_words)})
                    st.rerun()
                if c2.button("❌ СКІП"):
                    ref.update({"word": random.choice(st.session_state.all_words)})
                    st.rerun()
            elif my_name == data["listener"]:
                st.warning("ТИ ВІДГАДУЄШ!")
                st.markdown('<div class="word-box">???</div>', unsafe_allow_html=True)
            else:
                st.info(f"Глядач. Грають {data['explainer']} та {data['listener']}")
        time.sleep(1)
        st.rerun()

# --- СТАРИЙ IRL РЕЖИМ ---
elif st.session_state.game_state == "playing_irl":
    with st.sidebar:
        st.markdown("### 📊 Рахунок команд")
        for player, score in st.session_state.scores.items():
            st.write(f"{player}: **{score}** ⭐")
        st.divider()
        if st.button("🔴 ВИЙТИ ДО НАЛАШТУВАНЬ"):
            st.session_state.game_state = "setup"
            st.session_state.game_mode = "irl"
            st.rerun()

    if st.session_state.current_round > st.session_state.total_rounds:
        st.session_state.game_state = "finished"
        st.rerun()

    active = st.session_state.players[st.session_state.current_player_idx]
    
    if 'turn_active' not in st.session_state or not st.session_state.turn_active:
        st.title(f"Раунд {st.session_state.current_round} з {st.session_state.total_rounds}")
        st.subheader(f"Черга: {active}")
        tips = ["Готуйся, зараз буде щось крінжове... 🤡", "Дивись у вічі тіммейту! 👀"]
        st.warning(random.choice(tips))
        if st.button("Я ГОТОВИЙ! ▶️"):
            st.session_state.turn_active = True
            st.session_state.start_time = time.time()
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        if rem <= 0:
            st.session_state.turn_active = False
            st.session_state.current_player_idx += 1
            if st.session_state.current_player_idx >= len(st.session_state.players):
                st.session_state.current_player_idx = 0
                st.session_state.current_round += 1
            st.rerun()

        st.subheader(f"⏱ {rem} сек | {active}: {st.session_state.scores[active]} ⭐")
        word_to_show = st.session_state.current_word.upper()
        diff_emoji = "🔴" if len(word_to_show) > 8 else "🟢"
        st.markdown(f'<div class="word-box">{diff_emoji} {word_to_show}</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        if c1.button("✅ ВГАДАНО"):
            st.session_state.scores[active] += 1
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
        if c2.button("❌ СКІП"):
            st.session_state.current_word = random.choice(st.session_state.all_words)
            st.rerun()
        time.sleep(0.1)
        st.rerun()

# --- ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.balloons()
    st.title("🏆 ТАБЛИЦЯ РЕЗУЛЬТАТІВ")
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for n, s in sorted_scores:
        st.write(f"### {n}: {s} балів")
    st.divider()
    if st.button("В ГОЛОВНЕ МЕНЮ 🔄"):
        # Очищуємо статус кімнати в базі, щоб наступного разу вона створилася чистою
        if db and hasattr(st.session_state, 'room_id'):
            db.collection("rooms").document(st.session_state.room_id).update({"state": "finished"})
            
        st.session_state.game_state = "mode_select"
        st.session_state.current_player_idx = 0
        st.session_state.current_round = 1
        st.rerun()
