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
        st.markdown(
            "### 🏠 Режим IRL\n**Для тих, хто в одній кімнаті:**\n* Один телефон на всіх.\n* Передаєте мобілу тому, чия черга.\n* Тиснете **'Я готовий'** і вперед!")
    with col2:
        st.markdown(
            "### 🎙️ DISCORD\n**Для гри на відстані:**\n* Кожен заходить зі свого девайсу.\n* Один створює кімнату (Начальнік), інші вводять код.\n* Система сама каже, хто пояснює.")

    st.info("💡 **Головне правило:** Пояснюй як хочеш, але не називай саме слово або спільнокореневі.")
    st.write(
        "➕ У налаштуваннях можна додати свої слова! (ми ще не розібралися як вони зберігаються, але обовʼязково пофіксимо). p.s: при натисканні вас флешне, будьте готові)))")
    if st.button("ЗРОЗУМІВ, ПОГНАЛИ! 🚀"):
        st.session_state.game_state = "mode_select"
        st.rerun()

elif st.session_state.game_state == "mode_select":
    st.title("🕹️ Оберіть режим гри")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            '<a href="/?mode=irl" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🏠 IRL</h3><p>Командна гра вживу</p></div></a>',
            unsafe_allow_html=True)
    with col2:
        st.markdown(
            '<a href="/?mode=discord" target="_self" style="text-decoration: none;"><div class="mode-selection"><h3>🎙️ DISCORD</h3><p>Грайте разом онлайн</p></div></a>',
            unsafe_allow_html=True)

    st.divider()
    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        if st.button("❓ Я ЗАБУВ ЯК РУЛИТЬ", use_container_width=True):
            st.session_state.game_state = "tutorial";
            st.rerun()

elif st.session_state.game_state == "setup":
    if st.button("⬅️ НАЗАД"):
        st.session_state.game_state = "mode_select";
        st.rerun()

    st.markdown("### ⚙️ Налаштування")

    # 1. Твій нік (тільки для Discord)
    if st.session_state.game_mode == "discord":
        my_name = st.text_input("Твій нікнейм:", placeholder="Введи шось прикольне...", key="setup_name")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<p style='text-align: center; font-weight: bold;'>Ти хостити будеш?</p>",
                        unsafe_allow_html=True)
            st.markdown("<div style='height: 57px;'></div>", unsafe_allow_html=True)
            if st.button("СТВОРИТИ КІМНАТУ ✨"):
                if my_name:
                    r_id = generate_room_code()
                    st.session_state.room_id = r_id;
                    st.session_state.my_name = my_name
                    if db:
                        db.collection("rooms").document(r_id).set({
                            "host": my_name, "players": [my_name], "scores": {my_name: 0},
                            "state": "lobby", "total_rounds": 3, "duration": 60, "current_round": 1,
                            "explainer": "", "listener": "", "word": ""
                        })
                        st.session_state.game_state = "sync_lobby";
                        st.rerun()
                else:
                    st.error("Спочатку введи нікнейм!")

        with col2:
            st.markdown("<p style='text-align: center; font-weight: bold;'>Маєш код?</p>", unsafe_allow_html=True)
            enter_code = st.text_input("Введи код:", placeholder="Код тут...", label_visibility="collapsed",
                                       key="join_input_sync").upper().strip()
            if st.button("УВІЙТИ 🚪"):
                if my_name and enter_code:
                    if db:
                        ref = db.collection("rooms").document(enter_code)
                        doc = ref.get()
                        if doc.exists:
                            data = doc.to_dict()
                            st.session_state.room_id = enter_code;
                            st.session_state.my_name = my_name
                            if my_name not in data["players"]:
                                data["players"].append(my_name)
                                data["scores"][my_name] = 0
                                ref.update({"players": data["players"], "scores": data["scores"]})
                            st.session_state.game_state = "sync_lobby";
                            st.rerun()
                        else:
                            st.error("❌ Код невірний!")
                else:
                    st.error("Введи нік та код!")

    # --- ЛОГІКА IRL ---
    elif st.session_state.game_mode == "irl":
        st.subheader("🏠 Налаштування гри вживу")
        num = st.slider("Кількість команд?", 2, 6, 2)
        names = []
        c_names = st.columns(2)
        for i in range(num):
            with c_names[i % 2]:
                name = st.text_input(f"Команда {i + 1}", f"Команда {i + 1}", key=f"n_{i}")
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
                st.session_state.players = names;
                st.session_state.scores = {n: 0 for n in names}
                st.session_state.total_rounds = rounds;
                st.session_state.duration = timer
                st.session_state.current_player_idx = 0;
                st.session_state.current_round = 1
                st.session_state.game_state = "playing_irl";
                st.rerun()

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
            if st.session_state.msg_data["type"] == "success":
                st.success(st.session_state.msg_data["text"])
            else:
                st.error(st.session_state.msg_data["text"])
        if st.session_state.last_added_word:
            st.markdown(f"✅ Останнє: **{st.session_state.last_added_word}**")

