#!/usr/bin/env python3
"""
Test script to demonstrate JSON-to-C++ generation system
"""

import requests
import json
import time
import os
from pathlib import Path

def test_json_to_cpp_generation():
    """Test the complete JSON-to-C++ generation pipeline"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing TTG Genesis JSON-to-C++ Generation System")
    print("=" * 70)
    
    # Step 1: Generate JSON Data for Alien City
    print("📝 Step 1: Generating JSON Data for Alien City...")
    
    json_payload = {
        "prompt": "Create a Alien City where you have to defeat aliens to complete the quest",
        "options": {
            "includeNPCs": True,
            "includeQuests": True,
            "includeEnvironment": True,
            "includeCombat": True
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/generate-json", json=json_payload)
        
        if response.status_code == 200:
            json_result = response.json()
            print("✅ JSON Generation Successful!")
            
            world_data = json_result.get('world_data', {})
            world_id = json_result.get('world_id')
            
            print(f"🌍 World: {world_data.get('name')}")
            print(f"🎨 Theme: {world_data.get('theme')}")
            print(f"👥 NPCs: {len(world_data.get('npcs', []))}")
            print(f"⚔️ Quests: {len(world_data.get('quests', []))}")
            
            # Display the JSON structure
            print("\n📄 Generated JSON Structure:")
            print("=" * 50)
            print(json.dumps(world_data, indent=2))
            print("=" * 50)
            
        else:
            print(f"❌ JSON Generation Failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ JSON Generation Error: {e}")
        return
    
    print("\n" + "=" * 70)
    
    # Step 2: Create UE5 Project with C++ Classes
    print("🎮 Step 2: Creating UE5 Project with C++ Classes from JSON...")
    
    ue5_payload = {
        "world_id": world_id,
        "ue5_options": {
            "generateProjectFiles": False,
            "compileProject": False
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/create-ue5-project", json=ue5_payload)
        
        if response.status_code == 200:
            ue5_result = response.json()
            print("✅ UE5 Project Creation Successful!")
            print(f"📁 Project: {ue5_result.get('message')}")
            
            # Check generated C++ files
            check_generated_cpp_files(world_data)
            
        else:
            print(f"❌ UE5 Project Creation Failed: {response.text}")
            
    except Exception as e:
        print(f"❌ UE5 Project Creation Error: {e}")
    
    print("\n" + "=" * 70)
    print("🧪 JSON-to-C++ Test Complete!")

def check_generated_cpp_files(world_data):
    """Check if C++ files were generated correctly"""
    
    world_name = world_data.get('name', 'Generated World')
    safe_name = world_name.replace(' ', '').replace('-', '')
    
    # Expected project path
    project_path = Path("../../../TTG-Generated-UE5-Projects") / f"TTG_{safe_name}"
    source_path = project_path / "Source" / "TTGWorldGenerator" / "Worlds" / safe_name
    
    print(f"\n🔍 Checking Generated C++ Files in: {source_path}")
    print("-" * 50)
    
    if not source_path.exists():
        print(f"⚠️ Source folder not found: {source_path}")
        return
    
    # Check for generated files
    expected_files = [
        f"{safe_name}BaseNPC.h",
        f"{safe_name}BaseNPC.cpp",
        f"{safe_name}QuestSystem.h",
        f"{safe_name}WorldManager.h",
        f"{safe_name}Environment.h",
        f"{safe_name}GameMode.h",
        f"{safe_name}DataStructures.h"
    ]
    
    # Check for specific NPC classes
    npcs = world_data.get('npcs', [])
    for i, npc in enumerate(npcs):
        if isinstance(npc, dict):
            npc_name = npc.get('name', f'NPC_{i}').replace(' ', '').replace('-', '')
            expected_files.extend([
                f"{safe_name}{npc_name}NPC.h",
                f"{safe_name}{npc_name}NPC.cpp"
            ])
    
    print("📋 Expected C++ Files:")
    for file_name in expected_files:
        file_path = source_path / file_name
        if file_path.exists():
            print(f"  ✅ {file_name}")
            
            # Show file size and first few lines
            file_size = file_path.stat().st_size
            print(f"     📊 Size: {file_size} bytes")
            
            if file_name.endswith('.h'):
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()[:5]
                        print(f"     📄 Preview: {lines[0].strip() if lines else 'Empty'}")
                except:
                    pass
        else:
            print(f"  ❌ {file_name} - NOT FOUND")
    
    print("\n🎯 JSON-to-C++ Mapping Analysis:")
    print("-" * 30)
    
    # Analyze NPCs
    npcs = world_data.get('npcs', [])
    print(f"👥 NPCs in JSON: {len(npcs)}")
    for i, npc in enumerate(npcs):
        if isinstance(npc, dict):
            npc_name = npc.get('name', f'NPC_{i}')
            npc_type = npc.get('type', 'friendly')
            dialogue_count = len(npc.get('dialogue', []))
            print(f"  🧙‍♀️ {npc_name} ({npc_type}) - {dialogue_count} dialogue lines")
            print(f"     → Generated: {safe_name}{npc_name.replace(' ', '')}NPC.h/.cpp")
    
    # Analyze Quests
    quests = world_data.get('quests', [])
    print(f"\n⚔️ Quests in JSON: {len(quests)}")
    for i, quest in enumerate(quests):
        if isinstance(quest, dict):
            quest_name = quest.get('name', f'Quest_{i}')
            objectives = len(quest.get('objectives', []))
            rewards = len(quest.get('rewards', []))
            print(f"  🎯 {quest_name} - {objectives} objectives, {rewards} rewards")
    print(f"     → Generated: {safe_name}QuestSystem.h")
    
    # Analyze Environment
    environment = world_data.get('environment', {})
    theme = world_data.get('theme', 'unknown')
    print(f"\n🌍 Environment: {theme}")
    print(f"     → Generated: {safe_name}Environment.h")
    print(f"     → Generated: {safe_name}WorldManager.h")
    print(f"     → Generated: {safe_name}GameMode.h")

if __name__ == "__main__":
    test_json_to_cpp_generation()
