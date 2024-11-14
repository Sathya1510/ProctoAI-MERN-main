import gradio as gr
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from markupsafe import Markup

# Set up the LangChain model and prompt
template = """
    Based on the following information, generate both questions and answers as specified.

    Information:
    Text: {question_text}

    Output:
    """
model = OllamaLLM(model="coding:latest")
prompt_template = ChatPromptTemplate.from_template(template)

def generate_questions_and_answers(question_text):
    # Format the prompt
    prompt = prompt_template.format(question_text=question_text)
    
    # Generate response from the model
    raw_text = model(prompt)
    
    # Organize the generated text with line-by-line HTML formatting
    formatted_text = organize_output_line_by_line(raw_text)
    return Markup(formatted_text)  # Return HTML formatted text for Gradio to render

def organize_output_line_by_line(text):
    # Organize the output by splitting each line and wrapping it in a <p> tag
    lines = text.split("\n")  # Split text by newlines
    html_output = "<div>"

    for line in lines:
        if line.strip():  # Skip empty lines
            html_output += f"<p>{line.strip()}</p>"

    html_output += "</div>"
    return html_output

# Define Gradio interface
iface = gr.Interface(
    fn=generate_questions_and_answers,
    inputs="text",
    outputs="html",
    title="Question and Answer Generator",
    description="Enter text to generate questions and answers line by line based on the input."
)

if __name__ == "__main__":
    iface.launch()
