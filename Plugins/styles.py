# styles.py

# CSS Styles
GLASS_SIDEBAR_CSS = """
    <style>
    /* Sidebar Glass Effect */
    [data-testid="stSidebar"] {
        background: rgba(15, 22, 30, 0.7);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Remove default Streamlit padding */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }
    
    /* Smooth scrollbar */
    [data-testid="stSidebar"]::-webkit-scrollbar {
        width: 6px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb {
        background: rgba(207, 154, 196, 0.5);
        border-radius: 10px;
    }
    
    [data-testid="stSidebar"]::-webkit-scrollbar-thumb:hover {
        background: rgba(207, 154, 196, 0.8);
    }
    </style>
"""

# Menu Styles Dictionary
MENU_STYLES = {
    "container": {
        "padding": "0px",
        "background-color": "transparent",
    },
    "icon": {
        "color": "#CF9AC4", 
        "font-size": "20px"
    }, 
    "nav-link": {
        "font-size": "16px", 
        "text-align": "left", 
        "margin": "5px 0",
        "padding": "14px 20px",
        "background-color": "rgba(255, 255, 255, 0.05)",
        "backdrop-filter": "blur(10px)",
        "-webkit-backdrop-filter": "blur(10px)",
        "border": "1px solid rgba(255, 255, 255, 0.1)",
        "border-radius": "15px",
        "color": "#ffffff",
        "font-weight": "500",
        "transition": "all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        "box-shadow": "0 4px 15px rgba(0, 0, 0, 0.1)",
    },
    "nav-link:hover": {
        "background-color": "rgba(255, 255, 255, 0.1)",
        "border-color": "rgba(207, 154, 196, 0.3)",
        "transform": "translateX(5px)",
    },
    "nav-link-selected": {
        "background": "linear-gradient(135deg, rgba(207, 154, 196, 0.3), rgba(155, 123, 168, 0.3))",
        "backdrop-filter": "blur(15px)",
        "-webkit-backdrop-filter": "blur(15px)",
        "border": "1px solid rgba(207, 154, 196, 0.5)",
        "color": "#ffffff",
        "font-weight": "600",
        "box-shadow": "0 8px 25px rgba(207, 154, 196, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2)",
    },
}

# HTML Components Functions
def get_profile_card_html(first_name):
    return f"""
        <div style='
            background: rgba(207, 154, 196, 0.15);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border: 1px solid rgba(207, 154, 196, 0.3);
            padding: 25px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 
                0 8px 32px 0 rgba(0, 0, 0, 0.37),
                inset 0 1px 0 0 rgba(255, 255, 255, 0.1);
        '>
            <div style='
                width: 70px;
                height: 70px;
                background: linear-gradient(135deg, rgba(207, 154, 196, 0.3), rgba(155, 123, 168, 0.3));
                backdrop-filter: blur(5px);
                border: 2px solid rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                margin: 0 auto 15px;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 35px;
                box-shadow: 0 4px 15px rgba(207, 154, 196, 0.3);
            '>
                👤
            </div>
            <h2 style='
                color: #ffffff; 
                margin: 0;
                font-size: 24px;
                font-weight: 600;
                letter-spacing: -0.5px;
            '>Welcome</h2>
            <h3 style='
                background: linear-gradient(90deg, #CF9AC4, #9b7ba8);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin: 5px 0 0 0;
                font-size: 20px;
                font-weight: 700;
            '>{first_name}</h3>
            <p style='
                color: rgba(255, 255, 255, 0.6); 
                font-size: 13px; 
                margin: 8px 0 0 0;
                font-weight: 500;
            '>Premium Member</p>
        </div>
    """

GLASS_DIVIDER_HTML = """
    <div style='
        height: 1px;
        background: linear-gradient(90deg, 
            transparent, 
            rgba(255, 255, 255, 0.2), 
            transparent
        );
        margin: 25px 0;
    '></div>
"""

GLASS_FOOTER_STATS_HTML = """
    <div style='
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        margin-top: 20px;
    '>
        <div style='display: flex; justify-content: space-around; text-align: center;'>
            <div>
                <p style='color: #CF9AC4; font-size: 20px; font-weight: 700; margin: 0;'>24</p>
                <p style='color: rgba(255,255,255,0.6); font-size: 11px; margin: 5px 0 0 0;'>Scans</p>
            </div>
            <div style='
                width: 1px; 
                background: linear-gradient(180deg, transparent, rgba(255,255,255,0.2), transparent);
            '></div>
            <div>
                <p style='color: #CF9AC4; font-size: 20px; font-weight: 700; margin: 0;'>98%</p>
                <p style='color: rgba(255,255,255,0.6); font-size: 11px; margin: 5px 0 0 0;'>Accuracy</p>
            </div>
            <div style='
                width: 1px; 
                background: linear-gradient(180deg, transparent, rgba(255,255,255,0.2), transparent);
            '></div>
            <div>
                <p style='color: #CF9AC4; font-size: 20px; font-weight: 700; margin: 0;'>12</p>
                <p style='color: rgba(255,255,255,0.6); font-size: 11px; margin: 5px 0 0 0;'>Projects</p>
            </div>
        </div>
    </div>
"""

GLASS_VERSION_BADGE_HTML = """
    <div style='
        text-align: center;
        margin-top: 20px;
        padding: 10px;
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    '>
        <p style='
            color: rgba(255, 255, 255, 0.4); 
            font-size: 11px; 
            margin: 0;
            font-weight: 500;
            letter-spacing: 0.5px;
        '>VERSION 1.0.0</p>
    </div>
"""
