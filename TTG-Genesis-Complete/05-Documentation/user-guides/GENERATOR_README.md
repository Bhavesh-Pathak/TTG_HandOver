# 🎮 TTG Genesis - UE5 Code Generator

**Transform JSON game world data into production-ready Unreal Engine 5 C++ and Blueprint code**

## ✨ Features

- 🔧 **Complete C++ System**: Quest, NPC, Environment, and Player Controller classes
- 📋 **Blueprint Integration**: JSON data files compatible with UE5 Blueprints
- 🔌 **VaRest Support**: Plugin-compatible data structures
- 📦 **Module System**: Full UE5 module with Build.cs configuration
- 📖 **Integration Guide**: Comprehensive README with usage examples
- 🚀 **Batch Processing**: Generate multiple worlds at once

## 🚀 Quick Start

### Method 1: From JSON File
```bash
# Generate from existing JSON world data
python ttg-genesis/bhiv-core/generator.py ue5_exports/your_world.json -w YourWorldName

# Auto-detect world name from JSON
python ttg-genesis/bhiv-core/generator.py ue5_exports/your_world.json
```

### Method 2: From Prompt (Direct)
```bash
# Generate directly from a prompt
python ttg-genesis/bhiv-core/generator.py "Create a space station with alien NPCs" -p -w SpaceStation
```

### Method 3: Batch Processing
```bash
# Process all JSON files in a directory
python ttg-genesis/bhiv-core/generator.py ue5_exports/ -b
```

## 📁 Generated Files

### C++ Files (`ue5-c++/`)
- **QuestSystem.h/.cpp** - Complete quest management system with Blueprint integration
- **NPCSystem.h/.cpp** - NPC spawning, interaction, and behavior system
- **Environment.h/.cpp** - Environment configuration and world settings
- **PlayerController.h/.cpp** - Player controller with custom abilities
- **Module.h/.cpp** - UE5 module definition and lifecycle
- **Build.cs** - Module build configuration

### Blueprint Data (`ue5-exports/`)
- **QuestData.json** - Quest system data for Blueprint consumption
- **NPCData.json** - NPC spawning and behavior data
- **EnvironmentData.json** - Environment configuration
- **AssetList.json** - Required assets for the world
- **WorldData_VaRest.json** - VaRest plugin compatible format

### Documentation
- **UE5_Integration_README.md** - Complete integration guide with examples

## 🎯 Generated C++ Features

### Quest System
```cpp
// Quest management with Blueprint events
UFUNCTION(BlueprintCallable, Category = "Quest System")
bool StartQuest(const FString& QuestID);

UFUNCTION(BlueprintCallable, Category = "Quest System")
bool CompleteQuest(const FString& QuestID);

// Blueprint events
UPROPERTY(BlueprintAssignable, Category = "Quest System")
FOnQuestStarted OnQuestStarted;
```

### NPC System
```cpp
// NPC interaction and dialogue
UFUNCTION(BlueprintCallable, Category = "NPC")
FString GetCurrentDialogue();

UFUNCTION(BlueprintCallable, Category = "NPC")
void StartInteraction(AActor* InteractingActor);

// Blueprint events
UFUNCTION(BlueprintImplementableEvent, Category = "NPC")
void OnInteractionStarted(AActor* InteractingActor);
```

### Environment System
```cpp
// Environment configuration
UFUNCTION(BlueprintCallable, Category = "Environment")
void LoadEnvironmentFromJSON();

UFUNCTION(BlueprintCallable, Category = "Environment")
void ApplyEnvironmentSettings();
```

## 🔧 UE5 Integration

### 1. C++ Integration
1. Copy all `.h` and `.cpp` files to your UE5 project's `Source/` folder
2. Copy the `.Build.cs` file to your module directory
3. Add the module to your `.uproject` file:
```json
"Modules": [
    {
        "Name": "YourWorldName",
        "Type": "Runtime",
        "LoadingPhase": "Default"
    }
]
```
4. Regenerate project files and compile

### 2. Blueprint Integration
1. Copy JSON files to `Content/Data/` folder
2. Create Blueprint classes inheriting from generated C++ classes
3. Use Blueprint events for custom logic

### 3. VaRest Integration
Use `WorldData_VaRest.json` with VaRest plugin for dynamic data loading

## 📊 Example Output

### Generated for "Magical Forest Temple"
```
✅ Generated 17 files:
📄 MagicalForestQuestSystem.h/cpp - 5 quests with rewards
📄 MagicalForestNPCSystem.h/cpp - 2 NPCs with dialogue
📄 MagicalForestEnvironment.h/cpp - Forest environment
📄 MagicalForestPlayerController.h/cpp - Magic abilities
📄 QuestData.json - Blueprint-ready quest data
📄 NPCData.json - NPC spawning data
📄 AssetList.json - Required models, textures, sounds
```

## 🎮 Usage Examples

### Command Line Options
```bash
# Basic usage
python generator.py world.json

# Custom world name
python generator.py world.json -w MyWorld

# Custom output directory
python generator.py world.json -o /path/to/output

# From prompt
python generator.py "Create a desert temple" -p

# Batch processing
python generator.py json_folder/ -b
```

### Programmatic Usage
```python
from generator import UE5CodeGenerator, generate_ue5_files_from_json

# Generate from JSON file
files = generate_ue5_files_from_json("world.json", "MyWorld")

# Generate from prompt
files = generate_ue5_files_from_prompt("Create a space station", "SpaceWorld")

# Custom generator
generator = UE5CodeGenerator("./output")
files = generator.generate_all(json_data, "WorldName")
```

## 🔍 Generated Code Quality

- ✅ **UE5 Standards**: Follows official UE5 C++ coding conventions
- ✅ **Blueprint Compatible**: All classes expose Blueprint functions
- ✅ **Memory Safe**: Proper UPROPERTY usage and garbage collection
- ✅ **Modular**: Clean separation of concerns
- ✅ **Extensible**: Easy to modify and extend generated code
- ✅ **Production Ready**: Includes error handling and logging

## 🚀 Advanced Features

### Batch Processing
Process multiple worlds at once:
```bash
python generator.py ue5_exports/ -b
```

### Custom Templates
The generator uses intelligent templates that adapt to your world data:
- Quest types automatically determine C++ enums
- NPC behaviors generate appropriate interaction code
- Environment types influence lighting and atmosphere code
- Player abilities create corresponding controller functions

### VaRest Integration
Generated `WorldData_VaRest.json` includes:
- Structured data for easy Blueprint parsing
- Metadata for version tracking
- Compatible format for HTTP requests

## 🎯 Perfect for

- **Rapid Prototyping**: Generate complete game systems in seconds
- **Game Jams**: Quick world creation with full UE5 integration
- **Learning**: Study well-structured UE5 C++ code
- **Production**: Use as base for complex game systems
- **Automation**: Integrate into CI/CD pipelines

## 🎉 Ready to Generate!

Transform your game world ideas into production-ready UE5 code with a single command!

**Happy Coding! 🚀**
