from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Configuration settings for the MCP server.
    """
    # MCP / API
    mcp_version: str = Field("0.4.0-beta", description="Version of the MCP server")
    server_version: str = Field("1.0.0", description="API version reported in /info endpoint")
    server_port: int = Field(8000, description="Port for the HTTP server")
    mcp_server_name: str = Field("ACL Analytics Helper MCP", description='Name of the server passed to the LLM')

    # ACL Scraper
    acl_version: str = Field("19", description="Version of ACL Analytics to target")

    # Database
    db_path: str = Field("./db/auth.db", description="Path to the SQLite auth database")
    db_script_path: str = Field("db/scripts/recreate_db.sql", description="Path to the DB schema SQL script")
    db_mock_data_path: str = Field("db/scripts/mock_data.sql", description="Path to the mock data SQL script")
    token_default_days: int = Field(30, description="Default token expiration in days")

    # Cache
    cache_ttl: int = Field(86400, description="Cache TTL in seconds (24h default)")
    cache_folder: str = Field("cache/", description="Folder path for cache files")

    # Auth
    timezone_utc_offset: int = Field(-3, description="UTC offset for token validation timezone (BRT = -3)")
    datetime_format: str = Field("%Y-%m-%d %H:%M:%S", description="Datetime format for storing/parsing timestamps")
    free_routes: list[str] = Field(default_factory=lambda: ["/info"], description="Routes that bypass authentication")

    # CORS
    allowed_origins: list[str] = Field(default_factory=list, description="List of allowed origins for CORS")
    session_timeout: int = Field(3600, description="Session timeout duration in seconds")


settings = Settings()
