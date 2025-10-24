#!/usr/bin/env python3
"""
TTG Genesis UE5 Server - Working Version
2-Step Generation: JSON -> UE 5.6.0 Project
"""

import os
import sys
import json
import uuid
from datetime import datetime
from pathlib import Path
from flask import Flask, request, jsonify

# Add UE5 integration to path
sys.path.append(str(Path(__file__).parent.parent.parent / "04-UE5-Integration"))

# Add prompt parser to path
sys.path.append(str(Path(__file__).parent.parent.parent / "01-Core-System" / "prompt-parser"))

try:
    from ue5_world_generator import UE5WorldGenerator
    UE5_AVAILABLE = True
    print("UE5 World Generator imported")
except ImportError:
    UE5_AVAILABLE = False
    print("UE5 World Generator not available")

# Import prompt parser for LLM-based world generation
try:
    from prompt_parser import PromptParser, OllamaConfig, validate_ollama_connection
    PROMPT_PARSER_AVAILABLE = True
    print("Prompt Parser imported")

    # Test Ollama connection
    if validate_ollama_connection():
        print("✅ Ollama LLM connection successful")
        OLLAMA_AVAILABLE = True
    else:
        print("⚠️ Ollama not available - will use intelligent fallback")
        OLLAMA_AVAILABLE = False

except ImportError as e:
    PROMPT_PARSER_AVAILABLE = False
    OLLAMA_AVAILABLE = False
    print(f"Prompt Parser not available: {e}")

app = Flask(__name__)

# Initialize UE5 world generator
ue5_generator = None
if UE5_AVAILABLE:
    ue5_generator = UE5WorldGenerator()
    print("UE5 World Generator initialized for UE 5.6.0")

# Initialize prompt parser for intelligent world generation
prompt_parser = None
if PROMPT_PARSER_AVAILABLE:
    try:
        config = OllamaConfig(model="llama3")  # Use llama3 for better results
        prompt_parser = PromptParser(config)
        print("Prompt Parser initialized with Llama3")
    except Exception as e:
        print(f"Failed to initialize prompt parser: {e}")

# Global cache
json_cache = {}

def generate_intelligent_world_data(prompt: str, options: dict) -> dict:
    """Generate world data using LLM analysis or intelligent fallback"""

    # Try LLM-based generation first
    if prompt_parser and OLLAMA_AVAILABLE:
        try:
            print(f"🤖 Using LLM to analyze prompt: {prompt}")
            llm_data = prompt_parser.parse_prompt(prompt)

            # Convert LLM format to our expected format
            world_data = convert_llm_to_world_data(llm_data, prompt, options)
            print("✅ LLM-based world generation successful")
            return world_data

        except Exception as e:
            print(f"⚠️ LLM generation failed: {e}, using intelligent fallback")

    # Intelligent fallback - analyze prompt keywords
    print(f"🧠 Using intelligent analysis for prompt: {prompt}")
    return analyze_prompt_intelligently(prompt, options)

def convert_llm_to_world_data(llm_data: dict, prompt: str, options: dict) -> dict:
    """Convert LLM-generated data to our world data format"""

    print(f"🔄 Converting LLM data to UE5 format...")
    print(f"🔍 LLM data keys: {list(llm_data.keys())}")

    world_id = str(uuid.uuid4())
    metadata = llm_data.get('metadata', {})

    # Convert complex LLM NPCs to simple format
    simple_npcs = []
    if options.get('includeNPCs') and llm_data.get('npcs'):
        for i, npc in enumerate(llm_data['npcs']):
            if isinstance(npc, dict):
                simple_npc = {
                    'name': npc.get('name', f'NPC_{i}'),
                    'type': npc.get('type', 'friendly'),
                    'dialogue': npc.get('dialogue', ['Hello!', 'How can I help?']),
                    'location': {'x': i * 200, 'y': 0, 'z': 0},  # Simple location
                    'health': npc.get('stats', {}).get('health', 100),
                    'level': 1
                }
                simple_npcs.append(simple_npc)
                print(f"✅ Converted NPC: {simple_npc['name']} ({simple_npc['type']})")

    # Convert complex LLM quests to simple format
    simple_quests = []
    if options.get('includeQuests') and llm_data.get('quests'):
        for i, quest in enumerate(llm_data['quests']):
            if isinstance(quest, dict):
                # Extract rewards properly
                rewards = []
                if isinstance(quest.get('rewards'), dict):
                    reward_obj = quest['rewards']
                    if reward_obj.get('gold'):
                        rewards.append(f"{reward_obj['gold']} Gold")
                    if reward_obj.get('experience'):
                        rewards.append(f"{reward_obj['experience']} XP")
                    if reward_obj.get('items'):
                        rewards.extend(reward_obj['items'])
                elif isinstance(quest.get('rewards'), list):
                    rewards = quest['rewards']

                simple_quest = {
                    'name': quest.get('name', f'Quest_{i}'),
                    'description': quest.get('description', 'Complete this quest'),
                    'objectives': [quest.get('objective', 'Complete objective')],
                    'rewards': rewards if rewards else ['Experience']
                }
                simple_quests.append(simple_quest)
                print(f"✅ Converted Quest: {simple_quest['name']}")

    # Override theme detection - analyze the original prompt
    prompt_lower = prompt.lower()
    theme_analysis = analyze_theme(prompt_lower, prompt_lower.split())
    detected_theme = theme_analysis['type']

    world_data = {
        'id': world_id,
        'name': metadata.get('level_name', llm_data.get('name', 'Generated World')),
        'description': prompt,
        'theme': detected_theme,  # Use our theme detection instead of LLM's
        'created_at': datetime.now().isoformat(),
        'environment': llm_data.get('environment', {}),
        'npcs': simple_npcs,
        'quests': simple_quests,
        'physics': llm_data.get('physics', {}),
        'metadata': metadata
    }

    print(f"✅ Converted to simple format: {len(simple_npcs)} NPCs, {len(simple_quests)} quests")
    return world_data

