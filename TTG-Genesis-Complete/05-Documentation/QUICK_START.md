# 🚀 TTG Genesis - Quick Start Guide

**Get up and running in 5 minutes!**

## 🎯 **What You Have**

A complete **Text-to-Game World Generator** system that creates UE5-compatible game worlds from simple text prompts.

---

## ⚡ **Quick Start Options**

### **Option 1: Web Interface (Easiest)**
```bash
# Navigate to web interface
cd "02-Web-Interface/backend"

# Install dependencies
pip install Flask Flask-CORS requests PyYAML

# Start the server
python start_server.py
```
**Then open:** http://localhost:5000

### **Option 2: Command Line (Advanced)**
```bash
# Navigate to core system
cd "01-Core-System/prompt-parser"

# Generate a world
python prompt_parser.py "Create a magical forest with fairy NPCs"

# Generate UE5 code
cd "../world-generator"
python generator.py "../../03-Generated-Worlds/json-data/your_world.json"
```

### **Option 3: Complete Setup**
```bash
# Navigate to configuration
cd "06-Configuration/system-config"

# Run full setup
python setup.py
```

---

## 🎮 **Usage Examples**

### **Generate Your First World**
1. **Open Web Interface**: http://localhost:5000
2. **Enter Prompt**: "Create a haunted mansion with 3 ghost NPCs and puzzle quests"
3. **Click Generate**: Wait for JSON output
4. **Download**: Save your world data

### **Integrate with UE5**
1. **Find Generated Files**: Check `04-UE5-Integration/`
2. **Copy C++ Files**: Move to your UE5 project's Source folder
3. **Copy JSON Files**: Move to your UE5 project's Content/Data folder
4. **Compile**: Build your UE5 project

---

## 📁 **File Locations**

| What You Need | Where to Find It |
|---------------|------------------|
| **Web Interface** | `02-Web-Interface/` |
| **Core System** | `01-Core-System/` |
| **Generated Worlds** | `03-Generated-Worlds/json-data/` |
| **UE5 Code** | `04-UE5-Integration/` |
| **Documentation** | `05-Documentation/` |
| **Configuration** | `06-Configuration/` |

---

## 🎯 **Common Tasks**

### **Generate a New World**
```bash
# Method 1: Web Interface
# Open http://localhost:5000 and use the UI

# Method 2: Command Line
cd "01-Core-System/prompt-parser"
python prompt_parser.py "Your prompt here"
```

### **Create UE5 Code**
```bash
cd "01-Core-System/world-generator"
python generator.py "path/to/your/world.json" -w YourWorldName
```

### **View Documentation**
```bash
# Open any of these files:
# 05-Documentation/user-guides/README.md
# 05-Documentation/user-guides/WEB_README.md
# 05-Documentation/user-guides/GENERATOR_README.md
```

---

## 🔧 **System Requirements**

- **Python 3.7+**
- **Flask** (for web interface)
- **Requests** (for Ollama integration)
- **PyYAML** (for YAML support)
- **Optional: Ollama** (for enhanced AI generation)

---

## 🎓 **Learning Path**

### **Beginner (5 minutes)**
1. Use web interface to generate a world
2. Download the JSON file
3. Explore the generated data

### **Intermediate (15 minutes)**
1. Try command line generation
2. Examine the generated UE5 code
3. Read the integration guide

### **Advanced (30 minutes)**
1. Set up Ollama for enhanced generation
2. Integrate generated code with UE5
3. Customize the system for your needs

---

## 🆘 **Troubleshooting**

### **Web Interface Won't Start**
```bash
# Install dependencies
pip install Flask Flask-CORS requests PyYAML

# Try alternative startup
cd "02-Web-Interface/backend"
python app.py
```

### **Generation Fails**
- Check `03-Generated-Worlds/json-data/` for output
- Try simpler prompts first
- Check console for error messages

### **UE5 Integration Issues**
- Read `05-Documentation/integration-guides/`
- Ensure all files are copied correctly
- Check UE5 compilation logs

---

## 🎉 **You're Ready!**

**Your TTG Genesis system is organized and ready to use!**

- **Generate worlds** with simple text prompts
- **Create UE5 code** automatically
- **Build games** faster than ever

**Start with the web interface and explore from there!** 🌟

---

## 📞 **Need Help?**

- **Documentation**: Check `05-Documentation/`
- **Examples**: Look in `07-Examples/`
- **Configuration**: See `06-Configuration/`

**Happy World Building!** 🎮
