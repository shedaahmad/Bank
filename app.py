import os
from flask import Flask, render_template, request, jsonify
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

class BankingBot:
    """A banking assistant chatbot powered by Mistral Large model"""
    
    def __init__(self):
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables")
        
        self.client = Mistral(api_key=api_key)
        self.model = "mistral-large-latest"
        self.conversation_history = []
        
        # System prompt for banking bot
        self.system_prompt = """You are a friendly, professional banking assistant. Your goal is to help customers with their banking needs in a clear, conversational manner.

You can help with:
- Account questions (savings, checking, credit cards)
- Money transfers and payments
- Loan and credit information
- Banking products and services
- General financial questions

Guidelines:
1. Keep responses concise and easy to understand (2-3 sentences)
2. Use simple language, avoid jargon
3. For sensitive matters, recommend secure verification
4. Never ask for passwords or PIN numbers
5. Be warm and helpful while maintaining professionalism
6. Format responses clearly without excessive formatting marks
7. Always be ready to escalate to a human agent if needed

Remember: You're here to make banking easier and more pleasant!"""
    
    def chat(self, user_message):
        """Send a message and get a response from the bot"""
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call Mistral API
            response = self.client.chat.complete(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ]
            )
            
            # Extract assistant response
            assistant_message = response.choices[0].message.content
            
            # Add to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            error_msg = f"Error communicating with Mistral API: {str(e)}"
            return error_msg
    
    def get_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []


# Initialize the bot
try:
    bot = BankingBot()
except ValueError as e:
    print(f"Error: {e}")
    bot = None


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatting with the bot"""
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    response = bot.chat(user_message)
    return jsonify({'response': response})


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    return jsonify({'history': bot.get_history()})


@app.route('/api/clear', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    if not bot:
        return jsonify({'error': 'Bot not initialized'}), 500
    
    bot.clear_history()
    return jsonify({'message': 'History cleared'})


if __name__ == '__main__':
    if bot:
        print("\n" + "="*60)
        print("🏦 Banking Bot Web Server Starting")
        print("="*60)
        print("\n✅ Access the bot at: http://127.0.0.1:5000")
        print("\n" + "="*60 + "\n")
        app.run(debug=True, use_reloader=False)
    else:
        print("Failed to start the bot. Check your configuration.")