def analyze_prompt_intelligently(prompt: str, options: dict) -> dict:
    """Intelligent prompt analysis without LLM"""

    prompt_lower = prompt.lower()
    words = prompt_lower.split()

    # Analyze theme/environment
    theme_analysis = analyze_theme(prompt_lower, words)

    # Generate world name from prompt
    world_name = generate_world_name(prompt, theme_analysis['type'])

    world_id = str(uuid.uuid4())

    world_data = {
        'id': world_id,
        'name': world_name,
        'description': prompt,
        'theme': theme_analysis['type'],
        'created_at': datetime.now().isoformat(),
        'environment': theme_analysis
    }

    # Add NPCs based on prompt analysis
    if options.get('includeNPCs'):
        world_data['npcs'] = generate_contextual_npcs(prompt_lower, theme_analysis['type'])

    # Add quests based on prompt analysis
    if options.get('includeQuests'):
        world_data['quests'] = generate_contextual_quests(prompt_lower, theme_analysis['type'])

    return world_data

def analyze_theme(prompt_lower: str, words: list = None) -> dict:
    """Analyze the theme/environment from prompt"""

    # Theme detection with priority order (more specific themes first)
    theme_keywords = {
        'alien': ['alien', 'extraterrestrial', 'ufo', 'space', 'sci-fi', 'futuristic', 'cyberpunk', 'martian', 'galactic'],
        'horror': ['horror', 'scary', 'haunted', 'ghost', 'zombie', 'dark', 'spooky'],
        'medieval': ['medieval', 'castle', 'knight', 'dragon', 'sword', 'kingdom', 'fortress'],
        'underwater': ['underwater', 'ocean', 'sea', 'submarine', 'coral', 'aquatic'],
        'arctic': ['arctic', 'ice', 'snow', 'frozen', 'cold', 'winter', 'tundra'],
        'desert': ['desert', 'sand', 'oasis', 'pyramid', 'dune', 'sahara'],
        'fantasy': ['magic', 'wizard', 'fairy', 'forest', 'crystal', 'magical', 'enchanted'],
        'modern': ['city', 'urban', 'modern', 'street', 'building', 'car', 'metropolitan']
    }

    detected_theme = 'fantasy'  # default

    # Check themes in priority order
    for theme, keywords in theme_keywords.items():
        if any(keyword in prompt_lower for keyword in keywords):
            detected_theme = theme
            print(f"🎯 Detected theme: {detected_theme} (found keywords: {[kw for kw in keywords if kw in prompt_lower]})")
            break

    return {
        'type': detected_theme,
        'atmosphere': 'mysterious' if 'dark' in prompt_lower else 'adventurous',
        'size': 'large' if any(word in prompt_lower for word in ['big', 'large', 'huge', 'massive']) else 'medium'
    }

def generate_world_name(prompt: str, theme: str) -> str:
    """Generate a world name from the prompt"""
    words = prompt.split()[:4]  # Take first 4 words
    name_words = [word.capitalize() for word in words if word.isalpha()]
    if name_words:
        return ' '.join(name_words)
    else:
        return f"{theme.capitalize()} World"

def generate_contextual_npcs(prompt_lower: str, theme: str) -> list:
    """Generate NPCs based on prompt and theme"""

    npcs = []

    if theme == 'alien':
        if 'defeat' in prompt_lower or 'fight' in prompt_lower or 'battle' in prompt_lower:
            npcs.extend([
                {
                    'name': 'Alien Warrior',
                    'type': 'enemy',
                    'dialogue': ['You shall not pass, human!', 'Prepare for battle!'],
                    'location': {'x': 200, 'y': 0, 'z': 0},
                    'health': 150,
                    'level': 3
                },
                {
                    'name': 'Alien Commander',
                    'type': 'enemy',
                    'dialogue': ['I am the commander of this sector!', 'You will be eliminated!'],
                    'location': {'x': 500, 'y': 0, 'z': 0},
                    'health': 300,
                    'level': 5
                }
            ])

        # Add friendly alien if not purely combat
        if 'quest' in prompt_lower or 'help' in prompt_lower:
            npcs.append({
                'name': 'Alien Informant',
                'type': 'friendly',
                'dialogue': ['I can help you navigate this city', 'Beware of the hostile aliens'],
                'location': {'x': 100, 'y': 0, 'z': 0},
                'quest_giver': True
            })

    elif theme == 'fantasy':
        npcs.extend([
            {
                'name': 'Forest Guardian',
                'type': 'friendly',
                'dialogue': ['Welcome to our magical world!', 'How can I assist you today?'],
                'location': {'x': 100, 'y': 0, 'z': 0}
            }
        ])

    elif theme == 'medieval':
        npcs.extend([
            {
                'name': 'Castle Guard',
                'type': 'neutral',
                'dialogue': ['Halt! State your business', 'The castle is well protected'],
                'location': {'x': 150, 'y': 0, 'z': 0}
            }
        ])

    return npcs