# --- СИНХРОНІЗОВАНЕ ЛОББІ (DISCORD) ---
elif st.session_state.game_state == "sync_lobby":
    st.title(f"🏠 Кімната: {st.session_state.room_id}")
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()

    if doc.exists:
        data = doc.to_dict()
        current_players = data.get("players", [])
        my_name = st.session_state.my_name
        is_host = (data.get("host") == my_name)

        # Сповіщення (тоасти)
        if "old_players" not in st.session_state:
            st.session_state.old_players = current_players
        for p in current_players:
            if p not in st.session_state.old_players:
                st.toast(f"✨ {p} приєднався до гри!")
        for p in st.session_state.old_players:
            if p not in current_players:
                st.toast(f"🚪 {p} лівнув з катки...")
        st.session_state.old_players = current_players

        with st.sidebar:
            st.write(f"🏠 Код: **{st.session_state.room_id}**")
            st.write(f"👤 Ти: **{my_name}** {'(👑)' if is_host else ''}")
            st.divider()
            st.write("👥 Гравці:")
            for p in current_players:
                st.caption(f"• {p} {'(Хост)' if p == data.get('host') else ''}")

            if st.button("🔴 ВИЙТИ З ГРИ", key="exit_btn"):
                updated_players = [p for p in current_players if p != my_name]
                ref.update({"players": updated_players})
                del st.session_state.room_id
                st.session_state.game_state = "mode_select"
                st.rerun()
    elif doc.exists:
        st.error("Кімнату не знайдено!");
        st.session_state.game_state = "setup";
        st.rerun()

    data = doc.to_dict()
    if data.get("state") == "playing":
        st.session_state.game_state = "playing_sync";
        st.rerun()

    st.write("### Гравці в лобі:")
    cols = st.columns(3)
    for i, p in enumerate(data["players"]):
        cols[i % 3].button(f"👤 {p}", disabled=True, key=f"p_{i}")

    st.divider()
    is_host = (data.get("host") == st.session_state.my_name)

    if is_host:
        st.subheader("👑 Ви Хост (Адмін)")
        h_rounds = st.number_input("Кількість раундів", 1, 20, data.get("total_rounds", 3), key="host_rounds_sync")
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
        updated_players = [p for p in current_players if p != my_name]
        ref.update({"players": updated_players})
        del st.session_state.room_id
        st.session_state.game_state = "mode_select"
        st.rerun()

    time.sleep(2);
    st.rerun()

# --- ЗАГАЛЬНА ЛОГІКА ДЛЯ DISCORD (САЙДБАР, СПОВІЩЕННЯ ТА ЕКРАНИ) ---
# --- САЙДБАР (З'ЯВЛЯЄТЬСЯ ВІДРАЗУ ПРИ НАЯВНОСТІ ROOM_ID) ---
if 'room_id' in st.session_state and st.session_state.game_state == "playing_sync":
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()

    if doc.exists:
        data = doc.to_dict()
        current_players = data.get("players", [])
        my_name = st.session_state.my_name
        is_host = (data.get("host") == my_name)

        # Сповіщення (тоасти)
        if "old_players" not in st.session_state:
            st.session_state.old_players = current_players
        for p in current_players:
            if p not in st.session_state.old_players:
                st.toast(f"✨ {p} приєднався до гри!")
        for p in st.session_state.old_players:
            if p not in current_players:
                st.toast(f"🚪 {p} лівнув з катки...")
        st.session_state.old_players = current_players

        with st.sidebar:
            st.write(f"🏠 Код: **{st.session_state.room_id}**")
            st.write(f"👤 Ти: **{my_name}** {'(👑)' if is_host else ''}")
            st.divider()
            st.write("👥 Гравці:")
            for p in current_players:
                st.caption(f"• {p} {'(Хост)' if p == data.get('host') else ''}")

            if st.button("🔴 ВИЙТИ З ГРИ", key="exit_btn"):
                updated_players = [p for p in current_players if p != my_name]
                ref.update({"players": updated_players})
                del st.session_state.room_id
                st.session_state.game_state = "mode_select"
                st.rerun()

