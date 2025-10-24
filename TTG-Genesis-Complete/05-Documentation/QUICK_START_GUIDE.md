# 🚀 TTG Genesis Enhanced - Quick Start Guide

**Get your enhanced world generation system running in 5 minutes!**

---

## 🎯 **Super Quick Start (1-Click)**

### **Windows Users**
1. **Double-click** `START_TTG_GENESIS.bat`
2. **Wait** for automatic setup and launch
3. **Browser opens** automatically to http://localhost:5000
4. **Start generating worlds!**

---

## 🖥️ **Manual Start (All Platforms)**

### **Step 1: Open Terminal/Command Prompt**
```bash
# Windows
Win + R → type "cmd" → Enter
# or
Win + R → type "powershell" → Enter

# Mac
Cmd + Space → type "terminal" → Enter

# Linux
Ctrl + Alt + T
```

### **Step 2: Navigate to TTG Genesis**
```bash
# Replace with your actual path
cd "C:\path\to\TTG-Genesis-Complete"
# or
cd "/path/to/TTG-Genesis-Complete"
```

### **Step 3: Go to Backend Folder**
```bash
# Windows
cd "02-Web-Interface\backend"

# Mac/Linux
cd "02-Web-Interface/backend"
```

### **Step 4: Install Dependencies (First Time Only)**
```bash
pip install flask flask-cors requests pyyaml
```

### **Step 5: Start the Server**
```bash
# Option 1: Enhanced Server (Recommended)
python enhanced-start-server.py

# Option 2: Enhanced App
python enhanced-app.py

# Option 3: Demo Server
python simple-demo.py

# Option 4: Basic Server
python app.py
```

### **Step 6: Open Browser**
Go to: **http://localhost:5000**

---

## 🎮 **What You'll See**

### **Enhanced Interface Features**
- **🎛️ Toggle Controls**: Choose exactly what to generate
- **🖼️ World Gallery**: Visual thumbnails of all your worlds
- **📜 Generation History**: Track all your creations
- **👁️ 3D Previews**: Interactive world visualization
- **⚙️ UE5 Settings**: Configure Unreal Engine integration

### **Generation Options**
- **Content**: Quests, NPCs, Environment, Combat
- **UE5 Integration**: C++, Blueprints, Levels, Auto-compile
- **Project Type**: New UE5 project or existing integration
- **Automation**: Full automation or selective control
- **Previews**: 3D web preview and/or UE5 screenshots

---

## 🌟 **Try Your First World**

### **Example Prompts**
Copy and paste any of these into the generator:

```
Create a magical forest with fairy NPCs who give quests to collect enchanted crystals. Include a hidden temple with puzzle challenges and a wise dragon boss.
```

```
Cyberpunk city district with hacker NPCs who offer data heist missions. Include neon-lit streets, corporate buildings, and underground hideouts.
```

```
Medieval castle under siege with knight NPCs defending against orc invaders. Include castle walls, armory, and throne room with king NPC.
```

```
Space station orbiting alien planet with scientist NPCs studying mysterious artifacts. Include research labs, observation decks, and alien encounters.
```

### **Quick Generation Steps**
1. **Enter prompt** in the text area
2. **Enable options** you want (or use defaults)
3. **Choose automation level** (Full for beginners)
4. **Click "Generate World"**
5. **Watch the progress** in real-time
6. **View results** in gallery and 3D preview!

---

## 🛠️ **Troubleshooting**

### **❌ "Python is not recognized"**
**Solution**: Install Python from https://python.org
- ✅ Check "Add Python to PATH" during installation
- ✅ Restart command prompt after installation

### **❌ "No module named 'flask'"**
**Solution**: Install Flask
```bash
pip install flask flask-cors requests pyyaml
```

### **❌ "Address already in use"**
**Solution**: Port 5000 is busy
```bash
# Try different port
python enhanced-app.py --port 5001

# Or kill existing process (Windows)
netstat -ano | findstr :5000
taskkill /PID [PID_NUMBER] /F
```

