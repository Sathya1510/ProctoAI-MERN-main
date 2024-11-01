let questions = {{ questions | tojson }};

function loadQuestion() {
    const questionId = document.getElementById("questionSelect").value;
    const question = questions.find(q => q.id == questionId);
    document.getElementById("description").textContent = question.description;
}

async function runCode() {
    const code = document.getElementById("codeInput").value;
    const language = document.getElementById("languageSelect").value;
    const questionId = document.getElementById("questionSelect").value;

    const response = await fetch("/run_code", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ code: code, language: language, question_id: questionId }),
    });

    const result = await response.json();
    document.getElementById("resultSummary").textContent = `Test Cases Passed: ${result.total_passed}/${result.total_cases}`;
    
    const testCaseResults = result.results.map((test, index) => `
        <div>
            <h4>Test Case ${index + 1}</h4>
            <p><strong>Input:</strong> ${test.input}</p>
            <p><strong>Expected Output:</strong> ${test.expected_output}</p>
            <p><strong>Your Output:</strong> ${test.output}</p>
            <p>${test.is_pass ? "✅ Passed" : "❌ Failed"}</p>
        </div>
    `).join("");

    document.getElementById("testCases").innerHTML = testCaseResults;
}
