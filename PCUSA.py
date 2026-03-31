import streamlit as st
st.title("MRZ Generator + Validator (TD1 / Passport Card style)")
# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def char_value(c):
    if c.isdigit():
        return int(c)
    if c == "<":
        return 0
    return ord(c) - 55  # A=10 ... Z=35
def check_digit(data):
    weights = [7, 3, 1]
    total = 0
    for i, c in enumerate(data):
        total += char_value(c) * weights[i % 3]
    return str(total % 10)
def format_name(s):
    return s.upper().replace(" ", "<")
def pad(text, length):
    return text.ljust(length, "<")[:length]
def split_optional(data):
    return [x for x in data.split("<") if x]
# --- ВВОД ДАННЫХ ---
st.subheader("Основные данные")
doc_type = st.text_input("Тип документа (например IP)", "IP")
country = st.text_input("Страна выдачи (3 буквы)", "USA")
document_number = st.text_input("Номер документа", "C081685505")
st.subheader("Персональные данные")
surname = st.text_input("Фамилия", "SOLANKI")
given_names = st.text_input("Имя и второе имя", "PADMANAND Y")
sex = st.selectbox("Пол", ["M", "F", "<"])
nationality = st.text_input("Гражданство", "USA")
st.subheader("Даты")
birth_date = st.text_input("Дата рождения (YYMMDD)", "611120")  
expiry_date = st.text_input("Срок действия (YYMMDD)", "240529")
st.subheader("Дополнительные данные")
optional1 = st.text_input("Доп. данные строка 1 (например 07<21<B02<121)", "07<21<B02<121")
optional2 = st.text_input("Доп. данные строка 2", "2623327569")
# --- ГЕНЕРАЦИЯ ---
if st.button("Сгенерировать MRZ"):
    # --- СТРОКА 1 ---
    line1_core = doc_type + country + document_number
    line1 = pad(line1_core + "<<" + optional1, 30)
    # --- СТРОКА 2 ---
    birth_cd = check_digit(birth_date)
    expiry_cd = check_digit(expiry_date)
    line2_core = (
        birth_date + birth_cd +
        sex +
        expiry_date + expiry_cd +
        nationality
    )
    line2 = pad(line2_core + "<<" + optional2, 30)
    # --- СТРОКА 3 ---
    name_block = format_name(surname) + "<<" + format_name(given_names)
    line3 = pad(name_block, 30)
    # --- ВЫВОД MRZ ---
    st.subheader("Сгенерированный MRZ")
    st.text(line1)
    st.text(line2)
    st.text(line3)
    # --- ПРОВЕРКА ---
    st.subheader("Проверка валидности")
    calc_birth_cd = check_digit(birth_date)
    calc_expiry_cd = check_digit(expiry_date)
    st.write("Контроль даты рождения:", birth_cd, "| Проверка:", calc_birth_cd == birth_cd)
    st.write("Контроль срока:", expiry_cd, "| Проверка:", calc_expiry_cd == expiry_cd)
    st.subheader("Разбивка optional data")
    st.write("Строка 1:", split_optional(optional1))
    st.write("Строка 2:", split_optional(optional2))