### **❌ "Permission denied"**
**Solution**: Run as administrator
- Right-click Command Prompt → "Run as administrator"
- Or use: `sudo python enhanced-start-server.py` (Mac/Linux)

### **❌ Files not found**
**Solution**: Check you're in the right directory
```bash
# Check current location
pwd  # Mac/Linux
cd   # Windows

# List files
ls   # Mac/Linux
dir  # Windows

# Should see: 02-Web-Interface folder
```

---

## 🎯 **Server Options Explained**

### **🌟 enhanced-start-server.py (Best)**
- ✅ Complete system checks
- ✅ Automatic dependency installation
- ✅ Beautiful startup banner
- ✅ Browser auto-launch
- ✅ All enhanced features

### **🎮 enhanced-app.py (Full Features)**
- ✅ World gallery with thumbnails
- ✅ 3D previews with Three.js
- ✅ Generation history tracking
- ✅ UE5 integration system
- ✅ Advanced toggle controls

### **🎪 simple-demo.py (Demo)**
- ✅ Quick demonstration
- ✅ Beautiful interface
- ✅ Example prompts
- ✅ No complex setup needed

### **🔧 app.py (Basic)**
- ✅ Simple world generation
- ✅ JSON output
- ✅ Minimal dependencies

---

## 🌐 **Accessing the Interface**

### **URLs**
- **Main Interface**: http://localhost:5000
- **Alternative Port**: http://localhost:5001 (if 5000 is busy)

### **Interface Sections**
1. **🚀 World Generator**: Create new worlds
2. **🖼️ World Gallery**: Manage existing worlds
3. **📜 Generation History**: Track all generations
4. **⚙️ UE5 Settings**: Configure integration

---

## 🎉 **Success Indicators**

### **✅ Server Started Successfully**
You should see:
```
🎉 TTG GENESIS ENHANCED IS READY!
🌐 Web Interface: http://localhost:5000
```

### **✅ Browser Opens Automatically**
- Beautiful dark interface loads
- Toggle controls are visible
- Example prompts are clickable

### **✅ Generation Works**
- Progress bar shows during generation
- Results appear in output tabs
- Gallery updates with new worlds

---

## 🚀 **Next Steps**

### **1. Generate Your First World**
- Use one of the example prompts
- Enable all options for full experience
- Watch the real-time progress

### **2. Explore the Gallery**
- See visual thumbnails of worlds
- Try search and filter options
- Use preview, edit, delete actions

### **3. Check Generation History**
- View timeline of all generations
- See success/failure rates
- Try regenerating failed attempts

### **4. Configure UE5 Integration**
- Set UE5 installation path
- Test connection status
- Try auto-detection feature

### **5. Create Complex Worlds**
- Experiment with different themes
- Try selective automation
- Integrate with existing UE5 projects

---

## 🆘 **Still Need Help?**

### **Check These Files**
- `HOW_TO_RUN.md` - Detailed instructions
- `ENHANCED_README.md` - Complete feature guide
- `SYSTEM_OVERVIEW.md` - Technical overview

### **Common Solutions**
1. **Restart** command prompt/terminal
2. **Run as administrator** (Windows)
3. **Try different port** (5001, 5002, etc.)
4. **Reinstall Python** with PATH option
5. **Use full Python path**: `C:\Python39\python.exe`

---

## 🎮 **You're Ready!**

**Your TTG Genesis Enhanced system should now be running!**

### **🌟 What You Can Do:**
- ✨ Generate unlimited game worlds
- 🎮 Create complete UE5 projects
- 👁️ Preview worlds in 3D
- 📊 Track your generation history
- 🖼️ Manage worlds visually
- ⚙️ Integrate with Unreal Engine

### **🚀 Start Creating:**
1. **Open** http://localhost:5000
2. **Enter** a world description
3. **Configure** generation options
4. **Click** "Generate World"
5. **Watch** the magic happen!

**Transform your imagination into reality!** 🌟🎮✨

---

**Happy World Building!** 🚀
