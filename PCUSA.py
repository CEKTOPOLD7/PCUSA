import streamlit as st
st.title("MRZ Generator + Full Validator (TD1)")
# --- ФУНКЦИИ ---
def char_value(c):
    if c.isdigit():
        return int(c)
    if c == "<":
        return 0
    return ord(c) - 55
def check_digit(data):
    weights = [7, 3, 1]
    total = 0
    for i, c in enumerate(data):
        total += char_value(c) * weights[i % 3]
    return str(total % 10)
def pad(text, length):
    return text.ljust(length, "<")[:length]
def format_name(s):
    return s.upper().replace(" ", "<")
def split_optional(data):
    return [x for x in data.split("<") if x]
# --- ВВОД ---
st.subheader("Основные данные")
doc_type = st.text_input("Тип документа (IP)", "IP")
country = st.text_input("Страна (USA)", "USA")
document_number = st.text_input("Номер документа", "C12928600")
st.subheader("Персональные данные")
surname = st.text_input("Фамилия", "GOMEZ")
given_names = st.text_input("Имя", "KEVIN ALEXANDER")
sex = st.selectbox("Пол", ["M", "F", "<"])
nationality = st.text_input("Гражданство", "USA")
st.subheader("Даты")
birth_date = st.text_input("Дата рождения YYMMDD", "930728")
expiry_date = st.text_input("Срок действия YYMMDD", "260831")
st.subheader("Дополнительные данные")
optional1 = st.text_input("Optional строка 1", "05<15<B02<323")
optional2 = st.text_input("Optional строка 2", "4187905123")
# --- ГЕНЕРАЦИЯ ---
if st.button("Сгенерировать MRZ"):
    # --- контрольные цифры ---
    doc_cd = check_digit(document_number)
    birth_cd = check_digit(birth_date)
    expiry_cd = check_digit(expiry_date)
    # --- СТРОКА 1 ---
    line1_core = doc_type + country + document_number + doc_cd
    line1 = pad(line1_core + "<<" + optional1, 30)
    # --- СТРОКА 2 ---
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
    # --- ВЫВОД ---
    st.subheader("MRZ")
    st.text(line1)
    st.text(line2)
    st.text(line3)
    # --- ПОЛНАЯ ПРОВЕРКА ---
    st.subheader("Проверка (как сканер)")
    # проверка номера
    doc_valid = (check_digit(document_number) == doc_cd)
    # проверка даты рождения
    birth_valid = (check_digit(birth_date) == birth_cd)
    # проверка срока
    expiry_valid = (check_digit(expiry_date) == expiry_cd)
    # ОБЩАЯ КОНТРОЛЬНАЯ СУММА (комбинированная)
    final_string = (
        document_number + doc_cd +
        birth_date + birth_cd +
        expiry_date + expiry_cd +
        optional2
    )
    final_cd = check_digit(final_string)
    st.write("Номер документа валиден:", doc_valid)
    st.write("Дата рождения валидна:", birth_valid)
    st.write("Срок действия валиден:", expiry_valid)
    st.write("Общая контрольная сумма:", final_cd)
    # --- OPTIONAL DATA ---
    st.subheader("Optional данные")
    st.write("Строка 1:", split_optional(optional1))
    st.write("Строка 2:", split_optional(optional2))
