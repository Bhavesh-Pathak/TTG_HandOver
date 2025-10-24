# 🎮 TTG Genesis - Web Interface

**Beautiful, minimalistic web frontend for the Text-to-Game World Generator**

Transform your imagination into structured game worlds through an elegant web interface with a stunning blurred background and modern UI design.

## ✨ Features

- 🎨 **Beautiful UI**: Minimalistic black & grey design with blurred background
- 🌐 **Web-based**: No command line needed - just type and generate
- 🚀 **Real-time Generation**: Instant world creation from your prompts
- 📱 **Responsive**: Works on desktop, tablet, and mobile
- 💾 **Download & Copy**: Easy export of generated JSON/YAML files
- 🎯 **Example Prompts**: Click-to-use example prompts for inspiration
- 🔄 **Multiple Models**: Support for different AI models (Llama2, Llama3, Mistral)
- 📄 **Format Options**: Generate JSON or YAML output

## 🚀 Quick Start

### Method 1: One-Click Start (Recommended)
```bash
python start_server.py
```
This will automatically:
- Install required dependencies
- Start the web server
- Open your browser to http://localhost:5000

### Method 2: Manual Setup
```bash
# Install dependencies
pip install Flask Flask-CORS requests PyYAML

# Start the server
python app.py
```

Then open your browser to: **http://localhost:5000**

## 🎯 How to Use

1. **Open the Web Interface**: Navigate to http://localhost:5000
2. **Enter Your Prompt**: Type your game world description in the text area
3. **Choose Settings**: Select AI model and output format
4. **Generate**: Click "Generate World" button
5. **Download**: Copy or download your generated world data

### 📝 Example Prompts

Try these example prompts (or click them in the web interface):

```
Create a forest level where the player has to complete 3 quests to save a village
```

```
Design a desert temple with ancient puzzles and treasure hunting mechanics
```

```
Build an underwater city level with swimming mechanics and sea creature NPCs
```

```
Create a haunted mansion with ghost NPCs and mystery-solving quests
```

```
Design a space station level with zero gravity mechanics and alien encounters
```

## 🎨 UI Features

### Design Elements
- **Background**: Stunning blurred landscape image from Unsplash
- **Color Scheme**: Elegant black and grey with cyan accents
- **Typography**: Modern Inter font family
- **Animations**: Smooth transitions and hover effects
- **Icons**: Font Awesome icons throughout

### Interactive Elements
- **Smart Textarea**: Auto-expanding prompt input with syntax highlighting
- **Model Selector**: Choose between different AI models
- **Format Toggle**: Switch between JSON and YAML output
- **Example Tags**: Click any example to auto-fill the prompt
- **Copy/Download**: One-click export functionality

## 🔧 Technical Details

### Frontend Stack
- **HTML5**: Semantic, accessible markup
- **CSS3**: Modern styling with flexbox and grid
- **JavaScript**: Vanilla JS for optimal performance
- **Font Awesome**: Beautiful icons
- **Google Fonts**: Inter typography

### Backend Stack
- **Flask**: Lightweight Python web framework
- **Flask-CORS**: Cross-origin resource sharing
- **Integration**: Direct connection to your prompt_parser.py

### File Structure
```
frontend/
├── index.html          # Main web interface
├── style.css          # Beautiful styling
└── script.js          # Frontend functionality

app.py                 # Flask backend server
start_server.py        # Quick start script
requirements.txt       # Python dependencies
```

## 🌐 API Endpoints

### POST /api/generate
Generate a game world from a prompt.

**Request Body:**
```json
{
    "prompt": "Your game world description",
    "model": "llama2",
    "format": "json"
}
```

**Response:**
```json
{
    "success": true,
    "data": { /* Generated world data */ },
    "filename": "generated_world.json",
    "level_name": "Generated World Name",
    "format": "json"
}
```

## 🎮 Generated Output

The web interface generates the same comprehensive JSON structure as the command-line version:

- **Metadata**: Level name, description, difficulty, playtime
- **Environment**: Terrain, lighting, weather, assets
- **Quests**: Objectives, rewards, requirements
- **NPCs**: Characters, dialogue, stats
- **Physics**: Player abilities, mechanics
- **Assets**: Required models, textures, sounds, effects

## 🔧 Configuration

### Environment Variables
```bash
export FLASK_ENV=development    # For development mode
export FLASK_PORT=5000         # Custom port (default: 5000)
export OLLAMA_HOST=localhost   # Ollama server host
export OLLAMA_PORT=11434       # Ollama server port
```

### Custom Background Image
To use your own background image, edit `frontend/style.css`:

```css
body::before {
    background-image: url('your-image-url-here');
}
```

## 🐛 Troubleshooting

### Common Issues

**"Connection refused" error**
- Make sure the Flask server is running
- Check that port 5000 is not blocked
- Try accessing http://127.0.0.1:5000 instead

**"Module not found" error**
- Run: `pip install Flask Flask-CORS requests PyYAML`
- Make sure you're in the correct directory

**Ollama not working**
- The web interface has a fallback demo mode
- Install and run Ollama for full functionality
- Check Ollama is running on localhost:11434

**Blank page or styling issues**
- Clear your browser cache
- Check browser console for JavaScript errors
- Ensure all files are in the correct directories

### Performance Tips

- **Use Chrome/Firefox**: Best compatibility and performance
- **Close other tabs**: For better memory usage
- **Stable internet**: For loading external fonts and images
- **Modern browser**: Supports all CSS features used

## 🚀 Deployment

### Local Network Access
To access from other devices on your network:

```bash
python app.py
# Server will be available at http://your-ip:5000
```

### Production Deployment
For production use, consider:
- Using a WSGI server like Gunicorn
- Setting up HTTPS with SSL certificates
- Using a reverse proxy like Nginx
- Implementing rate limiting and security measures

## 🎨 Customization

### Changing Colors
Edit `frontend/style.css` to customize the color scheme:

```css
:root {
    --primary-color: #00d4ff;    /* Cyan accent */
    --bg-dark: #0a0a0a;          /* Main background */
    --bg-card: rgba(20,20,20,0.8); /* Card backgrounds */
    --text-light: #e0e0e0;       /* Main text */
    --text-muted: #a0a0a0;       /* Secondary text */
}
```

### Adding Features
The modular structure makes it easy to add:
- User authentication
- Saved prompts/favorites
- Prompt history
- Collaborative editing
- Advanced settings panels

## 📱 Mobile Support

The interface is fully responsive and works great on:
- 📱 **Mobile phones**: Optimized touch interface
- 📱 **Tablets**: Perfect for creative work
- 💻 **Desktops**: Full feature set
- 🖥️ **Large screens**: Scales beautifully

## 🎉 Ready to Create!

Your beautiful web interface is ready! Start creating amazing game worlds with just a few clicks.

**Happy World Building! 🌟**
