import streamlit as st
st.title("US Passport Card MRZ Generator (реальный формат)")
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
# --- ВВОД ---
doc_type = st.text_input("Тип документа", "IP")
country = st.text_input("Страна", "USA")
document_number = st.text_input("Номер документа", "C12928600")
surname = st.text_input("Фамилия", "GOMEZ")
given_names = st.text_input("Имя", "KEVIN ALEXANDER")
sex = st.selectbox("Пол", ["M", "F", "<"])
nationality = st.text_input("Гражданство", "USA")
birth_date = st.text_input("Дата рождения YYMMDD", "930728")
expiry_date = st.text_input("Срок действия YYMMDD", "260831")
optional1 = st.text_input("Optional строка 1", "05<15<B02<323")
optional2 = st.text_input("Optional строка 2", "4187905123")
# --- ГЕНЕРАЦИЯ ---
if st.button("Сгенерировать"):
    # контрольные цифры
    doc_cd = check_digit(document_number)
    birth_cd = check_digit(birth_date)
    expiry_cd = check_digit(expiry_date)
    # СТРОКА 1 (как в США)
    line1 = pad(
        doc_type + country + document_number + doc_cd + "<<" + optional1,
        30
    )
    # СТРОКА 2
    line2 = pad(
        birth_date + birth_cd +
        sex +
        expiry_date + expiry_cd +
        nationality + "<<" + optional2,
        30
    )
    # СТРОКА 3
    line3 = pad(
        format_name(surname) + "<<" + format_name(given_names),
        30
    )
    st.subheader("MRZ")
    st.text(line1)
    st.text(line2)
    st.text(line3)
    # --- ПРОВЕРКА (как валидатор) ---
    st.subheader("Проверка")
    # 1. Проверка номера
    extracted_number = line1[5:14]
    extracted_cd = line1[14]
    valid_doc = check_digit(extracted_number) == extracted_cd
    # 2. Проверка даты рождения
    birth = line2[0:6]
    birth_cd_real = line2[6]
    valid_birth = check_digit(birth) == birth_cd_real
    # 3. Проверка срока
    expiry = line2[8:14]
    expiry_cd_real = line2[14]
    valid_expiry = check_digit(expiry) == expiry_cd_real
    st.write("Номер документа валиден:", valid_doc)
    st.write("Дата рождения валидна:", valid_birth)
    st.write("Срок действия валиден:", valid_expiry)
