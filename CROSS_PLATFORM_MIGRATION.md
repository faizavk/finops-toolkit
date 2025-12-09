# 🖥️ Cross-Platform Migration Guide: Mac → Windows

## 📦 Step 1: Prepare Project for Transfer

### Files to INCLUDE in ZIP:
```
fin/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── schemas.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json (if exists)
├── ideal_cost_data.csv (or your dataset)
├── demo_aws_cost_data.csv (if using demo data)
├── generate_demo_dataset.py (optional)
├── outputs/ (empty folder, or with .gitkeep)
└── All .md documentation files
```

### Files to EXCLUDE from ZIP:
```
❌ backend/venv/          # Virtual environment (will recreate)
❌ backend/__pycache__/   # Python cache
❌ backend/logs/          # Log files
❌ backend/.env           # Environment variables (sensitive)
❌ frontend/node_modules/ # Node modules (will reinstall)
❌ frontend/build/        # Build files
❌ .DS_Store              # Mac system files
❌ *.pyc                  # Python bytecode
❌ .git/                  # Git repository (optional)
```

### Quick Command to Create Clean ZIP (Mac):
```bash
cd /Users/summaiya.sarvari/Desktop
zip -r finops-project.zip fin \
  -x "*.DS_Store" \
  -x "*/venv/*" \
  -x "*/node_modules/*" \
  -x "*/__pycache__/*" \
  -x "*/logs/*" \
  -x "*/.env" \
  -x "*/build/*"
```

---

## 🪟 Step 2: Windows Setup Instructions

### Prerequisites to Install on Windows:

1. **Python 3.10.6** (or 3.10.x)
   - Download from: https://www.python.org/downloads/
   - ✅ Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt, type `python --version`

2. **Node.js 20.11.1** (or latest LTS)
   - Download from: https://nodejs.org/
   - Includes npm automatically
   - Verify: `node --version` and `npm --version`

3. **Git** (Optional, for version control)
   - Download from: https://git-scm.com/download/win

---

## 📥 Step 3: Extract and Setup on Windows

### 1. Extract ZIP File
- Extract `finops-project.zip` to a location like:
  - `C:\Users\YourName\Desktop\fin`
  - Or `C:\Projects\fin`

### 2. Open Command Prompt or PowerShell
- Press `Win + R`, type `cmd`, press Enter
- Or use PowerShell (recommended)

### 3. Navigate to Project Directory
```cmd
cd C:\Users\YourName\Desktop\fin
```

---

## 🔵 Step 4: Backend Setup (Windows)

### 1. Navigate to Backend Directory
```cmd
cd backend
```

### 2. Create Virtual Environment
```cmd
python -m venv venv
```

**Note:** If `python` doesn't work, try `python3` or `py`

### 3. Activate Virtual Environment

**In Command Prompt:**
```cmd
venv\Scripts\activate
```

**In PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**If PowerShell gives execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\Activate.ps1
```

**You should see:** `(venv)` at the start of your prompt

### 4. Upgrade Pip (Recommended)
```cmd
python -m pip install --upgrade pip
```

### 5. Install Dependencies
```cmd
pip install -r requirements.txt
```

**This will install:**
- flask, flask-cors, pandas, numpy, prophet, etc.
- Security packages: flask-limiter, marshmallow, python-dotenv
- Production server: gunicorn

**Note:** Prophet installation may take 5-10 minutes. Be patient!

### 6. Create Environment File (Optional)
```cmd
copy .env.example .env
```

Then edit `.env` with Notepad or any text editor:
```
REQUIRE_API_KEY=false
API_KEY_1=dev-key-12345
API_KEY_2=dev-key-67890
FRONTEND_URL=http://localhost:3000
PORT=5000
```

### 7. Verify Data File Exists
Make sure `ideal_cost_data.csv` is in the parent directory:
```cmd
cd ..
dir ideal_cost_data.csv
```

If missing, copy it from the extracted files.

### 8. Test Backend
```cmd
cd backend
python app.py
```

**You should see:**
```
 * Running on http://127.0.0.1:5000
```

**Press `Ctrl + C` to stop**

---

## 🟢 Step 5: Frontend Setup (Windows)

### 1. Open NEW Command Prompt/PowerShell Window
(Keep backend running in the first window)

### 2. Navigate to Frontend Directory
```cmd
cd C:\Users\YourName\Desktop\fin\frontend
```

### 3. Install Dependencies
```cmd
npm install
```

**This will install:**
- react, react-dom, react-scripts
- recharts, axios, react-toastify
- All other frontend dependencies

**Note:** This may take 5-10 minutes on first install.

### 4. Test Frontend
```cmd
npm start
```

**You should see:**
- Browser opens automatically to `http://localhost:3000`
- Or you can manually open it

