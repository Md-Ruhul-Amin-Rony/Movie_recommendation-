import streamlit as st
import pickle
import joblib
import pandas as pd
import numpy as np
import requests
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    .movie-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .similarity-score {
        font-weight: bold;
        color: #FF6B6B;
    }
    </style>
""", unsafe_allow_html=True)

# Load pre-trained models and data
@st.cache_resource
def load_models():
    try:
        import warnings
        warnings.filterwarnings('ignore')
        
        # Try to load with joblib first (more compatible)
        try:
            tfidf_matrix = joblib.load('tfidf_matrix.pkl')
            df = joblib.load('df.pkl')
            tfidf = joblib.load('tfidf.pkl')
            
            # Recreate indices from dataframe
            indices = pd.Series(df.index, index=df['title']).drop_duplicates()
        except:
            # Fallback: try with pickle
            with open('tfidf_matrix.pkl', 'rb') as f:
                tfidf_matrix = pickle.load(f)
            with open('df.pkl', 'rb') as f:
                df = pickle.load(f)
            with open('tfidf.pkl', 'rb') as f:
                tfidf = pickle.load(f)
            
            # Recreate indices from dataframe
            indices = pd.Series(df.index, index=df['title']).drop_duplicates()
        
        return tfidf_matrix, indices, df, tfidf
    except Exception as e:
        import traceback
        error_msg = f"Error loading models: {str(e)}\n{traceback.format_exc()}"
        st.error(error_msg)
        return None, None, None, None

# Fetch movie details from TMDB
def get_movie_details(movie_title):
    """Fetch movie details from TMDB API"""
    try:
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'page': 1
        }
        response = requests.get(search_url, params=params, timeout=5)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            if results:
                movie = results[0]
                return {
                    'title': movie.get('title', movie_title),
                    'poster_path': movie.get('poster_path'),
                    'overview': movie.get('overview', 'No overview available'),
                    'release_date': movie.get('release_date', 'N/A'),
                    'rating': movie.get('vote_average', 'N/A'),
                    'popularity': movie.get('popularity', 'N/A'),
                    'tmdb_id': movie.get('id')
                }
    except Exception as e:
        st.warning(f"Could not fetch details for {movie_title}: {str(e)}")
    
    return None

# Recommendation function
def recommend(title, n=10, tfidf_matrix=None, indices=None, df=None):
    """
    Recommend similar movies based on TF-IDF and cosine similarity
    """
    if title not in indices.index:
        # Find closest match using fuzzy matching
        closest_match = None
        highest_score = 0
        
        for movie_title in indices.index:
            score = fuzz.token_sort_ratio(title.lower(), movie_title.lower())
            if score > highest_score:
                highest_score = score
                closest_match = movie_title
        
        if closest_match and highest_score > 70:
            title = closest_match
        else:
            return None, f"Movie '{title}' not found in database"
    
    # Get the index of the movie
    idx_result = indices[title]
    if isinstance(idx_result, pd.Series):
        idx = int(idx_result.iloc[0])
    else:
        idx = int(idx_result)
    
    # Compute similarity
    sim_score = cosine_similarity(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
    
    # Get top similar movies (skip the first which is the movie itself)
    similar_indices = np.argsort(-sim_score)[1:n+1]
    
    # Filter to ensure indices are within bounds
    valid_indices = [i for i in similar_indices if 0 <= i < len(df)]
    
    if not valid_indices:
        return None, "No similar movies found"
    
    # Create result dataframe with scores
    results = []
    for i in valid_indices:
        try:
            popularity = float(df['popularity'].iloc[i])
        except (ValueError, TypeError):
            popularity = 0.0
        
        try:
            vote_avg = float(df['vote_average'].iloc[i])
        except (ValueError, TypeError):
            vote_avg = 0.0
            
        results.append({
            'Title': df['title'].iloc[i],
            'Similarity Score': round(sim_score[i], 4),
            'Vote Average': vote_avg,
            'Popularity': round(popularity, 2)
        })
    
    return pd.DataFrame(results), None

# Main app
def main():
    # Load models
    tfidf_matrix, indices, df, tfidf = load_models()
    
    if tfidf_matrix is None:
        st.error("Failed to load models. Please ensure all pickle files are present.")
        return
    
    # Header
    col1, col2 = st.columns([1, 4])
    with col1:
        st.markdown("# 🎬")
    with col2:
        st.title("Movie Recommendation System")
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        num_recommendations = st.slider(
            "Number of recommendations",
            min_value=3,
            max_value=20,
            value=10,
            step=1
        )
        
        st.markdown("---")
        st.markdown("""
        ### 📊 About This System
        This recommendation engine uses:
        - **TF-IDF Vectorization** for text analysis
        - **Cosine Similarity** for movie comparison
        - **Fuzzy Matching** for typo tolerance
        - **TMDB API** for movie details
        """)
    
    # Main content with tabs
    tab1, tab2 = st.tabs(["🔍 Get Recommendations", "📚 About Dataset"])
    
    with tab1:
        st.subheader("Find Movies Similar to Your Favorite")
        
        # Search input
        col1, col2 = st.columns([3, 1])
        with col1:
            movie_title = st.text_input(
                "Enter a movie title (e.g., 'Avatar', 'Titanic', 'Toy Story')",
                placeholder="Search for a movie..."
            )
        with col2:
            search_button = st.button("🔍 Search", use_container_width=True)
        
        if search_button and movie_title:
            with st.spinner(f"Finding movies similar to '{movie_title}'..."):
                # Get recommendations
                recommendations_df, error = recommend(
                    movie_title,
                    num_recommendations,
                    tfidf_matrix,
                    indices,
                    df
                )
                
                if error:
                    st.error(f"❌ {error}")
                else:
                    # Display original movie
                    st.markdown("### 🎯 Searching For:")
                    original_movie = recommendations_df.iloc[0]['Title'] if len(recommendations_df) > 0 else movie_title
                    
                    # Try to get original movie details if it's the input
                    search_title = movie_title if movie_title in indices.index else original_movie
                    original_details = get_movie_details(search_title)
                    
                    if original_details and original_details['poster_path']:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.image(
                                f"{TMDB_IMAGE_BASE_URL}{original_details['poster_path']}",
                                width=150
                            )
                        with col2:
                            st.markdown(f"**{original_details['title']}**")
                            st.markdown(f"📅 Release: {original_details['release_date']}")
                            st.markdown(f"⭐ Rating: {original_details['rating']}/10")
                            st.markdown(f"📈 Popularity: {original_details['popularity']}")
                            st.markdown(f"📝 {original_details['overview'][:300]}...")
                    else:
                        st.info(f"Movie: **{search_title}**")
                    
                    # Display recommendations
                    st.markdown("---")
                    st.markdown(f"### 🎁 Top {num_recommendations} Similar Movies")
                    
                    # Display in columns for better visual layout
                    cols = st.columns(2)
                    
                    for idx, row in recommendations_df.iterrows():
                        col = cols[idx % 2]
                        
                        with col:
                            movie_details = get_movie_details(row['Title'])
                            
                            if movie_details and movie_details['poster_path']:
                                # Create card with poster
                                st.markdown(f"""
                                <div class="movie-card">
                                <img src="{TMDB_IMAGE_BASE_URL}{movie_details['poster_path']}" width="100%">
                                </div>
                                """, unsafe_allow_html=True)
                            else:
                                st.markdown(f"""
                                <div class="movie-card">
                                <p style="text-align: center; padding: 50px 10px; background: #ddd; border-radius: 5px;">
                                No poster available
                                </p>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            # Movie info
                            st.markdown(f"**{row['Title']}**")
                            
                            col_metrics = st.columns(3)
                            with col_metrics[0]:
                                st.metric("Similarity", f"{row['Similarity Score']:.1%}")
                            with col_metrics[1]:
                                st.metric("Rating", f"{row['Vote Average']:.1f}/10")
                            with col_metrics[2]:
                                st.metric("Popularity", f"{row['Popularity']:.0f}")
                            
                            if movie_details:
                                st.caption(movie_details['overview'][:150] + "...")
                            
                            st.markdown("---")
    
    with tab2:
        st.subheader("📊 Dataset Information")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Movies", len(df))
        with col2:
            st.metric("Unique Titles", df['title'].nunique())
        with col3:
            st.metric("Avg Rating", f"{df['vote_average'].mean():.2f}")
        with col4:
            st.metric("Total Features", df.shape[1])
        
        st.markdown("---")
        st.markdown("### Available Columns")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - **title** - Movie name
            - **overview** - Plot summary
            - **genres** - Movie categories
            - **tagline** - Short description
            """)
        
        with col2:
            st.markdown("""
            - **vote_average** - IMDb rating
            - **popularity** - Popularity score
            - **tags** - Processed text for ML
            """)
        
        st.markdown("---")
        st.markdown("### Sample Movies")
        st.dataframe(
            df[['title', 'vote_average', 'popularity']].head(10),
            use_container_width=True,
            hide_index=True
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #888; padding: 20px 0;">
    <p>🎬 Movie Recommendation System | Powered by TF-IDF & Cosine Similarity</p>
    <p>Data from TMDB API | Model trained on 40,000+ movies</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
