# ⚡ Quick Transfer Guide: Mac → Windows

## 🎯 TL;DR - Fastest Way

### On Mac (Before Transfer):

1. **Create ZIP (exclude large folders):**
   ```bash
   cd /Users/summaiya.sarvari/Desktop
   zip -r finops-project.zip fin \
     -x "*.DS_Store" \
     -x "*/venv/*" \
     -x "*/node_modules/*" \
     -x "*/__pycache__/*" \
     -x "*/logs/*" \
     -x "*/.env"
   ```

2. **Transfer ZIP** (USB, cloud, email, etc.)

### On Windows (After Transfer):

1. **Extract ZIP** to `C:\Users\YourName\Desktop\fin`

2. **Install Prerequisites:**
   - Python 3.10.x from python.org (check "Add to PATH")
   - Node.js from nodejs.org

3. **Backend Setup:**
   ```cmd
   cd C:\Users\YourName\Desktop\fin\backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   python app.py
   ```

4. **Frontend Setup (New Terminal):**
   ```cmd
   cd C:\Users\YourName\Desktop\fin\frontend
   npm install
   npm start
   ```

5. **Open Browser:** `http://localhost:3000`

**Done!** ✅

---

## 📋 Or Use Batch Files (Easier!)

After extracting on Windows, just **double-click:**
- `start_backend.bat` - Starts backend
- `start_frontend.bat` - Starts frontend

They'll handle everything automatically!

---

## 🆘 Quick Troubleshooting

**"python is not recognized"**
→ Reinstall Python, check "Add to PATH"

**"npm is not recognized"**
→ Reinstall Node.js, restart terminal

**"Port already in use"**
→ Close other programs using ports 3000/5000

**"Module not found"**
→ Make sure virtual environment is activated (see `(venv)` in prompt)

---

**For detailed instructions, see `CROSS_PLATFORM_MIGRATION.md`**

