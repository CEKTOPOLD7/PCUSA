import streamlit as st
st.title("MRZ Parser (Passport Card USA TD1)")
line1 = st.text_input("Строка 1 MRZ", "IPUSAC081685505<<07<21<B02<121")
line2 = st.text_input("Строка 2 MRZ", "6111209M2405296USA<<2623327569")
line3 = st.text_input("Строка 3 MRZ", "SOLANKI<<PADMANAND<Y<<<<<<<<<<")
def highlight_line1(line):
    return (
        f"<span style='color:red'> {line[0:2]} </span>"
        f"<span style='color:blue'> {line[2:5]} </span>"
        f"<span style='color:green'> {line[5:14]} </span>"
        f"<span style='color:gray'> {line[14:]} </span>"
    )
def highlight_line2(line):
    return (
        f"<span style='color:purple'> {line[0:7]} </span>"
        f"<span style='color:red'> {line[7]} </span>"
        f"<span style='color:green'> {line[8:14]} </span>"
        f"<span style='color:orange'> {line[14]} </span>"
        f"<span style='color:blue'> {line[15:18]} </span>"
        f"<span style='color:gray'> {line[18:]} </span>"
    )
def highlight_line3(line):
    parts = line.split("<<")
    surname = parts[0]
    rest = line[len(surname):]
    return (
        f"<span style='color:green'>{surname}</span>"
        f"<span style='color:gray'>{rest}</span>"
    )
def split_optional(data):
    return [x for x in data.split("<") if x]
if st.button("Разобрать MRZ"):
    st.subheader("Визуализация MRZ")
    st.markdown("Строка 1:", unsafe_allow_html=True)
    st.markdown(highlight_line1(line1), unsafe_allow_html=True)
    st.markdown("Строка 2:", unsafe_allow_html=True)
    st.markdown(highlight_line2(line2), unsafe_allow_html=True)
    st.markdown("Строка 3:", unsafe_allow_html=True)
    st.markdown(highlight_line3(line3), unsafe_allow_html=True)
    # Разбор
    doc_type = line1[0:2]
    country = line1[2:5]
    document_number = line1[5:14]
    optional_data_1 = line1[14:]
    birth_raw = line2[0:7]
    sex = line2[7]
    expiry_date = line2[8:14]
    expiry_check = line2[14]
    nationality = line2[15:18]
    optional_data_2 = line2[18:]
    parts = line3.split("<<")
    surname = parts[0]
    given_names = parts[1].replace("<", " ") if len(parts) > 1 else ""
    st.subheader("Расшифровка")
    st.write("Тип документа:", doc_type)
    st.write("Страна:", country)
    st.write("Номер:", document_number)
    st.write("Фамилия:", surname)
    st.write("Имя:", given_names)
    st.write("Пол:", sex)
    st.write("Гражданство:", nationality)
    st.write("Дата рождения (raw):", birth_raw)
    st.write("Срок действия:", expiry_date)
    st.write("Доп. данные 1:", split_optional(optional_data_1))
    st.write("Доп. данные 2:", split_optional(optional_data_2))