# --- ЕКРАНИ ЛОБІ ТА ГРИ ---
if st.session_state.game_state == "sync_lobby":
    # Перевіряємо, чи ми вже отримали дані в блоці сайдбару вище
    ref = db.collection("rooms").document(st.session_state.room_id)
    data = ref.get().to_dict()

    if data.get("state") == "playing":
        st.session_state.game_state = "playing_sync"
        st.rerun()

    st.title("🏠 Лобі очікування")

    # Вивід плиток гравців
    cols = st.columns(3)
    for i, p in enumerate(data.get("players", [])):
        cols[i % 3].button(f"👤 {p}", disabled=True, key=f"l_p_{i}")

    st.divider()
    if is_host:
        st.subheader("⚙️ Налаштування раундів")
        # Встановлюємо значення прямо з бази, щоб не злітало
        h_rounds = st.number_input("Раундів", 1, 20, value=int(data.get("total_rounds", 3)), key="host_r_input")
        h_timer = st.slider("Час (сек)", 10, 120, value=int(data.get("duration", 60)), key="host_t_input")

        # Оновлюємо БД тільки якщо значення реально змінилися (це фіксить "зліт")
        if h_rounds != data.get("total_rounds") or h_timer != data.get("duration"):
            print(f"[UPDATE] Host changed settings: Rounds={h_rounds}, Time={h_timer}")
            ref.update({"total_rounds": h_rounds, "duration": h_timer})

        if st.button("ПОЧАТИ ГРУ 🔥", use_container_width=True):
            print("[GAME] Host started the match!")
            ref.update({"state": "playing", "current_round": 1, "explainer": "", "listener": ""})
            st.rerun()
    else:
        st.info("🕒 Чекаємо, поки хост запустить гру...")
        st.write(f"📊 Раундів: **{data.get('total_rounds')}** | ⏱ Час: **{data.get('duration')}с**")

    time.sleep(2)
    st.rerun()


