import streamlit as st
import pandas as pd
import os
from datetime import datetime
import json
import random

# --- CONFIGURATION ---
st.set_page_config(page_title="Fiat Musica: Triangulation Platform v6.3", layout="wide", page_icon="🎹")

# File paths
CSV_FILE = 'catalog.csv'
SETTINGS_FILE = 'settings.json'
HISTORY_FILE = 'review_history.csv'
REVIEWS_FILE = 'song_reviews.csv'
SONGS_MASTER_FILE = 'songs_master.csv'
PERSONAL_ALBUMS_FILE = 'personal_albums.csv'
VOTING_FILE = 'voting.csv'
ALBUM_AGENTS_FILE = 'album_agents.json'
DEFAULT_ALBUMS_FILE = 'default_albums.json'
VIDEO_PROJECTS_FILE = 'video_projects.json'

# --- DEFAULT CONFIGURATIONS ---
DEFAULT_DISCS = [
    "Disc 1: 1981", "Disc 2: Stadium", "Disc 3: Masterpiece", 
    "Disc 4: Atmospheres", "Disc 5: Roots", "Disc 6: Jazz", 
    "Disc 7: The Muse", "Disc 8: Classical", "Disc 9: Incubator", "Disc 10: B-Sides"
]

DEFAULT_ERAS = [
    "1981 Tapes (New Wave)", "Stadium Years (Rock)", "Introspective (Acoustic)", 
    "Atmospheres (Experimental)", "Roots Return (Folk)", "Jazz Sessions",
    "Classical Works", "Protosongs (Incubator)", "B-Sides (Fun)"
]

# --- CORE FUNCTIONS ---
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {"discs": DEFAULT_DISCS, "eras": DEFAULT_ERAS}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=2)

def load_songs_master():
    if os.path.exists(SONGS_MASTER_FILE):
        return pd.read_csv(SONGS_MASTER_FILE)
    return pd.DataFrame(columns=[
        "Song_ID", "Title", "Original_Date", "Writing_History", 
        "Lyrics", "Themes", "Imagery_Notes", "Key_Signature", 
        "Tempo", "Duration", "Status", "Notes"
    ])

def save_songs_master(df):
    df.to_csv(SONGS_MASTER_FILE, index=False)

def load_data():
    """Load catalog with 4-part scoring system"""
    if os.path.exists(CSV_FILE):
        df = pd.read_csv(CSV_FILE)
        required_cols = ["Title", "Era", "Disc", "Version", "Score", "Status", "Notes"]
        for col in required_cols:
            if col not in df.columns:
                df[col] = ""
        
        # NEW: Add 4-part scoring columns if missing
        scoring_cols = ["Score_Composition", "Score_Performance", "Score_Production", "Score_Commercial"]
        for col in scoring_cols:
            if col not in df.columns:
                # Default: distribute existing Score across 4 categories
                df[col] = df['Score'] * 2.5  # Score is 0-10, each part is 0-25
        
        return df
    
    return pd.DataFrame(columns=[
        "Title", "Era", "Disc", "Version", "Score", 
        "Score_Composition", "Score_Performance", "Score_Production", "Score_Commercial",
        "Status", "Notes"
    ])

def save_data(df):
    if os.path.exists(CSV_FILE):
        backup_name = f'catalog_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        os.rename(CSV_FILE, backup_name)
        backups = sorted([f for f in os.listdir('.') if f.startswith('catalog_backup_')])
        for old_backup in backups[:-5]:
            os.remove(old_backup)
    df.to_csv(CSV_FILE, index=False)

def ensure_song_in_master(title):
    songs_master = load_songs_master()
    if title not in songs_master['Title'].values:
        new_id = songs_master['Song_ID'].max() + 1 if not songs_master.empty else 1
        new_song = pd.DataFrame([{
            "Song_ID": new_id, "Title": title, "Original_Date": "", "Writing_History": "",
            "Lyrics": "", "Themes": "", "Imagery_Notes": "", "Key_Signature": "",
            "Tempo": "", "Duration": "", "Status": "Active", "Notes": ""
        }])
        songs_master = pd.concat([songs_master, new_song], ignore_index=True)
        save_songs_master(songs_master)

def get_all_versions(title):
    catalog = load_data()
    return catalog[catalog['Title'] == title]

# --- VIDEO PRODUCTION FUNCTIONS ---
def ensure_asset_directories(song_title):
    """Create directory structure for video assets"""
    base_path = f"assets/{song_title}"
    subdirs = ["images", "video_clips", "audio", "prompts", "exports"]
    
    created = []
    for subdir in subdirs:
        dir_path = os.path.join(base_path, subdir)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            created.append(subdir)
    
    return base_path, created

def get_asset_counts(song_title):
    """Count files in each asset directory"""
    base_path = f"assets/{song_title}"
    counts = {}
    
    if not os.path.exists(base_path):
        return counts
    
    for subdir in ["images", "video_clips", "audio", "prompts", "exports"]:
        dir_path = os.path.join(base_path, subdir)
        if os.path.exists(dir_path):
            counts[subdir] = len([f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))])
        else:
            counts[subdir] = 0
    
    return counts

