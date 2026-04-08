import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import random

# Theme system imports
from theme_config import (
    THEMES, 
    NAVIGATION_STRUCTURE, 
    PERSONA_THEMES,
    get_default_theme, 
    get_theme, 
    get_all_themes,
    get_persona_theme
)
from theme_engine import inject_theme_css

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Fiat Musica v7.0: The Platonic Album OS", 
    layout="wide", 
    page_icon="")

# File paths
CSV_FILE = 'catalog.csv'
SETTINGS_FILE = 'settings.json'
VIRTUAL_SONGS_FILE = 'virtual_songs.json'
PERSONAS_FILE = 'personas.json'
LIVING_ARCHIVE_FILE = 'living_archive.json'
MY_ALBUMS_FILE = 'my_albums.json'
FOUNDING_MEMBERS_FILE = 'founding_members.json'
DOCUMENTATION_FILE = 'documentation_library.json'
VOTES_FILE = 'votes.json'
REVIEWS_FILE = 'reviews.json'
ARTIST_TARGETS_FILE = 'artist_targets.json'
PROTOSONGS_FILE = 'protosongs.json'
BAND_FILE = 'band_data.json'
NOTES_FILE = 'page_notes.json'

# --- DEFAULT PERSONAS ---
DEFAULT_PERSONAS = {
"meridian-quartet": {
"persona_id":"meridian-quartet",
"name":"The Meridian Quartet",
"type":"jazz_ensemble",
"brand_identity": {
"visual_style":"Noir sophistication",
"color_palette": ["Deep Blue","Gold Accent","Cream"],
"typography":"Serif Elegant" },
"musical_identity": {
"genre":"Jazz",
"instrumentation": ["Piano","Upright Bass","Drums","Saxophone"],
"arrangement_style":"Sophisticated swing",
"tempo_preference":"Moderate to slow",
"dynamic_range":"Subtle dynamics" },
"narrative":"Late-night sophistication, urbane reflection",
"target_demographic":"40-65, jazz aficionados, NPR listeners",
"tracks_performed": [],
"created": datetime.now().strftime("%Y-%m-%d"),
"active": True
    },
"lumen-vox": {
"persona_id":"lumen-vox",
"name":"Lumen Vox",
"type":"female_vocalist",
"brand_identity": {
"visual_style":"Ethereal intimate",
"color_palette": ["Soft Pink","White","Silver"],
"typography":"Sans-serif minimal" },
"musical_identity": {
"genre":"Acoustic Folk",
"instrumentation": ["Acoustic Guitar","Subtle Strings","Female Vocal"],
"arrangement_style":"Minimalist intimate",
"tempo_preference":"Slow to moderate",
"dynamic_range":"Quiet to medium" },
"narrative":"Vulnerable confessional, bedroom intimacy",
"target_demographic":"25-40 female, Phoebe Bridgers fans, introspective listeners",
"tracks_performed": [],
"created": datetime.now().strftime("%Y-%m-%d"),
"active": True
    },
"of-broken-light": {
"persona_id":"of-broken-light",
"name":"Of Broken Light",
"type":"live_band",
"brand_identity": {
"visual_style":"Raw alternative rock",
"color_palette": ["Black","White","Red Accent"],
"typography":"Bold sans-serif" },
"musical_identity": {
"genre":"Alternative Rock",
"instrumentation": ["Electric Guitar","Bass","Drums","Vocals"],
"arrangement_style":"Full band electric",
"tempo_preference":"Moderate to fast",
"dynamic_range":"Medium to loud" },
"narrative":"Raw emotional intensity, authentic rock energy",
"target_demographic":"30-55 rock fans, alternative music lovers",
"band_members": [
    {"name":"Jim Gannaway","role":"Vocals/Guitar","status":"Founding"},
    {"name":"TBD","role":"Lead Guitar","status":"Recruiting"},
    {"name":"TBD","role":"Bass","status":"Recruiting"},
    {"name":"TBD","role":"Drums","status":"Recruiting"}
    ],
"tracks_performed": [],
"created": datetime.now().strftime("%Y-%m-%d"),
"active": True
    },
"neon-room": {
"persona_id":"neon-room",
"name":"Neon Room",
"type":"synth_pop",
"brand_identity": {
"visual_style":"Retro-futuristic pop",
"color_palette": ["Neon Pink","Electric Blue","Purple"],
"typography":"Geometric modern" },
"musical_identity": {
"genre":"Synth Pop / Electronic",
"instrumentation": ["Synthesizers","Drum Machine","Processed Vocals"],
"arrangement_style":"Layered electronic",
"tempo_preference":"Moderate to fast",
"dynamic_range":"Consistent electronic" },
"narrative":"Nostalgia meets future, catchy electronic hooks",
"target_demographic":"18-35, electronic music fans, playlist listeners",
"tracks_performed": [],
"created": datetime.now().strftime("%Y-%m-%d"),
"active": True
    }
}

# --- DOCUMENTATION CATEGORIES ---
DOCUMENTATION_CATEGORIES = {
"philosophy":"Philosophy & Vision",
"methodology":"Methodology & Process",
"business":"Business Model",
"case_studies":"Case Studies",
"technical":"Technical Documentation",
"legal":"Legal & IP",
"partnerships":"Strategic Partnerships"}

# --- CORE FUNCTIONS ---