---

## 🚀 Step 6: Run the Project

### Terminal 1 - Backend:
```cmd
cd C:\Users\YourName\Desktop\fin\backend
venv\Scripts\activate
python app.py
```

### Terminal 2 - Frontend:
```cmd
cd C:\Users\YourName\Desktop\fin\frontend
npm start
```

### Access the Application:
- Open browser: `http://localhost:3000`
- Backend API: `http://localhost:5000`

---

## 🔧 Windows-Specific Differences

### Path Separators:
- **Mac/Linux:** `/` (forward slash)
- **Windows:** `\` (backslash) or `/` (both work in most cases)

### Command Differences:

| Task | Mac/Linux | Windows |
|------|-----------|---------|
| Activate venv | `source venv/bin/activate` | `venv\Scripts\activate` |
| List files | `ls` | `dir` |
| Change directory | `cd` | `cd` (same) |
| Python command | `python3` or `python` | `python` or `py` |
| Stop process | `Ctrl + C` | `Ctrl + C` (same) |

### Environment Variables:
**Mac/Linux:**
```bash
export REACT_APP_API_URL=http://localhost:5000/api
```

**Windows (Command Prompt):**
```cmd
set REACT_APP_API_URL=http://localhost:5000/api
```

**Windows (PowerShell):**
```powershell
$env:REACT_APP_API_URL="http://localhost:5000/api"
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "python is not recognized"
**Solution:**
- Reinstall Python and check "Add to PATH"
- Or use `py` instead of `python`
- Or use full path: `C:\Python310\python.exe`

### Issue 2: "npm is not recognized"
**Solution:**
- Reinstall Node.js
- Restart Command Prompt after installation
- Verify: `npm --version`

### Issue 3: "Prophet installation fails"
**Solution:**
- Install Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
- Select "C++ build tools" during installation
- Then retry: `pip install prophet`

### Issue 4: "PowerShell execution policy error"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue 5: "Port 5000 already in use"
**Solution:**
- Find process: `netstat -ano | findstr :5000`
- Kill process: `taskkill /PID <process_id> /F`
- Or change port in `.env` file

### Issue 6: "CORS errors"
**Solution:**
- Check `backend/.env` has correct `FRONTEND_URL`
- Or update `backend/app.py` CORS settings

### Issue 7: "Module not found errors"
**Solution:**
- Make sure virtual environment is activated (see `(venv)` in prompt)
- Reinstall: `pip install -r requirements.txt`
- Check you're in the correct directory

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Browser opens to `http://localhost:3000`
- [ ] "Load Forecast" button works
- [ ] "Load Anomalies" button works
- [ ] Charts display correctly
- [ ] No console errors in browser (F12)
- [ ] No errors in backend terminal

---

## 📝 Quick Start Scripts for Windows

### Create `start_backend.bat` (Windows Batch File):
```batch
@echo off
cd backend
call venv\Scripts\activate
python app.py
pause
```

### Create `start_frontend.bat`:
```batch
@echo off
cd frontend
npm start
pause
```

**Usage:** Double-click these files to start backend/frontend!

---

## 🔄 Alternative: Use WSL (Windows Subsystem for Linux)

If you prefer Linux commands on Windows:

1. Install WSL: `wsl --install`
2. Use Linux commands inside WSL
3. Follow Mac/Linux instructions instead

---

## 📦 Complete Setup Commands (Copy-Paste Ready)

### Backend Setup:
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python app.py
```

### Frontend Setup (New Terminal):
```cmd
cd frontend
npm install
npm start
```

---

## 🎯 Summary

1. **Zip project** (exclude venv, node_modules, logs)
2. **Extract on Windows**
3. **Install Python & Node.js**
4. **Create venv** and install backend dependencies
5. **Install frontend** dependencies with npm
6. **Run both** servers
7. **Access** at `http://localhost:3000`

**That's it! Your project should work on Windows!** 🎉

---

## 📞 Need Help?

If you encounter issues:
1. Check error messages carefully
2. Verify Python and Node.js are installed correctly
3. Make sure virtual environment is activated
4. Check that ports 3000 and 5000 are not in use
5. Review the troubleshooting section above

**The project is fully cross-platform compatible!** ✅

