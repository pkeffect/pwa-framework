# PWA Framework Generator - Developer Documentation

**Version:** 2.0.0  
**Purpose:** Universal LLM-readable documentation for understanding generated PWA frameworks  
**Audience:** AI assistants, code analysis tools, developers

---

## Overview

This document describes the **PWA Game Framework Generator** (`pwa_create.py`) and the structure of projects it generates. Use this as a complete reference for understanding, debugging, and extending any framework instance created by this tool.

---

## Generator Script: `pwa_create.py`

### What It Does

Generates a **complete, production-ready PWA framework** in ~150ms with:
- 24 files across 11 directories
- Zero external dependencies (vanilla JavaScript ES6 modules)
- Built-in accessibility, security, error handling, and performance optimizations
- 788-line comprehensive README.md

### Execution

```bash
python pwa_create.py my-project
```

**Input:** Project name (alphanumeric, hyphens, underscores)  
**Output:** Complete directory structure with all necessary files  
**Dependencies:** Python 3.10-3.12 stdlib only (argparse, json, re, sys, pathlib)

### Key Features of Generator

1. **Input Validation:** Regex `r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'`, length 1-50 chars
2. **Sanitization:** Lowercase conversion, space-to-hyphen, duplicate hyphen removal
3. **Error Recovery:** All file operations wrapped in try/except with detailed messages
4. **CLI:** Argparse-based with interactive mode if no args provided

---

## Generated Framework Architecture

### Philosophy

- **Zero Build Step:** Deploy instantly, no transpilation/bundling
- **Zero Dependencies:** No npm, no node_modules, no package.json
- **Progressive Enhancement:** Works offline-first as PWA
- **Separation of Concerns:** Clear module boundaries
- **Intentional Stubs:** InputManager, Scoreboard are 3-line templates for flexibility

---

## Complete File Structure

```
<project-name>/
│
├── index.html                 # 119 lines - Entry point with CSP, SRI, ARIA
├── manifest.json              # 8 lines - PWA config (name, icons, theme)
├── service-worker.js          # 60 lines - Cache versioning, fetch strategy
├── README.md                  # 788 lines - Complete user documentation
├── .gitignore                 # 6 lines - Standard exclusions
│
├── assets/                    # Media directory (empty scaffolding)
│   ├── icons/                # PWA icons (192x192, 512x512 required)
│   ├── audio/                # Sound effects, music files
│   ├── textures/             # Sprites, backgrounds, tilesets
│   ├── models/               # 3D models (optional)
│   └── shaders/              # WebGL shaders (optional)
│
├── css/
│   ├── main.css              # 89 lines - Reset, layout, canvas, layers
│   └── ui.css                # 147 lines - Modals, sidebar, glassmorphism
│
└── js/
    ├── main.js               # 36 lines - App bootstrap & initialization
    │
    ├── core/                 # Engine layer
    │   ├── Renderer.js       # 22 lines - High DPI canvas setup
    │   ├── GameLoop.js       # 38 lines - RAF with Visibility API
    │   ├── AssetLoader.js    # 74 lines - Chunked loading + retry logic
    │   ├── AudioManager.js   # 19 lines - Web Audio unlocking
    │   └── InputManager.js   # 3 lines - Intentional stub
    │
    ├── scenes/               # Game state machines
    │   ├── SceneManager.js   # 12 lines - Scene transitions
    │   ├── MenuScene.js      # 34 lines - Main menu logic
    │   └── GameScene.js      # 6 lines - Template (developer extends this)
    │
    ├── state/                # Data persistence
    │   ├── Store.js          # 7 lines - Global state object
    │   ├── SaveSystem.js     # 4 lines - localStorage wrapper
    │   ├── Settings.js       # 31 lines - User preferences
    │   └── Scoreboard.js     # 3 lines - Intentional stub
    │
    ├── ui/                   # DOM interaction
    │   ├── UIManager.js      # 109 lines - Modals, keyboard nav, focus trap
    │   └── ErrorDisplay.js   # 11 lines - Toast notifications
    │
    └── utils/                # Helpers
        ├── ErrorHandler.js   # 28 lines - Global error catching
        ├── DOMUtils.js       # 11 lines - Show/hide helpers
        └── MathUtils.js      # 4 lines - Clamp, lerp functions
```

**Total:** 24 files, 1,460 lines of generated code (~50KB uncompressed)

---

