from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.auth import BearerAuthProvider


with open("authentication/public.pem", "r") as f:
    public_key_pem = f.read().encode("utf-8")


auth_provider = BearerAuthProvider(public_key=public_key_pem)
