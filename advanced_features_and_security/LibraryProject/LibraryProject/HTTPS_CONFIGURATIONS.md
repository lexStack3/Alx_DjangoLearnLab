# Securing Django with HTTPS and Security Header
---
## Overview
This documentation explains how I configured my Django application to enforce secure HTTPS connections, enable security-related headers, and ensure secure cookie transmission.
These changes strengthen the application against common security vulnerabilities such as man-in-the-middle attacks, clickjacking, and cross-site scripting (XSS).

## Objectives
- Force all request to use HTTPS.
- Secure cookies so they are transmitted only over HTTPS.
- Add HTTP response headers to protect against clickjacking, MIME-sniffing, and XSS.
- Configure the server to serve the application securely with SSL/TLS.

---
## Steps Taken
#### 1. Enforcing HTTPS in Django
Updated `settings.py` to redirect all HTTP requests to HTTPS and instruct browsers to always use HTTPS.
```python
# Redirect all HTTP requests to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (HSTS) - enforce HTTPS for 1 year
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```
**WHY**: HSTS prevents browsers from connecting to the server over insecure HTTP, reducing the risk of protocol downgrade attacks.

#### 2. Securing Cookies
Configured session and CSRF cookies to be transmitted only over HTTPS.
```python
# Only send cookies over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```
**WHY**: This prevents sensitive cookies from being intercepted over insecure connections.

#### 3. Implementing Security Headers
Added extra security headers to protect against clickjacking, MIME-sniffing, and XSS.
```python
# Prevent clickjacking
X_FRAME_OPTIONS = "DENY"

# Prevent MIME type sniffing
SECURE_CONTENT_TYPE_NOSNIFF = True

# Enable browser XSS protection
SECURE_BROWSER_XSS_FILTER = True
```
**WHY**: These headers instruct browsers to block malicious framing, avoid executing non-declared file types, and stop certain cross-site scripting attempts.

#### 4. Configuring HTTPS in Deployment
Configured the web server (e.g., Nginx or Apache) to use SSL/LTS certificates.

Example (Nginx SSL config):
```sh
server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/ssl/certs/ssl_cert.crt;
    ssl_certificate_key /etc/ssl/private/ssl_key.key

    location / {
        proxy_pass http://127.0.0.1:8000;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_url;
}
```
**WHY**: SSL/TLS encrypts all traffic between the server and client, making it unreadable to attackers.

#### 5. Testing
After configuration:
- Accessing via `http://` redirects to `https://`
- Security headers verified using:
```bash
(env) $ curl -I https://localhost
```
- SSL certificate tested with <a href="https://www.ssllabs.com/ssltest/">SSL LABs</a>

---
### Conclusion
With this configuration:
- All requests are encrypted (HTTPS).
- Cookies are secure.
- Additional HTTP security headers are enforced.
- The application follows ALX security best practices for production deployment.