## Design Patterns & Architecture Decisions

### 1. ES6 Module System

**Why:** No build step, native browser support (2020+), clear dependencies

**Pattern:**
```javascript
// Export
export class Renderer { ... }

// Import
import { Renderer } from './core/Renderer.js';
```

**Rules:**
- All `.js` files must have `.js` extension in imports
- Relative paths required (`./` or `../`)
- Top-level `await` not used (broader compatibility)

---

### 2. Scene-Based Architecture

**Pattern:** State machine for game/menu screens

**Files:**
- `SceneManager.js` - Orchestrator (loads scenes, routes update/render)
- `MenuScene.js` - Main menu implementation
- `GameScene.js` - Placeholder for game logic

**Scene Lifecycle:**
```javascript
class Scene {
    enter() {
        // Called when scene becomes active
        // Initialize state, show DOM elements, bind events
    }
    
    update(deltaTime) {
        // Called every frame while active
        // Update game logic, physics, AI
    }
    
    render() {
        // Called every frame after update
        // Draw to canvas
    }
    
    exit() {
        // Called when switching away
        // Cleanup, hide DOM elements, unbind events
    }
}
```

**Why Scenes?**
- Clear state boundaries (menu vs gameplay)
- Prevents memory leaks (exit() cleanup)
- Easy to extend (add PauseScene, GameOverScene)

---

### 3. High DPI (Retina) Rendering

**File:** `Renderer.js`

**Problem:** Canvas looks blurry on 4K/Retina displays

**Solution:**
```javascript
const dpr = window.devicePixelRatio || 1;

// Internal resolution matches physical pixels
canvas.width = window.innerWidth * dpr;
canvas.height = window.innerHeight * dpr;

// CSS size matches screen space
canvas.style.width = window.innerWidth + 'px';
canvas.style.height = window.innerHeight + 'px';

// Scale drawing context
ctx.scale(dpr, dpr);
```

**Result:** Crisp 1:1 pixel mapping on all displays

---

### 4. Asset Loading with Retry Logic

**File:** `AssetLoader.js`

**Features:**
- **Chunked Loading:** 5 assets at a time (prevents mobile network saturation)
- **Exponential Backoff:** Retry delays: 0ms → 1000ms → 2000ms
- **Graceful Degradation:** Failed images get placeholder, logged to `failedAssets[]`
- **Progress Tracking:** Callback for loading screens

**Implementation:**
```javascript
async loadImage(src, key, retries = 2) {
    for (let attempt = 0; attempt <= retries; attempt++) {
        try {
            const img = new Image();
            await new Promise((resolve, reject) => {
                img.onload = resolve;
                img.onerror = reject;
                img.src = src;
            });
            return img;
        } catch (error) {
            if (attempt < retries) {
                const delay = 1000 * Math.pow(2, attempt); // 1s, 2s
                await new Promise(r => setTimeout(r, delay));
            }
        }
    }
    // Failed after all retries - return placeholder
}
```

**Why Retry?**
- Network hiccups (mobile switching towers, weak WiFi)
- CDN momentary failures
- Race conditions on slow connections

---

### 5. Battery & Performance Optimization

**File:** `GameLoop.js`

**Visibility API Integration:**
```javascript
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        this.isRunning = false; // Stop game loop
    } else {
        this.isRunning = true;
        this.lastTime = performance.now(); // Prevent huge deltaTime spike
    }
});
```

**Frame Skip Protection:**
```javascript
const dt = (now - this.lastTime) / 1000; // Convert to seconds

if (dt < 0.1) { // Normal frame (<100ms)
    this.callback(dt);
} else { // Slow frame (>100ms)
    console.warn('Frame took ' + dt + 's - skipping to prevent spiral of death');
    // Don't update - prevents compounding slowdown
}
```

**Why This Matters:**
- Mobile devices save battery when tab backgrounded
- Prevents "spiral of death" (slow frame → more work → slower frame)
- Users won't drain battery with tab open but not visible

---

### 6. Audio Context Unlocking

**File:** `AudioManager.js`

**Browser Restriction:** Modern browsers block audio until user interaction (anti-annoyance policy)

**Solution:**
```javascript
class AudioManager {
    static async resume() {
        if (this.audioContext.state === 'suspended') {
            await this.audioContext.resume();
        }
    }
}

// In MenuScene.js - start button triggers unlock
document.getElementById('btn-start').onclick = () => {
    AudioManager.resume().then(() => {
        SceneManager.loadScene('GAME');
    });
};
```

