// Global variables
let currentWorldData = null;
let currentFilename = null;

// DOM elements
const promptInput = document.getElementById('prompt-input');
const modelSelect = document.getElementById('model-select');
const formatSelect = document.getElementById('format-select');
const generateBtn = document.getElementById('generate-btn');
const outputSection = document.getElementById('output-section');
const outputText = document.getElementById('output-text');
const statusMessage = document.getElementById('status-message');
const loadingSpinner = document.getElementById('loading-spinner');
const copyBtn = document.getElementById('copy-btn');
const downloadBtn = document.getElementById('download-btn');

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    generateBtn.addEventListener('click', generateWorld);
    copyBtn.addEventListener('click', copyToClipboard);
    downloadBtn.addEventListener('click', downloadFile);
    
    // Enter key to generate
    promptInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            generateWorld();
        }
    });
});

// Set example prompt
function setPrompt(prompt) {
    promptInput.value = prompt;
    promptInput.focus();
    
    // Add a nice animation
    promptInput.style.transform = 'scale(1.02)';
    setTimeout(() => {
        promptInput.style.transform = 'scale(1)';
    }, 200);
}

// Generate world function
async function generateWorld() {
    const prompt = promptInput.value.trim();
    
    if (!prompt) {
        showStatus('Please enter a prompt to generate your world!', 'error');
        promptInput.focus();
        return;
    }
    
    // Show loading state
    setLoadingState(true);
    hideOutput();
    showStatus('', '');
    
    try {
        const model = modelSelect.value;
        const format = formatSelect.value;
        
        // Call the Python backend
        const response = await fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                prompt: prompt,
                model: model,
                format: format
            })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.success) {
            currentWorldData = result.data;
            currentFilename = result.filename;
            
            // Display the generated world
            displayOutput(result.data, format);
            showStatus(`✅ Successfully generated "${result.level_name}"!`, 'success');
        } else {
            throw new Error(result.error || 'Unknown error occurred');
        }
        
    } catch (error) {
        console.error('Error generating world:', error);
        showStatus(`❌ Error: ${error.message}`, 'error');
        
        // Fallback: try to call Python script directly (for development)
        if (error.message.includes('fetch')) {
            await generateWorldFallback(prompt, modelSelect.value, formatSelect.value);
        }
    } finally {
        setLoadingState(false);
    }
}

// Fallback method - call Python script directly
async function generateWorldFallback(prompt, model, format) {
    try {
        showStatus('🔄 Using fallback method...', '');
        
        // This would typically be handled by a backend API
        // For now, we'll simulate the response
        const simulatedData = generateSimulatedWorld(prompt);
        
        currentWorldData = simulatedData;
        currentFilename = `generated_world.${format}`;
        
        displayOutput(simulatedData, format);
        showStatus('✅ World generated using fallback method!', 'success');
        
    } catch (error) {
        showStatus(`❌ Fallback failed: ${error.message}`, 'error');
    }
}

// Generate simulated world data (for demo purposes)
function generateSimulatedWorld(prompt) {
    const promptLower = prompt.toLowerCase();
    
    // Detect environment
    let envType = 'forest';
    if (promptLower.includes('desert')) envType = 'desert';
    else if (promptLower.includes('haunted') || promptLower.includes('mansion')) envType = 'haunted';
    else if (promptLower.includes('space') || promptLower.includes('station')) envType = 'space';
    else if (promptLower.includes('underwater') || promptLower.includes('ocean')) envType = 'ocean';
    
    // Extract quest count
    let questCount = 1;
    const numbers = prompt.match(/\d+/g);
    if (numbers) questCount = Math.min(parseInt(numbers[0]), 5);
    
    return {
        metadata: {
            level_name: `Generated ${envType.charAt(0).toUpperCase() + envType.slice(1)} World`,
            description: `An immersive ${envType} adventure: ${prompt}`,
            difficulty: "medium",
            estimated_playtime: "30-45 minutes",
            theme: envType
        },
        environment: {
            type: envType,
            setting: `A ${envType} environment with unique challenges`,
            terrain: getTerrainForEnv(envType),
            lighting: "dynamic",
            weather: "clear",
            atmosphere: "mysterious",
            size: "medium",
            assets: getAssetsForEnv(envType)
        },
        quests: generateQuests(questCount, envType),
        npcs: generateNPCs(envType),
        physics: {
            player_abilities: ["walk", "run", "jump", "interact"],
            movement_speed: 5.0,
            jump_height: 2.0,
            combat_system: "action_based",
            interaction_mechanics: ["pickup_items", "talk_to_npcs", "activate_objects"],
            special_mechanics: ["quest_tracking", "inventory_system"]
        },
        win_conditions: ["Complete all main quests"],
        lose_conditions: ["Player health reaches 0"],
        assets_required: {
            models: [`${envType}_props`, "player_character", "interactive_objects"],
            textures: [`${envType}_textures`, "ui_elements"],
            sounds: ["ambient_sounds", "ui_sounds", "footsteps"],
            effects: ["particle_effects", "lighting_effects"],
            animations: ["player_animations", "npc_animations"]
        }
    };
}

