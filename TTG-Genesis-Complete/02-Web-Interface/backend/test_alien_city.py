#!/usr/bin/env python3
"""
Test script to reproduce the alien city generation issue
"""

import requests
import json
import time

def test_alien_city_generation():
    """Test the exact same flow as the UI"""
    
    base_url = "http://localhost:5000"
    
    print("🧪 Testing TTG Genesis Alien City Generation")
    print("=" * 60)
    
    # Step 1: Generate JSON Data (same as UI)
    print("📝 Step 1: Generating JSON Data...")
    
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
        print(f"JSON Generation Response Status: {response.status_code}")
        
        if response.status_code == 200:
            json_result = response.json()
            print("✅ JSON Generation Successful!")
            print(f"World ID: {json_result.get('world_id')}")
            print(f"World Name: {json_result.get('world_data', {}).get('name')}")
            print(f"Theme: {json_result.get('world_data', {}).get('theme')}")
            print(f"NPCs: {len(json_result.get('world_data', {}).get('npcs', []))}")
            print(f"Quests: {len(json_result.get('world_data', {}).get('quests', []))}")
            
            # Print the actual JSON structure
            print("\n📄 Generated JSON Structure:")
            print(json.dumps(json_result.get('world_data', {}), indent=2))
            
            world_id = json_result.get('world_id')
            
        else:
            print(f"❌ JSON Generation Failed: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ JSON Generation Error: {e}")
        return
    
    print("\n" + "=" * 60)
    
    # Step 2: Create UE5 Project (same as UI)
    print("🎮 Step 2: Creating UE5 Project...")
    
    ue5_payload = {
        "world_id": world_id,
        "ue5_options": {
            "generateProjectFiles": False,
            "compileProject": False
        }
    }
    
    try:
        response = requests.post(f"{base_url}/api/create-ue5-project", json=ue5_payload)
        print(f"UE5 Creation Response Status: {response.status_code}")
        
        if response.status_code == 200:
            ue5_result = response.json()
            print("✅ UE5 Project Creation Successful!")
            print(f"Message: {ue5_result.get('message')}")
            
        else:
            print(f"❌ UE5 Project Creation Failed: {response.text}")
            ue5_result = response.json()
            print(f"Error Details: {ue5_result.get('error')}")
            
    except Exception as e:
        print(f"❌ UE5 Project Creation Error: {e}")
        return
    
    print("\n" + "=" * 60)
    print("🧪 Test Complete!")

if __name__ == "__main__":
    test_alien_city_generation()
