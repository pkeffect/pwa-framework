---
name: Feature Request
about: Suggest an enhancement to the generator
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## Feature Description

<!-- Clear description of the feature you'd like added -->

## Problem it Solves

<!-- What problem does this feature address? -->

## Proposed Solution

<!-- How would you implement this? -->

## Type of Feature

- [ ] **New generated file** (e.g., ParticleSystem.js, TilemapLoader.js)
- [ ] **Modification to existing template** (e.g., improve Renderer.js)
- [ ] **Generator enhancement** (e.g., new CLI option)
- [ ] **Documentation improvement**
- [ ] **Other:** ___________

## Details (for new generated files)

**File path:** `js/___/_____.js`

**Purpose:** <!-- What would this file do? -->

**Dependencies:** <!-- What other generated files would it interact with? -->

**Approximate LOC:** <!-- Rough estimate -->

## Example Usage (if applicable)

```javascript
// Show how a developer would use this feature
import { NewFeature } from './proposed/NewFeature.js';

const feature = new NewFeature();
feature.doSomething();
```

## Alternatives Considered

<!-- What other approaches could solve this problem? -->

## Impact Assessment

- [ ] **Breaking change** (would affect existing generated projects)
- [ ] **Non-breaking addition** (backward compatible)
- [ ] **Zero dependency impact** (maintains stdlib-only requirement)
- [ ] **Increases generated output size** (estimate: _____ KB)
- [ ] **Affects generation time** (estimate: _____ ms increase)

## Related Documentation

- [ ] Would require README.md update
- [ ] Would require DEVELOPER.md update
- [ ] Would require new section in generated README
- [ ] No documentation changes needed

## Additional Context

<!-- Mockups, code samples, links to similar implementations -->

## Alignment with Project Philosophy

How does this align with:
- ✨ **Zero build step** - 
- 📦 **Zero dependencies** - 
- 🚀 **~150ms generation** - 
- 🎮 **Game-focused** - 

## Validation

- [ ] I've checked this isn't already in the generated framework
- [ ] I've reviewed DEVELOPER.md to understand the architecture
- [ ] This feature maintains the zero-dependency philosophy
