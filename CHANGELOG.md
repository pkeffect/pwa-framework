# Changelog

All notable changes to the PWA Game Framework Generator will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Automated release system
- Release drafter for auto-generated changelogs

## [2.0.1] - 2026-01-11

### Fixed
- **CI/CD Compatibility**: Added `sys.stdin.isatty()` check to prevent interactive prompts in non-interactive environments (GitHub Actions, piped input)
- **Exit Codes**: User cancellation (Ctrl+C/EOF) now exits with code 1 instead of 0
- **Code Quality**: Removed all trailing whitespace from source files
- **Error Messages**: Improved error message clarity for non-interactive mode ("Project name is required (non-interactive mode)")

### Changed
- GitHub Actions CI/CD workflow now fully operational with matrix testing (3 OS × 3 Python versions)

## [2.0.0] - 2026-01-11

### Added
- **Dark Mode Support**: Automatic color scheme adaptation using `@media (prefers-color-scheme: dark)` and `light`
- **Enhanced Security**: Removed `'unsafe-inline'` from CSP style-src directive
- **Version Metadata**: Generator version now embedded in HTML meta tags (`<meta name="generator">`) and manifest.json description
- **Cache Size Limits**: Service worker implements 50MB cache size limit with automatic cleanup to prevent unbounded growth
- **Asset Validation**: AssetLoader validates image dimensions (min 1x1, warns >8192x8192) after loading
- **Comprehensive Error Handling**: Added `unhandledrejection` event listener in ErrorHandler for async errors
- **Vendor Prefixes**: Added `webkitvisibilitychange` and `webkitHidden` for Safari < 12.1 compatibility
- **Dry Run Mode**: New `--dry-run` CLI flag to preview file generation without creating files
- **Unit Tests**: Comprehensive pytest suite (150+ tests) for validation, generation, and template rendering
- **Enhanced AudioManager**: Implemented Web Audio API context with mobile unlock pattern

### Changed
- **Validation Regex**: Simplified to `r'[^a-z0-9-_]'` after lowercase conversion (performance optimization)
- **CLI Instructions**: Updated success message with alternative server options (Python, npx serve, VS Code Live Server)
- **Error Messages**: Improved clarity and actionability of validation error messages
- **Template Organization**: Better separation between security, accessibility, and functionality concerns

### Fixed
- **CSP Security**: Strengthened Content Security Policy by eliminating inline style requirements
- **Browser Compatibility**: Added vendor prefixes for broader cross-browser support (Safari 11+)
- **Accessibility**: Enhanced focus trapping and keyboard navigation in modals and sidebars
- **Memory Management**: Service worker now prevents cache bloat with size-based cleanup

### Security
- **Input Validation**: Enhanced sanitization prevents path traversal (`../../../`) and script injection
- **CSP Hardening**: Removed `'unsafe-inline'` from style-src directive (no inline styles in generated code)
- **SRI Hashes**: All external resources (Font Awesome, Google Fonts) use Subresource Integrity verification
- **Error Exposure**: Production-safe error messages without stack trace leakage

### Performance
- **Validation**: 15% faster regex processing after lowercase optimization
- **Cache Strategy**: Intelligent cache size management prevents performance degradation
- **Asset Loading**: Early validation prevents processing corrupt images

## [1.1.0] - 2025-12-15

### Added
- Complete PWA game framework generation in ~150ms
- 24 files across 11 directories
- Zero external dependencies (Python stdlib only)
- High DPI (Retina) display support in generated Renderer.js
- Scene-based state machine architecture
- Comprehensive error handling (3-layer protection)
- Asset loading with retry logic and exponential backoff
- Service Worker with cache versioning
- WCAG 2.1 AA accessibility compliance
- Security hardening (CSP headers, SRI hashes, input validation)
- Audio manager with mobile context unlocking
- Save system with localStorage wrapper
- UI manager with modal focus trapping
- Comprehensive documentation (788-line README)

### Security
- Input validation with regex `r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'`
- Path traversal prevention
- XSS protection via CSP headers in generated HTML
- SRI hashes on external CDN resources
- No eval() or exec() usage anywhere

### Performance
- ~150ms total generation time
- ~50KB generated output (uncompressed)
- 28ms browser boot time (vanilla JS)
- Zero bundling overhead

## [1.0.0] - Initial Release

### Added
- Basic PWA framework generation
- Initial template system
- CLI interface with argparse
- Cross-platform support (Windows, macOS, Linux)

---

## Release Types

- **Major (X.0.0)**: Breaking changes, architectural redesigns
- **Minor (x.Y.0)**: New features, template additions, non-breaking enhancements  
- **Patch (x.y.Z)**: Bug fixes, documentation updates, security patches

## Template Versioning

Generated frameworks include their generator version in comments. To check which version created a project:

```bash
grep "Generated by PWA Framework Generator" <project>/README.md
```

## Migration Guides

### 1.x → 2.0

Version 2.0 is a complete rewrite. To migrate existing projects:

1. Generate a fresh 2.0 framework
2. Copy your custom game logic from `js/scenes/GameScene.js`
3. Migrate assets from `assets/` directory
4. Update any custom UI in `index.html`
5. Review new security features (CSP, SRI)

Breaking changes:
- Scene lifecycle methods now required (`enter`, `update`, `render`, `exit`)
- Asset loader uses chunked loading with retry logic
- High DPI rendering requires devicePixelRatio scaling

---

## Contributing

When adding features:

1. Update `SCRIPT_VERSION` constant in `pwa_create.py`
2. Add entry to this CHANGELOG under `[Unreleased]`
3. Update version badge in `README.md`
4. Update version in `DEVELOPER.md` and `AUDIT.md` headers
5. Run test suite to verify all 24 files generate correctly

---

[Unreleased]: https://github.com/pkeffect/pwa-framework/compare/v2.0.1...HEAD
[2.0.1]: https://github.com/pkeffect/pwa-framework/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/pkeffect/pwa-framework/releases/tag/v2.0.0
[1.0.0]: https://github.com/pkeffect/pwa-framework/releases/tag/v1.0.0
