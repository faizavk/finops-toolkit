# Free Deployment Guide for FinOps Toolkit

## 🆓 Best Free Deployment Options

### Option 1: Render (Recommended - Easiest) ⭐

**Why Render?**
- ✅ Free tier available
- ✅ Automatic deployments from GitHub
- ✅ Supports both Python (Flask) and React
- ✅ Free SSL certificates
- ✅ Easy setup

**Steps:**
1. Push your code to GitHub
2. Create account at [render.com](https://render.com)
3. Create two services:
   - **Web Service** (Backend - Flask)
   - **Static Site** (Frontend - React)

**Free Tier Limits:**
- 750 hours/month (enough for 24/7)
- Auto-sleeps after 15 min inactivity (wakes on request)
- 100 GB bandwidth/month

**Cost:** FREE (with limitations)

---

### Option 2: Vercel (Frontend) + Railway (Backend)

**Vercel (Frontend):**
- ✅ Free tier
- ✅ Automatic deployments
- ✅ Great for React apps
- ✅ Free SSL

**Railway (Backend):**
- ✅ $5 free credit/month (enough for small apps)
- ✅ Easy Flask deployment
- ✅ Auto-deploy from GitHub

**Cost:** FREE (Railway gives $5/month credit)

---

### Option 3: Netlify (Frontend) + PythonAnywhere (Backend)

**Netlify (Frontend):**
- ✅ Free tier
- ✅ React support
- ✅ Continuous deployment

**PythonAnywhere (Backend):**
- ✅ Free tier available
- ✅ Flask support
- ✅ Limited to 1 web app on free tier

**Cost:** FREE

---

### Option 4: Fly.io (Both Backend & Frontend)

**Why Fly.io?**
- ✅ Free tier (3 shared VMs)
- ✅ Supports both Python and Node.js
- ✅ Global edge network
- ✅ Docker-based deployment

**Free Tier:**
- 3 shared VMs
- 160 GB outbound data transfer
- 3 GB persistent storage

**Cost:** FREE (with limits)

---

### Option 5: Heroku (Both - Limited Free Tier)

**Note:** Heroku removed free tier in 2022, but has low-cost options ($5/month)

**Alternatives:**
- **Render** (better free option)
- **Fly.io** (better free option)

---

## 🏠 Local Deployment (Your Computer)

If you want to keep it running locally on your machine:

### Option A: Keep Running in Terminal
- Just run both servers (backend + frontend)
- Access via `localhost:3000`
- **Free:** ✅ Yes
- **Limitation:** Only accessible on your computer

### Option B: Make it Accessible on Local Network
1. Find your local IP: `ifconfig` (Mac/Linux) or `ipconfig` (Windows)
2. Update frontend API URL to use your IP
3. Access from other devices on same network
- **Free:** ✅ Yes
- **Limitation:** Only works on local network

---

## 🚀 Recommended: Render Deployment (Step-by-Step)

### Prerequisites:
1. GitHub account
2. Code pushed to GitHub repository

### Step 1: Prepare Your Code

#### Backend Setup:
Create `backend/Procfile`:
```
web: gunicorn app:app
```

Create `backend/runtime.txt`:
```
python-3.10.6
```

Ensure `backend/requirements.txt` includes all dependencies:
```
flask==3.0.0
flask-cors==4.0.0
pandas==2.1.4
numpy==1.26.2
prophet==1.1.5
python-dateutil==2.8.2
gunicorn==21.2.0          # Production server
flask-limiter==3.5.0      # Rate limiting
marshmallow==3.20.1       # Input validation
python-dotenv==1.0.0      # Environment variables
```

**Note:** The code includes fallbacks for security packages, so it will work even if some packages fail to install. However, for full security features, all dependencies should be installed.

#### Frontend Setup:
Build the React app:
```bash
cd frontend
npm run build
```

### Step 2: Deploy Backend to Render

1. Go to [render.com](https://render.com)
2. Sign up (free)
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name:** finops-backend
   - **Environment:** Python 3
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Root Directory:** `backend`
6. Add Environment Variables (if needed)
7. Click "Create Web Service"
8. Copy the URL (e.g., `https://finops-backend.onrender.com`)

### Step 3: Deploy Frontend to Render

1. In Render dashboard, click "New +" → "Static Site"
2. Connect same GitHub repository
3. Configure:
   - **Name:** finops-frontend
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Publish Directory:** `frontend/build`
4. Add Environment Variable:
   - `REACT_APP_API_URL` = Your backend URL from Step 2
5. Update `frontend/src/components/Dashboard.js`:
   ```javascript
   const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';
   ```
6. Click "Create Static Site"
7. Your app will be live!

---

## 📋 Quick Comparison Table

| Platform | Backend | Frontend | Free Tier | Ease of Use | Best For |
|----------|---------|----------|-----------|-------------|----------|
| **Render** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ | Best overall |
| **Vercel** | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ | Frontend only |
| **Railway** | ✅ | ❌ | ✅ ($5 credit) | ⭐⭐⭐⭐ | Backend |
| **Fly.io** | ✅ | ✅ | ✅ | ⭐⭐⭐ | Both services |
| **Netlify** | ❌ | ✅ | ✅ | ⭐⭐⭐⭐⭐ | Frontend only |
| **PythonAnywhere** | ✅ | ❌ | ✅ | ⭐⭐⭐ | Backend only |
| **Local** | ✅ | ✅ | ✅ | ⭐⭐⭐⭐⭐ | Development |

---

## 🎯 My Recommendation

**For Free Deployment: Use Render**

**Why?**
1. ✅ Free tier is generous
2. ✅ Supports both backend and frontend
3. ✅ Easy GitHub integration
4. ✅ Automatic SSL
5. ✅ Simple setup process

**Steps Summary:**
1. Push code to GitHub
2. Deploy backend as Web Service on Render
3. Deploy frontend as Static Site on Render
4. Update frontend API URL
5. Done! 🎉

---

## 🔧 Deployment Checklist

### Before Deploying:
- [ ] Code pushed to GitHub
- [ ] All dependencies in requirements.txt/package.json (including security packages)
- [ ] Environment variables configured (API keys, CORS, etc.)
- [ ] Security features tested (rate limiting, validation)
- [ ] Environment variables documented
- [ ] CORS configured for production URL
- [ ] Frontend built successfully (`npm run build`)
- [ ] Backend tested locally

### After Deploying:
- [ ] Backend health check works
- [ ] Frontend loads correctly
- [ ] API calls work from frontend
- [ ] Charts render properly
- [ ] All features functional

---

## 💡 Pro Tips

1. **Use Environment Variables** for API URLs
2. **Enable CORS** for your production domain
3. **Test locally first** before deploying
4. **Monitor logs** in Render dashboard
5. **Set up auto-deploy** from GitHub

---

## 🆘 Troubleshooting

### Backend Issues:
- Check Render logs
- Verify PORT environment variable
- Ensure all dependencies are in requirements.txt (including gunicorn, flask-limiter, marshmallow, python-dotenv)
- Configure environment variables for production (API keys, CORS origins)
- Test security features after deployment

### Frontend Issues:
- Check build logs
- Verify API URL environment variable
- Ensure CORS allows your frontend domain

### CORS Errors:
- Update `backend/app.py` CORS settings:
  ```python
  CORS(app, resources={r"/api/*": {"origins": ["https://your-frontend.onrender.com"]}})
  ```

---

## 📞 Need Help?

- Render Docs: https://render.com/docs
- Vercel Docs: https://vercel.com/docs
- Fly.io Docs: https://fly.io/docs

---

**Recommended:** Start with **Render** - it's the easiest and most reliable free option! 🚀

