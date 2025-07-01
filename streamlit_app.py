import streamlit as st
import google.generativeai as genai

# Configure the Gemini API
# Replace with your actual API key
# For security, it's recommended to use Streamlit's secrets management
try:
    from google.colab import userdata
    api_key = userdata.get('GEMINI_API_KEY')
except ImportError:
    api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def generate_content(prompt):
    """Generates content using the Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

st.set_page_config(layout="wide")

st.title("🐍 Interactive Python Tutorial")
st.write("Learn Python from scratch with detailed notes, runnable code examples, and interactive quizzes.")

# --- Sidebar for Topic Selection ---
st.sidebar.title("Topics")
topic = st.sidebar.selectbox(
    "Choose a topic to learn:",
    [
        "Python HOME", "Python Intro", "Python Get Started", "Python Syntax",
        "Python Comments", "Python Variables", "Python Data Types", "Python Numbers",
        "Python Casting", "Python Strings", "Python Booleans", "Python Operators",
        "Python Lists", "Python Tuples", "Python Sets", "Python Dictionaries",
        "Python If...Else", "Python Match", "Python While Loops", "Python For Loops",
        "Python Functions", "Python Lambda", "Python Arrays", "Python OOP",
        "Python Classes/Objects", "Python Inheritance", "Python Iterators",
        "Python Polymorphism", "Python Scope", "Python Modules", "Python Dates",
        "Python Math", "Python JSON", "Python RegEx", "Python PIP", "Python Try...Except",
        "Python String Formatting", "Python User Input", "Python VirtualEnv",
        "Python File Handling", "Python Read Files", "Python Write/Create Files",
        "Python Delete Files", "NumPy Tutorial", "Pandas Tutorial"
    ]
)

# --- Main Content Area ---
if topic:
    st.header(f"Learn: {topic}")

    # Generate and display detailed notes
    with st.spinner(f"Generating notes for {topic}..."):
        notes_prompt = f"""
        Generate a detailed, summary-style note for the Python topic: '{topic}'.
        Cover all key concepts within this topic.
        Use Markdown for formatting.
        """
        notes = generate_content(notes_prompt)
        st.markdown(notes)

    # Generate and display code examples
    st.subheader("Code Examples")
    with st.spinner("Generating code examples..."):
        examples_prompt = f"""
        Provide 5 runnable Python code examples for the topic: '{topic}'.
        For each example, include a brief explanation.
        Format the output as a numbered list with code blocks.
        """
        examples = generate_content(examples_prompt)
        st.markdown(examples)

    # Interactive code editor
    st.subheader("Try it Yourself!")
    code = st.text_area("Write your Python code here:", height=200)
    if st.button("Run Code"):
        if code:
            try:
                # Using exec to run the code and capture output
                import io
                from contextlib import redirect_stdout

                f = io.StringIO()
                with redirect_stdout(f):
                    exec(code)
                output = f.getvalue()
                st.text_area("Output:", value=output, height=150, disabled=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter some code to run.")

    # Generate and display MCQs
    st.subheader("Test Your Knowledge")
    with st.spinner("Generating multiple-choice questions..."):
        mcq_prompt = f"""
        Create 5 multiple-choice questions for the Python topic: '{topic}'.
        For each question, provide 4 options and indicate the correct answer.
        Format as a numbered list.
        """
        mcqs_text = generate_content(mcq_prompt)
        st.markdown(mcqs_text)

    # Interactive MCQ validation
    st.subheader("MCQ Practice")
    mcq_answers = st.text_input("Enter your answers for the MCQs above (e.g., 1A, 2B, 3C):")
    if st.button("Check Answers"):
        # This is a simplified validation. A more robust solution would parse the generated MCQs.
        st.info("Answer validation is a complex feature and this is a simplified example.")
        # In a real app, you would parse the generated MCQs and their answers for validation.
        # For now, we'll just show a success message.
        st.success("Answers submitted! In a full app, you'd get detailed feedback here.")

    # Coding practice
    st.subheader("Coding Practice")
    with st.spinner("Generating a coding practice problem..."):
        practice_prompt = f"""
        Create a simple coding practice problem related to the Python topic: '{topic}'.
        Include the problem description and a hint.
        """
        practice_problem = generate_content(practice_prompt)
        st.markdown(practice_problem)

    practice_code = st.text_area("Your solution:", height=200)
    if st.button("Submit Solution"):
        if practice_code:
            st.success("Solution submitted! In a real application, this would be tested against predefined test cases.")
        else:
            st.warning("Please enter your solution.")
