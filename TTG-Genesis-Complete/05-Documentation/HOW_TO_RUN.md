# 🚀 How to Run TTG Genesis Enhanced - Complete Guide

## 📋 **Quick Start (5 Minutes)**

### **Step 1: Open Command Prompt or PowerShell**
```bash
# Windows (Command Prompt)
Win + R → type "cmd" → Enter

# Windows (PowerShell) - Recommended
Win + R → type "powershell" → Enter

# Mac/Linux (Terminal)
Cmd + Space → type "terminal" → Enter
```

### **Step 2: Navigate to the TTG Genesis Folder**
```bash
# Find where you saved TTG-Genesis-Complete
# Example paths:
cd "C:\TTG-Genesis-Complete"
cd "C:\Users\YourName\Desktop\TTG-Genesis-Complete"
cd "C:\Users\YourName\Downloads\TTG-Genesis-Complete"

# Or if you're in the same folder as TTG-Genesis-Complete:
cd TTG-Genesis-Complete
```

### **Step 3: Navigate to Backend Folder**
```bash
cd "02-Web-Interface\backend"
# or on Mac/Linux:
cd "02-Web-Interface/backend"
```

### **Step 4: Run the Enhanced Server**
```bash
# Option 1: Enhanced startup (recommended)
python enhanced-start-server.py

# Option 2: Direct server start
python enhanced-app.py

# Option 3: Basic server (if enhanced doesn't work)
python app.py
```

### **Step 5: Open Your Browser**
The server will automatically open your browser, or manually go to:
```
http://localhost:5000
```

---

## 🔧 **Detailed Setup Instructions**

### **Prerequisites Check**

#### **1. Python Installation**
```bash
# Check if Python is installed
python --version
# Should show Python 3.7+ (e.g., Python 3.9.7)

# If not installed, download from: https://python.org
```

#### **2. Required Packages**
```bash
# Install required packages
pip install flask flask-cors requests pyyaml

# Or install all at once
pip install -r requirements.txt
```

#### **3. Directory Structure Verification**
Make sure you have this structure:
```
TTG-Genesis-Complete/
├── 02-Web-Interface/
│   ├── frontend/
│   │   ├── enhanced-index.html
│   │   ├── enhanced-style.css
│   │   ├── enhanced-script.js
│   │   └── three-preview.js
│   └── backend/
│       ├── enhanced-start-server.py
│       ├── enhanced-app.py
│       └── app.py
```

---

## 🚀 **Running Options**

### **Option 1: Enhanced Startup (Recommended)**
```bash
# Navigate to backend folder
cd "TTG-Genesis-Complete/02-Web-Interface/backend"

# Run enhanced startup
python enhanced-start-server.py
```

**Features:**
- ✅ Automatic system checks
- ✅ Dependency installation
- ✅ Directory creation
- ✅ Browser auto-launch
- ✅ Beautiful startup banner

### **Option 2: Direct Enhanced Server**
```bash
# Navigate to backend folder
cd "TTG-Genesis-Complete/02-Web-Interface/backend"

# Run enhanced server directly
python enhanced-app.py
```

**Features:**
- ✅ Full UE5 integration
- ✅ World gallery
- ✅ 3D previews
- ✅ Generation history

### **Option 3: Basic Server**
```bash
# Navigate to backend folder
cd "TTG-Genesis-Complete/02-Web-Interface/backend"

# Run basic server
python app.py
```

**Features:**
- ✅ Basic world generation
- ✅ Simple web interface
- ✅ JSON output

---

## 🌐 **Accessing the Web Interface**

### **Default URLs**
- **Main Interface**: http://localhost:5000
- **Enhanced Interface**: http://localhost:5000 (with enhanced-app.py)
- **API Endpoint**: http://localhost:5000/api/generate

### **Interface Features**

#### **Enhanced Interface (enhanced-app.py)**
- 🎛️ **Toggle Controls**: Choose what to generate
- 🖼️ **World Gallery**: Visual world management
- 📜 **Generation History**: Track all generations
- ⚙️ **UE5 Settings**: Configure UE5 integration
- 👁️ **3D Previews**: Interactive world previews

#### **Basic Interface (app.py)**
- 📝 **Text Input**: Enter world description
- 🎮 **Generate Button**: Create world
- 📄 **JSON Output**: View generated data

---

## 🛠️ **Troubleshooting**

### **Common Issues & Solutions**

#### **❌ "Python is not recognized"**
```bash
# Solution 1: Add Python to PATH
# Windows: Add Python installation folder to system PATH

# Solution 2: Use full Python path
C:\Python39\python.exe enhanced-start-server.py

# Solution 3: Reinstall Python with "Add to PATH" checked
```

#### **❌ "No module named 'flask'"**
```bash
# Install Flask
pip install flask flask-cors requests pyyaml

# If pip doesn't work, try:
python -m pip install flask flask-cors requests pyyaml
```

#### **❌ "Address already in use"**
```bash
# Port 5000 is busy, use different port
python enhanced-app.py --port 5001

# Or kill existing process:
# Windows: netstat -ano | findstr :5000
# Mac/Linux: lsof -ti:5000 | xargs kill
```

