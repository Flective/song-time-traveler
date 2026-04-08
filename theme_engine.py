"""
FIAT MUSICA v7.0 - THEME ENGINE
Generates CSS from theme configuration
"""

from theme_config import THEMES, GOOGLE_FONTS, get_theme

def get_google_fonts_import():
    """Generate Google Fonts import URL"""
    font_families = []
    for font in GOOGLE_FONTS:
        # Replace spaces with + for URL
        font_url = font.replace(" ", "+")
        font_families.append(f"family={font_url}:wght@400;500;600;700")
    
    return f"@import url('https://fonts.googleapis.com/css2?{'&'.join(font_families)}&display=swap');"

def generate_css_variables(theme):
    """Generate CSS custom properties from theme"""
    colors = theme["colors"]
    fonts = theme["fonts"]
    spacing = theme["spacing"]
    typography = theme["typography"]
    effects = theme["effects"]
    
    return f"""
    :root {{
        /* Colors - Backgrounds */
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --bg-card: {colors['bg_card']};
        --bg-input: {colors['bg_input']};
        --bg-hover: {colors['bg_hover']};
        --bg-sidebar: {colors['bg_sidebar']};
        
        /* Colors - Accents */
        --accent-primary: {colors['accent_primary']};
        --accent-secondary: {colors['accent_secondary']};
        --accent-tertiary: {colors['accent_tertiary']};
        
        /* Colors - Text */
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --text-muted: {colors['text_muted']};
        --text-inverse: {colors['text_inverse']};
        
        /* Colors - Status */
        --color-success: {colors['success']};
        --color-warning: {colors['warning']};
        --color-error: {colors['error']};
        --color-info: {colors['info']};
        
        /* Colors - Borders */
        --border-color: {colors['border']};
        --border-light: {colors['border_light']};
        
        /* Fonts */
        --font-heading: '{fonts['heading']}', sans-serif;
        --font-body: '{fonts['body']}', sans-serif;
        --font-mono: '{fonts['mono']}', monospace;
        --font-heading-weight: {fonts['heading_weight']};
        --font-body-weight: {fonts['body_weight']};
        
        /* Typography */
        --h1-size: {typography['h1_size']};
        --h2-size: {typography['h2_size']};
        --h3-size: {typography['h3_size']};
        --h4-size: {typography['h4_size']};
        --body-size: {typography['body_size']};
        --small-size: {typography['small_size']};
        --line-height: {typography['line_height']};
        
        /* Spacing */
        --space-xs: {spacing['xs']};
        --space-sm: {spacing['sm']};
        --space-md: {spacing['md']};
        --space-lg: {spacing['lg']};
        --space-xl: {spacing['xl']};
        --space-xxl: {spacing['xxl']};
        
        /* Effects */
        --border-radius: {effects['border_radius']};
        --box-shadow: {effects['box_shadow']};
        --box-shadow-hover: {effects['box_shadow_hover']};
        --transition: {effects['transition']};
    }}
    """