def generate_contextual_quests(prompt_lower: str, theme: str) -> list:
    """Generate quests based on prompt and theme"""

    quests = []

    if theme == 'alien':
        if 'defeat' in prompt_lower or 'fight' in prompt_lower:
            quest = {
                'name': 'Alien Invasion Defense',
                'description': 'Defeat the alien invaders to save the city',
                'objectives': [
                    'Eliminate 5 alien warriors',
                    'Defeat the alien commander',
                    'Secure the city center'
                ],
                'rewards': ['Plasma Rifle', '500 Credits', 'Hero Badge'],
                'npc': 'Alien Informant'
            }
            # Ensure it's a proper dictionary
            if isinstance(quest, dict):
                quests.append(quest)

        if 'city' in prompt_lower:
            quest = {
                'name': 'City Liberation',
                'description': 'Free the alien-occupied city',
                'objectives': [
                    'Infiltrate alien base',
                    'Disable alien technology',
                    'Rally human resistance'
                ],
                'rewards': ['Advanced Armor', '1000 Credits']
            }
            # Ensure it's a proper dictionary
            if isinstance(quest, dict):
                quests.append(quest)

    elif theme == 'fantasy':
        quest = {
            'name': 'Crystal Collection',
            'description': 'Collect magical crystals scattered throughout the forest',
            'objectives': ['Find 5 magical crystals', 'Return to the Elder'],
            'rewards': ['Magic Staff', '100 Gold']
        }
        # Ensure it's a proper dictionary
        if isinstance(quest, dict):
            quests.append(quest)

    # Final validation - ensure all quests are dictionaries
    validated_quests = []
    for quest in quests:
        if isinstance(quest, dict):
            validated_quests.append(quest)
        else:
            print(f"⚠️ Warning: Invalid quest type {type(quest)}: {quest}")

    return validated_quests

def validate_world_data(world_data):
    """Validate and fix world data structure"""
    if not isinstance(world_data, dict):
        print(f"❌ Critical Error: world_data is not a dict: {type(world_data)}")
        print(f"world_data content: {world_data}")
        return None

    # Ensure required fields exist
    if 'id' not in world_data:
        world_data['id'] = str(uuid.uuid4())
    if 'name' not in world_data:
        world_data['name'] = 'Generated World'
    if 'theme' not in world_data:
        world_data['theme'] = 'fantasy'

    # Validate NPCs
    if 'npcs' in world_data:
        if not isinstance(world_data['npcs'], list):
            print(f"⚠️ Warning: NPCs is not a list, converting: {type(world_data['npcs'])}")
            world_data['npcs'] = []
        else:
            # Validate each NPC
            valid_npcs = []
            for i, npc in enumerate(world_data['npcs']):
                if isinstance(npc, dict):
                    valid_npcs.append(npc)
                else:
                    print(f"⚠️ Warning: NPC {i} is not a dict, skipping: {type(npc)}")
            world_data['npcs'] = valid_npcs

    # Validate Quests
    if 'quests' in world_data:
        if not isinstance(world_data['quests'], list):
            print(f"⚠️ Warning: Quests is not a list, converting: {type(world_data['quests'])}")
            world_data['quests'] = []
        else:
            # Validate each quest
            valid_quests = []
            for i, quest in enumerate(world_data['quests']):
                if isinstance(quest, dict):
                    valid_quests.append(quest)
                else:
                    print(f"⚠️ Warning: Quest {i} is not a dict, skipping: {type(quest)}")
            world_data['quests'] = valid_quests

    print(f"✅ World data validation complete. NPCs: {len(world_data.get('npcs', []))}, Quests: {len(world_data.get('quests', []))}")
    return world_data

