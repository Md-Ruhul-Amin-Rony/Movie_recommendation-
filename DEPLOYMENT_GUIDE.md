# 🚀 Deploy to Streamlit Cloud (FREE)

## **Step-by-Step Deployment Guide**

### **Step 1: Push Your Project to GitHub**

Make sure all files are committed and pushed:
```bash
git add .
git commit -m "Add Streamlit UI and deployment files"
git push origin main
```

**Ensure these files are in your repo:**
- ✅ `app.py` (Streamlit UI)
- ✅ `requirements.txt` (Dependencies)
- ✅ `.env.example` (Template)
- ✅ `.streamlit/config.toml` (Configuration)
- ✅ `df.pkl`, `tfidf.pkl`, `tfidf_matrix.pkl` (Model files)

---

### **Step 2: Create Streamlit Cloud Account**

1. Go to **[share.streamlit.io](https://share.streamlit.io)**
2. Click "Sign Up" → Use GitHub to authenticate
3. Authorize Streamlit to access your GitHub repositories

---

### **Step 3: Deploy Your App**

1. Click "Create app"
2. Select:
   - **Repository:** `MoviesRecommendation` (your repo)
   - **Branch:** `main` (or your default branch)
   - **Main file path:** `app.py`
3. Click "Deploy"

**That's it! 🎉** Your app will be live in 1-2 minutes.

---

### **Step 4: Add Secrets (API Key)**

Since `.env` files aren't committed to GitHub for security:

1. In Streamlit Cloud dashboard, click on your app
2. Go to **Settings** → **Secrets**
3. Add your TMDB API key:
   ```
   TMDB_API_KEY = "your_actual_api_key_here"
   ```
4. The app automatically reads from this secret

---

## **Pre-Deployment Checklist**

- [ ] All files pushed to GitHub
- [ ] `requirements.txt` has all dependencies
- [ ] `.env` is in `.gitignore` (not committed)
- [ ] API key will be added via Streamlit Secrets
- [ ] Model files (`.pkl`) are in repo
- [ ] `.streamlit/config.toml` is configured

---

## **Troubleshooting**

### **Problem: "Module not found" errors**
- **Solution:** Update `requirements.txt` with all dependencies
- Run: `pip freeze > requirements.txt`

### **Problem: API key not working**
- **Solution:** Add TMDB_API_KEY to Streamlit Secrets (see Step 4)

### **Problem: Model files too large**
- **Solution:** Streamlit Cloud has a 1GB limit. If models exceed this:
  - Use GitHub LFS (Large File Storage)
  - Or download models on first run from a cloud storage

### **Problem: App loads but recommendations fail**
- **Solution:** Check Streamlit logs in the app's "Manage app" panel
- Verify API key is correct in Secrets

---

## **After Deployment**

Your app will be live at:
```
https://[your-username]-movierecommendation-[random-id].streamlit.app
```

**Share the link!** Anyone can access it.

---

## **Free Tier Limits**

- ✅ Unlimited apps
- ✅ 1GB storage per app
- ✅ 1 vCPU, 2GB RAM
- ✅ Always available (no sleeping)
- ⚠️ Limited compute for heavy operations

**Sufficient for:** Small-medium traffic, data exploration, demos

---

## **Optional: Custom Domain**

Upgrade to Pro ($5/month) to use a custom domain like `recommendations.yoursite.com`

---

## **Next Steps (Advanced)**

After basic deployment, you can:
- Add a REST API (FastAPI) alongside Streamlit
- Use GitHub Actions for automated deployments
- Monitor app performance with Streamlit Community Cloud analytics
- Scale to production (AWS, Google Cloud) if needed

---

**Your app is ready for production! 🚀**
