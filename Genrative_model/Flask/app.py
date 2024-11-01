from flask import Flask, render_template, request, Markup
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)

# Set up the LangChain model and prompt
template = """
    Based on the following information, generate questions as specified.

    Information:
    Text: {question}

    Answer:
    """
model = OllamaLLM(model="coding:latest")
prompt_template = ChatPromptTemplate.from_template(template)

@app.route("/", methods=["GET", "POST"])
def index():
    generated_text = None
    if request.method == "POST":
        # Get input from form
        question_text = request.form.get("question")

        # Format prompt
        prompt = prompt_template.format(question=question_text)
        
        # Generate response
        raw_text = model(prompt)
        
        # Organize the generated text with HTML formatting
        formatted_text = organize_output(raw_text)
        generated_text = Markup(formatted_text)  # Use Markup to allow HTML rendering

    # Render the template with generated text if available
    return render_template("index.html", generated_text=generated_text)

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

if __name__ == "__main__":
    app.run(debug=True, port=6000)