def generate_component_css():
    """Generate CSS for Streamlit components using variables"""
    return """
    /* ===== BASE STYLES ===== */
    
    .stApp {
        background-color: var(--bg-primary);
        color: var(--text-primary);
        font-family: var(--font-body);
        font-size: var(--body-size);
        line-height: var(--line-height);
    }
    
    /* Main content area */
    .main .block-container {
        background-color: var(--bg-primary);
        padding: var(--space-lg) var(--space-xl);
        max-width: 1200px;
    }
    
    /* ===== SIDEBAR ===== */
    
    [data-testid="stSidebar"] {
        background-color: var(--bg-sidebar);
        border-right: 1px solid var(--border-color);
    }
    
    [data-testid="stSidebar"] .block-container {
        padding: var(--space-md);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary);
    }
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label {
        color: var(--text-secondary);
    }
    
    /* ===== TYPOGRAPHY ===== */
    
    h1, .stMarkdown h1 {
        font-family: var(--font-heading);
        font-weight: var(--font-heading-weight);
        font-size: var(--h1-size);
        color: var(--text-primary);
        margin-bottom: var(--space-md);
    }
    
    h2, .stMarkdown h2 {
        font-family: var(--font-heading);
        font-weight: var(--font-heading-weight);
        font-size: var(--h2-size);
        color: var(--text-primary);
        margin-bottom: var(--space-md);
    }
    
    h3, .stMarkdown h3 {
        font-family: var(--font-heading);
        font-weight: var(--font-heading-weight);
        font-size: var(--h3-size);
        color: var(--text-primary);
        margin-bottom: var(--space-sm);
    }
    
    h4, .stMarkdown h4 {
        font-family: var(--font-heading);
        font-weight: var(--font-heading-weight);
        font-size: var(--h4-size);
        color: var(--text-primary);
    }
    
    p, .stMarkdown p {
        color: var(--text-primary);
        font-size: var(--body-size);
        line-height: var(--line-height);
    }
    
    /* Captions and small text */
    .stCaption, small, .caption {
        color: var(--text-muted);
        font-size: var(--small-size);
    }
    
    /* ===== BUTTONS ===== */
    
    .stButton > button {
        background-color: var(--accent-primary);
        color: var(--text-inverse);
        border: none;
        border-radius: var(--border-radius);
        padding: var(--space-sm) var(--space-md);
        font-family: var(--font-body);
        font-weight: 500;
        transition: var(--transition);
        box-shadow: var(--box-shadow);
    }
    
    .stButton > button:hover {
        background-color: var(--accent-secondary);
        box-shadow: var(--box-shadow-hover);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary button variant */
    .stButton > button[kind="primary"] {
        background-color: var(--accent-primary);
    }
    
    /* Secondary button variant */
    .stButton > button[kind="secondary"] {
        background-color: transparent;
        border: 1px solid var(--accent-primary);
        color: var(--accent-primary);
    }
    
    .stButton > button[kind="secondary"]:hover {
        background-color: var(--accent-primary);
        color: var(--text-inverse);
    }
    
    /* ===== FORM INPUTS ===== */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > div,
    .stMultiSelect > div > div > div,
    .stNumberInput > div > div > input,
    .stDateInput > div > div > input {
        background-color: var(--bg-input);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: var(--space-sm);
        font-family: var(--font-body);
        transition: var(--transition);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > div:focus-within,
    .stNumberInput > div > div > input:focus {
        border-color: var(--accent-primary);
        box-shadow: 0 0 0 2px rgba(212, 175, 55, 0.2);
    }
    
    /* Input labels */
    .stTextInput label,
    .stTextArea label,
    .stSelectbox label,
    .stMultiSelect label,
    .stNumberInput label,
    .stDateInput label,
    .stCheckbox label,
    .stRadio label {
        color: var(--text-secondary);
        font-weight: 500;
        font-size: var(--small-size);
    }
    
    /* ===== TABS ===== */
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: var(--bg-secondary);
        border-radius: var(--border-radius);
        padding: var(--space-xs);
        gap: var(--space-xs);
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        color: var(--text-secondary);
        border-radius: var(--border-radius);
        padding: var(--space-sm) var(--space-md);
        font-family: var(--font-body);
        font-weight: 500;
        transition: var(--transition);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--bg-hover);
        color: var(--text-primary);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent-primary) !important;
        color: var(--text-inverse) !important;
    }
    
    /* ===== METRICS ===== */
    
    [data-testid="stMetricValue"] {
        color: var(--accent-primary);
        font-family: var(--font-heading);
        font-weight: var(--font-heading-weight);
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary);
        font-size: var(--small-size);
    }
    
    [data-testid="stMetricDelta"] {
        font-size: var(--small-size);
    }
    
    /* ===== EXPANDERS ===== */
    
    .streamlit-expanderHeader {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        color: var(--text-primary);
        font-weight: 500;
        transition: var(--transition);
    }
    
    .streamlit-expanderHeader:hover {
        background-color: var(--bg-hover);
        border-color: var(--accent-primary);
    }
    
    .streamlit-expanderContent {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-top: none;
        border-radius: 0 0 var(--border-radius) var(--border-radius);
        padding: var(--space-md);
    }
    
    /* ===== CONTAINERS & CARDS ===== */
    
    [data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: var(--space-md);
    }
    
    /* Bordered containers */
    div[data-testid="stHorizontalBlock"]:has(> div[data-testid="column"]) {
        gap: var(--space-md);
    }
    
    /* ===== DATAFRAMES & TABLES ===== */
    
    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
    }
    
    .stDataFrame [data-testid="stDataFrameResizable"] {
        background-color: var(--bg-card);
    }
    
    .stDataFrame th {
        background-color: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    .stDataFrame td {
        background-color: var(--bg-card) !important;
        color: var(--text-primary) !important;
    }
    
    .stDataFrame tr:hover td {
        background-color: var(--bg-hover) !important;
    }
    
    /* ===== ALERTS ===== */
    
    .stAlert {
        border-radius: var(--border-radius);
        padding: var(--space-md);
    }
    
    .stAlert[data-baseweb="notification"][kind="info"] {
        background-color: color-mix(in srgb, var(--color-info) 15%, var(--bg-card));
        border-left: 4px solid var(--color-info);
    }
    
    .stAlert[data-baseweb="notification"][kind="success"] {
        background-color: color-mix(in srgb, var(--color-success) 15%, var(--bg-card));
        border-left: 4px solid var(--color-success);
    }
    
    .stAlert[data-baseweb="notification"][kind="warning"] {
        background-color: color-mix(in srgb, var(--color-warning) 15%, var(--bg-card));
        border-left: 4px solid var(--color-warning);
    }
    
    .stAlert[data-baseweb="notification"][kind="error"] {
        background-color: color-mix(in srgb, var(--color-error) 15%, var(--bg-card));
        border-left: 4px solid var(--color-error);
    }
    
    /* ===== PROGRESS BARS ===== */
    
    .stProgress > div > div {
        background-color: var(--bg-secondary);
        border-radius: var(--border-radius);
    }
    
    .stProgress > div > div > div {
        background-color: var(--accent-primary);
        border-radius: var(--border-radius);
    }
    
    /* ===== DIVIDERS ===== */
    
    hr, .stDivider {
        border-color: var(--border-color);
        margin: var(--space-lg) 0;
    }
    
    /* ===== CHECKBOXES & RADIOS ===== */
    
    .stCheckbox [data-testid="stMarkdownContainer"] p {
        color: var(--text-primary);
    }
    
    .stRadio [data-testid="stMarkdownContainer"] p {
        color: var(--text-primary);
    }
    
    /* ===== CODE BLOCKS ===== */
    
    code, .stCodeBlock {
        background-color: var(--bg-secondary);
        color: var(--accent-tertiary);
        font-family: var(--font-mono);
        border-radius: var(--border-radius);
        padding: var(--space-xs) var(--space-sm);
    }
    
    pre {
        background-color: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
        padding: var(--space-md);
    }
    
    /* ===== LINKS ===== */
    
    a {
        color: var(--accent-primary);
        text-decoration: none;
        transition: var(--transition);
    }
    
    a:hover {
        color: var(--accent-tertiary);
        text-decoration: underline;
    }
    
    /* ===== SCROLLBARS ===== */
    
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-secondary);
    }
    
    /* ===== TOOLTIPS ===== */
    
    [data-baseweb="tooltip"] {
        background-color: var(--bg-card);
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        border-radius: var(--border-radius);
    }
    
    /* ===== NAVIGATION CATEGORIES ===== */
    
    .nav-category {
        color: var(--text-muted);
        font-size: var(--small-size);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: var(--space-lg);
        margin-bottom: var(--space-sm);
        padding-left: var(--space-sm);
    }
    
    .nav-category:first-child {
        margin-top: 0;
    }
    """

def generate_full_css(theme_name):
    """Generate complete CSS for a theme"""
    theme = get_theme(theme_name)
    
    css = f"""
    <style>
    {get_google_fonts_import()}
    
    {generate_css_variables(theme)}
    
    {generate_component_css()}
    </style>
    """
    
    return css

def inject_theme_css(theme_name="noir_jazz"):
    """Inject theme CSS into Streamlit"""
    import streamlit as st
    css = generate_full_css(theme_name)
    st.markdown(css, unsafe_allow_html=True)
