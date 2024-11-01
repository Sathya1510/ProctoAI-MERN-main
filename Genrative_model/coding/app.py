import streamlit as st
import subprocess

# Define the questions with test cases
questions = [
    {
        "id": 1,
        "title": "Sum of Two Numbers",
        "description": "Write a program that takes two numbers as input and prints their sum.",
        "test_cases": [
            {"input": "5\n3", "expected_output": "8"},
            {"input": "10\n20", "expected_output": "30"},
            {"input": "0\n0", "expected_output": "0"}
        ]
    },
    {
        "id": 2,
        "title": "Reverse a String",
        "description": "Write a program that reverses the input string.",
        "test_cases": [
            {"input": "hello", "expected_output": "olleh"},
            {"input": "world", "expected_output": "dlrow"},
            {"input": "Python", "expected_output": "nohtyP"}
        ]
    }
]

# Streamlit UI Components
st.title("Online Code Compiler")

# Select a question
question_titles = [q["title"] for q in questions]
selected_question_title = st.selectbox("Select a Question", question_titles)
selected_question = next(q for q in questions if q["title"] == selected_question_title)

st.write(f"### {selected_question['title']}")
st.write(selected_question["description"])

# Select Language
language = st.selectbox("Select Language", ["Python", "JavaScript"])

# Code input area
code = st.text_area("Write your code here...", height=200)

# Run Code Button
if st.button("Run Code"):
    results = []
    
    for test_case in selected_question["test_cases"]:
        input_data = test_case["input"]  # This should have the correct input format
        
        if language == "Python":
            # Define a Python function to run user code
            wrapped_code = f"""
def user_code():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    a = int(data[0])  # first input
    b = int(data[1])  # second input
    return a + b

print(user_code())
"""
            command = ["python3", "-c", wrapped_code]
        elif language == "JavaScript":
            # JavaScript version of the function
            wrapped_code = f"""
const user_code = () => {{
    const input = `{input_data}`;
    const data = input.split('\\n');
    const a = parseInt(data[0]); // first input
    const b = parseInt(data[1]); // second input
    return a + b;
}};
console.log(user_code());
"""
            command = ["node", "-e", wrapped_code]
        else:
            st.error("Unsupported language.")
            continue
        
        try:
            result = subprocess.run(
                command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5
            )
            output = result.stdout.strip()
            is_pass = output == test_case["expected_output"]
            results.append({
                "input": input_data, 
                "expected_output": test_case["expected_output"], 
                "output": output, 
                "is_pass": is_pass
            })
        except subprocess.TimeoutExpired:
            results.append({"input": input_data, "expected_output": test_case["expected_output"], "output": "Error: Code execution timed out.", "is_pass": False})

    # Display results summary
    total_passed = sum(1 for result in results if result["is_pass"])
    total_cases = len(selected_question["test_cases"])

    st.write(f"### Test Cases Passed: {total_passed}/{total_cases}")

    # Display each test case result
    for idx, result in enumerate(results, 1):
        st.write(f"**Test Case {idx}**")
        st.write(f"- **Input:** {result['input']}")
        st.write(f"- **Expected Output:** {result['expected_output']}")
        st.write(f"- **Your Output:** {result['output']}")
        st.write(f"- **Result:** {'✅ Passed' if result['is_pass'] else '❌ Failed'}")