**Result:** Audio works on Chrome, Safari, Firefox mobile/desktop

---

### 7. Error Handling (3-Layer Protection)

**File:** `ErrorHandler.js`

**Layer 1: Synchronous Errors**
```javascript
window.addEventListener('error', (e) => {
    console.error('💥 Error:', e.error);
    ErrorDisplay.show(e.message);
});
```

**Layer 2: Unhandled Promise Rejections**
```javascript
window.addEventListener('unhandledrejection', (e) => {
    console.error('💥 Promise Rejection:', e.reason);
    ErrorDisplay.show(`Async Error: ${e.reason.message || e.reason}`);
});
```

**Layer 3: Resource Loading Failures**
```javascript
window.addEventListener('error', (e) => {
    if (e.target.tagName === 'IMG') {
        e.target.style.display = 'none'; // Hide broken image
    } else if (e.target.tagName === 'SCRIPT') {
        ErrorDisplay.show('Critical script failed to load');
    }
}, true); // Capture phase
```

**Philosophy:** Never crash silently, always inform user

---

### 8. Service Worker Cache Strategy

**File:** `service-worker.js`

**Strategy:** Cache-first with version-based invalidation

```javascript
const CACHE_VERSION = 1; // Increment to force update
const CACHE_NAME = 'my-project-v1';

// Install: Cache core files
self.addEventListener('install', (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll([
                '/',
                '/index.html',
                '/css/main.css',
                // ... etc
            ]);
        })
    );
});

// Activate: Delete old caches
self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then(names => {
            return Promise.all(
                names.filter(n => n.startsWith('my-project-v') && n !== CACHE_NAME)
                     .map(old => caches.delete(old))
            );
        })
    );
});

// Fetch: Serve from cache, fallback to network
self.addEventListener('fetch', (e) => {
    e.respondWith(
        caches.match(e.request).then(cached => {
            return cached || fetch(e.request);
        })
    );
});
```

**Update Process:**
1. Edit code
2. Increment `CACHE_VERSION` to `2`
3. Deploy
4. Service worker auto-updates, old cache deleted

---

### 9. Accessibility (WCAG 2.1 AA)

**File:** `UIManager.js`

**Keyboard Navigation:**
- `Tab` / `Shift+Tab` - Navigate interactive elements
- `ESC` - Close modals/sidebars
- `Enter` - Activate buttons

**Focus Trapping in Modals:**
```javascript
static trapFocus(modal) {
    const focusable = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    
    modal.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        }
    });
}
```

**ARIA Attributes:**
```html
<button aria-label="Start game">Start</button>
<div role="dialog" aria-modal="true" aria-labelledby="modal-title">
```

**Why WCAG Compliance?**
- Legal requirement for many jurisdictions
- Better UX for everyone (keyboard users, screen readers)
- SEO benefits (semantic HTML)

---

### 10. Security Features

#### Content Security Policy (CSP)

**File:** `index.html`

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self'; 
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; 
               font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com;">
```

**Protection:**
- ✅ Blocks inline `<script>` tags (XSS prevention)
- ✅ Only allows scripts from same origin
- ✅ Whitelists CDNs explicitly

#### Subresource Integrity (SRI)

**File:** `index.html`

```html
<link rel="stylesheet" 
      href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
      integrity="sha512-9usAa10IRO0HhonpyAIVpjrylPvoDwiPUiKdWk5t3PyolY1cOd4DSE0Ga+ri4AuTroPR5aQvXU9xC6qOPnzFeg=="
      crossorigin="anonymous">
```

**Protection:**
- ✅ Verifies CDN file hasn't been tampered with
- ✅ Cryptographic hash validation (SHA-512)
- ✅ Browser refuses to load mismatched files

---

## Intentional Design Choices

### Why No TypeScript?

**Reason:** Zero-dependency philosophy

- TypeScript requires compilation step (tsc or bundler)
- Adds node_modules, package.json, build scripts
- JSDoc comments provide type hints for IDEs without compilation

**Alternative:** Use JSDoc for type safety without compilation:
```javascript
/**
 * @param {number} x - Position
 * @param {number} y - Position
 * @returns {boolean} True if collision
 */
