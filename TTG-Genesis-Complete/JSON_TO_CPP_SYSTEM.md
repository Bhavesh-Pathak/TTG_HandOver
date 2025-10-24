# 🔧 TTG Genesis - JSON-to-C++ Generation System

## 🎯 **Overview**

The TTG Genesis system now automatically generates complete C++ header files, class files, and Blueprints directly from JSON data. This creates a comprehensive C++ foundation for your game world based on the intelligent prompt analysis.

## 🚀 **How It Works**

### **1. JSON Analysis → C++ Generation Pipeline**

```
User Prompt → LLM Analysis → JSON World Data → C++ Classes → UE5 Blueprints
```

1. **Prompt Analysis**: "Create a Alien City where you have to defeat aliens to complete the quest"
2. **JSON Generation**: Creates structured world data with NPCs, quests, environment
3. **C++ Generation**: Automatically creates C++ classes for each JSON element
4. **Blueprint Creation**: Generates UE5 Blueprints that use the C++ classes

### **2. Generated C++ Class Structure**

For an alien city world, the system generates:

#### **Base Classes**
- `AlienCityBaseNPC.h/.cpp` - Base NPC class with dialogue system
- `AlienCityQuestSystem.h` - Quest management system
- `AlienCityWorldManager.h` - World configuration and management
- `AlienCityEnvironment.h` - Environment and atmosphere control
- `AlienCityGameMode.h` - Game mode with world integration
- `AlienCityDataStructures.h` - Data structures from JSON

#### **Specific NPC Classes** (Generated per JSON NPC)
- `AlienCityAlienWarriorNPC.h/.cpp` - Enemy alien warrior
- `AlienCityAlienCommanderNPC.h/.cpp` - Boss alien commander  
- `AlienCityAlienInformantNPC.h/.cpp` - Friendly quest giver

## 📊 **JSON-to-C++ Mapping**

### **NPC JSON → C++ Class**

**JSON Input:**
```json
{
  "name": "Alien Warrior",
  "type": "enemy", 
  "dialogue": ["You shall not pass, human!", "Prepare for battle!"],
  "health": 150,
  "level": 3,
  "location": {"x": 200, "y": 0, "z": 0}
}
```

**Generated C++ Class:**
```cpp
// AlienCityAlienWarriorNPC.h
class TTGWORLDGENERATOR_API AAlienCityAlienWarriorNPC : public AAlienCityBaseNPC
{
    GENERATED_BODY()

public:
    AAlienCityAlienWarriorNPC();

protected:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specific NPC Data")
    FString SpecificNPCType; // "enemy"

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specific NPC Data")
    bool bIsHostile; // true

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Specific NPC Data")
    float AttackDamage; // 15.0f (calculated from health)

public:
    UFUNCTION(BlueprintCallable, Category = "NPC")
    virtual void StartDialogue() override;

    UFUNCTION(BlueprintCallable, Category = "NPC")
    void ExecuteNPCBehavior();
};
```

### **Quest JSON → C++ System**

**JSON Input:**
```json
{
  "name": "Alien Invasion Defense",
  "description": "Defeat the alien invaders to save the city",
  "objectives": ["Eliminate 5 alien warriors", "Defeat the alien commander"],
  "rewards": ["Plasma Rifle", "500 Credits", "Hero Badge"]
}
```

**Generated C++ Structure:**
```cpp
// AlienCityQuestSystem.h
USTRUCT(BlueprintType)
struct FAlienCityQuestData : public FTableRowBase
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest Data")
    FString QuestName; // "Alien Invasion Defense"

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest Data")
    FString QuestDescription; // "Defeat the alien invaders..."

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest Data")
    TArray<FString> Objectives; // ["Eliminate 5 alien warriors", ...]

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Quest Data")
    TArray<FString> Rewards; // ["Plasma Rifle", "500 Credits", ...]
};
```

## 🎮 **Generated Features**

### **1. NPC System**
- **Base NPC Class**: Common functionality for all NPCs
- **Specific NPC Classes**: Individual classes for each JSON NPC
- **Dialogue System**: Automatic dialogue management from JSON
- **Interaction System**: Sphere collision for player interaction
- **Behavior System**: Different behaviors based on NPC type (friendly/enemy)

