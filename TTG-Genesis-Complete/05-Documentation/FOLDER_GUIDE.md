# 📁 TTG Genesis - Complete Folder Structure Guide

**Organized, clean, and easy to navigate system for learning and development**

## 🎯 **Folder Organization Philosophy**

This structure is designed for:
- **Easy Learning**: Logical progression from core to advanced
- **Clear Separation**: Each component has its dedicated space
- **Professional Structure**: Industry-standard organization
- **Scalability**: Easy to add new features and components

---

## 📂 **Detailed Folder Breakdown**

### **01-Core-System/** - The Heart of TTG Genesis
```
01-Core-System/
├── prompt-parser/          # Natural Language Processing
│   └── prompt_parser.py    # Main prompt analysis engine
└── world-generator/        # UE5 Code Generation
    └── generator.py        # C++ and Blueprint generator
```

**What's Here:**
- **prompt_parser.py**: Converts text prompts to structured JSON
- **generator.py**: Creates UE5-compatible C++ and Blueprint files
- **Purpose**: Core functionality that powers everything else

---

### **02-Web-Interface/** - User-Friendly Frontend
```
02-Web-Interface/
├── frontend/               # Web UI Components
│   ├── index.html         # Main webpage
│   ├── style.css          # Beautiful styling
│   └── script.js          # Interactive functionality
└── backend/               # Server Components
    ├── app.py             # Flask web server
    └── start_server.py    # Easy startup script
```

**What's Here:**
- **Frontend**: Beautiful black/grey UI with blurred background
- **Backend**: Flask server connecting web UI to core system
- **Purpose**: Easy-to-use interface for non-technical users

---

### **03-Generated-Worlds/** - Output Repository
```
03-Generated-Worlds/
└── json-data/             # Generated World Files
    ├── chrome_citadel.json
    ├── generated_desert_level.json
    ├── generated_forest_level.json
    ├── the_ancient_hidden.json
    ├── the_ancient_magical.json
    └── whispering_woods.json
```

**What's Here:**
- **JSON Files**: Complete world data from prompts
- **World Archives**: Saved and organized world generations
- **Purpose**: Repository of all generated game worlds

---

### **04-UE5-Integration/** - Unreal Engine Ready Code
```
04-UE5-Integration/
├── cpp-code/              # Generated C++ Classes
│   ├── *QuestSystem.h/cpp # Quest management systems
│   ├── *NPCSystem.h/cpp   # NPC interaction systems
│   ├── *Environment.h/cpp # Environment controllers
│   ├── *PlayerController.h/cpp # Player controllers
│   ├── *Module.h/cpp      # UE5 module definitions
│   └── *.Build.cs         # Build configurations
└── blueprint-data/        # Blueprint-Compatible JSON
    ├── QuestData.json     # Quest system data
    ├── NPCData.json       # NPC spawning data
    ├── EnvironmentData.json # Environment settings
    ├── AssetList.json     # Required assets
    └── WorldData_VaRest.json # VaRest plugin format
```

**What's Here:**
- **C++ Code**: Production-ready UE5 classes
- **Blueprint Data**: JSON files for Blueprint integration
- **Purpose**: Everything needed to integrate with Unreal Engine 5

---

### **05-Documentation/** - Learning Resources
```
05-Documentation/
├── user-guides/           # How-to Documentation
│   ├── GENERATOR_README.md # Generator usage guide
│   ├── WEB_README.md      # Web interface guide
│   ├── README.md          # Original system docs
│   └── prompt_samples.md  # Example prompts
└── integration-guides/    # UE5 Integration Help
    └── (UE5 integration guides)
```

**What's Here:**
- **User Guides**: Step-by-step instructions
- **Integration Guides**: UE5 setup and usage
- **Purpose**: Complete learning and reference materials

---

### **06-Configuration/** - System Settings
```
06-Configuration/
└── system-config/         # Core Configuration Files
    ├── requirements.txt   # Python dependencies
    ├── setup.py          # System setup script
    └── config.yaml       # System configuration
```

**What's Here:**
- **Dependencies**: All required packages
- **Setup Scripts**: Easy installation tools
- **Configuration**: System settings and options
- **Purpose**: Everything needed to configure the system

---

### **07-Examples/** - Sample Content
```
07-Examples/
├── sample-worlds/         # Example World Data
├── demo-projects/         # Complete Demo Projects
└── test-cases/           # Testing Scenarios
```

**What's Here:**
- **Sample Worlds**: Ready-to-use example worlds
- **Demo Projects**: Complete working examples
- **Purpose**: Learning materials and testing content

---

## 🎓 **Learning Path Recommendation**

### **For Beginners:**
1. Start with `05-Documentation/user-guides/README.md`
2. Try the web interface in `02-Web-Interface/`
3. Explore examples in `07-Examples/`
4. Check generated worlds in `03-Generated-Worlds/`

### **For Developers:**
1. Study core system in `01-Core-System/`
2. Examine generated code in `04-UE5-Integration/`
3. Review configuration in `06-Configuration/`
4. Customize and extend the system

### **For UE5 Integration:**
1. Read `05-Documentation/integration-guides/`
2. Use files from `04-UE5-Integration/`
3. Follow step-by-step integration process
4. Test with sample worlds

---

## 🔍 **Quick File Finder**

**Need to...**
- **Generate worlds?** → `02-Web-Interface/` or `01-Core-System/prompt-parser/`
- **Integrate with UE5?** → `04-UE5-Integration/`
- **Learn the system?** → `05-Documentation/`
- **Configure settings?** → `06-Configuration/`
- **See examples?** → `07-Examples/` or `03-Generated-Worlds/`

---

## 🎯 **Benefits of This Structure**

✅ **Easy Navigation**: Logical numbering and clear names
✅ **Separation of Concerns**: Each component isolated
✅ **Scalable**: Easy to add new features
✅ **Professional**: Industry-standard organization
✅ **Learning-Friendly**: Progressive complexity
✅ **Clean**: No duplicates or scattered files

**This structure makes TTG Genesis easy to understand, learn, and extend!** 🚀
