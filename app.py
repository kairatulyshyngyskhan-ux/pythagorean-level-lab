import os
from typing import List

import streamlit as st
from google import genai
from google.genai import types
from pydantic import BaseModel, Field


# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Right Triangle Level Lab",
    page_icon="📐",
    layout="wide",
)


# =========================================================
# DESIGN
# =========================================================

st.markdown(
    """
    <style>
    .stApp {
        background: #f7faf9;
    }

    .block-container {
        max-width: 1120px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    h1, h2, h3 {
        color: #173f3a !important;
    }

    .hero {
        padding: 1.1rem 1.25rem;
        border: 1px solid #d9e7e3;
        border-radius: 18px;
        background: linear-gradient(
            90deg,
            #eef9f5 0%,
            #fff8ea 100%
        );
        color: #24433f;
        margin-bottom: 1.3rem;
    }

    .level-card {
        min-height: 150px;
        padding: 1.1rem;
        border: 1px solid #d9e4e1;
        border-radius: 18px;
        background: white;
        color: #263c39;
    }

    .level-card h3 {
        margin-top: 0;
    }

    .result-card {
        padding: 1.2rem 1.3rem;
        border: 1px solid #d7e5e1;
        border-radius: 18px;
        background: white;
        color: #223a36;
        margin-top: .6rem;
    }

    .small-muted {
        color: #667b77;
        font-size: .94rem;
    }

    div[data-testid="stSidebar"] {
        background: #172522;
    }

    div[data-testid="stSidebar"] * {
        color: #f4f7f6;
    }

    div[data-testid="stSidebar"] input,
    div[data-testid="stSidebar"] textarea {
        color: #172522 !important;
        background: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# GEMINI RESPONSE FORMAT
# =========================================================

class AdaptedTask(BaseModel):
    title: str = Field(
        description="Short title for the adapted task."
    )

    problem: str = Field(
        description="The adapted student problem."
    )

    hint: str = Field(
        description="A useful hint without immediately giving the answer."
    )

    solution_steps: List[str] = Field(
        description="Clear step-by-step solution."
    )

    final_answer: str = Field(
        description="Final mathematical answer."
    )

    why_this_level: str = Field(
        description="Why this task fits the selected level."
    )


# =========================================================
# API KEY
# =========================================================

def get_api_key():
    try:
        return st.secrets["GEMINI_API_KEY"]
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


# =========================================================
# GEMINI GENERATION
# =========================================================

def generate_with_gemini(
    api_key,
    level,
    grade,
    unit,
    core_problem,
    learning_goal
):

    client = genai.Client(api_key=api_key)

    level_rules = {

        "Foundation": """
        Use simple and friendly numbers.
        Give strong scaffolding.
        Give a direct but useful hint.
        Use short solution steps.
        Prefer familiar Pythagorean triples when possible.
        """,

        "Standard": """
        Keep normal grade-level difficulty.
        Give moderate support.
        The student should decide how to use
        the Pythagorean theorem.
        """,

        "Advanced": """
        Add a realistic context or an extra reasoning step.
        Do not make the problem difficult only
        by using large or ugly numbers.
        Require deeper mathematical reasoning.
        """
    }

    prompt = f"""
You are a mathematics teacher creating
differentiated learning tasks.

TOPIC:
Pythagorean theorem

TARGET GROUP:
{grade}

UNIT:
{unit}

SELECTED LEVEL:
{level}

CORE PROBLEM:
{core_problem}

LEARNING GOAL:
{learning_goal}

Important mathematics:

- Work only with right triangles.
- The hypotenuse is side c.
- The hypotenuse is opposite the 90-degree angle.
- Use a² + b² = c² correctly.
- Check all calculations.
- Keep the same mathematical learning goal.
- Change the difficulty, support and reasoning
  according to the selected level.

LEVEL RULES:

{level_rules[level]}

Write clear student-friendly English.

Do not mention that you are an AI.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=AdaptedTask,
        ),
    )

    if response.parsed:
        return response.parsed

    return AdaptedTask.model_validate_json(
        response.text
    )


# =========================================================
# FALLBACK TASKS
# =========================================================

