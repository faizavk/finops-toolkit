# 🔧 Troubleshooting Guide

## ✅ Backend is Running
The backend server is running on `http://localhost:5000` and responding correctly.

## ✅ Frontend is Running  
The frontend React app is running on `http://localhost:3000`.

## 🔍 How to Check What's Wrong

### Step 1: Check Browser Console
1. Open your browser: `http://localhost:3000`
2. Press `F12` or `Cmd+Option+I` (Mac) to open Developer Tools
3. Click on the **Console** tab
4. Try clicking "Load Forecast" button
5. Look for any **red error messages** in the console
6. **Copy and share those error messages** - they will tell us exactly what's wrong

### Step 2: Check Network Tab
1. In Developer Tools, click the **Network** tab
2. Try clicking "Load Forecast" button
3. Look for requests to `http://localhost:5000/api/forecast`
4. Click on that request
5. Check:
   - **Status Code**: Should be 200 (green) or 401/400/500 (red)
   - **Response**: What does it say?
   - **Headers**: Any CORS errors?

### Step 3: Test Backend Directly
Open a new terminal and run:
```bash
curl http://localhost:5000/api/historical
```

If this works, the backend is fine. If it fails, the backend has an issue.

---

## 🚨 Common Issues & Fixes

### Issue 1: "Cannot connect to backend"
**Fix**: Make sure backend is running:
```bash
cd backend
source venv/bin/activate
python app.py
```

### Issue 2: CORS Error
**Fix**: Backend CORS is configured. If you see CORS errors, check:
- Backend is running on port 5000
- Frontend is running on port 3000
- No firewall blocking connections

### Issue 3: 401 Unauthorized
**Fix**: API key authentication is disabled by default. If you see 401:
- Check `backend/.env` file - set `REQUIRE_API_KEY=false`
- Or restart backend without `.env` file

### Issue 4: 500 Server Error
**Fix**: Check backend terminal for error messages. Common causes:
- Missing data file (`ideal_cost_data.csv`)
- Prophet model errors (fallback should handle this)
- Import errors

---

## 📋 Quick Checklist

- [ ] Backend running on port 5000? (`curl http://localhost:5000/api/health`)
- [ ] Frontend running on port 3000? (Browser shows React app)
- [ ] Data file exists? (`ls backend/../ideal_cost_data.csv`)
- [ ] No errors in backend terminal?
- [ ] Browser console shows what error?

---

## 🆘 Still Not Working?

**Please share:**
1. Error message from browser console (F12 → Console tab)
2. Error message from backend terminal
3. Network request details (F12 → Network tab → click failed request)

This will help me fix it quickly!

