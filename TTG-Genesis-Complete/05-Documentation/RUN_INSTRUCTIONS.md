# 🎮 TTG Genesis Enhanced - How to Run the Web Interface

**Complete step-by-step instructions to get your enhanced world generation system running!**

---

## 🚀 **Method 1: One-Click Start (Windows)**

### **Super Easy - Just Double-Click!**
1. **Find** the `START_TTG_GENESIS.bat` file in the TTG-Genesis-Complete folder
2. **Double-click** it
3. **Wait** for automatic setup (installs dependencies if needed)
4. **Browser opens** automatically to http://localhost:5000
5. **Start generating worlds!**

**That's it! The system handles everything automatically.**

---

## 🖥️ **Method 2: Manual Start (All Platforms)**

### **Step-by-Step Instructions**

#### **1. Open Terminal/Command Prompt**
- **Windows**: Press `Win + R`, type `cmd`, press Enter
- **Mac**: Press `Cmd + Space`, type `terminal`, press Enter  
- **Linux**: Press `Ctrl + Alt + T`

#### **2. Navigate to TTG Genesis Folder**
```bash
# Example paths - replace with your actual path:
cd "C:\Users\YourName\Desktop\TTG-Genesis-Complete"
cd "C:\Users\YourName\Downloads\TTG-Genesis-Complete"
cd "/Users/YourName/Desktop/TTG-Genesis-Complete"
```

#### **3. Go to Backend Directory**
```bash
# Windows
cd "02-Web-Interface\backend"

# Mac/Linux  
cd "02-Web-Interface/backend"
```

#### **4. Install Dependencies (First Time Only)**
```bash
pip install flask flask-cors requests pyyaml
```

#### **5. Start the Server**
Choose one of these options:

```bash
# Option A: Enhanced Server (Recommended)
python enhanced-start-server.py

# Option B: Enhanced App  
python enhanced-app.py

# Option C: Demo Server
python simple-demo.py

# Option D: Basic Server
python app.py
```

#### **6. Open Your Browser**
Go to: **http://localhost:5000**

---

## 🎯 **What Each Server Option Does**

### **🌟 enhanced-start-server.py (BEST CHOICE)**
- ✅ **Complete system checks** and automatic setup
- ✅ **Installs missing dependencies** automatically  
- ✅ **Creates required folders** if missing
- ✅ **Beautiful startup banner** with status info
- ✅ **Opens browser automatically**
- ✅ **All enhanced features** included

**Use this for the full experience!**

### **🎮 enhanced-app.py (FULL FEATURES)**
- ✅ **World Gallery** with visual thumbnails
- ✅ **3D Previews** using Three.js
- ✅ **Generation History** tracking
- ✅ **UE5 Integration** system
- ✅ **Advanced Toggle Controls**
- ✅ **Screenshot Generation**

**Use this if you want all features without the startup checks.**

### **🎪 simple-demo.py (QUICK DEMO)**
- ✅ **Beautiful demo interface**
- ✅ **Example prompts** for quick testing
- ✅ **No complex setup** required
- ✅ **Shows system capabilities**

**Use this for a quick demonstration or if other servers don't work.**

### **🔧 app.py (BASIC)**
- ✅ **Simple world generation**
- ✅ **JSON output only**
- ✅ **Minimal dependencies**

**Use this as a fallback if enhanced versions don't work.**

---

## 🌟 **Expected Results**

### **✅ Successful Startup**
You should see output like this:

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

### **✅ Browser Interface**
Your browser should open to a beautiful dark interface with:
- **Header**: "TTG Genesis Enhanced" with version badge
- **Navigation**: Generator, Gallery, History, Settings tabs
- **Toggle Controls**: Visual switches for generation options
- **Example Prompts**: Clickable example world descriptions

---

## 🛠️ **Troubleshooting Guide**

### **❌ Problem: "Python is not recognized"**
**Solution**: Install Python
1. Go to https://python.org
2. Download Python 3.7 or higher
3. **IMPORTANT**: Check "Add Python to PATH" during installation
4. Restart command prompt and try again

### **❌ Problem: "No module named 'flask'"**
**Solution**: Install Flask
```bash
pip install flask flask-cors requests pyyaml

# If pip doesn't work, try:
python -m pip install flask flask-cors requests pyyaml
```

### **❌ Problem: "Address already in use"**
**Solution**: Port 5000 is busy
```bash
# Try a different port
python enhanced-app.py --port 5001

# Then go to: http://localhost:5001
```

### **❌ Problem: "Permission denied"**
**Solution**: Run as administrator
- **Windows**: Right-click Command Prompt → "Run as administrator"
- **Mac/Linux**: Use `sudo python enhanced-start-server.py`

