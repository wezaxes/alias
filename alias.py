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
        background: #cdd6f4; /* Світлий фон (якщо хочеш чорні букви) */
        border: 3px solid #89b4fa; 
        margin-bottom: 20px;
        transition: 0.3s;
        cursor: pointer;
        display: block;
        width: 100%;
        text-decoration: none !important;
        color: #000000 !important; /* Чорний колір для всього всередині */
    }

    .mode-selection:hover {
        background: #bac2de; /* Трохи темніший при наведенні */
        border-color: #fab387;
        transform: scale(1.02);
    }

    /* Примусово робимо всі тексти чорними */
    .mode-selection h3, 
    .mode-selection p, 
    .mode-selection span { 
        color: #000000 !important; 
        margin-top: 0; 
        text-decoration: none !important;
    }

    /* Щоб посилання не міняло колір при натисканні */
    a:link, a:visited, a:hover, a:active {
        text-decoration: none !important;
        color: inherit !important;
    }

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
    st.link_button("ЗАПРОПОНУВАТИ ФІЧУ/НАЯБІДНІЧАТЬ ✈️", "https://t.me/aliashihibot", use_container_width=True)
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
    st.write("➕ У налаштуваннях можна додати свої слова! (ми ще не розібралися як вони зберігаються, але обовʼязково пофіксимо). p.s: при натисканні вас флешне, будьте готові)))")
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
    
    st.markdown("### ⚙️ Налаштування")
    
    # 1. Твій нік (тільки для Discord)
    if st.session_state.game_mode == "discord":
        my_name = st.text_input("Твій нікнейм:", placeholder="Введи шось прикольне...", key="setup_name")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='text-align: center; font-weight: bold;'>Ти хостити будеш?</p>", unsafe_allow_html=True)
            st.markdown("<div style='height: 57px;'></div>", unsafe_allow_html=True) 
            if st.button("СТВОРИТИ КІМНАТУ ✨"):
                if my_name:
                    r_id = generate_room_code()
                    st.session_state.room_id = r_id; st.session_state.my_name = my_name
                    if db:
                        db.collection("rooms").document(r_id).set({
                            "host": my_name, "players": [my_name], "scores": {my_name: 0},
                            "state": "lobby", "total_rounds": 3, "duration": 60, "current_round": 1,
                            "explainer": "", "listener": "", "word": ""
                        })
                        st.session_state.game_state = "sync_lobby"; st.rerun()
                else: st.error("Спочатку введи нікнейм!")

        with col2:
            st.markdown("<p style='text-align: center; font-weight: bold;'>Маєш код?</p>", unsafe_allow_html=True)
            enter_code = st.text_input("Введи код:", placeholder="Код тут...", label_visibility="collapsed", key="join_input_sync").upper().strip()
            if st.button("УВІЙТИ 🚪"):
                if my_name and enter_code:
                    if db:
                        ref = db.collection("rooms").document(enter_code)
                        doc = ref.get()
                        if doc.exists:
                            data = doc.to_dict()
                            st.session_state.room_id = enter_code; st.session_state.my_name = my_name
                            if my_name not in data["players"]:
                                data["players"].append(my_name)
                                data["scores"][my_name] = 0
                                ref.update({"players": data["players"], "scores": data["scores"]})
                            st.session_state.game_state = "sync_lobby"; st.rerun()
                        else: st.error("❌ Код невірний!")
                else: st.error("Введи нік та код!")

    # --- ЛОГІКА IRL ---
    elif st.session_state.game_mode == "irl":
        st.subheader("🏠 Налаштування гри вживу")
        num = st.slider("Кількість команд?", 2, 6, 2)
        names = []
        c_names = st.columns(2)
        for i in range(num):
            with c_names[i % 2]:
                name = st.text_input(f"Команда {i+1}", f"Команда {i+1}", key=f"n_{i}")
                names.append(name)
        st.divider()
        col_r, col_t = st.columns(2)
        with col_r:
            rounds = st.number_input("Кількість раундів", 1, 20, 3)
        with col_t:
            timer = st.slider("Секунди на хід", 10, 120, 60)
        st.divider()
        if st.button("🔥 ПОЧАТИ ГРУ"):
            if any(n.strip() == "" for n in names):
                st.error("Всі команди повинні мати назву!")
            else:
                st.session_state.players = names; st.session_state.scores = {n: 0 for n in names}
                st.session_state.total_rounds = rounds; st.session_state.duration = timer
                st.session_state.current_player_idx = 0; st.session_state.current_round = 1
                st.session_state.game_state = "playing_irl"; st.rerun()

    # --- ДОДАВАННЯ СЛІВ ---
    st.divider()
    with st.expander("➕ Додати своє слово"):
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
                    st.session_state.msg_data = {"text": "Слово додано!", "type": "success"}
                    append_word_to_file(word)
                st.rerun()
        if st.session_state.msg_data["text"]:
            if st.session_state.msg_data["type"] == "success": st.success(st.session_state.msg_data["text"])
            else: st.error(st.session_state.msg_data["text"])
        if st.session_state.last_added_word:
            st.markdown(f"✅ Останнє: **{st.session_state.last_added_word}**")

