# Contributing to PWA Game Framework Generator

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Contribution Types](#contribution-types)
- [Style Guidelines](#style-guidelines)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Versioning Strategy](#versioning-strategy)

---

## Code of Conduct

This project follows a professional, respectful development environment:

- ✅ **Be respectful** - Constructive feedback only
- ✅ **Be inclusive** - Welcome contributors of all skill levels
- ✅ **Be helpful** - Share knowledge, explain decisions
- ❌ **No harassment** - Zero tolerance policy
- ❌ **No spam** - Stay on topic

---

## Getting Started

### Prerequisites

- Python 3.10 - 3.12
- Git
- Code editor (VS Code recommended)
- Basic understanding of:
  - Python (stdlib, pathlib, type hints)
  - JavaScript ES6 modules
  - HTML/CSS
  - PWA concepts (optional but helpful)

### Fork & Clone

```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/pwa-framework.git
cd pwa-framework

# Add upstream remote
git remote add upstream https://github.com/pkeffect/pwa-framework.git
```

### Test Your Setup

```bash
# Generate a test project
python pwa_create.py test-contribution

# Verify output
cd test-contribution
python -m http.server 8000
# Open http://localhost:8000
```

---

## Development Workflow

### 1. Create a Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
# or
git checkout -b template/new-component
```

**Branch naming conventions:**
- `feature/*` - New generator features
- `fix/*` - Bug fixes
- `template/*` - New or modified generated files
- `docs/*` - Documentation updates
- `test/*` - CI/testing improvements

### 2. Make Changes

**Editing templates:**
```python
# In pwa_create.py, locate Templates class

@staticmethod
def get_new_template() -> str:
    """Generate NewTemplate.js content.
    
    Returns:
        str: JavaScript content for NewTemplate.js
    """
    return """export class NewTemplate {
    constructor() {
        // Implementation
    }
}
"""
```

**Adding to structure:**
```python
# In create_framework() function
structure = {
    # ... existing files ...
    base / "js" / "new" / "NewTemplate.js": Templates.get_new_template(),
}
```

### 3. Update Documentation

**Required for all changes:**

1. **Version bump** (if adding features):
   ```python
   # Line 24 in pwa_create.py
   SCRIPT_VERSION = "2.1.0"  # Bump appropriately
   ```

2. **Update badges** (if version changed):
   ```markdown
   # README.md line 8
   ![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)
   
   # DEVELOPER.md line 3
   **Version:** 2.1.0
   
   # AUDIT.md line 7
   **Version:** 2.1.0
   ```

3. **Update CHANGELOG.md**:
   ```markdown
   ## [Unreleased]
   
   ### Added
   - New template: NewTemplate.js for X functionality
   ```

4. **Update file counts** (if added/removed files):
   - README.md: "24 files" → "25 files"
   - DEVELOPER.md: File structure table
   - .github/workflows/validate.yml: File count checks

### 4. Test Locally

```bash
# Run generator
python pwa_create.py local-test

# Verify all files created
cd local-test
find . -type f | wc -l  # Should match expected count

# Check for syntax errors
grep -r "eval(" js/ && echo "FAIL: Found eval()" || echo "PASS"

# Test in browser
python -m http.server 8000
```

### 5. Commit

```bash
git add pwa_create.py
git commit -m "feat: Add NewTemplate.js for X functionality

- Adds Templates.get_new_template() method
- Updates structure dict in create_framework()
- Updates documentation (README, DEVELOPER, CHANGELOG)
- Increments version to 2.1.0"
```

**Commit message format:**
```
<type>: <subject>

<body>

<footer>
```

**Types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Formatting, whitespace
- `refactor:` - Code restructuring
- `test:` - Adding/updating tests
- `chore:` - Maintenance (CI, deps)

### 6. Push & PR

```bash
git push origin feature/your-feature-name
```

Then open a Pull Request on GitHub using the [PR template](.github/PULL_REQUEST_TEMPLATE.md).

---

## Contribution Types

### 🐛 Bug Fixes

**Checklist:**
- [ ] Identify root cause
- [ ] Add test case that fails before fix
- [ ] Implement fix
- [ ] Verify test passes
- [ ] Update CHANGELOG.md
- [ ] Version bump (patch: x.y.Z)

### ✨ New Features

**Checklist:**
- [ ] Open issue first (for discussion)
- [ ] Implement feature
- [ ] Add documentation
- [ ] Add CI test coverage
- [ ] Update CHANGELOG.md
- [ ] Version bump (minor: x.Y.0)

### 📝 New Templates

**Checklist:**
- [ ] Create `Templates.get_js_newfile()` method
- [ ] Add to `structure` dict
- [ ] Keep LOC count reasonable (intentional stub: 3-10, basic: 50-100, complete: 100-150)
- [ ] Document in generated README
- [ ] Add to file verification in CI
- [ ] Update DEVELOPER.md file structure table
- [ ] Version bump (minor: x.Y.0)

**Template design guidelines:**
- Prefer intentional stubs for highly customizable components
- Include type hints in JSDoc comments
- Use ES6 modules with explicit `.js` extensions
- No external dependencies
- Follow existing naming conventions

### 📚 Documentation

**Checklist:**
- [ ] Fix typos, improve clarity
- [ ] Keep line counts accurate
- [ ] Update examples if code changed
- [ ] Check markdown rendering (preview in GitHub)
- [ ] No version bump needed (unless substantial rewrite)

---

## Style Guidelines

### Python (pwa_create.py)

```python
# ✅ Good
def create_something(name: str) -> bool:
    """Create something with the given name.
    
    Args:
        name: The name to use
        
    Returns:
        bool: True if successful
        
    Raises:
        ValueError: If name is invalid
    """
    if not name:
        raise ValueError("Name required")
    
    try:
        result = do_work(name)
        return result
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

# ❌ Bad
def create_something(name):  # No type hints
    # No docstring
    if not name: raise ValueError("Name required")  # Multi-statement line
    try:
        result = do_work(name)
        return result
    except:  # Bare except
        return False
```

**Rules:**
- Type hints on all functions (`-> str | bool | None`)
- Google-style docstrings with Args/Returns/Raises
- Use `pathlib.Path` (never string concatenation for paths)
- PEP 8 compliance (snake_case, 4-space indent)
- Specific exception types (no bare `except:`)
- Max line length: 120 (templates can exceed)

### JavaScript (Generated Templates)

```javascript
// ✅ Good
export class GoodExample {
    constructor() {
        this.state = {};
    }
    
    doSomething(param) {
        // Clear logic
        return result;
    }
}

// ❌ Bad
class BadExample {  // Not exported
    constructor() {
        eval("code");  // NEVER
        this.elem.innerHTML = userInput;  // XSS risk
    }
}
```

**Rules:**
- ES6 modules with `export`
- Explicit `.js` in import paths
- No `eval()`, `Function()`, `exec()`
- No `innerHTML` with user data
- Clear variable names
- Comments for complex logic

### CSS (Generated Styles)

```css
/* ✅ Good */
:root {
    --primary-color: #e96714;
}

.component {
    color: var(--primary-color);
    box-sizing: border-box;
}

/* ❌ Bad */
.component {
    color: #e96714 !important;  /* Avoid !important */
    box-sizing: border-box;
    -webkit-box-sizing: border-box;  /* Unnecessary prefixes */
}
```

---

## Testing Requirements

### Manual Testing

Before submitting PR:

1. **Generate test project:**
   ```bash
   python pwa_create.py pr-test-$(date +%s)
   ```

2. **Verify file count:**
   ```bash
   cd pr-test-*
   find . -type f | wc -l
   # Expected: 24 (or updated count)
   ```

3. **Browser test:**
   ```bash
   python -m http.server 8000
   # Open http://localhost:8000
   # Check console for errors
   # Test service worker registration
   ```

4. **Security checks:**
   ```bash
   grep -r "eval(" js/ && echo "FAIL" || echo "PASS"
   grep -q "Content-Security-Policy" index.html && echo "PASS" || echo "FAIL"
   ```

### CI Testing

Our GitHub Actions will automatically test:
- Python 3.10, 3.11, 3.12
- Ubuntu, Windows, macOS
- All 24+ files created
- No `eval()` usage
- CSP headers present
- ES6 module syntax correct
- Input validation
- Documentation version consistency

**View CI results** on your PR before requesting review.

---

## Pull Request Process

### Before Submitting

- [ ] Branch is up to date with `main`
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] CHANGELOG.md entry added
- [ ] Version bumped (if applicable)
- [ ] No merge conflicts

### PR Template

Use [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) - it will auto-populate.

### Review Process

1. **Automated checks** run (CI/CD)
2. **Maintainer review** (1-3 business days)
3. **Feedback/changes** requested (if needed)
4. **Approval & merge** (squash merge to `main`)

### After Merge

- Your branch will be deleted
- Changes appear in next release
- You'll be credited in release notes

---

## Versioning Strategy

We follow [Semantic Versioning](https://semver.org/):

**Format:** `MAJOR.MINOR.PATCH`

### When to Bump

**MAJOR (x.0.0)** - Breaking changes
- Removes generated files
- Changes scene lifecycle API
- Requires migration guide

**MINOR (x.Y.0)** - New features (backward compatible)
- Adds new generated files
- Enhances existing templates
- New CLI options
- Substantial documentation additions

**PATCH (x.y.Z)** - Bug fixes (backward compatible)
- Fixes generation errors
- Typos in generated code
- Documentation corrections
- Security patches

### Version Update Checklist

```python
# 1. Update constant
SCRIPT_VERSION = "2.1.0"

# 2. Update badges
# README.md line 8
![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)

# 3. Update docs
# DEVELOPER.md line 3, AUDIT.md line 7
**Version:** 2.1.0

# 4. Add CHANGELOG entry
## [2.1.0] - 2026-01-15
### Added
- Feature description
```

---

## Need Help?

- 💬 **Questions:** [Open a discussion](https://github.com/pkeffect/pwa-framework/discussions)
- 🐛 **Bugs:** [File an issue](https://github.com/pkeffect/pwa-framework/issues/new?template=bug_report.md)
- 💡 **Ideas:** [Feature request](https://github.com/pkeffect/pwa-framework/issues/new?template=feature_request.md)
- 📧 **Direct contact:** pkeffect@gmail.com

---

## Recognition

Contributors are credited in:
- Release notes (GitHub releases)
- CHANGELOG.md (linked GitHub profiles)
- AUDIT.md (Security Hall of Fame for vulnerability reports)

---

**Thank you for contributing!** 🎉
