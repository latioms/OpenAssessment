from flask import Flask, request, jsonify, render_template
import openai, os

app = Flask(__name__)

class ChatGPTBotAPI:
    def __init__(self, api_key, model):
        self.api_key = api_key
        self.model = model

    def initialize_gpt3(self):
        # on instacie la classe openai avec la clé api
        openai.api_key = self.api_key 

    def create_prompt(self, prompt):
        # For simplicity, we will use an in-memory 
        if not hasattr(self, 'prompts'):
            self.prompts = []
        self.prompts.append(prompt)
        return f"Prompt '{prompt}' stored successfully."

    def get_response(self, prompt_index):
        # Get the ChatGPT bot's response to a previously stored prompt at the given index
        # For simplicity, we assume the prompt_index is valid.
        prompt = self.prompts[prompt_index]
        # define type of response
        response = openai.Completion.create(
            engine=self.model,
            prompt=prompt,
            max_tokens=100
        )
        if response != None:
         return response['choices'][0]['text']
        else : 
            return "Aouch, something went wrong !"

    def update_prompt(self, prompt_index, new_prompt):
        # Update an existing prompt at the given index with a new prompt provided by the user
        # For simplicity, we assume the prompt_index is valid.
        self.prompts[prompt_index] = new_prompt
        return f"Prompt at index {prompt_index} updated successfully."

# Initialize the ChatGPTBotAPI instance
bot_api = ChatGPTBotAPI(api_key= os.getenv("OPENAI_API_KEY") , model="gpt-3.5-turbo")
bot_api.initialize_gpt3()

# Create API endpoints
@app.route("/initialize_gpt3", methods=["POST"])
def initialize_gpt3():
    bot_api.initialize_gpt3()
    return jsonify({"message": "OpenAI API initialized successfully."})

@app.route("/create_prompt", methods=["POST"])
def create_prompt():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required."}), 400
    message = bot_api.create_prompt(prompt)
    return jsonify({"message": message})

@app.route("/get_response/<int:prompt_index>", methods=["GET"])
def get_response(prompt_index):
    response = bot_api.get_response(prompt_index)
    return jsonify({"response": response})

@app.route("/update_prompt/<int:prompt_index>", methods=["PUT"])
def update_prompt(prompt_index):
    data = request.get_json()
    new_prompt = data.get("new_prompt")
    if not new_prompt:
        return jsonify({"error": "New prompt is required."}), 400
    message = bot_api.update_prompt(prompt_index, new_prompt)
    return jsonify({"message": message})

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        prompt = request.form.get("prompt")
        if not prompt:
            return render_template("index.html", error="Prompt is required.")
        message = bot_api.create_prompt(prompt)
        return render_template("index.html", message=message)
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