function checkCollision(x, y) { ... }
```

---

### Why No Bundler (Webpack/Vite)?

**Reason:** Instant deployment, zero build time

- ES6 modules natively supported in all modern browsers (2020+)
- HTTP/2 makes multiple small files efficient
- No watching, no rebuilding, no build failures

**Trade-off:** Slightly more HTTP requests (mitigated by HTTP/2 multiplexing)

---

### Why Vanilla CSS?

**Reason:** No preprocessor dependencies

- No SASS/LESS compilation
- CSS variables provide dynamic theming
- Modern CSS supports nesting proposals (2024+)

**Glassmorphism Implementation:**
```css
.modal {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

---

### Why Stubs for InputManager & Scoreboard?

**Reason:** Project diversity - different needs

**Examples:**
- **Touchscreen Game:** Needs touch/gesture input (swipe, pinch)
- **Keyboard Game:** Needs key state tracking
- **Mouse Game:** Needs click/drag handlers
- **Gamepad Game:** Needs Gamepad API integration

**Scoreboard:**
- **Local Only:** Simple array in SaveSystem
- **Online Leaderboard:** Fetch API to backend
- **No Scores:** Remove entirely

**Philosophy:** Template, not constraint

---

## Common LLM Assistance Scenarios

### Scenario 1: "Add player movement to my game"

**Files to Modify:**
- `js/scenes/GameScene.js`

**Pattern:**
```javascript
export class GameScene {
    enter() {
        this.player = { x: 400, y: 300, speed: 200 };
        this.keys = {};
        
        this.keyDownHandler = (e) => this.keys[e.key] = true;
        this.keyUpHandler = (e) => this.keys[e.key] = false;
        
        window.addEventListener('keydown', this.keyDownHandler);
        window.addEventListener('keyup', this.keyUpHandler);
    }
    
    update(dt) {
        if (this.keys['ArrowLeft']) this.player.x -= this.player.speed * dt;
        if (this.keys['ArrowRight']) this.player.x += this.player.speed * dt;
        if (this.keys['ArrowUp']) this.player.y -= this.player.speed * dt;
        if (this.keys['ArrowDown']) this.player.y += this.player.speed * dt;
    }
    
    render() {
        const ctx = Renderer.canvas.getContext('2d');
        ctx.fillStyle = '#00ff00';
        ctx.fillRect(this.player.x - 10, this.player.y - 10, 20, 20);
    }
    
    exit() {
        window.removeEventListener('keydown', this.keyDownHandler);
        window.removeEventListener('keyup', this.keyUpHandler);
    }
}
```

**Key Points:**
- Use `deltaTime` for frame-independent movement
- Bind/unbind events in `enter()`/`exit()` to prevent leaks
- `speed` in pixels/second

---

### Scenario 2: "Load and draw a sprite"

**Files to Modify:**
1. `js/main.js` - Add to `MANIFEST`
2. `js/scenes/GameScene.js` - Use asset

**Step 1: Define Asset**
```javascript
// js/main.js
const MANIFEST = [
    { type: 'image', src: 'assets/textures/player.png', key: 'player' }
];
```

**Step 2: Use Asset**
```javascript
// js/scenes/GameScene.js
import { AssetLoader } from '../core/AssetLoader.js';

export class GameScene {
    enter() {
        this.playerImg = AssetLoader.get('player');
        this.playerX = 100;
        this.playerY = 100;
    }
    
    render() {
        const ctx = Renderer.canvas.getContext('2d');
        if (this.playerImg) {
            ctx.drawImage(this.playerImg, this.playerX, this.playerY);
        }
    }
}
```

**Debugging:**
- Check `AssetLoader.failedAssets` in console
- Verify file path matches (case-sensitive on Linux/Mac)
- Check browser Network tab for 404s

---

### Scenario 3: "Add background music"

**Files to Modify:**
1. `js/main.js` - Add to `MANIFEST`
2. `js/scenes/MenuScene.js` - Start on user click
3. `js/scenes/GameScene.js` - Play/loop

**Step 1: Load Audio**
```javascript
// js/main.js
const MANIFEST = [
    { type: 'audio', src: 'assets/audio/bgm.mp3', key: 'bgm' }
];
```

**Step 2: Play on User Interaction**
```javascript
// js/scenes/MenuScene.js
import { AssetLoader } from '../core/AssetLoader.js';
import { AudioManager } from '../core/AudioManager.js';

const startBtn = document.getElementById('btn-start');
startBtn.onclick = async () => {
    await AudioManager.resume(); // Unlock audio context
    
    const bgm = AssetLoader.get('bgm');
    bgm.loop = true;
    bgm.volume = 0.5;
    bgm.play();
    
    SceneManager.loadScene('GAME');
};
```

**Important:** Must call `AudioManager.resume()` on user gesture (browser policy)

---

### Scenario 4: "Save high score"

**Files to Modify:**
- `js/state/Scoreboard.js` - Implement logic

**Implementation:**
```javascript
// js/state/Scoreboard.js
import { SaveSystem } from './SaveSystem.js';

export class Scoreboard {
    static saveScore(score) {
        const saved = SaveSystem.load();
        const highScores = saved.highScores || [];
        
        highScores.push(score);
        highScores.sort((a, b) => b - a); // Descending
        highScores.splice(10); // Keep top 10
        
        SaveSystem.save({ ...saved, highScores });
    }
    
    static getTopScores() {
        const saved = SaveSystem.load();
        return saved.highScores || [];
    }
}
```

**Usage in GameScene:**
```javascript
gameOver() {
    Scoreboard.saveScore(this.score);
    const topScores = Scoreboard.getTopScores();
    console.log('Top 10:', topScores);
}
```

---

### Scenario 5: "Deploy to Netlify"

**Files to Create:**
- `netlify.toml` (in project root)

**Content:**
```toml
[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Steps:**
1. Create `netlify.toml`
2. Drag project folder to [app.netlify.com](https://app.netlify.com)
3. Done - auto-deployed with HTTPS

**Why redirect?** Ensures SPA routing works (all paths serve index.html)

---

## Troubleshooting Guide for LLMs

### Error: "Failed to load module script"

**Cause:** Missing `.js` extension in import

```javascript
// ❌ Wrong
import { Renderer } from './core/Renderer';

// ✅ Correct
import { Renderer } from './core/Renderer.js';
```

---

### Error: "Cannot read property of undefined"

**Common Cause:** Asset not loaded before use

**Fix:** Always check asset exists:
```javascript
const img = AssetLoader.get('player');
if (img) {
    ctx.drawImage(img, x, y);
} else {
    console.warn('Player image not loaded yet');
}
```

---

### Error: "The AudioContext was not allowed to start"

**Cause:** Audio context not unlocked by user gesture

**Fix:** Call `AudioManager.resume()` on button click:
```javascript
startBtn.onclick = async () => {
    await AudioManager.resume();
    // Now audio will work
};
```

---

### Service Worker Not Updating

**Cause:** Browser cached old service worker

**Fix 1 (Developer):** Hard refresh `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)

