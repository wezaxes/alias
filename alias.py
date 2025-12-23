import streamlit as st
import random
import time

# --- НАЛАШТУВАННЯ ТА БРЕНДИНГ ---
st.set_page_config(page_title="Alias - Wezaxes Edition", layout="centered")

# Стилізація великих кнопок через CSS
st.markdown("""
    <style>
    div.stButton > button:first-child {
        height: 100px;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .st-emotion-cache-12fmjuu { 
        font-size: 30px !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# Ініціалізація бази слів у сесії
if 'words' not in st.session_state:
    st.session_state.words = ["Україна", "Борщ", "Кава", "Велосипед", "Програміст", "iPhone", "Кіт", "Паляниця"]

if 'scores' not in st.session_state:
    st.session_state.scores = {}
    st.session_state.game_started = False
    st.session_state.current_round = 1
    st.session_state.team_idx = 0
    st.session_state.welcome_done = False

# --- ВІКНО ПРИВІТАННЯ ---
if not st.session_state.welcome_done:
    st.title("ДИСКЛЕЙМЕР КОД ПИСАЛА ЖІНКА‼️")
    st.error("### УВАГА!")
    st.write("Це СУПЕР пробна версія. Слова і все інше ше буде допрацьовуватись, шанс потрапити на тупориле слово 70%.")
    if st.button("ЛАДНО"):
        st.session_state.welcome_done = True
        st.rerun()
    st.stop()

# --- НАЛАШТУВАННЯ ГРИ ---
if not st.session_state.game_started:
    st.title("⚙️ Налаштування Alias")
    
    n_teams = st.number_input("Скільки команд?", 2, 6, 2)
    teams = []
    for i in range(n_teams):
        name = st.text_input(f"Назва команди {i+1}", f"Команда {i+1}")
        teams.append(name)
    
    rounds = st.number_input("Кількість раундів", 1, 20, 3)
    r_time = st.number_input("Час раунду (сек)", 10, 300, 60)
    
    if st.button("ПОЧАТИ ГРУ"):
        st.session_state.teams = teams
        st.session_state.scores = {name: 0 for name in teams}
        st.session_state.total_rounds = rounds
        st.session_state.duration = r_time
        st.session_state.game_started = True
        st.rerun()
    
    # Додавання слів
    st.divider()
    new_w = st.text_input("Додати нове слово в базу:")
    if st.button("Додати"):
        if new_w:
            st.session_state.words.append(new_w)
            st.success(f"Слово '{new_w}' додано!")

else:
    # --- ІГРОВИЙ ЕКРАН ---
    team_list = st.session_state.teams
    current_team = team_list[st.session_state.team_idx]
    
    st.subheader(f"Раунд {st.session_state.current_round} / {st.session_state.total_rounds}")
    st.info(f"Зараз грає: **{current_team.upper()}**")
    
    if 'round_active' not in st.session_state or not st.session_state.round_active:
        if st.button(f"ПОЧАТИ РАУНД ({current_team})"):
            st.session_state.round_active = True
            st.session_state.start_time = time.time()
            st.session_state.current_word = random.choice(st.session_state.words)
            st.rerun()
    else:
        # Раунд активний
        elapsed = time.time() - st.session_state.start_time
        remaining = int(st.session_state.duration - elapsed)
        
        if remaining <= 0:
            st.session_state.round_active = False
            st.session_state.team_idx += 1
            if st.session_state.team_idx >= len(team_list):
                st.session_state.team_idx = 0
                st.session_state.current_round += 1
            
            if st.session_state.current_round > st.session_state.total_rounds:
                st.success("ГРА ЗАВЕРШЕНА!")
                st.write(st.session_state.scores)
                if st.button("Нова гра"):
                    st.session_state.game_started = False
                    st.rerun()
            else:
                st.warning("ЧАС ВИЙШОВ!")
                st.rerun()
        
        st.metric("Залишилось часу", f"{remaining} сек")
        
        # Відображення слова
        st.markdown(f"""
            <div style="background-color: #313244; padding: 40px; border-radius: 15px; text-align: center; margin: 20px 0;">
                <h1 style="color: #f9e2af; margin: 0;">{st.session_state.current_word.upper()}</h1>
            </div>
        """, unsafe_allow_html=True)
        
        # Великі кнопки одна під одною
        if st.button("✅ ВГАДАНО (+1)"):
            st.session_state.scores[current_team] += 1
            st.session_state.current_word = random.choice(st.session_state.words)
            st.rerun()
            
        if st.button("❌ СКІП (-1)"):
            st.session_state.scores[current_team] -= 1
            st.session_state.current_word = random.choice(st.session_state.words)
            st.rerun()

    # Поточний рахунок внизу
    st.divider()
    st.write("### Рахунок:")
    st.write(st.session_state.scores)
