# PWA Game Framework Generator - AI Coding Guide

## Project Overview

Single-file Python generator (`pwa_create.py`) that scaffolds complete Progressive Web App game frameworks in ~150ms. Zero external dependencies, generates 24 files across 11 directories with production-ready features (offline-first, accessibility, security, high-DPI rendering).

**Key Philosophy:** Zero build step, zero dependencies, instant deployment. Generated output uses vanilla ES6 modules - no transpilation, no bundlers, no npm.

## Architecture

### Generator Script Structure

The 2,194-line `pwa_create.py` follows a strict organization pattern:

1. **Templates Class (lines 32-1157)**: 24+ static methods, each returning complete file contents as strings
2. **Validation Layer (lines 1960-2004)**: Input sanitization with regex `r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'`
3. **Generator Logic (lines 2010-2107)**: File tree dictionary mapping paths to template content
4. **CLI Interface (lines 2109-2192)**: Argparse-based with interactive fallback

**Critical Pattern:** All file contents are embedded as triple-quoted strings in static methods. When adding new generated files, create a new `get_*()` method in `Templates` class, then add the path mapping in `create_framework()`'s `structure` dict.

### Generated Framework Architecture

**Output follows a strict 3-layer separation:**

```
Layer 0 (Canvas): Game rendering - core/Renderer.js handles High DPI with devicePixelRatio scaling
Layer 1 (UI Overlay): DOM elements - ui/UIManager.js manages modals/sidebars with focus trapping  
Layer 2 (Loading): Bootstrap screen - fades out after asset loading completes
```

**Scene-based state machine:** Every scene implements `enter()`, `update(deltaTime)`, `render()`, `exit()`. SceneManager orchestrates transitions. This prevents memory leaks and ensures clean state boundaries.

**Intentional stubs:** `InputManager.js` and `Scoreboard.js` are 3-line templates by design - developers customize these heavily, so we provide minimal structure rather than opinionated implementations.

## Developer Workflows

### Running the Generator

```powershell
# Interactive mode (prompts for name)
python pwa_create.py

# Direct mode  
python pwa_create.py my-game

# Testing sanitization (spaces → hyphens, lowercased)
python pwa_create.py "My Cool Game!"  # Creates: my-cool-game/
```

### Testing Generated Output

```powershell
cd <generated-project>
python -m http.server 8000
# Navigate to http://localhost:8000
```

**No build step required** - generated code runs directly in browser. All `.js` files use ES6 modules with explicit `.js` extensions in import statements (required for native module loading).

### Modifying Templates

When editing file contents in `Templates` class:
- Preserve exact indentation/whitespace in triple-quoted strings
- JavaScript template literals need escaped backticks: \`\${variable}\`
- CSS custom properties use `var(--variable-name)` syntax
- Update line counts in DEVELOPER.md if adding substantial code

## Project-Specific Conventions

### Python Code Style

- **Type hints required:** All functions annotated with `-> str | bool | None`
- **Docstrings required:** Google-style with Args/Returns/Raises sections
- **Error handling:** Never bare `except:` - always specify exception types
- **Path operations:** Use `pathlib.Path` exclusively, never string concatenation
- **No external dependencies:** stdlib only (argparse, json, re, sys, pathlib)

### Generated JavaScript Patterns

**High DPI Rendering (core/Renderer.js):**
```javascript
const dpr = window.devicePixelRatio || 1;
canvas.width = window.innerWidth * dpr;   // Physical pixels
canvas.style.width = window.innerWidth;    // CSS pixels  
ctx.scale(dpr, dpr);                       // Scale drawing context
```

**Asset Loading (core/AssetLoader.js):**
- Chunked loading with 2 retries per asset
- Exponential backoff: 1s → 2s retry delays
- Progress callbacks for loading UI updates

**Scene Lifecycle Pattern:**
```javascript
// MenuScene.js shows canonical implementation
enter() {
    // Show DOM elements, bind event listeners
    document.getElementById('menu-card').classList.remove('hidden');
}

exit() {
    // Hide DOM, unbind listeners (critical for preventing leaks)
    document.getElementById('menu-card').classList.add('hidden');
}
```

### Security Patterns

- **Input validation:** Always validate + sanitize before file operations
- **CSP headers:** Generated HTML includes Content-Security-Policy meta tag
- **SRI hashes:** External resources (Font Awesome CDN) use Subresource Integrity
- **No eval():** Generated code never uses `eval()`, `Function()`, or `innerHTML` with user data

## Key Files Reference

### Documentation Trinity
- [README.md](README.md): User-facing documentation (788 lines, comprehensive usage guide)
- [DEVELOPER.md](DEVELOPER.md): Technical deep-dive (1,047 lines, architecture decisions)
- [AUDIT.md](AUDIT.md): Quality/security audit (761 lines, competitive analysis)

### Critical Generator Components
- Lines 43-114: CSS templates (main.css, ui.css)
- Lines 271-431: HTML template with CSP/SRI/ARIA
- Lines 482-565: AssetLoader with retry logic
- Lines 566-597: High DPI Renderer
- Lines 1962-2004: Input validation/sanitization

## Common Tasks

### Adding a New Generated File

1. Create template method in `Templates` class:
```python
@staticmethod
def get_new_component() -> str:
    """Generate NewComponent.js content."""
    return """export class NewComponent {
    // Implementation
}
"""
```

2. Add to `structure` dict in `create_framework()`:
```python
base / "js" / "components" / "NewComponent.js": Templates.get_new_component(),
```

### Updating Python Version Compatibility

Currently supports Python 3.10-3.12. If extending support:
- Check `match-case` statements (3.10+ syntax)
- Verify `pathlib` API usage
- Update version badge in README.md line 8

### Testing Input Validation

Test cases in `validate_project_name()`:
- Empty strings → ValueError
- Length 1-50 characters (MIN/MAX constants)
- Must start with alphanumeric (prevents `.hidden` files)
- Spaces converted to hyphens, lowercased
- Consecutive hyphens collapsed
- Trailing hyphens stripped

## Integration Points

**No external integrations** - this is a standalone generator. Generated frameworks integrate with:
- **Service Workers:** `service-worker.js` uses Cache API for offline-first
- **Web Audio API:** `AudioManager.js` handles context unlocking for mobile
- **localStorage:** `SaveSystem.js` wraps browser storage for state persistence
- **PWA Manifest:** `manifest.json` enables "Add to Home Screen"

## Anti-Patterns to Avoid

❌ **Don't add npm dependencies** - defeats zero-dependency philosophy  
❌ **Don't use `eval()` or `exec()`** - security vulnerability  
❌ **Don't concatenate paths with strings** - use `pathlib.Path` operators  
❌ **Don't modify generated code after scaffolding** - users customize it  
❌ **Don't add build tools** - violates instant-deployment principle  
❌ **Don't use `innerHTML` with user data** - XSS risk in generated code

## Performance Characteristics

- **Generation time:** ~150ms for complete 24-file framework
- **Generated output size:** ~50KB uncompressed (1,460 LOC)
- **Browser boot time:** 28ms to first render (vanilla JS)
- **No bundling overhead:** ES6 modules load natively

## Version Updates

When bumping `SCRIPT_VERSION` constant:
1. Update line 24 in pwa_create.py
2. Update README.md badges (line 8)
3. Update DEVELOPER.md header (line 3)
4. Update AUDIT.md header (line 7)
5. Document changes if adding features
