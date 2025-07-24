from fastmcp.server.middleware import Middleware, MiddlewareContext
import os


class AuthMiddleware(Middleware):
    """Middleware that checks for Bearer token authentication."""

    async def on_message(self, context: MiddlewareContext, call_next):
        auth_header = context.fastmcp_context.get_http_request().headers.get(
            "Authorization"
        )
        secret = os.environ.get("SECRET")
        if not auth_header or not auth_header.startswith("Bearer "):
            return {"error": "Missing or invalid Authorization header"}, 401
        token = auth_header.split("Bearer ")[-1]
        if token != secret:
            return {"error": "Invalid token"}, 403
        return await call_next(context)
