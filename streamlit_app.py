import streamlit as st
import requests
import json
import time

# --- Page and API Configuration ---
st.set_page_config(
    page_title="PyLearn AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# IMPORTANT: Replace with your actual Google AI Studio API key
# For better security, use Streamlit secrets: st.secrets["API_KEY"]
API_KEY = st.secrets["GOOGLE_API_KEY"]

# --- Data for Topics (Expanded Curriculum) ---
TOPICS = {
    "Python Fundamentals": {
        "icon": "📘",
        "subtopics": [
            "Introduction & Setup", "Basic Syntax & print()", "Keywords & Identifiers", "Comments & Docstrings",
            "Variables & Assignment", "Core Data Types", "Type Casting", "Arithmetic Operators", "Assignment Operators",
            "Comparison & Logical Operators", "Identity & Membership Operators", "Bitwise Operators", "Strings",
            "Lists", "Tuples", "Dictionaries", "Sets", "Bytes & Bytearray", "Conditional Statements (if/elif/else)",
            "for Loops", "while Loops", "Loop Control (break/continue/pass)", "Defining Functions",
            "Function Arguments (*args, **kwargs)", "Return Statement & Scope", "Lambda Functions", "Modules & Imports",
            "The input() Function", "File Handling (with statement)", "Reading & Writing Files", "Exception Handling (try/except)"
        ],
    },
    "Intermediate Python": {
        "icon": "🧠",
        "subtopics": [
            "OOP - Classes & Objects", "OOP - __init__ & Attributes", "OOP - Methods", "Encapsulation", "Inheritance",
            "Polymorphism & Overriding", "Abstraction & Dunder Methods", "collections Module", "map() Function", "filter() Function",
            "reduce() Function", "List Comprehensions", "Dictionary & Set Comprehensions", "Iterators & Generators",
            "Generator Expressions", "Regular Expressions (re module)", "datetime Module", "calendar Module",
            "JSON Serialization", "Pickle Serialization", "Decorators", "Context Managers (with)"
        ],
    },
    "Advanced Python": {
        "icon": "💻",
        "subtopics": [
            "Threading", "Multiprocessing", "The GIL", "Asynchronous Programming (asyncio)", "Coroutines (async/await)",
            "Type Hints & Static Analysis", "Descriptors", "__slots__", "Metaclasses", "Unit Testing (unittest/pytest)",
            "Debugging with pdb", "Code Profiling (cProfile)", "Partial Functions", "__new__ vs __init__", "Weak References",
            "eval() and exec()", "C Interoperability (ctypes)", "Writing C Extensions", "Common Design Patterns",
            "Memory Management & Garbage Collection", "Packaging & Distribution (PyPI)"
        ],
    },
    "Data Structures: Linear": {
        "icon": "⛓️",
        "subtopics": [
            "Arrays & Lists: list (Dynamic Array)", "Arrays & Lists: tuple (Immutable Array)", "Arrays & Lists: array.array (Typed Array)", "Arrays & Lists: str (String / Character Array)", "Arrays & Lists: bytes", "Arrays & Lists: bytearray",
            "Linked Lists: Singly Linked List", "Linked Lists: Doubly Linked List", "Linked Lists: Circular Linked List", "Linked Lists: Skip List", "Linked Lists: XOR Linked List", "Linked Lists: Self-Organizing List", "Linked Lists: Unrolled Linked List",
            "Stacks (LIFO): Implementation via list", "Stacks (LIFO): Implementation via collections.deque", "Stacks (LIFO): queue.LifoQueue",
            "Queues (FIFO): Implementation via collections.deque", "Queues (FIFO): queue.Queue", "Queues (FIFO): multiprocessing.Queue", "Queues (FIFO): Double-Ended Queue (deque)", "Queues (FIFO): Circular Queue",
            "Hash-Based: dict (Hash Map)", "Hash-Based: set", "Hash-Based: frozenset", "Hash-Based: collections.Counter", "Hash-Based: collections.defaultdict", "Hash-Based: collections.OrderedDict", "Hash-Based: collections.ChainMap"
        ]
    },
    "Data Structures: Trees": {
        "icon": "🌳",
        "subtopics": [
            "General Trees: N-ary Tree",
            "Binary Trees: Full, Complete, Perfect", "Binary Trees: Balanced & Degenerate",
            "Binary Search Trees (BSTs)", "BSTs: Cartesian Tree & Treap",
            "Self-Balancing BSTs: AVL Tree", "Self-Balancing BSTs: Red-Black Tree", "Self-Balancing BSTs: Splay Tree", "Self-Balancing BSTs: Scapegoat Tree",
            "Heaps (Priority Queues): Binary Heap (heapq)", "Heaps: Min-Heap & Max-Heap", "Heaps: Binomial Heap", "Heaps: Fibonacci Heap",
            "Tries (Prefix Trees): Standard Trie", "Tries: Ternary Search Tree", "Tries: Palindromic Tree",
            "Segment/Interval: Segment Tree", "Segment/Interval: Fenwick Tree (BIT)", "Segment/Interval: Interval Tree", "Segment/Interval: K-D Tree",
            "Multiway Trees: B-Tree & B+ Tree",
            "Suffix Structures: Suffix Tree", "Suffix Structures: Suffix Automaton", "Suffix Structures: Suffix Array"
        ]
    },
    "Data Structures: Graphs & Other": {
        "icon": "🕸️",
        "subtopics": [
            "Graph Representations: Adjacency List", "Graph Representations: Adjacency Matrix", "Graph Representations: Incidence Matrix",
            "Specialized Graphs: Gomory-Hu Tree",
            "Advanced: Disjoint Set Union (DSU)", "Advanced: Bloom Filter", "Advanced: Sparse Table", "Advanced: Sparse Set", "Advanced: Rope", "Advanced: BK-Tree", "Advanced: Persistent Data Structures"
        ]
    },
    "Algorithms: Sorting & Searching": {
        "icon": "🔢",
        "subtopics": [
            "Sorting: Bubble Sort", "Sorting: Selection Sort", "Sorting: Insertion Sort", "Sorting: Merge Sort", "Sorting: Quick Sort", "Sorting: Heap Sort",
            "Sorting: Timsort (Python's default)", "Sorting: Radix Sort", "Sorting: Counting Sort", "Sorting: Bucket Sort", "Sorting: Shell Sort",
            "Searching: Linear Search", "Searching: Binary Search (bisect)", "Searching: Jump Search", "Searching: Interpolation Search", "Searching: Exponential Search", "Searching: Ternary Search"
        ]
    },
    "Algorithms: Graphs": {
        "icon": "📈",
        "subtopics": [
            "Graph Traversal: Breadth-First Search (BFS)", "Graph Traversal: Depth-First Search (DFS)",
            "Shortest Path: Dijkstra's Algorithm", "Shortest Path: A* Search", "Shortest Path: Bellman-Ford", "Shortest Path: Floyd-Warshall (All-Pairs)", "Shortest Path: Johnson's Algorithm (All-Pairs)",
            "Minimum Spanning Tree (MST): Kruskal's", "Minimum Spanning Tree (MST): Prim's", "Minimum Spanning Tree (MST): Borůvka's",
            "Connectivity: Strongly Connected Components (Tarjan's)", "Connectivity: Bridges & Articulation Points",
            "Network Flow: Ford-Fulkerson & Edmonds-Karp", "Network Flow: Dinic's Algorithm",
            "Cycles: Cycle Detection",
            "Matching: Hopcroft–Karp (Bipartite)", "Matching: Hungarian Algorithm",
            "Other: Topological Sort", "Other: Graph Coloring", "Other: Lowest Common Ancestor (LCA)"
        ]
    },
     "Algorithms: Paradigms & Techniques": {
        "icon": "💡",
        "subtopics": [
            "Paradigms: Brute Force", "Paradigms: Greedy Algorithms", "Paradigms: Divide and Conquer",
            "Dynamic Programming: Memoization (Top-down)", "Dynamic Programming: Tabulation (Bottom-up)", "Dynamic Programming: Knuth's Optimization",
            "Paradigms: Backtracking", "Paradigms: Randomized Algorithms",
            "String: Naive Search", "String: KMP Algorithm", "String: Boyer-Moore", "String: Rabin-Karp", "String: Aho-Corasick",
            "String: Longest Common Subsequence (LCS)", "String: Longest Common Substring", "String: Edit Distance (Levenshtein)", "String: Manacher's Algorithm", "String: Z-algorithm",
            "Techniques: Bit Manipulation / Bitmasking", "Techniques: Sliding Window", "Techniques: Two Pointers", "Techniques: Mo's Algorithm", "Techniques: Square Root Decomposition", "Techniques: Heavy-Light Decomposition", "Techniques: Meet-in-the-Middle"
        ]
    },
    "Algorithms: Mathematical": {
        "icon": "♾️",
        "subtopics": [
            "Prime Numbers: Primality Tests (Fermat, Miller-Rabin)", "Prime Numbers: Sieve of Eratosthenes", "Prime Numbers: Segmented Sieve",
            "GCD: Euclidean Algorithm", "GCD: Extended Euclidean Algorithm",
            "Modular Arithmetic: Modular Exponentiation", "Modular Arithmetic: Modular Multiplicative Inverse", "Modular Arithmetic: Chinese Remainder Theorem",
            "Matrix Exponentiation", "Factorial of Large Numbers", "Gaussian Elimination",
            "Computational Geometry: Convex Hull", "Computational Geometry: Line Intersection", "Computational Geometry: Closest Pair of Points"
        ]
    }
}


# --- Custom Styling ---
st.markdown("""
<style>
    /* Main app theming */
    .stApp {
        background-color: #0f172a; /* slate-900 */
    }
    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
    }
    /* Welcome message */
    .welcome-text {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        padding: 2rem;
    }
    /* Markdown styling */
    .stMarkdown h1 {
        border-bottom: 2px solid #334155;
        padding-bottom: 0.5rem;
    }
    .stMarkdown h2 {
        border-bottom: 1px solid #334155;
        padding-bottom: 0.3rem;
    }
    code {
        background-color: rgba(168, 85, 247, 0.2); /* purple-500/20 */
        color: #d8b4fe; /* purple-300 */
        padding: 0.2rem 0.4rem;
        border-radius: 0.3rem;
        font-family: 'monospace';
    }
    pre code {
        background-color: transparent;
        padding: 0;
    }
    /* Problem card styling */
    .problem-card {
        background-color: #1e293b; /* slate-800 */
        border: 1px solid #334155;
        border-radius: 0.75rem;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    /* Correct/Incorrect answer boxes */
    .correct-answer {
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.5);
        color: #4ade80;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
    .incorrect-answer {
        background-color: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.5);
        color: #f87171;
        padding: 0.75rem;
        border-radius: 0.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# --- API Call Logic ---
def fetch_api_content(prompt, content_type="course"):
    """Generic function to fetch content from the Google AI API."""
    if API_KEY == "YOUR_API_KEY_HERE" or not API_KEY:
        st.error("Please add your Google AI Studio API key to Streamlit secrets (st.secrets['GOOGLE_API_KEY']).")
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"role": "user", "parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception for 4XX or 5XX status codes

        result = response.json()
        if "candidates" in result and result["candidates"]:
            text_content = result["candidates"][0]["content"]["parts"][0]["text"]
            return text_content
        else:
            st.error(f"Failed to fetch {content_type}. The API returned an empty or invalid response.")
            st.write("API Response:", result) # For debugging
            return None

    except requests.exceptions.HTTPError as http_err:
        st.error(f"API Error ({http_err.response.status_code}): Could not fetch {content_type}. Please check your API key and network connection.")
        st.write(http_err.response.json()) # Show detailed error from API
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

def get_course_content(topic):
    prompt = f'I need a very detailed, well-structured explanation on the Python topic: "{topic}". The explanation should cover all concepts from basics to advanced. Use markdown for all formatting. CRITICAL: For each concept, provide multiple, varied, and practical code examples in Python to illustrate the point clearly. Use markdown code blocks for all examples.'
    return fetch_api_content(prompt, "course content")

def get_practice_problems(topic, level, problem_count=5):
    prompt = f'Generate {problem_count} {level}-level industry-relevant practice problems for the Python topic "{topic}". For each problem, provide a JSON object with this structure: {{"type": "mcq" | "coding", "statement": "Problem description.", "options": ["A", "B", "C", "D"] (only for mcq), "answer": "The correct option\'s text or full code solution"}}. Return a valid JSON array of these objects. Ensure the JSON is well-formed. VERY IMPORTANT: The entire response must be ONLY the raw JSON array. All backslashes in the JSON strings must be properly escaped (e.g., use \'\\\\\' for a literal backslash in a regex).'
    json_string = fetch_api_content(prompt, f"{level} practice problems")

    if json_string:
        try:
            # Clean the response to ensure it's valid JSON
            cleaned_json = json_string.strip().replace("```json", "").replace("```", "")
            problems = json.loads(cleaned_json)
            # Add state tracking fields to each problem
            for p in problems:
                p['id'] = f"{p['statement'][:30]}_{time.time()}"
                p['status'] = 'unanswered'
                p['user_answer'] = ''
            return problems
        except json.JSONDecodeError as e:
            st.error("Failed to parse practice problems from the API response.")
            st.write("Received text:", json_string)
            return []
    return []

# --- Initialize Session State ---
if 'selected_topic' not in st.session_state:
    st.session_state.selected_topic = None
if 'course_content' not in st.session_state:
    st.session_state.course_content = ""
if 'practice_problems' not in st.session_state:
    st.session_state.practice_problems = {'Easy': [], 'Medium': [], 'Hard': []}
if 'active_view' not in st.session_state:
    st.session_state.active_view = 'learn'

# ---- UI Components ----
def display_sidebar():
    """Renders the sidebar navigation."""
    with st.sidebar:
        st.markdown("<h1 style='font-size: 2rem; font-weight: bold;'>🤖 PyLearn AI</h1>", unsafe_allow_html=True)
        st.markdown("---")

        for category, data in TOPICS.items():
            # Keep the first three categories expanded by default
            is_expanded = category in ["Python Fundamentals", "Intermediate Python", "Advanced Python"]
            with st.expander(f"{data['icon']} {category}", expanded=is_expanded):
                for topic in data['subtopics']:
                    if st.button(topic, key=topic, use_container_width=True):
                        handle_topic_select(topic)

def handle_topic_select(topic):
    """Callback function when a user selects a new topic."""
    if st.session_state.selected_topic != topic:
        st.session_state.selected_topic = topic
        st.session_state.course_content = ""
        st.session_state.practice_problems = {'Easy': [], 'Medium': [], 'Hard': []}
        st.session_state.active_view = 'learn'

        with st.spinner(f"Generating course content for '{topic}'..."):
            st.session_state.course_content = get_course_content(topic)
            st.rerun()


def display_welcome_message():
    """Shows the initial welcome screen."""
    st.markdown("<p class='welcome-text'>📘 Master Python, Data Structures & Algorithms with AI</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Select a topic from the sidebar to begin your personalized learning journey.</p>", unsafe_allow_html=True)

def display_course_content():
    """Renders the fetched course content as markdown."""
    st.markdown(st.session_state.course_content, unsafe_allow_html=True)

def display_practice_problems():
    """Handles the practice problems view, including difficulty selection and problem rendering."""
    st.subheader("Practice Problems")

    difficulties = ['Easy', 'Medium', 'Hard']
    difficulty = st.radio(
        "Select Difficulty",
        difficulties,
        horizontal=True,
        label_visibility="collapsed"
    )

    # Fetch problems if they don't exist for the selected difficulty
    if not st.session_state.practice_problems[difficulty]:
        with st.spinner(f"Generating {difficulty} problems for '{st.session_state.selected_topic}'..."):
            new_problems = get_practice_problems(st.session_state.selected_topic, difficulty)
            if new_problems:
                st.session_state.practice_problems[difficulty].extend(new_problems)
                st.rerun()

    # Display problems
    if not st.session_state.practice_problems[difficulty]:
        st.info(f"Could not generate {difficulty} problems. Please try again or select a different topic.")
        return

    for i, problem in enumerate(st.session_state.practice_problems[difficulty]):
        st.markdown("<div class='problem-card'>", unsafe_allow_html=True)

        # Using a form for each problem so submission is handled independently
        with st.form(key=f"problem_form_{problem['id']}"):
            st.markdown(f"**Problem {i+1}:** {problem['statement']}")

            user_answer = None
            if problem['type'] == 'mcq':
                user_answer = st.radio("Options", problem.get('options', []), label_visibility="collapsed", key=f"radio_{problem['id']}")
            elif problem['type'] == 'coding':
                user_answer = st.text_area("Your Solution (as a single string or function body)", height=200, key=f"code_{problem['id']}")

            submitted = st.form_submit_button("Submit Answer")

            if submitted:
                problem['user_answer'] = user_answer
                # Simple string comparison for checking answer
                if str(user_answer).strip() == str(problem['answer']).strip():
                    problem['status'] = 'correct'
                else:
                    problem['status'] = 'incorrect'
                st.rerun()

        # Display feedback outside the form
        if problem['status'] == 'correct':
            st.markdown("<div class='correct-answer'>✅ Correct!</div>", unsafe_allow_html=True)
        elif problem['status'] == 'incorrect':
            feedback = f"❌ Incorrect. The correct answer is: **{problem['answer']}**"
            st.markdown(f"<div class='incorrect-answer'>{feedback}</div>", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # Button to generate more problems
    if st.session_state.practice_problems[difficulty]:
        if st.button(f"Generate More {difficulty} Problems", use_container_width=True):
            with st.spinner("Fetching more problems..."):
                new_problems = get_practice_problems(st.session_state.selected_topic, difficulty)
                if new_problems:
                    st.session_state.practice_problems[difficulty].extend(new_problems)
                    st.rerun()


# --- Main App Logic ---
display_sidebar()

# Main content area
if not st.session_state.selected_topic:
    display_welcome_message()
else:
    st.title(st.session_state.selected_topic)
    st.markdown("<p style='color: #94a3b8;'>AI-powered concepts and practice problems.</p>", unsafe_allow_html=True)

    learn_tab, practice_tab = st.tabs(["📘 Learn", "🏋️ Practice"])

    with learn_tab:
        if st.session_state.course_content:
            display_course_content()
        else:
            st.info("Course content is being generated or was not found.")

    with practice_tab:
        display_practice_problems()