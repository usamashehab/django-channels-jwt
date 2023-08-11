# Django Channels JWT 

Django Channels JWT Middleware is a secure way to handle authentication for Django Channels WebSocket connections without directly exposing JWT tokens. Instead of sending the token itself in the query parameter, this middleware uses UUID-based authentication and cache-based user retrieval for enhanced security.

## Security Benefits

- **Enhanced Security**: JWT tokens can potentially be intercepted if sent as query parameters. This middleware avoids sending tokens directly, minimizing the risk of token leakage.

- **UUID-based Authentication**: This middleware generates UUIDs as tokens for WebSocket connections. These UUIDs are short-lived and act as temporary access keys. When a user connects, they provide the UUID, which is used to retrieve the authenticated user.

- **Cache-based User Retrieval**: Upon connection, the middleware validates the UUID, retrieves the corresponding user ID from the cache, and fetches the user asynchronously. This ensures that the WebSocket connection is only established for authenticated users.

## Risks of Sending Tokens as Query Parameters

Sending tokens as query parameters can expose security vulnerabilities:
- **Token Exposure**: Tokens in query parameters can be captured in logs, browser history, or server logs, increasing the risk of unauthorized access.
- **Caching**: Some proxies or servers may cache URLs, which could lead to tokens being stored in shared caches.

## Installation

Install the package using pip:

```bash
pip install django-channels-jwt
```

## Configuration

1. Wrap your URLRouter
   ```python
   from django_channels_jwt.middlware import JwtAuthMiddlewareStack

   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": JwtAuthMiddlewareStack(
           URLRouter(
               websocket_urlpatterns,
           )
       ),
   })
   ```

2. Include the provided URL for ticket generation in your project's `urls.py`:

  ```python
   from django.urls import path, include

   url_patterns = [
       # ... your other URL patterns
       path("api/auth/", include('django_channels_jwt.urls')
   ]
   ```
or if you want to set customized route

   ```python
   from django.urls import path, include
   from django_channels_jwt.views import AsgiValidateTokenView

   url_patterns = [
       # ... your other URL patterns
       path("auth_for_ws_connection/", AsgiValidateTokenView.as_view())
   ]
   ```

## Usage

1. Ensure your Django app's models are configured correctly.
2. Use the included `AsgiValidateTokenView` to generate a ticket (UUID) for WebSocket connections.
3. Connect to your WebSocket with the generated UUID to authenticate the connection without exposing the token.
 ```
 ws://localhost:8001/ws/chat/?uuid=
 ```
