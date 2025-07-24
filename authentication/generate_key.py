from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.auth.providers.bearer import RSAKeyPair
from dotenv import load_dotenv
import os

_ = load_dotenv()

try:
    # Generate a new key pair
    key_pair = RSAKeyPair.generate()
    
    try:
        with open("authentication/public.pem", "wb") as f:
            f.write(key_pair.public_key.encode("utf-8"))
    except IOError as e:
        print(f"Error writing public key to file: {e}")
        raise

    # Configure the auth provider with the public key
    auth = BearerAuthProvider(
        public_key=key_pair.public_key,
        issuer=os.getenv("AUTH_ISSUER"),
        audience=os.getenv("AUTH_AUDIENCE"),
    )

    # Generate a token for testing
    try:
        token = key_pair.create_token(
            subject="dev-user",
            issuer="https://dev.example.com",
            audience="my-dev-server",
            scopes=["read", "write"],
            expires_in_seconds=60*60*24  # 1 day
        )
    except Exception as e:
        print(f"Error generating token: {e}")
        raise

    print("--------------------------------------------------")
    print("Token Generation for Development Environment 🔐")
    print("--------------------------------------------------")
    print(f"⚠️  Keep this token secure and use it in your development environment.")
    print("IMPORTANT : The token will be generated only once and will not be stored.")
    print(f"\n\n✅ Test token for MCP:\n\n{token}")
    print("\n\n✅ RSA public key pair saved to 'authentication/public.pem'")

except Exception as e:
    print(f"An error occurred during the authentication setup: {e}")