def generate_theme_npcs(theme: str, include_npcs: bool) -> list:
    """Generate NPCs based on theme"""
    if not include_npcs:
        return []
    
    npcs = []
    
    if theme == "fantasy":
        npcs = [
            {
                'name': 'Village Elder',
                'type': 'friendly',
                'health': 100,
                'level': 5,
                'faction': 'village',
                'quest_giver': True,
                'dialogue': ['Welcome, young adventurer!', 'I have a quest for you.', 'The village needs your help.'],
                'location': {'x': 0, 'y': 0, 'z': 0}
            },
            {
                'name': 'Fairy Merchant',
                'type': 'friendly',
                'health': 50,
                'level': 3,
                'faction': 'fairy',
                'merchant': True,
                'dialogue': ['Welcome to my shop!', 'I have magical items for sale.', 'Take a look at my wares.'],
                'location': {'x': 200, 'y': 100, 'z': 0}
            },
            {
                'name': 'Forest Guardian',
                'type': 'neutral',
                'health': 150,
                'level': 8,
                'faction': 'nature',
                'quest_giver': True,
                'dialogue': ['The forest speaks to me.', 'I protect this sacred grove.', 'What brings you here?'],
                'location': {'x': 400, 'y': 300, 'z': 0}
            }
        ]
    elif theme == "cyberpunk":
        npcs = [
            {
                'name': 'Hacker',
                'type': 'friendly',
                'health': 80,
                'level': 6,
                'faction': 'underground',
                'quest_giver': True,
                'dialogue': ['Hey, need some tech work?', 'I can hack anything.', 'The corps are watching.'],
                'location': {'x': 0, 'y': 0, 'z': 0}
            },
            {
                'name': 'Street Vendor',
                'type': 'friendly',
                'health': 60,
                'level': 2,
                'faction': 'street',
                'merchant': True,
                'dialogue': ['Fresh synth-meat!', 'Best prices in the district.', 'Stay safe out there.'],
                'location': {'x': 200, 'y': 100, 'z': 0}
            },
            {
                'name': 'Corporate Agent',
                'type': 'hostile',
                'health': 120,
                'level': 7,
                'faction': 'corporate',
                'quest_giver': False,
                'dialogue': ['Unauthorized access detected.', 'You will be terminated.', 'Surrender now.'],
                'location': {'x': 400, 'y': 300, 'z': 0}
            }
        ]
    elif theme == "medieval":
        npcs = [
            {
                'name': 'Knight Commander',
                'type': 'friendly',
                'health': 150,
                'level': 10,
                'faction': 'kingdom',
                'quest_giver': True,
                'dialogue': ['Greetings, brave warrior!', 'The kingdom needs your sword.', 'Honor and glory await.'],
                'location': {'x': 0, 'y': 0, 'z': 0}
            },
            {
                'name': 'Blacksmith',
                'type': 'friendly',
                'health': 100,
                'level': 4,
                'faction': 'craftsmen',
                'merchant': True,
                'dialogue': ['Fine weapons for sale!', 'I forge the best steel.', 'What can I make for you?'],
                'location': {'x': 200, 'y': 100, 'z': 0}
            },
            {
                'name': 'Wise Wizard',
                'type': 'friendly',
                'health': 80,
                'level': 12,
                'faction': 'magic',
                'quest_giver': True,
                'dialogue': ['Magic flows through this land.', 'I sense great power in you.', 'The ancient spells call.'],
                'location': {'x': 400, 'y': 300, 'z': 0}
            }
        ]
    else:
        # Default NPCs
        npcs = [
            {
                'name': 'Local Guide',
                'type': 'friendly',
                'health': 100,
                'level': 3,
                'faction': 'local',
                'quest_giver': True,
                'dialogue': ['Welcome to our world!', 'I can help you get started.', 'Adventure awaits!'],
                'location': {'x': 0, 'y': 0, 'z': 0}
            }
        ]
    
    return npcs

def generate_theme_quests(theme: str, include_quests: bool) -> list:
    """Generate quests based on theme"""
    if not include_quests:
        return []
    
    quests = []
    
    if theme == "fantasy":
        quests = [
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
            },
            {
                'name': 'Forest Guardian',
                'type': 'main',
                'objective': 'Defeat the corrupted guardian',
                'description': 'The forest guardian has been corrupted by dark magic',
                'rewards': {'experience': 200, 'gold': 100},
                'location': {'x': 700, 'y': 400, 'z': 0}
            }
        ]
    elif theme == "cyberpunk":
        quests = [
            {
                'name': 'Data Heist',
                'type': 'main',
                'objective': 'Steal corporate data',
                'description': 'Infiltrate the corporate building and steal classified data',
                'rewards': {'experience': 150, 'credits': 100},
                'location': {'x': 300, 'y': 200, 'z': 0}
            },
            {
                'name': 'Street Justice',
                'type': 'side',
                'objective': 'Stop street gang activity',
                'description': 'Help clean up the streets from gang violence',
                'rewards': {'experience': 75, 'credits': 50},
                'location': {'x': 500, 'y': 300, 'z': 0}
            },
            {
                'name': 'System Override',
                'type': 'main',
                'objective': 'Hack the mainframe',
                'description': 'Override the corporate security system',
                'rewards': {'experience': 250, 'credits': 150},
                'location': {'x': 700, 'y': 400, 'z': 0}
            }
        ]
    elif theme == "medieval":
        quests = [
            {
                'name': 'Dragon Slayer',
                'type': 'main',
                'objective': 'Defeat the dragon',
                'description': 'The kingdom is under threat from a fearsome dragon',
                'rewards': {'experience': 300, 'gold': 200},
                'location': {'x': 300, 'y': 200, 'z': 0}
            },
            {
                'name': 'Royal Delivery',
                'type': 'side',
                'objective': 'Deliver royal message',
                'description': 'Carry an important message to the neighboring kingdom',
                'rewards': {'experience': 100, 'gold': 75},
                'location': {'x': 500, 'y': 300, 'z': 0}
            },
            {
                'name': 'Ancient Relic',
                'type': 'main',
                'objective': 'Find the ancient relic',
                'description': 'Recover a powerful relic from the ancient ruins',
                'rewards': {'experience': 400, 'gold': 300},
                'location': {'x': 700, 'y': 400, 'z': 0}
            }
        ]
    else:
        # Default quests
        quests = [
            {
                'name': 'Exploration',
                'type': 'main',
                'objective': 'Explore the world',
                'description': 'Discover the secrets of this mysterious world',
                'rewards': {'experience': 100, 'gold': 50},
                'location': {'x': 300, 'y': 200, 'z': 0}
            }
        ]
    
    return quests