// Helper functions for simulated data
function getTerrainForEnv(envType) {
    const terrainMap = {
        forest: ["grass", "dirt_paths", "rocky_areas", "streams"],
        desert: ["sand_dunes", "rocky_outcrops", "oasis", "canyons"],
        haunted: ["old_floorboards", "stone_corridors", "dusty_rooms"],
        space: ["metal_floors", "corridors", "observation_decks"],
        ocean: ["water", "coral_reefs", "sandy_bottom", "rock_formations"]
    };
    return terrainMap[envType] || ["grass", "dirt", "rocks"];
}

function getAssetsForEnv(envType) {
    const assetMap = {
        forest: ["trees", "bushes", "rocks", "flowers", "wildlife"],
        desert: ["cacti", "sand_dunes", "rocks", "palm_trees", "ruins"],
        haunted: ["furniture", "paintings", "candles", "cobwebs", "mirrors"],
        space: ["control_panels", "screens", "machinery", "windows", "doors"],
        ocean: ["coral", "seaweed", "fish", "treasure", "shipwrecks"]
    };
    return assetMap[envType] || ["generic_props"];
}

function generateQuests(count, envType) {
    const quests = [];
    for (let i = 0; i < count; i++) {
        quests.push({
            id: `quest_${i + 1}`,
            name: `${envType.charAt(0).toUpperCase() + envType.slice(1)} Quest ${i + 1}`,
            type: i === 0 ? "main" : "side",
            objective: `Complete objective ${i + 1} in the ${envType}`,
            description: `An important task that must be completed`,
            requirements: i === 0 ? [] : [`complete_quest_${i}`],
            rewards: {
                experience: 100 + (i * 50),
                gold: 50 + (i * 25),
                items: [`quest_${i + 1}_reward`]
            },
            location: envType,
            estimated_time: `${10 + (i * 5)} minutes`
        });
    }
    return quests;
}

function generateNPCs(envType) {
    const npcMap = {
        forest: [{ name: "Forest Guardian", type: "friendly", role: "guide" }],
        desert: [{ name: "Desert Nomad", type: "neutral", role: "trader" }],
        haunted: [{ name: "Restless Spirit", type: "friendly", role: "quest_giver" }],
        space: [{ name: "Station Commander", type: "friendly", role: "authority" }],
        ocean: [{ name: "Sea Creature", type: "neutral", role: "inhabitant" }]
    };
    
    const npcTemplate = npcMap[envType] || [{ name: "Mysterious Stranger", type: "neutral", role: "guide" }];
    
    return npcTemplate.map((npc, i) => ({
        id: `npc_${i + 1}`,
        name: npc.name,
        role: npc.role,
        type: npc.type,
        location: envType,
        dialogue: [`Hello, traveler!`, `Welcome to the ${envType}!`],
        behavior: "stationary_helpful",
        stats: { health: 100, attack: 0, defense: 10 },
        inventory: ["common_item"]
    }));
}

// Display output
function displayOutput(data, format) {
    let formattedData;
    
    if (format === 'yaml') {
        // Simple YAML formatting (basic implementation)
        formattedData = JSON.stringify(data, null, 2)
            .replace(/"/g, '')
            .replace(/,/g, '')
            .replace(/\{/g, '')
            .replace(/\}/g, '')
            .replace(/\[/g, '')
            .replace(/\]/g, '');
    } else {
        formattedData = JSON.stringify(data, null, 2);
    }
    
    outputText.textContent = formattedData;
    outputSection.style.display = 'block';
    
    // Smooth scroll to output
    outputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Utility functions
function setLoadingState(loading) {
    generateBtn.disabled = loading;
    if (loading) {
        loadingSpinner.style.display = 'flex';
        generateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    } else {
        loadingSpinner.style.display = 'none';
        generateBtn.innerHTML = '<i class="fas fa-rocket"></i> Generate World';
    }
}

function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
    statusMessage.style.display = message ? 'block' : 'none';
}

function hideOutput() {
    outputSection.style.display = 'none';
}

function copyToClipboard() {
    if (currentWorldData) {
        const format = formatSelect.value;
        let textToCopy;
        
        if (format === 'yaml') {
            textToCopy = outputText.textContent;
        } else {
            textToCopy = JSON.stringify(currentWorldData, null, 2);
        }
        
        navigator.clipboard.writeText(textToCopy).then(() => {
            showStatus('✅ Copied to clipboard!', 'success');
            setTimeout(() => showStatus('', ''), 2000);
        }).catch(() => {
            showStatus('❌ Failed to copy to clipboard', 'error');
        });
    }
}

function downloadFile() {
    if (currentWorldData) {
        const format = formatSelect.value;
        let content, mimeType;
        
        if (format === 'yaml') {
            content = outputText.textContent;
            mimeType = 'text/yaml';
        } else {
            content = JSON.stringify(currentWorldData, null, 2);
            mimeType = 'application/json';
        }
        
        const blob = new Blob([content], { type: mimeType });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = currentFilename || `generated_world.${format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showStatus('✅ File downloaded!', 'success');
        setTimeout(() => showStatus('', ''), 2000);
    }
}