def load_json_file(filepath, default=None):
    """Load JSON file with error handling"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except:
            return default if default is not None else {}
    return default if default is not None else {}

def save_json_file(filepath, data):
    """Save JSON file with error handling"""
    try:
    with open(filepath, 'w') as f:
    json.dump(data, f, indent=2)
    return True
    except Exception as e:
    st.error(f"Error saving {filepath}: {str(e)}")
    return False

def load_personas():
    """Load personas, create defaults if needed"""
    personas = load_json_file(PERSONAS_FILE, {})
    if not personas:
    personas = DEFAULT_PERSONAS.copy()
    save_json_file(PERSONAS_FILE, personas)
    return personas

def save_personas(personas):
    """Save personas"""
    return save_json_file(PERSONAS_FILE, personas)

def load_virtual_songs():
    """Load virtual songs (the Platonic ideals)"""
    return load_json_file(VIRTUAL_SONGS_FILE, {})

def save_virtual_songs(songs):
    """Save virtual songs"""
    return save_json_file(VIRTUAL_SONGS_FILE, songs)

def load_living_archive():
    """Load living archive data"""
    return load_json_file(LIVING_ARCHIVE_FILE, {})

def save_living_archive(archive):
    """Save living archive"""
    return save_json_file(LIVING_ARCHIVE_FILE, archive)

def load_my_albums():
    """Load user-configured albums"""
    return load_json_file(MY_ALBUMS_FILE, {})

def save_my_albums(albums):
    """Save My Albums"""
    return save_json_file(MY_ALBUMS_FILE, albums)

def load_founding_members():
    """Load founding members"""
    return load_json_file(FOUNDING_MEMBERS_FILE, {})

def save_founding_members(members):
    """Save founding members"""
    return save_json_file(FOUNDING_MEMBERS_FILE, members)

def load_documentation():
    """Load documentation library"""
    return load_json_file(DOCUMENTATION_FILE, {})

def save_documentation(docs):
    """Save documentation library"""
    return save_json_file(DOCUMENTATION_FILE, docs)

def load_votes():
    """Load voting data"""
    return load_json_file(VOTES_FILE, {})

def save_votes(votes):
    """Save votes"""
    return save_json_file(VOTES_FILE, votes)

def load_reviews():
    """Load reviews"""
    return load_json_file(REVIEWS_FILE, {})

def save_reviews(reviews):
    """Save reviews"""
    return save_json_file(REVIEWS_FILE, reviews)

def load_page_notes():
    """Load page notes"""
    return load_json_file(NOTES_FILE, {})

def save_page_notes(notes):
    """Save page notes"""
    return save_json_file(NOTES_FILE, notes)

def get_page_note(page_id):
    """Get note for specific page"""
    notes = load_page_notes()
    return notes.get(page_id,"")

def save_page_note(page_id, note_text):
    """Save note for specific page"""
    notes = load_page_notes()
    notes[page_id] = note_text
    save_page_notes(notes)

def render_notes_section(page_id, page_title):
    """Render expandable notes section for any page"""
    with st.expander(f"Notes: {page_title}", expanded=False):
    current_note = get_page_note(page_id)
 
    st.markdown("**Purpose:** Document strategy, decisions, and ideas for this page")
 
    note_text = st.text_area(
"Notes",
    value=current_note,
    height=200,
    key=f"notes_{page_id}",
    placeholder="Enter notes about this page's purpose, strategy, decisions, or future ideas...",
    label_visibility="collapsed" )
 
    col1, col2 = st.columns([1, 5])
    with col1:
    if st.button("Save Note", key=f"save_note_{page_id}"):
    save_page_note(page_id, note_text)
    st.success("Note saved!")
 
    if current_note:
    with col2:
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- INITIALIZE STATE ---
if 'personas' not in st.session_state:
    st.session_state.personas = load_personas()
if 'virtual_songs' not in st.session_state:
    st.session_state.virtual_songs = load_virtual_songs()
if 'living_archive' not in st.session_state:
    st.session_state.living_archive = load_living_archive()
if 'my_albums' not in st.session_state:
    st.session_state.my_albums = load_my_albums()
if 'founding_members' not in st.session_state:
    st.session_state.founding_members = load_founding_members()
if 'documentation' not in st.session_state:
    st.session_state.documentation = load_documentation()
if 'votes' not in st.session_state:
    st.session_state.votes = load_votes()
if 'reviews' not in st.session_state:
    st.session_state.reviews = load_reviews()
if 'current_user' not in st.session_state:
    st.session_state.current_user ="jim_gannaway"if 'user_role' not in st.session_state:
    st.session_state.user_role ="founder"# founder, founding_member, public
if 'selected_theme' not in st.session_state:
    st.session_state.selected_theme = get_default_theme()
if 'active_persona' not in st.session_state:
    st.session_state.active_persona = None # For persona-specific theme overrides

# Apply theme CSS
current_theme = st.session_state.selected_theme

# Check if viewing a specific persona - override with persona theme
if st.session_state.active_persona:
    persona_theme = get_persona_theme(st.session_state.active_persona)
    if persona_theme:
    current_theme = persona_theme

# Inject CSS
st.markdown(inject_theme_css(current_theme), unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.header("FIAT MUSICA")
    st.caption("v7.0 — The Platonic Album Operating System")
 
    # Current theme indicator
    current_theme_display = get_theme(st.session_state.selected_theme)
    st.caption(f"Theme: {current_theme_display['name']}")
 
    st.divider()
 
    # Navigation Guide
    st.subheader("Navigation")
 
    for category_name, category_data in NAVIGATION_STRUCTURE.items():
    # Clean category name (remove emoji)
    clean_category = category_name.split(' ', 1)[1] if ' ' in category_name else category_name
 
    with st.expander(clean_category, expanded=False):
    st.caption(category_data['description'])
    for tab_name in category_data['tabs']:
    st.markdown(f"• {tab_name}")
 
    st.divider()
 
    # Key Metrics
    st.subheader("System Overview")
 
    virtual_songs_count = len(st.session_state.virtual_songs)
    st.metric("Virtual Songs", virtual_songs_count)
 
    # Count total manifestations across all virtual songs
    total_manifestations = 0
    for song in st.session_state.virtual_songs.values():
    total_manifestations += len(song.get('manifestations', []))
    st.metric("Manifestations", total_manifestations)
 
    # Triangulation density
    if virtual_songs_count > 0:
    density = total_manifestations / virtual_songs_count
    st.metric("Triangulation Density", f"{density:.1f}×")
 
    st.divider()
 
    # Persona metrics
    active_personas = sum(1 for p in st.session_state.personas.values() if p.get('active', True))
    st.metric("Active Personas", active_personas)
 
    # My Albums
    my_albums_count = len(st.session_state.my_albums)
    st.metric("My Albums", my_albums_count)
 
    # Founding Members
    founding_members_count = len(st.session_state.founding_members)
    st.metric("Founding Members", f"{founding_members_count}/100")
 
    st.divider()
 
    # Documentation
    docs_count = len(st.session_state.documentation)
    st.metric("Documentation", docs_count)
 
    st.divider()
 
    # User info
    st.caption(f"User: {st.session_state.current_user}")
    st.caption(f"Role: {st.session_state.user_role.title()}")
    st.caption(f"Session: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# --- MAIN INTERFACE ---
st.title("FIAT MUSICA")
st.markdown("#### The Platonic Album Operating System — Version 7.0")
st.caption("Experience songs as living ideals through multiple manifestations")

# Main tabs
tabs = st.tabs([
"My Album Builder",
"Virtual Songs",
"Personas",
"Living Archive",
"Founding Members",
"Documentation",
"Voting",
"Reviews",
"Band HQ",
"Artist Outreach",
"Protosongs",
"Analytics",
"Settings"])

# --- TAB 1: MY ALBUM BUILDER ---
with tabs[0]:
    st.subheader("My Album Builder")
    st.caption("Create your unique listening experience by choosing your favorite manifestation of each virtual song")
 
    render_notes_section("my_album_builder","My Album Builder")
 
    st.divider()
 
    # Overall stats
    col1, col2, col3 = st.columns(3)
 
    total_albums = len(st.session_state.my_albums)
    col1.metric("Your Albums", total_albums)
 
    # Most popular configuration
    if st.session_state.my_albums:
    # Count manifestation popularity
    manifestation_counts = {}
    for album in st.session_state.my_albums.values():
    for man_id in album.get('selections', {}).values():
    manifestation_counts[man_id] = manifestation_counts.get(man_id, 0) + 1
 
    if manifestation_counts:
    most_popular_man = max(manifestation_counts, key=manifestation_counts.get)
    col2.metric("Most Chosen Manifestation", f"{manifestation_counts[most_popular_man]}x")
 
    col3.metric("Available Songs", len(st.session_state.virtual_songs))
 
    st.divider()
 
    # View existing My Albums
    if st.session_state.my_albums:
    with st.expander("Your Saved Albums", expanded=False):
    for album_id, album in st.session_state.my_albums.items():
    with st.container(border=True):
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
 
    with col1:
    st.markdown(f"### {album['name']}")
    st.caption(f"Created: {album.get('created', 'Unknown')[:10]}")
    st.caption(f"Tracks: {len(album.get('selections', {}))} | Public: {'Yes' if album.get('public', False) else 'No'}")
 
    with col2:
    st.metric("Plays", album.get('plays', 0))
 
    with col3:
    if st.button("Edit", key=f"edit_{album_id}"):
    # Store album to edit
    st.session_state['editing_album'] = album_id
    st.rerun()
 
    with col4:
    if st.button("Delete", key=f"delete_{album_id}"):
    del st.session_state.my_albums[album_id]
    save_my_albums(st.session_state.my_albums)
    st.success("Deleted!")
    st.rerun()
 
    # Show selections
    if st.checkbox("Show tracks", key=f"show_{album_id}"):
    for song_id, man_id in album.get('selections', {}).items():
    song = st.session_state.virtual_songs.get(song_id, {})
 
    # Find manifestation
    man_title ="Unknown" for man in song.get('manifestations', []):
    if man.get('manifestation_id') == man_id:
    man_title = man.get('title', 'Untitled')
    break
 
    st.caption(f"- {song.get('title', song_id)}: **{man_title}**")
 
    st.divider()
 
    # Check if editing
    editing_album_id = st.session_state.get('editing_album')
 
    if editing_album_id and editing_album_id in st.session_state.my_albums:
    st.markdown("### Editing Album")
    editing_album = st.session_state.my_albums[editing_album_id]
 
    album_name = st.text_input("Album Name", value=editing_album['name'])
    album_public = st.checkbox("Make Public", value=editing_album.get('public', False))
 
    if st.button("Cancel Edit"):
    del st.session_state['editing_album']
    st.rerun()
 
    st.divider()
 
    # Use existing selections
    if 'my_album_selections' not in st.session_state:
    st.session_state.my_album_selections = editing_album.get('selections', {}).copy()
    else:
    st.markdown("### Create New Album")
    album_name = st.text_input("Album Name", placeholder="My Perfect Album")
    album_public = st.checkbox("Make Public", value=False)
 
    # Initialize selections if needed
    if 'my_album_selections' not in st.session_state:
    st.session_state.my_album_selections = {}
 
    st.divider()
 
    if st.session_state.virtual_songs:
    st.markdown("#### Select & Order Tracks")
 
    # Track management
    col1, col2 = st.columns([3, 1])
 
    with col1:
    st.caption(f"{len(st.session_state.my_album_selections)} tracks in album")
 
    with col2:
    if st.button("Reset Selections"):
    st.session_state.my_album_selections = {}
    st.rerun()
 
    st.divider()
 
    # Song ordering interface
    st.markdown("**Track Order:**")
    st.caption("Use numbers to set playback order. Tracks not numbered will appear at the end.")
 
    # Create ordered list
    ordered_songs = []
    unordered_songs = []
 
    for song_id in st.session_state.my_album_selections.keys():
    song = st.session_state.virtual_songs.get(song_id, {})
    order = st.session_state.my_album_selections.get(song_id, {}).get('order')
 
    if isinstance(order, int):
    ordered_songs.append((order, song_id, song))
    else:
    unordered_songs.append((song_id, song))
 
    ordered_songs.sort(key=lambda x: x[0])
 
    # Display ordered tracks
    for order, song_id, song in ordered_songs:
    col1, col2, col3 = st.columns([0.5, 2, 1])
 
    with col1:
    st.markdown(f"**{order}.**")
 
    with col2:
    st.markdown(f"**{song.get('title', song_id)}**")
 
    # Show selected manifestation
    man_id = st.session_state.my_album_selections[song_id].get('manifestation_id')
    if man_id:
    for man in song.get('manifestations', []):
    if man.get('manifestation_id') == man_id:
    persona = st.session_state.personas.get(man.get('performed_by_persona', ''), {})
    st.caption(f"→ {man.get('title')} ({persona.get('name', 'Unknown')})")
    break
 
    with col3:
    if st.button("Remove", key=f"remove_ordered_{song_id}"):
    del st.session_state.my_album_selections[song_id]
    st.rerun()
 
    # Display unordered tracks
    if unordered_songs:
    st.markdown("**Unordered Tracks:**")
    for song_id, song in unordered_songs:
    col1, col2 = st.columns([3, 1])
 
    with col1:
    st.markdown(f"**{song.get('title', song_id)}**")
 
    with col2:
    if st.button("", key=f"remove_unordered_{song_id}"):
    del st.session_state.my_album_selections[song_id]
    st.rerun()
 
    st.divider()
 
    # Add/modify tracks
    st.markdown("#### Add or Modify Tracks")
 
    with st.form("add_track_form"):
    # Select song
    available_songs = list(st.session_state.virtual_songs.keys())
 
    selected_song_id = st.selectbox(
"Song",
    available_songs,
    format_func=lambda x: st.session_state.virtual_songs[x].get('title', x)
    )
 
    if selected_song_id:
    song = st.session_state.virtual_songs[selected_song_id]
    manifestations = song.get('manifestations', [])
 
    if manifestations:
    # Select manifestation
    manifestation_options = []
    for m in manifestations:
    persona = st.session_state.personas.get(m.get('performed_by_persona', ''), {})
    label = f"{m.get('title', 'Untitled')} ({persona.get('name', 'Unknown')})" manifestation_options.append((m.get('manifestation_id'), label))
 
    selected_man = st.selectbox(
"Manifestation",
    [opt[0] for opt in manifestation_options],
    format_func=lambda x: next(opt[1] for opt in manifestation_options if opt[0] == x)
    )
 
    # Set order
    track_order = st.number_input("Track Position (optional)", 
    min_value=1, max_value=50, value=len(st.session_state.my_album_selections) + 1, step=1)
 
    col1, col2 = st.columns(2)
 
    with col1:
    if st.form_submit_button("Add/Update Track", type="primary"):
    st.session_state.my_album_selections[selected_song_id] = {
    'manifestation_id': selected_man,
    'order': track_order
    }
    st.success("Track added/updated!")
    st.rerun()
 
    with col2:
    if st.form_submit_button("Add without order"):
    st.session_state.my_album_selections[selected_song_id] = {
    'manifestation_id': selected_man,
    'order': None
    }
    st.success("Track added!")
    st.rerun()
    else:
    st.info("This song has no manifestations yet")
 
    st.divider()
 
    # Save album
    col1, col2, col3 = st.columns([2, 1, 1])
 
    with col1:
    if st.button("Save Album", type="primary", use_container_width=True):
    if album_name and st.session_state.my_album_selections:
    # Prepare selections for save
    save_selections = {}
    for song_id, data in st.session_state.my_album_selections.items():
    save_selections[song_id] = data['manifestation_id']
 
    if editing_album_id and editing_album_id in st.session_state.my_albums:
    # Update existing
    st.session_state.my_albums[editing_album_id].update({
"name": album_name,
"public": album_public,
"selections": save_selections,
"modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.success(f"Album '{album_name}' updated!")
    del st.session_state['editing_album']
    else:
    # Create new
    album_id = f"album_{len(st.session_state.my_albums) + 1}" 
    new_album = {
"name": album_name,
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"user_id": st.session_state.current_user,
"selections": save_selections,
"public": album_public,
"plays": 0,
"shares": 0
    }
 
    st.session_state.my_albums[album_id] = new_album
    st.success(f"Album '{album_name}' created!")
 
    save_my_albums(st.session_state.my_albums)
    st.session_state.my_album_selections = {}
    st.rerun()
    else:
    st.error("Please provide album name and select tracks")
 
    with col2:
    if st.button("Random Album", use_container_width=True):
    # Auto-select random manifestations
    st.session_state.my_album_selections = {}
 
    for song_id, song in st.session_state.virtual_songs.items():
    manifestations = song.get('manifestations', [])
    if manifestations:
    random_man = random.choice(manifestations)
    st.session_state.my_album_selections[song_id] = {
    'manifestation_id': random_man.get('manifestation_id'),
    'order': None
    }
 
    st.success("Random album generated!")
    st.rerun()
 
    with col3:
    if st.button("Stats", use_container_width=True):
    st.info("Album statistics")
    else:
    st.info("No virtual songs yet. Add songs to start building albums!")

# --- TAB 2: VIRTUAL SONGS (Song Home Pages) ---
with tabs[1]:
    st.subheader("Virtual Songs - The Platonic Ideals")
    st.markdown("Deep dive into each composition's essence, manifestations, and journey")
 
    render_notes_section("virtual_songs","Virtual Songs")
 
    st.divider()
 
    # Add new virtual song
    with st.expander("Add New Virtual Song", expanded=False):
    with st.form("new_virtual_song"):
    new_title = st.text_input("Song Title")
    new_year = st.number_input("Year Written", min_value=1900, max_value=2025, value=1985)
    new_themes = st.text_input("Core Themes (comma-separated)", placeholder="obsession, longing, surveillance")
    new_lyrics = st.text_area("Lyrics", height=200)
 
    col1, col2 = st.columns(2)
    with col1:
    melody_rating = st.slider("Melody Rating", 0, 10, 8)
    harmony_rating = st.slider("Harmony Rating", 0, 10, 8)
    with col2:
    lyrics_rating = st.slider("Lyrics Rating", 0, 10, 8)
    structure_rating = st.slider("Structure Rating", 0, 10, 8)
 
    if st.form_submit_button("Create Virtual Song", type="primary"):
    if new_title:
    song_id = f"vs_{new_title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}" 
    new_song = {
"ideal_id": song_id,
"title": new_title,
"the_ideal": {
"genesis": {
"year_written": new_year,
"themes": [t.strip() for t in new_themes.split(',')] if new_themes else [],
"lyrics": new_lyrics
    },
"compositional_rating": {
"melody": melody_rating,
"harmony": harmony_rating,
"lyrics": lyrics_rating,
"structure": structure_rating,
"aggregate": (melody_rating + harmony_rating + lyrics_rating + structure_rating) / 4
    }
    },
"manifestations": [],
"living_archive_chapters": [],
"strategic_positioning": {},
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    st.session_state.virtual_songs[song_id] = new_song
    save_virtual_songs(st.session_state.virtual_songs)
    st.success(f"Virtual Song '{new_title}' created!")
    st.rerun()
 
    st.divider()
 
    # Display virtual songs
    if st.session_state.virtual_songs:
    song_list = list(st.session_state.virtual_songs.keys())
    selected_song_id = st.selectbox(
"Select Virtual Song",
    song_list,
    format_func=lambda x: st.session_state.virtual_songs[x].get('title', x)
    )
 
    if selected_song_id:
    song = st.session_state.virtual_songs[selected_song_id]
 
    st.markdown(f"# {song.get('title', 'Untitled')}")
 
    # Song tabs
    song_tabs = st.tabs([
"The Ideal",
"Manifestations",
"Living Archive",
"Strategy",
"Reviews" ])
 
    # THE IDEAL tab
    with song_tabs[0]:
    ideal = song.get('the_ideal', {})
    genesis = ideal.get('genesis', {})
    rating = ideal.get('compositional_rating', {})
 
    col1, col2 = st.columns([2, 1])
 
    with col1:
    st.markdown("### Genesis")
    st.markdown(f"**Year Written:** {genesis.get('year_written', 'Unknown')}")
 
    themes = genesis.get('themes', [])
    if themes:
    st.markdown(f"**Themes:** {', '.join(themes)}")
 
    lyrics = genesis.get('lyrics', '')
    if lyrics:
    with st.expander("Lyrics", expanded=False):
    st.text_area("", lyrics, height=300, disabled=True, label_visibility="collapsed")
 
    with col2:
    st.markdown("### Compositional Rating")
 
    if rating:
    st.metric("Aggregate", f"{rating.get('aggregate', 0):.1f}/10")
 
    st.markdown("**Components:**")
    st.markdown(f"- Melody: {rating.get('melody', 0)}/10")
    st.markdown(f"- Harmony: {rating.get('harmony', 0)}/10")
    st.markdown(f"- Lyrics: {rating.get('lyrics', 0)}/10")
    st.markdown(f"- Structure: {rating.get('structure', 0)}/10")
 
    # MANIFESTATIONS tab
    with song_tabs[1]:
    st.markdown("### All Manifestations")
 
    # Add new manifestation
    with st.expander("Add New Manifestation"):
    with st.form(f"new_manifestation_{selected_song_id}"):
    man_title = st.text_input("Manifestation Title", placeholder="Acoustic Version")
 
    persona_options = list(st.session_state.personas.keys())
    man_persona = st.selectbox(
"Performed By Persona",
    persona_options,
    format_func=lambda x: st.session_state.personas[x]['name']
    )
 
    man_file = st.text_input("Audio File", placeholder="song_acoustic.mp3")
 
    col1, col2 = st.columns(2)
    with col1:
    man_tempo = st.number_input("Tempo (BPM)", min_value=40, max_value=200, value=120)
    man_key = st.text_input("Key", value="Am")
    with col2:
    man_energy = st.slider("Energy Level", 1, 10, 7)
 
    if st.form_submit_button("Add Manifestation"):
    manifestation_id = f"man_{len(song.get('manifestations', []))}_{datetime.now().strftime('%Y%m%d%H%M%S')}" 
    new_manifestation = {
"manifestation_id": manifestation_id,
"title": man_title,
"performed_by_persona": man_persona,
"file_assets": {
"audio_file": man_file
    },
"production_characteristics": {
"tempo": man_tempo,
"key": man_key,
"energy_level": man_energy
    },
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    if 'manifestations' not in song:
    song['manifestations'] = []
 
    song['manifestations'].append(new_manifestation)
 
    # Update persona's tracks_performed
    if man_persona in st.session_state.personas:
    if manifestation_id not in st.session_state.personas[man_persona]['tracks_performed']:
    st.session_state.personas[man_persona]['tracks_performed'].append(manifestation_id)
    save_personas(st.session_state.personas)
 
    save_virtual_songs(st.session_state.virtual_songs)
    st.success(f"Manifestation added!")
    st.rerun()
 
    # Display manifestations
    manifestations = song.get('manifestations', [])
 
    if manifestations:
    for man in manifestations:
    persona_id = man.get('performed_by_persona', 'unknown')
    persona = st.session_state.personas.get(persona_id, {})
 
    with st.container(border=True):
    col1, col2, col3 = st.columns([3, 1, 1])
 
    with col1:
    st.markdown(f"### {man.get('title', 'Untitled')}")
    st.caption(f"**Performed by:** {persona.get('name', persona_id)}")
    st.caption(f"**Created:** {man.get('created', 'Unknown')}")
 
    with col2:
    prod = man.get('production_characteristics', {})
    st.metric("Tempo", f"{prod.get('tempo', 0)} BPM")
    st.metric("Energy", f"{prod.get('energy_level', 0)}/10")
 
    with col3:
    st.metric("Key", prod.get('key', 'Unknown'))
 
    # File info
    file_assets = man.get('file_assets', {})
    audio_file = file_assets.get('audio_file', '')
    if audio_file:
    st.caption(f"{audio_file}")
    else:
    st.info("No manifestations yet. Add your first manifestation above!")
 
    # LIVING ARCHIVE tab
    with song_tabs[2]:
    st.markdown("### Living Archive - Song Journey Timeline")
    st.caption("Document significant moments in this song's evolution")
 
    # Add new chapter
    with st.expander("Add New Chapter"):
    with st.form(f"new_chapter_{selected_song_id}"):
    chapter_date = st.date_input("Date")
    chapter_type = st.selectbox("Type", [
"Genesis","Release","Studio Session","Performance", 
"Media Feature","Milestone","Planned" ])
    chapter_title = st.text_input("Title", placeholder="The Cassette Demo")
    chapter_description = st.text_area("Description", height=100)
    chapter_significance = st.text_area("Significance", height=100,
    placeholder="Why is this moment important?")
 
    if st.form_submit_button("Add Chapter"):
    chapter_id = f"ch_{len(song.get('living_archive_chapters', []))}_{datetime.now().strftime('%Y%m%d')}" 
    new_chapter = {
"chapter_id": chapter_id,
"date": chapter_date.strftime("%Y-%m-%d"),
"type": chapter_type,
"title": chapter_title,
"description": chapter_description,
"significance": chapter_significance,
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    if 'living_archive_chapters' not in song:
    song['living_archive_chapters'] = []
 
    song['living_archive_chapters'].append(new_chapter)
    save_virtual_songs(st.session_state.virtual_songs)
    st.success("Chapter added!")
    st.rerun()
 
    # Display timeline
    chapters = song.get('living_archive_chapters', [])
 
    if chapters:
    # Sort by date
    sorted_chapters = sorted(chapters, key=lambda x: x.get('date', ''))
 
    st.markdown("#### Timeline")
 
    for idx, chapter in enumerate(sorted_chapters):
    with st.container(border=True):
    col1, col2 = st.columns([1, 4])
 
    with col1:
    st.markdown(f"**{chapter.get('date', 'Unknown')}**")
    st.caption(chapter.get('type', 'Unknown'))
 
    with col2:
    st.markdown(f"### {chapter.get('title', 'Untitled Chapter')}")
    st.markdown(chapter.get('description', ''))
 
    if chapter.get('significance'):
    st.info(f"**Significance:** {chapter['significance']}")
 
    # Timeline connector
    if idx < len(sorted_chapters) - 1:
    st.markdown("")
    else:
    st.info("No chapters yet. Document the first significant moment in this song's journey!")
 
    # STRATEGY tab
    with song_tabs[3]:
    st.markdown("### Strategic Positioning")
 
    positioning = song.get('strategic_positioning', {})
 
    col1, col2 = st.columns(2)
 
    with col1:
    st.markdown("#### Primary Uses")
 
    uses = positioning.get('primary_uses', {})
 
    band_use = st.checkbox("Band Setlist", value=uses.get('band_setlist', False),
    key=f"band_use_{selected_song_id}")
    artist_pitch = st.checkbox("Artist Pitch", value=uses.get('artist_pitch', False),
    key=f"artist_pitch_{selected_song_id}")
    sync_licensing = st.checkbox("Sync Licensing", value=uses.get('sync_licensing', False),
    key=f"sync_{selected_song_id}")
    founding_member = st.checkbox("Founding Member Engagement", 
    value=uses.get('founding_member', False),
    key=f"fm_{selected_song_id}")
 
    if st.button("Save Strategic Uses"):
    if 'strategic_positioning' not in song:
    song['strategic_positioning'] = {}
 
    song['strategic_positioning']['primary_uses'] = {
    'band_setlist': band_use,
    'artist_pitch': artist_pitch,
    'sync_licensing': sync_licensing,
    'founding_member': founding_member
    }
 
    save_virtual_songs(st.session_state.virtual_songs)
    st.success("Strategic uses saved!")
 
    with col2:
    st.markdown("#### Notes")
 
    strategy_notes = st.text_area("Strategic Notes",
    value=positioning.get('notes', ''),
    height=200,
    key=f"strat_notes_{selected_song_id}",
    placeholder="Why this song serves these purposes..." )
 
    if st.button("Save Notes"):
    if 'strategic_positioning' not in song:
    song['strategic_positioning'] = {}
 
    song['strategic_positioning']['notes'] = strategy_notes
    save_virtual_songs(st.session_state.virtual_songs)
    st.success("Notes saved!")
 
    # REVIEWS tab
    with song_tabs[4]:
    st.markdown("### Reviews & Feedback")
 
    # Add review
    with st.expander("Add Review"):
    with st.form(f"new_review_{selected_song_id}"):
    review_version = st.selectbox("For Manifestation",
    ["The Ideal (Composition Itself)"] + [m.get('title', m.get('manifestation_id')) 
    for m in song.get('manifestations', [])]
    )
    review_type = st.selectbox("Review Type", [
"Gemini Analysis","Founding Member Feedback", 
"Critical Review","Artist Notes" ])
    review_rating = st.slider("Rating", 1, 10, 8)
    review_text = st.text_area("Review", height=150)
 
    if st.form_submit_button("Add Review"):
    review_id = f"rev_{selected_song_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}" 
    new_review = {
"review_id": review_id,
"song_id": selected_song_id,
"version": review_version,
"type": review_type,
"rating": review_rating,
"text": review_text,
"reviewer": st.session_state.current_user,
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    if selected_song_id not in st.session_state.reviews:
    st.session_state.reviews[selected_song_id] = []
 
    st.session_state.reviews[selected_song_id].append(new_review)
    save_reviews(st.session_state.reviews)
    st.success("Review added!")
    st.rerun()
 
    # Display reviews
    song_reviews = st.session_state.reviews.get(selected_song_id, [])
 
    if song_reviews:
    for review in song_reviews:
    with st.container(border=True):
    col1, col2 = st.columns([3, 1])
 
    with col1:
    st.markdown(f"**{review.get('version', 'Unknown')}** - {review.get('type', 'Unknown')}")
    st.caption(f"By {review.get('reviewer', 'Unknown')} on {review.get('created', 'Unknown')[:10]}")
 
    with col2:
    st.metric("Rating", f"{review.get('rating', 0)}/10")
 
    st.markdown(review.get('text', ''))
    else:
    st.info("No reviews yet.")
    else:
    st.info("No virtual songs yet. Create your first virtual song above!")

# --- TAB 3: PERSONAS ---
with tabs[2]:
    st.subheader("Persona Manager")
    st.markdown("Create and manage the recurring artistic identities that perform your virtual songs")
 
    render_notes_section("personas","Persona Manager")
 
    st.divider()
 
    # Persona overview
    col1, col2, col3, col4 = st.columns(4)
 
    active_personas = [p for p in st.session_state.personas.values() if p.get('active', True)]
 
    col1.metric("Total Personas", len(st.session_state.personas))
    col2.metric("Active", len(active_personas))
 
    # Count tracks performed
    total_tracks = sum(len(p.get('tracks_performed', [])) for p in st.session_state.personas.values())
    col3.metric("Total Tracks Performed", total_tracks)
 
    col4.metric("Average Tracks/Persona", f"{total_tracks/len(st.session_state.personas):.1f}" if st.session_state.personas else"0")
 
    st.divider()
 
    # Add new persona
    with st.expander("Create New Persona"):
    with st.form("new_persona"):
    new_persona_name = st.text_input("Persona Name", placeholder="The Midnight Ensemble")
 
    col1, col2 = st.columns(2)
 
    with col1:
    persona_type = st.selectbox("Type", [
"jazz_ensemble","female_vocalist","male_vocalist",
"live_band","synth_pop","acoustic_duo","orchestral",
"electronic_producer","other" ])
 
    genre = st.text_input("Genre", placeholder="Jazz")
    arrangement_style = st.text_input("Arrangement Style", placeholder="Sophisticated swing")
 
    with col2:
    visual_style = st.text_input("Visual Style", placeholder="Noir sophistication")
    color_palette = st.text_input("Color Palette (comma-separated)", 
    placeholder="Deep Blue, Gold, Cream")
 
    narrative = st.text_area("Narrative", height=100,
    placeholder="Late-night sophistication, urbane reflection")
    target_demo = st.text_input("Target Demographic",
    placeholder="40-65, jazz aficionados, NPR listeners")
 
    if st.form_submit_button("Create Persona", type="primary"):
    if new_persona_name:
    persona_id = f"persona_{new_persona_name.lower().replace(' ', '_')}" 
    new_persona = {
"persona_id": persona_id,
"name": new_persona_name,
"type": persona_type,
"brand_identity": {
"visual_style": visual_style,
"color_palette": [c.strip() for c in color_palette.split(',')] if color_palette else [],
"typography":"" },
"musical_identity": {
"genre": genre,
"arrangement_style": arrangement_style,
"instrumentation": []
    },
"narrative": narrative,
"target_demographic": target_demo,
"tracks_performed": [],
"created": datetime.now().strftime("%Y-%m-%d"),
"active": True
    }
 
    st.session_state.personas[persona_id] = new_persona
    save_personas(st.session_state.personas)
    st.success(f"Persona '{new_persona_name}' created!")
    st.rerun()
 
    st.divider()
 
    # Display personas
    for persona_id, persona in st.session_state.personas.items():
    with st.expander(f"{persona['name']}", expanded=False):
    col1, col2 = st.columns([2, 1])
 
    with col1:
    st.markdown(f"**Type:** {persona.get('type', 'Unknown').replace('_', ' ').title()}")
    st.markdown(f"**Genre:** {persona.get('musical_identity', {}).get('genre', 'Unknown')}")
 
    narrative = persona.get('narrative', '')
    if narrative:
    st.markdown(f"**Narrative:** {narrative}")
 
    target_demo = persona.get('target_demographic', '')
    if target_demo:
    st.markdown(f"**Target Demo:** {target_demo}")
 
    with col2:
    st.markdown("**Brand Identity:**")
 
    visual = persona.get('brand_identity', {}).get('visual_style', '')
    if visual:
    st.caption(f"Visual: {visual}")
 
    colors = persona.get('brand_identity', {}).get('color_palette', [])
    if colors:
    st.caption(f"Colors: {', '.join(colors)}")
 
    # Tracks performed
    tracks_performed = persona.get('tracks_performed', [])
 
    st.markdown(f"**Tracks Performed:** {len(tracks_performed)}")
 
    if tracks_performed:
    st.caption(f"Track IDs: {', '.join(tracks_performed[:5])}{'...' if len(tracks_performed) > 5 else ''}")
 
    # Active toggle
    col_a, col_b = st.columns([1, 3])
 
    with col_a:
    active = st.checkbox("Active", value=persona.get('active', True), key=f"active_{persona_id}")
 
    with col_b:
    if st.button("Update Status", key=f"update_{persona_id}"):
    persona['active'] = active
    save_personas(st.session_state.personas)
    st.success("Status updated!")

# --- TAB 4: LIVING ARCHIVE ---
with tabs[3]:
    st.subheader("Living Archive Manager")
    st.markdown("Create the temporal narrative of each song's journey from genesis to present to future")
 
    render_notes_section("living_archive","Living Archive Manager")
 
    st.divider()
 
    if st.session_state.virtual_songs:
    st.markdown("### Select Song to Manage Archive")
 
    archive_song_id = st.selectbox(
"Virtual Song",
    list(st.session_state.virtual_songs.keys()),
    format_func=lambda x: st.session_state.virtual_songs[x].get('title', x),
    key="archive_song_select" )
 
    if archive_song_id:
    archive_song = st.session_state.virtual_songs[archive_song_id]
 
    st.markdown(f"## {archive_song.get('title', 'Untitled')} - Timeline")
 
    chapters = archive_song.get('living_archive_chapters', [])
 
    # Timeline visualization
    if chapters:
    sorted_chapters = sorted(chapters, key=lambda x: x.get('date', ''))
 
    st.markdown("### Timeline View")
 
    # Simple timeline
    for idx, chapter in enumerate(sorted_chapters):
    col1, col2 = st.columns([1, 5])
 
    with col1:
    st.markdown(f"**{chapter.get('date', 'Unknown')}**")
 
    # Type badge
    type_colors = {
"Genesis":"🟢",
"Release":"",
"Studio Session":"🟡",
"Performance":"",
"Planned":"" }
    type_icon = type_colors.get(chapter.get('type', ''),"")
    st.markdown(f"{type_icon} {chapter.get('type', 'Unknown')}")
 
    with col2:
    with st.container(border=True):
    st.markdown(f"### {chapter.get('title', 'Untitled')}")
    st.markdown(chapter.get('description', ''))
 
    if chapter.get('significance'):
    st.info(f"**Significance:** {chapter['significance']}")
 
    if idx < len(sorted_chapters) - 1:
    st.markdown("")
    else:
    st.info("No chapters in this song's archive yet. Add the first milestone below!")
 
    st.divider()
 
    # Quick add chapter
    st.markdown("### Add Chapter")
 
    with st.form(f"quick_chapter_{archive_song_id}"):
    qc_date = st.date_input("Date", value=datetime.now())
 
    col1, col2 = st.columns(2)
 
    with col1:
    qc_type = st.selectbox("Type", [
"Genesis","Release","Studio Session","Performance",
"Media Feature","Milestone","Planned" ])
 
    with col2:
    qc_title = st.text_input("Title", placeholder="The Meridian Sessions")
 
    qc_description = st.text_area("Description", height=100,
    placeholder="What happened...")
 
    qc_significance = st.text_area("Significance", height=100,
    placeholder="Why this matters...")
 
    if st.form_submit_button("Add Chapter", type="primary"):
    chapter_id = f"ch_{len(chapters)}_{datetime.now().strftime('%Y%m%d%H%M%S')}" 
    new_chapter = {
"chapter_id": chapter_id,
"date": qc_date.strftime("%Y-%m-%d"),
"type": qc_type,
"title": qc_title,
"description": qc_description,
"significance": qc_significance,
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    if 'living_archive_chapters' not in archive_song:
    archive_song['living_archive_chapters'] = []
 
    archive_song['living_archive_chapters'].append(new_chapter)
    save_virtual_songs(st.session_state.virtual_songs)
    st.success("Chapter added!")
    st.rerun()
    else:
    st.info("No virtual songs yet. Create songs first to build their living archives!")

# --- TAB 5: FOUNDING MEMBERS ---
with tabs[4]:
    st.subheader("Founding Member Portal")
    st.markdown("Manage the 100 Founding Members @ $1,000 each = $100K investment")
 
    render_notes_section("founding_members","Founding Members")
 
    st.divider()
 
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
 
    total_members = len(st.session_state.founding_members)
    col1.metric("Members", f"{total_members}/100")
 
    paid_members = sum(1 for m in st.session_state.founding_members.values() if m.get('paid', False))
    col2.metric("Paid", paid_members)
 
    total_raised = paid_members * 1000
    col3.metric("Raised", f"${total_raised:,}")
 
    remaining = 100000 - total_raised
    col4.metric("Remaining", f"${remaining:,}")
 
    # Progress bar
    st.progress(paid_members / 100)
 
    st.divider()
 
    # Add member
    with st.expander("Add Founding Member"):
    with st.form("new_member"):
    member_name = st.text_input("Name")
    member_email = st.text_input("Email")
 
    col1, col2 = st.columns(2)
 
    with col1:
    member_joined = st.date_input("Join Date", value=datetime.now())
    member_paid = st.checkbox("Payment Received")
 
    with col2:
    member_tier = st.selectbox("Tier", [
"Founding Member ($1,000)",
"Echo Circle ($1,000)",
"Lux Participant ($10,000)" ])
 
    member_notes = st.text_area("Notes", placeholder="Champion of specific songs, special interests...")
 
    if st.form_submit_button("Add Member"):
    if member_name:
    member_id = f"fm_{len(st.session_state.founding_members) + 1:03d}" 
    new_member = {
"member_id": member_id,
"name": member_name,
"email": member_email,
"joined": member_joined.strftime("%Y-%m-%d"),
"paid": member_paid,
"tier": member_tier,
"notes": member_notes,
"vote_weight": 10, # Founding members get 10x vote weight
"songs_championed": [],
"votes_cast": 0
    }
 
    st.session_state.founding_members[member_id] = new_member
    save_founding_members(st.session_state.founding_members)
    st.success(f"Member {member_name} added!")
    st.rerun()
 
    st.divider()
 
    # Member list
    if st.session_state.founding_members:
    st.markdown("### Member Roster")
 
    for member_id, member in st.session_state.founding_members.items():
    with st.expander(f"{'' if member.get('paid') else '⏳'} {member['name']} ({member_id})"):
    col1, col2 = st.columns(2)
 
    with col1:
    st.markdown(f"**Email:** {member.get('email', 'N/A')}")
    st.markdown(f"**Joined:** {member.get('joined', 'Unknown')}")
    st.markdown(f"**Tier:** {member.get('tier', 'Unknown')}")
    st.markdown(f"**Vote Weight:** {member.get('vote_weight', 10)}x")
 
    with col2:
    st.markdown(f"**Payment:** {' Received' if member.get('paid') else '⏳ Pending'}")
    st.markdown(f"**Votes Cast:** {member.get('votes_cast', 0)}")
 
    championed = member.get('songs_championed', [])
    st.markdown(f"**Songs Championed:** {len(championed)}")
 
    if member.get('notes'):
    st.info(member['notes'])
    else:
    st.info("No founding members yet. Add your first member above!")

# --- TAB 6: DOCUMENTATION LIBRARY ---
with tabs[5]:
    st.subheader("Documentation Library")
    st.markdown("Organize whitepapers, methodologies, case studies, and intellectual property documentation")
 
    render_notes_section("documentation","Documentation Library")
 
    st.divider()
 
    # Add new document
    with st.expander("Add Document"):
    with st.form("new_doc"):
    doc_title = st.text_input("Document Title")
    doc_category = st.selectbox("Category", list(DOCUMENTATION_CATEGORIES.keys()),
    format_func=lambda x: DOCUMENTATION_CATEGORIES[x])
 
    col1, col2 = st.columns(2)
 
    with col1:
    doc_version = st.text_input("Version", value="1.0")
    doc_status = st.selectbox("Status", ["Draft","Final","Published"])
 
    with col2:
    doc_file = st.text_input("Filename", placeholder="triangulation_framework_v2.pdf")
 
    doc_description = st.text_area("Description", height=100)
 
    if st.form_submit_button("Add Document"):
    if doc_title:
    doc_id = f"doc_{len(st.session_state.documentation) + 1:03d}" 
    new_doc = {
"doc_id": doc_id,
"title": doc_title,
"category": doc_category,
"version": doc_version,
"status": doc_status,
"filename": doc_file,
"description": doc_description,
"created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
"last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    st.session_state.documentation[doc_id] = new_doc
    save_documentation(st.session_state.documentation)
    st.success(f"Document '{doc_title}' added!")
    st.rerun()
 
    st.divider()
 
    # Display by category
    if st.session_state.documentation:
    st.markdown("### Document Library")
 
    for category_key, category_name in DOCUMENTATION_CATEGORIES.items():
    # Get docs in this category
    category_docs = {k: v for k, v in st.session_state.documentation.items() 
    if v.get('category') == category_key}
 
    if category_docs:
    with st.expander(f"{category_name} ({len(category_docs)} documents)", expanded=True):
    for doc_id, doc in category_docs.items():
    with st.container(border=True):
    col1, col2, col3 = st.columns([3, 1, 1])
 
    with col1:
    st.markdown(f"### {doc['title']}")
    st.caption(f"**Filename:** {doc.get('filename', 'N/A')}")
    if doc.get('description'):
    st.markdown(doc['description'])
 
    with col2:
    st.metric("Version", doc.get('version', '1.0'))
 
    status_colors = {
"Draft":"🟡",
"Final":"🟢",
"Published":"" }
    status_icon = status_colors.get(doc.get('status', 'Draft'),"")
    st.markdown(f"{status_icon} {doc.get('status', 'Draft')}")
 
    with col3:
    st.caption(f"Updated: {doc.get('last_updated', 'Unknown')[:10]}")
 
    if st.button("Download", key=f"download_{doc_id}"):
    st.info(f"Download: {doc.get('filename', 'N/A')}")
    else:
    st.info("No documentation yet. Add your first document above!")
 
    st.markdown("### Suggested Documents to Create:")
 
    suggestions = [
    ("philosophy","Triangulation: The Complete Framework"),
    ("philosophy","The Platonic Album Model"),
    ("methodology","Contrived Music Control Parameters (Patent)"),
    ("business","Revenue Multiplication Analysis"),
    ("case_studies","Of Broken Light: Proof of Concept"),
    ("technical","Fiat Musica App User Guide"),
    ("legal","Patent Strategy Overview"),
    ("partnerships","Paul Sinclair / Suno Opportunity Analysis")
    ]
 
    for cat, title in suggestions:
    st.markdown(f"- {DOCUMENTATION_CATEGORIES[cat]}: **{title}**")

# --- VOTING FUNCTIONS ---
def cast_vote(item_type, item_id, vote_type, user_id, weight=1):
    """Cast a vote for an item (manifestation or persona)"""
    if 'votes' not in st.session_state.votes:
    st.session_state.votes = {}
 
    vote_key = f"{item_type}_{item_id}" 
    if vote_key not in st.session_state.votes:
    st.session_state.votes[vote_key] = {
    'item_type': item_type,
    'item_id': item_id,
    'upvotes': [],
    'downvotes': []
    }
 
    # Remove any existing vote from this user
    st.session_state.votes[vote_key]['upvotes'] = [
    v for v in st.session_state.votes[vote_key].get('upvotes', [])
    if v['user_id'] != user_id
    ]
    st.session_state.votes[vote_key]['downvotes'] = [
    v for v in st.session_state.votes[vote_key].get('downvotes', [])
    if v['user_id'] != user_id
    ]
 
    # Add new vote
    vote_record = {
    'user_id': user_id,
    'weight': weight,
    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    if vote_type == 'upvote':
    st.session_state.votes[vote_key]['upvotes'].append(vote_record)
    else:
    st.session_state.votes[vote_key]['downvotes'].append(vote_record)
 
    save_votes(st.session_state.votes)

def get_vote_stats(item_type, item_id):
    """Get voting statistics for an item"""
    vote_key = f"{item_type}_{item_id}" 
    if vote_key not in st.session_state.votes:
    return {
    'total_votes': 0,
    'upvotes': 0,
    'downvotes': 0,
    'weighted_upvotes': 0,
    'weighted_downvotes': 0,
    'approval_rate': 0,
    'pantheon_status': False
    }
 
    vote_data = st.session_state.votes[vote_key]
 
    upvotes = vote_data.get('upvotes', [])
    downvotes = vote_data.get('downvotes', [])
 
    weighted_upvotes = sum(v['weight'] for v in upvotes)
    weighted_downvotes = sum(v['weight'] for v in downvotes)
 
    total_weighted = weighted_upvotes + weighted_downvotes
 
    approval_rate = (weighted_upvotes / total_weighted * 100) if total_weighted > 0 else 0
    pantheon_status = approval_rate >= 94 and len(upvotes) + len(downvotes) >= 3
 
    return {
    'total_votes': len(upvotes) + len(downvotes),
    'upvotes': len(upvotes),
    'downvotes': len(downvotes),
    'weighted_upvotes': int(weighted_upvotes),
    'weighted_downvotes': int(weighted_downvotes),
    'approval_rate': approval_rate,
    'pantheon_status': pantheon_status
    }

def get_pantheon_badge(approval_rate):
    """Get pantheon status badge"""
    if approval_rate >= 94:
    return"PANTHEON","green" elif approval_rate >= 70:
    return"APPROVED","blue" else:
    return"EXPERIMENTAL","orange"
# --- TAB 7: VOTING ---
with tabs[6]:
    st.subheader("Voting & Pantheon")
    st.markdown("Community consensus on manifestations + governance votes")
 
    render_notes_section("voting","Voting System")
 
    st.divider()
 
    # Overall voting stats
    col1, col2, col3, col4 = st.columns(4)
 
    total_votes = sum(
    len(v.get('upvotes', [])) + len(v.get('downvotes', []))
    for v in st.session_state.votes.values()
    )
    col1.metric("Total Votes Cast", total_votes)
 
    # Count pantheon items
    pantheon_count = sum(
    1 for v in st.session_state.votes.values()
    if get_vote_stats(v.get('item_type', ''), v.get('item_id', ''))['pantheon_status']
    )
    col2.metric("Pantheon Items", pantheon_count)
 
    # User vote weight
    user_weight = 10 if st.session_state.user_role =="founder"or st.session_state.user_role =="founding_member"else 1
    col3.metric("Your Vote Weight", f"{user_weight}x")
 
    # Items voted on
    items_with_votes = len([v for v in st.session_state.votes.values() 
    if len(v.get('upvotes', [])) + len(v.get('downvotes', [])) > 0])
    col4.metric("Items with Votes", items_with_votes)
 
    st.divider()
 
    # Vote type selector
    vote_type = st.radio("Vote Type", ["Manifestation Quality","Persona Session Priority"], horizontal=True)
 
    if vote_type =="Manifestation Quality":
    st.markdown("### Rate Manifestations")
    st.caption("Vote on the quality of individual manifestations. Pantheon status = 94%+ approval with 3+ votes")
 
    # Filter options
    col1, col2, col3 = st.columns(3)
 
    with col1:
    filter_status = st.selectbox("Filter by Status", [
"All","Pantheon Only","Approved+","Needs Votes" ])
 
    with col2:
    sort_by = st.selectbox("Sort by", [
"Song Title","Most Votes","Highest Approval","Lowest Approval" ])
 
    with col3:
    show_voted = st.checkbox("Show only items I've voted on", value=False)
 
    st.divider()
 
    # Voting interface
    if st.session_state.virtual_songs:
    # Collect all manifestations with their data
    all_manifestations = []
 
    for song_id, song in st.session_state.virtual_songs.items():
    manifestations = song.get('manifestations', [])
 
    for man in manifestations:
    man_id = man.get('manifestation_id')
    stats = get_vote_stats('manifestation', man_id)
 
    # Apply filters
    if filter_status =="Pantheon Only"and not stats['pantheon_status']:
    continue
    elif filter_status =="Approved+"and stats['approval_rate'] < 70:
    continue
    elif filter_status =="Needs Votes"and stats['total_votes'] > 0:
    continue
 
    # Check if user voted
    vote_key = f"manifestation_{man_id}" user_voted = False
    if vote_key in st.session_state.votes:
    vote_data = st.session_state.votes[vote_key]
    user_voted = any(
    v['user_id'] == st.session_state.current_user 
    for v in vote_data.get('upvotes', []) + vote_data.get('downvotes', [])
    )
 
    if show_voted and not user_voted:
    continue
 
    all_manifestations.append({
    'song_id': song_id,
    'song_title': song.get('title', 'Untitled'),
    'manifestation': man,
    'stats': stats,
    'user_voted': user_voted
    })
 
    # Sort manifestations
    if sort_by =="Song Title":
    all_manifestations.sort(key=lambda x: x['song_title'])
    elif sort_by =="Most Votes":
    all_manifestations.sort(key=lambda x: x['stats']['total_votes'], reverse=True)
    elif sort_by =="Highest Approval":
    all_manifestations.sort(key=lambda x: x['stats']['approval_rate'], reverse=True)
    elif sort_by =="Lowest Approval":
    all_manifestations.sort(key=lambda x: x['stats']['approval_rate'])
 
    # Display manifestations
    if all_manifestations:
    for item in all_manifestations:
    man = item['manifestation']
    stats = item['stats']
    man_id = man.get('manifestation_id')
 
    persona = st.session_state.personas.get(man.get('performed_by_persona', ''), {})
    status_badge, status_color = get_pantheon_badge(stats['approval_rate'])
 
    with st.container(border=True):
    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 0.5, 0.5])
 
    with col1:
    st.markdown(f"**{item['song_title']}** - {man.get('title', 'Untitled')}")
    st.caption(f"Performed by: {persona.get('name', 'Unknown')}")
    if item['user_voted']:
    st.caption("You voted on this")
 
    with col2:
    st.markdown(f":{status_color}[{status_badge}]")
    if stats['total_votes'] > 0:
    st.caption(f"{stats['weighted_upvotes'] + stats['weighted_downvotes']} weighted votes")
 
    with col3:
    if stats['total_votes'] > 0:
    st.metric("Approval", f"{stats['approval_rate']:.0f}%")
    else:
    st.caption("No votes yet")
 
    with col4:
    if st.button("", key=f"up_man_{man_id}"):
    cast_vote('manifestation', man_id, 'upvote', 
    st.session_state.current_user, user_weight)
    st.rerun()
 
    with col5:
    if st.button("", key=f"down_man_{man_id}"):
    cast_vote('manifestation', man_id, 'downvote', 
    st.session_state.current_user, user_weight)
    st.rerun()
 
    # Vote breakdown
    if stats['total_votes'] > 0:
    st.progress(stats['approval_rate'] / 100)
    st.caption(f"↑ {stats['weighted_upvotes']} weighted upvotes | ↓ {stats['weighted_downvotes']} weighted downvotes | {stats['total_votes']} total votes")
    else:
    st.info("No manifestations match your filter criteria")
    else:
    st.info("No manifestations to vote on yet!")
 
    else: # Persona Session Priority
    st.markdown("### Vote: Which Persona Should Record Next?")
    st.caption("Founding members decide which persona gets the next studio session")
 
    if st.session_state.personas:
    # Display current vote standings
    st.markdown("#### Current Standings")
 
    persona_votes = []
    for persona_id, persona in st.session_state.personas.items():
    if persona.get('active', True):
    stats = get_vote_stats('persona_priority', persona_id)
    persona_votes.append({
    'persona_id': persona_id,
    'name': persona.get('name'),
    'votes': stats['weighted_upvotes'],
    'voter_count': stats['upvotes']
    })
 
    persona_votes.sort(key=lambda x: x['votes'], reverse=True)
 
    for idx, pv in enumerate(persona_votes):
    col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
 
    with col1:
    st.markdown(f"**#{idx + 1}**")
 
    with col2:
    st.markdown(f"**{pv['name']}**")
 
    with col3:
    st.metric("Votes", pv['voter_count'])
 
    with col4:
    st.metric("Weighted", pv['votes'])
 
    st.divider()
 
    # Cast vote
    st.markdown("#### Cast Your Vote")
 
    persona_options = [p for p in st.session_state.personas.keys() 
    if st.session_state.personas[p].get('active', True)]
 
    if persona_options:
    voted_persona = st.selectbox(
"Choose persona for next session",
    persona_options,
    format_func=lambda x: st.session_state.personas[x]['name']
    )
 
    col1, col2 = st.columns([1, 3])
 
    with col1:
    if st.button("Cast Vote", type="primary", use_container_width=True):
    cast_vote('persona_priority', voted_persona, 'upvote',
    st.session_state.current_user, user_weight)
    st.success(f"Voted for {st.session_state.personas[voted_persona]['name']}!")
    st.info(f"Vote weight: {user_weight}x")
    st.rerun()
 
    with col2:
    st.caption(f"Your vote weight: {user_weight}x ({'Founder/Founding Member' if user_weight > 1 else 'Public'})")
    else:
    st.info("No active personas to vote on")
    else:
    st.info("No personas yet!")

# --- TAB 8: REVIEWS ---
with tabs[7]:
    st.subheader("Reviews Manager")
    st.markdown("Track all feedback across virtual songs and manifestations")
 
    render_notes_section("reviews","Reviews Manager")
 
    st.divider()
 
    # Summary stats
    total_reviews = sum(len(reviews) for reviews in st.session_state.reviews.values())
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Reviews", total_reviews)
    col2.metric("Songs with Reviews", len(st.session_state.reviews))
 
    if total_reviews > 0:
    all_ratings = [r['rating'] for reviews in st.session_state.reviews.values() for r in reviews]
    avg_rating = sum(all_ratings) / len(all_ratings)
    col3.metric("Average Rating", f"{avg_rating:.1f}/10")
 
    st.divider()
 
    # Display reviews by song
    if st.session_state.reviews:
    for song_id, song_reviews in st.session_state.reviews.items():
    song = st.session_state.virtual_songs.get(song_id, {})
    song_title = song.get('title', song_id)
 
    with st.expander(f"{song_title} ({len(song_reviews)} reviews)"):
    for review in song_reviews:
    with st.container(border=True):
    col1, col2 = st.columns([3, 1])
 
    with col1:
    st.markdown(f"**{review.get('version', 'Unknown')}**")
    st.caption(f"{review.get('type', 'Unknown')} by {review.get('reviewer', 'Unknown')}")
    st.caption(f"Date: {review.get('created', 'Unknown')[:10]}")
 
    with col2:
    st.metric("Rating", f"{review.get('rating', 0)}/10")
 
    st.markdown(review.get('text', ''))
    else:
    st.info("No reviews yet!")

# --- TAB 9: BAND HQ ---
with tabs[8]:
    st.subheader("Of Broken Light - Band Headquarters")
    st.markdown("Manage the live band formation and operations")
 
    render_notes_section("band_hq","Band Headquarters")
 
    st.divider()
 
    # Band status overview
    col1, col2, col3, col4 = st.columns(4)
 
    band_persona = st.session_state.personas.get('of-broken-light', {})
    band_members = band_persona.get('band_members', [])
 
    filled_positions = sum(1 for m in band_members if m.get('status') != 'Recruiting')
    col1.metric("Positions Filled", f"{filled_positions}/{len(band_members)}")
 
    band_tracks = band_persona.get('tracks_performed', [])
    col2.metric("Setlist Songs", len(band_tracks))
 
    # Load band data
    band_data = load_json_file(BAND_FILE, {
    'rehearsals': [],
    'performances': [],
    'equipment': [],
    'venues': []
    })
 
    col3.metric("Rehearsals Logged", len(band_data.get('rehearsals', [])))
    col4.metric("Performances", len(band_data.get('performances', [])))
 
    st.divider()
 
    # Band tabs
    band_tabs = st.tabs([
"Roster",
"Setlist",
"Rehearsals",
"Performances",
"Equipment" ])
 
    # ROSTER tab
    with band_tabs[0]:
    st.markdown("### Band Roster")
 
    if band_members:
    for idx, member in enumerate(band_members):
    with st.container(border=True):
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
 
    with col1:
    st.markdown(f"### {member.get('role', 'Unknown')}")
 
    status_colors = {
"Founding":"🟢",
"Recruited":"",
"Recruiting":"🟡",
"Audition":"🟠" }
    status = member.get('status', 'Recruiting')
    status_icon = status_colors.get(status,"")
    st.markdown(f"{status_icon} **Status:** {status}")
 
    with col2:
    current_name = member.get('name', 'TBD')
    new_name = st.text_input("Name", value=current_name, 
    key=f"name_{idx}", label_visibility="collapsed")
 
    if new_name != current_name:
    member['name'] = new_name
 
    with col3:
    new_status = st.selectbox(
"Status",
    ["Recruiting","Audition","Recruited","Founding"],
    index=["Recruiting","Audition","Recruited","Founding"].index(status) if status in ["Recruiting","Audition","Recruited","Founding"] else 0,
    key=f"status_{idx}",
    label_visibility="collapsed" )
 
    if new_status != status:
    member['status'] = new_status
 
    with col4:
    if st.button("Update", key=f"update_member_{idx}"):
    save_personas(st.session_state.personas)
    st.success("Updated!")
    st.rerun()
 
    # Contact info
    if status !="Recruiting":
    email = st.text_input("Email", value=member.get('email', ''), 
    key=f"email_{idx}")
    phone = st.text_input("Phone", value=member.get('phone', ''),
    key=f"phone_{idx}")
 
    if email != member.get('email', '') or phone != member.get('phone', ''):
    member['email'] = email
    member['phone'] = phone
 
    # Add position
    with st.expander("Add New Position"):
    with st.form("add_position"):
    new_role = st.text_input("Role", placeholder="Keyboard")
 
    if st.form_submit_button("Add Position"):
    if new_role:
    band_members.append({
"name":"TBD",
"role": new_role,
"status":"Recruiting",
"email":"",
"phone":"" })
    save_personas(st.session_state.personas)
    st.success("Position added!")
    st.rerun()
 
    # SETLIST tab
    with band_tabs[1]:
    st.markdown("### Setlist Builder")
 
    # Show current setlist
    if band_tracks:
    st.markdown(f"**Current Setlist:** {len(band_tracks)} songs")
 
    # Setlist with reordering
    st.markdown("#### Track Order")
 
    for idx, track_id in enumerate(band_tracks):
    # Find track info
    track_info = None
    for song in st.session_state.virtual_songs.values():
    for man in song.get('manifestations', []):
    if man.get('manifestation_id') == track_id:
    track_info = {
    'song_title': song.get('title'),
    'man_title': man.get('title')
    }
    break
    if track_info:
    break
 
    if track_info:
    col1, col2, col3 = st.columns([0.5, 3, 1])
 
    with col1:
    st.markdown(f"**{idx + 1}.**")
 
    with col2:
    st.markdown(f"**{track_info['song_title']}** - {track_info['man_title']}")
 
    with col3:
    col_a, col_b, col_c = st.columns(3)
 
    with col_a:
    if idx > 0:
    if st.button("", key=f"up_{track_id}"):
    # Move up
    band_tracks[idx], band_tracks[idx-1] = band_tracks[idx-1], band_tracks[idx]
    save_personas(st.session_state.personas)
    st.rerun()
 
    with col_b:
    if idx < len(band_tracks) - 1:
    if st.button("", key=f"down_{track_id}"):
    # Move down
    band_tracks[idx], band_tracks[idx+1] = band_tracks[idx+1], band_tracks[idx]
    save_personas(st.session_state.personas)
    st.rerun()
 
    with col_c:
    if st.button("", key=f"remove_{track_id}"):
    band_tracks.remove(track_id)
    save_personas(st.session_state.personas)
    st.rerun()
    else:
    st.info("No setlist yet. Band manifestations will appear here automatically when created.")
 
    st.divider()
 
    # Setlist statistics
    if band_tracks:
    st.markdown("### Setlist Stats")
 
    total_duration = len(band_tracks) * 4 # Assume 4 min average
 
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Songs", len(band_tracks))
    col2.metric("Est. Duration", f"{total_duration} min")
    col3.metric("Set Length", f"{total_duration // 60}h {total_duration % 60}m")
 
    # REHEARSALS tab
    with band_tabs[2]:
    st.markdown("### Rehearsal Log")
 
    rehearsals = band_data.get('rehearsals', [])
 
    # Add rehearsal
    with st.expander("Log New Rehearsal"):
    with st.form("new_rehearsal"):
    reh_date = st.date_input("Date", value=datetime.now())
    reh_location = st.text_input("Location", placeholder="Main St Studios")
 
    col1, col2 = st.columns(2)
 
    with col1:
    reh_duration = st.number_input("Duration (hours)", min_value=0.5, max_value=8.0, value=2.0, step=0.5)
 
    with col2:
    reh_attendees = st.multiselect("Attendees", 
    [m.get('name', 'TBD') for m in band_members])
 
    reh_songs = st.multiselect("Songs Rehearsed",
    band_tracks if band_tracks else [],
    format_func=lambda x: x) # Show track IDs for now
 
    reh_notes = st.text_area("Notes", height=100,
    placeholder="What was accomplished, issues, next steps...")
 
    if st.form_submit_button("Log Rehearsal"):
    new_rehearsal = {
    'date': reh_date.strftime("%Y-%m-%d"),
    'location': reh_location,
    'duration': reh_duration,
    'attendees': reh_attendees,
    'songs': reh_songs,
    'notes': reh_notes,
    'logged': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    rehearsals.append(new_rehearsal)
    band_data['rehearsals'] = rehearsals
    save_json_file(BAND_FILE, band_data)
 
    st.success("Rehearsal logged!")
    st.rerun()
 
    # Display rehearsals
    if rehearsals:
    st.markdown("#### Recent Rehearsals")
 
    for reh in sorted(rehearsals, key=lambda x: x.get('date', ''), reverse=True)[:10]:
    with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1, 1])
 
    with col1:
    st.markdown(f"**{reh.get('date', 'Unknown')}**")
    st.caption(reh.get('location', 'Unknown location'))
 
    with col2:
    st.metric("Duration", f"{reh.get('duration', 0)}h")
 
    with col3:
    st.metric("Attendees", len(reh.get('attendees', [])))
 
    if reh.get('notes'):
    st.markdown(reh['notes'])
 
    if reh.get('songs'):
    st.caption(f"Songs: {len(reh['songs'])}")
    else:
    st.info("No rehearsals logged yet")
 
    # PERFORMANCES tab
    with band_tabs[3]:
    st.markdown("### Performance Schedule")
 
    performances = band_data.get('performances', [])
 
    # Add performance
    with st.expander("Schedule Performance"):
    with st.form("new_performance"):
    perf_date = st.date_input("Date", value=datetime.now())
    perf_venue = st.text_input("Venue", placeholder="The Sinclair, Cambridge MA")
    perf_type = st.selectbox("Type", ["Show","Festival","Private Event","Audition"])
 
    col1, col2 = st.columns(2)
 
    with col1:
    perf_doors = st.time_input("Doors", value=datetime.strptime("19:00","%H:%M").time())
    perf_set = st.time_input("Set Time", value=datetime.strptime("20:00","%H:%M").time())
 
    with col2:
    perf_payment = st.number_input("Payment ($)", min_value=0, value=500, step=100)
    perf_capacity = st.number_input("Venue Capacity", min_value=0, value=200, step=50)
 
    perf_notes = st.text_area("Notes", height=100)
 
    if st.form_submit_button("Schedule Performance"):
    new_perf = {
    'date': perf_date.strftime("%Y-%m-%d"),
    'venue': perf_venue,
    'type': perf_type,
    'doors': perf_doors.strftime("%H:%M"),
    'set_time': perf_set.strftime("%H:%M"),
    'payment': perf_payment,
    'capacity': perf_capacity,
    'notes': perf_notes,
    'status': 'Scheduled',
    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    performances.append(new_perf)
    band_data['performances'] = performances
    save_json_file(BAND_FILE, band_data)
 
    st.success("Performance scheduled!")
    st.rerun()
 
    # Display performances
    if performances:
    st.markdown("#### Upcoming Shows")
 
    upcoming = [p for p in performances if p.get('date', '') >= datetime.now().strftime("%Y-%m-%d")]
    upcoming.sort(key=lambda x: x.get('date', ''))
 
    if upcoming:
    for perf in upcoming:
    with st.container(border=True):
    col1, col2, col3 = st.columns([2, 1, 1])
 
    with col1:
    st.markdown(f"### {perf.get('venue', 'Unknown')}")
    st.caption(f"**{perf.get('date', 'Unknown')}** - {perf.get('type', 'Show')}")
    st.caption(f"Doors: {perf.get('doors', 'TBD')} | Set: {perf.get('set_time', 'TBD')}")
 
    with col2:
    st.metric("Payment", f"${perf.get('payment', 0)}")
 
    with col3:
    st.metric("Capacity", perf.get('capacity', 0))
 
    if perf.get('notes'):
    st.info(perf['notes'])
    else:
    st.info("No upcoming performances scheduled")
    else:
    st.info("No performances scheduled yet")
 
    # EQUIPMENT tab
    with band_tabs[4]:
    st.markdown("### Equipment Inventory")
 
    equipment = band_data.get('equipment', [])
 
    # Add equipment
    with st.expander("Add Equipment"):
    with st.form("new_equipment"):
    equip_name = st.text_input("Item Name", placeholder="Fender Stratocaster")
    equip_type = st.selectbox("Type", ["Guitar","Bass","Drums","Keyboard","Amp","PA","Mic","Cable","Other"])
    equip_owner = st.selectbox("Owner", [m.get('name', 'TBD') for m in band_members] + ["Band"])
    equip_condition = st.selectbox("Condition", ["Excellent","Good","Fair","Needs Repair"])
    equip_notes = st.text_area("Notes", height=60)
 
    if st.form_submit_button("Add Item"):
    new_equip = {
    'name': equip_name,
    'type': equip_type,
    'owner': equip_owner,
    'condition': equip_condition,
    'notes': equip_notes,
    'added': datetime.now().strftime("%Y-%m-%d")
    }
 
    equipment.append(new_equip)
    band_data['equipment'] = equipment
    save_json_file(BAND_FILE, band_data)
 
    st.success("Equipment added!")
    st.rerun()
 
    # Display equipment
    if equipment:
    # Group by type
    by_type = {}
    for item in equipment:
    item_type = item.get('type', 'Other')
    if item_type not in by_type:
    by_type[item_type] = []
    by_type[item_type].append(item)
 
    for equip_type, items in sorted(by_type.items()):
    with st.expander(f"{equip_type} ({len(items)} items)"):
    for item in items:
    col1, col2, col3 = st.columns([3, 1, 1])
 
    with col1:
    st.markdown(f"**{item.get('name', 'Unknown')}**")
    if item.get('notes'):
    st.caption(item['notes'])
 
    with col2:
    st.caption(f"Owner: {item.get('owner', 'Unknown')}")
 
    with col3:
    condition = item.get('condition', 'Unknown')
    condition_colors = {
"Excellent":"🟢",
"Good":"",
"Fair":"🟡",
"Needs Repair":"" }
    st.caption(f"{condition_colors.get(condition, '')} {condition}")
    else:
    st.info("No equipment logged yet")

# --- TAB 10: ARTIST OUTREACH ---
with tabs[9]:
    st.subheader("Artist Outreach Tracker")
    st.markdown("Track pitching songs to established artists")
 
    render_notes_section("artist_outreach","Artist Outreach")
 
    st.divider()
 
    # Load artist targets
    artist_targets = load_json_file(ARTIST_TARGETS_FILE, {})
 
    # Overall stats
    col1, col2, col3, col4 = st.columns(4)
 
    col1.metric("Target Artists", len(artist_targets))
 
    contacted = sum(1 for a in artist_targets.values() if a.get('status') not in ['Research', 'Not Contacted'])
    col2.metric("Contacted", contacted)
 
    interested = sum(1 for a in artist_targets.values() if a.get('status') == 'Interested')
    col3.metric("Interested", interested)
 
    active_pitches = sum(1 for a in artist_targets.values() if a.get('status') in ['Sent Demo', 'Follow-up'])
    col4.metric("Active Pitches", active_pitches)
 
    st.divider()
 
    # Add new target artist
    with st.expander("Add Target Artist"):
    with st.form("new_artist_target"):
    artist_name = st.text_input("Artist Name", placeholder="Phoebe Bridgers")
 
    col1, col2 = st.columns(2)
 
    with col1:
    artist_genre = st.text_input("Genre", placeholder="Indie/Folk")
    artist_label = st.text_input("Label", placeholder="Dead Oceans")
 
    with col2:
    artist_priority = st.selectbox("Priority", ["High","Medium","Low"])
    artist_status = st.selectbox("Initial Status", [
"Research","Not Contacted","Contacted","Sent Demo", 
"Follow-up","Interested","Passed","Deal" ])
 
    # Song matching
    if st.session_state.virtual_songs:
    st.markdown("**Suggested Songs:**")
    suggested_songs = st.multiselect(
"Which songs fit this artist?",
    list(st.session_state.virtual_songs.keys()),
    format_func=lambda x: st.session_state.virtual_songs[x].get('title', x)
    )
    else:
    suggested_songs = []
 
    artist_fit = st.text_area("Why This Artist?", height=100,
    placeholder="Matches introspective melancholy style, surveillance themes resonate...")
 
    artist_contact = st.text_input("Contact Info", placeholder="Email, manager, agent...")
 
    if st.form_submit_button("Add Artist Target"):
    if artist_name:
    artist_id = f"artist_{len(artist_targets) + 1:03d}" 
    new_target = {
    'artist_id': artist_id,
    'name': artist_name,
    'genre': artist_genre,
    'label': artist_label,
    'priority': artist_priority,
    'status': artist_status,
    'suggested_songs': suggested_songs,
    'fit_reasoning': artist_fit,
    'contact_info': artist_contact,
    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'interactions': [],
    'notes': ''
    }
 
    artist_targets[artist_id] = new_target
    save_json_file(ARTIST_TARGETS_FILE, artist_targets)
 
    st.success(f"Added {artist_name} to targets!")
    st.rerun()
 
    st.divider()
 
    # Filter and display targets
    col1, col2, col3 = st.columns(3)
 
    with col1:
    filter_status = st.selectbox("Filter by Status", [
"All","Research","Not Contacted","Contacted","Sent Demo",
"Follow-up","Interested","Passed","Deal" ])
 
    with col2:
    filter_priority = st.selectbox("Filter by Priority", ["All","High","Medium","Low"])
 
    with col3:
    sort_by = st.selectbox("Sort by", ["Name","Priority","Status","Date Added"])
 
    st.divider()
 
    # Display artist targets
    if artist_targets:
    st.markdown("### Target Artists")
 
    # Apply filters
    filtered_targets = []
 
    for artist_id, artist in artist_targets.items():
    # Status filter
    if filter_status !="All"and artist.get('status') != filter_status:
    continue
 
    # Priority filter
    if filter_priority !="All"and artist.get('priority') != filter_priority:
    continue
 
    filtered_targets.append((artist_id, artist))
 
    # Sort
    if sort_by =="Name":
    filtered_targets.sort(key=lambda x: x[1].get('name', ''))
    elif sort_by =="Priority":
    priority_order = {"High": 0,"Medium": 1,"Low": 2}
    filtered_targets.sort(key=lambda x: priority_order.get(x[1].get('priority', 'Low'), 3))
    elif sort_by =="Date Added":
    filtered_targets.sort(key=lambda x: x[1].get('created', ''), reverse=True)
 
    # Display
    for artist_id, artist in filtered_targets:
    with st.expander(f"{artist.get('name', 'Unknown')} - {artist.get('status', 'Unknown')}", expanded=False):
    col1, col2 = st.columns([2, 1])
 
    with col1:
    st.markdown(f"**Genre:** {artist.get('genre', 'Unknown')}")
    st.markdown(f"**Label:** {artist.get('label', 'Unknown')}")
    st.markdown(f"**Contact:** {artist.get('contact_info', 'N/A')}")
 
    if artist.get('fit_reasoning'):
    st.info(f"**Why:** {artist['fit_reasoning']}")
 
    with col2:
    # Priority badge
    priority = artist.get('priority', 'Low')
    priority_colors = {
"High":"",
"Medium":"🟡",
"Low":"🟢" }
    st.markdown(f"{priority_colors.get(priority, '')} **Priority: {priority}**")
 
    # Status
    status = artist.get('status', 'Research')
    st.markdown(f"**Status:** {status}")
 
    st.divider()
 
    # Suggested songs
    suggested = artist.get('suggested_songs', [])
    if suggested:
    st.markdown("**Suggested Songs:**")
    for song_id in suggested:
    song = st.session_state.virtual_songs.get(song_id, {})
    st.markdown(f"- {song.get('title', song_id)}")
 
    st.divider()
 
    # Interactions log
    st.markdown("**Interaction Log:**")
 
    interactions = artist.get('interactions', [])
 
    if interactions:
    for interaction in sorted(interactions, key=lambda x: x.get('date', ''), reverse=True):
    with st.container(border=True):
    st.markdown(f"**{interaction.get('date', 'Unknown')}** - {interaction.get('type', 'Unknown')}")
    st.markdown(interaction.get('notes', ''))
    else:
    st.caption("No interactions logged yet")
 
    # Add interaction
    with st.form(f"add_interaction_{artist_id}"):
    int_date = st.date_input("Date", value=datetime.now(), key=f"int_date_{artist_id}")
    int_type = st.selectbox("Type", [
"Initial Research","Email Sent","Follow-up", 
"Phone Call","Meeting","Demo Sent","Response Received" ], key=f"int_type_{artist_id}")
    int_notes = st.text_area("Notes", height=60, key=f"int_notes_{artist_id}")
 
    col_a, col_b = st.columns(2)
 
    with col_a:
    if st.form_submit_button("Log Interaction"):
    new_interaction = {
    'date': int_date.strftime("%Y-%m-%d"),
    'type': int_type,
    'notes': int_notes
    }
 
    interactions.append(new_interaction)
    artist['interactions'] = interactions
    save_json_file(ARTIST_TARGETS_FILE, artist_targets)
 
    st.success("Interaction logged!")
    st.rerun()
 
    st.divider()
 
    # Update status
    col1, col2, col3 = st.columns([2, 1, 1])
 
    with col1:
    new_status = st.selectbox("Update Status", [
"Research","Not Contacted","Contacted","Sent Demo",
"Follow-up","Interested","Passed","Deal" ], index=["Research","Not Contacted","Contacted","Sent Demo",
"Follow-up","Interested","Passed","Deal"].index(status) if status in [
"Research","Not Contacted","Contacted","Sent Demo",
"Follow-up","Interested","Passed","Deal" ] else 0, key=f"status_{artist_id}")
 
    with col2:
    if st.button("Update", key=f"update_{artist_id}"):
    artist['status'] = new_status
    save_json_file(ARTIST_TARGETS_FILE, artist_targets)
    st.success("Status updated!")
    st.rerun()
 
    with col3:
    if st.button("Delete", key=f"delete_{artist_id}"):
    del artist_targets[artist_id]
    save_json_file(ARTIST_TARGETS_FILE, artist_targets)
    st.success("Deleted!")
    st.rerun()
    else:
    st.info("No target artists yet. Add your first target above!")
 
    st.markdown("### Suggested Artists to Consider:")
 
    suggestions = [
    ("Phoebe Bridgers","Indie/Folk","Introspective melancholy"),
    ("Julien Baker","Indie/Rock","Emotional intensity"),
    ("Norah Jones","Jazz","Sophisticated arrangements"),
    ("Bon Iver","Indie/Folk","Atmospheric arrangements"),
    ("The National","Alternative","Brooding intensity")
    ]
 
    for name, genre, fit in suggestions:
    st.markdown(f"- **{name}** ({genre}) - {fit}")

# --- TAB 11: PROTOSONGS ---
with tabs[10]:
    st.subheader("Protosong Workshop")
    st.markdown("Archive and develop your 100-200 cassette songs from the 1980s-1990s")
 
    render_notes_section("protosongs","Protosong Workshop")
 
    st.divider()
 
    # Load protosongs
    protosongs = load_json_file(PROTOSONGS_FILE, {})
 
    # Stats
    col1, col2, col3, col4 = st.columns(4)
 
    col1.metric("Protosongs Archived", len(protosongs))
 
    digitized = sum(1 for p in protosongs.values() if p.get('digitized', False))
    col2.metric("Digitized", digitized)
 
    transcribed = sum(1 for p in protosongs.values() if p.get('lyrics_transcribed', False))
    col3.metric("Lyrics Transcribed", transcribed)
 
    graduated = sum(1 for p in protosongs.values() if p.get('graduated_to_vs', False))
    col4.metric("Graduated to VS", graduated)
 
    st.divider()
 
    # Add new protosong
    with st.expander("Archive New Protosong"):
    with st.form("new_protosong"):
    proto_title = st.text_input("Title (from cassette)", placeholder="Song title as heard on tape")
 
    col1, col2 = st.columns(2)
 
    with col1:
    proto_tape = st.text_input("Tape ID", placeholder="Cassette A, Side 1, Track 3")
    proto_year = st.number_input("Year Recorded", min_value=1980, max_value=2000, value=1985)
 
    with col2:
    proto_digitized = st.checkbox("Digitized?")
    proto_file = st.text_input("Digital File", placeholder="cassette_a_s1_t3.mp3") if proto_digitized else"" 
    proto_lyrics = st.text_area("Lyrics (transcribed)", height=200,
    placeholder="Transcribe lyrics from cassette...")
 
    proto_lyrics_complete = st.checkbox("Lyrics fully transcribed")
 
    proto_writing_context = st.text_area("Writing Context", height=100,
    placeholder="What was happening when this was written? What inspired it?")
 
    proto_notes = st.text_area("Notes", height=100,
    placeholder="Sound quality, tape condition, future ideas...")
 
    if st.form_submit_button("Archive Protosong", type="primary"):
    if proto_title:
    proto_id = f"proto_{len(protosongs) + 1:03d}" 
    new_proto = {
    'proto_id': proto_id,
    'title': proto_title,
    'tape_id': proto_tape,
    'year_recorded': proto_year,
    'digitized': proto_digitized,
    'digital_file': proto_file,
    'lyrics': proto_lyrics,
    'lyrics_transcribed': proto_lyrics_complete,
    'writing_context': proto_writing_context,
    'notes': proto_notes,
    'graduated_to_vs': False,
    'vs_id': None,
    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'evolution_log': []
    }
 
    protosongs[proto_id] = new_proto
    save_json_file(PROTOSONGS_FILE, protosongs)
 
    st.success(f"Protosong '{proto_title}' archived!")
    st.rerun()
 
    st.divider()
 
    # Filter and display
    col1, col2, col3 = st.columns(3)
 
    with col1:
    filter_status = st.selectbox("Filter", [
"All","Needs Digitizing","Needs Lyrics","Ready to Develop","Graduated" ])
 
    with col2:
    sort_proto_by = st.selectbox("Sort by", ["Title","Year","Date Added"])
 
    with col3:
    search_term = st.text_input("Search", placeholder="Search titles...")
 
    st.divider()
 
    # Display protosongs
    if protosongs:
    st.markdown("### Protosong Archive")
 
    # Apply filters
    filtered_protos = []
 
    for proto_id, proto in protosongs.items():
    # Status filter
    if filter_status =="Needs Digitizing"and proto.get('digitized', False):
    continue
    elif filter_status =="Needs Lyrics"and proto.get('lyrics_transcribed', False):
    continue
    elif filter_status =="Ready to Develop"and (not proto.get('digitized', False) or not proto.get('lyrics_transcribed', False)):
    continue
    elif filter_status =="Graduated"and not proto.get('graduated_to_vs', False):
    continue
 
    # Search filter
    if search_term and search_term.lower() not in proto.get('title', '').lower():
    continue
 
    filtered_protos.append((proto_id, proto))
 
    # Sort
    if sort_proto_by =="Title":
    filtered_protos.sort(key=lambda x: x[1].get('title', ''))
    elif sort_proto_by =="Year":
    filtered_protos.sort(key=lambda x: x[1].get('year_recorded', 0), reverse=True)
    elif sort_proto_by =="Date Added":
    filtered_protos.sort(key=lambda x: x[1].get('created', ''), reverse=True)
 
    # Display count
    st.caption(f"Showing {len(filtered_protos)} protosongs")
 
    # Display each protosong
    for proto_id, proto in filtered_protos:
    # Status indicators
    status_icons = []
    if proto.get('digitized'):
    status_icons.append("Digitized")
    else:
    status_icons.append("Cassette Only")
 
    if proto.get('lyrics_transcribed'):
    status_icons.append("Lyrics")
    else:
    status_icons.append("No Lyrics")
 
    if proto.get('graduated_to_vs'):
    status_icons.append("Graduated")
 
    status_str ="|".join(status_icons)
 
    with st.expander(f"{proto.get('title', 'Untitled')} ({proto.get('year_recorded', 'Unknown')}) - {status_str}"):
    col1, col2 = st.columns([2, 1])
 
    with col1:
    st.markdown(f"**Tape ID:** {proto.get('tape_id', 'Unknown')}")
    st.markdown(f"**Year:** {proto.get('year_recorded', 'Unknown')}")
 
    if proto.get('digital_file'):
    st.markdown(f"**Digital File:** {proto['digital_file']}")
 
    if proto.get('writing_context'):
    st.info(f"**Context:** {proto['writing_context']}")
 
    with col2:
    st.markdown("**Status:**")
    st.checkbox("Digitized", value=proto.get('digitized', False), 
    key=f"dig_{proto_id}", disabled=True)
    st.checkbox("Lyrics Complete", value=proto.get('lyrics_transcribed', False),
    key=f"lyr_{proto_id}", disabled=True)
    st.checkbox("Graduated", value=proto.get('graduated_to_vs', False),
    key=f"grad_{proto_id}", disabled=True)
 
    # Lyrics
    if proto.get('lyrics'):
    with st.expander("Lyrics"):
    lyrics_text = st.text_area("Edit Lyrics", value=proto['lyrics'],
    height=200, key=f"lyrics_{proto_id}")
 
    col_a, col_b = st.columns(2)
 
    with col_a:
    if st.button("Save Lyrics", key=f"save_lyrics_{proto_id}"):
    proto['lyrics'] = lyrics_text
    save_json_file(PROTOSONGS_FILE, protosongs)
    st.success("Lyrics saved!")
 
    with col_b:
    lyrics_complete = st.checkbox("Mark as Complete",
    value=proto.get('lyrics_transcribed', False),
    key=f"complete_{proto_id}")
    if lyrics_complete != proto.get('lyrics_transcribed', False):
    proto['lyrics_transcribed'] = lyrics_complete
    save_json_file(PROTOSONGS_FILE, protosongs)
    st.rerun()
 
    # Evolution log
    st.markdown("**Evolution Log:**")
 
    evolution = proto.get('evolution_log', [])
 
    if evolution:
    for entry in sorted(evolution, key=lambda x: x.get('date', ''), reverse=True):
    with st.container(border=True):
    st.markdown(f"**{entry.get('date', 'Unknown')}** - {entry.get('type', 'Update')}")
    st.markdown(entry.get('notes', ''))
    else:
    st.caption("No evolution entries yet")
 
    # Add evolution entry
    with st.form(f"evolution_{proto_id}"):
    evo_date = st.date_input("Date", value=datetime.now(), key=f"evo_date_{proto_id}")
    evo_type = st.selectbox("Type", [
"Digitized","Lyrics Updated","Arrangement Ideas",
"Production Notes","Other" ], key=f"evo_type_{proto_id}")
    evo_notes = st.text_area("Notes", height=60, key=f"evo_notes_{proto_id}")
 
    if st.form_submit_button("Log Evolution"):
    new_entry = {
    'date': evo_date.strftime("%Y-%m-%d"),
    'type': evo_type,
    'notes': evo_notes
    }
 
    evolution.append(new_entry)
    proto['evolution_log'] = evolution
    save_json_file(PROTOSONGS_FILE, protosongs)
 
    st.success("Evolution logged!")
    st.rerun()
 
    st.divider()
 
    # Actions
    col1, col2, col3 = st.columns(3)
 
    with col1:
    if not proto.get('graduated_to_vs') and proto.get('digitized') and proto.get('lyrics_transcribed'):
    if st.button("Graduate to Virtual Song", key=f"graduate_{proto_id}", type="primary"):
    # Create virtual song from protosong
    new_vs_id = f"vs_{proto.get('title', 'untitled').lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}" 
    new_vs = {
    'ideal_id': new_vs_id,
    'title': proto.get('title'),
    'the_ideal': {
    'genesis': {
    'year_written': proto.get('year_recorded'),
    'themes': [],
    'lyrics': proto.get('lyrics', ''),
    'writing_context': proto.get('writing_context', ''),
    'protosong_origin': proto_id
    },
    'compositional_rating': {
    'melody': 0,
    'harmony': 0,
    'lyrics': 0,
    'structure': 0,
    'aggregate': 0
    }
    },
    'manifestations': [],
    'living_archive_chapters': [
    {
    'chapter_id': 'ch_genesis',
    'date': str(proto.get('year_recorded')),
    'type': 'Genesis',
    'title': 'Protosong Origin',
    'description': f"Original cassette recording from {proto.get('tape_id')}",
    'significance': 'The birth of this composition',
    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    ],
    'strategic_positioning': {},
    'created': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
 
    st.session_state.virtual_songs[new_vs_id] = new_vs
    save_virtual_songs(st.session_state.virtual_songs)
 
    # Mark as graduated
    proto['graduated_to_vs'] = True
    proto['vs_id'] = new_vs_id
    save_json_file(PROTOSONGS_FILE, protosongs)
 
    st.success(f"Graduated to Virtual Song: {proto.get('title')}!")
    st.info(f"Virtual Song ID: {new_vs_id}")
    st.rerun()
    elif proto.get('graduated_to_vs'):
    st.info(f"Graduated to: {proto.get('vs_id')}")
 
    with col2:
    if st.button("Edit", key=f"edit_{proto_id}"):
    st.info("Edit mode (implement inline editing)")
 
    with col3:
    if st.button("Delete", key=f"delete_proto_{proto_id}"):
    del protosongs[proto_id]
    save_json_file(PROTOSONGS_FILE, protosongs)
    st.success("Protosong deleted!")
    st.rerun()
    else:
    st.info("No protosongs archived yet. Start documenting your cassette archive above!")
 
    st.markdown("### Workflow Guide")
 
    st.markdown(""" **The Protosong Workshop Process:**
 
    1. **Archive** - Document each song from your cassettes
    - Tape ID, track number, year
    - Initial notes on sound quality, condition
 
    2. **Digitize** - Transfer from cassette to digital
    - Upload/link to digital file
    - Mark as digitized
 
    3. **Transcribe** - Extract lyrics from recording
    - Listen carefully, transcribe words
    - Mark as complete when done
 
    4. **Document Context** - Remember why you wrote it
    - What was happening in your life?
    - What inspired this song?
 
    5. **Evolve** - Track development over time
    - Arrangement ideas
    - Production notes
    - Future plans
 
    6. **Graduate** - Transform into Virtual Song
    - Once digitized + lyrics complete
    - Becomes full Virtual Song
    - Protosong preserved as origin story
