---
name: api-architect
description: "API design, REST, GraphQL, gRPC, WebSocket architecture, and API best practices. Use when the user asks about designing APIs, REST conventions, GraphQL schema design, API versioning, authentication, rate limiting, pagination, error handling, OpenAPI/Swagger, or any API architecture question."
metadata:
  version: "1.0.0"
---

# API Architect

Design APIs that developers love. Consistent, predictable, well-documented.

## REST API Conventions

### URL Structure
```
GET    /api/v1/users          → List users
POST   /api/v1/users          → Create user
GET    /api/v1/users/:id      → Get user
PUT    /api/v1/users/:id      → Replace user
PATCH  /api/v1/users/:id      → Update user fields
DELETE /api/v1/users/:id      → Delete user

GET    /api/v1/users/:id/orders    → List user's orders (nested resource)
```

Rules:
- Plural nouns for resources (`/users` not `/user`)
- No verbs in URLs (`POST /users` not `POST /createUser`)
- Kebab-case for multi-word (`/order-items`)
- Nest max 2 levels (`/users/:id/orders` OK, deeper = use query params)

### HTTP Status Codes
| Code | Meaning | Use when |
|---|---|---|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST (return the created resource) |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Validation error, malformed request |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Authenticated but not authorized |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Duplicate, state conflict |
| 422 | Unprocessable | Valid JSON but business logic rejection |
| 429 | Too Many Requests | Rate limited |
| 500 | Internal Error | Unexpected server error |

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable description",
    "details": [
      { "field": "email", "message": "Must be a valid email" }
    ]
  }
}
```

### Pagination
```
GET /api/v1/users?page=2&per_page=20
GET /api/v1/users?cursor=abc123&limit=20  (preferred for large datasets)
```

Response includes:
```json
{
  "data": [...],
  "meta": {
    "total": 150,
    "page": 2,
    "per_page": 20,
    "next_cursor": "def456"
  }
}
```

### Filtering, Sorting, Fields
```
GET /api/v1/users?status=active&role=admin          (filter)
GET /api/v1/users?sort=-created_at,name              (sort, - for desc)
GET /api/v1/users?fields=id,name,email                (sparse fields)
```

## Authentication

| Method | Use case |
|---|---|
| API Key (header) | Server-to-server, simple integrations |
| JWT (Bearer token) | Stateless auth, SPAs, mobile apps |
| OAuth 2.0 | Third-party access, user delegation |
| Session cookies | Traditional web apps (with CSRF protection) |

JWT structure: access token (short-lived, 15-60 min) + refresh token (long-lived, 7-30 days).

## Rate Limiting

Headers to include:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1620000000
Retry-After: 30
```

Strategies: fixed window, sliding window, token bucket. Redis INCR + EXPIRE is simplest.

## GraphQL Schema Design

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  orders(first: Int, after: String): OrderConnection!
}

type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
}

type Query {
  user(id: ID!): User
  users(filter: UserFilter, first: Int, after: String): UserConnection!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
  updateUser(id: ID!, input: UpdateUserInput!): UpdateUserPayload!
}
```

Best practices:
- Use Relay connection spec for pagination
- Input types for mutations (`CreateUserInput`)
- Payload types for mutation responses (include errors)
- N+1: use DataLoader for batching
- Depth limiting and query complexity analysis

## API Versioning

| Strategy | Pros | Cons |
|---|---|---|
| URL path (`/v1/`) | Clear, easy routing | URL pollution |
| Header (`Accept: application/vnd.api.v1+json`) | Clean URLs | Harder to test |
| Query param (`?version=1`) | Simple | Ugly, easy to forget |

Recommendation: URL path for major versions. Additive changes (new fields) don't need a version bump.

## OpenAPI / Swagger

Always document APIs with OpenAPI 3.x:
- Every endpoint, method, parameter
- Request/response schemas with examples
- Authentication requirements
- Error responses
- Generate from code (preferred) or write spec first

## WebSocket API Design

```json
// Client → Server
{ "type": "subscribe", "channel": "orders", "filters": { "user_id": "123" } }
{ "type": "unsubscribe", "channel": "orders" }
{ "type": "ping" }

// Server → Client
{ "type": "event", "channel": "orders", "data": { ... } }
{ "type": "error", "code": "AUTH_REQUIRED", "message": "..." }
{ "type": "pong" }
```

Always implement: heartbeat/ping-pong, reconnection with backoff, message acknowledgment for critical events.
