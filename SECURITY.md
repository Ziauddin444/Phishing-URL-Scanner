# Security Policy

## Reporting Security Issues

**Do not** open public GitHub issues for security vulnerabilities. Instead, please email your findings to the project maintainers privately.

### Responsible Disclosure

1. **Do** report vulnerabilities to maintainers privately
2. **Do** give us reasonable time to fix issues (typically 90 days)
3. **Do** help us understand the vulnerability scope
4. **Don't** publicly disclose vulnerabilities before fixes are available
5. **Don't** access or modify other users' data

## Security Considerations for Users

### 1. Environment Variables
- Always use `.env` file for sensitive configuration
- Never commit `.env` file to version control
- Copy `.env.example` to `.env` and update values
- Use strong SECRET_KEY in production

### 2. URL Analysis
- This tool analyzes URL characteristics for phishing patterns
- It makes network requests to check for redirects (can be disabled)
- Some URLs may not be analyzable due to network restrictions
- Always verify results with multiple sources

### 3. Deployment Security

#### Local Development
```bash
# Safe for development only
export FLASK_ENV=development
export DEBUG=False  # Turn off debug mode
python src/app.py
```

#### Production Deployment
```bash
# Use production configuration
export FLASK_ENV=production
export DEBUG=False
export SECRET_KEY=very-long-random-secure-key

# Restrict CORS to your own domain(s)
export CORS_ALLOWED_ORIGINS=https://yourdomain.com

# Use WSGI server (Gunicorn 26+)
gunicorn -w 4 -b 0.0.0.0:3000 "src.app:app"

# Use HTTPS
# Use reverse proxy (nginx)
# Implement rate limiting
# Add authentication if needed
```

### 4. Data Privacy
- URLs are analyzed locally
- No user data is logged by default
- Feature data is not stored permanently
- For production, consider:
  - Implementing audit logs
  - Adding rate limiting
  - Using HTTPS only
  - Adding authentication

### 5. Dependency Security

Dependencies are pinned to patched versions. Run the following locally before any release:

```bash
# Audit for known CVEs (replaces deprecated `pip audit`)
pip-audit -r requirements.txt --desc

# Or upgrade all pinned packages and re-audit
pip install --upgrade -r requirements.txt
pip-audit -r requirements.txt
```

A `pip-audit` check also runs automatically in GitHub Actions on every push and pull request (see `.github/workflows/security.yml`).

## Security Features Implemented

✅ **Input Validation**
- URL length limits (2048 characters)
- Format validation
- Type checking

✅ **Error Handling**
- No sensitive data in error messages
- Proper exception handling
- Graceful degradation

✅ **Configuration**
- Secrets in environment variables
- Separate configs for dev/prod
- Secure defaults

✅ **CORS**
- Origin allowlist driven by `CORS_ALLOWED_ORIGINS` environment variable
- Private network access disabled (`allow_private_network=False`)
- Credentials not forwarded when using wildcard origins

✅ **HTTP Security Headers** (implemented via `@app.after_request`)
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Content-Security-Policy: default-src 'self'`
- `Strict-Transport-Security` (when HTTPS / production)
- `Server` fingerprinting header removed

✅ **API Security**
- JSON input validation
- Content-Type checking
- Request size limits
- Raw exception messages never exposed to API consumers

✅ **CI/CD Security Gate**
- `pip-audit` runs on every push and pull request (`.github/workflows/security.yml`)
- Weekly scheduled scan catches newly-published CVEs against pinned versions

## Future Security Improvements

- [ ] Rate limiting on API endpoints (e.g., `flask-limiter`)
- [ ] API authentication / API key support
- [ ] HTTPS enforcement at the application layer
- [ ] Audit logging (request source, URL scanned, result)
- [ ] Input sanitization enhancements

## Security Guidelines for Contributors

### Code Review
- All contributions reviewed for security
- No hardcoded secrets allowed
- Input validation required
- Error messages reviewed

### Testing
- Security tests included
- OWASP Top 10 considerations
- SQL injection prevention (when applicable)
- XSS prevention (client-side code)

### Dependencies
- Minimize external dependencies
- Review new dependencies
- Keep dependencies updated
- Check for known vulnerabilities

## Vulnerability Disclosure Timeline

1. **Day 1**: Report received
2. **Day 2-5**: Initial assessment
3. **Day 6-30**: Fix development
4. **Day 31-60**: Testing and validation
5. **Day 61-90**: Patch release
6. **Day 91**: Public disclosure (if not already disclosed)

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Flask Security](https://flask.palletsprojects.com/en/2.3.x/security/)
- [CWE Top 25](https://cwe.mitre.org/top25/)

---

**Thank you for helping keep Phishing URL Scanner secure!** 🔒
