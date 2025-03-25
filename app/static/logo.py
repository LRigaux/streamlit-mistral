"""
Logo and branding elements for the Mistral Chat application.
"""


def display_brand():
    """Return HTML for displaying the brand name."""
    return """
    <div style="font-family: 'Inter', sans-serif; font-weight: 300; letter-spacing: -0.5px; font-size: 1.8rem; margin-bottom: 2rem;">
        LRIGS<span style="color: #A82C3A; font-weight: 500;">CHAT</span>
    </div>
    """

def display_header():
    """Return HTML for the app header with LRIGSCHAT name."""
    return """
    <div style="position: fixed; top: 0; left: 0; right: 0; background-color: white; z-index: 1000; 
         padding: 0.5rem 1rem; box-shadow: 0 2px 5px rgba(0,0,0,0.05); display: flex; align-items: center;">
        <div style="font-family: 'Inter', sans-serif; font-size: 1.2rem; font-weight: 500;">
            LRIGS<span style="color: #A82C3A;">CHAT</span>
        </div>
    </div>
    <div style="height: 3rem;"></div> <!-- Spacer to prevent content from hiding under the header -->
    """ 