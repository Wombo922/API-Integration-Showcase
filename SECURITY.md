# Security Policy

## 🔒 Reporting Security Issues

If you discover a security vulnerability, please **DO NOT** open a public issue. Instead:

1. Email: anthonygalindo922@gmail.com
2. Include detailed description of the vulnerability
3. Provide steps to reproduce if applicable
4. Allow 48 hours for initial response

## 🛡️ Security Best Practices

### API Key Management
- **NEVER commit `.env` file** to version control
- Use `.env.example` as template only
- Rotate API keys regularly (every 90 days recommended)
- Use separate keys for development and production

### Sensitive Files Protected
The following files are automatically ignored by `.gitignore`:
- `.env` and all environment files
- `dashboard_cache.json` (may contain API responses)
- `CONSOLIDATED_MASTER_KEY_LIST.txt` 
- All credential and secret files

### Deployment Security
- Use HTTPS in production
- Set proper CORS policies
- Implement rate limiting on endpoints
- Use environment variables for all secrets
- Never expose Flask debug mode in production

## ✅ Security Checklist Before Pushing

- [ ] No API keys in code
- [ ] `.env` file not committed
- [ ] `.gitignore` properly configured
- [ ] No hardcoded credentials
- [ ] Sensitive files listed in `.gitignore`
- [ ] README doesn't contain real API keys

## 🔐 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| Latest  | ✅ Yes             |
| Older   | ❌ No              |

## 📝 Security Updates

This project is actively maintained. Security updates will be released as needed.