#### **❌ "File not found" errors**
```bash
# Make sure you're in the right directory
pwd  # Check current directory
ls   # List files (Mac/Linux)
dir  # List files (Windows)

# Navigate to correct folder
cd "path/to/TTG-Genesis-Complete/02-Web-Interface/backend"
```

#### **❌ Browser doesn't open automatically**
```bash
# Manually open browser and go to:
http://localhost:5000

# Or try different browsers:
# Chrome, Firefox, Edge, Safari
```

#### **❌ "Permission denied" errors**
```bash
# Windows: Run as Administrator
# Right-click Command Prompt → "Run as administrator"

# Mac/Linux: Use sudo if needed
sudo python enhanced-start-server.py
```

---

## 🎯 **Step-by-Step Example**

### **Complete Walkthrough**

#### **1. Open Terminal/Command Prompt**
```bash
# Windows: Win + R → "cmd" → Enter
# Mac: Cmd + Space → "terminal" → Enter
```

#### **2. Navigate to TTG Genesis**
```bash
# Example for Windows Desktop
cd "C:\Users\YourName\Desktop\TTG-Genesis-Complete"

# Example for Downloads folder
cd "C:\Users\YourName\Downloads\TTG-Genesis-Complete"
```

#### **3. Go to Backend Folder**
```bash
cd "02-Web-Interface\backend"
```

#### **4. Check Python**
```bash
python --version
# Should show: Python 3.7.x or higher
```

#### **5. Install Dependencies**
```bash
pip install flask flask-cors requests pyyaml
```

#### **6. Start Server**
```bash
python enhanced-start-server.py
```

#### **7. Expected Output**
```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🎮 TTG GENESIS ENHANCED - Full UE5 Integration System                    ║
║                                                                              ║
║    Transform your imagination into playable UE5 game worlds!                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

🔍 Checking Python version...
✅ Python version: 3.9.7 (Compatible)

🔍 Checking dependencies...
✅ Flask: Available
✅ Flask-CORS: Available
✅ Requests: Available
✅ PyYAML: Available

🚀 Starting TTG Genesis Enhanced Server...
🌐 Starting web server...
🌍 Opening browser: http://localhost:5000

🎉 TTG GENESIS ENHANCED IS READY!
🌐 Web Interface: http://localhost:5000
```

#### **8. Use the Interface**
- Browser opens automatically to http://localhost:5000
- Enter world description: "Create a magical forest with fairy NPCs"
- Configure options using toggle switches
- Click "Generate World"
- View results in gallery and 3D preview!

---

## 🎮 **Using the Enhanced Interface**

### **Main Sections**

#### **🚀 World Generator**
- **Text Input**: Describe your world
- **Toggle Options**: Choose what to generate
- **Project Settings**: New or existing UE5 project
- **Automation Level**: Full or selective
- **Preview Options**: 3D and/or screenshots

#### **🖼️ World Gallery**
- **Visual Thumbnails**: See all your worlds
- **Search & Filter**: Find specific worlds
- **Quick Actions**: Preview, edit, delete
- **Status Indicators**: UE5 ready, C++ generated, etc.

#### **📜 Generation History**
- **Timeline View**: All generation attempts
- **Success/Failure**: Track what worked
- **Performance**: Generation times
- **Actions**: View, regenerate, delete

#### **⚙️ UE5 Settings**
- **Connection Setup**: Configure UE5 paths
- **Template Selection**: Choose project templates
- **System Status**: Check integration health

---

## 🎉 **Success! You're Ready**

### **What You Can Do Now:**

1. **🌟 Generate Your First World**
   - Try: "Create a magical forest with fairy NPCs and crystal quest"
   - Enable all options for full experience

2. **🖼️ Explore the Gallery**
   - See visual thumbnails of your worlds
   - Use search and filter options

3. **👁️ View 3D Previews**
   - Interactive 3D visualization
   - Multiple camera angles
   - Wireframe toggle

4. **🎮 UE5 Integration**
   - Configure UE5 settings
   - Generate complete projects
   - Auto-compile and test

5. **📜 Track Your Progress**
   - View generation history
   - Monitor success rates
   - Export/import data

---

## 🆘 **Still Having Issues?**

### **Get Help:**

1. **Check Error Messages**: Read console output carefully
2. **Verify File Structure**: Ensure all files are present
3. **Test Basic Version**: Try `python app.py` first
4. **Check Dependencies**: Reinstall packages if needed
5. **Try Different Port**: Use `--port 5001` if 5000 is busy

### **Alternative Startup Methods:**

```bash
# Method 1: Enhanced with custom port
python enhanced-app.py --port 5001

# Method 2: Basic server
python app.py

# Method 3: Direct Flask run
flask --app enhanced-app run --port 5000

# Method 4: Python module
python -m flask --app enhanced-app run
```

---

## 🎯 **You're All Set!**

**Your TTG Genesis Enhanced system is now running!**

🌐 **Open your browser to**: http://localhost:5000
🎮 **Start generating amazing game worlds!**
✨ **Transform your imagination into reality!**

**Happy World Building!** 🚀🎮🌟
