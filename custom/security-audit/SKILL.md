---
name: security-audit
description: "Authorized web-application security audit / pentest methodology the agent runs itself — no external tool or LLM key. Use when the user asks to security-test, pentest, scan, audit, or 'find ways to hack' a site or codebase THEY own or are authorized to test (e.g. 'افحص الموقع', 'اختبر الاختراق', 'security review', 'vulnerabilities', 'is my site secure'). Covers recon, static code review, safe non-destructive active probing, OWASP Top 10, and a severity-ranked report. Laravel/PHP-aware but general. Refuses unauthorized targets and destructive/DoS actions."
---

# Web Application Security Audit

A structured methodology for auditing a web app the user **owns or is explicitly authorized to test**. You (the agent) are the pentester — you already reason like the LLM a tool like VulnClaw would call, and you can read the codebase directly, so no external scanner or API key is needed. This keeps all data local and gives higher-signal, lower-false-positive results than a black-box tool.

## Keywords
security audit, pentest, penetration test, vulnerability scan, security review, find vulnerabilities, is my site secure, hack my site, OWASP, injection, XSS, CSRF, IDOR, broken access control, exposed secrets, security headers, افحص الموقع, اختبر الاختراق, ثغرات, أمان الموقع, فحص أمني

## HARD GATES — read first, every time

1. **Authorization.** Only proceed against a target the user owns or is clearly authorized to test. If there is any doubt, ask one confirming question and stop until answered. Never test a third party's site, and never help target infrastructure the user does not control.
2. **Non-destructive by default.** Static review and passive/read-only probing are always allowed. For anything that *writes, deletes, brute-forces, floods, or could take the target down*, STOP and get explicit per-action go-ahead. Never run DoS/stress, mass account creation, data-destroying payloads, or detection-evasion for malicious ends.
3. **Prefer staging over production for active tests.** Point active probes at a local/staging copy when one exists. Active-test production only with explicit confirmation, and keep it read-only.
4. **Never print secrets.** When you find a secret (key, token, password, .env value), report *that it exists and where*, never the value. Reference config by key name only.
5. **Report, don't weaponize.** Output is a defensive report: the flaw, how to confirm it, its impact, and the fix. Provide a proof-of-concept only to the extent needed to demonstrate the issue on the authorized target — not a reusable attack kit.

## Process

Create a todo per phase and work them in order. Scale depth to the user's ask ("quick check" vs "thorough audit").

### 1. Scope & recon
- Confirm the target (URL and/or codebase path) and that it's authorized.
- Map the app: framework/stack, routes/endpoints, auth model, roles, the trust boundaries (what's public vs authenticated vs admin), and every place untrusted input enters (forms, query/route params, headers, file uploads, webhooks, APIs).
- For a codebase: read the router, middleware, controllers, models, config, and dependency manifests. Build a picture of the attack surface before diving in.

### 2. Static code review (highest signal when you have the code)
Work through these, citing `file:line` for each finding:
- **Broken access control / IDOR** — routes missing auth/authorization middleware; object lookups by user-supplied id without an ownership check; admin actions reachable by non-admins; mass assignment (unguarded fillable / `$request->all()` into models).
- **Injection** — raw SQL / string-interpolated queries / `DB::raw` / unparameterised queries; OS command exec (`shell_exec`, `exec`, `system`, `proc_open`); LDAP/NoSQL/template injection.
- **XSS** — unescaped output (Blade `{!! !!}`, `->raw()`, `v-html`, `dangerouslySetInnerHTML`); reflected user input; unsanitised URLs (`javascript:`), rich-text/HTML stored without sanitising.
- **CSRF** — state-changing routes without CSRF protection; `VerifyCsrfToken` exceptions; SameSite cookie config.
- **Auth & session** — password hashing (bcrypt/argon vs md5/sha1); default/seeded credentials; predictable tokens; session fixation; missing rate-limit/lockout on login and OTP; JWT alg/secret issues.
- **Secrets & config** — hardcoded keys/tokens; `.env`/`.git` committed or web-served; `APP_DEBUG=true` in prod; verbose error pages; overly-permissive CORS.
- **SSRF / file handling** — user-controlled URLs fetched server-side; unrestricted file upload (type/size/location, then served/executed); path traversal in file params.
- **Insecure deserialization**, **open redirect**, **race conditions** on balance/coins/inventory-type operations (check for locking/transactions).
- **Dependencies** — known-vulnerable packages (`composer audit`, `npm audit`); outdated framework.

### 3. Safe active probing (non-destructive, authorized target only)
Use `curl` / read-only requests. Confirm, don't exploit:
- **Security headers & cookies** — `curl -sI`: HSTS, X-Content-Type-Options, X-Frame-Options/CSP, Referrer-Policy; cookie `Secure`/`HttpOnly`/`SameSite`.
- **Exposed paths** — `/.env`, `/.git/config`, `/storage/`, `/vendor/`, `phpinfo`, backups (`.bak`, `.sql`, `.zip`), `/telescope`, `/horizon`, `/_ignition` (Laravel debug), directory listing. Expect 403/404; a 200 is a finding.
- **Error verbosity** — trigger a benign 404/500 and check for stack traces / framework version leakage.
- **Auth flows** — is a protected page reachable unauthenticated? does logout invalidate the session? is there rate-limiting on login (a few attempts, not a brute-force)?
- **TLS** — cert validity, protocol/redirect (`http`→`https`).
Keep request volume low and payloads benign. Anything beyond confirmation needs go-ahead.

### 4. Verify & rank
- Re-check each candidate finding to kill false positives (does the code path actually reach it? is there a compensating control?).
- Rank by severity (Critical/High/Medium/Low) using real-world impact + ease of exploit.
- Note the blast radius (single user vs all users vs full compromise).

### 5. Report
Deliver a ranked report. For each finding:
- **Title + severity.**
- **Where** — `file:line` (static) or the request/endpoint (active).
- **Impact** — what an attacker gains.
- **Proof** — the minimal evidence it's real (a code excerpt, a response snippet — secrets redacted).
- **Fix** — the concrete remediation (and framework-idiomatic way to do it).

End with a short prioritized action list (fix these first) and note anything you did NOT test (so coverage is honest).

## Laravel / Filament specifics (when the stack matches)
- Middleware on routes (`auth`, custom gates, admin panel access); Filament resource `canAccess`/policies; `Gate`/policies coverage.
- Mass assignment (`$fillable`/`$guarded`), `$request->all()` into `create/update`.
- Blade `{!! !!}`, `@php`, and any custom "raw/safe url" helpers.
- `config/app.php` debug, `APP_ENV`, `APP_KEY` set; `TrustProxies`; session `secure`/`same_site`; `SANCTUM`/`CORS` config.
- Seeders/factories leaving default admin creds in non-local envs.
- Signed URLs, throttling middleware on sensitive/public POST routes, webhook signature verification (HMAC).
- Storage: `public` disk exposure, `storage:link`, upload validation.

## Notes
- Favor breadth first (map everything), then depth on the riskiest areas.
- A clean result is a valid result — say so plainly rather than inventing findings.
- If the user wants an external active scanner too, recommend well-known vetted tools (OWASP ZAP, nuclei, nikto) against staging — but this skill's own value is the code-aware review you do directly.