**Fix 2 (Production):** Increment cache version:
```javascript
// service-worker.js
const CACHE_VERSION = 2; // Was 1, now 2
```

---

### Canvas Blurry on 4K Display

**Cause:** Not using High DPI scaling

**Fix:** Renderer already handles this - ensure you're not overriding canvas size:
```javascript
// ❌ Don't do this
canvas.width = 800;
canvas.height = 600;

// ✅ Let Renderer handle it
Renderer.init('game-canvas'); // Auto-sizes with DPI
```

---

## Extension Points

### Adding New Scenes

**Example:** Pause screen

**File:** `js/scenes/PauseScene.js`

```javascript
import { DOMUtils } from '../utils/DOMUtils.js';

export class PauseScene {
    enter() {
        DOMUtils.show('pause-menu');
        document.getElementById('btn-resume').onclick = () => {
            SceneManager.loadScene('GAME');
        };
    }
    
    update(dt) {
        // Paused - no updates
    }
    
    render() {
        // Optionally darken background
    }
    
    exit() {
        DOMUtils.hide('pause-menu');
    }
}
```

**Register in SceneManager.js:**
```javascript
import { PauseScene } from './PauseScene.js';

this.scenes = {
    MENU: new MenuScene(),
    GAME: new GameScene(),
    PAUSE: new PauseScene() // Add this
};
```

---

### Adding Particle Effects

**File:** `js/utils/ParticleSystem.js` (create new)

