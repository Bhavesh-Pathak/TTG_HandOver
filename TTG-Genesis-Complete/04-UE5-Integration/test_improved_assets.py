#!/usr/bin/env python3
"""
Test script to verify improved UE5 asset generation
"""

import os
import sys
from pathlib import Path

# Add the UE5 integration to path
sys.path.append(str(Path(__file__).parent))

from ue5_world_generator import UE5WorldGenerator

def test_improved_asset_generation():
    """Test the improved asset generation"""
    
    print("🧪 Testing Improved UE5 Asset Generation")
    print("=" * 50)
    
    # Initialize the world generator
    generator = UE5WorldGenerator()
    
    # Create test world data
    test_world_data = {
        'name': 'Test_Magical_Forest',
        'description': 'A magical forest with fairy NPCs and crystal quests',
        'theme': 'fantasy',
        'difficulty': 'medium',
        'estimated_playtime': '30 minutes',
        'npcs': [
            {
                'name': 'Village Elder',
                'type': 'friendly',
                'health': 100,
                'level': 5,
                'faction': 'village',
                'quest_giver': True,
                'dialogue': ['Welcome, young adventurer!', 'I have a quest for you.'],
                'location': {'x': 0, 'y': 0, 'z': 0}
            },
            {
                'name': 'Fairy Merchant',
                'type': 'friendly',
                'health': 50,
                'level': 3,
                'faction': 'fairy',
                'merchant': True,
                'dialogue': ['Welcome to my shop!', 'I have magical items for sale.'],
                'location': {'x': 200, 'y': 100, 'z': 0}
            }
        ],
        'quests': [
            {
                'name': 'Crystal Collection',
                'type': 'main',
                'objective': 'Collect 5 magical crystals',
                'description': 'The village needs magical crystals to power their defenses',
                'rewards': {'experience': 100, 'gold': 50},
                'location': {'x': 300, 'y': 200, 'z': 0}
            },
            {
                'name': 'Fairy Rescue',
                'type': 'side',
                'objective': 'Rescue a trapped fairy',
                'description': 'A fairy is trapped in a spider web',
                'rewards': {'experience': 50, 'gold': 25},
                'location': {'x': 500, 'y': 300, 'z': 0}
            }
        ],
        'environment': {
            'type': 'forest',
            'lighting': 'dynamic_lighting',
            'weather': 'clear',
            'atmosphere': 'magical',
            'size': 'medium',
            'assets': ['trees', 'bushes', 'rocks', 'flowers', 'mushrooms']
        }
    }
    
    # Create a test world folder
    test_folder = Path(__file__).parent / "test_world"
    test_folder.mkdir(exist_ok=True)
    
    print(f"📁 Test folder: {test_folder}")
    
    # Test Blueprint asset generation
    print("\n🔧 Testing Blueprint Asset Generation...")
    blueprints_folder = test_folder / "Blueprints"
    blueprints_folder.mkdir(exist_ok=True)
    
    # Test NPC Blueprint generation
    generator.create_npc_blueprint_uasset_embedded(blueprints_folder, test_world_data, "TestWorld")
    
    # Test GameMode Blueprint generation
    generator.create_gamemode_blueprint_uasset_embedded(blueprints_folder, test_world_data, "TestWorld")
    
    # Test Quest Blueprint generation
    generator.create_quest_blueprint_uasset_embedded(blueprints_folder, test_world_data, "TestWorld")
    
    # Test Level asset generation
    print("\n🗺️ Testing Level Asset Generation...")
    level_data = generator.create_ue5_level_asset(test_world_data, "TestWorld", "TestLevel")
    
    level_file = test_folder / "TestLevel.umap"
    with open(level_file, 'wb') as f:
        f.write(level_data)
    
    # Check file sizes
    print("\n📊 Asset File Size Analysis:")
    print("-" * 40)
    
    for file_path in blueprints_folder.glob("*.uasset"):
        file_size = file_path.stat().st_size
        print(f"📄 {file_path.name}: {file_size:,} bytes ({file_size/1024:.1f} KB)")
        
        if file_size < 1024:
            print(f"   ⚠️  WARNING: File too small ({file_size} bytes)")
        elif file_size < 4096:
            print(f"   ⚠️  WARNING: File may be too small ({file_size} bytes)")
        else:
            print(f"   ✅ Good size ({file_size} bytes)")
    
    # Check level file size
    level_size = level_file.stat().st_size
    print(f"🗺️ {level_file.name}: {level_size:,} bytes ({level_size/1024:.1f} KB)")
    
    if level_size < 10240:  # 10KB
        print(f"   ⚠️  WARNING: Level file too small ({level_size} bytes)")
    elif level_size < 51200:  # 50KB
        print(f"   ⚠️  WARNING: Level file may be too small ({level_size} bytes)")
    else:
        print(f"   ✅ Good level size ({level_size} bytes)")
    
    # Test asset content
    print("\n🔍 Testing Asset Content...")
    
    for file_path in blueprints_folder.glob("*.uasset"):
        print(f"\n📄 Analyzing {file_path.name}:")
        
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Check for UE5 signature
        if b'UE5' in content[:100] or b'UNREAL' in content[:100]:
            print("   ✅ Contains UE5 signature")
        else:
            print("   ❌ Missing UE5 signature")
        
        # Check for embedded data
        if b'Properties' in content or b'EmbeddedData' in content:
            print("   ✅ Contains embedded data")
        else:
            print("   ❌ Missing embedded data")
        
        # Check for JSON content
        if b'{' in content and b'}' in content:
            print("   ✅ Contains JSON data")
        else:
            print("   ❌ Missing JSON data")
    
    print("\n🎉 Asset Generation Test Complete!")
    print(f"📁 Generated assets in: {test_folder}")
    
    return True

if __name__ == "__main__":
    test_improved_asset_generation()

