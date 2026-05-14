# 🎬 Movie Recommendation System

> **A smart, content-based movie recommendation engine powered by TF-IDF vectorization, cosine similarity, and fuzzy matching. Find your next favorite movie instantly!**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://aminmovierecommendation.streamlit.app/)

**Live Demo:** https://aminmovierecommendation.streamlit.app/

---

## 📊 Project Overview

This project is a **production-ready recommendation system** that analyzes 45,000+ movies and suggests content you'll love based on text similarity. Whether you're searching for movies like "Titanic" or accidentally type "avtar", our intelligent system finds exactly what you need.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎯 **Content-Based Filtering** | Analyzes movie text (overview, genres, tagline) to find similar films |
| 🔍 **Fuzzy Matching** | Handles typos and misspellings intelligently (e.g., "avtar" → "Avatar") |
| 📈 **TF-IDF Vectorization** | Advanced text analysis with 50,000 features and bigrams |
| ⭐ **Similarity Scoring** | Shows 0-100% similarity scores to explain recommendations |
| 🎨 **Beautiful Web UI** | Interactive Streamlit interface with movie posters from TMDB |
| 🌐 **Live Deployment** | Free cloud hosting on Streamlit Cloud |
| 📱 **Responsive Design** | Works on desktop, tablet, and mobile devices |
| 🚀 **Fast Processing** | Returns recommendations in <1 second |
| 🎬 **Movie Metadata** | Displays IMDb ratings, popularity, release dates, and plot summaries |
| 🔒 **Secure API Keys** | Safe credential management via Streamlit Secrets |


---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER INTERFACE                        │
│                  (Streamlit Web App)                     │
│  https://aminmovierecommendation.streamlit.app/         │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │ Fuzzy Matching  │
        │ (70% threshold) │
        └────────┬────────┘
                 │
        ┌────────▼──────────────┐
        │ Load Pre-trained      │
        │ Models from Pickle    │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │ Cosine Similarity     │
        │ Computation           │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │ Rank & Filter         │
        │ Top N Results         │
        └────────┬──────────────┘
                 │
        ┌────────▼──────────────┐
        │ Fetch TMDB Details    │
        │ (Posters, ratings)    │
        └────────┬──────────────┘
                 │
┌────────────────▼────────────────────────────────────────┐
│                   RESULTS DISPLAY                        │
│         Movies with posters, scores, ratings             │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Live Demo

### **Visit:** https://aminmovierecommendation.streamlit.app/

**Try these searches:**
- "Avatar" → Get sci-fi recommendations
- "Titanic" → Get historical drama recommendations  
- "avtar" → See fuzzy matching in action!
- "toy story" → Get family-friendly recommendations

---

## 🎯 How It Works (In Detail)

### **1. Data Collection & Cleaning**
```
Raw Data (45,450 movies)
  ↓
Remove Duplicates & Nulls
  ↓
Select Key Columns:
  • title, overview, genres
  • tagline, vote_average, popularity
  ↓
Clean Dataset (45,460 ready)
```

### **2. Feature Engineering**
Combine: `overview + genres + tagline = "tags"`

### **3. Text Preprocessing**
- Lowercase conversion
- Remove punctuation & special characters
- Remove stopwords (common words)
- Lemmatization (reduce to root form)

### **4. TF-IDF Vectorization**
Convert processed text → 50,000-dimensional vectors
Each number = importance score for a word/phrase

### **5. Cosine Similarity**
Calculate similarity between query movie & all 45,460 movies
Return top N ranked by similarity (0.0-1.0 scale)

### **6. Fuzzy Matching**
If exact title match fails, find closest match using Levenshtein Distance
(70% threshold)


---

## 📈 Key Metrics

| Metric | Value |
|--------|-------|
| **Total Movies** | 45,460 |
| **Feature Dimensions** | 50,000 (TF-IDF) |
| **Similarity Range** | 0.0 - 1.0 |
| **Fuzzy Match Threshold** | 70% |
| **Response Time** | <1 second |

---

## 💻 Installation & Setup

### **Option 1: Use the Live Demo (No Installation!)**
Just visit: https://aminmovierecommendation.streamlit.app/

### **Option 2: Run Locally**

**Prerequisites:**
- Python 3.10+
- TMDB API Key (free at https://www.themoviedb.org/settings/api)

**Steps:**

1. Clone repository:
```bash
git clone https://github.com/yourusername/MoviesRecommendation.git
cd MoviesRecommendation
```

2. Create environment:
```bash
conda create -n movieapp python=3.10
conda activate movieapp
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure API key:
```bash
cp .env.example .env
# Edit .env and add your TMDB API key
```

5. Run the app:
```bash
streamlit run app.py
```

Visit: http://localhost:8501

---

## 🎮 Usage Guide

### **Web Interface (Easiest)**

**Live at:** https://aminmovierecommendation.streamlit.app/

**Steps:**
1. Enter a movie title
2. Adjust number of recommendations (3-20)
3. Click "🔍 Search"
4. View results with posters, scores, and ratings

### **Jupyter Notebook**

Run `movies.ipynb` for full ML code:

```python
# Basic recommendation
recommend('Titanic', 5)

# With similarity scores
recommend_with_scores('Avatar', 10)

# Handles typos
recommend('avtar', 5)  # → Finds "Avatar"
```
