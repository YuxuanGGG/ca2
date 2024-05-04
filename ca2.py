import streamlit as st
import time
import re
import logging
import logging.handlers

def setup_papertrail_logging():
    papertrail_handler = logging.handlers.SysLogHandler(address=('logs5.papertrailapp.com', 20304))
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
    papertrail_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(papertrail_handler)
    return logger

logger = setup_papertrail_logging()

st.sidebar.header("Hinweis zu den Stichwörtern:")
st.sidebar.markdown("""
1. Präventive Maßnahmen diskutieren
2. Empfohlene Salzaufnahme
3. Empfehlungen für Gemüse und Obst
4. Empfehlungen zur Trainingshäufigkeit
5. Schrittweise Integration von Übungen
6. Abschluss
""")

st.sidebar.header("Hinweis zum Format:")
st.sidebar.markdown("""
Stichwörter: Text.

Zum Beispiel:
- **Präventive Maßnahmen diskutieren**: Ich leide in meiner Familie an Bluthochdruck und hätte gerne Ratschläge zur Vorbeugung.
""", unsafe_allow_html=True)

st.sidebar.header("Persona: Jim")
st.sidebar.markdown("""
- Alter: 30 Jahre
- Beruf: Büroangestellter
- Gesundheitszustand: Familiäre Vorgeschichte von Bluthochdruck
- Ernährungsgewohnheiten:
    - Mag keine zu salzigen Speisen
    - Isst ungern Gemüse und Obst
    - Liebt Fleisch
- Aktivitätslevel:
    - Geht am Wochenende bei gutem Wetter spazieren
    - Fühlt sich oft nach der Arbeit angestrengt
""")

keyword_to_response = {
    'präventive maßnahmen diskutieren:|präventive maßnahmen diskutieren': "Verstanden. Ich würde gerne mehr über Ihre Lebensgewohnheiten erfahren. Wie ernähren Sie sich? Wie viel Salz nehmen Sie beispielweise täglich zu sich?",
    "empfohlene salzaufnahme:|empfohlene salzaufnahme": "Verstehe. Ich empfehle Ihnen, die tägliche Salzaufnahme auf maximal 5 Gramm zu beschränken, was etwa einem Teelöffel entspricht. Wie ist außerdem das Verhältnis von Obst, Gemüse und Fetten in Ihrer täglichen Ernährung?",
    "empfehlungen für gemüse und obst:|empfehlungen für gemüse und obst": "Ich verstehe, und empfehle Ihnen, mehr frisches Gemüse und Obst zu essen. Bei der Auswahl von Fleischprodukten sollten Sie sich auf hochwertige Fette konzentrieren. Bewegen Sie sich regelmäßig oder treiben Sie Sport?",
    "empfehlungen zur trainingshäufigkeit:|empfehlungen zur trainingshäufigkeit": "Verstanden. Ich würde Ihnen empfehlen, drei Mal pro Woche für 30 bis 45 Minuten ein regelmäßiges Ausdauertraining zu absolvieren. Gibt es bestimmte Zeiten, die für Sie am besten wären, um das Training in Ihren Alltag einzuplanen? Beispielsweise nach der Arbeit?",
    "schrittweise integration von übungen:|schrittweise integration von übungen": "Das verstehe ich. Ich empfehle Ihnen, die körperliche Aktivität schrittweise in Ihren Alltag zu integrieren. Kann ich Ihnen noch mit etwas anderem behilflich sein?",
    "abschluss:|abschluss": "Kein Problem. Bitte beachten Sie, dass meine Antworten nur Vorschläge sind. Ich wünsche Ihnen gute Gesundheit!"
}

st.title("Medical AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Guten Tag! Wir wissen, dass die familiäre Vorgeschichte die Gesundheit einer Person beeinflussen kann. Die Anpassung von Lebensgewohnheiten ist der Schlüssel zur Krankheitsprävention. Hat Ihre Familie ähnliche Gesundheitsprobleme? Haben Sie darüber nachgedacht, wie Sie durch die Verbesserung Ihrer täglichen Gewohnheiten Ihre Gesundheit optimieren können?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "last_input" not in st.session_state:
    st.session_state.last_input = ""
    
if prompt := st.chat_input("Bitte geben Sie Ihren Text im richtigen Format ein."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    logger.info(f"User input logged: {prompt}")  # 标注 - 添加这行代码来调用记录函数

    found_response = False
    for pattern, response in keyword_to_response.items():
        if re.search(pattern, prompt.lower()):
            assistant_response = response
            found_response = True
            break
    if not found_response:
        assistant_response = "Es tut mir leid, ich kann Ihre Eingabe nicht verarbeiten."

    time.sleep(2)
    response_placeholder = st.empty()

    current_text = ""
    for word in assistant_response.split():
        current_text += word + " "
        response_placeholder.text(current_text)
        time.sleep(0.05)  # Delay for 0.5 seconds between words
    response_placeholder.empty()
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
