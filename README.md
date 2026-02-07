# Banking Bot

A conversational banking assistant powered by Mistral Large AI model.

## Features

- 🤖 AI-powered banking assistant using Mistral Large
- 💬 Natural language conversations
- 🏦 Support for common banking queries
- 📜 Conversation history tracking
- 🔒 Secure API key management

## Setup

### Prerequisites
- Python 3.8+
- Mistral API key

### Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate     # macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file with your Mistral API key:
```
MISTRAL_API_KEY=your_api_key_here
```

## Usage

### Interactive Chat
```bash
python banking_bot.py
```

Commands:
- `exit` - Quit the application
- `clear` - Clear conversation history
- `help` - Show available commands

### Run Tests
```bash
python test_bot.py
```

## Features Explained

### BankingBot Class
- **chat()** - Send a message and get AI response
- **get_history()** - View conversation history
- **clear_history()** - Reset the conversation

### System Prompt
The bot is configured with a banking-specific system prompt to provide:
- Account information assistance
- Transaction support
- Loan and credit card information
- General financial advice
- Professional and secure responses

## API Integration

The bot uses:
- **Model**: mistral-large-latest
- **API**: Mistral AI Python SDK
- **Security**: Environment variables for API key management

## Example Interaction

```
User: What banking services do you offer?
Bot: As a banking assistant, I can help you with:
- Account information and balance inquiries
- Transaction history
- Money transfers
- Loan information
- Credit card details
- Banking services and products
- General financial advice

Feel free to ask me anything related to banking!
```

## Security Notes

⚠️ **Important**:
- Never commit `.env` file to version control
- Always use environment variables for sensitive data
- The bot won't ask for passwords or sensitive credentials
- For real sensitive operations, users should verify through secure banking channels

## Requirements

See `requirements.txt` for dependencies.
