# 🎬 Movie Recommendation System - Setup & Running Guide

## Prerequisites
- Python 3.8+
- Conda or pip package manager
- TMDB API Key (free account at https://www.themoviedb.org/settings/api)

## Installation & Setup

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

Or if you're using conda:
```bash
conda create -n movies-app python=3.10
conda activate movies-app
pip install -r requirements.txt
```

### Step 2: Configure API Key
1. Get your free TMDB API key from: https://www.themoviedb.org/settings/api
2. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env` and replace `your_api_key_here` with your actual API key:
   ```
   TMDB_API_KEY=your_actual_api_key_here
   ```

### Step 3: Verify Model Files
Ensure these files exist in the project directory:
- `tfidf_matrix.pkl` - Pre-computed TF-IDF matrix
- `indices.pkl` - Movie title to index mapping
- `df.pkl` - Processed DataFrame with movie data
- `tfidf.pkl` - TF-IDF vectorizer

These should already be present from the notebook execution.

## Running the Application

### Option 1: Run with Streamlit (Recommended)
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

### Option 2: Run with Conda Environment
```bash
# First time setup
conda create -n movieapp python=3.10
conda activate movieapp
pip install -r requirements.txt

# Running
streamlit run app.py
```

## How to Use the App

### 1. **Search for a Movie**
   - Enter a movie title in the search box (e.g., "Avatar", "Titanic", "Toy Story")
   - The system has fuzzy matching, so typos are handled (e.g., "avtar" → "Avatar")
   - Click the 🔍 Search button

### 2. **Get Recommendations**
   - Adjust the number of recommendations using the slider (3-20 movies)
   - View the original movie's poster and details
   - See the top N similar movies with:
     - Movie poster from TMDB
     - Similarity score (0-100%)
     - IMDb rating
     - Popularity score
     - Plot overview

### 3. **Explore Dataset**
   - Switch to the "📚 About Dataset" tab
   - View dataset statistics and sample movies
   - Understand available data

## Features

### 🤖 Machine Learning
- **TF-IDF Vectorization** - Converts movie metadata into numerical vectors
- **Cosine Similarity** - Measures similarity between movies (0-1 scale)
- **Fuzzy Matching** - Handles typos and misspellings (70% threshold)

### 🎨 User Interface
- Clean, responsive Streamlit interface
- Movie posters from TMDB API
- Multiple recommendation views
- Dataset statistics and exploration
- Easy navigation with tabs

### 📊 Data
- 40,000+ movies from TMDB
- Movie metadata: title, overview, genres, tagline, ratings, popularity
- Preprocessed text with stopword removal and lemmatization

## Troubleshooting

### Error: "Failed to load models"
- Ensure all `.pkl` files are present in the project directory
- Run the `movies.ipynb` notebook to regenerate pickle files if needed

### Error: "TMDB_API_KEY not found"
- Check that `.env` file exists in the project root
- Ensure you have a valid TMDB API key in `.env`
- Verify the `.env` file format matches `.env.example`

### Error: "Movie not found"
- The movie might not be in the dataset (40,000+ movies)
- Try a different movie or check spelling
- The fuzzy matcher should handle minor typos

### Slow API Responses
- TMDB API might have rate limits
- Try again after a few seconds
- This is normal during high traffic

## Project Structure

```
MoviesRecommendation/
├── app.py                    # Main Streamlit application
├── movies.ipynb              # Jupyter notebook with model training
├── movies_metadata.csv       # Original dataset (40,000+ movies)
├── requirements.txt          # Python dependencies
├── .env                      # API keys (NOT in git)
├── .env.example              # Template for .env
├── .gitignore               # Git ignore file
├── README.md                # Project documentation
├── tfidf_matrix.pkl         # Serialized TF-IDF matrix
├── indices.pkl              # Movie index mapping
├── df.pkl                   # Processed DataFrame
└── tfidf.pkl                # TF-IDF vectorizer
```

## API Limits & Notes

- **TMDB API** has rate limits (~40 requests/10 seconds for free tier)
- Movie posters may not be available for all movies
- The recommendation model uses preprocessed text from overview, genres, and tagline

## Future Enhancements

- [ ] Add collaborative filtering recommendations
- [ ] User rating history and personalized recommendations
- [ ] Filter recommendations by genre, rating, year
- [ ] Add movie reviews and social features
- [ ] Deploy to cloud (Heroku, AWS, Google Cloud)
- [ ] Add watch list / favorites feature
- [ ] Dark mode theme

## Support

For issues or improvements:
1. Check the troubleshooting section above
2. Verify all files are present
3. Ensure API key is valid
4. Check internet connection for TMDB API calls

---

**Last Updated:** May 2026  
**Model:** Content-Based Recommendation with TF-IDF & Cosine Similarity