elif st.session_state.game_state == "playing_sync":
    # 1. Отримуємо свіжі дані з бази
    ref = db.collection("rooms").document(st.session_state.room_id)
    doc = ref.get()
    if not doc.exists:
        st.session_state.game_state = "mode_select"
        st.rerun()

    data = doc.to_dict()
    total_rounds = data.get("total_rounds", 3)
    current_round = data.get("current_round", 1)
    my_name = st.session_state.my_name
    is_host = (data.get("host") == my_name)

    # Перевірка на фінал гри
    if current_round > total_rounds:
        st.session_state.scores = data.get("scores", {})
        st.session_state.game_state = "finished"
        st.rerun()

    # Стан 1: Очікування початку ходу (вибір пари)
    if not data.get("explainer"):
        st.title(f"Раунд {current_round} з {total_rounds}")

        quotes = [
            "💡 Порада: якщо не знаєш слова - кажи що всі інші безнадійні і теж не знають та скіпай!",
            "💅 Факт: зі словника колись приберуть слово Імплікація. Чесно.",
            "⏳ Очікуємо... Тим часом придумай, як пояснити слово 'Бебра'.",
            "🚀 Шанс випадіння тупого слова сьогодні — 99%.",
            "🎮 Ви вже намагались написати сюди слово хуй?",
            "🎲 Натисни і дізнайся, що зламається цього разу.",
            "🚨 Увага: можливий словесний понос.",
            "🎤 Порада: пояснюй, ніби перед тобою пʼятирічна дитина.",
            "🤝 Порада: команда не осудить. Максимум похіхікає.",
            "🚨 Увага: можливі слова, які неможливо пояснити, імпровізуйте я хз.",
            "🚨 Увага: наступне слово може викликати екзистенційну кризу у всієї команди.",
            "🚨 Увага: шанс того, що ви зараз посваритесь через неправильну здогадку — 85%.",
            "🚨 Увага: гра може викликати раптові напади сміху або бажання видалити цей код.",
            "🚨 Увага: ми все ще не знаємо, як працює база даних, тому просто насолоджуйтесь моментом.",
            "🚨 Увага: якщо партнер вас не розуміє, можливо, справа не в слові, а в партнері?",
            "🚨 Увага: кожне пропущене слово робить хост-бота трохи сумнішим.",
            "🚨 Увага: імпровізація — це ваш єдиний шанс вижити в цьому раунді.",
            "🚨 Увага: цей напис тут просто щоб ви не бачили, яке складне слово зараз випаде.",
            "🛸 Цей напис тут просто щоб ви не нудьгували, поки інші гравці нарешті зайдуть у лобі.",
            "🛸 Цей напис тут просто щоб забити місце на екрані, поки сервер збирає ваші дані для оформлення кредиту.",
            "🚨 Цей напис тут просто щоб забити місце на екрані, поки база даних намагається не впасти.",
            "🛸 Цей напис тут просто щоб створити ілюзію активності, поки ви чекаєте на старт.",
            "🛸 Цей напис тут просто щоб ви хоч щось читали, поки всі збираються з думками.",
            "🛸 Цей напис тут просто щоб додати трохи загадковості перед початком гри.",
            "🛸 Цей напис тут просто щоб ви не забули, як виглядає екран вашого телефону.",
            "⚠️ Не оновлюй. Працює ж.",
            "🤝 Якщо не вгадав слово, це не ти тупий - це пояснили хуйово.",
            "⏳ Очікуємо... Тим часом придумай, як пояснити слово «шльоп».",
            "⏳ Очікуємо... Поясни людині, що таке «кринжулька».",
            "⏳ Очікуємо... Спробуй не засміятись, пояснюючи «бульк».",
            "⏳ Очікуємо... Як би ти описав слово «хернячок»?",
            "⏳ Очікуємо... Поясни «плюмп» без жестів. А, ні, з жестами можна.",
            "⏳ Очікуємо... Ну давай, що таке «шмигдик»?",
            "⏳ Очікуємо... Поясни «ляпця» так, щоб тебе зрозуміли.",
            "⏳ Очікуємо... Слово «фігня» але ускладнений рівень.",
            "⏳ Очікуємо... Як пояснити «бздик», якщо ти доросла людина?",
            "⏳ Очікуємо... Спробуй логічно пояснити «хлюп».",
            "⏳ Очікуємо... Поясни «квазіпук». Так, це слово.",
            "⏳ Очікуємо... Ну що, як там з поясненням «шурушун»?",
            "⏳ Очікуємо... Поясни «йойк». Без «ну типу».",
            "⏳ Очікуємо... Слово «пукля». Удачі.",
            "⏳ Очікуємо... Як би ти описав «мдааа»?",
            "⏳ Очікуємо... Поясни «хихань». Не смійся.",
            "⏳ Очікуємо... Спробуй пояснити «блінчик» без їжі.",
            "📐 4(x - 5) = 3x - 6",
            "📐 (a - 4)(a + 2) - (a - 1)²",
            "📐 25x² - 16y²",
            "📐 2x³ - 3x² + x, x = -1",
            "📐 (x⁴)² * x³",
            "📐 x + y = 5 та 2x - y = 1",
            "📐 (-0,2)⁴ * 5⁴",
            "📐 -3a²b * 4a³b⁴",
            "📐 |x + 3| = 7",
            "📐 ax + ay + 3x + 3y",
            "📐 Кути рівнобедреного трикутника, вершина 40°",
            "📐 (x - 3)(x + 3) = x² - 9",
            "📐 (x + 2)/3 - (x - 1)/2 = 1",
            "📐 (3m - n)² - (3m + n)²",
            "📐 Графік функції y = 2x - 3",
            "📐 2x² - 3x + 1 та x² + 3x - 4",
            "😁 Ми теж не знаємо що таке Барбадос."
        ]

        st.info(random.choice(quotes))

        if is_host:
            if st.button("ПОЧАТИ ХІД 🎲", use_container_width=True):
                current_players = data.get("players", [])
                if len(current_players) >= 2:
                    p1, p2 = random.sample(current_players, 2)
                    print(f"[GAME] Host picked: {p1} explaining to {p2}")
                    ref.update({
                        "explainer": p1,
                        "listener": p2,
                        "word": random.choice(st.session_state.all_words),
                        "t_end": time.time() + data.get("duration", 60)
                    })
                    st.rerun()
                else:
                    st.error("Для гри потрібно мінімум 2 гравці!")
        else:
            st.warning("⏳ Очікуємо, поки хост запустить наступний хід...")
            time.sleep(2)
            st.rerun()

    # Стан 2: Активний хід (таймер і слова)
    else:
        rem = int(data["t_end"] - time.time())

        if rem <= 0:
            ref.update({
                "explainer": "",
                "listener": ""
            })
            st.warning("⏰ Час вийшов!")
            if is_host:
                if st.button("НАСТУПНИЙ ХІД ➡️", use_container_width=True):
                    ref.update({
                        "word": "",
                        "current_round": current_round + 1 if is_host else current_round
                    })
                    st.rerun()
            else:
                st.info("🕒 Очікуємо, поки хост переключить раунд...")
                time.sleep(2)
                st.rerun()
        else:
            st.subheader(f"⏱ Залишилось: {rem} сек")
            st.write(f"🎤 Пояснює: **{data['explainer']}** ➜ Слухає: **{data['listener']}**")

            if my_name == data["explainer"]:
                st.success("ТВОЯ ЧЕРГА ПОЯСНЮВАТИ!")
                st.markdown(f'<div class="word-box">{data["word"].upper()}</div>', unsafe_allow_html=True)

                c1, c2 = st.columns(2)
                if c1.button("✅ ВГАДАНО", use_container_width=True):
                    # Оновлюємо бали в базі
                    new_scores = data.get("scores", {})
                    new_scores[my_name] = new_scores.get(my_name, 0) + 1
                    ref.update({
                        "scores": new_scores,
                        "word": random.choice(st.session_state.all_words)
                    })
                    st.rerun()

                if c2.button("❌ ПРОПУСТИТИ", use_container_width=True):
                    ref.update({"word": random.choice(st.session_state.all_words)})
                    st.rerun()

            elif my_name == data["listener"]:
                st.warning("ТИ ВІДГАДУЄШ!")
                st.markdown('<div class="word-box">???</div>', unsafe_allow_html=True)

            else:
                st.info("Спостерігайте за грою інших...")
                st.markdown(f'<div class="word-box" style="font-size: 24px;">{data["explainer"]} пояснює...</div>',
                            unsafe_allow_html=True)

            time.sleep(1)
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
            st.session_state.current_word = random.choice(st.session_state.all_words);
            st.rerun()
    else:
        rem = int(st.session_state.duration - (time.time() - st.session_state.start_time))
        if rem <= 0:
            st.session_state.turn_active = False
            st.session_state.current_player_idx = (st.session_state.current_player_idx + 1) % len(
                st.session_state.players)
            if st.session_state.current_player_idx == 0: st.session_state.current_round += 1
            st.rerun()
        st.subheader(f"⏱ {rem} сек | {active}")
        st.markdown(f'<div class="word-box">{st.session_state.current_word.upper()}</div>', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("✅ ВГАДАНО"):
            st.session_state.scores[active] += 1;
            st.session_state.current_word = random.choice(st.session_state.all_words);
            st.rerun()
        if c2.button("❌ СКІП"):
            st.session_state.current_word = random.choice(st.session_state.all_words);
            st.rerun()
        time.sleep(0.1);
        st.rerun()

# --- ФІНАЛ ---
elif st.session_state.game_state == "finished":
    st.balloons();
    st.title("🏆 РЕЗУЛЬТАТИ")
    for n, s in sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True):
        st.write(f"### {n}: {s} балів")
    if st.button("В ГОЛОВНЕ МЕНЮ 🔄"):
        st.session_state.game_state = "mode_select";
        st.rerun()