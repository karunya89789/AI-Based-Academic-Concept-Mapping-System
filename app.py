import time
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI-Based Academic Concept Mapping System",
    page_icon="🎓",
    layout="wide"
)

st.markdown("""
<style>
.title {
    text-align: center;
    color: #17365d;
    font-size: 36px;
    font-weight: bold;
}
.subtitle {
    text-align: center;
    color: #666;
    font-size: 18px;
    margin-bottom: 25px;
}
.topic {
    background: #eaf2f8;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    font-size: 26px;
    font-weight: bold;
    color: #17365d;
    margin: 20px 0;
}
.card {
    background: white;
    border: 1px solid #d5dce5;
    border-radius: 12px;
    padding: 20px;
    margin: 10px 0;
}
.card h3 {
    color: #17365d;
}
.footer {
    text-align: center;
    color: #777;
    margin-top: 35px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">AI-Based Academic Concept Mapping System</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered academic learning and concept organization system</div>',
    unsafe_allow_html=True
)

st.divider()

st.header("📚 About the System")

st.write(
    "This system uses Artificial Intelligence to organize an academic topic "
    "into meaningful concepts. Students can enter a topic and receive a "
    "structured concept map containing important academic information."
)

st.header("🔍 Enter Academic Topic")

topic = st.text_input(
    "Enter your topic",
    placeholder="Example: Artificial Intelligence"
)

if st.button("🧠 Generate AI Concept Map", type="primary"):

    if not topic.strip():
        st.warning("Please enter an academic topic.")
        st.stop()

    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except Exception:
        st.error("Gemini API key was not found.")
        st.stop()

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
You are an academic teaching assistant.

Create a clear academic concept map for:
{topic}

Use simple college-level English.

Return EXACTLY these sections:

INTRODUCTION:
Write one short paragraph.

CORE CONCEPTS:
Give 4 important concepts.
Format:
- Concept: explanation

TYPES:
Give 3 important types.
Format:
- Type: explanation

APPLICATIONS:
Give 4 important applications.
Format:
- Application: explanation

ADVANTAGES:
Give 4 short points.
Format:
- Point

CHALLENGES:
Give 4 short points.
Format:
- Point

FUTURE SCOPE:
Give 4 short points.
Format:
- Point

SUMMARY:
Write one short paragraph.

Do not add any other headings.
"""

        response = None

        with st.spinner("Generating concepts using Gemini..."):

            for attempt in range(3):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.8-flash",
                        contents=prompt
                    )
                    break

                except Exception as e:
                    if "503" in str(e) and attempt < 2:
                        time.sleep(5)
                    else:
                        raise e

        if not response or not response.text:
            st.error("Gemini did not return any information.")
            st.stop()

        text = response.text

        st.success("AI concept map generated successfully!")

        st.markdown(
            f'<div class="topic">📘 {topic}</div>',
            unsafe_allow_html=True
        )

        st.header("🧠 AI-Generated Concept Map")

        sections = [
            "INTRODUCTION:",
            "CORE CONCEPTS:",
            "TYPES:",
            "APPLICATIONS:",
            "ADVANTAGES:",
            "CHALLENGES:",
            "FUTURE SCOPE:",
            "SUMMARY:"
        ]

        parts = {}
        current = None

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            upper = line.upper()
            matched = False

            for section in sections:

                if upper.startswith(section):

                    current = section.replace(":", "")
                    parts[current] = []
                    matched = True
                    break

            if not matched and current:
                parts[current].append(line)

        for section in sections:

            name = section.replace(":", "")

            if name not in parts:
                continue

            st.markdown(
                f'<div class="card"><h3>{name.title()}</h3>',
                unsafe_allow_html=True
            )

            for item in parts[name]:

                item = item.lstrip("-•* ")

                if item:
                    st.write("• " + item)

            st.markdown("</div>", unsafe_allow_html=True)

    except Exception as e:

        if "503" in str(e):
            st.error(
                "Gemini is temporarily busy. Please try again after a few seconds."
            )
        else:
            st.error("Gemini generation failed.")
            st.code(str(e))

st.markdown(
    """
    <div class="footer">
    AI-Based Academic Concept Mapping System<br>
    Academic Project | Powered by Gemini AI
    </div>
    """,
    unsafe_allow_html=True
)
