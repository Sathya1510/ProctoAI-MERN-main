import streamlit as st
from extract_text import extract_text_from_pdf

from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

# Initialize session state for page navigation and extracted text storage
if "page" not in st.session_state:
    st.session_state.page = "Upload"
if "extracted_text" not in st.session_state:
    st.session_state.extracted_text = ""
if "mcq_count" not in st.session_state:
    st.session_state.mcq_count = 0
if "short_answer_count" not in st.session_state:
    st.session_state.short_answer_count = 0

# Sidebar
with st.sidebar:
    st.image("file.png")
    st.title("Mcq")
    choice = st.radio(
        "Navigation",
        ["Upload", "Profiling", "test", "Download"],
        index=["Upload", "Profiling", "test", "Download"].index(st.session_state.page),
    )
    st.info("This project application helps you build and explore your data.")

    # Update session state based on sidebar selection
    st.session_state.page = choice

# Main app logic based on page state
if st.session_state.page == "Upload":
    st.title("Upload Your PDF")

    # File uploader for PDF files
    file = st.file_uploader("Upload Your PDF Dataset", type=["pdf"])

    # Text area for user input
    user_input = st.text_area("Enter your text here:", height=200)

    # Display label as handwritten-style text
    st.markdown("<h3>Enter Count:</h3>", unsafe_allow_html=True)

    # Number inputs for counts
    st.session_state.mcq_count = st.number_input(
        "MCQ Question Count", min_value=0, max_value=100
    )
    st.session_state.short_answer_count = st.number_input(
        "Short Answer Count", min_value=0, max_value=100
    )

    # Button to trigger text extraction and navigate to profiling
    if st.button("Generate"):
        if file is not None:
            # Call the extraction function
            extracted_text = extract_text_from_pdf(file)

            # Append the counts to the extracted text and save to session state
            st.session_state.extracted_text = (
                f"{extracted_text}\n\n"
                f"MCQ Question Count: {st.session_state.mcq_count}\n"
                f"Short Answer Count: {st.session_state.short_answer_count}"
            )

            # Navigate to the "Profiling" page and rerun the app
            st.session_state.page = "Profiling"
            st.experimental_rerun()
        else:
            st.warning("Please upload a PDF file.")

elif st.session_state.page == "Profiling":
    st.title("Profiling Page")
    st.write("Here you can explore and profile your extracted data.")

    # Display the extracted text from session state
    if st.session_state.extracted_text:
        st.text_area("Extracted Text", st.session_state.extracted_text, height=300)

        # Set up the model and prompt
        template = """
        Based on the following information, generate questions as specified.

        Information:
        Text: {question}

        Answer:
        """
        model = OllamaLLM(model="dexter:latest")
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        # Combine everything into a single input variable
        question = (
            f"Generate {st.session_state.mcq_count} MCQs and {st.session_state.short_answer_count} short-answer questions and last give answer for all question "
            f"based on the following text:\n\n{st.session_state.extracted_text}"
        )

        # Initialize streaming output
        st.write("Generated Questions:")
        response_placeholder = st.empty()

        def generate_questions():
            response = ""

            # Stream response incrementally
            for result in chain.stream({"question": question}):
                response += result
                response_placeholder.text(response)  # Update the text incrementally

        # Run the question generation function when the page loads
        generate_questions()

    else:
        st.warning(
            "No extracted text found. Please go to 'Upload' and generate the text first."
        )
