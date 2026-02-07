import os
from banking_bot import BankingBot


def test_banking_bot():
    """Test the banking bot functionality"""
    print("Testing Banking Bot...\n")
    
    try:
        bot = BankingBot()
        
        # Test queries
        test_queries = [
            "What banking services do you offer?",
            "How can I check my account balance?",
            "I want to transfer money to another account",
            "What's the interest rate on savings accounts?"
        ]
        
        for query in test_queries:
            print(f"User: {query}")
            response = bot.chat(query)
            print(f"Bot: {response}\n")
            print("-" * 60 + "\n")
        
        print("Test completed successfully!")
        
    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    test_banking_bot()