import streamlit as st
import time
import random

# --- 1. ЗАГАЛЬНА ЛОГІКА ТА САЙДБАР (Спільне для Лобі та Гри) ---
if 'room_id' in st.session_state and st.session_state.game_state in ["sync_lobby", "playing_sync"]:
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()

    if doc.exists:
        data = doc.to_dict()
        current_players = data.get("players", [])
        my_name = st.session_state.my_name
        is_host = (data.get("host") == my_name)

        # Сповіщення (тоасти) — працюють всюди
        if "old_players" not in st.session_state:
            st.session_state.old_players = current_players
        for p in current_players:
            if p not in st.session_state.old_players:
                st.toast(f"✨ {p} приєднався до гри!")
        for p in st.session_state.old_players:
            if p not in current_players:
                st.toast(f"🚪 {p} лівнув з катки...")
        st.session_state.old_players = current_players

        # Малюємо сайдбар
        with st.sidebar:
            st.header("🎮 Alias Sync")
            st.write(f"🏠 Код: **{st.session_state.room_id}**")
            st.write(f"👤 Ти: **{my_name}** {'(👑)' if is_host else ''}")
            st.divider()
            st.write("👥 Гравці:")
            for p in current_players:
                p_label = f"• {p}"
                if p == data.get("host"): p_label += " 👑"
                if p == my_name: p_label += " (ти)"
                st.caption(p_label)

            st.divider()
            if st.button("🔴 ВИЙТИ З ГРИ", key="sidebar_exit_btn"):
                updated_players = [p for p in current_players if p != my_name]
                ref.update({"players": updated_players})
                del st.session_state.room_id
                st.session_state.game_state = "mode_select"
                st.rerun()

        # --- 2. ЕКРАН ЛОБІ ОЧІКУВАННЯ ---
        if st.session_state.game_state == "sync_lobby":
            # Якщо хост натиснув старт — миттєво перемикаємось
            if data.get("state") == "playing":
                st.session_state.game_state = "playing_sync"
                st.rerun()

            st.title(f"🏠 Кімната: {st.session_state.room_id}")
            st.write("### Гравці в лобі:")
            cols = st.columns(3)
            for i, p in enumerate(current_players):
                cols[i % 3].button(f"👤 {p}", disabled=True, key=f"lobby_p_{i}")

            st.divider()
            if is_host:
                st.subheader("👑 Налаштування раундів")
                h_rounds = st.number_input("Раундів", 1, 20, value=int(data.get("total_rounds", 3)), key="host_r_input")
                h_timer = st.slider("Час (сек)", 10, 120, value=int(data.get("duration", 60)), key="host_t_input")

                if h_rounds != data.get("total_rounds") or h_timer != data.get("duration"):
                    ref.update({"total_rounds": h_rounds, "duration": h_timer})

                if st.button("ПОЧАТИ ГРУ ДЛЯ ВСІХ 🔥", use_container_width=True):
                    ref.update({"state": "playing", "current_round": 1})
                    st.rerun()
            else:
                st.info("🕒 Чекаємо, поки хост запустить гру...")
                st.write(f"📊 Раундів: **{data.get('total_rounds', 3)}** | ⏱ Час: **{data.get('duration', 60)}с**")

            if st.button("🚪 ПОКИНУТИ КІМНАТУ", key="lobby_exit_bottom"):
                updated_players = [p for p in current_players if p != my_name]
                ref.update({"players": updated_players})
                del st.session_state.room_id
                st.session_state.game_state = "mode_select"
                st.rerun()

            time.sleep(2)
            st.rerun()

        # --- 3. ЕКРАН ПРОЦЕСУ ГРИ ---
        elif st.session_state.game_state == "playing_sync":
            total_rounds = data.get("total_rounds", 3)
            current_round = data.get("current_round", 1)

            print(f"[GAME LOG] Room: {st.session_state.room_id} | Round: {current_round}/{total_rounds}")

            if current_round > total_rounds:
                st.session_state.scores = data.get("scores", {})
                st.session_state.game_state = "finished"
                st.rerun()

            # --- ПІДСТАН 1: Очікування вибору пари ---
            if not data.get("explainer"):
                st.title(f"Раунд {current_round} з {total_rounds}")

                quotes = [
                    "💡 Порада: якщо не знаєш слова - кажи що всі інші безнадійні і теж не знають та скіпай!",
                    "💅 Факт: зі словника колись приберуть слово Імплікація. Чесно.",
                    "⏳ Очікуємо... Тим часом придумай, як пояснити слово 'Бебра'.",
                    "🚀 Шанс випадіння тупого слова сьогодні — 99%.",
                    "🎲 Натисни і дізнайся, що зламається цього разу.",
                    "🚨 Увага: можливий словесний понос.",
                    "🎤 Порада: пояснюй, ніби перед тобою пʼятирічна дитина.",
                    "🚨 Увага: наступне слово може викликати екзистенційну кризу у всієї команди.",
                    "📐 4(x - 5) = 3x - 6", "📐 25x² - 16y²", "📐 |x + 3| = 7",
                    "😁 Ми теж не знаємо що таке Барбадос."
                ]
                st.info(random.choice(quotes))

                if is_host:
                    if st.button("ПОЧАТИ ХІД 🎲", use_container_width=True):
                        if len(current_players) >= 2:
                            p1, p2 = random.sample(current_players, 2)
                            ref.update({
                                "explainer": p1, "listener": p2,
                                "word": random.choice(st.session_state.all_words),
                                "t_end": time.time() + data.get("duration", 60)
                            })
                            st.rerun()
                        else:
                            st.error("Потрібно мінімум 2 гравці!")
                else:
                    st.warning("⏳ Хост готує наступний хід...")
                    time.sleep(2)
                    st.rerun()

            # --- ПІДСТАН 2: Активний хід (Таймер) ---
            else:
                # Додаємо безпечне отримання значення. Якщо t_end немає, ставимо 0
                t_end = data.get("t_end")

                if t_end is None:
                    # Якщо таймера ще немає в базі, просто малюємо заглушку і робимо реран
                    st.info("⌛ Готуємося до старту...")
                    time.sleep(1)
                    st.rerun()
                else:
                    rem = int(t_end - time.time())

                    if rem <= 0:
                        st.warning("⏰ Час вийшов!")
                        if is_host:
                            if st.button("НАСТУПНИЙ ХІД ➡️", use_container_width=True):
                                # Очищаємо дані ходу для наступної пари
                                ref.update({
                                    "explainer": "",
                                    "listener": "",
                                    "word": "",
                                    "t_end": None,  # Важливо очистити таймер
                                    "current_round": current_round + 1
                                })
                                st.rerun()
                        else:
                            st.info("🕒 Очікуємо, поки хост переключить раунд...")
                            time.sleep(2)
                            st.rerun()
                    else:
                        # Твій звичайний код відображення ходу
                        st.subheader(f"⏱ {rem} сек | {data['explainer']} ➜ {data['listener']}")
                        # ... далі твій код з кнопками ✅ ВГАДАНО / ❌ СКІП ...

                    if my_name == data["explainer"]:
                        st.success("ТВОЯ ЧЕРГА ПОЯСНЮВАТИ!")
                        st.markdown(f'<div class="word-box">{data["word"].upper()}</div>', unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        if c1.button("✅ ВГАДАНО", use_container_width=True):
                            new_scores = data.get("scores", {})
                            new_scores[my_name] = new_scores.get(my_name, 0) + 1
                            ref.update({"scores": new_scores, "word": random.choice(st.session_state.all_words)})
                            st.rerun()
                        if c2.button("❌ ПРОПУСТИТИ", use_container_width=True):
                            ref.update({"word": random.choice(st.session_state.all_words)})
                            st.rerun()

                    elif my_name == data["listener"]:
                        st.warning("ТИ ВІДГАДУЄШ!")
                        st.markdown('<div class="word-box">???</div>', unsafe_allow_html=True)
                    else:
                        st.info(f"Грають {data['explainer']} та {data['listener']}")

                    time.sleep(1)
                    st.rerun()
    else:
        st.error("Кімнату не знайдено!")
        st.session_state.game_state = "mode_select"
        st.rerun()
# --- IRL РЕЖИМ ---
elif st.session_state.game_state == "playing_irl":
    if st.session_state.current_round > st.session_state.total_rounds:
        st.session_state.game_state = "finished"
        st.rerun()

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
