"""
Styles module for the Streamlit application.
Contains CSS styles and theme configuration for the Mistral AI Chat application.
"""

def get_app_css():
    """Return the CSS for the application."""
    return """
    /* Font and Base Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
    }
    
    /* Color palette - minimal with accent colors */
    :root {
        --bg-color: #FFFFFF;
        --text-color: #111111;
        --accent1: #A82C3A;  /* Red from autumn palette */
        --accent2: #DE7921;  /* Orange from autumn palette */
        --accent3: #3A2A3A;  /* Dark Purple from autumn palette */
        --light-gray: #F5F5F5;
        --medium-gray: #E0E0E0;
        --dark-gray: #666666;
    }
    
    /* Apply colors to elements */
    .stApp {
        background-color: var(--bg-color);
        color: var(--text-color);
    }
    
    /* Header styling */
    h1, h2, h3 {
        font-weight: 400;
        letter-spacing: -0.5px;
        color: var(--text-color);
    }
    
    h1 {
        font-size: 2.2rem;
        margin-bottom: 2rem;
    }
    
    h2 {
        font-size: 1.5rem;
        margin-top: 2rem;
    }
    
    /* Form styling */
    div[data-testid="stForm"] {
        background-color: var(--light-gray);
        padding: 1.5rem;
        border-radius: 0px;
        border: none;
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: var(--accent1);
        color: white;
        border: none;
        border-radius: 0px;
        padding: 0.5rem 1.5rem;
        font-weight: 400;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--text-color);
        color: white;
        transform: translateY(-2px);
    }
    
    /* Input fields */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-color: var(--medium-gray);
        border-radius: 0px;
    }
    
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--accent1);
        box-shadow: none;
    }
    
    /* Sidebar styling */
    .stSidebar {
        background-color: var(--bg-color);
        border-right: 1px solid var(--medium-gray);
    }
    
    /* File uploader */
    .stFileUploader > div > button {
        background-color: transparent;
        border: 1px dashed var(--medium-gray);
        border-radius: 0px;
        color: var(--dark-gray);
    }
    
    .stFileUploader > div > button:hover {
        border-color: var(--accent1);
        color: var(--accent1);
    }
    
    /* Chat messages */
    .stChatMessage {
        background-color: var(--light-gray);
        border-radius: 0px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .stChatMessage.user {
        background-color: var(--light-gray);
    }
    
    .stChatMessage.assistant {
        background-color: white;
        border-left: 3px solid var(--accent1);
    }
    
    /* Select boxes */
    .stSelectbox label, .stNumberInput label {
        color: var(--text-color) !important;
        font-weight: 400;
    }
    
    .stSelectbox > div > div, .stNumberInput > div > div {
        border-radius: 0px;
    }
    
    /* For all labels */
    label {
        font-weight: 400 !important;
        color: var(--text-color) !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background-color: var(--accent1);
    }
    
    /* Horizontal rule */
    hr {
        border-color: var(--medium-gray);
    }
    
    /* Footer text */
    .stFooter {
        color: var(--dark-gray);
        font-size: 0.8rem;
    }
    
    /* Make the chat area stand out more */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Customize scrollbar */
    ::-webkit-scrollbar {
        width: 5px;
        height: 5px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light-gray);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--dark-gray);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent1);
    }
    
    /* Hide main title - we'll use our custom logo instead */
    .main > div:first-child {
        height: 0;
        padding: 0;
        margin: 0;
    }

    /* Adjust sidebar scrolling to make room for fixed header */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        padding-top: 3rem;
    }
    """

def get_fixed_input_css():
    """Return CSS for fixed input container at bottom of screen."""
    return """
    /* Fixed input container at bottom */
    #fixed-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: white;
        padding-bottom: 20px;
        padding-top: 10px;
        border-top: 1px solid #e0e0e0;
        margin-left: 1rem; /* Match Streamlit's default padding */
        z-index: 100;
    }
    
    /* Ensure content doesn't get hidden behind fixed input */
    .main .block-container {
        padding-bottom: 240px !important;
    }
    
    /* Prevent form from being hidden */
    [data-testid="stForm"] {
        background-color: white;
    }
    """

def get_scroll_to_input_js():
    """Return JavaScript for scrolling to input when chat message is clicked."""
    return """
    function scrollToInput() {
        document.getElementById('fixed-input-container').scrollIntoView({behavior: 'smooth'});
    }
    document.addEventListener('DOMContentLoaded', function() {
        var chatMessages = document.querySelectorAll('[data-testid="stChatMessage"]');
        chatMessages.forEach(function(message) {
            message.addEventListener('click', scrollToInput);
        });
    });
    """

def get_keyboard_shortcuts_js():
    """Return JavaScript for keyboard shortcuts."""
    return """
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to submit the form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            var submitBtn = document.querySelector('button[type="submit"]');
            if (submitBtn) submitBtn.click();
        }
        
        // Escape to clear textarea
        if (e.key === 'Escape') {
            var textarea = document.querySelector('textarea');
            if (textarea) textarea.value = '';
        }
    });
    """ 