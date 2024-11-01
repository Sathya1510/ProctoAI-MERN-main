import gradio as gr
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from markupsafe import Markup

# Set up the LangChain model and prompt
template = """
    Based on the following information, generate questions as specified.

    Information:
    Text: {question}

    Answer:
    """
model = OllamaLLM(model="coding:latest")
prompt_template = ChatPromptTemplate.from_template(template)

def generate_questions(question_text):
    # Format the prompt
    prompt = prompt_template.format(question=question_text)
    
    # Generate response from the model
    raw_text = model(prompt)
    
    # Organize the generated text with HTML formatting
    formatted_text = organize_output(raw_text)
    return Markup(formatted_text)  # Return HTML formatted text for Gradio to render

def organize_output(text):
    # Organize the output by splitting and adding HTML tags for better readability
    sections = text.split("**")  # Split text by "**" to find headings
    html_output = "<div>"

    for section in sections:
        if section.strip().startswith("1.") or section.strip().startswith("2.") or section.strip().startswith("3."):
            html_output += f"<h2>{section.strip()}</h2>"
        elif "Examples:" in section:
            html_output += f"<h3>Examples:</h3><ul>"
        elif "Example" in section:
            html_output += f"<li><strong>{section.strip()}</strong></li>"
        else:
            html_output += f"<p>{section.strip()}</p>"

    html_output += "</ul></div>"
    return html_output

# Define Gradio interface
iface = gr.Interface(
    fn=generate_questions,
    inputs="text",
    outputs="html",
    title="Question Generator",
    description="Enter text to generate questions based on the input."
)

if __name__ == "__main__":
    iface.launch()