def generate_theme_environment(theme: str, environment_type: str, include_environment: bool) -> dict:
    """Generate environment data based on theme"""
    if not include_environment:
        return {}
    
    environment = {
        'type': environment_type,
        'lighting': 'dynamic_lighting',
        'weather': 'clear',
        'atmosphere': 'normal',
        'size': 'medium'
    }
    
    if theme == "fantasy":
        environment.update({
            'atmosphere': 'magical',
            'assets': ['trees', 'bushes', 'rocks', 'flowers', 'mushrooms', 'crystals', 'magic_portals']
        })
    elif theme == "cyberpunk":
        environment.update({
            'lighting': 'neon_lighting',
            'weather': 'rainy',
            'atmosphere': 'urban',
            'assets': ['buildings', 'neon_signs', 'vehicles', 'street_lights', 'holograms', 'security_cameras']
        })
    elif theme == "medieval":
        environment.update({
            'atmosphere': 'historical',
            'assets': ['castles', 'towers', 'walls', 'banners', 'torches', 'stone_paths', 'moats']
        })
    elif theme == "desert":
        environment.update({
            'weather': 'hot',
            'atmosphere': 'arid',
            'assets': ['sand_dunes', 'cacti', 'rocks', 'oasis', 'ruins', 'tents']
        })
    else:
        environment.update({
            'assets': ['trees', 'rocks', 'buildings', 'paths']
        })
    
    return environment

