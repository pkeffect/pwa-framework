---
name: Template Addition
about: Propose a new file to be included in generated frameworks
title: '[TEMPLATE] Add '
labels: template, enhancement
assignees: ''
---

## Proposed Template

**File:** `js/___/_____.js`  
**Category:** <!-- core / scenes / state / ui / utils / other -->

## Purpose

<!-- What functionality does this template provide? -->

## Use Case

<!-- When would developers use this? Give 2-3 concrete examples -->

1. 
2. 
3. 

## Template Code

```javascript
// Paste proposed implementation here
// Keep it minimal - developers should customize this

export class ProposedComponent {
    constructor() {
        // Intentional stub or basic implementation?
    }
    
    // Methods...
}
```

## Integration Points

**Imports this template would need:**
```javascript
import { Renderer } from './core/Renderer.js';
// Other imports...
```

**Files that would import this template:**
- [ ] main.js
- [ ] SceneManager.js
- [ ] GameScene.js
- [ ] Other: ___________

## Documentation

**Generated README.md section:**

```markdown
### ProposedComponent

Brief description...

**Location:** `js/___/_____.js`  
**Lines:** ~50  
**Dependencies:** Renderer.js, Store.js

**Methods:**
- `method1()` - Description
- `method2()` - Description
```

## Implementation Checklist

For maintainer review:

- [ ] Create `Templates.get_js_proposedcomponent()` method
- [ ] Add to `structure` dict in `create_framework()`
- [ ] Update README.md (project structure section)
- [ ] Update DEVELOPER.md (file structure table)
- [ ] Update line counts in documentation
- [ ] Add to CI validation workflow
- [ ] Bump `SCRIPT_VERSION` (minor version)
- [ ] Update CHANGELOG.md

## Size Impact

**Estimated LOC:** _____ lines  
**Complexity:** <!-- Low / Medium / High -->  
**Output size increase:** ~_____ KB

## Design Philosophy Alignment

- [ ] **Intentional stub** (3-10 lines, developers customize heavily)
- [ ] **Basic implementation** (50-100 lines, works out-of-box)
- [ ] **Complete implementation** (100+ lines, production-ready)

## Alternatives

<!-- Could this be achieved by modifying an existing template instead? -->

## Related Features

<!-- Links to related issues/PRs -->

## Example Projects That Need This

<!-- Link to game jam projects, repos, or describe scenarios where this would be valuable -->
