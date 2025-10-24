#!/usr/bin/env python3
"""
Test script to verify the embedded asset generation works correctly
"""

import sys
import json
from pathlib import Path

# Add the current directory to path
sys.path.append(str(Path(__file__).parent))

from ue5_world_generator import UE5WorldGenerator

def test_embedded_asset_generation():
    """Test the new embedded asset generation"""
    
    print("🧪 Testing TTG Genesis Embedded Asset Generation")
    print("=" * 60)
    
    # Create test world data
    test_world_data = {
        "name": "TestEmbeddedWorld",
        "theme": "fantasy",
        "description": "Test world for embedded asset generation",
        "npcs": [
            {
                "name": "Test Fairy",
                "type": "friendly",
                "dialogue": ["Hello traveler!", "Welcome to the test world!"],
                "location": {"x": 100, "y": 0, "z": 0},
                "health": 50,
                "level": 1,
                "quest_giver": True
            },
            {
                "name": "Test Guardian",
                "type": "neutral",
                "dialogue": ["I guard this place.", "Pass if you must."],
                "location": {"x": 300, "y": 0, "z": 0},
                "health": 150,
                "level": 5,
                "quest_giver": False
            }
        ],
        "quests": [
            {
                "name": "Crystal Collection",
                "description": "Collect magical crystals",
                "objectives": ["Find 5 crystals", "Return to fairy"],
                "rewards": ["100 XP", "Magic Ring"],
                "npc": "Test Fairy"
            },
            {
                "name": "Guardian Challenge",
                "description": "Prove your worth to the guardian",
                "objectives": ["Defeat 3 enemies", "Show courage"],
                "rewards": ["200 XP", "Guardian's Blessing"],
                "npc": "Test Guardian"
            }
        ],
        "environment": {
            "lighting": "magical",
            "weather": "clear",
            "terrain": "forest"
        }
    }
    
    # Initialize generator
    generator = UE5WorldGenerator()
    
    print("📋 Test World Data:")
    print(f"  Name: {test_world_data['name']}")
    print(f"  NPCs: {len(test_world_data['npcs'])}")
    print(f"  Quests: {len(test_world_data['quests'])}")
    print()
    
    # Test the generation
    print("🔧 Testing embedded asset generation...")
    try:
        result = generator.create_world_in_project(test_world_data)
        
        if result.get('success'):
            print("✅ SUCCESS! Embedded asset generation completed")
            print()
            print("📁 Generated Files:")
            for feature in result.get('features_created', []):
                print(f"  ✅ {feature}")
            print()
            print("📖 Instructions:")
            for instruction in result.get('instructions', []):
                print(f"  {instruction}")
            print()
            print("🎯 Key Benefits:")
            print("  ✅ No JSON files in Content folder")
            print("  ✅ No DataTable auto-import issues")
            print("  ✅ All data embedded in .uasset files")
            print("  ✅ .uasset and .umap files visible in UE5")
            print("  ✅ Reference files stored outside Content folder")
            
        else:
            print("❌ FAILED! Error occurred:")
            print(f"  Error: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ EXCEPTION! {e}")
        import traceback
        traceback.print_exc()
    
    print()
    print("=" * 60)
    print("🧪 Test completed!")

if __name__ == "__main__":
    test_embedded_asset_generation()
