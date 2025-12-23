import streamlit as st
import random
import time
import os

# Налаштування сторінки
st.set_page_config(page_title="Alias Ultimate - Wezaxes Edition", page_icon="🎮", layout="centered")

# Стилізація інтерфейсу
st.markdown("""
    <style>
    /* Центрування кнопок */
    .stButton { display: flex; justify-content: center; }
    .stButton>button { 
        width: 100%; 
        max-width: 500px;
        height: 4.5em; 
        font-size: 24px !important; 
        font-weight: bold; 
        border-radius: 15px; 
        transition: 0.3s; 
        margin-bottom: 10px;
        text-transform: uppercase;
    }
    .stButton>button:hover { transform: scale(1.02); }
    h1, h2, h3, p { text-align: center !important; }
    
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

# --- РОБОТА З ФАЙЛОМ ---
def load_words_from_file():
    filename = "words.txt"
    default_words = ["Пудж", "Бебра", "Стан", "Мід", "Рошан", "Сленг", "Крінж", "Абобус", "Wezaxes", "Тілт"]
    if not os.path.exists(filename):
        with open(filename, "w", encoding="utf-8") as f:
            for w in default_words:
                f.write(w + "\n")
        return default_words
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def append_word_to_file(word):
    with open("words.txt", "a", encoding="utf-8") as f:
        f.write(word + "\n")

# Ініціалізація станів
if 'init_done' not in st.session_state:
    st.session_state.all_words = load_words_from_file()
    st.session_state.teams = {}
    st.session_state.team_names = []
    st.session_state.current_team_idx = 0
    st.session_state.current_round = 1
    st.session_state.playing = False
    st.session_state.game_over = False
    st.session_state.welcome_done = False
    st.session_state.last_added_word = ""
    st.session_state.init_done = True

# --- 1. ЕКРАН ДИСКЛЕЙМЕРА ---
if not st.session_state.welcome_done:
    st.markdown("<h2 style='color: #fab387;'>ДИСКЛЕЙМЕР</h2>", unsafe_allow_html=True)
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
    
        with st.expander("➕ Додати своє дебільне слово"):
        st.warning("⚠️ Вписуйте тільки ті слова, які реально грабельні і які можна пояснити!")
        
        # Ініціалізація пам'яті для повідомлень та останнього слова, якщо їх ще немає
        if 'msg' not in st.session_state: st.session_state.msg = None
        if 'msg_type' not in st.session_state: st.session_state.msg_type = None
        if 'last_added_word' not in st.session_state: st.session_state.last_added_word = ""

        # Рандомний приклад слова (беремо з сесії)
        example_word = random.choice(st.session_state.all_words) if st.session_state.all_words else "Слово"
        
        # Поле вводу
        new_word_raw = st.text_input("Введи слово:", placeholder=f"Наприклад: {example_word}")

        if st.button("ДОДАТИ В СЛОВНИК"):
            clean_word = new_word_raw.strip().capitalize()
            compare_word = new_word_raw.strip().lower()
            
            # Очищений список для перевірки на дублікати
            existing_words_clean = [w.strip().lower() for w in st.session_state.all_words]

            if not clean_word:
                st.session_state.msg = "Ну введи хоч щось..."
                st.session_state.msg_type = "warning"
            elif compare_word in existing_words_clean:
                st.session_state.msg = "Таке слово вже є, давай придумаємо щось прикольніше"
                st.session_state.msg_type = "error"
            else:
                # 1. Додаємо в список у сесії
                st.session_state.all_words.append(clean_word)
                # 2. Записуємо у файл words.txt
                append_word_to_file(clean_word)
                # 3. Зберігаємо як ОСТАННЄ додане
                st.session_state.last_added_word = clean_word
                # 4. Готуємо повідомлення про успіх
                st.session_state.msg = f"Вітаю, ви придумали нове прикольне слово, дякую! (Всього: {len(st.session_state.all_words)})"
                st.session_state.msg_type = "success"
            
            # Перезавантажуємо, щоб зберегти зміни
            st.rerun()

        # --- ТУТ МИ ВИВОДИМО РЕЗУЛЬТАТИ ПІСЛЯ ПЕРЕЗАВАНТАЖЕННЯ ---
        
        # Вивід повідомлення (зелене/червоне/жовте)
        if st.session_state.msg:
            if st.session_state.msg_type == "success":
                st.success(st.session_state.msg)
            elif st.session_state.msg_type == "error":
                st.error(st.session_state.msg)
            elif st.session_state.msg_type == "warning":
                st.warning(st.session_state.msg)
            
            # Очищуємо повідомлення після виводу, щоб воно не висіло вічно
            # (якщо хочеш щоб висіло - видали ці два рядки нижче)
            st.session_state.msg = None 
            st.session_state.msg_type = None

        # Вивід останнього доданого слова (беремо з сесії)
        if st.session_state.last_added_word:
            st.markdown(f"**Останнє додане слово:** `{st.session_state.last_added_word}`")


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
        st.session_state.game_words = st.session_state.all_words.copy()
        random.shuffle(st.session_state.game_words)
        st.session_state.playing = True
        st.rerun()

# --- 3. ЕКРАН ГРИ ---
elif st.session_state.playing:
    current_team = st.session_state.team_names[st.session_state.current_team_idx]
    
    if 'start_time' not in st.session_state:
        st.title(f"Черга: {current_team}")
        st.write(f"### Раунд: {st.session_state.current_round} / {st.session_state.total_rounds}")
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
            st.write(f"### ⏱ {time_left} сек | {current_team}: {st.session_state.teams[current_team]} ⭐")
            
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
        st.write(f"### {i+1}. {name}: {score} балів")
    
    if st.button("ЗІГРАТИ ЩЕ РАЗ 🔄"):
        words_backup = load_words_from_file() # Підтягуємо нові слова з файлу
        st.session_state.clear()
        st.session_state.all_words = words_backup
        st.session_state.init_done = True
        st.session_state.welcome_done = True
        st.rerun()
