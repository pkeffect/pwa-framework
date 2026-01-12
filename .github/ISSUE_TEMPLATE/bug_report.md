---
name: Bug Report
about: Report incorrect or broken output from the generator
title: '[BUG] '
labels: bug
assignees: ''
---

## Bug Description

<!-- Clear description of what went wrong -->

## Environment

- **OS:** <!-- Windows 11, macOS 14, Ubuntu 22.04, etc. -->
- **Python Version:** <!-- Output of `python --version` -->
- **Generator Version:** <!-- Check line 24 in pwa_create.py or run `python pwa_create.py --version` -->
- **Project Name Used:** <!-- The name you provided to the generator -->

## Command Used

```bash
# Paste the exact command you ran
python pwa_create.py my-game
```

## Expected Behavior

<!-- What you expected to happen -->

## Actual Behavior

<!-- What actually happened -->

## Error Output

```
<!-- Paste full error traceback/output here -->
```

## Files Not Created (if applicable)

Check which of the 24 expected files are missing:

- [ ] index.html
- [ ] manifest.json
- [ ] service-worker.js
- [ ] README.md
- [ ] .gitignore
- [ ] css/main.css
- [ ] css/ui.css
- [ ] js/main.js
- [ ] js/core/Renderer.js
- [ ] js/core/GameLoop.js
- [ ] js/core/AssetLoader.js
- [ ] js/core/AudioManager.js
- [ ] js/core/InputManager.js
- [ ] js/scenes/SceneManager.js
- [ ] js/scenes/MenuScene.js
- [ ] js/scenes/GameScene.js
- [ ] js/state/Store.js
- [ ] js/state/SaveSystem.js
- [ ] js/state/Settings.js
- [ ] js/state/Scoreboard.js
- [ ] js/ui/UIManager.js
- [ ] js/ui/ErrorDisplay.js
- [ ] js/utils/MathUtils.js
- [ ] js/utils/DOMUtils.js
- [ ] js/utils/ErrorHandler.js

## Files With Errors (if applicable)

<!-- List any generated files that have syntax errors or incorrect content -->

## Steps to Reproduce

1. 
2. 
3. 

## Additional Context

<!-- Screenshots, generated file contents, anything else relevant -->

## Validation Checklist

- [ ] I've verified Python version is 3.10-3.12
- [ ] I've tried with a different project name
- [ ] I've checked file/folder permissions in the target directory
- [ ] I've reviewed the error output above
