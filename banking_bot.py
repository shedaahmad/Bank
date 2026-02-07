import os
from mistralai import Mistral
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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
            print(error_msg)
            return error_msg
    
    def get_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*60)
        print("🏦 Welcome to Banking Bot")
        print("="*60)
        print("Powered by Mistral Large AI Model")
        print("\nI'm here to help with your banking needs.")
        print("Type 'exit' to quit, 'clear' to reset conversation, or 'help' for commands.\n")
        print("="*60 + "\n")


def main():
    """Main function to run the banking bot"""
    try:
        bot = BankingBot()
        bot.display_welcome()
        
        while True:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "exit":
                print("\nThank you for using Banking Bot. Goodbye! 👋")
                break
            
            if user_input.lower() == "clear":
                bot.clear_history()
                print("Conversation history cleared.\n")
                continue
            
            if user_input.lower() == "help":
                print("\n--- Commands ---")
                print("exit  - Quit the application")
                print("clear - Clear conversation history")
                print("help  - Show this help message\n")
                continue
            
            print("\nBot: ", end="")
            response = bot.chat(user_input)
            print(response + "\n")
            
    except KeyError as e:
        print(f"Configuration error: {e}")
        print("Please ensure MISTRAL_API_KEY is set in .env file")


if __name__ == "__main__":
    main()
