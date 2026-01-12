# Security Policy

## Supported Versions

We actively maintain security updates for the following versions:

| Version | Supported          | Status |
| ------- | ------------------ | ------ |
| 2.0.x   | :white_check_mark: | Active |
| 1.x.x   | :x:                | EOL    |

**Recommendation:** Always use the latest version from [releases](https://github.com/pkeffect/pwa-framework/releases).

---

## Scope

This security policy covers:

1. **Generator Script (`pwa_create.py`)** - Input validation, file operations, code generation
2. **Generated Framework Output** - Security features in scaffolded projects

### What's In Scope

- ✅ Input validation bypasses (path traversal, injection)
- ✅ Code injection vulnerabilities in generator
- ✅ XSS vulnerabilities in generated HTML/JS
- ✅ CSP header bypasses in generated output
- ✅ Unsafe code patterns in templates (eval, innerHTML with user data)
- ✅ Hardcoded secrets/credentials
- ✅ Path traversal in file generation
- ✅ DoS vectors (resource exhaustion, infinite loops)

### What's Out of Scope

- ❌ Vulnerabilities in Python interpreter itself
- ❌ Issues in user-added code (after customizing generated framework)
- ❌ Browser security bugs (report to browser vendors)
- ❌ General web security advice (see OWASP resources)
- ❌ Social engineering attacks

---

## Security Features

### Generator Script Protections

| Feature | Implementation | Protection Against |
|---------|----------------|---------------------|
| **Input Validation** | Regex `r'^[a-zA-Z0-9][a-zA-Z0-9_-]*$'` | Command injection, path traversal |
| **Length Limits** | 1-50 characters (MAX_PROJECT_NAME_LENGTH) | DoS via resource exhaustion |
| **Sanitization** | Lowercase, space→hyphen, dedupe | Directory name confusion |
| **Path Operations** | `pathlib.Path` only (no string concat) | Path traversal |
| **No Code Execution** | No `eval()`, `exec()`, `compile()` | Arbitrary code execution |
| **Exception Handling** | Specific exception types, no bare except | Information disclosure |

### Generated Framework Protections

| Feature | File | Protection Against |
|---------|------|---------------------|
| **CSP Headers** | index.html line 7 | XSS, data injection |
| **SRI Hashes** | index.html line 11 | CDN tampering |
| **Input Validation** | js/state/Settings.js | Stored XSS |
| **No eval()** | All JS files | Code injection |
| **No innerHTML** | All JS files | DOM XSS |
| **localStorage Wrapping** | js/state/SaveSystem.js | Quota exhaustion |
| **Error Handling** | js/utils/ErrorHandler.js | Information disclosure |

---

## Reporting a Vulnerability

### 🚨 **DO NOT** open public GitHub issues for security vulnerabilities

**Preferred Method:** GitHub Security Advisories
1. Go to https://github.com/pkeffect/pwa-framework/security/advisories/new
2. Click "Report a vulnerability"
3. Fill in the details using the template below

**Alternative Method:** Email
- **Contact:** pkeffect@gmail.com
- **PGP Key:** [Optional: Link to public key]

### Report Template

```
## Vulnerability Summary
One-line description of the issue.

## Affected Component
- [ ] Generator script (pwa_create.py)
- [ ] Generated HTML template
- [ ] Generated JavaScript template
- [ ] Generated CSS template
- [ ] Service Worker template
- [ ] Documentation

## Severity Assessment
- [ ] Critical (RCE, authentication bypass)
- [ ] High (XSS, CSRF, data exposure)
- [ ] Medium (DoS, information disclosure)
- [ ] Low (edge case, requires uncommon conditions)

## Proof of Concept
Step-by-step reproduction:
1. 
2. 
3. 

## Expected vs Actual Behavior
**Expected:**
**Actual:**

## Impact
Who is affected and how?

## Suggested Fix (optional)
```

### Response Timeline

| Stage | Timeframe |
|-------|-----------|
| **Initial Response** | 48 hours |
| **Triage & Validation** | 5 business days |
| **Fix Development** | Depends on severity |
| **Release & Disclosure** | Coordinated with reporter |

**Severity-based SLAs:**
- **Critical:** Patch within 7 days
- **High:** Patch within 30 days
- **Medium:** Patch within 90 days
- **Low:** Next scheduled release

---

## Disclosure Policy

We follow **Coordinated Vulnerability Disclosure**:

1. **Report received** → Private acknowledgment to reporter
2. **Validation** → Confirm vulnerability, assess severity
3. **Fix development** → Create patch (in private fork if needed)
4. **Reporter review** → Share fix with reporter for verification
5. **Release** → Publish patched version
6. **Public disclosure** → Security advisory published (30 days after fix or by agreement)

### Hall of Fame

We recognize security researchers who responsibly disclose vulnerabilities:

<!-- 
- [Researcher Name](https://github.com/username) - CVE-2026-XXXXX - January 2026
-->

*None yet - be the first!*

---

## Security Best Practices

### For Generator Users

When using `pwa_create.py`:

```bash
# ✅ Good - Validate you have the official script
curl -LO https://github.com/pkeffect/pwa-framework/releases/latest/download/pwa_create.py
curl -LO https://github.com/pkeffect/pwa-framework/releases/latest/download/SHA256SUMS
sha256sum -c SHA256SUMS

# ✅ Good - Use a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# ❌ Bad - Running from untrusted sources
curl random-site.com/pwa_create.py | python
```

### For Generated Framework Developers

After generating your project:

1. **Keep CSP strict:** Don't weaken Content-Security-Policy headers
2. **Validate user input:** Always sanitize before storing in localStorage
3. **Use HTTPS:** Service Workers require secure contexts
4. **Update dependencies:** If you add npm packages (breaking zero-dependency), keep them updated
5. **Review generated code:** Understand what you're deploying

### For Contributors

When submitting PRs:

1. **No hardcoded secrets** - Use environment variables or config
2. **Validate all inputs** - Especially if adding CLI options
3. **No dynamic code execution** - No eval(), exec(), compile()
4. **Use pathlib.Path** - Prevent path traversal
5. **Test XSS vectors** - If modifying HTML/JS templates
6. **Check CSP compliance** - Don't add inline scripts/styles

---

## Known Security Considerations

### Deliberate Design Decisions

1. **File Overwrite:** Generator overwrites existing directories without confirmation (intentional for rapid prototyping)
   - **Mitigation:** Pre-check directory existence, show clear error
   
2. **No Dependency Scanning:** Zero dependencies means no npm audit/pip check needed
   - **Benefit:** Eliminates entire class of supply chain attacks

3. **Minimal InputManager:** 3-line stub allows developers to implement keyboard/mouse/touch
   - **Risk:** Developers must implement their own input sanitization
   - **Mitigation:** Generated README includes security guidance

### Non-Issues

These are **not vulnerabilities**:

- ❌ "Generated code allows user input" - This is intentional; developers must sanitize
- ❌ "No HTTPS enforcement" - Local development uses http://localhost
- ❌ "localStorage used" - Standard web API, properly wrapped
- ❌ "CSS injection via custom properties" - Not exploitable for XSS

---

## Security Audit History

| Date | Version | Auditor | Findings | Status |
|------|---------|---------|----------|--------|
| 2026-01-11 | 2.0.0 | Internal (AUDIT.md) | 0 critical, 0 high | ✅ Passed |

**Next scheduled audit:** Q2 2026

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CSP Reference](https://content-security-policy.com/)
- [SRI Hash Generator](https://www.srihash.org/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)

---

## Contact

- **General Questions:** [Open a discussion](https://github.com/pkeffect/pwa-framework/discussions)
- **Security Issues:** pkeffect@gmail.com or [Security Advisory](https://github.com/pkeffect/pwa-framework/security/advisories/new)
- **Maintainer:** [@peffect](https://github.com/peffect)

**Last Updated:** January 11, 2026
