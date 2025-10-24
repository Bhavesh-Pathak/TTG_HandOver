# TTG Genesis - Text to Game World Generator

🎮 **Transform natural language prompts into structured game worlds for Unreal Engine 5**

## Overview

TTG Genesis is an advanced prompt parser system that uses Ollama LLM to convert natural language descriptions into structured JSON/YAML files for game world generation in Unreal Engine 5. Simply describe your game world in plain English, and the system will generate comprehensive data including environments, quests, NPCs, physics, and assets.

## Features

- 🤖 **LLM-Powered**: Uses Ollama with models like Llama2, Llama3, Mistral
- 🌍 **Comprehensive World Generation**: Environments, quests, NPCs, physics, assets
- 📄 **Multiple Output Formats**: JSON and YAML support
- 🔄 **Fallback System**: Works even when LLM is unavailable
- 🎯 **UE5 Ready**: Structured output designed for Unreal Engine 5 integration
- 🔧 **Configurable**: Extensive configuration options
- 📊 **Batch Processing**: Generate multiple worlds at once

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd TASK_4

# Run the setup script
python setup.py
```

### 2. Install Ollama (if not already installed)

```bash
# Visit https://ollama.ai and install Ollama
# Then run:
ollama serve
ollama pull llama2  # or llama3, mistral, etc.
```

### 3. Generate Your First World

```bash
# Interactive mode
python ttg-genesis/bhiv-core/prompt-parser.py

# Direct prompt
python ttg-genesis/bhiv-core/prompt-parser.py "Create a mystical forest with ancient ruins and magical creatures"
```

## Example Usage

### Input Prompt
```
"Create a forest level where the player has to complete 3 quests to save a village"
```

### Generated Output
```json
{
    "metadata": {
        "level_name": "Forest Guardian's Trial",
        "description": "A mystical forest where ancient magic protects a village",
        "difficulty": "medium",
        "estimated_playtime": "45 minutes",
        "theme": "forest"
    },
    "environment": {
        "type": "forest",
        "setting": "Ancient woodland with magical elements",
        "terrain": ["grass", "dirt_paths", "rocky_areas", "streams"],
        "lighting": "filtered_sunlight",
        "weather": "misty",
        "atmosphere": "mystical",
        "size": "medium",
        "assets": ["ancient_trees", "glowing_mushrooms", "stone_ruins", "crystal_streams"]
    },
    "quests": [
        {
            "id": "forest_quest_1",
            "name": "Gather Sacred Herbs",
            "type": "main",
            "objective": "Collect 5 sacred herbs from the enchanted grove",
            "description": "The village healer needs rare herbs to cure the cursed villagers",
            "requirements": ["access_to_enchanted_grove"],
            "rewards": {
                "experience": 150,
                "gold": 75,
                "items": ["healing_elixir", "herb_pouch"]
            },
            "location": "enchanted_grove",
            "estimated_time": "15 minutes"
        }
    ],
    "npcs": [
        {
            "id": "village_elder",
            "name": "Elder Thornwick",
            "role": "quest_giver",
            "type": "friendly",
            "location": "village_center",
            "dialogue": [
                "Welcome, brave adventurer!",
                "Our village is under a terrible curse...",
                "Only you can help us now!"
            ],
            "behavior": "stationary_helpful",
            "stats": {"health": 100, "attack": 0, "defense": 20},
            "inventory": ["village_key", "ancient_map"]
        }
    ],
    "physics": {
        "player_abilities": ["walk", "run", "jump", "climb", "magic_cast"],
        "movement_speed": 5.5,
        "jump_height": 2.2,
        "combat_system": "magic_enhanced_combat",
        "interaction_mechanics": ["herb_gathering", "rune_activation", "npc_dialogue"],
        "special_mechanics": ["magic_detection", "curse_cleansing"]
    },
    "win_conditions": ["Complete all three sacred quests", "Lift the village curse"],
    "lose_conditions": ["Player health reaches 0", "Village curse becomes permanent"],
    "assets_required": {
        "models": ["tree_ancient", "mushroom_glowing", "ruins_stone", "herb_sacred"],
        "textures": ["bark_mystical", "grass_enchanted", "stone_weathered", "water_crystal"],
        "sounds": ["forest_ambient", "magic_chime", "stream_flowing", "wind_mystical"],
        "effects": ["particle_magic", "light_rays", "mist_ground", "sparkle_herbs"],
        "animations": ["player_herb_gather", "npc_blessing", "magic_cast", "curse_lift"]
    }
}
```

## Configuration

Edit `ttg-genesis/config.yaml` to customize:

```yaml
ollama:
  host: "localhost"
  port: 11434
  model: "llama2"  # Change to llama3, mistral, etc.

