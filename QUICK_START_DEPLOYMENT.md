# ⚡ Quick Start - Render Deployment (5 Minutes)

## 🎯 Fast Track Deployment

### Prerequisites:
- ✅ All project files ready
- ✅ GitHub account
- ✅ Render account (sign up at render.com - FREE)

---

## 📤 STEP 1: Push to GitHub (2 minutes)

```bash
# In your project directory
git init
git add .
git commit -m "Ready for Render deployment"
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

---

## 🔵 STEP 2: Deploy Backend (2 minutes)

1. Go to [render.com](https://render.com) → Sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Settings:
   - **Name:** `finops-backend`
   - **Root Directory:** `backend`
   - **Build:** `pip install -r requirements.txt`
   - **Start:** `gunicorn app:app --bind 0.0.0.0:$PORT`
5. Click **"Create Web Service"**
6. **WAIT** for deployment (5-10 min)
7. **COPY** the URL (e.g., `https://finops-backend.onrender.com`)

---

## 🟢 STEP 3: Deploy Frontend (1 minute)

1. In Render, click **"New +"** → **"Static Site"**
2. Connect same repository
3. Settings:
   - **Name:** `finops-frontend`
   - **Root Directory:** `frontend`
   - **Build:** `npm install && npm run build`
   - **Publish:** `build`
4. **Add Environment Variable:**
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://finops-backend.onrender.com/api` (use YOUR backend URL)
5. Click **"Create Static Site"**
6. **WAIT** for deployment (5-10 min)
7. **DONE!** Your app is live! 🎉

---

## ✅ Verify

- Backend: `https://finops-backend.onrender.com/api/health` → Should show `{"status":"ok"}`
- Frontend: `https://finops-frontend.onrender.com` → Should show dashboard

---

## 🐛 If Frontend Can't Connect

Update `backend/app.py` line 13:
```python
CORS(app, resources={r"/api/*": {"origins": ["https://finops-frontend.onrender.com"]}})
```

Then push to GitHub - Render auto-deploys!

---

**That's it! Your app is deployed! 🚀**

