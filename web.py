from flask import Flask, request, send_from_directory, jsonify
from openai import OpenAI
import os
import re

# Initialize Flask app
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ANSWERS_FILE = 'answers.txt'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize OpenAI client
client = OpenAI()

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_audio():
    # Save uploaded audio file
    file = request.files['answer']
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Transcribe the audio to text
    try:
        with open(file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                language="ar",
                timestamp_granularities=["word"]
            )
        answer_text = transcript.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Save the transcribed text in order
    try:
        with open(ANSWERS_FILE, "a", encoding="utf-8") as f:
            f.write(f"Answer {filename}: {answer_text}\n")
    except Exception as e:
        return jsonify({"error": f"Failed to save transcription: {str(e)}"}), 500
    
    return jsonify({"message": "Answer saved successfully", "transcription": answer_text}), 200

# Function to interact with the assistant
def ask_assistant(prompt):
    # Initialize assistant_id
    assistant_id = "asst_giR1NLSsZhx8nxft3gNvpDna"

    # Create a thread and attach the file to the message
    thread = client.beta.threads.create(
        messages=[{
            "role": "user",
            "content": prompt,
            "attachments": [],
        }]
    )

    # Use the create and poll SDK helper to create a run and poll the status of the run until it's in a terminal state.
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant_id
    )

    messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

    cv_content = ""
    for message in messages:
        # Extract the text content from the message
        text_content = message.content[0].text.value
        
        # Clean the text by removing the Markdown-like syntax (** and ---)
        clean_text = re.sub(r"(\*\*|---)", "", text_content).strip()
        
        # Optionally, remove empty sections or notes like "(لا توجد معلومات إضافية)"
        clean_text = re.sub(r"\(.*?\)", "", clean_text).strip()

        # Append the clean text to the final CV content
        cv_content += clean_text + "\n"

    return cv_content  # Return the cleaned CV content to the frontend

@app.route('/generate-cv', methods=['POST'])
def generate_cv():
    try:
        # Read answers from the answers.txt file
        with open(ANSWERS_FILE, "r", encoding="utf-8") as file:
            answers = file.read()

        # Call assistant to process answers and generate CV (you can modify this as needed)
        cv_content = ask_assistant(answers)
        
        # Return the CV content to be displayed in the frontend
        return jsonify({"cv": cv_content}), 200
    except Exception as e:
        return jsonify({"error": f"Error generating CV: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
