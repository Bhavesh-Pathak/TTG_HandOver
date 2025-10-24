# 🛠️ TTG Genesis Enhanced - Troubleshooting Guide

**Solutions for common issues when running the enhanced system**

---

## 🚨 **Error: "No module named 'enhanced_app'"**

### **✅ Solution 1: Use the Correct File**
The issue is fixed! Use the new `enhanced_app.py` file (with underscore):

```bash
cd "TTG-Genesis-Complete/02-Web-Interface/backend"
python enhanced_app.py
```

### **✅ Solution 2: Test First**
Run the test script to verify everything works:

```bash
cd "TTG-Genesis-Complete/02-Web-Interface/backend"
python test_server.py
```

### **✅ Solution 3: Use the Startup Script**
The enhanced startup script now handles this automatically:

```bash
cd "TTG-Genesis-Complete/02-Web-Interface/backend"
python enhanced-start-server.py
```

---

## 🚨 **Error: "Python is not recognized"**

### **✅ Solution: Install Python Properly**

1. **Download Python** from https://python.org
2. **During installation**: ✅ Check "Add Python to PATH"
3. **Restart** your command prompt/terminal
4. **Test**: Run `python --version`

### **Alternative: Use Full Path**
```bash
# Windows example
C:\Python39\python.exe enhanced_app.py

# Find Python location
where python
```

---

## 🚨 **Error: "No module named 'flask'"**

### **✅ Solution: Install Dependencies**

```bash
# Install all required packages
pip install flask flask-cors requests pyyaml

# If pip doesn't work, try:
python -m pip install flask flask-cors requests pyyaml

# Or install one by one:
pip install flask
pip install flask-cors
pip install requests
pip install pyyaml
```

### **Alternative: Use requirements.txt**
```bash
pip install -r requirements.txt
```

---

## 🚨 **Error: "Address already in use" (Port 5000 busy)**

### **✅ Solution 1: Use Different Port**
```bash
python enhanced_app.py --port 5001
# Then go to: http://localhost:5001
```

### **✅ Solution 2: Kill Existing Process**

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

**Mac/Linux:**
```bash
lsof -ti:5000 | xargs kill
```

### **✅ Solution 3: Find Available Port**
Try ports: 5001, 5002, 8000, 8080, 3000

---

## 🚨 **Error: "Permission denied"**

### **✅ Solution: Run as Administrator**

**Windows:**
- Right-click Command Prompt → "Run as administrator"
- Or right-click PowerShell → "Run as administrator"

**Mac/Linux:**
```bash
sudo python enhanced_app.py
```

---

## 🚨 **Error: "File not found" or "No such file or directory"**

### **✅ Solution: Check Your Location**

```bash
# Check where you are
pwd  # Mac/Linux
cd   # Windows (shows current directory)

# List files - you should see "02-Web-Interface" folder
ls   # Mac/Linux
dir  # Windows

# Navigate to correct folder
cd "path/to/TTG-Genesis-Complete/02-Web-Interface/backend"
```

### **Common Correct Paths:**
```bash
# Examples - replace with your actual path
cd "C:\Users\YourName\Desktop\TTG-Genesis-Complete\02-Web-Interface\backend"
cd "C:\Users\YourName\Downloads\TTG-Genesis-Complete\02-Web-Interface\backend"
cd "/Users/YourName/Desktop/TTG-Genesis-Complete/02-Web-Interface/backend"
```

---

## 🚨 **Browser doesn't open automatically**

### **✅ Solution: Open Manually**

1. **Start the server** (you should see "Server running" message)
2. **Open any browser** (Chrome, Firefox, Edge, Safari)
3. **Go to**: http://localhost:5000
4. **If port 5000 doesn't work**, try: http://localhost:5001

---

## 🚨 **Interface loads but generation doesn't work**

### **✅ Solution 1: Check Console**
1. **Open browser developer tools** (F12)
2. **Check Console tab** for error messages
3. **Look for network errors** in Network tab

### **✅ Solution 2: Test with Simple Prompt**
Try a basic prompt first:
```
Create a simple village with 2 NPCs
```

### **✅ Solution 3: Check Server Output**
Look at the terminal/command prompt where the server is running for error messages.

---

## 🚨 **"Import Error" or "Module not found" for other modules**

### **✅ Solution: Install Missing Packages**

```bash
# Common missing packages
pip install pathlib
pip install datetime
pip install uuid
pip install json

# Or install everything at once
pip install flask flask-cors requests pyyaml pathlib
```

