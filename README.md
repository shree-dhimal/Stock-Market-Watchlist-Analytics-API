# Distributed Stock Market Watchlist & Analytics API

## Overview

This project is a **production-grade backend system** built with **Django + Django REST Framework** for managing stock watchlists, real-time pricing, analytics, alerts, and third‑party integrations.

The system is designed following **scalable backend architecture principles**, strong **domain modeling**, **security-first authentication**, and **high-performance API patterns**.

---

## Architecture Summary

* **Backend**: Django, Django REST Framework
* **Database**: PostgreSQL
* **Caching / Messaging**: Redis
* **Async Processing**: Celery (or Django-Q) (yet to setup)
* **WebSockets**: Django Channels + Redis
* **Authentication**: JWT, API Keys
* **Deployment**: Docker & Docker Compose (Yet to setup)

### App Separation (Separation of Concerns)

* `user` – User, authentication, roles, API keys
* `stocks` – Stock master data
* `pricing` – Time-series stock prices
* `watchlists` – Watchlists and watchlist items
* `notifications` – Alerts, webhooks, in-app notifications
* `setup` – Base models, permissions, pagination, response handlers

---

## Authentication & Authorization

### Authentication Flow

The system uses **JWT-based authentication** without creating Django server-side sessions.

#### Login API

* **Endpoint**: `POST /api/v1/login/`
* **Input**: `username`, `password`
* **Behavior**:

  * Credentials are validated
  * JWT **access & refresh tokens** are generated
  * Tokens are attached to the **response headers under the `Set-Cookie` key**

> ⚠️ **Important**: Django sessions are **not created**. Tokens are stateless and client-managed.

#### Example Response Headers

```
Set-Cookie: access_token=jwt_token_here; HttpOnly; Secure
Set-Cookie: refresh_token=jwt_token_here; HttpOnly; Secure
```

---

### Supported Authentication Methods

End users and services can authenticate using **any one** of the following:

1. **Cookies (JWT attached)**

   * Browser or client sends back the cookies automatically
2. **Bearer Token (Authorization Header)**

   ```http
   Authorization: Bearer <access_token>
   ```
3. **API Key Authentication (Third‑Party Integrations)**

   ```http
   X-API-KEY: <api_key>
   ```

This hybrid approach allows:

* Secure browser-based auth
* Mobile / frontend SPA support
* External system integrations without JWT lifecycle handling

---

## APIKey Model – Why It Exists

### Purpose

The `APIKey` model is used for **third-party or internal service integrations** where JWT-based user authentication is not suitable.

### Use Cases

* Webhook consumers
* External analytics systems
* Internal microservices

### Benefits

* Stateless authentication
* Easy revocation & rotation
* Scoped permissions per key
* No user login flow required

Each API key:

* Is tied to a user or service account
* Has permission constraints
* Can be rate-limited

---

## WebhookSubscription Model – Why It Exists

### Purpose

The `WebhookSubscription` model enables **event-driven integrations** with external systems.

### Supported Events

* Stock price changes
* Alert triggers (price threshold crossed)

### How It Works

1. User or service registers a webhook endpoint
2. Subscription is stored in `WebhookSubscription`
3. When an event occurs:

   * Background task triggers
   * Payload is sent to subscribed endpoints

### Benefits

* Decoupled architecture
* Near real-time notifications
* No polling required by clients
* Scales independently of core API

---

## Permissions & Access Control

### Role Management

* Uses **Django default Groups & Permissions**
* Roles:

  * Admin
  * Premium User
  * Standard User

### Permission Enforcement

* A custom permission class: `CustomPermission`
* Combines:

  * Django permissions
  * User tier constraints
  * API key scopes

### Adding New Permissions

1. Add permission rules in **permission constraints**
2. Run:

   ```bash
   python manage.py permission_seeder
   ```

This ensures:

* Consistent permission setup across environments
* No manual DB permission handling

---

## Response Handling

### Uniform API Responses

All API responses are handled using a custom:

```
ResponseHandlerMixin
```

### Standard Response Envelope

```json
{
  "data": {},
  "meta": {},
  "errors": []
}
```

### Why This Is Useful

* Predictable API contracts
* Easier frontend integration
* Centralized error formatting
* Cleaner views & serializers

---

## Error Handling & Logging

### Error Logs

* All **server-side errors** are recorded in an `error_logs` table
* Includes:

  * Stack trace
  * Request metadata
  * Correlation ID

### Benefits

* Easier debugging
* Production issue traceability
* Audit-ready error history

---

## Pagination

A **custom pagination class** is used for all paginated endpoints.

### Why Custom Pagination?

* Consistent metadata structure
* Cursor-based pagination for large datasets
* Performance-friendly for time-series data

---

## Caching Strategy

### User-Self API Cache

The `GET /api/v1/self/` endpoint is heavily accessed and includes:

* Roles
* Permissions
* Account tier

This response is cached using **Redis**.

### Benefits

* Reduced database load
* Faster authentication checks
* Improves overall API latency

Cache is automatically invalidated on:

* Role changes
* Permission updates

---

## WebSockets & Real-Time Updates

### Technology

* **Django Channels**
* **Redis** as message broker

### Behavior

* If the application is hosted on an **ASGI-compatible service**:

  * Direct WebSocket communication via Channels
* Otherwise:

  * Messages are published via Redis and consumed asynchronously

### Use Cases

* Live stock price updates
* Real-time alert notifications

---

## Security Considerations

* HttpOnly & Secure cookies
* Token rotation & blacklisting
* API key scope enforcement
* Rate limiting via Redis
* Soft deletion for users

---

## Why This Design Is Useful

* **Scalable**: Stateless auth, async processing, caching
* **Secure**: Multiple auth methods, fine-grained permissions
* **Maintainable**: Centralized responses, permissions, pagination
* **Extensible**: Webhooks, API keys, event-driven architecture
* **Production-ready**: Observability, logging, and performance optimizations

---

---

## Final Notes

This system prioritizes **clean architecture**, **real-world production patterns**, and **developer experience**, making it suitable for both startup-scale and enterprise-scale deployments.
