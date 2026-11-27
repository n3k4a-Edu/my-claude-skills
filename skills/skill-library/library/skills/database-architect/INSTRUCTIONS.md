---
name: database-architect
description: "Database design, SQL optimization, schema modeling, and database administration. Use when the user asks about database schema design, normalization, indexing, query optimization, migrations, PostgreSQL, MySQL, MongoDB, Redis, SQLite, database scaling, replication, partitioning, or any database architecture question."
metadata:
  version: "1.0.0"
---

# Database Architect

Design for correctness first, then performance. Every schema decision has trade-offs — make them explicit.

## Schema Design Process

1. **Identify entities**: What are the nouns? (User, Order, Product, etc.)
2. **Identify relationships**: How do entities relate? (1:1, 1:N, M:N)
3. **Define attributes**: What data does each entity need?
4. **Normalize**: 3NF by default. Denormalize only when you can prove the performance need.
5. **Add constraints**: NOT NULL, UNIQUE, CHECK, FOREIGN KEY. The database is the last line of defense.
6. **Plan indexes**: Based on query patterns, not guesses.
7. **Consider time**: created_at, updated_at on every table. Soft delete (deleted_at) if needed.

## Naming Conventions

- Tables: `snake_case`, plural (`users`, `order_items`)
- Columns: `snake_case` (`first_name`, `created_at`)
- Primary keys: `id` (integer auto-increment or UUID)
- Foreign keys: `{referenced_table_singular}_id` (`user_id`, `order_id`)
- Indexes: `idx_{table}_{columns}` (`idx_users_email`)
- Constraints: `chk_{table}_{column}`, `uq_{table}_{column}`

## Indexing Strategy

### When to index
- Columns in WHERE clauses (frequently queried)
- Columns in JOIN conditions (foreign keys)
- Columns in ORDER BY (if sorting large result sets)
- Columns with high cardinality (many distinct values)

### When NOT to index
- Small tables (< 1000 rows, full scan is fine)
- Columns with low cardinality (boolean, status with 3 values)
- Tables with heavy writes and rare reads
- Already covered by a composite index

### Composite Index Rules
- Order matters: `(a, b, c)` covers queries on `(a)`, `(a, b)`, `(a, b, c)` but NOT `(b)` or `(c)` alone
- Most selective column first (unless range query changes the plan)
- Include covering columns to avoid table lookups

## Query Optimization

### Read the execution plan first
```sql
EXPLAIN ANALYZE SELECT ...;
```

Look for:
- **Seq Scan** on large tables → need an index
- **Nested Loop** with large tables → consider Hash Join
- **Sort** on large datasets → index the ORDER BY columns
- **Rows** estimate vs actual → stale statistics → ANALYZE

### Common Optimizations
1. **N+1 queries**: Use JOINs or subqueries, not loops
2. **SELECT ***: Only select columns you need
3. **Pagination**: Use keyset (`WHERE id > ?`) over OFFSET for large tables
4. **Bulk operations**: Batch INSERT/UPDATE, not one-by-one
5. **Connection pooling**: PgBouncer, ProxySQL — don't open/close connections

## PostgreSQL Specifics

```sql
-- Partial index (index only matching rows)
CREATE INDEX idx_orders_pending ON orders(created_at) WHERE status = 'pending';

-- GIN index for JSONB
CREATE INDEX idx_users_metadata ON users USING gin(metadata);

-- Full-text search
CREATE INDEX idx_articles_search ON articles USING gin(to_tsvector('english', title || ' ' || body));

-- Table partitioning
CREATE TABLE events (id bigint, created_at timestamptz, data jsonb)
PARTITION BY RANGE (created_at);
```

## Scaling Patterns

| Pattern | When | Complexity |
|---|---|---|
| Read replicas | Read-heavy, write ratio < 20% | Low |
| Connection pooling | Many short-lived connections | Low |
| Caching (Redis) | Hot data, repeated reads | Medium |
| Vertical scaling | Easy wins left (RAM, SSD) | Low |
| Partitioning | Large tables, time-series data | Medium |
| Sharding | Write-heavy, > 1TB, global scale | High |

## Migration Best Practices

- One change per migration (don't mix schema + data changes)
- Always write a rollback (down migration)
- Test on a copy of production data before deploying
- For large tables: add column → backfill → add constraint (not all at once)
- Zero-downtime: expand-contract pattern (add new, migrate data, remove old)

## Redis Patterns

| Pattern | Use case |
|---|---|
| Cache-aside | Read-through caching with TTL |
| Session store | User sessions with auto-expiry |
| Rate limiter | INCR + EXPIRE per key |
| Queue | LPUSH + BRPOP (simple job queue) |
| Pub/Sub | Real-time notifications |
| Sorted sets | Leaderboards, priority queues |
