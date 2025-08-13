# Implementing Security Best Practices in Django
---
## Overview
This project is configured with Django security best practices suitable for a production environment. The goal is to protect against common web vulnerabilities such as Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), clickjacking, and session hijacking.

## Security Settings Applied
#### 1. Debug Mode Disabled
```python
DEBUG = False
```
- Prevents sensitive debug information from bing exposed to users.
- Ensures that Django returns proper error pages instead of detailed stack traces.

#### 2. Allowed Hosts
```python
# For testing; should be replaced with production domain(s)
ALLOWED_HOSTS = ["*"]
```
- Restricts which hostnames can serve the application.
- `"*"` allows all hosts (temporary for testing).
- **Production recommendation**: explicitly list domain names or IP addresses.

#### 3. Browser Security Headers
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```
- `SECURE_BROWSER_XSS_FILTER`: Activates browser XSS protection.
- `SECURE_CONTENT_TYPE_NOSNIFF`: Prevents MIME-type sniffing.
- `X_FRAME_OPTIONS`: Stops the site from being embedded in iframes (prevents clickjacking)

#### 3. Secure Cookies
```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
- Ensures cookies are only sent over HTTPS, preventing theft over insecure connections.

#### 4. Content Security Policy (CSP)
Install `django-csp` if you haven't already
```bash
(env) $ pip install django-csp
```
Then add:
```python
# Append CSP Middleware
MIDDLEWARE = [
    ...
    'csp.middleware.CSPMiddleware',
]

# Set CSP Configurations
CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "https://cdnjs.cloudflare.com")
CSP_STYLE_SRC = ("'self'", "https://fonts.googleapis.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com")
CSP_IMG_SRC = ("'self'", "data:")
CSP_FRAME_SRC = ("'self'",)
```
- Restricts where resources (scripts, styles, fonts, images) can be loaded from.
- Mitigates XSS by disallowing untrusted content.


---
Security Audit
To verify production readiness, run:
```bash
(env) $ python manage.py check --deploy
```
This checks for missing security configurations according to Django's deployment checklist.