---
name: it-infrastructure
description: "IT operations, system administration, infrastructure, and DevOps. Use when the user asks about servers, networking, cloud (AWS/GCP/Azure), Docker, Kubernetes, CI/CD, monitoring, backups, disaster recovery, DNS, SSL, firewalls, VPNs, Active Directory, Linux/Windows administration, database administration, or any IT infrastructure question. Also for troubleshooting, security hardening, and infrastructure planning."
metadata:
  version: "1.0.0"
  author: "custom"
---

# IT Infrastructure & Operations

Practical, production-tested guidance. Security-first. Automate everything that can be automated.

## Server Setup Checklist (Linux)

1. **OS**: Update all packages. Enable unattended security updates.
2. **Users**: Disable root SSH. Create admin user with sudo. SSH key only (no passwords).
3. **Firewall**: UFW/iptables — deny all, allow only needed ports (22, 80, 443).
4. **SSH hardening**: Change port, disable password auth, fail2ban.
5. **Monitoring**: Install node_exporter + Prometheus or Netdata for real-time.
6. **Logging**: Centralize with rsyslog/journald → ELK or Loki.
7. **Backups**: Automated daily, tested monthly. 3-2-1 rule (3 copies, 2 media, 1 offsite).
8. **Time sync**: NTP configured.
9. **Swap**: Configured based on RAM (1x for >8GB, 2x for <8GB).

## Cloud Architecture Patterns

| Pattern | When to use |
|---|---|
| Single server | Prototypes, <1K users, budget-constrained |
| Load balancer + app servers | Horizontal scaling, HA needed |
| Containers (Docker/K8s) | Microservices, consistent deploys, team >3 devs |
| Serverless (Lambda/Cloud Functions) | Event-driven, sporadic traffic, <15min execution |
| CDN + Static + API | JAMstack, global audience, cacheable content |
| Multi-region | Compliance requirements, global low-latency, DR |

## Networking Essentials

- **DNS**: A/AAAA for servers, CNAME for aliases, MX for email, TXT for verification/SPF/DKIM
- **SSL/TLS**: Always. Let's Encrypt for free, auto-renew with certbot. HSTS header.
- **VPN**: WireGuard (fast, modern) or OpenVPN (broader compatibility)
- **Subnets**: Separate public (web), private (app), database (no internet) tiers
- **Load balancing**: Health checks, session affinity only if needed, prefer stateless

## Docker Best Practices

- Multi-stage builds to minimize image size
- Non-root user in container
- Pin base image versions (not :latest)
- .dockerignore to exclude unnecessary files
- Health checks in Dockerfile
- Resource limits (--memory, --cpus)
- Use docker-compose for local dev, Kubernetes for production

## CI/CD Pipeline

```
Code Push → Lint → Test → Build → Security Scan → Deploy Staging → Integration Test → Deploy Production
```

- Every step must be automated and reproducible
- Staging must mirror production (same infra, same config)
- Blue-green or canary deployments for zero-downtime
- Rollback plan: one command to revert
- Secrets in vault (not in code, not in env files in repo)

## Monitoring Stack

| Layer | Tool options | What to watch |
|---|---|---|
| Infrastructure | Prometheus + Grafana, Datadog | CPU, RAM, disk, network, uptime |
| Application | APM (New Relic, Datadog, Sentry) | Response time, error rate, throughput |
| Logs | ELK, Loki + Grafana, CloudWatch | Errors, security events, audit trail |
| Uptime | UptimeRobot, Pingdom, Blackbox Exporter | Endpoint availability, SSL expiry, DNS |
| Alerts | PagerDuty, Opsgenie, Slack webhooks | On-call rotation, escalation policies |

Alert on symptoms (high error rate) not causes (high CPU). Set thresholds that mean action, not noise.

## Backup Strategy (3-2-1)

- **3** copies of data (original + 2 backups)
- **2** different storage types (local + cloud, or SSD + tape)
- **1** offsite (different region/provider)
- Automated daily, tested quarterly (restore test)
- Database: pg_dump/mysqldump + WAL archiving for point-in-time recovery
- Files: rsync/rclone to object storage (S3, B2)
- Document RTO (Recovery Time Objective) and RPO (Recovery Point Objective)

## Security Hardening

- Principle of least privilege everywhere
- MFA on all admin accounts
- Regular patching schedule
- Network segmentation
- Intrusion detection (OSSEC, Wazuh)
- Regular vulnerability scanning
- Incident response plan documented and tested
- Secrets management: HashiCorp Vault, AWS Secrets Manager, or similar

## Troubleshooting Flow

1. **Reproduce**: Can you reliably trigger the issue?
2. **Isolate**: Which component? (network, app, database, DNS, etc.)
3. **Logs**: What do the logs say at the time of the issue?
4. **Recent changes**: What changed? Deployment? Config? Traffic spike?
5. **Quick wins**: DNS propagation? Certificate expiry? Disk full? OOM?
6. **Systematic**: Binary search — disable half the components, narrow down
7. **Fix and document**: Root cause, fix applied, prevention measure