""")

# --- TAB 12: ANALYTICS ---
with tabs[11]:
    st.subheader("Platform Analytics")
    st.markdown("Comprehensive performance intelligence across the Platonic Album system")
 
    render_notes_section("analytics","Analytics")
 
    st.divider()
 
    # Top-level metrics
    st.markdown("### Platform Overview")
 
    col1, col2, col3, col4, col5 = st.columns(5)
 
    total_vs = len(st.session_state.virtual_songs)
    col1.metric("Virtual Songs", total_vs)
 
    total_manifestations = sum(len(s.get('manifestations', [])) for s in st.session_state.virtual_songs.values())
    col2.metric("Manifestations", total_manifestations)
 
    density = total_manifestations / total_vs if total_vs > 0 else 0
    col3.metric("Avg Density", f"{density:.1f}x")
 
    pantheon_count = 0
    for song in st.session_state.virtual_songs.values():
    for man in song.get('manifestations', []):
    stats = get_vote_stats('manifestation', man.get('manifestation_id'))
    if stats['pantheon_status']:
    pantheon_count += 1
    col4.metric("Pantheon Items", pantheon_count)
 
    total_votes = sum(
    len(v.get('upvotes', [])) + len(v.get('downvotes', []))
    for v in st.session_state.votes.values()
    )
    col5.metric("Total Votes", total_votes)
 
    st.divider()
 
    # Detailed analytics tabs
    analytics_tabs = st.tabs([
"Virtual Songs",
"Personas",
"Triangulation",
"Voting Intelligence",
"My Albums",
"Community" ])
 
    # Virtual Songs Analytics
    with analytics_tabs[0]:
    st.markdown("### Virtual Songs Performance")
 
    if st.session_state.virtual_songs:
    songs_data = []
 
    for song_id, song in st.session_state.virtual_songs.items():
    manifestations = song.get('manifestations', [])
    reviews = st.session_state.reviews.get(song_id, [])
    chapters = song.get('living_archive_chapters', [])
 
    # Calculate voting stats across all manifestations
    total_song_votes = 0
    avg_approval = 0
    pantheon_manifestations = 0
 
    for man in manifestations:
    stats = get_vote_stats('manifestation', man.get('manifestation_id'))
    total_song_votes += stats['total_votes']
    if stats['total_votes'] > 0:
    avg_approval += stats['approval_rate']
    if stats['pantheon_status']:
    pantheon_manifestations += 1
 
    avg_approval = avg_approval / len(manifestations) if manifestations else 0
 
    rating = song.get('the_ideal', {}).get('compositional_rating', {}).get('aggregate', 0)
 
    songs_data.append({
"Title": song.get('title', song_id),
"Comp Rating": f"{rating:.1f}",
"Manifestations": len(manifestations),
"Pantheon": pantheon_manifestations,
"Avg Approval": f"{avg_approval:.0f}%",
"Total Votes": total_song_votes,
"Reviews": len(reviews),
"Archive Chapters": len(chapters),
"Density": f"{len(manifestations):.0f}x" })
 
    df = pd.DataFrame(songs_data)
 
    # Sort options
    sort_by = st.selectbox("Sort by", [
"Title","Comp Rating","Manifestations","Pantheon","Avg Approval","Total Votes" ])
 
    if sort_by =="Title":
    df = df.sort_values("Title")
    else:
    # Convert to numeric for sorting
    df = df.sort_values(sort_by, ascending=False, key=lambda x: pd.to_numeric(x.str.replace(r'[^0-9.]', '', regex=True), errors='coerce'))
 
    st.dataframe(df, use_container_width=True, hide_index=True)
 
    st.divider()
 
    # Top performers
    col1, col2, col3 = st.columns(3)
 
    with col1:
    st.markdown("#### Highest Rated")
    top_rated = sorted(songs_data, key=lambda x: float(x['Comp Rating']), reverse=True)[:3]
    for idx, song in enumerate(top_rated):
    st.markdown(f"{idx+1}. **{song['Title']}** ({song['Comp Rating']})")
 
    with col2:
    st.markdown("#### Most Manifestations")
    top_manifested = sorted(songs_data, key=lambda x: x['Manifestations'], reverse=True)[:3]
    for idx, song in enumerate(top_manifested):
    st.markdown(f"{idx+1}. **{song['Title']}** ({song['Manifestations']})")
 
    with col3:
    st.markdown("#### Most Voted")
    top_voted = sorted(songs_data, key=lambda x: x['Total Votes'], reverse=True)[:3]
    for idx, song in enumerate(top_voted):
    st.markdown(f"{idx+1}. **{song['Title']}** ({song['Total Votes']} votes)")
 
    else:
    st.info("No virtual songs to analyze yet!")
 
    # Persona Analytics
    with analytics_tabs[1]:
    st.markdown("### Persona Performance")
 
    persona_data = []
 
    for persona_id, persona in st.session_state.personas.items():
    tracks = len(persona.get('tracks_performed', []))
 
    # Calculate voting performance for this persona's tracks
    persona_votes = 0
    persona_approval = 0
    pantheon_tracks = 0
 
    for track_id in persona.get('tracks_performed', []):
    stats = get_vote_stats('manifestation', track_id)
    persona_votes += stats['total_votes']
    if stats['total_votes'] > 0:
    persona_approval += stats['approval_rate']
    if stats['pantheon_status']:
    pantheon_tracks += 1
 
    avg_approval = persona_approval / tracks if tracks > 0 else 0
 
    # Get persona priority votes
    priority_stats = get_vote_stats('persona_priority', persona_id)
 
    persona_data.append({
"Persona": persona.get('name', persona_id),
"Type": persona.get('type', 'Unknown').replace('_', ' ').title(),
"Tracks": tracks,
"Pantheon": pantheon_tracks,
"Avg Approval": f"{avg_approval:.0f}%",
"Total Votes": persona_votes,
"Priority Votes": priority_stats['weighted_upvotes'],
"Active":""if persona.get('active') else"" })
 
    df_personas = pd.DataFrame(persona_data)
 
    # Sort
    sort_persona_by = st.selectbox("Sort by", [
"Persona","Tracks","Pantheon","Avg Approval","Total Votes","Priority Votes" ], key="persona_sort")
 
    if sort_persona_by =="Persona":
    df_personas = df_personas.sort_values("Persona")
    else:
    df_personas = df_personas.sort_values(sort_persona_by, ascending=False, 
    key=lambda x: pd.to_numeric(x.str.replace(r'[^0-9.]', '', regex=True), errors='coerce') if x.dtype == 'object' else x)
 
    st.dataframe(df_personas, use_container_width=True, hide_index=True)
 
    st.divider()
 
    # Persona insights
    col1, col2 = st.columns(2)
 
    with col1:
    st.markdown("#### Most Productive")
    top_productive = sorted(persona_data, key=lambda x: x['Tracks'], reverse=True)[:3]
    for idx, p in enumerate(top_productive):
    st.markdown(f"{idx+1}. **{p['Persona']}** ({p['Tracks']} tracks)")
 
    with col2:
    st.markdown("#### Highest Approval")
    top_approved = sorted(persona_data, key=lambda x: float(x['Avg Approval'].replace('%', '')), reverse=True)[:3]
    for idx, p in enumerate(top_approved):
    st.markdown(f"{idx+1}. **{p['Persona']}** ({p['Avg Approval']})")
 
    # Triangulation Intelligence
    with analytics_tabs[2]:
    st.markdown("### Triangulation Intelligence")
 
    st.markdown("#### Density Distribution")
 
    if st.session_state.virtual_songs:
    density_data = {}
 
    for song in st.session_state.virtual_songs.values():
    manifestation_count = len(song.get('manifestations', []))
 
    if manifestation_count not in density_data:
    density_data[manifestation_count] = 0
    density_data[manifestation_count] += 1
 
    # Display distribution
    col1, col2 = st.columns(2)
 
    with col1:
    st.markdown("**Distribution:**")
    for count in sorted(density_data.keys()):
    st.markdown(f"- {count} manifestations: {density_data[count]} songs")
 
    with col2:
    st.markdown("**Targets:**")
    under_3 = sum(density_data.get(i, 0) for i in range(3))
    at_3_to_5 = sum(density_data.get(i, 0) for i in range(3, 6))
    over_5 = sum(density_data.get(i, 0) for i in range(6, 20))
 
    st.metric("Under 3x (needs work)", under_3)
    st.metric("3-5x (good)", at_3_to_5)
    st.metric("5+ (excellent)", over_5)
 
    st.divider()
 
    # Dimensional coverage
    st.markdown("#### Dimensional Coverage")
    st.caption("Which personas are covering which songs?")
 
    coverage_matrix = {}
 
    for song_id, song in st.session_state.virtual_songs.items():
    song_title = song.get('title', song_id)
    coverage_matrix[song_title] = {}
 
    for persona_id in st.session_state.personas.keys():
    # Check if this persona has performed this song
    persona_performed = any(
    m.get('performed_by_persona') == persona_id
    for m in song.get('manifestations', [])
    )
    coverage_matrix[song_title][persona_id] =""if persona_performed else"" 
    # Create coverage dataframe
    coverage_df = pd.DataFrame(coverage_matrix).T
    coverage_df.columns = [st.session_state.personas[p]['name'] for p in coverage_df.columns]
 
    st.dataframe(coverage_df, use_container_width=True)
    else:
    st.info("No triangulation data yet!")
 
    # Voting Intelligence
    with analytics_tabs[3]:
    st.markdown("### Voting Intelligence")
 
    if total_votes > 0:
    # Voting patterns
    st.markdown("#### Voting Patterns")
 
    col1, col2, col3 = st.columns(3)
 
    # Calculate overall approval
    total_weighted_up = 0
    total_weighted_down = 0
 
    for vote_data in st.session_state.votes.values():
    for v in vote_data.get('upvotes', []):
    total_weighted_up += v['weight']
    for v in vote_data.get('downvotes', []):
    total_weighted_down += v['weight']
 
    overall_approval = (total_weighted_up / (total_weighted_up + total_weighted_down) * 100) if (total_weighted_up + total_weighted_down) > 0 else 0
 
    col1.metric("Overall Approval Rate", f"{overall_approval:.1f}%")
    col2.metric("Weighted Upvotes", total_weighted_up)
    col3.metric("Weighted Downvotes", total_weighted_down)
 
    st.divider()
 
    # Top voted items
    st.markdown("#### Most Voted Items")
 
    vote_leaderboard = []
 
    for vote_key, vote_data in st.session_state.votes.items():
    item_type = vote_data.get('item_type')
    item_id = vote_data.get('item_id')
 
    stats = get_vote_stats(item_type, item_id)
 
    if stats['total_votes'] > 0:
    # Get item name
    if item_type == 'manifestation':
    item_name = None
    for song in st.session_state.virtual_songs.values():
    for man in song.get('manifestations', []):
    if man.get('manifestation_id') == item_id:
    item_name = f"{song.get('title')} - {man.get('title')}" break
    if item_name:
    break
    elif item_type == 'persona_priority':
    item_name = st.session_state.personas.get(item_id, {}).get('name', item_id)
    else:
    item_name = item_id
 
    if item_name:
    vote_leaderboard.append({
    'Item': item_name,
    'Type': item_type.replace('_', ' ').title(),
    'Votes': stats['total_votes'],
    'Approval': f"{stats['approval_rate']:.0f}%",
    'Status': '' if stats['pantheon_status'] else ('' if stats['approval_rate'] >= 70 else '')
    })
 
    vote_leaderboard.sort(key=lambda x: x['Votes'], reverse=True)
 
    if vote_leaderboard:
    df_votes = pd.DataFrame(vote_leaderboard[:10])
    st.dataframe(df_votes, use_container_width=True, hide_index=True)
    else:
    st.info("No voting data yet!")
    else:
    st.info("No votes cast yet!")
 
    # My Albums Intelligence
    with analytics_tabs[4]:
    st.markdown("### My Albums Intelligence")
 
    if st.session_state.my_albums:
    st.metric("Total Albums Created", len(st.session_state.my_albums))
 
    # Analyze manifestation popularity in My Albums
    st.markdown("#### Most Popular Manifestations")
    st.caption("Which manifestations are chosen most often in My Albums?")
 
    manifestation_picks = {}
 
    for album in st.session_state.my_albums.values():
    for song_id, man_id in album.get('selections', {}).items():
    if man_id not in manifestation_picks:
    manifestation_picks[man_id] = 0
    manifestation_picks[man_id] += 1
 
    # Get manifestation details
    popularity_data = []
 
    for man_id, pick_count in manifestation_picks.items():
    # Find this manifestation
    for song in st.session_state.virtual_songs.values():
    for man in song.get('manifestations', []):
    if man.get('manifestation_id') == man_id:
    persona = st.session_state.personas.get(man.get('performed_by_persona', ''), {})
 
    popularity_data.append({
    'Manifestation': f"{song.get('title')} - {man.get('title')}",
    'Persona': persona.get('name', 'Unknown'),
    'Times Chosen': pick_count,
    'Popularity': f"{pick_count / len(st.session_state.my_albums) * 100:.0f}%" })
    break
 
    popularity_data.sort(key=lambda x: x['Times Chosen'], reverse=True)
 
    if popularity_data:
    df_pop = pd.DataFrame(popularity_data[:10])
    st.dataframe(df_pop, use_container_width=True, hide_index=True)
    else:
    st.info("No My Albums created yet!")
 
    # Community Analytics
    with analytics_tabs[5]:
    st.markdown("### Community Analytics")
 
    col1, col2 = st.columns(2)
 
    with col1:
    st.markdown("#### Founding Members")
 
    total_fm = len(st.session_state.founding_members)
    paid_fm = sum(1 for m in st.session_state.founding_members.values() if m.get('paid', False))
 
    st.metric("Total Members", f"{total_fm}/100")
    st.metric("Paid", paid_fm)
    st.metric("Funding Progress", f"${paid_fm * 1000:,}/100,000")
 
    if total_fm > 0:
    st.progress(paid_fm / 100)
 
    with col2:
    st.markdown("#### Documentation")
 
    total_docs = len(st.session_state.documentation)
    st.metric("Total Documents", total_docs)
 
    if total_docs > 0:
    by_category = {}
    for doc in st.session_state.documentation.values():
    cat = doc.get('category', 'unknown')
    by_category[cat] = by_category.get(cat, 0) + 1
 
    st.markdown("**By Category:**")
    for cat, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
    cat_name = DOCUMENTATION_CATEGORIES.get(cat, cat)
    st.markdown(f"- {cat_name}: {count}")

# --- TAB 13: SETTINGS ---
with tabs[12]:
    st.subheader("System Settings")
 
    render_notes_section("settings","Settings")
 
    st.divider()
 
    # Theme selector
    st.markdown("### Visual Theme")
 
    col1, col2 = st.columns([2, 1])
 
    with col1:
    # Get all themes
    all_themes = get_all_themes()
    theme_options = list(all_themes.keys())
    theme_labels = [all_themes[t] for t in theme_options]
 
    current_theme_idx = theme_options.index(st.session_state.selected_theme) if st.session_state.selected_theme in theme_options else 0
 
    selected_theme_key = st.selectbox(
"Choose Theme",
    theme_options,
    index=current_theme_idx,
    format_func=lambda x: all_themes[x]
    )
 
    # Show theme description
    selected_theme_data = get_theme(selected_theme_key)
    st.caption(f"**{selected_theme_data['name']}:** {selected_theme_data['description']}")
 
    # Show theme colors
    with st.expander("Theme Colors"):
    colors = selected_theme_data['colors']
 
    col_a, col_b, col_c = st.columns(3)
 
    with col_a:
    st.markdown("**Backgrounds:**")
    st.markdown(f"- Primary: `{colors['bg_primary']}`")
    st.markdown(f"- Secondary: `{colors['bg_secondary']}`")
    st.markdown(f"- Card: `{colors['bg_card']}`")
 
    with col_b:
    st.markdown("**Accents:**")
    st.markdown(f"- Primary: `{colors['accent_primary']}`")
    st.markdown(f"- Secondary: `{colors['accent_secondary']}`")
    st.markdown(f"- Tertiary: `{colors['accent_tertiary']}`")
 
    with col_c:
    st.markdown("**Text:**")
    st.markdown(f"- Primary: `{colors['text_primary']}`")
    st.markdown(f"- Secondary: `{colors['text_secondary']}`")
    st.markdown(f"- Muted: `{colors['text_muted']}`")
 
    # Show fonts
    with st.expander("Theme Fonts"):
    fonts = selected_theme_data['fonts']
    st.markdown(f"- **Headings:** {fonts['heading']} (weight: {fonts['heading_weight']})")
    st.markdown(f"- **Body:** {fonts['body']} (weight: {fonts['body_weight']})")
    st.markdown(f"- **Monospace:** {fonts['mono']}")
 
    with col2:
    if st.button("Apply Theme", type="primary", use_container_width=True):
    st.session_state.selected_theme = selected_theme_key
    st.success(f"Applied {selected_theme_data['name']}!")
    st.info("Theme will fully apply on next page refresh")
    st.rerun()
 
    st.markdown("---")
 
    st.markdown("### Persona-Specific Themes")
    st.caption("When viewing specific personas, their aesthetic theme automatically applies:")
 
    for persona_id, theme_id in PERSONA_THEMES.items():
    persona = st.session_state.personas.get(persona_id, {})
    theme = get_theme(theme_id)
    if persona:
    st.markdown(f"- **{persona.get('name', persona_id)}** → {theme['name']}")
 
    st.divider()
 
    # User settings
    st.markdown("### User Profile")
 
    col1, col2 = st.columns(2)
 
    with col1:
    current_user = st.text_input("User ID", value=st.session_state.current_user)
    user_role = st.selectbox("Role", ["founder","founding_member","public"],
    index=["founder","founding_member","public"].index(st.session_state.user_role))
 
    with col2:
    if st.button("Save User Settings"):
    st.session_state.current_user = current_user
    st.session_state.user_role = user_role
    st.success("Settings saved!")
 
    st.divider()
 
    # System info
    st.markdown("### System Information")
 
    st.markdown(f""" - **Version:** 7.0 - The Platonic Album OS
    - **Database:** JSON-based
    - **Active Theme:** {get_theme(st.session_state.selected_theme)['name']}
    - **Total Themes:** {len(THEMES)}
    - **Last Session:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
