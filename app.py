import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="Right Triangle Level Lab",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    .stApp {background: #f7faf9;}
    .main-title {
        font-size: 2.35rem;
        font-weight: 800;
        color: #183b36;
        margin-bottom: .15rem;
    }
    .sub-title {
        color: #58706c;
        font-size: 1.05rem;
        margin-bottom: 1.4rem;
    }
    .hero {
        background: linear-gradient(135deg, #e8f5f1 0%, #fff6e8 100%);
        border: 1px solid #d7e9e4;
        border-radius: 22px;
        padding: 1.35rem 1.5rem;
        margin-bottom: 1rem;
    }
    .level-card {
        border: 1px solid #dbe7e4;
        border-radius: 16px;
        padding: 1rem;
        min-height: 150px;
        background: white;
    }
    .small-note {
        color: #667975;
        font-size: .9rem;
    }
    div[data-testid="stButton"] button {
        border-radius: 12px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Helpers ----------
def get_api_key():
    try:
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return os.getenv("OPENAI_API_KEY")


def fallback(level: str, unit: str):
    if level == "Foundation":
        return f"""
### Adapted task
A right triangle has legs **3 {unit}** and **4 {unit}**. Find the hypotenuse.

### Hint
The hypotenuse is the side opposite the 90° angle. Use **a² + b² = c²**.

### Guided solution
1. Substitute the legs: **3² + 4² = c²**  
2. Calculate: **9 + 16 = 25**  
3. So **c = √25 = 5 {unit}**.

### Check yourself
Why must **c** be the longest side?
"""
    if level == "Advanced":
        return f"""
### Adapted task
A rectangular garden is **9 {unit}** wide and **12 {unit}** long. A student walks directly from one corner to the opposite corner.  
**a)** Find the diagonal distance.  
**b)** Compare the diagonal with walking along two sides of the garden. How much distance is saved?

### Hint
The width and length form the two legs of a right triangle. The diagonal is the hypotenuse.

### Solution
**a)** d² = 9² + 12² = 81 + 144 = 225, so **d = 15 {unit}**.  
**b)** Along two sides: 9 + 12 = 21 {unit}.  
Distance saved: 21 − 15 = **6 {unit}**.

### Extension
Explain why the direct diagonal route must be shorter than walking along two sides.
"""
    return f"""
### Adapted task
A right triangle has legs **6 {unit}** and **8 {unit}**. Find the hypotenuse and show your working.

### Hint
Identify the hypotenuse first, then use **a² + b² = c²**.

### Solution
6² + 8² = c²  
36 + 64 = c²  
100 = c²  
**c = 10 {unit}**.

### Quick check
Does your answer make sense compared with the two leg lengths?
"""


def build_prompt(level, grade, core_problem, learning_goal, unit):
    level_rules = {
        "Foundation": "Use friendly numbers, a simple context, strong scaffolding, and a direct hint. Prefer a 3-4-5 triangle when appropriate.",
        "Standard": "Keep normal grade-level difficulty. Require students to identify the hypotenuse and show standard working.",
        "Advanced": "Keep the same concept but add a realistic multi-step extension, comparison, or reasoning question. Do not make it advanced by numbers alone.",
    }
    return f"""
You are a mathematics teacher creating differentiated learning material.

Core topic: Pythagorean theorem
Target group: {grade}
Learning goal: {learning_goal}
Core problem: {core_problem}
Selected level: {level}
Preferred unit: {unit}

Adapt the SAME core mathematical idea to the selected learner level.
{level_rules[level]}

Return the response in clear student-friendly English using exactly these headings:
### Adapted task
### Hint
### Solution
### Check yourself

Requirements:
- Keep the mathematics correct.
- Make it easy to read.
- Clearly identify that the hypotenuse is opposite the 90° angle.
- Use the Pythagorean theorem correctly.
- Keep the whole response under 250 words.
"""


def generate_with_ai(prompt):
    key = get_api_key()
    if not key:
        return None
    client = OpenAI(api_key=key)
    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt,
    )
    return response.output_text


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Teacher settings")
    grade = st.selectbox("Target group", ["Grade 7", "Grade 8", "Grade 9"], index=1)
    unit = st.selectbox("Unit", ["cm", "m", "km"], index=0)
    st.markdown("---")
    st.caption("The same core idea is adapted by changing scaffolding, context, and reasoning demand.")
    api_ready = bool(get_api_key())
    st.success("AI connected") if api_ready else st.info("Demo mode: add OPENAI_API_KEY in Streamlit Secrets for live AI.")

# ---------- Main ----------
st.markdown('<div class="main-title">📐 Right Triangle Level Lab</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">One Pythagorean theorem task. Three levels of support. Choose the version that fits the learner.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <b>Core idea:</b> in a right triangle, the two legs and the hypotenuse are connected by
      <b>a² + b² = c²</b>. The side <b>c</b> is always opposite the 90° angle.
    </div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.2, 1])
with left:
    st.subheader("Core problem")
    core_problem = st.text_area(
        "Edit the original task if you want:",
        "A right triangle has legs 6 cm and 8 cm. Find the hypotenuse.",
        height=110,
    )
    learning_goal = st.text_input(
        "Learning goal",
        "Students use the Pythagorean theorem and correctly identify the hypotenuse.",
    )

with right:
    st.subheader("Quick visual")
    st.markdown(
        """
        ```text
             c (hypotenuse)
            /|
           / |
          /  | b
         /   |
        /____|
          a   90°
        ```
        **Remember:** the hypotenuse is opposite the **90°** angle.
        """
    )

st.subheader("Choose a learning level")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="level-card"><h4>🌱 Foundation</h4><p>Simple numbers, guided steps, direct hints.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="level-card"><h4>📘 Standard</h4><p>Normal curriculum-level problem solving.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="level-card"><h4>🚀 Advanced</h4><p>Real-world context and multi-step reasoning.</p></div>', unsafe_allow_html=True)

level = st.radio(
    "Difficulty",
    ["Foundation", "Standard", "Advanced"],
    horizontal=True,
    label_visibility="collapsed",
)

if st.button("Generate my adapted task", type="primary", use_container_width=True):
    with st.spinner("Adapting the task..."):
        prompt = build_prompt(level, grade, core_problem, learning_goal, unit)
        try:
            output = generate_with_ai(prompt)
        except Exception as e:
            output = None
            st.warning("The live AI request was unavailable, so the built-in checked example is shown instead.")
        if not output:
            output = fallback(level, unit)
        st.session_state["output"] = output
        st.session_state["last_level"] = level

if "output" in st.session_state:
    st.markdown("---")
    st.subheader(f"{st.session_state['last_level']} version")
    st.markdown(st.session_state["output"])

    with st.expander("Why is this differentiated?"):
        explanations = {
            "Foundation": "The mathematics is the same, but the numbers and hint structure reduce cognitive load and give the learner a clear entry point.",
            "Standard": "The student receives the expected grade-level task with enough information to solve independently.",
            "Advanced": "The student applies the same theorem in a richer situation and must connect more than one step or justify a conclusion.",
        }
        st.write(explanations[st.session_state["last_level"]])

st.markdown("---")
st.caption("Built for Educational Technology & AI • Differentiated Learning • Pythagorean Theorem")
