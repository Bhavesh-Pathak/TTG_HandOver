// TTG Genesis Enhanced JavaScript

class TTGEnhanced {
    constructor() {
        this.currentSection = 'generator';
        this.worlds = [];
        this.history = [];
        this.ue5Connected = false;
        this.currentWorldId = null;
        this.generationInProgress = false;
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadWorlds();
        this.loadHistory();
        this.checkUE5Connection();
        this.updateUI();
    }

    setupEventListeners() {
        // Navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const section = e.currentTarget.dataset.section;
                this.switchSection(section);
            });
        });

        // Project type radio buttons
        document.querySelectorAll('input[name="projectType"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                const existingPath = document.getElementById('existingProjectPath');
                if (e.target.value === 'existing') {
                    existingPath.style.display = 'block';
                } else {
                    existingPath.style.display = 'none';
                }
            });
        });

        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.generateWorld();
        });

        // Browse buttons
        document.getElementById('browseProject')?.addEventListener('click', () => {
            this.browseForProject();
        });

        // Output tabs
        document.querySelectorAll('.output-tab').forEach(tab => {
            tab.addEventListener('click', (e) => {
                this.switchOutputTab(e.target.dataset.tab);
            });
        });

        // Modal close
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', () => {
                this.closeModal();
            });
        });

        // Delete confirmation
        document.getElementById('confirmDelete')?.addEventListener('click', () => {
            this.confirmDeleteWorld();
        });

        document.getElementById('cancelDelete')?.addEventListener('click', () => {
            this.closeModal();
        });

        // Settings
        document.getElementById('testConnection')?.addEventListener('click', () => {
            this.testUE5Connection();
        });

        document.getElementById('autoDetect')?.addEventListener('click', () => {
            this.autoDetectUE5();
        });

        // Gallery controls
        document.getElementById('refreshGallery')?.addEventListener('click', () => {
            this.loadWorlds();
        });

        document.getElementById('gallerySearch')?.addEventListener('input', (e) => {
            this.filterWorlds(e.target.value);
        });

        document.getElementById('galleryFilter')?.addEventListener('change', (e) => {
            this.filterWorldsByType(e.target.value);
        });
    }

    switchSection(sectionName) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');

        // Update sections
        document.querySelectorAll('.main-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(`${sectionName}-section`).classList.add('active');

        this.currentSection = sectionName;

        // Load section-specific data
        if (sectionName === 'gallery') {
            this.loadWorlds();
        } else if (sectionName === 'history') {
            this.loadHistory();
        }
    }

    async generateWorld() {
        if (this.generationInProgress) return;

        const prompt = document.getElementById('prompt-input').value.trim();
        if (!prompt) {
            this.showNotification('Please enter a world description', 'error');
            return;
        }

        this.generationInProgress = true;
        this.showProgressPanel();
        this.updateGenerateButton(true);

        try {
            // Get generation options
            const options = this.getGenerationOptions();
            
            // Step 1: Parse prompt
            this.updateProgressStep('parsing', 'active', 'Analyzing your prompt...');
            await this.sleep(1000);
            
            // Step 2: Generate world data
            this.updateProgressStep('parsing', 'completed', 'Complete');
            this.updateProgressStep('generating', 'active', 'Creating world data...');
            
            const worldData = await this.callAPI('/api/generate', {
                prompt: prompt,
                options: options
            });
            
            await this.sleep(2000);
            
            // Step 3: Generate C++ if enabled
            if (options.generateCpp) {
                this.updateProgressStep('generating', 'completed', 'Complete');
                this.updateProgressStep('cpp', 'active', 'Generating C++ code...');
                
                const cppData = await this.callAPI('/api/generate-cpp', {
                    worldData: worldData,
                    worldName: this.extractWorldName(prompt)
                });
                
                await this.sleep(1500);
            }
            
            // Step 4: UE5 Integration if enabled
            if (options.generateBlueprints || options.generateLevel) {
                this.updateProgressStep('cpp', 'completed', 'Complete');
                this.updateProgressStep('ue5', 'active', 'Integrating with UE5...');
                
                const ue5Data = await this.callAPI('/api/ue5-integration', {
                    worldData: worldData,
                    options: options
                });
                
                await this.sleep(2000);
            }
            
            // Step 5: Generate previews
            if (options.generate3DPreview || options.generateScreenshots) {
                this.updateProgressStep('ue5', 'completed', 'Complete');
                this.updateProgressStep('preview', 'active', 'Creating previews...');
                
                const previewData = await this.callAPI('/api/generate-previews', {
                    worldData: worldData,
                    options: options
                });
                
                await this.sleep(1500);
            }
            
            // Complete
            this.updateProgressStep('preview', 'completed', 'Complete');
            
            // Save world and update UI
            const world = {
                id: this.generateId(),
                name: this.extractWorldName(prompt),
                prompt: prompt,
                data: worldData,
                options: options,
                createdAt: new Date(),
                status: this.getWorldStatus(options)
            };
            
            this.worlds.unshift(world);
            this.addToHistory(world, 'success');
            this.saveWorlds();
            
            // Show results
            this.showOutput(world);
            this.showNotification('World generated successfully!', 'success');
            
        } catch (error) {
            console.error('Generation error:', error);
            this.showNotification('Generation failed: ' + error.message, 'error');
            this.addToHistory({ prompt: prompt }, 'error');
        } finally {
            this.generationInProgress = false;
            this.updateGenerateButton(false);
            setTimeout(() => {
                this.hideProgressPanel();
            }, 2000);
        }
    }

    getGenerationOptions() {
        return {
            includeQuests: document.getElementById('includeQuests').checked,
            includeNPCs: document.getElementById('includeNPCs').checked,
            includeEnvironment: document.getElementById('includeEnvironment').checked,
            includeCombat: document.getElementById('includeCombat').checked,
            generateCpp: document.getElementById('generateCpp').checked,
            generateBlueprints: document.getElementById('generateBlueprints').checked,
            generateLevel: document.getElementById('generateLevel').checked,
            autoCompile: document.getElementById('autoCompile').checked,
            projectType: document.querySelector('input[name="projectType"]:checked').value,
            projectPath: document.getElementById('projectPath').value,
            automationLevel: document.querySelector('input[name="automationLevel"]:checked').value,
            generate3DPreview: document.getElementById('generate3DPreview').checked,
            generateScreenshots: document.getElementById('generateScreenshots').checked
        };
    }

    showProgressPanel() {
        const panel = document.getElementById('progressPanel');
        panel.style.display = 'block';
        
        // Reset all steps
        document.querySelectorAll('.progress-step').forEach(step => {
            step.classList.remove('active', 'completed');
            step.querySelector('.step-status').textContent = 'Waiting...';
            step.querySelector('.progress-bar').style.width = '0%';
        });
    }

    hideProgressPanel() {
        document.getElementById('progressPanel').style.display = 'none';
    }

    updateProgressStep(stepName, status, message) {
        const step = document.querySelector(`[data-step="${stepName}"]`);
        if (!step) return;

        step.classList.remove('active', 'completed');
        if (status !== 'waiting') {
            step.classList.add(status);
        }

        step.querySelector('.step-status').textContent = message;
        
        if (status === 'active') {
            step.querySelector('.progress-bar').style.width = '100%';
        } else if (status === 'completed') {
            step.querySelector('.progress-bar').style.width = '100%';
        }
    }

    updateGenerateButton(loading) {
        const btn = document.getElementById('generate-btn');
        const btnText = btn.querySelector('.btn-text');
        const btnLoading = btn.querySelector('.btn-loading');

        if (loading) {
            btnText.style.display = 'none';
            btnLoading.style.display = 'flex';
            btn.disabled = true;
        } else {
            btnText.style.display = 'block';
            btnLoading.style.display = 'none';
            btn.disabled = false;
        }
    }

    showOutput(world) {
        const outputSection = document.getElementById('output-section');
        outputSection.style.display = 'block';

        // Populate JSON tab
        document.getElementById('jsonOutput').textContent = JSON.stringify(world.data, null, 2);

        // Switch to preview tab
        this.switchOutputTab('preview');

        // Generate 3D preview if enabled
        if (world.options.generate3DPreview) {
            this.generate3DPreview(world.data);
        }

        // Load screenshots if available
        if (world.options.generateScreenshots) {
            this.loadScreenshots(world.id);
        }
    }

    switchOutputTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.output-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update tab content
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    async callAPI(endpoint, data) {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`API call failed: ${response.statusText}`);
        }

        return await response.json();
    }

    // Utility functions
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    extractWorldName(prompt) {
        // Simple extraction - could be enhanced with NLP
        const words = prompt.split(' ').slice(0, 3);
        return words.join(' ').replace(/[^a-zA-Z0-9\s]/g, '').trim() || 'Generated World';
    }

    getWorldStatus(options) {
        if (options.generateBlueprints && options.generateLevel) {
            return 'ue5-ready';
        } else if (options.generateCpp) {
            return 'cpp-ready';
        } else {
            return 'json-only';
        }
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check' : type === 'error' ? 'exclamation-triangle' : 'info'}"></i>
            <span>${message}</span>
        `;

        // Add to page
        document.body.appendChild(notification);

        // Auto remove
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // Data management
    loadWorlds() {
        const saved = localStorage.getItem('ttg-worlds');
        this.worlds = saved ? JSON.parse(saved) : [];
        this.updateWorldCount();
        this.renderWorldGallery();
    }

    saveWorlds() {
        localStorage.setItem('ttg-worlds', JSON.stringify(this.worlds));
        this.updateWorldCount();
    }

    updateWorldCount() {
        const count = document.getElementById('worldCount');
        if (count) {
            count.textContent = this.worlds.length;
        }
    }

    loadHistory() {
        const saved = localStorage.getItem('ttg-history');
        this.history = saved ? JSON.parse(saved) : [];
        this.renderHistory();
    }

    addToHistory(world, status) {
        this.history.unshift({
            id: this.generateId(),
            world: world,
            status: status,
            timestamp: new Date(),
            generationTime: Math.floor(Math.random() * 60) + 15 // Mock generation time
        });
        
        // Keep only last 50 entries
        this.history = this.history.slice(0, 50);
        localStorage.setItem('ttg-history', JSON.stringify(this.history));
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.ttgEnhanced = new TTGEnhanced();
});

// Global functions for backward compatibility
function setPrompt(text) {
    document.getElementById('prompt-input').value = text;
}

function switchSection(sectionName) {
    if (window.ttgEnhanced) {
        window.ttgEnhanced.switchSection(sectionName);
    }
}

// Extended TTGEnhanced class methods
TTGEnhanced.prototype.renderWorldGallery = function() {
    const gallery = document.getElementById('galleryGrid');
    const emptyState = document.getElementById('galleryEmpty');

    if (this.worlds.length === 0) {
        gallery.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    gallery.style.display = 'grid';
    emptyState.style.display = 'none';

    gallery.innerHTML = this.worlds.map(world => `
        <div class="world-card" data-world-id="${world.id}">
            <div class="world-thumbnail">
                <img src="data:image/svg+xml,${this.generateWorldThumbnail(world)}" alt="${world.name}">
                <div class="world-overlay">
                    <button class="overlay-btn" onclick="ttgEnhanced.previewWorld('${world.id}')" title="Preview">
                        <i class="fas fa-eye"></i>
                    </button>
                    <button class="overlay-btn" onclick="ttgEnhanced.editWorld('${world.id}')" title="Edit">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="overlay-btn delete" onclick="ttgEnhanced.deleteWorld('${world.id}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            <div class="world-info">
                <h3 class="world-title">${world.name}</h3>
                <p class="world-description">${world.prompt.substring(0, 100)}...</p>
                <div class="world-stats">
                    <span class="stat"><i class="fas fa-users"></i> ${this.countNPCs(world.data)} NPCs</span>
                    <span class="stat"><i class="fas fa-tasks"></i> ${this.countQuests(world.data)} Quests</span>
                    <span class="stat"><i class="fas fa-gamepad"></i> ${world.status.replace('-', ' ')}</span>
                </div>
                <div class="world-meta">
                    <span class="world-date">Created: ${this.formatDate(world.createdAt)}</span>
                    <span class="world-status ${world.status}">${this.getStatusLabel(world.status)}</span>
                </div>
            </div>
        </div>
    `).join('');
};

TTGEnhanced.prototype.renderHistory = function() {
    const timeline = document.getElementById('historyTimeline');
    const emptyState = document.getElementById('historyEmpty');

    if (this.history.length === 0) {
        timeline.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }

    timeline.style.display = 'block';
    emptyState.style.display = 'none';

    timeline.innerHTML = this.history.map(entry => `
        <div class="history-item">
            <div class="history-icon ${entry.status}">
                <i class="fas fa-${entry.status === 'success' ? 'check' : 'exclamation-triangle'}"></i>
            </div>
            <div class="history-content">
                <div class="history-header">
                    <h4>${entry.world.name || 'World Generation'}</h4>
                    <span class="history-time">${this.formatDate(entry.timestamp)}</span>
                </div>
                <p class="history-prompt">"${entry.world.prompt}"</p>
                <div class="history-details">
                    <span class="detail-item">
                        <i class="fas fa-clock"></i> ${entry.generationTime}s generation time
                    </span>
                    ${entry.status === 'success' ? `
                        <span class="detail-item">
                            <i class="fas fa-code"></i> C++ Generated
                        </span>
                        <span class="detail-item">
                            <i class="fas fa-gamepad"></i> UE5 Integrated
                        </span>
                    ` : `
                        <span class="detail-item">
                            <i class="fas fa-exclamation-triangle"></i> Generation Failed
                        </span>
                    `}
                </div>
                <div class="history-actions">
                    ${entry.status === 'success' ? `
                        <button class="history-btn" onclick="ttgEnhanced.viewHistoryWorld('${entry.id}')" title="View World">
                            <i class="fas fa-eye"></i>
                        </button>
                    ` : ''}
                    <button class="history-btn" onclick="ttgEnhanced.regenerateFromHistory('${entry.id}')" title="Regenerate">
                        <i class="fas fa-redo"></i>
                    </button>
                    <button class="history-btn" onclick="ttgEnhanced.deleteHistoryEntry('${entry.id}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join('');
};

