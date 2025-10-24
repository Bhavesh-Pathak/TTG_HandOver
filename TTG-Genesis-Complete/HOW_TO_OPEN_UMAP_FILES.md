# 🗺️ How to Open .umap Files in UE5 - Complete Guide

## 📁 Step 1: Locate Your Generated Project

After generating a world with TTG Genesis, your project will be located at:
```
TTG-Generated-UE5-Projects/
└── TTG_YourWorldName/
    ├── YourWorldName.uproject          # ← Double-click this file
    ├── Content/
    │   └── TTGWorlds/
    │       └── YourWorldName/
    │           ├── Blueprints/
    │           │   ├── BP_YourWorldNPC_*.uasset
    │           │   ├── BP_YourWorldQuestManager.uasset
    │           │   └── BP_YourWorldWorldManager.uasset
    │           └── YourWorldName_Level.umap    # ← Your level file
    └── Source/
        └── C++ classes...
```

## 🎮 Step 2: Open Project in UE5

### Method 1: Double-Click (Recommended)
1. Navigate to `TTG-Generated-UE5-Projects/TTG_YourWorldName/`
2. **Double-click** the `.uproject` file (e.g., `YourWorldName.uproject`)
3. UE5 will automatically launch and open your project

### Method 2: Through Epic Games Launcher
1. Open Epic Games Launcher
2. Go to **Unreal Engine** tab
3. Click **Launch** next to UE5 5.6
4. In UE5: **File → Open Project**
5. Navigate to your `.uproject` file and open it

### Method 3: Through UE5 Recent Projects
1. Launch UE5 5.6
2. Your project should appear in **Recent Projects**
3. Click on it to open

## ⚙️ Step 3: Compile C++ Code

**IMPORTANT**: You must compile the C++ code before opening the level!

1. Once the project opens in UE5, you'll see a notification about C++ code
2. Click **"Yes"** to compile, or go to **Build → Compile**
3. Wait for compilation to complete (may take 2-5 minutes)
4. You'll see "Compilation Successful" when done

## 🗺️ Step 4: Open the .umap Level File

### In Content Browser:
1. In UE5, look at the **Content Browser** (bottom panel)
2. Navigate to: `Content → TTGWorlds → YourWorldName`
3. You'll see your level file: `YourWorldName_Level.umap`
4. **Double-click** the `.umap` file to open the level

### Alternative Navigation:
1. Use the folder tree on the left side of Content Browser
2. Expand: `Content → TTGWorlds → YourWorldName`
3. Double-click the level file

## ✅ Step 5: Verify Everything Works

### Check Content Browser:
- ✅ You should see `.uasset` Blueprint files (not DataTables!)
- ✅ You should see the `.umap` level file
- ✅ No unwanted JSON DataTable imports

### Test the Level:
1. With the level open, click the **Play** button (▶️) in the toolbar
2. Your character should spawn in the generated world
3. NPCs and quest systems should be functional

## 🚨 Troubleshooting

### Problem: "Missing Modules" Error
**Solution**: 
1. Right-click the `.uproject` file
2. Select **"Generate Visual Studio project files"**
3. Open the generated `.sln` file in Visual Studio
4. Build the project (Build → Build Solution)
5. Then open the `.uproject` file

### Problem: Level Appears Empty
**Solution**:
1. Make sure you compiled the C++ code first
2. Check that you're opening the correct `.umap` file
3. Verify the Blueprint assets are present in Content Browser

### Problem: DataTable Import Errors
**Solution**: 
- This shouldn't happen with the new embedded system
- If it does, delete any JSON files from the Content folder
- The system now embeds all data in .uasset files

### Problem: Can't Find the Level File
**Solution**:
1. In Content Browser, click the **View Options** (eye icon)
2. Make sure **"Show Engine Content"** is unchecked
3. Use the search box to search for your world name
4. Check the correct folder path: `Content/TTGWorlds/YourWorldName/`

## 🎯 Quick Reference

| File Type | Purpose | Location |
|-----------|---------|----------|
| `.uproject` | Project file - double-click to open | Root folder |
| `.umap` | Level file - contains your world | `Content/TTGWorlds/YourWorldName/` |
| `.uasset` | Blueprint assets - NPCs, quests, etc. | `Content/TTGWorlds/YourWorldName/Blueprints/` |
| `.cpp/.h` | C++ source code | `Source/YourWorldName/` |

## 🌟 Success Indicators

When everything is working correctly:
- ✅ Project opens without errors
- ✅ C++ code compiles successfully  
- ✅ Level file opens and displays the world
- ✅ Blueprint assets are visible (not DataTables)
- ✅ Play mode works with NPCs and quests
- ✅ No JSON import errors

## 💡 Pro Tips

1. **Always compile C++ first** before opening levels
2. **Use the search** in Content Browser to quickly find files
3. **Save your level** after making changes (Ctrl+S)
4. **Check the Output Log** (Window → Developer Tools → Output Log) for any errors
5. **Use Play mode** to test your world immediately

Your TTG Genesis world is now ready to explore and develop further! 🎮✨
