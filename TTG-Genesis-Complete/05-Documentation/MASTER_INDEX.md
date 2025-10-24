# 🎮 TTG Genesis - Master Index

**Complete Text-to-Game World Generator System**

## 🎯 **System Overview**

TTG Genesis transforms natural language prompts into complete, playable game worlds for Unreal Engine 5. The system is organized into 7 logical sections for easy learning and development.

---

## 📂 **Complete File Organization**

### **🔧 01-Core-System** - The Engine
**Location**: `01-Core-System/`

| Component | File | Purpose |
|-----------|------|---------|
| **Prompt Parser** | `prompt-parser/prompt_parser.py` | Converts text to JSON world data |
| **World Generator** | `world-generator/generator.py` | Creates UE5 C++ and Blueprint code |

**What it does**: Takes your text prompt → Creates structured world data → Generates UE5 code

---

### **🌐 02-Web-Interface** - User Interface
**Location**: `02-Web-Interface/`

| Component | Files | Purpose |
|-----------|-------|---------|
| **Frontend** | `frontend/index.html, style.css, script.js` | Beautiful web UI |
| **Backend** | `backend/app.py, start_server.py` | Flask server |

**What it does**: Provides a beautiful web interface so you don't need command line

---

### **💾 03-Generated-Worlds** - Output Storage
**Location**: `03-Generated-Worlds/`

| Component | Contents | Purpose |
|-----------|----------|---------|
| **JSON Data** | `json-data/*.json` | All generated world files |

**What it contains**: 
- `chrome_citadel.json` - Cyberpunk city world
- `generated_forest_level.json` - Forest adventure
- `the_ancient_magical.json` - Magical forest temple
- And more...

---

### **🎮 04-UE5-Integration** - Unreal Engine Ready
**Location**: `04-UE5-Integration/`

| Component | Files | Purpose |
|-----------|-------|---------|
| **C++ Code** | `cpp-code/*.h, *.cpp, *.Build.cs` | Production-ready UE5 classes |
| **Blueprint Data** | `blueprint-data/*.json` | JSON for Blueprint integration |

**What you get**:
- Complete quest systems
- NPC interaction systems
- Environment controllers
- Player controllers with abilities
- Module configurations

---

### **📖 05-Documentation** - Learning Resources
**Location**: `05-Documentation/`

| Component | Files | Purpose |
|-----------|-------|---------|
| **User Guides** | `user-guides/*.md` | How-to documentation |
| **Integration Guides** | `integration-guides/*.md` | UE5 setup help |

**Available guides**:
- System overview and features
- Web interface usage
- UE5 integration steps
- Example prompts and samples

---

### **⚙️ 06-Configuration** - System Settings
**Location**: `06-Configuration/`

| Component | Files | Purpose |
|-----------|-------|---------|
| **System Config** | `system-config/requirements.txt, setup.py, config.yaml` | Installation and settings |

**What's included**:
- Python dependencies
- System setup scripts
- Configuration options

---

### **🎯 07-Examples** - Sample Content
**Location**: `07-Examples/`

| Component | Purpose |
|-----------|---------|
| **Sample Worlds** | Ready-to-use example worlds |
| **Demo Projects** | Complete working examples |
| **Test Cases** | Testing scenarios |

---

## 🚀 **How to Use This System**

### **Step 1: Choose Your Method**
- **Easy**: Use web interface (`02-Web-Interface/`)
- **Advanced**: Use command line (`01-Core-System/`)

### **Step 2: Generate World**
- Write a prompt like: "Create a space station with alien NPCs"
- Get structured JSON world data

### **Step 3: Generate UE5 Code**
- Use the world generator to create C++ and Blueprint files
- Get production-ready UE5 classes

### **Step 4: Integrate with UE5**
- Copy files to your UE5 project
- Compile and run
- Play your generated world!

---

## 🎓 **Learning Progression**

### **Beginner (Start Here)**
1. **Read**: `QUICK_START.md` (this file)
2. **Try**: Web interface in `02-Web-Interface/`
3. **Explore**: Generated worlds in `03-Generated-Worlds/`

### **Intermediate**
1. **Study**: Core system in `01-Core-System/`
2. **Examine**: Generated UE5 code in `04-UE5-Integration/`
3. **Learn**: Integration process

### **Advanced**
1. **Customize**: Modify core system code
2. **Extend**: Add new features
3. **Integrate**: Build complete games

---

## 🔍 **Quick Reference**

### **Generate World (Web)**
```
1. Open: 02-Web-Interface/backend/start_server.py
2. Visit: http://localhost:5000
3. Enter prompt and generate
```

### **Generate World (Command)**
```bash
cd "01-Core-System/prompt-parser"
python prompt_parser.py "Your prompt"
```

### **Create UE5 Code**
```bash
cd "01-Core-System/world-generator"
python generator.py "world.json" -w WorldName
```

### **Find Generated Files**
- **World Data**: `03-Generated-Worlds/json-data/`
- **UE5 C++**: `04-UE5-Integration/cpp-code/`
- **Blueprint JSON**: `04-UE5-Integration/blueprint-data/`

---

## 🎯 **Key Benefits of This Organization**

✅ **Logical Flow**: Numbered folders show progression
✅ **Clear Purpose**: Each folder has a specific role
✅ **Easy Learning**: Start simple, progress to advanced
✅ **No Confusion**: No duplicate or scattered files
✅ **Professional**: Industry-standard structure
✅ **Scalable**: Easy to add new components

---

## 🎮 **Ready to Create!**

Your TTG Genesis system is now perfectly organized and ready to transform your imagination into playable game worlds!

**Start with the web interface and work your way through the system!** 🚀

---

**Next Steps:**
1. Try the web interface
2. Generate your first world
3. Explore the UE5 integration
4. Build amazing games!

**Happy World Building!** ✨