def load_video_projects():
    """Load video project configurations"""
    if os.path.exists(VIDEO_PROJECTS_FILE):
        with open(VIDEO_PROJECTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_video_projects(projects):
    """Save video project configurations"""
    with open(VIDEO_PROJECTS_FILE, 'w') as f:
        json.dump(projects, f, indent=2)

def add_video_project(song_title, version, prompts):
    """Add or update a video project"""
    projects = load_video_projects()
    
    project_key = f"{song_title}_{version}"
    projects[project_key] = {
        "song_title": song_title,
        "version": version,
        "prompts": prompts,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    save_video_projects(projects)
    return project_key

# --- BULK REVIEW IMPORT ---
def bulk_import_reviews(csv_text, default_reviewer="Bulk Import"):
    """Import reviews from CSV text format"""
    reviews_df = load_reviews()
    
    imported_count = 0
    errors = []
    
    lines = csv_text.strip().split('\n')
    
    # Skip header if present
    start_idx = 1 if lines[0].lower().startswith('song') else 0
    
    for idx, line in enumerate(lines[start_idx:], start=start_idx+1):
        try:
            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 3:
                song_title = parts[0]
                song_version = parts[1]
                review_text = parts[2]
                rating = int(parts[3]) if len(parts) > 3 else 7
                review_type = parts[4] if len(parts) > 4 else "Bulk Import"
                
                review_id = reviews_df['Review_ID'].max() + 1 if not reviews_df.empty else 1
                
                new_review = pd.DataFrame([{
                    "Review_ID": review_id,
                    "Song_Title": song_title,
                    "Song_Version": song_version,
                    "Reviewer": default_reviewer,
                    "Review_Type": review_type,
                    "Review_Text": review_text,
                    "Rating": rating,
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Tags": ""
                }])
                
                reviews_df = pd.concat([reviews_df, new_review], ignore_index=True)
                imported_count += 1
        except Exception as e:
            errors.append(f"Line {idx}: {str(e)}")
    
    if imported_count > 0:
        save_reviews(reviews_df)
    
    return imported_count, errors

# --- VOTING SYSTEM ---
def load_voting():
    if os.path.exists(VOTING_FILE):
        return pd.read_csv(VOTING_FILE)
    return pd.DataFrame(columns=[
        "Vote_ID", "Song_Title", "Version", "User_ID", "Vote_Type", 
        "Timestamp", "Weight"
    ])

def save_voting(df):
    df.to_csv(VOTING_FILE, index=False)

def cast_vote(song_title, version, user_id, vote_type, weight=1):
    voting_df = load_voting()
    
    # Check if user already voted
    existing = voting_df[
        (voting_df['Song_Title'] == song_title) & 
        (voting_df['Version'] == version) &
        (voting_df['User_ID'] == user_id)
    ]
    
    if not existing.empty:
        # Update existing vote
        voting_df.loc[existing.index[0], 'Vote_Type'] = vote_type
        voting_df.loc[existing.index[0], 'Timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        # Add new vote
        vote_id = voting_df['Vote_ID'].max() + 1 if not voting_df.empty else 1
        new_vote = pd.DataFrame([{
            "Vote_ID": vote_id,
            "Song_Title": song_title,
            "Version": version,
            "User_ID": user_id,
            "Vote_Type": vote_type,
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Weight": weight
        }])
        voting_df = pd.concat([voting_df, new_vote], ignore_index=True)
    
    save_voting(voting_df)

def get_vote_stats(song_title, version):
    voting_df = load_voting()
    version_votes = voting_df[
        (voting_df['Song_Title'] == song_title) & 
        (voting_df['Version'] == version)
    ]
    
    if version_votes.empty:
        return {"total": 0, "upvotes": 0, "downvotes": 0, "approval": 0, "weighted_total": 0}
    
    upvotes = version_votes[version_votes['Vote_Type'] == 'upvote']['Weight'].sum()
    downvotes = version_votes[version_votes['Vote_Type'] == 'downvote']['Weight'].sum()
    total = len(version_votes)
    weighted_total = upvotes + downvotes
    approval = (upvotes / weighted_total * 100) if weighted_total > 0 else 0
    
    return {
        "total": total,
        "upvotes": int(upvotes),
        "downvotes": int(downvotes),
        "approval": approval,
        "weighted_total": int(weighted_total)
    }

def get_pantheon_status(approval):
    if approval >= 94:
        return "⭐⭐⭐ PANTHEON", "green"
    elif approval >= 70:
        return "⭐⭐ APPROVED", "blue"
    else:
        return "⭐ EXPERIMENTAL", "orange"

# --- PERSONAL ALBUMS ---
def load_personal_albums():
    if os.path.exists(PERSONAL_ALBUMS_FILE):
        return pd.read_csv(PERSONAL_ALBUMS_FILE)
    return pd.DataFrame(columns=[
        "Album_ID", "Album_Name", "User_ID", "Song_Title", 
        "Primary_Version", "Alternate_Versions", "Rotation_Weights", 
        "Created", "Modified"
    ])

def save_personal_albums(df):
    df.to_csv(PERSONAL_ALBUMS_FILE, index=False)

def create_personal_album(album_name, user_id, configuration):
    albums_df = load_personal_albums()
    album_id = albums_df['Album_ID'].max() + 1 if not albums_df.empty else 1
    
    new_entries = []
    for song_config in configuration:
        new_entry = {
            "Album_ID": album_id,
            "Album_Name": album_name,
            "User_ID": user_id,
            "Song_Title": song_config['title'],
            "Primary_Version": song_config['primary'],
            "Alternate_Versions": ",".join(song_config.get('alternates', [])),
            "Rotation_Weights": ",".join(map(str, song_config.get('weights', []))),
            "Created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Modified": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        new_entries.append(new_entry)
    
    new_df = pd.DataFrame(new_entries)
    albums_df = pd.concat([albums_df, new_df], ignore_index=True)
    save_personal_albums(albums_df)
    return album_id

def get_user_albums(user_id):
    albums_df = load_personal_albums()
    user_albums = albums_df[albums_df['User_ID'] == user_id]
    if user_albums.empty:
        return []
    return user_albums.groupby('Album_ID')['Album_Name'].first().to_dict()

# --- DEFAULT ALBUM TEMPLATES ---
def load_default_albums():
    if os.path.exists(DEFAULT_ALBUMS_FILE):
        with open(DEFAULT_ALBUMS_FILE, 'r') as f:
            return json.load(f)
    
    # Create default templates
    defaults = {
        "Writer's Recommended": {"description": "Jim's curated journey through the album", "priority": "score_desc"},
        "Community Pantheon": {"description": "Most-voted versions per song", "priority": "votes_desc"},
        "All Rock": {"description": "High-energy electric interpretations", "filter": "rock"},
        "All Acoustic": {"description": "Intimate stripped-down versions", "filter": "acoustic"},
        "All Jazz": {"description": "Complex sophisticated interpretations", "filter": "jazz"},
        "All Electronic": {"description": "Atmospheric modern productions", "filter": "electronic"},
        "All Instrumentals": {"description": "Pure musical interpretations", "filter": "instrumental"},
        "Energetic Journey": {"description": "Upbeat driving versions", "filter": "high_energy"},
        "Contemplative Experience": {"description": "Slow thoughtful interpretations", "filter": "contemplative"}
    }
    
    with open(DEFAULT_ALBUMS_FILE, 'w') as f:
        json.dump(defaults, f, indent=2)
    
    return defaults

# --- ALBUM AGENTS ---
def load_album_agents():
    if os.path.exists(ALBUM_AGENTS_FILE):
        with open(ALBUM_AGENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_album_agents(agents):
    with open(ALBUM_AGENTS_FILE, 'w') as f:
        json.dump(agents, f, indent=2)

def create_album_agent(disc_name, personality, focus_areas):
    agents = load_album_agents()
    agents[disc_name] = {
        "personality": personality,
        "focus_areas": focus_areas,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "last_active": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tasks_completed": 0
    }
    save_album_agents(agents)

# --- REVIEWS (from V4) ---
def load_reviews():
    if os.path.exists(REVIEWS_FILE):
        return pd.read_csv(REVIEWS_FILE)
    return pd.DataFrame(columns=[
        "Review_ID", "Song_Title", "Song_Version", "Reviewer", "Review_Type",
        "Review_Text", "Rating", "Timestamp", "Tags"
    ])

def save_reviews(reviews_df):
    reviews_df.to_csv(REVIEWS_FILE, index=False)

def get_song_reviews(song_title, version=None):
    reviews_df = load_reviews()
    if reviews_df.empty:
        return pd.DataFrame()
    
    if version:
        return reviews_df[
            (reviews_df['Song_Title'] == song_title) & 
            (reviews_df['Song_Version'] == version)
        ].sort_values('Timestamp', ascending=False)
    else:
        return reviews_df[reviews_df['Song_Title'] == song_title].sort_values('Timestamp', ascending=False)

def add_review(song_title, song_version, reviewer, review_type, review_text, rating, tags=""):
    reviews_df = load_reviews()
    review_id = reviews_df['Review_ID'].max() + 1 if not reviews_df.empty else 1
    
    new_review = pd.DataFrame([{
        "Review_ID": review_id,
        "Song_Title": song_title,
        "Song_Version": song_version,
        "Reviewer": reviewer,
        "Review_Type": review_type,
        "Review_Text": review_text,
        "Rating": rating,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Tags": tags
    }])
    
    reviews_df = pd.concat([reviews_df, new_review], ignore_index=True)
    save_reviews(reviews_df)
    return review_id

# --- REVIEW HISTORY ---
def load_review_history():
    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)
    return pd.DataFrame(columns=[
        "Song_Title", "Version", "Old_Score", "New_Score", 
        "Changed_By", "Reason", "Timestamp"
    ])

def save_review_history(df):
    df.to_csv(HISTORY_FILE, index=False)

def log_score_change(song_title, version, old_score, new_score, changed_by, reason):
    history = load_review_history()
    new_entry = pd.DataFrame([{
        "Song_Title": song_title,
        "Version": version,
        "Old_Score": old_score,
        "New_Score": new_score,
        "Changed_By": changed_by,
        "Reason": reason,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }])
    history = pd.concat([history, new_entry], ignore_index=True)
    save_review_history(history)

# --- INITIALIZE STATE ---
if 'catalog' not in st.session_state:
    st.session_state.catalog = load_data()
if 'settings' not in st.session_state:
    st.session_state.settings = load_settings()
if 'songs_master' not in st.session_state:
    st.session_state.songs_master = load_songs_master()
if 'voting' not in st.session_state:
    st.session_state.voting = load_voting()
if 'personal_albums' not in st.session_state:
    st.session_state.personal_albums = load_personal_albums()
if 'default_albums' not in st.session_state:
    st.session_state.default_albums = load_default_albums()
if 'album_agents' not in st.session_state:
    st.session_state.album_agents = load_album_agents()
if 'current_user' not in st.session_state:
    st.session_state.current_user = "demo_user"
if 'user_weight' not in st.session_state:
    st.session_state.user_weight = 10  # Founding Member = 10x weight
if 'video_projects' not in st.session_state:
    st.session_state.video_projects = load_video_projects()

# --- SIDEBAR ---
with st.sidebar:
    st.header("🎹 Fiat Musica v6.3")
    st.caption("The Complete Triangulation Platform")
    
    if not st.session_state.catalog.empty:
        unique_songs = st.session_state.catalog['Title'].nunique()
        total_versions = len(st.session_state.catalog)
        density = total_versions / unique_songs if unique_songs > 0 else 0
        
        st.metric("Unique Songs", unique_songs)
        st.metric("Total Versions", total_versions)
        st.metric("Triangulation Density", f"{density:.1f}x")
        
        voting_df = load_voting()
        if not voting_df.empty:
            st.metric("Total Votes", len(voting_df))
            
        pantheon_count = 0
        for _, row in st.session_state.catalog.iterrows():
            stats = get_vote_stats(row['Title'], row['Version'])
            if stats['approval'] >= 94:
                pantheon_count += 1
        if pantheon_count > 0:
            st.metric("Pantheon Versions", pantheon_count)
    
    st.divider()
    
    st.subheader("📥 Quick Add")
    with st.form("quick_add_form", clear_on_submit=True):
        new_title = st.text_input("Song Title")
        new_version = st.text_input("Version", placeholder="e.g., Acoustic, Rock, Jazz")
        new_disc = st.selectbox("Disc", st.session_state.settings['discs'])
        
        # NEW: 4-part scoring
        st.markdown("**4-Part Scoring (0-25 each):**")
        col1, col2 = st.columns(2)
        with col1:
            score_comp = st.number_input("Composition", 0, 25, 18, 1)
            score_perf = st.number_input("Performance", 0, 25, 18, 1)
        with col2:
            score_prod = st.number_input("Production", 0, 25, 18, 1)
            score_comm = st.number_input("Commercial", 0, 25, 15, 1)
        
        # Calculate aggregate score
        total_score = (score_comp + score_perf + score_prod + score_comm) / 10.0
        st.caption(f"Aggregate Score: {total_score:.1f}/10")
        
        if st.form_submit_button("💾 Add Version", use_container_width=True):
            if new_title and new_version:
                ensure_song_in_master(new_title)
                new_entry = pd.DataFrame([{
                    "Title": new_title,
                    "Era": st.session_state.settings['eras'][0],
                    "Disc": new_disc,
                    "Version": new_version,
                    "Score": total_score,
                    "Score_Composition": score_comp,
                    "Score_Performance": score_perf,
                    "Score_Production": score_prod,
                    "Score_Commercial": score_comm,
                    "Status": "Pending Audit",
                    "Notes": ""
                }])
                st.session_state.catalog = pd.concat([st.session_state.catalog, new_entry], ignore_index=True)
                save_data(st.session_state.catalog)
                st.success(f"✅ {new_title} ({new_version}) added!")
                st.rerun()
    
    st.divider()
    
    # Bulk import
    with st.expander("📋 Bulk Import"):
        st.markdown("**Paste multiple entries (one per line):**")
        st.caption("Format: `Title | Version | Disc | Score`")
        bulk_text = st.text_area("Bulk Data", height=150, placeholder="Every Breath | Acoustic | Disc 1: 1981 | 8.5\nEvery Breath | Rock | Disc 2: Stadium | 7.0")
        
        if st.button("Import All"):
            if bulk_text:
                lines = bulk_text.strip().split('\n')
                imported = 0
                for line in lines:
                    parts = [p.strip() for p in line.split('|')]
                    if len(parts) >= 3:
                        title = parts[0]
                        version = parts[1]
                        disc = parts[2]
                        score = float(parts[3]) if len(parts) > 3 else 7.0
                        
                        ensure_song_in_master(title)
                        new_entry = pd.DataFrame([{
                            "Title": title,
                            "Era": st.session_state.settings['eras'][0],
                            "Disc": disc,
                            "Version": version,
                            "Score": score,
                            "Score_Composition": score * 2.5,
                            "Score_Performance": score * 2.5,
                            "Score_Production": score * 2.5,
                            "Score_Commercial": score * 2.5,
                            "Status": "Pending Audit",
                            "Notes": ""
                        }])
                        st.session_state.catalog = pd.concat([st.session_state.catalog, new_entry], ignore_index=True)
                        imported += 1
                
                if imported > 0:
                    save_data(st.session_state.catalog)
                    st.success(f"✅ Imported {imported} versions!")
                    st.rerun()

# --- MAIN INTERFACE ---
st.title("🎹 Fiat Musica: The Triangulation Platform")
st.markdown("### *Experience Songs as Living Ideals* | **v6.3 Complete Edition**")

# Main tabs - ADDED Video Production
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "🎨 Compose Album",
    "🗳️ Vote & Pantheon",
    "🏠 Song Home Pages",
    "📝 Reviews Manager",
    "🎬 Video Production",
    "🤖 Album Agents",
    "💿 10-Disc Visualizer",
    "📊 Analytics",
    "📤 Export Tools",
    "⚙️ Settings"
])

# --- TAB 1: PERSONAL ALBUM COMPOSER ---
with tab1:
    st.subheader("🎨 Compose Your Personal Album")
    st.markdown("Create your unique listening experience by choosing your favorite interpretation of each song")
    
    # View existing albums
    user_albums = get_user_albums(st.session_state.current_user)
    if user_albums:
        with st.expander("📚 Your Saved Albums", expanded=False):
            for album_id, album_name in user_albums.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{album_name}** (ID: {album_id})")
                with col2:
                    if st.button("Load", key=f"load_{album_id}"):
                        st.info(f"Loading {album_name}...")
    
    st.divider()
    
    # Select disc to compose
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_disc = st.selectbox(
            "Select Album/Disc to Compose:",
            st.session_state.settings['discs']
        )
    
    with col2:
        st.markdown("**Or start from template:**")
        template_options = ["Custom (From Scratch)"] + list(st.session_state.default_albums.keys())
        selected_template = st.selectbox("Template", template_options, label_visibility="collapsed")
    
    if selected_template != "Custom (From Scratch)":
        template_info = st.session_state.default_albums[selected_template]
        st.info(f"📋 **{selected_template}**: {template_info['description']}")
    
    st.divider()
    
    # Get songs for selected disc
    disc_songs = st.session_state.catalog[st.session_state.catalog['Disc'] == selected_disc]
    unique_songs = disc_songs['Title'].unique()
    
    if len(unique_songs) == 0:
        st.info(f"No songs in {selected_disc} yet. Add songs via the sidebar!")
    else:
        st.markdown(f"### Building: **{selected_disc}**")
        st.caption(f"{len(unique_songs)} songs with triangulation pools")
        
        # Album composition interface
        album_config = []
        
        for idx, song_title in enumerate(sorted(unique_songs)):
            versions = get_all_versions(song_title)
            
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{idx+1}. {song_title}**")
                    st.caption(f"{len(versions)} versions available")
                
                with col2:
                    version_options = versions['Version'].tolist()
                    
                    # Show voting stats for each version
                    version_display = []
                    for v in version_options:
                        stats = get_vote_stats(song_title, v)
                        if stats['total'] > 0:
                            status, _ = get_pantheon_status(stats['approval'])
                            status_icon = status.split()[0]
                            version_display.append(f"{v} {status_icon} ({stats['total']} votes, {stats['approval']:.0f}%)")
                        else:
                            version_display.append(v)
                    
                    selected_version = st.selectbox(
                        "Choose Version",
                        version_options,
                        format_func=lambda x: version_display[version_options.index(x)],
                        key=f"version_{song_title}",
                        label_visibility="collapsed"
                    )
                
                with col3:
                    add_alternates = st.checkbox("Multi", key=f"multi_{song_title}", help="Include multiple versions that rotate")
                
                # Multi-version selection
                alternate_versions = []
                if add_alternates:
                    st.markdown("**Alternate Versions (will rotate):**")
                    col_a, col_b = st.columns(2)
                    
                    for v in version_options:
                        if v != selected_version:
                            with col_a if version_options.index(v) % 2 == 0 else col_b:
                                if st.checkbox(v, key=f"alt_{song_title}_{v}"):
                                    alternate_versions.append(v)
                
                # Store configuration
                song_config = {
                    'title': song_title,
                    'primary': selected_version,
                    'alternates': alternate_versions,
                    'weights': [50] + [50/len(alternate_versions)] * len(alternate_versions) if alternate_versions else [100]
                }
                album_config.append(song_config)
        
        st.divider()
        
        # Album statistics
        if album_config:
            col1, col2, col3 = st.columns(3)
            total_tracks = len(album_config)
            multi_tracks = sum(1 for c in album_config if c['alternates'])
            total_versions = sum(1 + len(c['alternates']) for c in album_config)
            
            col1.metric("Total Tracks", total_tracks)
            col2.metric("Multi-Version Tracks", multi_tracks)
            col3.metric("Total Versions Included", total_versions)
        
        # Save album
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            album_name = st.text_input("Album Name", value=f"My {selected_disc}")
        
        with col2:
            if st.button("💾 Save Album", use_container_width=True, type="primary"):
                if album_name and album_config:
                    album_id = create_personal_album(album_name, st.session_state.current_user, album_config)
                    st.success(f"✅ Album saved! ID: {album_id}")
                    st.session_state.personal_albums = load_personal_albums()
                else:
                    st.error("Album name and configuration required")
        
        with col3:
            if st.button("▶️ Preview Album", use_container_width=True):
                st.info("Preview mode: Would play your album configuration")

# --- TAB 2: VOTING & PANTHEON ---
with tab2:
    st.subheader("🗳️ Vote on Triangulation Entries")
    st.markdown("Help shape the community consensus on definitive versions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Vote Categories:**
        - ⭐⭐⭐ **Pantheon** (94%+ approval)
        - ⭐⭐ **Approved** (70-93% approval)  
        - ⭐ **Experimental** (<70% approval)
        """)
    
    with col2:
        voting_df = load_voting()
        if not voting_df.empty:
            st.metric("Total Votes Cast", len(voting_df))
            st.metric("Songs with Votes", voting_df['Song_Title'].nunique())
    
    with col3:
        st.metric("Your Vote Weight", f"{st.session_state.user_weight}x")
        st.caption("Founding Member")
        if not voting_df.empty:
            user_votes = len(voting_df[voting_df['User_ID'] == st.session_state.current_user])
            st.metric("Your Votes", user_votes)
    
    st.divider()
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_disc = st.selectbox("Filter by Disc", ["All Discs"] + st.session_state.settings['discs'])
    with col2:
        filter_status = st.selectbox("Filter by Status", ["All Status", "Pantheon Only", "Approved+", "Needs Votes"])
    with col3:
        sort_by = st.selectbox("Sort by", ["Song Title", "Most Votes", "Highest Approval", "Newest First"])
    
    st.divider()
    
    # Voting interface
    if st.session_state.catalog.empty:
        st.info("No triangulation entries yet. Add songs to start voting!")
    else:
        # Group by song
        songs = st.session_state.catalog['Title'].unique()
        
        for song_title in sorted(songs):
            versions = get_all_versions(song_title)
            
            # Apply disc filter
            if filter_disc != "All Discs":
                versions = versions[versions['Disc'] == filter_disc]
            
            if versions.empty:
                continue
            
            with st.expander(f"🎵 {song_title} ({len(versions)} versions)", expanded=False):
                for _, version_row in versions.iterrows():
                    version = version_row['Version']
                    stats = get_vote_stats(song_title, version)
                    status, status_color = get_pantheon_status(stats['approval'])
                    
                    # Apply status filter
                    if filter_status == "Pantheon Only" and stats['approval'] < 94:
                        continue
                    elif filter_status == "Approved+" and stats['approval'] < 70:
                        continue
                    elif filter_status == "Needs Votes" and stats['total'] > 0:
                        continue
                    
                    col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 0.5, 0.5])
                    
                    with col1:
                        st.markdown(f"**{version}**")
                        st.caption(f"Disc: {version_row['Disc']} | Score: {version_row['Score']} | Status: {version_row['Status']}")
                    
                    with col2:
                        st.markdown(f":{status_color}[{status}]")
                        if stats['total'] > 0:
                            st.caption(f"{stats['weighted_total']} weighted votes")
                    
                    with col3:
                        if stats['total'] > 0:
                            st.metric("Approval", f"{stats['approval']:.0f}%")
                        else:
                            st.caption("No votes yet")
                    
                    with col4:
                        if st.button("👍", key=f"up_{song_title}_{version}"):
                            cast_vote(song_title, version, st.session_state.current_user, "upvote", st.session_state.user_weight)
                            st.rerun()
                    
                    with col5:
                        if st.button("👎", key=f"down_{song_title}_{version}"):
                            cast_vote(song_title, version, st.session_state.current_user, "downvote", st.session_state.user_weight)
                            st.rerun()
                    
                    if stats['total'] > 0:
                        st.progress(stats['approval']/100)
                        st.caption(f"↑ {stats['upvotes']} upvotes | ↓ {stats['downvotes']} downvotes")

# --- TAB 3: SONG HOME PAGES (UPDATED WITH SPLIT-VIEW REVIEWS) ---
with tab3:
    st.subheader("🏠 Song Home Pages")
    st.markdown("Navigate to any song's home page to see all versions, metadata, and reviews")
    
    songs_master = load_songs_master()
    
    if songs_master.empty:
        st.info("No songs yet. Add songs via the sidebar!")
    else:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_song = st.selectbox("Select a song:", sorted(songs_master['Title'].unique()))
        
        with col2:
            if st.button("🔄 Refresh Data", use_container_width=True):
                st.session_state.songs_master = load_songs_master()
                st.session_state.catalog = load_data()
                st.rerun()
        
        if selected_song:
            song_data = songs_master[songs_master['Title'] == selected_song].iloc[0]
            versions = get_all_versions(selected_song)
            
            st.divider()
            st.markdown(f"# 🎵 {selected_song}")
            
            col1, col2, col3, col4, col5 = st.columns(5)
            col1.metric("Versions", len(versions))
            col2.metric("Avg Score", f"{versions['Score'].mean():.2f}" if not versions.empty else "N/A")
            
            voting_df = load_voting()
            song_votes = voting_df[voting_df['Song_Title'] == selected_song]
            col3.metric("Total Votes", len(song_votes))
            col4.metric("Discs", versions['Disc'].nunique() if not versions.empty else 0)
            
            # Pantheon count
            pantheon_versions = 0
            for _, v in versions.iterrows():
                stats = get_vote_stats(selected_song, v['Version'])
                if stats['approval'] >= 94:
                    pantheon_versions += 1
            col5.metric("Pantheon", pantheon_versions)
            
            st.divider()
            
            # Song tabs
            song_tab1, song_tab2, song_tab3, song_tab4 = st.tabs([
                "📋 Overview",
                "🔀 Triangulation Pool",
                "💬 Reviews",
                "✏️ Edit Metadata"
            ])
            
            with song_tab1:
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("### Core Information")
                    
                    info_data = {
                        "Date": song_data['Original_Date'] if song_data['Original_Date'] else "Not set",
                        "Key": song_data['Key_Signature'] if song_data['Key_Signature'] else "Not set",
                        "Tempo": song_data['Tempo'] if song_data['Tempo'] else "Not set",
                        "Duration": song_data['Duration'] if song_data['Duration'] else "Not set",
                        "Status": song_data['Status']
                    }
                    
                    for label, value in info_data.items():
                        st.markdown(f"**{label}:** {value}")
                    
                    if song_data['Themes']:
                        st.markdown(f"**Themes:** {song_data['Themes']}")
                    
                    if song_data['Writing_History']:
                        st.markdown("### Writing History")
                        st.markdown(song_data['Writing_History'])
                    
                    if song_data['Imagery_Notes']:
                        st.markdown("### Imagery Notes")
                        st.markdown(song_data['Imagery_Notes'])
                    
                    if song_data['Notes']:
                        st.markdown("### Additional Notes")
                        st.markdown(song_data['Notes'])
                
                with col2:
                    st.markdown("### Disc Appearances")
                    if not versions.empty:
                        for _, v in versions.iterrows():
                            stats = get_vote_stats(selected_song, v['Version'])
                            status, _ = get_pantheon_status(stats['approval'])
                            status_icon = status.split()[0]
                            
                            st.markdown(f"{status_icon} **{v['Disc']}**")
                            st.caption(f"{v['Version']} - Score: {v['Score']}")
                            if stats['total'] > 0:
                                st.caption(f"↑ {stats['approval']:.0f}% approval ({stats['total']} votes)")
                            st.markdown("---")
                
                if song_data['Lyrics']:
                    with st.expander("📜 View Lyrics", expanded=False):
                        st.text_area("", song_data['Lyrics'], height=300, disabled=True, label_visibility="collapsed")
            
            with song_tab2:
                st.markdown("### All Versions (Triangulation Pool)")
                st.caption("Compare all interpretations to perceive the compositional essence")
                
                if versions.empty:
                    st.info("No versions yet. Add via sidebar!")
                else:
                    # Sort options
                    sort_option = st.radio("Sort by:", ["Score (High to Low)", "Votes (Most to Least)", "Approval %", "Disc Name"], horizontal=True)
                    
                    for _, version in versions.iterrows():
                        stats = get_vote_stats(selected_song, version['Version'])
                        status, status_color = get_pantheon_status(stats['approval'])
                        
                        with st.container(border=True):
                            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                            
                            with col1:
                                st.markdown(f"### {version['Version']}")
                                st.caption(f"**Disc:** {version['Disc']} | **Status:** {version['Status']}")
                                if version['Notes']:
                                    st.caption(f"**Notes:** {version['Notes']}")
                            
                            with col2:
                                score_icon = "🟢" if version['Score'] >= 8.0 else "🟡" if version['Score'] >= 7.0 else "🔴"
                                st.markdown(f"### {score_icon} {version['Score']}")
                                st.caption("Equity Score")
                            
                            with col3:
                                st.markdown(f":{status_color}[{status}]")
                                if stats['total'] > 0:
                                    st.caption(f"{stats['approval']:.0f}% approval")
                            
                            with col4:
                                st.metric("Votes", stats['total'])
                                if stats['total'] > 0:
                                    st.caption(f"↑{stats['upvotes']} ↓{stats['downvotes']}")
                            
                            # Quick vote buttons
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("👍 Upvote", key=f"quick_up_{version['Version']}", use_container_width=True):
                                    cast_vote(selected_song, version['Version'], st.session_state.current_user, "upvote", st.session_state.user_weight)
                                    st.rerun()
                            with col_b:
                                if st.button("👎 Downvote", key=f"quick_down_{version['Version']}", use_container_width=True):
                                    cast_vote(selected_song, version['Version'], st.session_state.current_user, "downvote", st.session_state.user_weight)
                                    st.rerun()
            
            # NEW: SPLIT-VIEW REVIEWS
            with song_tab3:
                st.markdown("### Reviews & Feedback")
                
                song_reviews = get_song_reviews(selected_song)
                
                if song_reviews.empty:
                    st.info("No reviews yet. Add one below!")
                else:
                    st.caption(f"Showing {len(song_reviews)} reviews for this song")
                    
                    # Split reviews into AI and Board
                    ai_reviews = song_reviews[song_reviews['Review_Type'].str.contains('Gemini|AI|ai|gemini', case=False, na=False)]
                    board_reviews = song_reviews[~song_reviews['Review_Type'].str.contains('Gemini|AI|ai|gemini', case=False, na=False)]
                    
                    # Split-view display
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("#### 🤖 AI Consensus")
                        if ai_reviews.empty:
                            st.info("No AI reviews yet")
                        else:
                            for _, review in ai_reviews.iterrows():
                                with st.container(border=True):
                                    st.markdown(f"**{review['Song_Version']}** - {review['Review_Type']}")
                                    st.caption(f"By {review['Reviewer']} on {review['Timestamp'][:10]}")
                                    st.metric("Rating", f"{review['Rating']}/10")
                                    st.markdown(review['Review_Text'])
                                    if review['Tags']:
                                        st.caption(f"Tags: {review['Tags']}")
                    
                    with col2:
                        st.markdown("#### 👥 Board Feedback")
                        if board_reviews.empty:
                            st.info("No board reviews yet")
                        else:
                            for _, review in board_reviews.iterrows():
                                with st.container(border=True):
                                    st.markdown(f"**{review['Song_Version']}** - {review['Review_Type']}")
                                    st.caption(f"By {review['Reviewer']} on {review['Timestamp'][:10]}")
                                    st.metric("Rating", f"{review['Rating']}/10")
                                    st.markdown(review['Review_Text'])
                                    if review['Tags']:
                                        st.caption(f"Tags: {review['Tags']}")
                    
                    # Full history in collapsible expander
                    with st.expander("📊 Complete Review History", expanded=False):
                        st.dataframe(song_reviews[['Review_ID', 'Song_Version', 'Review_Type', 'Reviewer', 'Rating', 'Timestamp']], 
                                   use_container_width=True, hide_index=True)
                
                st.divider()
                
                # Add new review
                with st.expander("➕ Add New Review", expanded=False):
                    with st.form(f"review_form_{selected_song}"):
                        review_version = st.selectbox("Version", versions['Version'].tolist() if not versions.empty else [])
                        review_type = st.selectbox("Review Type", ["Gemini Comparative Analysis", "Founding Member Feedback", "User Review", "Artist Notes", "Critical Review"])
                        review_rating = st.slider("Rating", 1, 10, 7)
                        review_text = st.text_area("Review Text", height=150, placeholder="Enter detailed review...")
                        review_tags = st.text_input("Tags (comma-separated)", placeholder="emotional, production-quality, innovative")
                        
                        if st.form_submit_button("💾 Save Review"):
                            if review_text and review_version:
                                add_review(
                                    selected_song, 
                                    review_version, 
                                    st.session_state.current_user,
                                    review_type,
                                    review_text,
                                    review_rating,
                                    review_tags
                                )
                                st.success("Review saved!")
                                st.rerun()
            
            with song_tab4:
                st.markdown("### Edit Song Metadata")
                
                with st.form("edit_metadata"):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        edit_date = st.text_input("Original Date", value=song_data['Original_Date'])
                        edit_key = st.text_input("Key Signature", value=song_data['Key_Signature'])
                        edit_tempo = st.text_input("Tempo", value=song_data['Tempo'])
                        edit_duration = st.text_input("Duration", value=song_data['Duration'])
                    
                    with col2:
                        edit_status = st.selectbox("Status", ["Active", "Archive", "Draft", "Published"], 
                                                   index=["Active", "Archive", "Draft", "Published"].index(song_data['Status']) if song_data['Status'] in ["Active", "Archive", "Draft", "Published"] else 0)
                        edit_themes = st.text_input("Themes", value=song_data['Themes'])
                    
                    edit_history = st.text_area("Writing History", value=song_data['Writing_History'], height=150)
                    edit_imagery = st.text_area("Imagery Notes", value=song_data['Imagery_Notes'], height=100)
                    edit_lyrics = st.text_area("Lyrics", value=song_data['Lyrics'], height=300)
                    edit_notes = st.text_area("Additional Notes", value=song_data['Notes'], height=100)
                    
                    if st.form_submit_button("💾 Save Metadata", type="primary"):
                        songs_master = load_songs_master()
                        songs_master.loc[songs_master['Title'] == selected_song, 'Original_Date'] = edit_date
                        songs_master.loc[songs_master['Title'] == selected_song, 'Key_Signature'] = edit_key
                        songs_master.loc[songs_master['Title'] == selected_song, 'Tempo'] = edit_tempo
                        songs_master.loc[songs_master['Title'] == selected_song, 'Duration'] = edit_duration
                        songs_master.loc[songs_master['Title'] == selected_song, 'Status'] = edit_status
                        songs_master.loc[songs_master['Title'] == selected_song, 'Themes'] = edit_themes
                        songs_master.loc[songs_master['Title'] == selected_song, 'Writing_History'] = edit_history
                        songs_master.loc[songs_master['Title'] == selected_song, 'Imagery_Notes'] = edit_imagery
                        songs_master.loc[songs_master['Title'] == selected_song, 'Lyrics'] = edit_lyrics
                        songs_master.loc[songs_master['Title'] == selected_song, 'Notes'] = edit_notes
                        
                        save_songs_master(songs_master)
                        st.session_state.songs_master = songs_master
                        st.success("✅ Metadata saved!")
                        st.rerun()

# --- TAB 4: REVIEWS MANAGER (UPDATED WITH BULK IMPORT) ---
with tab4:
    st.subheader("📝 Reviews Manager")
    st.markdown("Comprehensive review tracking and management")
    
    reviews_df = load_reviews()
    
    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Reviews", len(reviews_df))
    if not reviews_df.empty:
        col2.metric("Songs Reviewed", reviews_df['Song_Title'].nunique())
        col3.metric("Avg Rating", f"{reviews_df['Rating'].mean():.1f}/10")
        col4.metric("Review Types", reviews_df['Review_Type'].nunique())
    
    st.divider()
    
    # NEW: Sub-tabs for Manual Entry and Bulk Import
    review_input_tab1, review_input_tab2 = st.tabs(["✍️ Manual Entry", "📋 Bulk Import"])
    
    with review_input_tab1:
        st.markdown("### Create a New Review")
        
        with st.form("add_review_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                review_song = st.selectbox("Song", sorted(st.session_state.songs_master['Title'].unique()) if not st.session_state.songs_master.empty else [])
                
                # Get versions for selected song
                if review_song:
                    song_versions = get_all_versions(review_song)
                    review_version = st.selectbox("Version", song_versions['Version'].tolist() if not song_versions.empty else [])
                else:
                    review_version = st.text_input("Version")
            
            with col2:
                review_reviewer = st.text_input("Reviewer", value=st.session_state.current_user)
                review_type = st.selectbox("Review Type", [
                    "Gemini Comparative Analysis",
                    "Founding Member Feedback",
                    "User Review",
                    "Artist Notes",
                    "Critical Review",
                    "Production Notes"
                ])
            
            review_rating = st.slider("Rating", 1, 10, 7, help="Overall quality rating")
            review_text = st.text_area("Review Text", height=200, placeholder="Enter detailed review, analysis, or feedback...")
            review_tags = st.text_input("Tags (comma-separated)", placeholder="emotional, innovative, technical, etc.")
            
            if st.form_submit_button("💾 Save Review", type="primary"):
                if review_song and review_version and review_text:
                    review_id = add_review(
                        review_song,
                        review_version,
                        review_reviewer,
                        review_type,
                        review_text,
                        review_rating,
                        review_tags
                    )
                    st.success(f"✅ Review saved! ID: {review_id}")
                    st.rerun()
                else:
                    st.error("Please fill in song, version, and review text")
    
    # NEW: Bulk Import Tab
    with review_input_tab2:
        st.markdown("### Bulk Import Reviews from CSV")
        st.markdown("""
        **CSV Format:** `Song_Title, Song_Version, Review_Text, Rating, Review_Type`
        
        Example:
```
        Every Breath, Acoustic, Beautiful intimate performance, 9, Gemini Comparative Analysis
        Every Breath, Rock, High energy production, 8, Founding Member Feedback
```
        """)
        
        with st.form("bulk_import_form"):
            bulk_csv = st.text_area("Paste CSV Data", height=250, 
                                   placeholder="Every Breath, Acoustic, Beautiful intimate performance, 9, Gemini Comparative Analysis\nEvery Breath, Rock, High energy production, 8, Founding Member Feedback")
            bulk_reviewer = st.text_input("Default Reviewer", value=st.session_state.current_user)
            
            if st.form_submit_button("📥 Import Reviews", type="primary"):
                if bulk_csv:
                    imported, errors = bulk_import_reviews(bulk_csv, bulk_reviewer)
                    
                    if imported > 0:
                        st.success(f"✅ Successfully imported {imported} reviews!")
                    
                    if errors:
                        st.warning("⚠️ Some errors occurred:")
                        for error in errors[:5]:  # Show first 5 errors
                            st.caption(error)
                    
                    if imported > 0:
                        st.rerun()
                else:
                    st.error("Please paste CSV data")
    
    st.divider()
    
    # Filter and display reviews
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_song = st.selectbox("Filter by Song", ["All Songs"] + sorted(reviews_df['Song_Title'].unique().tolist()) if not reviews_df.empty else ["All Songs"])
    
    with col2:
        filter_type = st.selectbox("Filter by Type", ["All Types"] + sorted(reviews_df['Review_Type'].unique().tolist()) if not reviews_df.empty else ["All Types"])
    
    with col3:
        sort_reviews = st.selectbox("Sort by", ["Newest First", "Oldest First", "Highest Rated", "Lowest Rated"])
    
    st.divider()
    
    if reviews_df.empty:
        st.info("No reviews yet. Add your first review above!")
    else:
        # Apply filters
        filtered_reviews = reviews_df.copy()
        
        if filter_song != "All Songs":
            filtered_reviews = filtered_reviews[filtered_reviews['Song_Title'] == filter_song]
        
        if filter_type != "All Types":
            filtered_reviews = filtered_reviews[filtered_reviews['Review_Type'] == filter_type]
        
        # Apply sorting
        if sort_reviews == "Newest First":
            filtered_reviews = filtered_reviews.sort_values('Timestamp', ascending=False)
        elif sort_reviews == "Oldest First":
            filtered_reviews = filtered_reviews.sort_values('Timestamp', ascending=True)
        elif sort_reviews == "Highest Rated":
            filtered_reviews = filtered_reviews.sort_values('Rating', ascending=False)
        elif sort_reviews == "Lowest Rated":
            filtered_reviews = filtered_reviews.sort_values('Rating', ascending=True)
        
        st.caption(f"Showing {len(filtered_reviews)} reviews")
        
        # Display reviews
        for _, review in filtered_reviews.iterrows():
            with st.container(border=True):
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {review['Song_Title']} - {review['Song_Version']}")
                    st.caption(f"**Type:** {review['Review_Type']} | **By:** {review['Reviewer']}")
                
                with col2:
                    rating_color = "green" if review['Rating'] >= 8 else "orange" if review['Rating'] >= 6 else "red"
                    st.markdown(f":{rating_color}[**Rating: {review['Rating']}/10**]")
                
                with col3:
                    st.caption(f"**ID:** {review['Review_ID']}")
                    st.caption(f"**Date:** {review['Timestamp'][:10]}")
                
                st.markdown(review['Review_Text'])
                
                if review['Tags']:
                    st.caption(f"🏷️ Tags: {review['Tags']}")

# --- TAB 5: VIDEO PRODUCTION (NEW) ---
with tab5:
    st.subheader("🎬 Video Production & Asset Manager")
    st.markdown("Manage AI-generated video assets, prompts, and production workflows")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Video Production Pipeline:
        1. **Select Song** - Choose a song and version
        2. **Asset Directories** - Auto-create folder structure
        3. **Prompt Management** - Store and version video generation prompts
        4. **Asset Tracking** - Monitor images, clips, audio files
        5. **Export** - Package for final video production
        """)
    
    with col2:
        video_projects = load_video_projects()
        st.metric("Active Projects", len(video_projects))
        
        # Count total assets
        total_assets = 0
        for song in st.session_state.songs_master['Title'].unique():
            counts = get_asset_counts(song)
            total_assets += sum(counts.values())
        st.metric("Total Assets", total_assets)
    
    st.divider()
    
    # Song selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        video_song = st.selectbox("Select Song for Video Production:", 
                                  sorted(st.session_state.songs_master['Title'].unique()) if not st.session_state.songs_master.empty else [])
    
    with col2:
        if video_song:
            song_versions = get_all_versions(video_song)
            video_version = st.selectbox("Version:", song_versions['Version'].tolist() if not song_versions.empty else ["Default"])
    
    if video_song:
        st.divider()
        
        # Asset directory management
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📁 Asset Directories")
            
            if st.button("🔨 Create/Verify Asset Directories", type="primary"):
                base_path, created = ensure_asset_directories(video_song)
                if created:
                    st.success(f"✅ Created directories: {', '.join(created)}")
                else:
                    st.info(f"✓ All directories exist at: {base_path}")
            
            # Display asset counts
            counts = get_asset_counts(video_song)
            
            if counts:
                st.markdown("**Current Assets:**")
                for asset_type, count in counts.items():
                    icon = "🖼️" if asset_type == "images" else "🎬" if asset_type == "video_clips" else "🎵" if asset_type == "audio" else "📝" if asset_type == "prompts" else "📦"
                    st.metric(f"{icon} {asset_type.title()}", count)
            else:
                st.info("No asset directory created yet. Click button above to create.")
        
        with col2:
            st.markdown("### 📝 Prompt Management")
            
            project_key = f"{video_song}_{video_version}"
            existing_project = video_projects.get(project_key, {})
            
            with st.form("video_prompt_form"):
                st.markdown("**Video Generation Prompts:**")
                
                scene_prompt = st.text_area("Scene Description", 
                                           value=existing_project.get('prompts', {}).get('scene', ''),
                                           height=100,
                                           placeholder="Describe the visual scene and atmosphere...")
                
                style_prompt = st.text_area("Visual Style", 
                                           value=existing_project.get('prompts', {}).get('style', ''),
                                           height=100,
                                           placeholder="Art style, color palette, cinematography...")
                
                motion_prompt = st.text_area("Motion & Dynamics", 
                                            value=existing_project.get('prompts', {}).get('motion', ''),
                                            height=100,
                                            placeholder="Camera movements, subject motion, transitions...")
                
                if st.form_submit_button("💾 Save Prompts", type="primary"):
                    prompts = {
                        'scene': scene_prompt,
                        'style': style_prompt,
                        'motion': motion_prompt
                    }
                    project_key = add_video_project(video_song, video_version, prompts)
                    st.session_state.video_projects = load_video_projects()
                    st.success(f"✅ Prompts saved for {project_key}")
                    st.rerun()
        
        st.divider()
        
        # Project status
        if project_key in video_projects:
            project = video_projects[project_key]
            
            st.markdown("### 📊 Project Status")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"**Created:** {project.get('created', 'N/A')}")
            with col2:
                st.markdown(f"**Modified:** {project.get('modified', 'N/A')}")
            with col3:
                status = "Ready" if counts and sum(counts.values()) > 0 else "Setup"
                st.markdown(f"**Status:** {status}")
            
            # Display saved prompts
            with st.expander("👁️ View Saved Prompts", expanded=False):
                prompts = project.get('prompts', {})
                if prompts.get('scene'):
                    st.markdown("**Scene:**")
                    st.info(prompts['scene'])
                if prompts.get('style'):
                    st.markdown("**Style:**")
                    st.info(prompts['style'])
                if prompts.get('motion'):
                    st.markdown("**Motion:**")
                    st.info(prompts['motion'])
        
        st.divider()
        
        # Export configuration
        st.markdown("### 📤 Export Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            export_format = st.selectbox("Video Format", ["MP4", "MOV", "AVI", "WebM"])
        with col2:
            export_resolution = st.selectbox("Resolution", ["1080p", "4K", "720p", "480p"])
        with col3:
            export_fps = st.selectbox("Frame Rate", ["30fps", "60fps", "24fps"])
        
        if st.button("📦 Package for Export"):
            st.info(f"Would package assets for {video_song} ({video_version}) as {export_format} @ {export_resolution} {export_fps}")

# --- TAB 6: ALBUM AGENTS ---
with tab6:
    st.subheader("🤖 Album Agents Dashboard")
    st.markdown("AI agents managing each album's performance, curation, and community engagement")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### What Album Agents Do:
        - 📊 Track performance metrics (streams, votes, engagement)
        - 📝 Generate content (social posts, newsletters, reports)
        - 🎯 Recommend triangulation opportunities
        - 👥 Monitor community sentiment
        - 🔍 Identify sync licensing opportunities
        - 📈 Analyze trends and patterns
        """)
    
    with col2:
        agents = load_album_agents()
        st.metric("Active Agents", len(agents))
        if agents:
            total_tasks = sum(a['tasks_completed'] for a in agents.values())
            st.metric("Tasks Completed", total_tasks)
    
    st.divider()
    
    # Create new agent
    with st.expander("➕ Create New Album Agent", expanded=False):
        with st.form("create_agent"):
            agent_disc = st.selectbox("Album/Disc", st.session_state.settings['discs'])
            
            agent_personality = st.selectbox("Personality", [
                "Analytical (Data-focused)",
                "Creative (Content-focused)",
                "Community (Engagement-focused)",
                "Curator (Quality-focused)",
                "Promoter (Marketing-focused)"
            ])
            
            agent_focus = st.multiselect("Focus Areas", [
                "Performance Analytics",
                "Social Media",
                "Content Generation",
                "Community Management",
                "Sync Licensing",
                "Triangulation Curation",
                "Voting Coordination",
                "Review Monitoring"
            ])
            
            if st.form_submit_button("Create Agent", type="primary"):
                if agent_focus:
                    create_album_agent(agent_disc, agent_personality, agent_focus)
                    st.session_state.album_agents = load_album_agents()
                    st.success(f"✅ Agent created for {agent_disc}!")
                    st.rerun()
                else:
                    st.error("Please select at least one focus area")
    
    st.divider()
    
    # Display existing agents
    agents = load_album_agents()
    
    if not agents:
        st.info("No agents created yet. Create your first album agent above!")
    else:
        for disc_name, agent in agents.items():
            with st.expander(f"🤖 {disc_name} Agent", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Personality:** {agent['personality']}")
                    st.markdown(f"**Created:** {agent['created']}")
                    st.markdown(f"**Last Active:** {agent['last_active']}")
                    st.markdown(f"**Tasks Completed:** {agent['tasks_completed']}")
                
                with col2:
                    st.markdown("**Focus Areas:**")
                    for focus in agent['focus_areas']:
                        st.markdown(f"- {focus}")
                
                st.divider()
                
                # Agent reports
                st.markdown("### Recent Activity")
                
                # Performance report
                disc_songs = st.session_state.catalog[st.session_state.catalog['Disc'] == disc_name]
                
                if not disc_songs.empty:
                    avg_score = disc_songs['Score'].mean()
                    total_versions = len(disc_songs)
                    unique_songs = disc_songs['Title'].nunique()
                    density = total_versions / unique_songs if unique_songs > 0 else 0
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Songs", unique_songs)
                    col2.metric("Versions", total_versions)
                    col3.metric("Density", f"{density:.1f}x")
                    
                    st.markdown(f"""
                    **Performance Summary:**
                    - Average equity score: {avg_score:.2f}
                    - Triangulation density: {density:.1f} versions per song
                    """)
                    
                    # Voting summary
                    voting_df = load_voting()
                    disc_votes = voting_df[voting_df['Song_Title'].isin(disc_songs['Title'])]
                    
                    if not disc_votes.empty:
                        pantheon_in_disc = 0
                        for _, row in disc_songs.iterrows():
                            stats = get_vote_stats(row['Title'], row['Version'])
                            if stats['approval'] >= 94:
                                pantheon_in_disc += 1
                        
                        st.markdown(f"""
                        **Community Engagement:**
                        - {len(disc_votes)} total votes cast
                        - {disc_votes['Song_Title'].nunique()} songs with votes
                        - {pantheon_in_disc} Pantheon versions
                        """)
                        
                        if not disc_votes.empty:
                            most_voted = disc_votes.groupby('Song_Title').size().sort_values(ascending=False).head(1)
                            if not most_voted.empty:
                                st.markdown(f"- Most voted: {most_voted.index[0]} ({most_voted.values[0]} votes)")
                    
                    # Recommendations
                    st.markdown("**Recommendations:**")
                    
                    approaching_pantheon = []
                    needs_triangulation = []
                    
                    for song_title in disc_songs['Title'].unique():
                        song_versions = get_all_versions(song_title)
                        
                        # Check for approaching Pantheon
                        for _, v in song_versions.iterrows():
                            stats = get_vote_stats(song_title, v['Version'])
                            if 85 <= stats['approval'] < 94 and stats['total'] >= 3:
                                approaching_pantheon.append(f"{song_title} ({v['Version']}) - {stats['approval']:.0f}%")
                        
                        # Check for insufficient triangulation
                        if len(song_versions) < 3:
                            needs_triangulation.append(f"{song_title} (only {len(song_versions)} versions)")
                    
                    if approaching_pantheon:
                        st.markdown("- **Approaching Pantheon:**")
                        for item in approaching_pantheon[:3]:
                            st.markdown(f"  - {item}")
                    
                    if needs_triangulation:
                        st.markdown("- **Needs More Triangulation:**")
                        for item in needs_triangulation[:3]:
                            st.markdown(f"  - {item}")
                else:
                    st.info(f"No songs in {disc_name} yet. Add songs to this disc to activate agent reporting.")

# --- TAB 7: 10-DISC VISUALIZER ---
with tab7:
    st.subheader("💿 The 10-Disc Box Set")
    st.markdown("View your catalog organized by disc")
    
    if st.session_state.catalog.empty:
        st.info("No songs yet!")
    else:
        # Overall stats
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Songs", st.session_state.catalog['Title'].nunique())
        col2.metric("Total Versions", len(st.session_state.catalog))
        col3.metric("Avg Equity", f"{st.session_state.catalog['Score'].mean():.2f}")
        
        voting_df = load_voting()
        total_pantheon = 0
        for _, row in st.session_state.catalog.iterrows():
            stats = get_vote_stats(row['Title'], row['Version'])
            if stats['approval'] >= 94:
                total_pantheon += 1
        col4.metric("Pantheon Versions", total_pantheon)
        
        st.divider()
        
        discs = [d for d in st.session_state.settings['discs'] if d in st.session_state.catalog["Disc"].values]
        
        cols = st.columns(2)
        for i, disc in enumerate(discs):
            with cols[i % 2]:
                disc_data = st.session_state.catalog[st.session_state.catalog["Disc"] == disc]
                avg = disc_data["Score"].mean()
                count = len(disc_data)
                unique = disc_data['Title'].nunique()
                density = count / unique if unique > 0 else 0
                
                # Count Pantheon in this disc
                disc_pantheon = 0
                for _, row in disc_data.iterrows():
                    stats = get_vote_stats(row['Title'], row['Version'])
                    if stats['approval'] >= 94:
                        disc_pantheon += 1
                
                with st.container(border=True):
                    st.markdown(f"#### {disc}")
                    
                    col_a, col_b, col_c = st.columns(3)
                    col_a.metric("Songs", unique)
                    col_b.metric("Versions", count)
                    col_c.metric("Pantheon", disc_pantheon)
                    
                    st.progress(avg/10.0)
                    st.caption(f"Avg Equity: {avg:.2f} | Density: {density:.1f}x")
                    
                    with st.expander(f"View {disc} Songs"):
                        for _, row in disc_data.iterrows():
                            stats = get_vote_stats(row['Title'], row['Version'])
                            status, _ = get_pantheon_status(stats['approval'])
                            status_icon = status.split()[0]
                            
                            st.markdown(f"{status_icon} **{row['Title']}** ({row['Version']}) - {row['Score']}")
                            if stats['total'] > 0:
                                st.caption(f"   {stats['approval']:.0f}% approval ({stats['total']} votes)")

# --- TAB 8: ANALYTICS ---
with tab8:
    st.subheader("📊 Platform Analytics")
    
    if st.session_state.catalog.empty:
        st.info("No data yet.")
    else:
        # Top metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        unique_songs = st.session_state.catalog['Title'].nunique()
        total_versions = len(st.session_state.catalog)
        triangulation_density = total_versions / unique_songs if unique_songs > 0 else 0
        
        col1.metric("Unique Songs", unique_songs)
        col2.metric("Total Versions", total_versions)
        col3.metric("Triangulation Density", f"{triangulation_density:.1f}x")
        
        voting_df = load_voting()
        col4.metric("Total Votes", len(voting_df))
        
        pantheon_count = 0
        for _, row in st.session_state.catalog.iterrows():
            stats = get_vote_stats(row['Title'], row['Version'])
            if stats['approval'] >= 94:
                pantheon_count += 1
        col5.metric("Pantheon Versions", pantheon_count)
        
        st.divider()
        
        # Key metrics explanation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Triangulation Density")
            st.markdown(f"**Current:** {triangulation_density:.1f}x")
            st.markdown("**Target:** 5-7x")
            
            if triangulation_density < 3:
                st.warning("⚠️ Low density - add more versions per song")
            elif triangulation_density < 5:
                st.info("📊 Good start - aim for 5-7x for optimal triangulation")
            else:
                st.success("✅ Excellent density - full triangulation achieved!")
        
        with col2:
            st.markdown("### Pantheon Achievement Rate")
            pantheon_rate = (pantheon_count / total_versions * 100) if total_versions > 0 else 0
            st.markdown(f"**Current:** {pantheon_rate:.1f}%")
            st.markdown("**Sweet Spot:** 20-30%")
            
            if pantheon_rate < 10:
                st.info("📊 Early stage - continue voting to identify excellence")
            elif pantheon_rate < 40:
                st.success("✅ Healthy Pantheon rate")
            else:
                st.warning("⚠️ High Pantheon rate - consider raising standards")
        
        st.divider()
        
        # Voting leaderboard
        st.markdown("### 🏆 Top Voted Versions")
        
        if not voting_df.empty:
            vote_summary = []
            for _, song in st.session_state.catalog.iterrows():
                stats = get_vote_stats(song['Title'], song['Version'])
                if stats['total'] > 0:
                    status, _ = get_pantheon_status(stats['approval'])
                    vote_summary.append({
                        'Song': song['Title'],
                        'Version': song['Version'],
                        'Status': status,
                        'Votes': stats['total'],
                        'Approval': f"{stats['approval']:.0f}%",
                        'Score': song['Score']
                    })
            
            if vote_summary:
                leaderboard = pd.DataFrame(vote_summary).sort_values('Votes', ascending=False).head(10)
                st.dataframe(leaderboard, use_container_width=True, hide_index=True)
        else:
            st.info("No votes cast yet. Visit the Voting tab to start!")
        
        st.divider()
        
        # Song-level triangulation report
        st.markdown("### 📊 Triangulation Coverage")
        
        triangulation_report = []
        for song_title in st.session_state.catalog['Title'].unique():
            versions = get_all_versions(song_title)
            version_count = len(versions)
            avg_score = versions['Score'].mean()
            
            votes = 0
            pantheon = 0
            for _, v in versions.iterrows():
                stats = get_vote_stats(song_title, v['Version'])
                votes += stats['total']
                if stats['approval'] >= 94:
                    pantheon += 1
            
            triangulation_report.append({
                'Song': song_title,
                'Versions': version_count,
                'Avg Score': f"{avg_score:.2f}",
                'Votes': votes,
                'Pantheon': pantheon,
                'Status': '✅ Full' if version_count >= 5 else '📊 Growing' if version_count >= 3 else '⚠️ Needs More'
            })
        
        report_df = pd.DataFrame(triangulation_report).sort_values('Versions', ascending=False)
        st.dataframe(report_df, use_container_width=True, hide_index=True)

# --- TAB 9: EXPORT TOOLS ---
with tab9:
    st.subheader("📤 Export Tools")
    st.markdown("Export your catalog data for backup, analysis, or external tools (like Gemini)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Available Exports")
        
        export_options = st.multiselect("Select data to export:", [
            "Full Catalog (all versions)",
            "Songs Master (metadata)",
            "Voting Data",
            "Personal Albums",
            "Reviews",
            "Album Agents Config",
            "Video Projects",
            "Complete Archive (all files)"
        ], default=["Full Catalog (all versions)"])
        
        format_option = st.radio("Export Format:", ["CSV", "JSON", "Markdown"])
    
    with col2:
        st.markdown("### Export Purpose")
        
        purpose = st.selectbox("Export for:", [
            "Gemini Analysis",
            "Backup",
            "External Tools",
            "Spreadsheet Analysis",
            "Documentation",
            "Other"
        ])
        
        if purpose == "Gemini Analysis":
            st.info("💡 Gemini exports include rich context and formatting optimized for AI analysis")
    
    st.divider()
    
    if st.button("📥 Generate Export", type="primary"):
        st.markdown("### Generated Export")
        
        export_data = []
        
        if "Full Catalog (all versions)" in export_options:
            st.markdown("#### Full Catalog")
            st.dataframe(st.session_state.catalog, use_container_width=True)
            export_data.append(("catalog.csv", st.session_state.catalog))
        
        if "Songs Master (metadata)" in export_options:
            st.markdown("#### Songs Master")
            st.dataframe(st.session_state.songs_master, use_container_width=True)
            export_data.append(("songs_master.csv", st.session_state.songs_master))
        
        if "Voting Data" in export_options:
            voting_df = load_voting()
            st.markdown("#### Voting Data")
            st.dataframe(voting_df, use_container_width=True)
            export_data.append(("voting.csv", voting_df))
        
        if "Reviews" in export_options:
            reviews_df = load_reviews()
            st.markdown("#### Reviews")
            st.dataframe(reviews_df, use_container_width=True)
            export_data.append(("song_reviews.csv", reviews_df))
        
        if "Video Projects" in export_options:
            video_proj = load_video_projects()
            st.markdown("#### Video Projects")
            st.json(video_proj)
        
        st.success("✅ Export generated! Data displayed above.")
        st.info("💡 In production, this would generate downloadable files. For now, you can copy data from the tables above or access the CSV files directly from your FiatMusica folder.")

# --- TAB 10: SETTINGS ---
with tab10:
    st.subheader("⚙️ Settings")
    
    settings_tab1, settings_tab2, settings_tab3 = st.tabs([
        "🎵 Disc Configuration",
        "👤 User Settings",
        "🔧 System Settings"
    ])
    
    with settings_tab1:
        st.markdown("### Disc Names")
        st.caption("Customize your 10-disc album names")
        
        new_discs = []
        for i in range(10):
            current = st.session_state.settings['discs'][i] if i < len(st.session_state.settings['discs']) else f"Disc {i+1}"
            new_name = st.text_input(f"Disc {i+1}", value=current, key=f"disc_{i}")
            new_discs.append(new_name)
        
        st.divider()
        
        st.markdown("### Era Names")
        st.caption("Customize your era labels")
        
        new_eras = []
        for i in range(9):
            current = st.session_state.settings['eras'][i] if i < len(st.session_state.settings['eras']) else f"Era {i+1}"
            new_era = st.text_input(f"Era {i+1}", value=current, key=f"era_{i}")
            new_eras.append(new_era)
        
        if st.button("💾 Save Disc & Era Settings", type="primary"):
            st.session_state.settings['discs'] = new_discs
            st.session_state.settings['eras'] = new_eras
            save_settings(st.session_state.settings)
            st.success("Settings saved!")
            st.rerun()
    
    with settings_tab2:
        st.markdown("### User Profile")
        
        user_name = st.text_input("Display Name", value=st.session_state.current_user)
        user_type = st.selectbox("User Type", ["Founding Member", "Regular User", "Artist", "Admin"])
        
        st.markdown("### Vote Weight")
        if user_type == "Founding Member":
            st.info("🌟 As a Founding Member, your votes count 10x")
            vote_weight = 10
        else:
            st.info("Your votes count 1x")
            vote_weight = 1
        
        st.session_state.user_weight = vote_weight
        
        if st.button("💾 Save User Settings"):
            st.session_state.current_user = user_name
            st.success("User settings saved!")
    
    with settings_tab3:
        st.markdown("### System Information")
        
        st.markdown(f"**Version:** 6.3 Complete Edition")
        st.markdown(f"**Database:** CSV-based")
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider()
        
        st.markdown("### Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Reload All Data"):
                st.session_state.catalog = load_data()
                st.session_state.songs_master = load_songs_master()
                st.session_state.voting = load_voting()
                st.session_state.personal_albums = load_personal_albums()
                st.session_state.video_projects = load_video_projects()
                st.success("All data reloaded!")
                st.rerun()
        
        with col2:
            if st.button("📊 Show File Stats"):
                st.markdown("**File Sizes:**")
                files = [CSV_FILE, SONGS_MASTER_FILE, VOTING_FILE, PERSONAL_ALBUMS_FILE, REVIEWS_FILE, VIDEO_PROJECTS_FILE]
                for f in files:
                    if os.path.exists(f):
                        size = os.path.getsize(f)
                        st.caption(f"{f}: {size:,} bytes")
        
        st.divider()
        
        st.markdown("### Backup & Restore")
        st.caption("Automatic backups are created before each save. Last 5 backups are kept.")
        
        if os.path.exists('.'):
            backups = [f for f in os.listdir('.') if f.startswith('catalog_backup_')]
            if backups:
                st.markdown(f"**Available Backups:** {len(backups)}")
                latest = sorted(backups)[-1] if backups else None
                if latest:
                    st.caption(f"Latest: {latest}")

# --- FOOTER ---
st.divider()

# Footer stats
col1, col2, col3, col4 = st.columns(4)
col1.metric("Songs", st.session_state.catalog['Title'].nunique() if not st.session_state.catalog.empty else 0)
col2.metric("Versions", len(st.session_state.catalog) if not st.session_state.catalog.empty else 0)

voting_df = load_voting()
col3.metric("Votes", len(voting_df))

pantheon_count = 0
for _, row in st.session_state.catalog.iterrows():
    stats = get_vote_stats(row['Title'], row['Version'])
    if stats['approval'] >= 94:
        pantheon_count += 1
col4.metric("Pantheon", pantheon_count)

st.caption(f"Fiat Musica v6.3 Complete Edition - The Triangulation Platform | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")