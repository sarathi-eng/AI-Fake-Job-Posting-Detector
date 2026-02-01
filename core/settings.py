"""Runtime settings (12-factor) for the FastAPI service.

These settings are intentionally small and environment-driven so the API can be
run locally, in Docker, or on any host without code changes.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "dev"  # dev | prod

    # Comma-separated list. Example:
    #   http://localhost:3000,https://your-domain.com
    cors_allow_origins: str = "*"

    # This API doesn't use cookies/sessions by default, so keep this false.
    # Note: browsers forbid using '*' with credentials.
    cors_allow_credentials: bool = False
    # Comma-separated list or '*'
    cors_allow_methods: str = "*"
    # Comma-separated list or '*'
    cors_allow_headers: str = "*"

    def cors_origins_list(self) -> list[str]:
        if self.app_env.lower() == "dev" and self.cors_allow_origins.strip() == "*":
            return ["*"]

        origins = [o.strip() for o in self.cors_allow_origins.split(",")]
        return [o for o in origins if o]

    def cors_methods_list(self) -> list[str]:
        methods = self.cors_allow_methods.strip()
        if methods == "*":
            return ["*"]
        return [m.strip().upper() for m in methods.split(",") if m.strip()]

    def cors_headers_list(self) -> list[str]:
        headers = self.cors_allow_headers.strip()
        if headers == "*":
            return ["*"]
        return [h.strip() for h in headers.split(",") if h.strip()]


settings = Settings()
