import streamlit as st
from extract_text import extract_text_from_pdf
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import json
from bson import ObjectId

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "Upload"
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "mcq_count" not in st.session_state:
    st.session_state.mcq_count = 0
if "short_answer_count" not in st.session_state:
    st.session_state.short_answer_count = 0
if "generated_questions" not in st.session_state:
    st.session_state.generated_questions = ""

# Sidebar Navigation
with st.sidebar:
    st.image("file.png")
    st.title("MCQ Generator")
    choice = st.radio(
        "Navigation",
        ["Upload", "Profiling", "Test", "Download"],
        index=["Upload", "Profiling", "Test", "Download"].index(st.session_state.page),
    )
    st.info("This project helps you build and explore your data.")
    st.session_state.page = choice

# Main Page Logic
if st.session_state.page == "Upload":
    st.title("Upload Your PDF")

    # File Upload
    file = st.file_uploader("Upload Your PDF Dataset", type=["pdf"])
    user_input = st.text_area("Enter your text here:", height=200)

    # Count Inputs
    st.markdown("<h3>Enter Question Count:</h3>", unsafe_allow_html=True)
    st.session_state.mcq_count = st.number_input("MCQ Question Count", min_value=0, max_value=100)
    st.session_state.short_answer_count = st.number_input("Short Answer Count", min_value=0, max_value=100)

    # Generate Questions
    if st.button("Generate"):
        if file is not None:
            extracted_text = extract_text_from_pdf(file)
            st.session_state.extracted_text = (
                f"{extracted_text}\n\nMCQ Question Count: {st.session_state.mcq_count}\nShort Answer Count: {st.session_state.short_answer_count}"
            )
            st.session_state.page = "Profiling"
            st.experimental_rerun()
        else:
            st.warning("Please upload a PDF file.")

elif st.session_state.page == "Profiling":
    st.title("Profiling Page")
    if st.session_state.extracted_text:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=300)

        # Setup the model and prompt
        template = "Based on the following information, generate questions as specified.\n\nText: {question}\nAnswer:give the correct option +answer after all question are genrated"
        model = OllamaLLM(model="dexter:latest")
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        # Define the input question prompt
        question = (
            f"Generate {st.session_state.mcq_count} MCQs and {st.session_state.short_answer_count} short-answer questions based on the following text:\n\n{st.session_state.extracted_text}"
        )

        # Display response
        st.write("Generating Questions...")
        response_placeholder = st.empty()

        def generate_questions():
            response = ""
            for result in chain.stream({"question": question}):
                response += result
                response_placeholder.text(response)
            st.session_state.generated_questions = response

        generate_questions()

    else:
        st.warning("No extracted text found. Please go to 'Upload' and generate the text first.")

elif st.session_state.page == "Test":
    st.title("Test Page")
    if st.session_state.generated_questions:
        st.write("Generated Questions:")
        st.write(st.session_state.generated_questions)

        # Clean and process the generated questions
        cleaned_questions = re.sub(r'\*\*|\*|\(.*?\)', '', st.session_state.generated_questions).strip()
        question_section = cleaned_questions.split("Answer Explanations:")[0]
        questions_pattern = r'(\d+\.\s+.+?)(?=\n\d+\.|\Z)'
        options_pattern = r'([a-d])\)\s+(.+)'
        
        questions = re.findall(questions_pattern, question_section, re.DOTALL)
        exam_id = "a2651b05-8a45-4a95-8b0c-082d0c261afe"
        timestamp = "2024-09-25T14:48:06.066+00:00"

        formatted_questions = []
        for i, question in enumerate(questions):
            question_lines = question.strip().split('\n')
            question_text = question_lines[0]
            answers_text = '\n'.join(question_lines[1:])
            options = re.findall(options_pattern, answers_text)
            explanation_match = re.search(rf"{i+1}\.\s+([a-d])", cleaned_questions)
            correct_letter = explanation_match.group(1) if explanation_match else None

            options_list = []
            for option_letter, option_text in options:
                options_list.append({
                    "optionText": option_text.strip(),
                    "isCorrect": option_letter == correct_letter,
                    "_id": ObjectId()
                })

            formatted_questions.append({
                "_id": ObjectId(),
                "question": question_text.strip(),
                "options": options_list,
                "examId": exam_id,
                "createdAt": timestamp,
                "updatedAt": timestamp,
                "__v": 0
            })
        

        # Only include questions that have non-empty options
        filtered_questions = [
    question for question in formatted_questions if question["options"]
]

# Convert to JSON
        json_output = json.dumps(filtered_questions, default=str, indent=2)


# Display a download button for the generated JSON
        st.download_button(
                label="Download Questions JSON",
                data=json_output,
                file_name="generated_questions.json",
                mime="application/json"
            )