---

## 🚨 **Firewall or Antivirus Blocking**

### **✅ Solution: Allow Python/Flask**

1. **Windows Defender**: Allow Python through firewall
2. **Antivirus**: Add Python.exe to exceptions
3. **Corporate Network**: Check with IT department
4. **Try different port**: Use 8080 or 3000 instead of 5000

---

## 🚨 **System is slow or unresponsive**

### **✅ Solution: Check System Resources**

1. **Close other applications** to free up memory
2. **Try basic server** instead of enhanced:
   ```bash
   python app.py  # If available
   ```
3. **Restart your computer** if needed
4. **Check available disk space**

---

## 🧪 **Testing Your Installation**

### **Step 1: Run System Test**
```bash
cd "TTG-Genesis-Complete/02-Web-Interface/backend"
python test_server.py
```

### **Step 2: Check Each Component**

**Test Python:**
```bash
python --version
# Should show Python 3.7 or higher
```

**Test Flask:**
```bash
python -c "import flask; print('Flask OK')"
```

**Test Enhanced App:**
```bash
python -c "from enhanced_app import app; print('Enhanced App OK')"
```

---

## 🎯 **Step-by-Step Diagnosis**

### **If Nothing Works, Try This Order:**

1. **Check Python Installation**
   ```bash
   python --version
   ```

2. **Install Dependencies**
   ```bash
   pip install flask flask-cors requests pyyaml
   ```

3. **Test Import**
   ```bash
   python -c "import flask; print('OK')"
   ```

4. **Navigate to Correct Folder**
   ```bash
   cd "TTG-Genesis-Complete/02-Web-Interface/backend"
   ```

5. **Run Test Server**
   ```bash
   python test_server.py
   ```

6. **Run Enhanced App**
   ```bash
   python enhanced_app.py
   ```

---

## 🆘 **Still Having Issues?**

### **Try These Alternative Methods:**

#### **Method 1: Basic Server**
```bash
python app.py  # If available
```

#### **Method 2: Demo Server**
```bash
python simple-demo.py
```

#### **Method 3: Direct Flask**
```bash
flask --app enhanced_app run --port 5000
```

#### **Method 4: One-Click Batch (Windows)**
Double-click: `START_TTG_GENESIS.bat`

---

## 📋 **System Requirements Check**

### **✅ Minimum Requirements:**
- **Python 3.7+** ✓
- **4GB RAM** ✓
- **2GB Storage** ✓
- **Modern Browser** ✓

### **✅ Required Packages:**
- **flask** ✓
- **flask-cors** ✓
- **requests** ✓
- **pyyaml** ✓

### **✅ File Structure:**
```
TTG-Genesis-Complete/
├── 02-Web-Interface/
│   └── backend/
│       ├── enhanced_app.py ✓
│       ├── enhanced-start-server.py ✓
│       ├── test_server.py ✓
│       └── simple-demo.py ✓
```

---

## 🎉 **Success Indicators**

### **✅ Server Started Successfully:**
```
🚀 Starting TTG Genesis Enhanced Server...
🌐 Web Interface: http://localhost:5000
Press Ctrl+C to stop the server
```

### **✅ Browser Interface Loads:**
- Dark theme with cyan accents
- "TTG Genesis Enhanced" header
- Text input area for prompts
- Toggle switches for options
- "Generate World" button

### **✅ Generation Works:**
- Click "Generate World" button
- Loading spinner appears
- Results show in output area
- JSON data is properly formatted

---

## 🚀 **Quick Fix Summary**

### **Most Common Issues & Quick Fixes:**

1. **"No module named 'enhanced_app'"** → Use `python enhanced_app.py`
2. **"Python not recognized"** → Install Python with PATH option
3. **"No module named 'flask'"** → Run `pip install flask flask-cors`
4. **"Address already in use"** → Use different port: `--port 5001`
5. **"Permission denied"** → Run as administrator
6. **"File not found"** → Navigate to correct backend folder

### **Emergency Backup Plan:**
If nothing works, try the simple demo:
```bash
python simple-demo.py
```

---

## 🎯 **You Should Now Be Able To:**

- ✅ Start the enhanced server without errors
- ✅ Open the web interface in your browser
- ✅ Generate worlds using the interface
- ✅ See results in JSON format
- ✅ Use all the enhanced features

**If you're still having issues, double-check that you're using the correct file names and paths!**

**Happy World Building!** 🌟🎮✨