""")
 
    st.divider()
 
    # Data management
    st.markdown("### Data Management")
 
    col1, col2 = st.columns(2)
 
    with col1:
    if st.button("Reload All Data"):
    st.session_state.personas = load_personas()
    st.session_state.virtual_songs = load_virtual_songs()
    st.session_state.living_archive = load_living_archive()
    st.session_state.my_albums = load_my_albums()
    st.session_state.founding_members = load_founding_members()
    st.session_state.documentation = load_documentation()
    st.success("All data reloaded!")
    st.rerun()
 
    with col2:
    if st.button("Save All Data"):
    save_personas(st.session_state.personas)
    save_virtual_songs(st.session_state.virtual_songs)
    save_living_archive(st.session_state.living_archive)
    save_my_albums(st.session_state.my_albums)
    save_founding_members(st.session_state.founding_members)
    save_documentation(st.session_state.documentation)
    st.success("All data saved!")

# --- FOOTER ---
st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Virtual Songs", len(st.session_state.virtual_songs))

total_manifestations = sum(len(s.get('manifestations', [])) for s in st.session_state.virtual_songs.values())
col2.metric("Manifestations", total_manifestations)

col3.metric("Personas", len([p for p in st.session_state.personas.values() if p.get('active')]))

col4.metric("Founding Members", f"{len(st.session_state.founding_members)}/100")

st.caption(f"Fiat Musica v7.0 - The Platonic Album Operating System | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