### **2. Quest System**
- **Quest Data Structures**: UE5 data tables from JSON quest data
- **Quest Manager**: Centralized quest management system
- **Objective Tracking**: Automatic objective progression
- **Reward System**: Configurable rewards from JSON

### **3. World Management**
- **World Manager**: Coordinates all world systems
- **Environment System**: Manages world atmosphere and settings
- **Game Mode Integration**: Custom game mode for the generated world
- **Spawn System**: Automatic NPC spawning from JSON locations

### **4. Data Integration**
- **JSON Initialization**: All classes initialize from JSON data
- **Blueprint Integration**: C++ classes exposed to Blueprints
- **UE5 Data Tables**: Structured data for designers
- **Runtime Configuration**: Dynamic world setup

## 🔧 **Technical Implementation**

### **Class Generation Process**

1. **Analyze JSON Structure**: Extract NPCs, quests, environment data
2. **Generate Base Classes**: Create foundation classes for the world
3. **Generate Specific Classes**: Create individual classes for each JSON element
4. **Create Data Structures**: Generate UE5-compatible data structures
5. **Generate Blueprints**: Create Blueprint assets that use C++ classes

### **File Organization**

```
TTGWorldGenerator/
├── Source/
│   └── TTGWorldGenerator/
│       └── Worlds/
│           └── AlienCity/
│               ├── AlienCityBaseNPC.h/.cpp
│               ├── AlienCityAlienWarriorNPC.h/.cpp
│               ├── AlienCityAlienCommanderNPC.h/.cpp
│               ├── AlienCityQuestSystem.h
│               ├── AlienCityWorldManager.h
│               ├── AlienCityEnvironment.h
│               ├── AlienCityGameMode.h
│               └── AlienCityDataStructures.h
└── Content/
    └── TTGWorlds/
        └── AlienCity/
            ├── Blueprints/
            │   ├── BP_AlienCityAlienWarriorNPC.uasset
            │   ├── BP_AlienCityQuestSystem.uasset
            │   └── BP_AlienCityWorldManager.uasset
            └── AlienCity_Level.umap
```

## 🎯 **Benefits**

### **1. Complete C++ Foundation**
- Professional C++ classes following UE5 best practices
- Proper inheritance hierarchy
- Blueprint-exposed functionality
- UE5 reflection system integration

### **2. Automatic Code Generation**
- No manual C++ coding required
- Consistent code structure
- Proper naming conventions
- Complete documentation

### **3. JSON-Driven Development**
- Easy world modification through JSON
- Designer-friendly data structures
- Runtime configuration support
- Version control friendly

### **4. UE5 Integration**
- Native UE5 C++ classes
- Blueprint compatibility
- Data table integration
- Component-based architecture

## 🧪 **Testing Your System**

### **1. Generate Alien City**
```bash
cd TTG-Genesis-Complete/02-Web-Interface/backend
python test_json_to_cpp.py
```

### **2. Check Generated Files**
The test script will show:
- ✅ Generated C++ header files
- ✅ Generated C++ implementation files  
- ✅ JSON-to-C++ mapping analysis
- ✅ File sizes and previews

### **3. Open in UE5**
1. Navigate to `TTG-Generated-UE5-Projects/TTG_AlienCity/`
2. Open `TTG_AlienCity.uproject`
3. Compile C++ code (Build → Compile)
4. See your generated C++ classes in the C++ Classes folder
5. Use the generated Blueprints in your level

## 🎉 **Result**

Your JSON prompt "Create a Alien City where you have to defeat aliens to complete the quest" now generates:

- ✅ **Complete C++ class system** with proper inheritance
- ✅ **Individual NPC classes** for each alien type
- ✅ **Quest management system** with objectives and rewards
- ✅ **World management classes** for environment control
- ✅ **UE5 Blueprints** that use the C++ foundation
- ✅ **Working .umap level** ready to play

**Your alien city is now a complete, professional UE5 C++ project!** 🛸👽🎮