### **❌ Problem: "File not found"**
**Solution**: Check your location
```bash
# Check where you are
pwd  # Mac/Linux
cd   # Windows

# List files - you should see "02-Web-Interface" folder
ls   # Mac/Linux  
dir  # Windows

# If not, navigate to the correct folder
cd "path/to/TTG-Genesis-Complete"
```

### **❌ Problem: Browser doesn't open**
**Solution**: Open manually
- Go to http://localhost:5000 in any browser
- Try Chrome, Firefox, Edge, or Safari

---

## 🎮 **Using the Interface**

### **🚀 Generate Your First World**
1. **Enter a description**: "Create a magical forest with fairy NPCs"
2. **Configure options**: Use toggle switches to choose what to generate
3. **Select automation**: Choose "Full Automation" for beginners
4. **Click "Generate World"**: Watch the real-time progress
5. **View results**: See JSON data, 3D preview, and screenshots

### **🖼️ Explore the Gallery**
- **Visual thumbnails** of all your worlds
- **Search and filter** by theme or date
- **Quick actions**: Preview, edit, or delete worlds
- **Status indicators**: See which worlds are UE5-ready

### **📜 Check History**
- **Timeline view** of all generations
- **Success/failure tracking**
- **Performance metrics**
- **Regeneration options**

### **⚙️ Configure UE5**
- **Set UE5 installation path**
- **Configure Python path for UE5**
- **Test connection status**
- **Auto-detect installations**

---

## 🌟 **Example Prompts to Try**

Copy and paste these into the generator:

### **🌲 Fantasy World**
```
Create a magical forest with fairy NPCs who give quests to collect enchanted crystals. Include a hidden temple with puzzle challenges and a wise dragon boss.
```

### **🏙️ Cyberpunk World**
```
Cyberpunk city district with hacker NPCs who offer data heist missions. Include neon-lit streets, corporate buildings, and underground hideouts.
```

### **🏰 Medieval World**
```
Medieval castle under siege with knight NPCs defending against orc invaders. Include castle walls, armory, and throne room with king NPC.
```

### **🚀 Space World**
```
Space station orbiting alien planet with scientist NPCs studying mysterious artifacts. Include research labs, observation decks, and alien encounters.
```

---

## 🎯 **Success Checklist**

### **✅ System is Working When:**
- [ ] Server starts without errors
- [ ] Browser opens to http://localhost:5000
- [ ] Interface loads with dark theme and toggle controls
- [ ] You can enter text in the prompt area
- [ ] Generate button responds when clicked
- [ ] Progress bar shows during generation
- [ ] Results appear in output tabs
- [ ] Gallery shows generated worlds
- [ ] History tracks generations

### **✅ Full Features Working When:**
- [ ] Toggle switches work
- [ ] 3D preview loads and is interactive
- [ ] Screenshots generate (if UE5 configured)
- [ ] World gallery shows thumbnails
- [ ] Search and filter work in gallery
- [ ] Generation history shows timeline
- [ ] UE5 settings page loads

---

## 🎉 **You're Ready to Create!**

**Once you see the interface, you can:**

### **🌟 Generate Unlimited Worlds**
- Enter any world description
- Choose exactly what to generate
- Get complete UE5-ready projects

### **🎮 Manage Your Creations**
- Visual gallery of all worlds
- Search and organize easily
- Track generation history

### **👁️ Preview Before Building**
- Interactive 3D previews
- Multiple camera angles
- See your world come to life

### **🚀 Integrate with UE5**
- Automatic C++ generation
- Blueprint creation
- Complete project setup
- One-click compilation

---

## 🆘 **Still Having Issues?**

### **📖 Check These Files:**
- `HOW_TO_RUN.md` - Detailed technical instructions
- `ENHANCED_README.md` - Complete feature documentation
- `SYSTEM_OVERVIEW.md` - Technical system overview

### **🔧 Alternative Methods:**
1. Try the **simple-demo.py** for a basic test
2. Use **app.py** for minimal functionality
3. Check **requirements.txt** for dependencies
4. Run **START_TTG_GENESIS.bat** on Windows

### **💡 Common Solutions:**
- Restart your terminal/command prompt
- Try running as administrator
- Use a different port (5001, 5002, etc.)
- Reinstall Python with PATH option
- Check firewall/antivirus settings

---

## 🚀 **Ready to Transform Ideas into Games!**

**Your TTG Genesis Enhanced system is now ready to turn any text description into a complete, playable UE5 game world!**

**Start creating amazing worlds today!** 🌟🎮✨