def fallback_task(level, unit):

    examples = {

        "Foundation": AdaptedTask(

            title="Find the missing side",

            problem=(
                f"A right triangle has legs "
                f"3 {unit} and 4 {unit}. "
                f"Find the hypotenuse c."
            ),

            hint=(
                "The side opposite the 90° angle is c. "
                "Use a² + b² = c²."
            ),

            solution_steps=[
                "Write a² + b² = c².",
                "Substitute: 3² + 4² = c².",
                "Calculate: 9 + 16 = 25.",
                "Take the square root: c = 5."
            ],

            final_answer=f"c = 5 {unit}",

            why_this_level=(
                "It uses a familiar 3-4-5 triangle "
                "and gives direct guidance."
            )
        ),

        "Standard": AdaptedTask(

            title="Use the Pythagorean theorem",

            problem=(
                f"A right triangle has legs "
                f"6 {unit} and 8 {unit}. "
                f"Find the hypotenuse."
            ),

            hint=(
                "Identify the side opposite the "
                "90° angle and use a² + b² = c²."
            ),

            solution_steps=[
                "Let a = 6 and b = 8.",
                "6² + 8² = c².",
                "36 + 64 = 100.",
                "Therefore c = 10."
            ],

            final_answer=f"c = 10 {unit}",

            why_this_level=(
                "It is a normal curriculum-level "
                "problem with moderate support."
            )
        ),

        "Advanced": AdaptedTask(

            title="Diagonal path",

            problem=(
                f"A rectangular garden is "
                f"9 {unit} wide and 12 {unit} long. "
                f"A straight path goes from one corner "
                f"to the opposite corner. "
                f"Find the length of the path."
            ),

            hint=(
                "The length and width form the two "
                "legs of a right triangle. "
                "The diagonal is the hypotenuse."
            ),

            solution_steps=[
                "Model the diagonal as c.",
                "Use 9² + 12² = c².",
                "81 + 144 = 225.",
                "Therefore c = 15."
            ],

            final_answer=f"15 {unit}",

            why_this_level=(
                "The student must first model a "
                "real situation as a right triangle."
            )
        )
    }

    return examples[level]


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("Teacher settings")

    grade = st.selectbox(
        "Target group",
        [
            "Grade 7",
            "Grade 8",
            "Grade 9"
        ],
        index=1
    )

    unit = st.selectbox(
        "Unit",
        [
            "cm",
            "m",
            "km"
        ],
        index=0
    )

    st.divider()

    st.caption(
        "The same core idea is adapted by changing "
        "scaffolding, context, and reasoning demand."
    )

    api_key = get_api_key()

    if api_key:
        st.success("Gemini AI connected")
        st.caption("Live AI generation is enabled.")
    else:
        st.info(
            "Demo mode: add GEMINI_API_KEY "
            "in Streamlit Secrets."
        )


# =========================================================
# MAIN PAGE
# =========================================================

st.title("📐 Right Triangle Level Lab")

st.markdown(
    """
    <p class="small-muted">
    One Pythagorean theorem task.
    Three levels of support.
    Choose the version that fits the learner.
    </p>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero">

    <b>Core idea:</b>

    In a right triangle, the two legs and the
    hypotenuse are connected by

    <b>a² + b² = c²</b>.

    Side <b>c</b> is always opposite the
    <b>90° angle</b>.

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CORE PROBLEM
# =========================================================

left, right = st.columns(
    [1.25, 1]
)

with left:

    st.subheader("Core problem")

    core_problem = st.text_area(
        "Core problem",
        value=(
            "A right triangle has legs 6 cm and 8 cm. "
            "Find the hypotenuse."
        ),
        height=110,
        label_visibility="collapsed"
    )

    learning_goal = st.text_input(
        "Learning goal",
        value=(
            "Students use the Pythagorean theorem "
            "and correctly identify the hypotenuse."
        )
    )


with right:

    st.subheader("Quick visual")

    st.code(
        """
        c (hypotenuse)
       /|
      / |
     /  | b
    /   |
   /____|
     a   90°
        """,
        language=None
    )

    st.caption(
        "c is opposite the 90° angle."
    )


# =========================================================
# LEVEL CARDS
# =========================================================

st.subheader(
    "Choose learner level"
)

c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        """
        <div class="level-card">

        <h3>🌱 Foundation</h3>

        <p>
        Simple numbers,
        guided steps,
        direct hints.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="level-card">

        <h3>📘 Standard</h3>

        <p>
        Normal curriculum-level
        problem solving.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="level-card">

        <h3>🚀 Advanced</h3>

        <p>
        Real-world context
        and deeper reasoning.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


level = st.radio(
    "Learner level",
    [
        "Foundation",
        "Standard",
        "Advanced"
    ],
    horizontal=True,
    label_visibility="collapsed"
)


# =========================================================
# GENERATE BUTTON
# =========================================================

if st.button(
    "Generate my adapted task",
    type="primary",
    use_container_width=True
):

    with st.spinner(
        "Adapting the task..."
    ):

        if api_key:

            try:

                task = generate_with_gemini(
                    api_key=api_key,
                    level=level,
                    grade=grade,
                    unit=unit,
                    core_problem=core_problem,
                    learning_goal=learning_goal
                )

                st.session_state["task"] = task

                st.session_state["source"] = (
                    "Gemini AI"
                )

                st.session_state["generated_level"] = (
                    level
                )

            except Exception as exc:

                st.error(
                    "Gemini request failed. "
                    "Check your API key and free-tier quota."
                )

                st.caption(
                    f"Technical detail: {exc}"
                )

        else:

            task = fallback_task(
                level,
                unit
            )

            st.session_state["task"] = task

            st.session_state["source"] = (
                "Built-in demo"
            )

            st.session_state["generated_level"] = (
                level
            )


# =========================================================
# SHOW RESULT
# =========================================================

if "task" in st.session_state:

    task = st.session_state["task"]

    source = st.session_state.get(
        "source",
        ""
    )

    generated_level = st.session_state.get(
        "generated_level",
        level
    )

    st.divider()

    st.subheader(
        f"{generated_level} result"
    )

    st.caption(
        f"Generated with: {source}"
    )

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True
    )

    st.markdown(
        f"### {task.title}"
    )

    st.markdown(
        "**Problem**"
    )

    st.write(
        task.problem
    )


    st.markdown(
        "**Hint**"
    )

    st.info(
        task.hint
    )


    st.markdown(
        "**Solution**"
    )

    for i, step in enumerate(
        task.solution_steps,
        start=1
    ):

        st.write(
            f"{i}. {step}"
        )


    st.success(
        f"Final answer: {task.final_answer}"
    )


    st.markdown(
        "**Why this level?**"
    )

    st.write(
        task.why_this_level
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "Differentiation changes support and reasoning "
    "demand while keeping the same mathematical objective."
)