TTGEnhanced.prototype.generateWorldThumbnail = function(world) {
    // Generate a simple SVG thumbnail based on world data
    const colors = this.getWorldColors(world.data);
    return encodeURIComponent(`
        <svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" style="stop-color:${colors.primary};stop-opacity:1" />
                    <stop offset="100%" style="stop-color:${colors.secondary};stop-opacity:1" />
                </linearGradient>
            </defs>
            <rect width="300" height="200" fill="url(#bg)"/>
            <text x="150" y="100" font-family="Arial" font-size="16" fill="white" text-anchor="middle">${world.name}</text>
        </svg>
    `);
};

TTGEnhanced.prototype.getWorldColors = function(worldData) {
    // Determine colors based on world theme
    const theme = this.detectTheme(worldData);
    const colorMap = {
        forest: { primary: '#2d5016', secondary: '#4a7c59' },
        desert: { primary: '#8b4513', secondary: '#daa520' },
        ocean: { primary: '#006994', secondary: '#4682b4' },
        space: { primary: '#191970', secondary: '#483d8b' },
        city: { primary: '#2f4f4f', secondary: '#696969' },
        fantasy: { primary: '#4b0082', secondary: '#8a2be2' },
        default: { primary: '#333333', secondary: '#666666' }
    };

    return colorMap[theme] || colorMap.default;
};

