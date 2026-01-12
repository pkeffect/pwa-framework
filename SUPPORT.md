# Support

Looking for help with the PWA Game Framework Generator? Here's how to get support.

---

## 📚 Documentation

Start with our comprehensive documentation:

- **[README.md](README.md)** - User guide, quick start, usage examples (788 lines)
- **[DEVELOPER.md](DEVELOPER.md)** - Architecture deep-dive, design patterns (1,047 lines)
- **[AUDIT.md](AUDIT.md)** - Quality/security audit, competitive analysis (761 lines)
- **[.github/copilot-instructions.md](.github/copilot-instructions.md)** - AI coding assistant guide

### Quick Links

- [Installation](README.md#-installation)
- [Quick Start](README.md#-quick-start)
- [Generated Project Structure](README.md#-generated-project-structure)
- [Input Validation Rules](README.md#project-name-rules)
- [Architecture Overview](DEVELOPER.md#overview)
- [Template System](DEVELOPER.md#generator-script-pwacreateyyy)
- [Security Features](SECURITY.md)

---

## 💬 Community Support

### GitHub Discussions (Recommended)

**Best for:** General questions, sharing projects, feature ideas

[Open a discussion](https://github.com/pkeffect/pwa-framework/discussions)

**Categories:**
- 💡 **Ideas** - Feature requests, suggestions
- 🙋 **Q&A** - "How do I...?" questions
- 🎮 **Show and Tell** - Share what you've built
- 📣 **Announcements** - Project updates

**Response time:** Usually within 24-48 hours

### Stack Overflow

Tag your question with:
- `pwa`
- `game-development`
- `python-3.x`
- `progressive-web-app`

[Ask on Stack Overflow](https://stackoverflow.com/questions/ask)

---

## 🐛 Bug Reports

If something isn't working:

1. **Search existing issues:** Someone may have already reported it
   - [Open issues](https://github.com/pkeffect/pwa-framework/issues)
   - [Closed issues](https://github.com/pkeffect/pwa-framework/issues?q=is%3Aissue+is%3Aclosed)

2. **File a new bug report:** Use our template
   - [Report a bug](https://github.com/pkeffect/pwa-framework/issues/new?template=bug_report.md)

**Include:**
- Python version (`python --version`)
- Generator version (line 24 of `pwa_create.py`)
- Operating system
- Full error output
- Steps to reproduce

**Response time:** 2-5 business days

---

## ✨ Feature Requests

Have an idea for improvement?

1. **Check discussions first:** Your idea may already be proposed
   - [Ideas discussion](https://github.com/pkeffect/pwa-framework/discussions/categories/ideas)

2. **File a feature request:**
   - [New feature](https://github.com/pkeffect/pwa-framework/issues/new?template=feature_request.md)
   - [New template](https://github.com/pkeffect/pwa-framework/issues/new?template=template_addition.md)

**Response time:** 1-2 weeks

---

## 🔐 Security Issues

**DO NOT** open public issues for security vulnerabilities.

**Instead:**
1. [Submit a security advisory](https://github.com/pkeffect/pwa-framework/security/advisories/new)
2. Or email: pkeffect@gmail.com

See [SECURITY.md](SECURITY.md) for full details.

**Response time:** 48 hours

---

## 📖 Self-Help Resources

### Common Issues

#### "Project name too long" Error

```bash
# Name must be 1-50 characters
python pwa_create.py "ThisNameIsWayTooLongAndExceedsTheFiftyCharacterLimit"
# ERROR: Project name too long (max 50 characters)

# Fix: Use shorter name
python pwa_create.py "short-game-name"
```

#### "Invalid project name" Error

```bash
# Must start with letter/number, only alphanumeric/hyphens/underscores
python pwa_create.py "../escape"
# ERROR: Project name must start with a letter or number

# Fix: Use valid characters
python pwa_create.py "my-game-2024"
```

#### "Folder already exists" Error

```bash
# Generator won't overwrite existing directories
python pwa_create.py existing-folder
# ERROR: Folder 'existing-folder' already exists

# Fix: Use different name or remove existing folder
rm -rf existing-folder
python pwa_create.py existing-folder
```

#### Generated Code Has Syntax Errors

```bash
# Check Python version compatibility
python --version
# Should be 3.10, 3.11, or 3.12

# Regenerate with known-good version
python3.12 pwa_create.py fresh-start
```

#### Service Worker Not Registering

```javascript
// Check browser console for errors
// Service Workers require HTTPS or localhost
// Fix: Use localhost for development
python -m http.server 8000
// Navigate to http://localhost:8000 (not file://)
```

### Debugging Tips

#### Verify File Count

```bash
cd your-project
find . -type f | wc -l
# Should output 24 (or more if templates added)
```

#### Check for Missing Files

```bash
# All 24 files should exist:
test -f index.html && echo "✓ index.html" || echo "✗ MISSING"
test -f manifest.json && echo "✓ manifest.json" || echo "✗ MISSING"
test -f service-worker.js && echo "✓ service-worker.js" || echo "✗ MISSING"
# ... etc
```

#### Validate Generated JavaScript

```bash
# Check for common issues
cd your-project

# No eval() (security risk)
grep -r "eval(" js/ && echo "FOUND eval()" || echo "✓ No eval()"

# Import statements have .js extension
grep -r "from ['\"]\..*['\"]" js/ | grep -v "\.js['\"]" && echo "MISSING .js" || echo "✓ Imports OK"
```

#### Test in Browser

```bash
# Start local server
python -m http.server 8000

# Open browser to:
# http://localhost:8000

# Check browser console (F12) for:
# - Service Worker registration
# - No 404 errors
# - No JavaScript errors
```

---

## 🤝 Contributing

Want to help improve the project?

- **Read:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Code of Conduct:** [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
- **Start with:** [Good first issues](https://github.com/pkeffect/pwa-framework/labels/good%20first%20issue)

---

## 📧 Direct Contact

For matters not suitable for public discussion:

- **Maintainer:** [@peffect](https://github.com/peffect)
- **Email:** pkeffect@gmail.com
- **Response time:** 3-7 business days

**Please don't use direct contact for:**
- ❌ General questions (use Discussions)
- ❌ Bug reports (use Issues)
- ❌ Feature requests (use Issues)
- ❌ Security issues (use Security Advisory)

**Do use for:**
- ✅ Private inquiries
- ✅ Partnership opportunities
- ✅ Media/press inquiries
- ✅ Sensitive topics

---

## 🌍 Community

- **GitHub:** [pkeffect/pwa-framework](https://github.com/pkeffect/pwa-framework)
- **Discussions:** [Community forum](https://github.com/pkeffect/pwa-framework/discussions)
- **Releases:** [Latest versions](https://github.com/pkeffect/pwa-framework/releases)

---

## ⏱️ Response Time Expectations

| Channel | Response Time | Best For |
|---------|---------------|----------|
| **GitHub Discussions** | 24-48 hours | Questions, ideas, general help |
| **Bug Reports** | 2-5 business days | Reproducible errors |
| **Feature Requests** | 1-2 weeks | Enhancement proposals |
| **Security Issues** | 48 hours | Vulnerabilities |
| **Email** | 3-7 business days | Private matters |

---

## 📜 License

This project is open source under the [MIT License](LICENSE).

Questions about licensing? See [LICENSE](LICENSE) or ask in Discussions.

---

**Last Updated:** January 11, 2026