output:
  directory: "ue5_exports"
  default_format: "json"  # or "yaml"

world_generation:
  difficulty_levels:
    easy: { quest_count: "1-2", npc_count: "2-4" }
    medium: { quest_count: "2-4", npc_count: "4-8" }
    hard: { quest_count: "4-6", npc_count: "6-12" }
```

## API Reference

### PromptParser Class

```python
from ttg_genesis.bhiv_core.prompt_parser import PromptParser, OllamaConfig

# Initialize with custom config
config = OllamaConfig(model="llama3", host="localhost", port=11434)
parser = PromptParser(config)

# Parse a prompt
game_data = parser.parse_prompt("Create a desert temple with puzzles")

# Save to file
filepath = parser.save_to_file(game_data, "my_world.json")
```

### Convenience Functions

```python
from ttg_genesis.bhiv_core.prompt_parser import create_world_from_prompt, batch_generate_worlds

# Single world generation
filepath = create_world_from_prompt(
    "Create a haunted mansion level",
    model="llama3",
    output_format="json"
)

# Batch generation
prompts = [
    "Create a forest adventure",
    "Design a space station level",
    "Build an underwater city"
]
files = batch_generate_worlds(prompts, model="llama2")
```

## Supported Environment Types

The system can generate various environment types:

- 🌲 **Forest**: Woodland areas with trees, wildlife, and natural elements
- 🏜️ **Desert**: Arid landscapes with sand dunes, oases, and ancient ruins
- 🏰 **Dungeon**: Underground chambers with puzzles and treasures
- 🏙️ **Urban**: City environments with buildings and NPCs
- 🌊 **Ocean**: Underwater or coastal areas with marine life
- ⛰️ **Mountain**: High-altitude areas with cliffs and caves
- 🚀 **Space**: Sci-fi environments with futuristic elements
- 👻 **Haunted**: Spooky locations with supernatural elements

## Example Prompts

Here are some example prompts to get you started:

### Adventure Prompts
```
"Create a forest level where the player has to complete 3 quests to save a village"
"Design a desert temple with ancient puzzles and treasure hunting mechanics"
"Build an underwater city level with swimming mechanics and sea creature NPCs"
```

### Specific Mechanics
```
"Create a stealth-based level in a medieval castle with guard patrols"
"Design a racing level through a futuristic city with power-ups"
"Build a survival level on a deserted island with crafting mechanics"
```

### Story-Driven
```
"Create a mystery level in a haunted mansion where the player solves a murder"
"Design a space station level where the player must prevent an alien invasion"
"Build a time-travel level where the player changes historical events"
```

## Output Structure

The generated JSON contains the following main sections:

### Metadata
- Level name and description
- Difficulty and estimated playtime
- Theme and setting information

### Environment
- Terrain types and layout
- Lighting and weather conditions
- Required assets and props

### Quests
- Main and side quests
- Objectives and requirements
- Rewards and progression

### NPCs
- Character roles and behaviors
- Dialogue and interactions
- Stats and inventory

### Physics
- Player abilities and mechanics
- Movement and combat systems
- Special interactions

### Assets Required
- 3D models and textures
- Sound effects and music
- Particle effects and animations

## Integration with Unreal Engine 5

The generated JSON files are designed to be easily imported into Unreal Engine 5:

1. **Blueprint Integration**: Use the JSON data to automatically spawn actors and set up level geometry
2. **Quest System**: Import quest data into your game's quest management system
3. **NPC Spawning**: Automatically place and configure NPCs based on the generated data
4. **Asset Loading**: Use the asset lists to preload required resources
5. **Physics Setup**: Configure player abilities and world physics based on the specifications

## Troubleshooting

### Common Issues

**Ollama Connection Failed**
```
❌ Failed to connect to Ollama server
```
- Make sure Ollama is installed and running: `ollama serve`
- Check if the correct port (11434) is being used
- Verify the model is installed: `ollama list`

**Invalid JSON Response**
```
❌ Failed to parse JSON from LLM response
```
- The system will automatically fall back to template generation
- Try using a different model (llama3 instead of llama2)
- Reduce the complexity of your prompt

**Missing Dependencies**
```
❌ Import "requests" could not be resolved
```
- Run the setup script: `python setup.py`
- Or manually install: `pip install -r requirements.txt`

### Performance Tips

- Use **llama2** for faster generation, **llama3** for higher quality
- Keep prompts concise but descriptive
- Use batch generation for multiple similar worlds
- Enable fallback mode for reliable operation

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- 📖 Documentation: Check this README and the `docs/` folder
- 🐛 Issues: Report bugs on the GitHub issues page
- 💬 Discussions: Join our community discussions
- 📧 Contact: Reach out to the development team

---

**Happy World Building! 🎮✨**