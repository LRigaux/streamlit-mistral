# Mistral AI Chat Application

A Streamlit application for chatting with Mistral AI models, including image upload capabilities.

## Features

- Chat interface with Mistral AI models
- Image upload for multimodal analysis
- API connection testing
- Secure API key management
- Beautiful UI with autumn color palette

## Screenshot

![Application Screenshot](asset\preview.png)

## Prerequisites

- Python 3.8+
- Mistral AI API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/streamlit-mistral.git
cd streamlit-mistral
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up your Mistral API key:

**Method 1: Environment Variable (Recommended for security)**
```bash
# For Windows
setx MISTRAL_API_KEY "your-api-key-here"

# For macOS/Linux
export MISTRAL_API_KEY="your-api-key-here"
```

**Method 2: .env File**
Create a `.env` file in the project root with the following content:
```
MISTRAL_API_KEY=your-api-key-here
```

## Running the Application

Run the Streamlit app:
```bash
streamlit run app.py
```

The application will be available at http://localhost:8501.

## Testing

Run the simplified test script:
```bash
# Run all tests
python test.py

# Test only API connection
python test.py api

# Test only chat functionality
python test.py chat
```

## Project Structure

```
streamlit-mistral/
├── app/
│   ├── components/    # UI components
│   │   ├── chat.py    # Chat interface
│   │   └── sidebar.py # Sidebar settings
│   ├── config/        # Configuration settings
│   │   └── config.py  # Environment & app config
│   └── utils/         # Utility modules
│       ├── logging_util.py   # Logging utilities 
│       └── mistral_client.py # Mistral API client
├── .env               # (git-ignored) Environment variables
├── .gitignore         # Git ignore file
├── app.py             # Main Streamlit application
├── README.md          # This README file
├── requirements.txt   # Python dependencies
└── test.py            # Test script
```

## Security Considerations

- This application uses environment variables to securely store API keys
- The API key is never exposed in the UI
- The .env file is included in .gitignore to prevent accidental commits of API keys

## Deployment

The application can be deployed to various platforms:

### Streamlit Cloud

1. Push your code to GitHub
2. Create an account on [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository and deploy
4. Set your `MISTRAL_API_KEY` as a secret in the Streamlit Cloud settings

### Heroku

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku and create a new app:
```bash
heroku login
heroku create your-app-name
```

3. Set your API key as a Heroku environment variable:
```bash
heroku config:set MISTRAL_API_KEY=your-api-key-here
```

4. Deploy to Heroku:
```bash
git push heroku main
```

## License

MIT

## Acknowledgements

- [Mistral AI](https://mistral.ai/) for their powerful language models
- [Streamlit](https://streamlit.io/) for the simple web application framework 