TTGEnhanced.prototype.detectTheme = function(worldData) {
    const text = JSON.stringify(worldData).toLowerCase();

    if (text.includes('forest') || text.includes('tree') || text.includes('nature')) return 'forest';
    if (text.includes('desert') || text.includes('sand') || text.includes('dune')) return 'desert';
    if (text.includes('ocean') || text.includes('sea') || text.includes('water')) return 'ocean';
    if (text.includes('space') || text.includes('star') || text.includes('galaxy')) return 'space';
    if (text.includes('city') || text.includes('urban') || text.includes('building')) return 'city';
    if (text.includes('magic') || text.includes('fantasy') || text.includes('dragon')) return 'fantasy';

    return 'default';
};

TTGEnhanced.prototype.countNPCs = function(worldData) {
    try {
        return worldData.npcs ? worldData.npcs.length : 0;
    } catch {
        return 0;
    }
};

TTGEnhanced.prototype.countQuests = function(worldData) {
    try {
        return worldData.quests ? worldData.quests.length : 0;
    } catch {
        return 0;
    }
};

TTGEnhanced.prototype.formatDate = function(date) {
    const now = new Date();
    const diff = now - new Date(date);
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return 'Just now';
    if (minutes < 60) return `${minutes} minutes ago`;
    if (hours < 24) return `${hours} hours ago`;
    if (days < 7) return `${days} days ago`;

    return new Date(date).toLocaleDateString();
};

