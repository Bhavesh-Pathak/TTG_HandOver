// TTG Genesis 3D Preview System using Three.js

class ThreePreview {
    constructor() {
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.worldObjects = [];
        this.isWireframe = false;
        this.animationId = null;
        
        this.init();
    }

    init() {
        this.setupScene();
        this.setupCamera();
        this.setupRenderer();
        this.setupLighting();
        this.setupControls();
        this.animate();
        
        // Setup event listeners
        this.setupEventListeners();
    }

    setupScene() {
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0x1a1a1a);
        this.scene.fog = new THREE.Fog(0x1a1a1a, 50, 200);
    }

    setupCamera() {
        const canvas = document.getElementById('threeCanvas');
        const aspect = canvas.clientWidth / canvas.clientHeight;
        this.camera = new THREE.PerspectiveCamera(75, aspect, 0.1, 1000);
        this.camera.position.set(20, 15, 20);
        this.camera.lookAt(0, 0, 0);
    }

    setupRenderer() {
        const canvas = document.getElementById('threeCanvas');
        this.renderer = new THREE.WebGLRenderer({ 
            canvas: canvas,
            antialias: true,
            alpha: true 
        });
        this.renderer.setSize(canvas.clientWidth, canvas.clientHeight);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.renderer.outputEncoding = THREE.sRGBEncoding;
        this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
        this.renderer.toneMappingExposure = 1.2;
    }

    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
        this.scene.add(ambientLight);

        // Directional light (sun)
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 50, 25);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        directionalLight.shadow.camera.near = 0.5;
        directionalLight.shadow.camera.far = 200;
        directionalLight.shadow.camera.left = -50;
        directionalLight.shadow.camera.right = 50;
        directionalLight.shadow.camera.top = 50;
        directionalLight.shadow.camera.bottom = -50;
        this.scene.add(directionalLight);

        // Point lights for atmosphere
        const pointLight1 = new THREE.PointLight(0x00ffff, 0.5, 30);
        pointLight1.position.set(-10, 10, -10);
        this.scene.add(pointLight1);

        const pointLight2 = new THREE.PointLight(0xff00ff, 0.3, 25);
        pointLight2.position.set(15, 8, 15);
        this.scene.add(pointLight2);
    }

    setupControls() {
        // Simple orbit controls implementation
        this.controls = {
            mouseDown: false,
            mouseX: 0,
            mouseY: 0,
            targetX: 0,
            targetY: 0,
            distance: 35,
            minDistance: 10,
            maxDistance: 100
        };
    }

    setupEventListeners() {
        const canvas = document.getElementById('threeCanvas');
        
        // Mouse controls
        canvas.addEventListener('mousedown', (e) => {
            this.controls.mouseDown = true;
            this.controls.mouseX = e.clientX;
            this.controls.mouseY = e.clientY;
        });

        canvas.addEventListener('mousemove', (e) => {
            if (!this.controls.mouseDown) return;
            
            const deltaX = e.clientX - this.controls.mouseX;
            const deltaY = e.clientY - this.controls.mouseY;
            
            this.controls.targetX += deltaX * 0.01;
            this.controls.targetY += deltaY * 0.01;
            
            this.controls.mouseX = e.clientX;
            this.controls.mouseY = e.clientY;
        });

        canvas.addEventListener('mouseup', () => {
            this.controls.mouseDown = false;
        });

        // Zoom with mouse wheel
        canvas.addEventListener('wheel', (e) => {
            e.preventDefault();
            this.controls.distance += e.deltaY * 0.01;
            this.controls.distance = Math.max(this.controls.minDistance, 
                Math.min(this.controls.maxDistance, this.controls.distance));
        });

        // Window resize
        window.addEventListener('resize', () => {
            this.onWindowResize();
        });

        // Preview controls
        document.getElementById('resetView')?.addEventListener('click', () => {
            this.resetView();
        });

        document.getElementById('toggleWireframe')?.addEventListener('click', () => {
            this.toggleWireframe();
        });
    }

    generateWorldPreview(worldData) {
        this.clearScene();
        
        try {
            // Create ground plane
            this.createGround(worldData);
            
            // Create environment based on world data
            this.createEnvironment(worldData);
            
            // Add NPCs
            if (worldData.npcs) {
                this.createNPCs(worldData.npcs);
            }
            
            // Add quest markers
            if (worldData.quests) {
                this.createQuestMarkers(worldData.quests);
            }
            
            // Add structures
            if (worldData.environment && worldData.environment.structures) {
                this.createStructures(worldData.environment.structures);
            }
            
            // Add particles for atmosphere
            this.createParticles(worldData);
            
        } catch (error) {
            console.error('Error generating 3D preview:', error);
            this.createFallbackScene();
        }
    }

    createGround(worldData) {
        const groundSize = 100;
        const groundGeometry = new THREE.PlaneGeometry(groundSize, groundSize, 32, 32);
        
        // Create ground material based on world theme
        const theme = this.detectWorldTheme(worldData);
        const groundMaterial = this.createGroundMaterial(theme);
        
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        
        // Add some height variation
        const vertices = ground.geometry.attributes.position.array;
        for (let i = 0; i < vertices.length; i += 3) {
            vertices[i + 2] = Math.random() * 2 - 1; // Y coordinate (height)
        }
        ground.geometry.attributes.position.needsUpdate = true;
        ground.geometry.computeVertexNormals();
        
        this.scene.add(ground);
        this.worldObjects.push(ground);
    }

    createGroundMaterial(theme) {
        const materialMap = {
            forest: new THREE.MeshLambertMaterial({ color: 0x2d5016 }),
            desert: new THREE.MeshLambertMaterial({ color: 0xdaa520 }),
            ocean: new THREE.MeshLambertMaterial({ color: 0x006994 }),
            space: new THREE.MeshLambertMaterial({ color: 0x191970 }),
            city: new THREE.MeshLambertMaterial({ color: 0x2f4f4f }),
            fantasy: new THREE.MeshLambertMaterial({ color: 0x4b0082 }),
            default: new THREE.MeshLambertMaterial({ color: 0x333333 })
        };
        
        return materialMap[theme] || materialMap.default;
    }

    createEnvironment(worldData) {
        const theme = this.detectWorldTheme(worldData);
        
        switch (theme) {
            case 'forest':
                this.createForestEnvironment();
                break;
            case 'desert':
                this.createDesertEnvironment();
                break;
            case 'city':
                this.createCityEnvironment();
                break;
            case 'space':
                this.createSpaceEnvironment();
                break;
            default:
                this.createGenericEnvironment();
        }
    }

    createForestEnvironment() {
        // Create trees
        for (let i = 0; i < 20; i++) {
            const tree = this.createTree();
            tree.position.set(
                (Math.random() - 0.5) * 80,
                0,
                (Math.random() - 0.5) * 80
            );
            this.scene.add(tree);
            this.worldObjects.push(tree);
        }
    }

    createTree() {
        const group = new THREE.Group();
        
        // Trunk
        const trunkGeometry = new THREE.CylinderGeometry(0.5, 0.8, 8, 8);
        const trunkMaterial = new THREE.MeshLambertMaterial({ color: 0x8B4513 });
        const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
        trunk.position.y = 4;
        trunk.castShadow = true;
        group.add(trunk);
        
        // Leaves
        const leavesGeometry = new THREE.SphereGeometry(4, 8, 6);
        const leavesMaterial = new THREE.MeshLambertMaterial({ color: 0x228B22 });
        const leaves = new THREE.Mesh(leavesGeometry, leavesMaterial);
        leaves.position.y = 10;
        leaves.castShadow = true;
        group.add(leaves);
        
        return group;
    }

    createDesertEnvironment() {
        // Create cacti and rocks
        for (let i = 0; i < 15; i++) {
            if (Math.random() > 0.5) {
                const cactus = this.createCactus();
                cactus.position.set(
                    (Math.random() - 0.5) * 80,
                    0,
                    (Math.random() - 0.5) * 80
                );
                this.scene.add(cactus);
                this.worldObjects.push(cactus);
            } else {
                const rock = this.createRock();
                rock.position.set(
                    (Math.random() - 0.5) * 80,
                    0,
                    (Math.random() - 0.5) * 80
                );
                this.scene.add(rock);
                this.worldObjects.push(rock);
            }
        }
    }

    createCactus() {
        const geometry = new THREE.CylinderGeometry(1, 1.2, 6, 8);
        const material = new THREE.MeshLambertMaterial({ color: 0x228B22 });
        const cactus = new THREE.Mesh(geometry, material);
        cactus.position.y = 3;
        cactus.castShadow = true;
        return cactus;
    }

    createRock() {
        const geometry = new THREE.DodecahedronGeometry(Math.random() * 2 + 1);
        const material = new THREE.MeshLambertMaterial({ color: 0x696969 });
        const rock = new THREE.Mesh(geometry, material);
        rock.position.y = 1;
        rock.castShadow = true;
        return rock;
    }

    createCityEnvironment() {
        // Create buildings
        for (let i = 0; i < 12; i++) {
            const building = this.createBuilding();
            building.position.set(
                (Math.random() - 0.5) * 60,
                0,
                (Math.random() - 0.5) * 60
            );
            this.scene.add(building);
            this.worldObjects.push(building);
        }
    }

    createBuilding() {
        const height = Math.random() * 20 + 10;
        const width = Math.random() * 4 + 3;
        const depth = Math.random() * 4 + 3;
        
        const geometry = new THREE.BoxGeometry(width, height, depth);
        const material = new THREE.MeshLambertMaterial({ 
            color: new THREE.Color().setHSL(0.6, 0.2, Math.random() * 0.3 + 0.3)
        });
        const building = new THREE.Mesh(geometry, material);
        building.position.y = height / 2;
        building.castShadow = true;
        return building;
    }

    createSpaceEnvironment() {
        // Create asteroids and space structures
        for (let i = 0; i < 10; i++) {
            const asteroid = this.createAsteroid();
            asteroid.position.set(
                (Math.random() - 0.5) * 100,
                Math.random() * 20,
                (Math.random() - 0.5) * 100
            );
            this.scene.add(asteroid);
            this.worldObjects.push(asteroid);
        }
        
        // Add stars
        this.createStarField();
    }

    createAsteroid() {
        const geometry = new THREE.IcosahedronGeometry(Math.random() * 3 + 1, 1);
        const material = new THREE.MeshLambertMaterial({ color: 0x444444 });
        const asteroid = new THREE.Mesh(geometry, material);
        asteroid.castShadow = true;
        return asteroid;
    }

    createStarField() {
        const starsGeometry = new THREE.BufferGeometry();
        const starsMaterial = new THREE.PointsMaterial({ color: 0xFFFFFF, size: 2 });
        
        const starsVertices = [];
        for (let i = 0; i < 1000; i++) {
            starsVertices.push(
                (Math.random() - 0.5) * 2000,
                (Math.random() - 0.5) * 2000,
                (Math.random() - 0.5) * 2000
            );
        }
        
        starsGeometry.setAttribute('position', new THREE.Float32BufferAttribute(starsVertices, 3));
        const stars = new THREE.Points(starsGeometry, starsMaterial);
        this.scene.add(stars);
        this.worldObjects.push(stars);
    }

    createGenericEnvironment() {
        // Create generic objects
        for (let i = 0; i < 10; i++) {
            const obj = this.createGenericObject();
            obj.position.set(
                (Math.random() - 0.5) * 60,
                0,
                (Math.random() - 0.5) * 60
            );
            this.scene.add(obj);
            this.worldObjects.push(obj);
        }
    }

    createGenericObject() {
        const geometries = [
            new THREE.BoxGeometry(2, 2, 2),
            new THREE.SphereGeometry(1.5, 8, 6),
            new THREE.ConeGeometry(1, 3, 8),
            new THREE.CylinderGeometry(1, 1, 3, 8)
        ];
        
        const geometry = geometries[Math.floor(Math.random() * geometries.length)];
        const material = new THREE.MeshLambertMaterial({ 
            color: new THREE.Color().setHSL(Math.random(), 0.7, 0.5)
        });
        const obj = new THREE.Mesh(geometry, material);
        obj.position.y = 1.5;
        obj.castShadow = true;
        return obj;
    }

    createNPCs(npcs) {
        npcs.forEach((npc, index) => {
            const npcMesh = this.createNPCMesh(npc);
            npcMesh.position.set(
                (Math.random() - 0.5) * 40,
                0,
                (Math.random() - 0.5) * 40
            );
            this.scene.add(npcMesh);
            this.worldObjects.push(npcMesh);
        });
    }

    createNPCMesh(npc) {
        const group = new THREE.Group();
        
        // Body
        const bodyGeometry = new THREE.CapsuleGeometry(0.5, 1.5, 4, 8);
        const bodyMaterial = new THREE.MeshLambertMaterial({ color: 0x4169E1 });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.position.y = 1;
        body.castShadow = true;
        group.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.4, 8, 6);
        const headMaterial = new THREE.MeshLambertMaterial({ color: 0xFFDBB3 });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        head.position.y = 2.2;
        head.castShadow = true;
        group.add(head);
        
        return group;
    }

    createQuestMarkers(quests) {
        quests.forEach((quest, index) => {
            const marker = this.createQuestMarker();
            marker.position.set(
                (Math.random() - 0.5) * 50,
                5,
                (Math.random() - 0.5) * 50
            );
            this.scene.add(marker);
            this.worldObjects.push(marker);
        });
    }

    createQuestMarker() {
        const geometry = new THREE.ConeGeometry(0.5, 2, 6);
        const material = new THREE.MeshLambertMaterial({ 
            color: 0xFFD700,
            emissive: 0x444400
        });
        const marker = new THREE.Mesh(geometry, material);
        marker.castShadow = true;
        
        // Add floating animation
        marker.userData = { 
            originalY: marker.position.y,
            time: Math.random() * Math.PI * 2
        };
        
        return marker;
    }

    createParticles(worldData) {
        const theme = this.detectWorldTheme(worldData);
        
        if (theme === 'forest' || theme === 'fantasy') {
            this.createMagicalParticles();
        } else if (theme === 'space') {
            this.createSpaceDust();
        }
    }

    createMagicalParticles() {
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesMaterial = new THREE.PointsMaterial({
            color: 0x00ffff,
            size: 0.5,
            transparent: true,
            opacity: 0.7
        });
        
        const particlesVertices = [];
        for (let i = 0; i < 100; i++) {
            particlesVertices.push(
                (Math.random() - 0.5) * 100,
                Math.random() * 20,
                (Math.random() - 0.5) * 100
            );
        }
        
        particlesGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlesVertices, 3));
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        this.scene.add(particles);
        this.worldObjects.push(particles);
    }

    createSpaceDust() {
        const particlesGeometry = new THREE.BufferGeometry();
        const particlesMaterial = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 0.2,
            transparent: true,
            opacity: 0.5
        });
        
        const particlesVertices = [];
        for (let i = 0; i < 500; i++) {
            particlesVertices.push(
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200,
                (Math.random() - 0.5) * 200
            );
        }
        
        particlesGeometry.setAttribute('position', new THREE.Float32BufferAttribute(particlesVertices, 3));
        const particles = new THREE.Points(particlesGeometry, particlesMaterial);
        this.scene.add(particles);
        this.worldObjects.push(particles);
    }

    detectWorldTheme(worldData) {
        const text = JSON.stringify(worldData).toLowerCase();
        
        if (text.includes('forest') || text.includes('tree') || text.includes('nature')) return 'forest';
        if (text.includes('desert') || text.includes('sand') || text.includes('dune')) return 'desert';
        if (text.includes('ocean') || text.includes('sea') || text.includes('water')) return 'ocean';
        if (text.includes('space') || text.includes('star') || text.includes('galaxy')) return 'space';
        if (text.includes('city') || text.includes('urban') || text.includes('building')) return 'city';
        if (text.includes('magic') || text.includes('fantasy') || text.includes('dragon')) return 'fantasy';
        
        return 'default';
    }

    clearScene() {
        this.worldObjects.forEach(obj => {
            this.scene.remove(obj);
            if (obj.geometry) obj.geometry.dispose();
            if (obj.material) {
                if (Array.isArray(obj.material)) {
                    obj.material.forEach(mat => mat.dispose());
                } else {
                    obj.material.dispose();
                }
            }
        });
        this.worldObjects = [];
    }

    createFallbackScene() {
        // Create a simple fallback scene
        const geometry = new THREE.BoxGeometry(5, 5, 5);
        const material = new THREE.MeshLambertMaterial({ color: 0x00ffff });
        const cube = new THREE.Mesh(geometry, material);
        cube.position.y = 2.5;
        cube.castShadow = true;
        this.scene.add(cube);
        this.worldObjects.push(cube);
        
        // Add text
        const loader = new THREE.FontLoader();
        // Note: In a real implementation, you'd load a font file
        // For now, we'll just add a simple placeholder
    }

    animate() {
        this.animationId = requestAnimationFrame(() => this.animate());
        
        // Update camera position based on controls
        const time = Date.now() * 0.001;
        
        this.camera.position.x = Math.cos(this.controls.targetX) * this.controls.distance;
        this.camera.position.z = Math.sin(this.controls.targetX) * this.controls.distance;
        this.camera.position.y = Math.sin(this.controls.targetY) * this.controls.distance * 0.5 + 10;
        this.camera.lookAt(0, 0, 0);
        
        // Animate quest markers
        this.worldObjects.forEach(obj => {
            if (obj.userData && obj.userData.originalY !== undefined) {
                obj.userData.time += 0.02;
                obj.position.y = obj.userData.originalY + Math.sin(obj.userData.time) * 2;
            }
        });
        
        // Animate particles
        this.scene.traverse((child) => {
            if (child instanceof THREE.Points) {
                child.rotation.y += 0.001;
            }
        });
        
        this.renderer.render(this.scene, this.camera);
    }

    resetView() {
        this.controls.targetX = 0;
        this.controls.targetY = 0;
        this.controls.distance = 35;
    }

    toggleWireframe() {
        this.isWireframe = !this.isWireframe;
        
        this.scene.traverse((child) => {
            if (child instanceof THREE.Mesh && child.material) {
                if (Array.isArray(child.material)) {
                    child.material.forEach(mat => {
                        mat.wireframe = this.isWireframe;
                    });
                } else {
                    child.material.wireframe = this.isWireframe;
                }
            }
        });
    }

    onWindowResize() {
        const canvas = document.getElementById('threeCanvas');
        if (!canvas) return;
        
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    dispose() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        
        this.clearScene();
        
        if (this.renderer) {
            this.renderer.dispose();
        }
    }
}

// Add to TTGEnhanced class
TTGEnhanced.prototype.generate3DPreview = function(worldData) {
    if (!this.threePreview) {
        this.threePreview = new ThreePreview();
    }
    
    this.threePreview.generateWorldPreview(worldData);
};

// Initialize 3D preview when needed
TTGEnhanced.prototype.init3DPreview = function() {
    if (!this.threePreview && document.getElementById('threeCanvas')) {
        this.threePreview = new ThreePreview();
    }
};
