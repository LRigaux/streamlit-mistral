# MISTRAL CHAT

A minimal, elegant chat application powered by Mistral AI's multimodal models.

![Mistral Chat UI](https://raw.githubusercontent.com/yourusername/streamlit-mistral/main/docs/mistral-chat-screenshot.png) <!-- Replace with your actual screenshot once available -->

## Features

- **Clean, Minimal Interface**: Simple and elegant design for distraction-free conversations
- **Multiple Model Support**: Choose from available Mistral AI models
- **Image Upload**: Send images to multimodal models for analysis
- **Token Control**: Limit token generation for faster, more focused responses
- **Multi-Chat Management**: Create, manage, and switch between multiple conversations
- **Responsive Design**: Works on desktop and mobile devices

## Installation

### Prerequisites
- Python 3.8 or higher
- A Mistral AI API key (get one at [https://console.mistral.ai/](https://console.mistral.ai/))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/streamlit-mistral.git
   cd streamlit-mistral
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set your Mistral API key:
   ```bash
   # On Linux/macOS
   export MISTRAL_API_KEY=your_api_key_here
   
   # On Windows (Command Prompt)
   set MISTRAL_API_KEY=your_api_key_here
   
   # On Windows (PowerShell)
   $env:MISTRAL_API_KEY="your_api_key_here"
   ```

## Usage

Run the application:
```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`.

### Managing Conversations

- **Create a New Chat**: Click the "New Chat" button in the sidebar
- **Switch Chats**: Select any conversation from the sidebar
- **Delete a Chat**: Click the delete icon next to a chat name
- **Rename Chat**: First message of your conversation becomes the chat title

### Chat Features

1. **Select a Model**: Choose from available Mistral AI models
2. **Set Token Limit**: Control response length with the token slider
3. **Upload Images**: Click the upload button to include images
4. **Send Messages**: Type your message and press Enter or click Send

## Testing

To run automated tests for the application:

```bash
python test.py
```

To run specific test cases:

```bash
python test.py --test api  # Test API connection
python test.py --test chat  # Test chat functionality
```

## Project Structure

```
streamlit-mistral/
├── app/
│   ├── components/
│   │   ├── chat.py          # Chat interface component
│   │   └── sidebar.py       # Sidebar component
│   ├── config/
│   │   └── config.py        # Configuration management
│   ├── static/
│   │   └── logo.py          # Logo and branding elements
│   └── utils/
│       ├── logging_util.py  # Logging utilities
│       └── mistral_client.py # Mistral API client
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── app.py                   # Main application
├── requirements.txt         # Project dependencies
├── test.py                  # Test suite
└── README.md                # This documentation
```

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Powered by [Mistral AI](https://mistral.ai/) models
- Design inspired by minimal interfaces

## License

MIT License 