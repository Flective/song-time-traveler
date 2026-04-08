"""
FIAT MUSICA v7.0 - THEME CONFIGURATION
Professional theme system with 5 themes
Edit colors, fonts, spacing here - no CSS knowledge needed
"""

# Google Fonts to load
GOOGLE_FONTS = [
    "Inter",
    "Montserrat", 
    "Work Sans",
    "Plus Jakarta Sans",
    "Outfit",
    "Crimson Text",
    "Libre Baskerville",
    "Orbitron",
    "Rajdhani",
    "Bebas Neue",
    "Roboto Condensed",
    "JetBrains Mono"
]

# Navigation structure - hierarchical organization
NAVIGATION_STRUCTURE = {
    "creative_studio": {
        "label": "Creative Studio",
        "tabs": ["My Album Builder", "Virtual Songs", "Personas", "Living Archive"]
    },
    "community_business": {
        "label": "Community & Business",
        "tabs": ["Founding Members", "Documentation", "Voting", "Reviews"]
    },
    "operations": {
        "label": "Operations",
        "tabs": ["Band HQ", "Artist Outreach", "Protosongs", "Analytics", "Settings"]
    }
}

# Persona to theme mappings
PERSONA_THEMES = {
    "meridian-quartet": "noir_jazz",
    "lumen-vox": "ethereal_minimal",
    "of-broken-light": "broken_light",
    "neon-room": "neon_synthwave"
}

