import streamlit as st
from extract_text import extract_text_from_pdf
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import re
import json

# Initialize session state variables
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
if "generated_questions_json" not in st.session_state:
    st.session_state.generated_questions_json = ""

# Sidebar Navigation
with st.sidebar:
    st.image("Copy-of-Copy-of-Copy-of-Pastel-Abstract-New-Blog-Instagram-Post-6.png")
    st.title("MCQ Generator")
    choice = st.radio(
        "Navigation",
        ["Upload", "Generating", "Test", "Download"],
        index=["Upload", "Generating", "Test", "Download"].index(st.session_state.page),
    )
    
    st.session_state.page = choice

# Helper function to extract and set text
def extract_text_from_input(file, user_input):
    if file:
        return extract_text_from_pdf(file)
    elif user_input.strip():
        return user_input
    else:
        st.warning("Please provide either a PDF file or text input.")
        return None

# Helper function for question generation
def generate_questions(model, question_prompt, response_placeholder):
    response = ""
    for result in model.stream({"question": question_prompt}):
        response += result
        response_placeholder.text(response)
    st.session_state.generated_questions = response

# Upload Page Logic
if st.session_state.page == "Upload":
    st.title("Upload Your PDF or Enter Text")
    file = st.file_uploader("Upload Your PDF Dataset", type=["pdf"])
    user_input = st.text_area("Enter your text here:", height=200)

    # Count Inputs
    st.markdown("<h3>Enter Question Count:</h3>", unsafe_allow_html=True)
    st.session_state.mcq_count = st.number_input("MCQ Question Count", min_value=0, max_value=100)
    st.session_state.short_answer_count = st.number_input("Short Answer Count", min_value=0, max_value=100)

    # Generate Questions Button
    if st.button("Generate"):
        extracted_text = extract_text_from_input(file, user_input)
        if extracted_text:
            st.session_state.extracted_text = f"{extracted_text}\n\nMCQ Question Count: {st.session_state.mcq_count}\nShort Answer Count: {st.session_state.short_answer_count}"
            st.session_state.page = "Generating"
            st.experimental_rerun()

# Generating Page Logic
elif st.session_state.page == "Generating":
    st.title("Generating Questions...")
    if st.session_state.extracted_text:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=300)

        # Model and prompt setup
        template = "Based on the following information, generate questions as specified.\n\nText: {question}\nAnswer: Provide the correct answer with text after all questions are generated."
        model = OllamaLLM(model="dexter:latest")
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        question_prompt = f"Generate {st.session_state.mcq_count} MCQs and {st.session_state.short_answer_count} short-answer questions based on the following text:\n\n{st.session_state.extracted_text}"
        response_placeholder = st.empty()
        generate_questions(chain, question_prompt, response_placeholder)

    else:
        st.warning("No extracted text found. Please return to 'Upload' to input text.")

# Test Page Logic
elif st.session_state.page == "Test":
    st.title("Test Generated Questions")
    if st.session_state.generated_questions:
        st.write("Generated Questions:")
        st.write(st.session_state.generated_questions)

        # Process the generated questions
        cleaned_questions = re.sub(r'\*\*|\*|\(.*?\)', '', st.session_state.generated_questions).strip()
        question_section = cleaned_questions.split("Answer Explanations:")[0]
        questions_pattern = r'(\d+\.\s+.+?)(?=\n\d+\.|\Z)'
        options_pattern = r'([a-d])\)\s+(.+)'
        
        questions = re.findall(questions_pattern, question_section, re.DOTALL)
        formatted_questions = []
        for i, question in enumerate(questions):
            question_lines = question.strip().split('\n')
            question_text = question_lines[0]
            answers_text = '\n'.join(question_lines[1:])
            options = re.findall(options_pattern, answers_text)
            explanation_match = re.search(rf"{i+1}\.\s+([a-d])", cleaned_questions)
            correct_letter = explanation_match.group(1) if explanation_match else None

            options_list = [{"optionText": option_text.strip(), "isCorrect": option_letter == correct_letter} for option_letter, option_text in options]
            if options_list:
                formatted_questions.append({"question": question_text.strip(), "options": options_list})

        # JSON Output
        json_output = json.dumps(formatted_questions, indent=4)
        st.session_state.generated_questions_json = json_output
        st.subheader("Generated Questions in JSON Format:")
        st.json(json_output)

# Download Page Logic
elif st.session_state.page == "Download":
    st.title("Download Your Generated Questions")

    if "generated_questions_json" in st.session_state:
        st.subheader("Generated Questions JSON Preview:")
        st.json(st.session_state.generated_questions_json)

        # Download button
        st.download_button(
            label="Download Questions JSON",
            data=st.session_state.generated_questions_json,
            file_name="generated_questions.json",
            mime="application/json"
        )
    else:
        st.warning("No questions generated. Please go to 'Test' to generate questions.")
