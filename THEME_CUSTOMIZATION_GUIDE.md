# 🎨 FIAT MUSICA v7.0 - THEME CUSTOMIZATION GUIDE

## Complete Guide to Visual Themes & Styling

---

## OVERVIEW

Fiat Musica v7.0 includes a complete theme system with:
- **5 Professional Themes** (ready to use)
- **Full CSS Variable System** (easy editing)
- **Persona-Specific Themes** (automatic aesthetic switching)
- **Google Fonts Integration** (elegant typography)
- **All Parameters Editable** (colors, fonts, spacing, effects)

---

## 5 BUILT-IN THEMES

### 1. NOIR JAZZ (Default)
**Aesthetic:** Sophisticated dark with gold accents
**Best For:** Meridian Quartet, sophisticated content
**Colors:**
- Background: Dark charcoal (#2a2a2a)
- Accent: Gold (#d4af37)
- Vibe: Late-night jazz club, Blue Note Records

**Fonts:**
- Headings: Montserrat (geometric, clean)
- Body: Inter (modern, readable)

---

### 2. NEON SYNTHWAVE
**Aesthetic:** Retro-futuristic with neon glow
**Best For:** Neon Room, electronic/synth content
**Colors:**
- Background: Deep purple (#1a0033)
- Accents: Neon pink (#ff006e), Cyan (#00f5ff)
- Vibe: Blade Runner, 80s arcade, synthwave

**Fonts:**
- Headings: Orbitron (futuristic)
- Body: Rajdhani (technical)

**Special Effects:** Glowing shadows, neon borders

---

### 3. BROKEN LIGHT
**Aesthetic:** Raw alternative with industrial feel
**Best For:** Of Broken Light, rock/alternative content
**Colors:**
- Background: Concrete gray (#2d2d2d)
- Accent: Rust orange (#e07a5f)
- Vibe: Indie venue posters, alternative aesthetic

**Fonts:**
- Headings: Bebas Neue (condensed, bold)
- Body: Roboto Condensed (tight, industrial)

**Special Effects:** Minimal, high contrast, rough edges

---

### 4. ETHEREAL MINIMAL
**Aesthetic:** Clean sophistication with lots of space
**Best For:** Lumen Vox, intimate/folk content
**Colors:**
- Background: Off-white/cream (#f5f5f0)
- Accent: Soft sage (#8b9d83)
- Vibe: A24 film posters, indie folk albums

**Fonts:**
- Headings: Crimson Text (elegant serif)
- Body: Work Sans (clean sans)

**Special Effects:** Generous whitespace, subtle shadows

---

### 5. PLATONIC IDEAL
**Aesthetic:** Philosophical modern with academic elegance
**Best For:** Framework documentation, intellectual content
**Colors:**
- Background: Deep navy (#0a1128)
- Accent: Silver/platinum (#c0c0c0)
- Vibe: Academic journals, philosophy texts

**Fonts:**
- Headings: Libre Baskerville (classical serif)
- Body: Plus Jakarta Sans (modern sans)

**Special Effects:** Refined, understated, intellectual

---

## HOW TO SWITCH THEMES

### In the App:
1. Go to **Settings** tab (far right)
2. Find **"Visual Theme"** section
3. Select theme from dropdown
4. Click **"Apply Theme"**
5. Page refreshes with new theme

### Persona-Specific Auto-Switching:
When viewing specific personas, their theme automatically applies:
- **Meridian Quartet** → Noir Jazz
- **Lumen Vox** → Ethereal Minimal
- **Of Broken Light** → Broken Light
- **Neon Room** → Neon Synthwave

---

## HOW TO CUSTOMIZE THEMES

### File Location:
`/mnt/user-data/outputs/theme_config.py`

### Structure:
All themes defined in Python dictionary format - NO CSS knowledge needed!

### Example - Editing Noir Jazz Colors:

```python
"noir_jazz": {
    "name": "Noir Jazz",
    
    "colors": {
        "bg_primary": "#2a2a2a",      # ← Change this!
        "bg_secondary": "#1a1a1a",    # ← Change this!
        "accent_primary": "#d4af37",  # ← Change this!
        # ... etc
    }
}
```

**Simple Process:**
1. Open `theme_config.py`
2. Find the theme you want to edit
3. Change the hex color codes
4. Save file
5. Reload app
6. Theme updates automatically!

---

## EDITABLE PARAMETERS

### 1. COLORS
```python
"colors": {
    # Backgrounds
    "bg_primary": "#2a2a2a",      # Main background
    "bg_secondary": "#1a1a1a",    # Sidebar, alternate sections
    "bg_card": "#333333",         # Cards, containers
    "bg_input": "#3a3a3a",        # Form inputs
    "bg_hover": "#404040",        # Hover states
    
    # Accents
    "accent_primary": "#d4af37",   # Primary accent (buttons, highlights)
    "accent_secondary": "#8b7355", # Secondary accent
    "accent_tertiary": "#c9a961",  # Tertiary accent
    
    # Text
    "text_primary": "#f5f5f5",     # Main text
    "text_secondary": "#a0a0a0",   # Secondary text
    "text_muted": "#707070",       # Muted text
    "text_inverse": "#1a1a1a",     # Text on light backgrounds
    
    # Status
    "success": "#4caf50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196f3",
    
    # Borders
    "border": "#404040",
    "border_light": "#4a4a4a"
}
```

---

### 2. FONTS
```python
"fonts": {
    "heading": "Montserrat",       # Heading font family
    "body": "Inter",               # Body text font
    "mono": "JetBrains Mono",      # Code/monospace font
    "heading_weight": "600",       # Heading weight (100-900)
    "body_weight": "400"           # Body weight (100-900)
}
```

**Available Google Fonts:**
Already loaded and ready to use:
- Montserrat, Inter, Outfit, Work Sans, Plus Jakarta Sans
- JetBrains Mono (monospace)
- Crimson Text, Libre Baskerville (serifs)
- Orbitron, Rajdhani (futuristic)
- Roboto Condensed, Bebas Neue (condensed)

**To add more fonts:**
Edit `GOOGLE_FONTS` list at top of `theme_config.py`

---

### 3. SPACING
```python
"spacing": {
    "xs": "0.25rem",
    "sm": "0.5rem",
    "md": "1rem",
    "lg": "1.5rem",
    "xl": "2rem",
    "xxl": "3rem"
}
```

---

### 4. TYPOGRAPHY SIZES
```python
"typography": {
    "h1_size": "2.5rem",       # Main title size
    "h2_size": "2rem",         # Section headers
    "h3_size": "1.5rem",       # Subsection headers
    "h4_size": "1.25rem",      # Minor headers
    "body_size": "1rem",       # Body text
    "small_size": "0.875rem",  # Small text/captions
    "line_height": "1.6"       # Line spacing
}
```

---

### 5. VISUAL EFFECTS
```python
"effects": {
    "border_radius": "8px",    # Corner rounding
    "box_shadow": "0 4px 6px rgba(0, 0, 0, 0.3)",  # Card shadow
    "box_shadow_hover": "0 6px 12px rgba(212, 175, 55, 0.2)",  # Hover shadow
    "transition": "all 0.3s ease"  # Animation speed
}
```

---

## CREATING A NEW THEME

### Step-by-Step:

1. **Open theme_config.py**

2. **Copy an existing theme** (e.g., noir_jazz)

3. **Paste and rename:**
```python
"my_custom_theme": {
    "name": "My Custom Theme",
    "description": "Your description here",
    "default": False,
    
    # Copy all sections from an existing theme
    "fonts": { ... },
    "colors": { ... },
    "spacing": { ... },
    "typography": { ... },
    "effects": { ... }
}
```

4. **Edit the parameters** to your liking

5. **Save file**

6. **Reload app** - new theme appears in Settings dropdown!

---

## COLOR SCHEME CREATION

### Tools to Help:
- **Coolors.co** - Generate color palettes
- **Adobe Color** - Color wheel tool
- **Paletton** - Color scheme designer

### Tips:
1. **Start with 1 primary accent** (this is your "brand color")
2. **Choose background darkness** (light, medium, dark)
3. **Ensure text contrast** (WCAG AA: 4.5:1 minimum)
4. **Test with real content** (don't just look at swatches)
5. **Consider accessibility** (colorblind-friendly)

### Good Contrast Ratios:
- Dark themes: Light text (#f5f5f5) on dark bg (#2a2a2a)
- Light themes: Dark text (#2a2a2a) on light bg (#f5f5f0)
- Accent text: Should pop but still readable

---

## FONT PAIRING GUIDE

### Classic Combinations:
1. **Serif Heading + Sans Body**
   - Libre Baskerville + Inter
   - Crimson Text + Work Sans

2. **Sans Heading + Sans Body** (different weights)
   - Montserrat + Inter
   - Outfit + Plus Jakarta Sans

3. **Display Heading + Clean Body**
   - Bebas Neue + Roboto Condensed
   - Orbitron + Rajdhani

### Font Personality:
- **Montserrat** - Geometric, modern, professional
- **Inter** - Neutral, readable, versatile
- **Crimson Text** - Classical, elegant, literary
- **Orbitron** - Futuristic, tech, sci-fi
- **Bebas Neue** - Bold, industrial, raw
- **Work Sans** - Clean, friendly, contemporary

---

## ADVANCED: CSS VARIABLES

If you want COMPLETE control, edit the generated CSS variables directly.

### Where They Are:
`theme_engine.py` generates CSS from your theme config.

### How They Work:
```css
:root {
  --bg-primary: #2a2a2a;
  --accent-primary: #d4af37;
  /* ... etc */
}

/* Used throughout CSS like: */
.main {
    background-color: var(--bg-primary);
}

.stButton button {
    background-color: var(--accent-primary);
}
```

### To Edit Directly:
1. Run `python theme_engine.py` to generate CSS files
2. Edit `theme_[name].css`
3. Advanced customization possible

---

## TROUBLESHOOTING

### Theme Not Applying:
1. Check you clicked "Apply Theme" in Settings
2. Refresh browser (Ctrl+R or Cmd+R)
3. Check for typos in `theme_config.py`
4. Verify hex codes are valid (6 digits, start with #)

### Colors Look Wrong:
- Check contrast ratios (text must be readable)
- Verify hex codes format: `#rrggbb`
- Test in both dark and light areas

### Fonts Not Loading:
- Check font name spelling in `theme_config.py`
- Verify font is in `GOOGLE_FONTS` list
- Check internet connection (fonts load from Google)

### CSS Not Updating:
- Streamlit caches CSS
- Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Restart Streamlit server

---

## PERSONA-SPECIFIC STYLING

### How It Works:
When you view a persona page (e.g., Meridian Quartet), their theme automatically applies.

### Mappings:
Defined in `theme_config.py`:
```python
PERSONA_THEMES = {
    "meridian-quartet": "noir_jazz",
    "lumen-vox": "ethereal_minimal",
    "of-broken-light": "broken_light",
    "neon-room": "neon_synthwave"
}
```

### To Add New Persona Themes:
1. Create the persona
2. Add mapping to `PERSONA_THEMES`
3. When viewing that persona, theme auto-applies

---

## EXPORT THEMES

### For External Use:
Run this to generate standalone CSS files:

```bash
cd /mnt/user-data/outputs
python theme_engine.py
```

Generates:
- `theme_noir_jazz.css`
- `theme_neon_synthwave.css`
- `theme_broken_light.css`
- `theme_ethereal_minimal.css`
- `theme_platonic_ideal.css`

Use these in any website!

---

## BEST PRACTICES

### DO:
✅ Test themes with real content
✅ Maintain consistent spacing
✅ Ensure good text contrast
✅ Use theme for branding
✅ Backup before major edits

### DON'T:
❌ Use too many accent colors
❌ Ignore accessibility
❌ Make text unreadable
❌ Over-animate everything
❌ Edit theme_engine.py unless you know CSS

---

## QUICK REFERENCE

### Common Tweaks:

**Make background darker:**
```python
"bg_primary": "#1a1a1a"  # Instead of #2a2a2a
```

**Change accent color:**
```python
"accent_primary": "#your_color_here"
```

**Increase font sizes:**
```python
"h1_size": "3rem"  # Instead of 2.5rem
"body_size": "1.1rem"  # Instead of 1rem
```

**More rounded corners:**
```python
"border_radius": "12px"  # Instead of 8px
```

**Softer shadows:**
```python
"box_shadow": "0 2px 4px rgba(0, 0, 0, 0.2)"  # Lighter
```

---

## FUTURE ENHANCEMENTS

Potential additions:
- Theme import/export
- Visual theme editor in Settings
- More pre-built themes
- Seasonal themes
- User-submitted theme library

---

## SUPPORT

### Documentation:
- Main README: `FIAT_MUSICA_V7_README.md`
- This file: `THEME_CUSTOMIZATION_GUIDE.md`

### Files to Know:
- **theme_config.py** - Edit themes here (easy!)
- **theme_engine.py** - Generates CSS (advanced)
- **fiat_musica_v7_platonic.py** - Main app (uses themes)

---

**FIAT MUSICA v7.0 THEME SYSTEM**
*Professional Design Meets Easy Customization*

🎨 Five themes ready to use
✏️ All parameters editable
🎭 Persona-specific styling
🎹 Beautiful by default

---