```javascript
export class ParticleSystem {
    constructor() {
        this.particles = [];
    }
    
    emit(x, y, count) {
        for (let i = 0; i < count; i++) {
            this.particles.push({
                x, y,
                vx: (Math.random() - 0.5) * 200,
                vy: (Math.random() - 0.5) * 200,
                life: 1.0,
                decay: Math.random() * 0.5 + 0.5
            });
        }
    }
    
    update(dt) {
        this.particles = this.particles.filter(p => {
            p.x += p.vx * dt;
            p.y += p.vy * dt;
            p.life -= p.decay * dt;
            return p.life > 0;
        });
    }
    
    render(ctx) {
        this.particles.forEach(p => {
            ctx.globalAlpha = p.life;
            ctx.fillStyle = '#ffff00';
            ctx.fillRect(p.x - 2, p.y - 2, 4, 4);
        });
        ctx.globalAlpha = 1.0;
    }
}
```

**Usage in GameScene:**
```javascript
import { ParticleSystem } from '../utils/ParticleSystem.js';

export class GameScene {
    enter() {
        this.particles = new ParticleSystem();
    }
    
    onExplosion(x, y) {
        this.particles.emit(x, y, 50); // 50 particles
    }
    
    update(dt) {
        this.particles.update(dt);
    }
    
    render() {
        this.particles.render(ctx);
    }
}
```

---

## Performance Best Practices

### 1. Object Pooling

**Problem:** Creating/destroying objects causes garbage collection pauses

**Solution:** Reuse objects
```javascript
class BulletPool {
    constructor(size) {
        this.pool = Array(size).fill(null).map(() => ({
            x: 0, y: 0, vx: 0, vy: 0, active: false
        }));
    }
    
    spawn(x, y, vx, vy) {
        const bullet = this.pool.find(b => !b.active);
        if (bullet) {
            bullet.x = x;
            bullet.y = y;
            bullet.vx = vx;
            bullet.vy = vy;
            bullet.active = true;
        }
        return bullet;
    }
    
    update(dt) {
        this.pool.forEach(b => {
            if (b.active) {
                b.x += b.vx * dt;
                b.y += b.vy * dt;
                if (b.x < 0 || b.x > 800) b.active = false; // Recycle
            }
        });
    }
}
```

---

### 2. Spatial Partitioning

**Problem:** Checking every object against every other (O(n²))

**Solution:** Quadtree or grid-based culling
```javascript
class Grid {
    constructor(cellSize) {
        this.cellSize = cellSize;
        this.cells = new Map();
    }
    
    getCell(x, y) {
        const cx = Math.floor(x / this.cellSize);
        const cy = Math.floor(y / this.cellSize);
        return `${cx},${cy}`;
    }
    
    insert(entity) {
        const key = this.getCell(entity.x, entity.y);
        if (!this.cells.has(key)) this.cells.set(key, []);
        this.cells.get(key).push(entity);
    }
    
    getNearby(x, y) {
        const key = this.getCell(x, y);
        return this.cells.get(key) || [];
    }
}
```

---

### 3. Minimize Canvas State Changes

**Problem:** State changes (fillStyle, strokeStyle) are expensive

**Solution:** Batch by color/style
```javascript
// ❌ Slow - state change per enemy
enemies.forEach(e => {
    ctx.fillStyle = e.color;
    ctx.fillRect(e.x, e.y, 10, 10);
});

// ✅ Fast - batch by color
const byColor = enemies.reduce((acc, e) => {
    (acc[e.color] = acc[e.color] || []).push(e);
    return acc;
}, {});

Object.entries(byColor).forEach(([color, group]) => {
    ctx.fillStyle = color;
    group.forEach(e => ctx.fillRect(e.x, e.y, 10, 10));
});
```

---

## Summary for LLMs

When assisting users with projects generated by `pwa_create.py`:

1. **Identify Framework:** Look for `js/core/Renderer.js`, `SceneManager.js`, `main.js` with AssetLoader
2. **Primary Edit Location:** 95% of game code goes in `js/scenes/GameScene.js`
3. **Asset Pipeline:** Add to `MANIFEST` in `main.js`, retrieve with `AssetLoader.get(key)`
4. **Audio:** Must unlock via `AudioManager.resume()` on user click
5. **Debugging:** Check `AssetLoader.failedAssets`, browser console, Network tab
6. **Performance:** Use `deltaTime`, object pooling, batched rendering
7. **Deployment:** Zero build step - just upload files with HTTPS server

**Key Principle:** Everything is intentional. If it seems missing (InputManager, Scoreboard), it's a template for user customization.

---

**Document Version:** 1.0  
**Last Updated:** 2026-01-11  
**Generator Version:** 2.0.0
