import json
import requests
import yaml
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class OllamaConfig:
    
    """Configuration for Ollama LLM connection"""
    host: str = "localhost"
    port: int = 11434
    model: str = "llama2"  # Default model, can be changed to llama3, mistral, etc.
    timeout: int = 60

class PromptParser:
    """
    Advanced prompt parser that uses Ollama LLM to generate structured game world data
    from natural language prompts for Unreal Engine 5 integration.
    """

    def __init__(self, config: OllamaConfig = None):
        self.config = config or OllamaConfig()
        self.base_url = f"http://{self.config.host}:{self.config.port}"

    def _call_ollama(self, prompt: str) -> str:
        """Make API call to Ollama LLM"""
        try:
            url = f"{self.base_url}/api/generate"
            payload = {
                "model": self.config.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 2000
                }
            }

            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()

            result = response.json()
            return result.get("response", "")

        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise Exception(f"Failed to connect to Ollama: {e}")

    def _create_structured_prompt(self, user_prompt: str) -> str:
        """Create a structured prompt for the LLM to generate game world JSON"""
        return f"""
You are a game world generator for Unreal Engine 5. Convert the following natural language prompt into a structured JSON format for game world creation.

User Prompt: "{user_prompt}"

Generate a comprehensive JSON structure with the following components:

1. LEVEL/ENVIRONMENT: Define the world setting, terrain, lighting, weather
2. QUESTS: Create engaging quests with objectives, rewards, and progression
3. NPCS: Design characters with roles, dialogue, behaviors, and relationships
4. PHYSICS: Define game mechanics, player abilities, and world interactions
5. ASSETS: List required 3D models, textures, sounds, and effects
6. WIN/LOSE CONDITIONS: Clear victory and failure states

Output ONLY valid JSON in this exact structure:
{{
    "metadata": {{
        "level_name": "string",
        "description": "string",
        "difficulty": "easy|medium|hard",
        "estimated_playtime": "string",
        "theme": "string"
    }},
    "environment": {{
        "type": "string",
        "setting": "string",
        "terrain": ["string"],
        "lighting": "string",
        "weather": "string",
        "atmosphere": "string",
        "size": "small|medium|large",
        "assets": ["string"]
    }},
    "quests": [
        {{
            "id": "string",
            "name": "string",
            "type": "main|side|optional",
            "objective": "string",
            "description": "string",
            "requirements": ["string"],
            "rewards": {{
                "experience": "number",
                "gold": "number",
                "items": ["string"]
            }},
            "location": "string",
            "estimated_time": "string"
        }}
    ],
    "npcs": [
        {{
            "id": "string",
            "name": "string",
            "role": "string",
            "type": "friendly|neutral|hostile",
            "location": "string",
            "dialogue": ["string"],
            "behavior": "string",
            "stats": {{
                "health": "number",
                "attack": "number",
                "defense": "number"
            }},
            "inventory": ["string"]
        }}
    ],
    "physics": {{
        "player_abilities": ["string"],
        "movement_speed": "number",
        "jump_height": "number",
        "combat_system": "string",
        "interaction_mechanics": ["string"],
        "special_mechanics": ["string"]
    }},
    "win_conditions": ["string"],
    "lose_conditions": ["string"],
    "assets_required": {{
        "models": ["string"],
        "textures": ["string"],
        "sounds": ["string"],
        "effects": ["string"],
        "animations": ["string"]
    }}
}}

Generate creative, detailed, and balanced content. Make it engaging and suitable for Unreal Engine 5 implementation.
"""

    def _clean_json_response(self, response: str) -> str:
        """Clean and extract JSON from LLM response"""
        # Find JSON content between curly braces
        start_idx = response.find('{')
        end_idx = response.rfind('}')

        if start_idx == -1 or end_idx == -1:
            raise ValueError("No valid JSON found in LLM response")

        json_str = response[start_idx:end_idx + 1]
        return json_str

    def _validate_game_data(self, game_data: Dict[str, Any]) -> bool:
        """Validate the generated game data structure"""
        required_keys = ["metadata", "environment", "quests", "npcs", "physics",
                        "win_conditions", "lose_conditions", "assets_required"]

        for key in required_keys:
            if key not in game_data:
                logger.warning(f"Missing required key: {key}")
                return False

        # Validate quests structure
        if not isinstance(game_data["quests"], list) or len(game_data["quests"]) == 0:
            logger.warning("Quests must be a non-empty list")
            return False

        # Validate NPCs structure
        if not isinstance(game_data["npcs"], list):
            logger.warning("NPCs must be a list")
            return False

        return True

    def parse_prompt(self, prompt: str, output_format: str = "json") -> Dict[str, Any]:
        """
        Parse natural language prompt and generate structured game world data

        Args:
            prompt: Natural language description of the game world
            output_format: Output format ("json" or "yaml")

        Returns:
            Dictionary containing structured game world data
        """
        logger.info(f"Processing prompt: {prompt}")

        # Create structured prompt for LLM
        structured_prompt = self._create_structured_prompt(prompt)

        # Get response from Ollama
        try:
            llm_response = self._call_ollama(structured_prompt)
            logger.info("Received response from Ollama LLM")
        except Exception as e:
            logger.error(f"Failed to get LLM response: {e}")
            # Fallback to template-based generation
            return self._generate_fallback_data(prompt)

        # Clean and parse JSON
        try:
            json_str = self._clean_json_response(llm_response)
            game_data = json.loads(json_str)
        except (ValueError, json.JSONDecodeError) as e:
            logger.error(f"Failed to parse JSON from LLM response: {e}")
            logger.info("Falling back to template-based generation")
            return self._generate_fallback_data(prompt)

        # Validate structure
        if not self._validate_game_data(game_data):
            logger.warning("Generated data failed validation, using fallback")
            return self._generate_fallback_data(prompt)

        logger.info("Successfully generated game world data")
        return game_data

    def _generate_fallback_data(self, prompt: str) -> Dict[str, Any]:
        """Generate intelligent fallback game data based on prompt analysis"""
        logger.info("Generating intelligent fallback game data based on prompt analysis")

        # Analyze the prompt in detail
        analysis = self._analyze_prompt(prompt)

        # Generate data based on analysis
        fallback_data = {
            "metadata": {
                "level_name": analysis["level_name"],
                "description": analysis["description"],
                "difficulty": analysis["difficulty"],
                "estimated_playtime": analysis["playtime"],
                "theme": analysis["theme"]
            },
            "environment": {
                "type": analysis["environment"]["type"],
                "setting": analysis["environment"]["setting"],
                "terrain": analysis["environment"]["terrain"],
                "lighting": analysis["environment"]["lighting"],
                "weather": analysis["environment"]["weather"],
                "atmosphere": analysis["environment"]["atmosphere"],
                "size": analysis["environment"]["size"],
                "assets": analysis["environment"]["assets"]
            },
            "quests": analysis["quests"],
            "npcs": analysis["npcs"],
            "physics": analysis["physics"],
            "win_conditions": analysis["win_conditions"],
            "lose_conditions": analysis["lose_conditions"],
            "assets_required": analysis["assets_required"]
        }

        return fallback_data

    def _analyze_prompt(self, prompt: str) -> Dict[str, Any]:
        """Analyze the user prompt to extract specific game world details"""
        prompt_lower = prompt.lower()
        words = prompt_lower.split()

        # Environment analysis
        env_analysis = self._analyze_environment(prompt_lower, words)

        # Quest analysis
        quest_analysis = self._analyze_quests(prompt_lower, words)

        # NPC analysis
        npc_analysis = self._analyze_npcs(prompt_lower, words)

        # Mechanics analysis
        mechanics_analysis = self._analyze_mechanics(prompt_lower, words)

        # Generate level name based on prompt
        level_name = self._generate_level_name(prompt, env_analysis["type"])

        # Determine difficulty
        difficulty = self._determine_difficulty(prompt_lower, words)

        # Estimate playtime
        playtime = self._estimate_playtime(quest_analysis["count"], difficulty)

        return {
            "level_name": level_name,
            "description": f"An immersive {env_analysis['type']} adventure: {prompt}",
            "difficulty": difficulty,
            "playtime": playtime,
            "theme": env_analysis["type"],
            "environment": env_analysis,
            "quests": quest_analysis["quests"],
            "npcs": npc_analysis,
            "physics": mechanics_analysis,
            "win_conditions": self._generate_win_conditions(prompt_lower, quest_analysis),
            "lose_conditions": self._generate_lose_conditions(prompt_lower, mechanics_analysis),
            "assets_required": self._generate_required_assets(env_analysis, quest_analysis, npc_analysis)
        }

    def _analyze_environment(self, prompt_lower: str, words: List[str]) -> Dict[str, Any]:
        """Analyze environment details from prompt"""
        # Environment type detection with more keywords
        env_keywords = {
            "forest": ["forest", "woods", "woodland", "trees", "grove", "jungle"],
            "desert": ["desert", "sand", "dunes", "oasis", "arid", "sahara"],
            "dungeon": ["dungeon", "cave", "underground", "cavern", "crypt", "tomb"],
            "urban": ["city", "town", "urban", "street", "building", "metropolis"],
            "ocean": ["ocean", "sea", "underwater", "aquatic", "marine", "deep"],
            "mountain": ["mountain", "peak", "cliff", "alpine", "highland", "summit"],
            "space": ["space", "station", "spaceship", "alien", "galaxy", "cosmic"],
            "haunted": ["haunted", "ghost", "spooky", "mansion", "scary", "paranormal"],
            "medieval": ["castle", "medieval", "knight", "kingdom", "fortress", "manor"],
            "futuristic": ["futuristic", "cyberpunk", "sci-fi", "robot", "android", "neon"]
        }

        env_type = "forest"  # default
        for env, keywords in env_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                env_type = env
                break

        # Size analysis
        size = "medium"
        if any(word in words for word in ["small", "tiny", "mini", "little"]):
            size = "small"
        elif any(word in words for word in ["large", "huge", "massive", "giant", "vast"]):
            size = "large"

        # Atmosphere analysis
        atmosphere_keywords = {
            "mysterious": ["mysterious", "enigmatic", "secret", "hidden"],
            "peaceful": ["peaceful", "calm", "serene", "tranquil"],
            "dangerous": ["dangerous", "hostile", "threatening", "perilous"],
            "magical": ["magical", "mystical", "enchanted", "arcane"],
            "dark": ["dark", "gloomy", "sinister", "ominous"],
            "bright": ["bright", "sunny", "cheerful", "vibrant"]
        }

        atmosphere = "mysterious"
        for atm, keywords in atmosphere_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                atmosphere = atm
                break

        # Weather analysis
        weather = "clear"
        weather_keywords = {
            "stormy": ["storm", "thunder", "lightning", "rain"],
            "foggy": ["fog", "mist", "misty", "hazy"],
            "snowy": ["snow", "blizzard", "winter", "cold"],
            "sunny": ["sunny", "bright", "clear", "warm"]
        }

        for w, keywords in weather_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                weather = w
                break

        return {
            "type": env_type,
            "setting": self._generate_setting_description(env_type, prompt_lower),
            "terrain": self._get_terrain_for_env(env_type),
            "lighting": self._determine_lighting(env_type, atmosphere),
            "weather": weather,
            "atmosphere": atmosphere,
            "size": size,
            "assets": self._get_contextual_assets(env_type, prompt_lower)
        }

    def _analyze_quests(self, prompt_lower: str, words: List[str]) -> Dict[str, Any]:
        """Analyze quest requirements from prompt"""
        # Extract quest count
        quest_count = 1
        for i, word in enumerate(words):
            if word.isdigit() and i > 0 and words[i-1] in ["complete", "finish", "do"]:
                quest_count = int(word)
                break
            elif word in ["three", "3"]:
                quest_count = 3
            elif word in ["two", "2"]:
                quest_count = 2
            elif word in ["four", "4"]:
                quest_count = 4
            elif word in ["five", "5"]:
                quest_count = 5

        # Quest type analysis
        quest_types = []
        if any(word in prompt_lower for word in ["collect", "gather", "find", "retrieve"]):
            quest_types.append("collection")
        if any(word in prompt_lower for word in ["defeat", "kill", "battle", "fight"]):
            quest_types.append("combat")
        if any(word in prompt_lower for word in ["rescue", "save", "help", "protect"]):
            quest_types.append("rescue")
        if any(word in prompt_lower for word in ["solve", "puzzle", "riddle", "mystery"]):
            quest_types.append("puzzle")
        if any(word in prompt_lower for word in ["explore", "discover", "investigate"]):
            quest_types.append("exploration")

        if not quest_types:
            quest_types = ["exploration"]  # default

        # Generate quests based on analysis
        quests = self._generate_contextual_quests(quest_count, quest_types, prompt_lower)

        return {
            "count": quest_count,
            "types": quest_types,
            "quests": quests
        }

    def _analyze_npcs(self, prompt_lower: str, words: List[str]) -> List[Dict[str, Any]]:
        """Analyze NPC requirements from prompt"""
        npcs = []

        # NPC type detection
        npc_keywords = {
            "villager": ["villager", "citizen", "townspeople", "villagers"],
            "merchant": ["merchant", "trader", "shopkeeper", "vendor"],
            "guard": ["guard", "soldier", "warrior", "knight"],
            "elder": ["elder", "chief", "leader", "mayor"],
            "enemy": ["enemy", "bandit", "monster", "creature"],
            "wizard": ["wizard", "mage", "sorcerer", "witch"],
            "ghost": ["ghost", "spirit", "phantom", "specter"],
            "animal": ["animal", "creature", "beast", "wolf", "bear"]
        }

        detected_npcs = []
        for npc_type, keywords in npc_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                detected_npcs.append(npc_type)

        # Generate NPCs based on detected types
        if not detected_npcs:
            detected_npcs = ["villager"]  # default

        for npc_type in detected_npcs:
            npc = self._create_contextual_npc(npc_type, prompt_lower)
            npcs.append(npc)

        return npcs

    def _analyze_mechanics(self, prompt_lower: str, words: List[str]) -> Dict[str, Any]:
        """Analyze game mechanics from prompt"""
        abilities = ["walk", "run", "jump", "interact"]
        mechanics = ["quest_tracking", "inventory_system"]
        combat_system = "action_based"

        # Special abilities
        if any(word in prompt_lower for word in ["swim", "swimming", "underwater"]):
            abilities.append("swim")
        if any(word in prompt_lower for word in ["fly", "flying", "flight"]):
            abilities.append("fly")
        if any(word in prompt_lower for word in ["climb", "climbing"]):
            abilities.append("climb")
        if any(word in prompt_lower for word in ["magic", "spell", "cast"]):
            abilities.append("cast_spells")
        if any(word in prompt_lower for word in ["stealth", "sneak", "hide"]):
            abilities.append("stealth")

        # Special mechanics
        if any(word in prompt_lower for word in ["craft", "crafting", "build"]):
            mechanics.append("crafting_system")
        if any(word in prompt_lower for word in ["puzzle", "riddle", "solve"]):
            mechanics.append("puzzle_solving")
        if any(word in prompt_lower for word in ["trade", "trading", "merchant"]):
            mechanics.append("trading_system")
        if any(word in prompt_lower for word in ["time", "temporal", "clock"]):
            mechanics.append("time_mechanics")

        # Combat system
        if any(word in prompt_lower for word in ["turn-based", "tactical"]):
            combat_system = "turn_based"
        elif any(word in prompt_lower for word in ["real-time", "action"]):
            combat_system = "real_time"
        elif any(word in prompt_lower for word in ["stealth", "avoid", "sneak"]):
            combat_system = "stealth_based"

        return {
            "player_abilities": abilities,
            "movement_speed": 5.0,
            "jump_height": 2.0,
            "combat_system": combat_system,
            "interaction_mechanics": ["pickup_items", "talk_to_npcs", "activate_objects"],
            "special_mechanics": mechanics
        }

    def _generate_level_name(self, prompt: str, env_type: str) -> str:
        """Generate a creative level name based on the prompt"""
        prompt_lower = prompt.lower()

        # Extract key descriptive words
        descriptive_words = []
        adjectives = ["ancient", "mystical", "dark", "hidden", "lost", "forgotten", "sacred", "cursed", "magical", "haunted"]
        nouns = ["temple", "forest", "castle", "city", "ruins", "sanctuary", "chamber", "valley", "peak", "depths"]

        for adj in adjectives:
            if adj in prompt_lower:
                descriptive_words.append(adj.title())

        for noun in nouns:
            if noun in prompt_lower:
                descriptive_words.append(noun.title())

        if descriptive_words:
            return f"The {' '.join(descriptive_words[:2])}"
        else:
            env_names = {
                "forest": "Whispering Woods",
                "desert": "Shifting Sands",
                "dungeon": "Forgotten Depths",
                "urban": "Neon Streets",
                "ocean": "Abyssal Depths",
                "mountain": "Frozen Peaks",
                "space": "Stellar Void",
                "haunted": "Phantom Manor",
                "medieval": "Ancient Keep",
                "futuristic": "Chrome Citadel"
            }
            return env_names.get(env_type, "Mysterious Realm")

    def _determine_difficulty(self, prompt_lower: str, words: List[str]) -> str:
        """Determine difficulty based on prompt complexity"""
        difficulty_keywords = {
            "easy": ["easy", "simple", "beginner", "casual", "peaceful"],
            "hard": ["hard", "difficult", "challenging", "complex", "expert", "hardcore"],
            "medium": ["medium", "moderate", "balanced", "normal"]
        }

        for diff, keywords in difficulty_keywords.items():
            if any(keyword in prompt_lower for keyword in keywords):
                return diff

        # Analyze complexity indicators
        complexity_score = 0
        if any(word in prompt_lower for word in ["puzzle", "riddle", "complex", "multiple"]):
            complexity_score += 1
        if any(word in prompt_lower for word in ["battle", "fight", "combat", "enemy"]):
            complexity_score += 1
        if any(word in prompt_lower for word in ["stealth", "sneak", "avoid"]):
            complexity_score += 1

        if complexity_score >= 2:
            return "hard"
        elif complexity_score == 1:
            return "medium"
        else:
            return "easy"

    def _estimate_playtime(self, quest_count: int, difficulty: str) -> str:
        """Estimate playtime based on quest count and difficulty"""
        base_time = quest_count * 10  # 10 minutes per quest

        if difficulty == "easy":
            base_time *= 0.8
        elif difficulty == "hard":
            base_time *= 1.5

        if base_time <= 20:
            return "15-20 minutes"
        elif base_time <= 40:
            return "30-40 minutes"
        elif base_time <= 60:
            return "45-60 minutes"
        else:
            return "60+ minutes"

    def _generate_setting_description(self, env_type: str, prompt_lower: str) -> str:
        """Generate contextual setting description"""
        base_descriptions = {
            "forest": "A lush woodland area",
            "desert": "An arid desert landscape",
            "dungeon": "Underground chambers and corridors",
            "urban": "A bustling city environment",
            "ocean": "Aquatic depths and marine environments",
            "mountain": "High-altitude rocky terrain",
            "space": "Futuristic space environment",
            "haunted": "A spooky supernatural location",
            "medieval": "A medieval fantasy setting",
            "futuristic": "An advanced technological environment"
        }

        base = base_descriptions.get(env_type, "A mysterious location")

        # Add contextual details from prompt
        if "ancient" in prompt_lower:
            base += " with ancient ruins and artifacts"
        if "magical" in prompt_lower or "mystical" in prompt_lower:
            base += " infused with magical energy"
        if "dangerous" in prompt_lower:
            base += " filled with hidden dangers"
        if "peaceful" in prompt_lower:
            base += " with a serene and tranquil atmosphere"

        return base

    def _determine_lighting(self, env_type: str, atmosphere: str) -> str:
        """Determine appropriate lighting based on environment and atmosphere"""
        lighting_map = {
            ("forest", "dark"): "filtered_moonlight",
            ("forest", "bright"): "dappled_sunlight",
            ("forest", "mysterious"): "filtered_sunlight",
            ("desert", "bright"): "harsh_sunlight",
            ("desert", "dark"): "starlight",
            ("dungeon", "dark"): "torch_light",
            ("dungeon", "mysterious"): "ambient_glow",
            ("space", "dark"): "artificial_lighting",
            ("haunted", "dark"): "dim_flickering"
        }

        return lighting_map.get((env_type, atmosphere), "dynamic_lighting")

    def _get_contextual_assets(self, env_type: str, prompt_lower: str) -> List[str]:
        """Get assets based on environment and prompt context"""
        base_assets = self._get_assets_for_env(env_type)

        # Add contextual assets based on prompt
        additional_assets = []

        if "ancient" in prompt_lower:
            additional_assets.extend(["ancient_ruins", "old_statues", "weathered_stones"])
        if "magical" in prompt_lower:
            additional_assets.extend(["glowing_crystals", "magic_circles", "enchanted_items"])
        if "puzzle" in prompt_lower:
            additional_assets.extend(["puzzle_mechanisms", "switches", "pressure_plates"])
        if "treasure" in prompt_lower:
            additional_assets.extend(["treasure_chests", "gold_coins", "precious_gems"])
        if "temple" in prompt_lower:
            additional_assets.extend(["temple_pillars", "altar", "sacred_symbols"])

        return base_assets + additional_assets

    def _generate_contextual_quests(self, quest_count: int, quest_types: List[str], prompt_lower: str) -> List[Dict[str, Any]]:
        """Generate quests based on prompt analysis"""
        quests = []

        quest_templates = {
            "collection": {
                "name": "Gather Sacred Items",
                "objective": "Collect {count} {items} from the {location}",
                "description": "Ancient {items} are needed to {purpose}",
                "items": ["herbs", "crystals", "artifacts", "scrolls"],
                "locations": ["forest", "temple", "ruins", "cave"],
                "purposes": ["save the village", "unlock the door", "restore balance", "break the curse"]
            },
            "combat": {
                "name": "Defeat the Guardian",
                "objective": "Defeat the {enemy} that guards the {location}",
                "description": "A powerful {enemy} blocks your path to {goal}",
                "enemies": ["guardian", "beast", "demon", "spirit"],
                "locations": ["temple", "chamber", "grove", "sanctum"],
                "goals": ["treasure", "exit", "artifact", "sanctuary"]
            },
            "rescue": {
                "name": "Save the Villagers",
                "objective": "Rescue {count} {people} from {danger}",
                "description": "Innocent {people} are trapped and need your help",
                "people": ["villagers", "travelers", "children", "elders"],
                "dangers": ["bandits", "monsters", "curse", "prison"]
            },
            "puzzle": {
                "name": "Solve Ancient Mysteries",
                "objective": "Solve the {puzzle_type} to unlock {reward}",
                "description": "Ancient {puzzle_type} guard the secrets of this place",
                "puzzle_types": ["riddles", "mechanisms", "symbols", "patterns"],
                "rewards": ["chamber", "treasure", "passage", "knowledge"]
            },
            "exploration": {
                "name": "Explore the Unknown",
                "objective": "Discover the secrets of the {location}",
                "description": "Uncover the mysteries hidden within the {location}",
                "locations": ["ancient ruins", "hidden chamber", "sacred grove", "lost temple"]
            }
        }

        import random

        for i in range(quest_count):
            quest_type = quest_types[i % len(quest_types)]
            template = quest_templates[quest_type]

            quest = {
                "id": f"quest_{i+1}",
                "name": template["name"],
                "type": "main" if i < quest_count // 2 + 1 else "side",
                "objective": self._format_quest_objective(template, prompt_lower),
                "description": self._format_quest_description(template, prompt_lower),
                "requirements": [] if i == 0 else [f"complete_quest_{i}"],
                "rewards": {
                    "experience": 100 + (i * 50),
                    "gold": 50 + (i * 25),
                    "items": [f"quest_{i+1}_reward"]
                },
                "location": self._extract_location_from_prompt(prompt_lower),
                "estimated_time": f"{10 + (i * 5)} minutes"
            }

            quests.append(quest)

        return quests

    def _create_contextual_npc(self, npc_type: str, prompt_lower: str) -> Dict[str, Any]:
        """Create NPC based on type and prompt context"""
        npc_templates = {
            "villager": {
                "name": "Village Elder",
                "role": "quest_giver",
                "type": "friendly",
                "dialogue": ["Welcome, brave adventurer!", "Our village needs your help!", "Thank you for coming!"],
                "behavior": "stationary_helpful",
                "stats": {"health": 100, "attack": 0, "defense": 10}
            },
            "merchant": {
                "name": "Traveling Merchant",
                "role": "trader",
                "type": "friendly",
                "dialogue": ["Welcome to my shop!", "I have rare items for sale!", "Safe travels, friend!"],
                "behavior": "stationary_trader",
                "stats": {"health": 80, "attack": 5, "defense": 15}
            },
            "guard": {
                "name": "Temple Guardian",
                "role": "protector",
                "type": "neutral",
                "dialogue": ["Halt! State your business.", "This area is protected.", "You may pass."],
                "behavior": "patrol_guard",
                "stats": {"health": 120, "attack": 30, "defense": 25}
            },
            "enemy": {
                "name": "Hostile Creature",
                "role": "antagonist",
                "type": "hostile",
                "dialogue": ["*growls menacingly*", "*attacks without warning*"],
                "behavior": "aggressive_patrol",
                "stats": {"health": 80, "attack": 25, "defense": 15}
            }
        }

        template = npc_templates.get(npc_type, npc_templates["villager"])

        # Customize based on prompt
        if "ghost" in prompt_lower:
            template["name"] = "Restless Spirit"
            template["dialogue"] = ["*whispers eerily*", "Help me find peace...", "*fades away*"]
        elif "wizard" in prompt_lower:
            template["name"] = "Ancient Wizard"
            template["dialogue"] = ["Magic flows through this place...", "Seek the ancient knowledge.", "Beware the dark forces."]

        npc = {
            "id": f"{npc_type}_npc",
            "name": template["name"],
            "role": template["role"],
            "type": template["type"],
            "location": self._extract_location_from_prompt(prompt_lower),
            "dialogue": template["dialogue"],
            "behavior": template["behavior"],
            "stats": template["stats"],
            "inventory": [f"{npc_type}_item", "common_item"]
        }

        return npc

    def _format_quest_objective(self, template: Dict[str, Any], prompt_lower: str) -> str:
        """Format quest objective based on template and prompt"""
        objective = template["objective"]

        # Replace all template variables
        replacements = {
            "{count}": "3",
            "{items}": template.get("items", ["mysterious items"])[0] if "items" in template else "items",
            "{location}": self._extract_location_from_prompt(prompt_lower),
            "{enemy}": template.get("enemies", ["guardian"])[0] if "enemies" in template else "enemy",
            "{people}": template.get("people", ["villagers"])[0] if "people" in template else "people",
            "{danger}": template.get("dangers", ["unknown threat"])[0] if "dangers" in template else "danger",
            "{puzzle_type}": template.get("puzzle_types", ["ancient puzzles"])[0] if "puzzle_types" in template else "puzzles",
            "{reward}": template.get("rewards", ["hidden treasure"])[0] if "rewards" in template else "reward"
        }

        for placeholder, replacement in replacements.items():
            objective = objective.replace(placeholder, replacement)

        return objective

    def _format_quest_description(self, template: Dict[str, Any], prompt_lower: str) -> str:
        """Format quest description based on template and prompt"""
        description = template["description"]

        # Replace all template variables
        replacements = {
            "{items}": template.get("items", ["mysterious items"])[0] if "items" in template else "items",
            "{purpose}": template.get("purposes", ["complete your mission"])[0] if "purposes" in template else "achieve your goal",
            "{people}": template.get("people", ["villagers"])[0] if "people" in template else "people",
            "{enemy}": template.get("enemies", ["guardian"])[0] if "enemies" in template else "enemy",
            "{goal}": template.get("goals", ["your destination"])[0] if "goals" in template else "your goal",
            "{puzzle_type}": template.get("puzzle_types", ["ancient puzzles"])[0] if "puzzle_types" in template else "puzzles",
            "{location}": self._extract_location_from_prompt(prompt_lower)
        }

        for placeholder, replacement in replacements.items():
            description = description.replace(placeholder, replacement)

        return description

    def _extract_location_from_prompt(self, prompt_lower: str) -> str:
        """Extract location information from prompt"""
        locations = ["temple", "forest", "village", "cave", "castle", "city", "desert", "mountain", "ocean"]

        for location in locations:
            if location in prompt_lower:
                return location

        return "mysterious_location"

    def _generate_win_conditions(self, prompt_lower: str, quest_analysis: Dict[str, Any]) -> List[str]:
        """Generate win conditions based on prompt and quests"""
        conditions = []

        if quest_analysis["count"] > 1:
            conditions.append("Complete all main quests")
        else:
            conditions.append("Complete the main objective")

        if "save" in prompt_lower or "rescue" in prompt_lower:
            conditions.append("Successfully rescue all targets")
        if "defeat" in prompt_lower:
            conditions.append("Defeat all hostile enemies")
        if "find" in prompt_lower or "discover" in prompt_lower:
            conditions.append("Discover the hidden secret")

        return conditions if conditions else ["Complete the main objective"]

    def _generate_lose_conditions(self, prompt_lower: str, mechanics: Dict[str, Any]) -> List[str]:
        """Generate lose conditions based on prompt and mechanics"""
        conditions = ["Player health reaches 0"]

        if "time" in prompt_lower or "timer" in prompt_lower:
            conditions.append("Time limit expires")
        if "stealth" in mechanics["special_mechanics"]:
            conditions.append("Player is detected by enemies")
        if "rescue" in prompt_lower:
            conditions.append("Targets are not rescued in time")

        return conditions

    def _generate_required_assets(self, env_analysis: Dict[str, Any], quest_analysis: Dict[str, Any], npc_analysis: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """Generate required assets based on all analyses"""
        models = self._get_models_for_env(env_analysis["type"])
        textures = self._get_textures_for_env(env_analysis["type"])
        sounds = ["ambient_background", "footsteps", "ui_sounds"]
        effects = ["particle_dust", "light_rays"]
        animations = ["player_walk", "player_idle"]

        # Add quest-specific assets
        for quest_type in quest_analysis["types"]:
            if quest_type == "combat":
                models.extend(["weapon_sword", "shield"])
                sounds.extend(["combat_sounds", "weapon_clash"])
                animations.extend(["attack_animation", "defend_animation"])
            elif quest_type == "collection":
                models.extend(["collectible_items", "item_glow"])
                sounds.extend(["pickup_sound", "item_collected"])
                effects.extend(["pickup_sparkle"])
            elif quest_type == "puzzle":
                models.extend(["puzzle_pieces", "mechanisms"])
                sounds.extend(["puzzle_solve", "mechanism_activate"])
                effects.extend(["puzzle_glow"])

        # Add NPC-specific assets
        for npc in npc_analysis:
            if npc["type"] == "hostile":
                sounds.extend(["enemy_growl", "combat_music"])
                animations.extend(["enemy_attack", "enemy_death"])
            else:
                sounds.extend(["npc_talk", "friendly_music"])
                animations.extend(["npc_idle", "npc_gesture"])

        return {
            "models": list(set(models)),  # Remove duplicates
            "textures": list(set(textures)),
            "sounds": list(set(sounds)),
            "effects": list(set(effects)),
            "animations": list(set(animations))
        }

    def _get_terrain_for_env(self, env_type: str) -> List[str]:
        """Get terrain types for environment"""
        terrain_map = {
            "forest": ["grass", "dirt_paths", "rocky_areas", "streams"],
            "desert": ["sand_dunes", "rocky_outcrops", "oasis", "canyons"],
            "dungeon": ["stone_floors", "corridors", "chambers", "stairs"],
            "urban": ["streets", "buildings", "parks", "plazas"],
            "ocean": ["water", "beaches", "coral_reefs", "islands"],
            "mountain": ["rocky_peaks", "cliffs", "caves", "snow_caps"]
        }
        return terrain_map.get(env_type, ["grass", "dirt", "rocks"])

    def _get_assets_for_env(self, env_type: str) -> List[str]:
        """Get basic assets for environment"""
        asset_map = {
            "forest": ["trees", "bushes", "rocks", "flowers", "mushrooms"],
            "desert": ["cacti", "sand_dunes", "rocks", "palm_trees", "ruins"],
            "dungeon": ["torches", "pillars", "chests", "doors", "stairs"],
            "urban": ["buildings", "streetlights", "benches", "fountains", "vehicles"],
            "ocean": ["water", "coral", "seaweed", "fish", "boats"],
            "mountain": ["rocks", "snow", "pine_trees", "caves", "peaks"]
        }
        return asset_map.get(env_type, ["generic_props"])

    def _generate_basic_quests(self, env_type: str) -> List[Dict[str, Any]]:
        """Generate basic quests for environment"""
        quest_templates = {
            "forest": [
                {
                    "id": "forest_quest_1",
                    "name": "Gather Forest Herbs",
                    "type": "main",
                    "objective": "Collect 10 healing herbs from the forest",
                    "description": "The village healer needs herbs to cure the sick",
                    "requirements": ["access_to_forest"],
                    "rewards": {"experience": 100, "gold": 50, "items": ["healing_potion"]},
                    "location": "forest_clearing",
                    "estimated_time": "10 minutes"
                },
                {
                    "id": "forest_quest_2",
                    "name": "Defeat the Forest Guardian",
                    "type": "main",
                    "objective": "Defeat the corrupted forest guardian",
                    "description": "A once-peaceful guardian has been corrupted by dark magic",
                    "requirements": ["complete_forest_quest_1"],
                    "rewards": {"experience": 200, "gold": 100, "items": ["guardian_sword"]},
                    "location": "ancient_grove",
                    "estimated_time": "15 minutes"
                }
            ],
            "desert": [
                {
                    "id": "desert_quest_1",
                    "name": "Find the Lost Oasis",
                    "type": "main",
                    "objective": "Locate the hidden oasis in the desert",
                    "description": "Travelers speak of a magical oasis that can save the dying town",
                    "requirements": ["desert_map"],
                    "rewards": {"experience": 150, "gold": 75, "items": ["water_crystal"]},
                    "location": "deep_desert",
                    "estimated_time": "12 minutes"
                }
            ]
        }

        return quest_templates.get(env_type, [
            {
                "id": "generic_quest_1",
                "name": "Explore the Area",
                "type": "main",
                "objective": "Explore and discover the secrets of this place",
                "description": "There are mysteries to uncover in this location",
                "requirements": [],
                "rewards": {"experience": 100, "gold": 50, "items": ["exploration_token"]},
                "location": "starting_area",
                "estimated_time": "10 minutes"
            }
        ])

    def _generate_basic_npcs(self, env_type: str) -> List[Dict[str, Any]]:
        """Generate basic NPCs for environment"""
        npc_templates = {
            "forest": [
                {
                    "id": "forest_villager_1",
                    "name": "Elder Willow",
                    "role": "village_elder",
                    "type": "friendly",
                    "location": "village_center",
                    "dialogue": ["Welcome, traveler!", "The forest is in danger!", "Please help us!"],
                    "behavior": "stationary_helpful",
                    "stats": {"health": 100, "attack": 0, "defense": 10},
                    "inventory": ["village_key", "quest_scroll"]
                },
                {
                    "id": "forest_enemy_1",
                    "name": "Corrupted Wolf",
                    "role": "forest_enemy",
                    "type": "hostile",
                    "location": "dark_forest",
                    "dialogue": ["*growls menacingly*"],
                    "behavior": "aggressive_patrol",
                    "stats": {"health": 80, "attack": 25, "defense": 15},
                    "inventory": ["wolf_pelt"]
                }
            ]
        }

        return npc_templates.get(env_type, [
            {
                "id": "generic_npc_1",
                "name": "Mysterious Stranger",
                "role": "guide",
                "type": "neutral",
                "location": "starting_point",
                "dialogue": ["Greetings, adventurer!", "This place holds many secrets."],
                "behavior": "helpful_guide",
                "stats": {"health": 100, "attack": 10, "defense": 20},
                "inventory": ["map", "compass"]
            }
        ])

    def _get_models_for_env(self, env_type: str) -> List[str]:
        """Get required 3D models for environment"""
        model_map = {
            "forest": ["tree_oak", "tree_pine", "bush_berry", "rock_moss", "flower_wild"],
            "desert": ["cactus_large", "palm_tree", "sand_dune", "rock_desert", "ruins_pillar"],
            "dungeon": ["wall_stone", "door_wooden", "torch_wall", "chest_treasure", "pillar_stone"],
            "urban": ["building_house", "streetlight", "bench_park", "fountain", "car_generic"],
            "ocean": ["water_plane", "coral_reef", "seaweed", "fish_tropical", "boat_small"],
            "mountain": ["rock_cliff", "tree_pine", "snow_patch", "cave_entrance", "peak_summit"]
        }
        return model_map.get(env_type, ["generic_prop"])

    def _get_textures_for_env(self, env_type: str) -> List[str]:
        """Get required textures for environment"""
        texture_map = {
            "forest": ["bark_oak", "grass_forest", "dirt_path", "moss_rock", "leaf_texture"],
            "desert": ["sand_fine", "rock_sandstone", "palm_bark", "cactus_skin", "ruins_stone"],
            "dungeon": ["stone_wall", "wood_aged", "metal_rusty", "flame_torch", "gem_crystal"],
            "urban": ["concrete_sidewalk", "brick_building", "metal_street", "glass_window", "asphalt_road"],
            "ocean": ["water_surface", "coral_colorful", "sand_beach", "seaweed_green", "wood_boat"],
            "mountain": ["rock_granite", "snow_fresh", "ice_crystal", "pine_bark", "cliff_face"]
        }
        return texture_map.get(env_type, ["generic_texture"])

    def save_to_file(self, game_data: Dict[str, Any], filename: str = None, format_type: str = "json") -> str:
        """
        Save generated game data to file

        Args:
            game_data: Generated game world data
            filename: Output filename (auto-generated if None)
            format_type: File format ("json" or "yaml")

        Returns:
            Path to saved file
        """
        if filename is None:
            level_name = game_data.get("metadata", {}).get("level_name", "generated_level")
            safe_name = "".join(c for c in level_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_name = safe_name.replace(' ', '_').lower()
            filename = f"{safe_name}.{format_type}"

        # Ensure output directory exists
        output_dir = "ue5_exports"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)

        # Save file
        with open(filepath, 'w', encoding='utf-8') as f:
            if format_type.lower() == "yaml":
                yaml.dump(game_data, f, default_flow_style=False, indent=2)
            else:
                json.dump(game_data, f, indent=4, ensure_ascii=False)

        logger.info(f"Game data saved to: {filepath}")
        return filepath

def create_world_from_prompt(prompt: str, model: str = "llama2", output_format: str = "json") -> str:
    """
    Convenience function to create a game world from a natural language prompt

    Args:
        prompt: Natural language description of the game world
        model: Ollama model to use (llama2, llama3, mistral, etc.)
        output_format: Output format ("json" or "yaml")

    Returns:
        Path to the generated file
    """
    config = OllamaConfig(model=model)
    parser = PromptParser(config)

    try:
        game_data = parser.parse_prompt(prompt, output_format)
        filepath = parser.save_to_file(game_data, format_type=output_format)

        print(f"\n✅ Successfully generated game world!")
        print(f"📁 Saved to: {filepath}")
        print(f"🎮 Level: {game_data['metadata']['level_name']}")
        print(f"🗺️  Environment: {game_data['environment']['type']}")
        print(f"📋 Quests: {len(game_data['quests'])}")
        print(f"👥 NPCs: {len(game_data['npcs'])}")

        return filepath

    except Exception as e:
        logger.error(f"Failed to generate world: {e}")
        print(f"❌ Error: {e}")
        return ""

def batch_generate_worlds(prompts: List[str], model: str = "llama2") -> List[str]:
    """
    Generate multiple game worlds from a list of prompts

    Args:
        prompts: List of natural language prompts
        model: Ollama model to use

    Returns:
        List of paths to generated files
    """
    generated_files = []
    config = OllamaConfig(model=model)
    parser = PromptParser(config)

    for i, prompt in enumerate(prompts, 1):
        print(f"\n🔄 Processing prompt {i}/{len(prompts)}: {prompt[:50]}...")

        try:
            game_data = parser.parse_prompt(prompt)
            filename = f"batch_world_{i}.json"
            filepath = parser.save_to_file(game_data, filename)
            generated_files.append(filepath)
            print(f"✅ Generated: {filepath}")

        except Exception as e:
            logger.error(f"Failed to generate world {i}: {e}")
            print(f"❌ Failed: {e}")

    print(f"\n🎉 Batch generation complete! Generated {len(generated_files)} worlds.")
    return generated_files

def validate_ollama_connection(host: str = "localhost", port: int = 11434) -> bool:
    """
    Validate connection to Ollama server

    Args:
        host: Ollama server host
        port: Ollama server port

    Returns:
        True if connection is successful
    """
    try:
        url = f"http://{host}:{port}/api/tags"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        models = response.json().get("models", [])
        print(f"✅ Connected to Ollama server at {host}:{port}")
        print(f"📦 Available models: {[m['name'] for m in models]}")
        return True

    except Exception as e:
        print(f"❌ Failed to connect to Ollama server: {e}")
        print("💡 Make sure Ollama is running: 'ollama serve'")
        return False

if __name__ == "__main__":
    import sys

    # Example usage and testing
    print("🎮 TTG Genesis - Prompt Parser for Unreal Engine 5")
    print("=" * 50)

    # Check Ollama connection
    if not validate_ollama_connection():
        print("\n⚠️  Ollama not available, will use fallback generation")

    # Default test prompts
    test_prompts = [
        "Create a forest level where the player has to complete 3 quests to save a village",
        "Design a desert temple with ancient puzzles and treasure hunting mechanics",
        "Build an underwater city level with swimming mechanics and sea creature NPCs",
        "Create a haunted mansion with ghost NPCs and mystery-solving quests",
        "Design a space station level with zero gravity mechanics and alien encounters"
    ]

    if len(sys.argv) > 1:
        # Use command line argument as prompt
        user_prompt = " ".join(sys.argv[1:])
        print(f"\n🎯 Processing user prompt: {user_prompt}")
        create_world_from_prompt(user_prompt)
    else:
        # Interactive mode
        print("\n🎯 Interactive Mode - Enter your game world prompt:")
        print("(or press Enter to use test prompts)")

        user_input = input("\n> ").strip()

        if user_input:
            create_world_from_prompt(user_input)
        else:
            print("\n🧪 Running test prompts...")
            batch_generate_worlds(test_prompts[:2])  # Generate first 2 test prompts

    print("\n🎉 Done! Check the 'ue5_exports' folder for generated files.")