TTGEnhanced.prototype.getStatusLabel = function(status) {
    const labels = {
        'ue5-ready': 'UE5 Integrated',
        'cpp-ready': 'C++ Generated',
        'json-only': 'JSON Only'
    };
    return labels[status] || status;
};

// World management functions
TTGEnhanced.prototype.previewWorld = function(worldId) {
    const world = this.worlds.find(w => w.id === worldId);
    if (!world) return;

    this.currentWorldId = worldId;
    this.showOutput(world);
    this.switchSection('generator');
};

TTGEnhanced.prototype.editWorld = function(worldId) {
    const world = this.worlds.find(w => w.id === worldId);
    if (!world) return;

    // Load world data into generator
    document.getElementById('prompt-input').value = world.prompt;
    this.switchSection('generator');
    this.showNotification('World loaded for editing', 'info');
};

TTGEnhanced.prototype.deleteWorld = function(worldId) {
    const world = this.worlds.find(w => w.id === worldId);
    if (!world) return;

    this.currentWorldId = worldId;
    this.showModal('deleteModal');
};

TTGEnhanced.prototype.confirmDeleteWorld = function() {
    if (!this.currentWorldId) return;

    // Remove from worlds array
    this.worlds = this.worlds.filter(w => w.id !== this.currentWorldId);
    this.saveWorlds();

    // Remove from history
    this.history = this.history.filter(h => h.world.id !== this.currentWorldId);
    localStorage.setItem('ttg-history', JSON.stringify(this.history));

    // Call API to delete files
    this.callAPI('/api/delete-world', { worldId: this.currentWorldId })
        .then(() => {
            this.showNotification('World deleted successfully', 'success');
        })
        .catch(error => {
            console.error('Delete error:', error);
            this.showNotification('Error deleting world files', 'error');
        });

    this.closeModal();
    this.renderWorldGallery();
    this.currentWorldId = null;
};

TTGEnhanced.prototype.showModal = function(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('show');
    }
};

TTGEnhanced.prototype.closeModal = function() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('show');
    });
};