# Theme definitions
THEMES = {
    "noir_jazz": {
        "name": "Noir Jazz",
        "description": "Sophisticated dark theme with gold accents. Late-night jazz club aesthetic.",
        "default": True,
        
        "fonts": {
            "heading": "Montserrat",
            "body": "Inter",
            "mono": "JetBrains Mono",
            "heading_weight": "600",
            "body_weight": "400"
        },
        
        "colors": {
            "bg_primary": "#2a2a2a",
            "bg_secondary": "#1f1f1f",
            "bg_card": "#333333",
            "bg_input": "#3a3a3a",
            "bg_hover": "#404040",
            "bg_sidebar": "#1a1a1a",
            
            "accent_primary": "#d4af37",
            "accent_secondary": "#8b7355",
            "accent_tertiary": "#c9a961",
            
            "text_primary": "#f5f5f5",
            "text_secondary": "#b0b0b0",
            "text_muted": "#707070",
            "text_inverse": "#1a1a1a",
            
            "success": "#4caf50",
            "warning": "#ff9800",
            "error": "#f44336",
            "info": "#2196f3",
            
            "border": "#404040",
            "border_light": "#4a4a4a"
        },
        
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
            "xxl": "3rem"
        },
        
        "typography": {
            "h1_size": "2.25rem",
            "h2_size": "1.75rem",
            "h3_size": "1.375rem",
            "h4_size": "1.125rem",
            "body_size": "1rem",
            "small_size": "0.875rem",
            "line_height": "1.6"
        },
        
        "effects": {
            "border_radius": "6px",
            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.3)",
            "box_shadow_hover": "0 4px 12px rgba(212, 175, 55, 0.15)",
            "transition": "all 0.2s ease"
        }
    },
    
    "neon_synthwave": {
        "name": "Neon Synthwave",
        "description": "Retro-futuristic with neon glow. Blade Runner meets 80s arcade.",
        "default": False,
        
        "fonts": {
            "heading": "Orbitron",
            "body": "Rajdhani",
            "mono": "JetBrains Mono",
            "heading_weight": "700",
            "body_weight": "400"
        },
        
        "colors": {
            "bg_primary": "#1a0033",
            "bg_secondary": "#120024",
            "bg_card": "#2a1045",
            "bg_input": "#3a1a5a",
            "bg_hover": "#4a2070",
            "bg_sidebar": "#0d001a",
            
            "accent_primary": "#ff006e",
            "accent_secondary": "#00f5ff",
            "accent_tertiary": "#bf00ff",
            
            "text_primary": "#ffffff",
            "text_secondary": "#d0d0ff",
            "text_muted": "#8080a0",
            "text_inverse": "#1a0033",
            
            "success": "#00ff88",
            "warning": "#ffaa00",
            "error": "#ff3366",
            "info": "#00f5ff",
            
            "border": "#6633aa",
            "border_light": "#7744bb"
        },
        
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
            "xxl": "3rem"
        },
        
        "typography": {
            "h1_size": "2.5rem",
            "h2_size": "1.875rem",
            "h3_size": "1.5rem",
            "h4_size": "1.25rem",
            "body_size": "1rem",
            "small_size": "0.875rem",
            "line_height": "1.5"
        },
        
        "effects": {
            "border_radius": "4px",
            "box_shadow": "0 0 20px rgba(255, 0, 110, 0.3)",
            "box_shadow_hover": "0 0 30px rgba(0, 245, 255, 0.4)",
            "transition": "all 0.3s ease"
        }
    },
    
    "broken_light": {
        "name": "Broken Light",
        "description": "Raw industrial aesthetic with rust accents. Alternative rock energy.",
        "default": False,
        
        "fonts": {
            "heading": "Bebas Neue",
            "body": "Roboto Condensed",
            "mono": "JetBrains Mono",
            "heading_weight": "400",
            "body_weight": "400"
        },
        
        "colors": {
            "bg_primary": "#2d2d2d",
            "bg_secondary": "#252525",
            "bg_card": "#383838",
            "bg_input": "#404040",
            "bg_hover": "#4a4a4a",
            "bg_sidebar": "#1d1d1d",
            
            "accent_primary": "#e07a5f",
            "accent_secondary": "#81b29a",
            "accent_tertiary": "#f2cc8f",
            
            "text_primary": "#f8f8f8",
            "text_secondary": "#c0c0c0",
            "text_muted": "#808080",
            "text_inverse": "#2d2d2d",
            
            "success": "#81b29a",
            "warning": "#f2cc8f",
            "error": "#e07a5f",
            "info": "#3d405b",
            
            "border": "#505050",
            "border_light": "#606060"
        },
        
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
            "xxl": "3rem"
        },
        
        "typography": {
            "h1_size": "2.75rem",
            "h2_size": "2rem",
            "h3_size": "1.5rem",
            "h4_size": "1.25rem",
            "body_size": "1rem",
            "small_size": "0.875rem",
            "line_height": "1.5"
        },
        
        "effects": {
            "border_radius": "2px",
            "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.4)",
            "box_shadow_hover": "0 4px 8px rgba(224, 122, 95, 0.2)",
            "transition": "all 0.15s ease"
        }
    },
    
    "ethereal_minimal": {
        "name": "Ethereal Minimal",
        "description": "Clean light theme with sage accents. Intimate and sophisticated.",
        "default": False,
        
        "fonts": {
            "heading": "Crimson Text",
            "body": "Work Sans",
            "mono": "JetBrains Mono",
            "heading_weight": "600",
            "body_weight": "400"
        },
        
        "colors": {
            "bg_primary": "#f5f5f0",
            "bg_secondary": "#eeeee8",
            "bg_card": "#ffffff",
            "bg_input": "#ffffff",
            "bg_hover": "#e8e8e0",
            "bg_sidebar": "#eaeae4",
            
            "accent_primary": "#8b9d83",
            "accent_secondary": "#6b7d63",
            "accent_tertiary": "#a8b8a0",
            
            "text_primary": "#2a2a2a",
            "text_secondary": "#555555",
            "text_muted": "#888888",
            "text_inverse": "#f5f5f0",
            
            "success": "#6b8f71",
            "warning": "#c9a961",
            "error": "#c17767",
            "info": "#7b8fa1",
            
            "border": "#d0d0c8",
            "border_light": "#e0e0d8"
        },
        
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.75rem",
            "xl": "2.5rem",
            "xxl": "3.5rem"
        },
        
        "typography": {
            "h1_size": "2.25rem",
            "h2_size": "1.75rem",
            "h3_size": "1.375rem",
            "h4_size": "1.125rem",
            "body_size": "1rem",
            "small_size": "0.875rem",
            "line_height": "1.7"
        },
        
        "effects": {
            "border_radius": "8px",
            "box_shadow": "0 1px 3px rgba(0, 0, 0, 0.08)",
            "box_shadow_hover": "0 2px 8px rgba(139, 157, 131, 0.15)",
            "transition": "all 0.25s ease"
        }
    },
    
    "platonic_ideal": {
        "name": "Platonic Ideal",
        "description": "Deep navy with silver accents. Academic elegance for documentation.",
        "default": False,
        
        "fonts": {
            "heading": "Libre Baskerville",
            "body": "Plus Jakarta Sans",
            "mono": "JetBrains Mono",
            "heading_weight": "700",
            "body_weight": "400"
        },
        
        "colors": {
            "bg_primary": "#0a1128",
            "bg_secondary": "#070d1d",
            "bg_card": "#141e38",
            "bg_input": "#1a2848",
            "bg_hover": "#243258",
            "bg_sidebar": "#050912",
            
            "accent_primary": "#c0c0c0",
            "accent_secondary": "#a0a0b0",
            "accent_tertiary": "#e0e0e8",
            
            "text_primary": "#f0f0f0",
            "text_secondary": "#b0b0c0",
            "text_muted": "#707088",
            "text_inverse": "#0a1128",
            
            "success": "#70a070",
            "warning": "#c0a060",
            "error": "#c07070",
            "info": "#7090c0",
            
            "border": "#2a3a5a",
            "border_light": "#3a4a6a"
        },
        
        "spacing": {
            "xs": "0.25rem",
            "sm": "0.5rem",
            "md": "1rem",
            "lg": "1.5rem",
            "xl": "2rem",
            "xxl": "3rem"
        },
        
        "typography": {
            "h1_size": "2.25rem",
            "h2_size": "1.75rem",
            "h3_size": "1.375rem",
            "h4_size": "1.125rem",
            "body_size": "1rem",
            "small_size": "0.875rem",
            "line_height": "1.65"
        },
        
        "effects": {
            "border_radius": "4px",
            "box_shadow": "0 2px 6px rgba(0, 0, 0, 0.4)",
            "box_shadow_hover": "0 4px 12px rgba(192, 192, 192, 0.1)",
            "transition": "all 0.2s ease"
        }
    }
}

# Helper functions
def get_default_theme():
    """Get the default theme name"""
    for name, theme in THEMES.items():
        if theme.get("default"):
            return name
    return "noir_jazz"

def get_theme(theme_name):
    """Get theme by name, fallback to default"""
    return THEMES.get(theme_name, THEMES[get_default_theme()])

def get_all_themes():
    """Get list of all theme names and display names"""
    return [(name, theme["name"]) for name, theme in THEMES.items()]

def get_persona_theme(persona_id):
    """Get theme for a specific persona"""
    return PERSONA_THEMES.get(persona_id, get_default_theme())