@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>TTG Genesis UE5 - Enhanced World Generator</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
            color: #e0e0e0;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            min-height: 100vh;
        }

        .left-panel, .right-panel {
            background: rgba(20, 20, 20, 0.9);
            border: 1px solid #333;
            border-radius: 12px;
            padding: 30px;
            backdrop-filter: blur(10px);
        }

        h1 {
            color: #00ff88;
            text-align: center;
            margin-bottom: 10px;
            font-size: 2.5em;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.3);
        }

        .subtitle {
            text-align: center;
            color: #888;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .input-group {
            margin: 25px 0;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #00ff88;
            font-size: 1.1em;
        }

        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #333;
            border-radius: 8px;
            font-size: 16px;
            background: #1a1a1a;
            color: #e0e0e0;
            transition: all 0.3s ease;
        }

        input[type="text"]:focus {
            border-color: #00ff88;
            box-shadow: 0 0 15px rgba(0, 255, 136, 0.2);
            outline: none;
        }

        .checkbox-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 15px;
            margin: 25px 0;
        }

        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px;
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 8px;
            transition: all 0.3s ease;
        }

        .checkbox-item:hover {
            background: #333;
            border-color: #00ff88;
        }

        .checkbox-item input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #00ff88;
        }

        .btn {
            padding: 15px 30px;
            margin: 10px 5px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .btn-primary {
            background: linear-gradient(45deg, #00ff88, #00cc6a);
            color: #000;
            box-shadow: 0 4px 15px rgba(0, 255, 136, 0.3);
        }

        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 255, 136, 0.4);
        }

        .btn-success {
            background: linear-gradient(45deg, #ff6b00, #ff8533);
            color: white;
            box-shadow: 0 4px 15px rgba(255, 107, 0, 0.3);
        }

        .btn-success:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(255, 107, 0, 0.4);
        }

        .btn:disabled {
            background: #444;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .step-indicator {
            display: flex;
            justify-content: center;
            margin: 25px 0;
            gap: 20px;
        }

        .step {
            padding: 12px 24px;
            border-radius: 25px;
            background: #2a2a2a;
            color: #888;
            border: 2px solid #444;
            transition: all 0.3s ease;
        }

        .step.active {
            background: linear-gradient(45deg, #00ff88, #00cc6a);
            color: #000;
            border-color: #00ff88;
        }

        .step.complete {
            background: linear-gradient(45deg, #ff6b00, #ff8533);
            color: white;
            border-color: #ff6b00;
        }

        .preview-container {
            margin-top: 20px;
            border: 1px solid #333;
            border-radius: 8px;
            background: #1a1a1a;
            overflow: hidden;
        }

        .preview-tabs {
            display: flex;
            background: #2a2a2a;
        }

        .preview-tab {
            padding: 12px 20px;
            cursor: pointer;
            border-right: 1px solid #333;
            transition: all 0.3s ease;
        }

        .preview-tab.active {
            background: #00ff88;
            color: #000;
        }

        .preview-content {
            padding: 20px;
            min-height: 400px;
            display: none;
        }

        .preview-content.active {
            display: block;
        }

        .json-preview {
            background: #0d1117;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 15px;
            font-family: 'Courier New', monospace;
            font-size: 14px;
            color: #e6edf3;
            white-space: pre-wrap;
            max-height: 350px;
            overflow-y: auto;
        }

        .canvas-3d {
            width: 100%;
            height: 350px;
            border: 1px solid #333;
            border-radius: 6px;
            background: #000;
        }

        .umap-guide {
            background: #2a2a2a;
            border: 1px solid #444;
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
        }

        .guide-step {
            margin: 15px 0;
            padding: 10px;
            background: #1a1a1a;
            border-left: 4px solid #00ff88;
            border-radius: 4px;
        }

        .guide-step h4 {
            color: #00ff88;
            margin-bottom: 8px;
        }

        .output {
            margin-top: 20px;
            padding: 20px;
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            display: none;
        }

        .success { color: #00ff88; }
        .error { color: #ff4444; }
        .warning { color: #ffaa00; }

        @media (max-width: 1200px) {
            .container {
                grid-template-columns: 1fr;
                gap: 20px;
            }
        }
    </style>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
</head>
<body>
    <div class="container">
        <div class="left-panel">
            <h1>TTG Genesis</h1>
            <p class="subtitle">Enhanced UE5 World Generator</p>

            <div class="step-indicator">
                <div class="step active" id="step1">Generate JSON</div>
                <div class="step" id="step2">Create UE5 World</div>
            </div>

            <div class="input-group">
                <label for="prompt">🌍 World Description:</label>
                <input type="text" id="prompt" placeholder="Create a magical forest with fairy NPCs and crystal collection quests">
            </div>

            <div class="checkbox-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="npcs" checked>
                    <label for="npcs">🧙‍♀️ Include NPCs</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="quests" checked>
                    <label for="quests">⚔️ Include Quests</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="environment" checked>
                    <label for="environment">🌲 Include Environment</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="combat" checked>
                    <label for="combat">⚡ Include Combat</label>
                </div>
            </div>

            <button onclick="generateJSON()" class="btn btn-primary" id="jsonBtn">
                🔮 Generate JSON Data
            </button>

            <button onclick="createUE5Project()" class="btn btn-success" id="ue5Btn" disabled>
                🎮 Create UE5 World
            </button>

            <div class="umap-guide">
                <h3 style="color: #00ff88; margin-bottom: 15px;">📖 How to Open .umap Files</h3>

                <div class="guide-step">
                    <h4>Step 1: Locate Your Project</h4>
                    <p>Generated projects are in: <code>TTG-Generated-UE5-Projects/</code></p>
                </div>

                <div class="guide-step">
                    <h4>Step 2: Open in UE5</h4>
                    <p>Double-click the <code>.uproject</code> file to open in Unreal Engine 5.6</p>
                </div>

                <div class="guide-step">
                    <h4>Step 3: Compile C++ Code</h4>
                    <p>In UE5: <strong>Build → Compile</strong> (wait for compilation to complete)</p>
                </div>

                <div class="guide-step">
                    <h4>Step 4: Open the Level</h4>
                    <p>Navigate to: <code>Content/TTGWorlds/YourWorld/YourWorld_Level.umap</code></p>
                    <p>Double-click the <code>.umap</code> file to open the level</p>
                </div>

                <div class="guide-step">
                    <h4>Step 5: Test Your World</h4>
                    <p>Press <strong>Play</strong> button in UE5 to test your generated world!</p>
                </div>
            </div>

            <div id="output" class="output"></div>
        </div>

        <div class="right-panel">
            <h2 style="color: #00ff88; margin-bottom: 20px;">📊 Preview & Results</h2>

            <div class="preview-container">
                <div class="preview-tabs">
                    <div class="preview-tab active" onclick="switchTab('json')">📄 JSON Data</div>
                    <div class="preview-tab" onclick="switchTab('3d')">🎮 3D Preview</div>
                </div>

                <div class="preview-content active" id="json-content">
                    <div class="json-preview" id="json-display">
                        Generate JSON data to see the world structure here...
                    </div>
                </div>

                <div class="preview-content" id="3d-content">
                    <canvas class="canvas-3d" id="canvas3d"></canvas>
                    <div style="margin-top: 10px; color: #888; text-align: center;">
                        3D preview will appear after UE5 world creation
                    </div>
                </div>
            </div>
        </div>

    <script>
        let currentWorldId = null;
        let currentWorldData = null;
        let scene, camera, renderer;

        // Initialize 3D scene
        function init3DScene() {
            const canvas = document.getElementById('canvas3d');
            scene = new THREE.Scene();
            camera = new THREE.PerspectiveCamera(75, canvas.clientWidth / canvas.clientHeight, 0.1, 1000);
            renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true });
            renderer.setSize(canvas.clientWidth, canvas.clientHeight);
            renderer.setClearColor(0x0a0a0a);

            // Add ambient light
            const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
            scene.add(ambientLight);

            // Add directional light
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(10, 10, 5);
            scene.add(directionalLight);

            camera.position.set(0, 5, 10);
            camera.lookAt(0, 0, 0);
        }

        // Switch between preview tabs
        function switchTab(tabName) {
            // Update tab buttons
            document.querySelectorAll('.preview-tab').forEach(tab => tab.classList.remove('active'));
            document.querySelector(`[onclick="switchTab('${tabName}')"]`).classList.add('active');

            // Update content
            document.querySelectorAll('.preview-content').forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabName}-content`).classList.add('active');

            if (tabName === '3d' && renderer) {
                renderer.setSize(document.getElementById('canvas3d').clientWidth, document.getElementById('canvas3d').clientHeight);
            }
        }

        // Display JSON data with syntax highlighting
        function displayJSON(data) {
            const jsonDisplay = document.getElementById('json-display');
            const formattedJSON = JSON.stringify(data, null, 2);

            // Simple syntax highlighting using replace with regex
            let highlighted = formattedJSON;
            highlighted = highlighted.replace(/"([^"]+)":/g, '<span style="color: #87ceeb;">"$1":</span>');
            highlighted = highlighted.replace(/: "([^"]+)"/g, ': <span style="color: #98fb98;">"$1"</span>');
            highlighted = highlighted.replace(/: (\\d+)/g, ': <span style="color: #ffa07a;">$1</span>');
            highlighted = highlighted.replace(/: (true|false|null)/g, ': <span style="color: #ff6b6b;">$1</span>');

            jsonDisplay.innerHTML = highlighted;
        }

        // Create 3D preview of the world
        function create3DPreview(worldData) {
            if (!scene) init3DScene();

            // Clear existing objects
            while(scene.children.length > 2) { // Keep lights
                scene.remove(scene.children[2]);
            }

            // Create ground plane
            const groundGeometry = new THREE.PlaneGeometry(20, 20);
            const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x2d5a27 });
            const ground = new THREE.Mesh(groundGeometry, groundMaterial);
            ground.rotation.x = -Math.PI / 2;
            scene.add(ground);

            // Add NPCs as colored cubes
            if (worldData.npcs) {
                worldData.npcs.forEach((npc, index) => {
                    const geometry = new THREE.BoxGeometry(1, 2, 1);
                    const material = new THREE.MeshLambertMaterial({
                        color: npc.type === 'friendly' ? 0x00ff00 : npc.type === 'enemy' ? 0xff0000 : 0xffff00
                    });
                    const cube = new THREE.Mesh(geometry, material);

                    const location = npc.location || { x: index * 3, y: 1, z: 0 };
                    cube.position.set(location.x / 100, location.z / 100 + 1, location.y / 100);
                    scene.add(cube);
                });
            }

            // Add quest markers as pyramids
            if (worldData.quests) {
                worldData.quests.forEach((quest, index) => {
                    const geometry = new THREE.ConeGeometry(0.5, 2, 4);
                    const material = new THREE.MeshLambertMaterial({ color: 0xffd700 });
                    const cone = new THREE.Mesh(geometry, material);
                    cone.position.set((index - worldData.quests.length/2) * 4, 1, -5);
                    scene.add(cone);
                });
            }

            // Start animation loop
            animate();
        }

        // Animation loop for 3D scene
        function animate() {
            requestAnimationFrame(animate);

            // Rotate camera around the scene
            const time = Date.now() * 0.0005;
            camera.position.x = Math.cos(time) * 15;
            camera.position.z = Math.sin(time) * 15;
            camera.lookAt(0, 0, 0);

            if (renderer) {
                renderer.render(scene, camera);
            }
        }

        // Initialize on page load
        window.addEventListener('load', () => {
            init3DScene();
        });

        async function generateJSON() {
            const prompt = document.getElementById('prompt').value.trim();
            if (!prompt) {
                alert('Please enter a world description!');
                return;
            }

            const options = {
                includeNPCs: document.getElementById('npcs').checked,
                includeQuests: document.getElementById('quests').checked,
                includeEnvironment: document.getElementById('environment').checked,
                includeCombat: document.getElementById('combat').checked
            };

            const jsonBtn = document.getElementById('jsonBtn');
            const ue5Btn = document.getElementById('ue5Btn');
            const output = document.getElementById('output');
            const step1 = document.getElementById('step1');
            const step2 = document.getElementById('step2');

            jsonBtn.disabled = true;
            jsonBtn.innerHTML = '⏳ Generating JSON...';
            output.style.display = 'block';
            output.innerHTML = '<p class="warning">🔮 Generating JSON data...</p>';

            try {
                const response = await fetch('/api/generate-json', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: prompt, options: options })
                });

                const result = await response.json();

                if (result.success) {
                    currentWorldId = result.world_id;
                    currentWorldData = result.world_data;

                    // Display JSON in preview
                    displayJSON(result.world_data);

                    output.innerHTML = '<div class="success"><h3>✅ Step 1 Complete!</h3><p>' + result.message + '</p></div>';
                    ue5Btn.disabled = false;
                    step1.className = 'step complete';
                    step2.className = 'step active';

                    // Auto-switch to JSON tab to show the generated data
                    switchTab('json');
                } else {
                    output.innerHTML = '<div class="error"><h3>❌ Error:</h3><p>' + result.error + '</p></div>';
                }

            } catch (error) {
                output.innerHTML = '<div class="error"><h3>🚫 Network Error:</h3><p>' + error.message + '</p></div>';
            } finally {
                jsonBtn.disabled = false;
                jsonBtn.innerHTML = '🔮 Generate JSON Data';
            }
        }
        
        async function createUE5Project() {
            if (!currentWorldId) {
                alert('Please generate JSON data first!');
                return;
            }

            const ue5Btn = document.getElementById('ue5Btn');
            const output = document.getElementById('output');
            const step2 = document.getElementById('step2');

            ue5Btn.disabled = true;
            ue5Btn.innerHTML = '⚙️ Creating UE5 World...';
            output.innerHTML += '<p class="warning">🎮 Creating UE5 world with embedded assets...</p>';

            try {
                const response = await fetch('/api/create-ue5-project', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        world_id: currentWorldId,
                        ue5_options: { generateProjectFiles: false, compileProject: false }
                    })
                });

                const result = await response.json();

                if (result.success) {
                    // Create 3D preview
                    if (currentWorldData) {
                        create3DPreview(currentWorldData);
                        switchTab('3d'); // Auto-switch to 3D preview
                    }

                    output.innerHTML += `
                        <div class="success">
                            <h3>🎉 UE5 World Created Successfully!</h3>
                            <p>${result.message}</p>
                            <div style="margin: 15px 0; padding: 15px; background: #2a2a2a; border-radius: 8px;">
                                <h4 style="color: #00ff88;">📁 Project Location:</h4>
                                <p><code>TTG-Generated-UE5-Projects/${result.ue5_project.world_name || 'YourWorld'}/</code></p>

                                <h4 style="color: #00ff88; margin-top: 15px;">🗺️ Level File:</h4>
                                <p><code>${result.ue5_project.level_file || 'YourWorld_Level.umap'}</code></p>

                                <h4 style="color: #00ff88; margin-top: 15px;">✅ Features:</h4>
                                <ul style="margin: 10px 0;">
                                    <li>✅ No DataTable import issues</li>
                                    <li>✅ All data embedded in .uasset files</li>
                                    <li>✅ .umap level ready to open</li>
                                    <li>✅ C++ classes generated</li>
                                </ul>
                            </div>
                        </div>
                    `;
                    step2.className = 'step complete';
                } else {
                    output.innerHTML += '<div class="error"><h3>❌ UE5 Project Error:</h3><p>' + result.error + '</p></div>';
                }

            } catch (error) {
                output.innerHTML += '<div class="error"><h3>🚫 Network Error:</h3><p>' + error.message + '</p></div>';
            } finally {
                ue5Btn.disabled = false;
                ue5Btn.innerHTML = '🎮 Create UE5 World';
            }
        }

    </script>
</body>
</html>
    '''

@app.route('/api/status')
def api_status():
    return jsonify({
        'status': 'running',
        'ue5_available': UE5_AVAILABLE,
        'cached_worlds': len(json_cache)
    })

@app.route('/api/generate-json', methods=['POST'])
def api_generate_json():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        options = data.get('options', {})
        
        if not prompt:
            return jsonify({'success': False, 'error': 'Prompt is required'}), 400
        
        # Use intelligent world generation based on prompt analysis
        print(f"🎯 Analyzing prompt: '{prompt}'")
        world_data = generate_intelligent_world_data(prompt, options)
        print(f"🔍 Debug - Generated world_data type: {type(world_data)}")
        print(f"🔍 Debug - Generated world_data keys: {list(world_data.keys()) if isinstance(world_data, dict) else 'Not a dict'}")
        world_id = world_data['id']
        
        # Cache for step 2
        json_cache[world_id] = {
            'world_data': world_data,
            'prompt': prompt,
            'options': options,
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'world_id': world_id,
            'world_data': world_data,
            'message': f'JSON data for "{world_data["name"]}" generated successfully! You can now create the UE5 project.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/create-ue5-project', methods=['POST'])
def api_create_ue5_project():
    try:
        data = request.get_json()
        world_id = data.get('world_id', '')
        ue5_options = data.get('ue5_options', {})
        
        if not world_id or world_id not in json_cache:
            return jsonify({'success': False, 'error': 'Invalid world ID'}), 400
        
        if not ue5_generator:
            return jsonify({'success': False, 'error': 'UE5 World Generator not available'}), 500

        cached_data = json_cache[world_id]
        print(f"🔍 Debug - cached_data type: {type(cached_data)}")
        print(f"🔍 Debug - cached_data keys: {list(cached_data.keys()) if isinstance(cached_data, dict) else 'Not a dict'}")

        world_data = cached_data['world_data']
        print(f"🔍 Debug - world_data from cache type: {type(world_data)}")
        print(f"🔍 Debug - world_data from cache: {world_data}")

        # Validate world data before passing to UE5 generator
        validated_world_data = validate_world_data(world_data)
        if validated_world_data is None:
            return jsonify({
                'success': False,
                'error': 'Invalid world data structure - validation failed'
            }), 500

        # Create world in existing project
        ue5_result = ue5_generator.create_world_in_project(validated_world_data, ue5_options)
        
        if ue5_result.get('success'):
            return jsonify({
                'success': True,
                'world_id': world_id,
                'ue5_project': ue5_result,
                'message': f'UE 5.6.0 project "{world_data["name"]}" created successfully!'
            })
        else:
            return jsonify({
                'success': False,
                'error': ue5_result.get('error', 'UE5 project creation failed')
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/add-test-cube', methods=['POST'])
def add_test_cube():
    """Add a simple test cube to the TTGWorldGenerator project"""
    try:
        data = request.get_json()
        cube_name = data.get('cube_name', 'TTG_Test_Cube')
        location = data.get('location', {'x': 500, 'y': 500, 'z': 100})

        if not ue5_generator:
            return jsonify({'success': False, 'error': 'UE5 World Generator not available'}), 500

        # Create test cube in the project
        cube_result = ue5_generator.create_test_cube(cube_name, location)

        if cube_result.get('success'):
            return jsonify({
                'success': True,
                'cube_info': cube_result,
                'message': f'Test cube "{cube_name}" created successfully in TTGWorldGenerator project!'
            })
        else:
            return jsonify({
                'success': False,
                'error': cube_result.get('error', 'Test cube creation failed')
            }), 500

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("="*50)
    print("TTG GENESIS UE5 SERVER READY!")
    print("="*50)
    print("Web Interface: http://localhost:5000")
    print("2-Step Process:")
    print("  1. Generate JSON Data")
    print("  2. Create UE 5.6.0 Project")
    if UE5_AVAILABLE and ue5_generator:
        print(f"UE5 Installation: Found")
        print(f"Base Project: TTG_WorldGenerator_Base")
    print("="*50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
