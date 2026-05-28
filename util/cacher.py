import hashlib
from typing import Optional, Any
import pathlib
import json
from datetime import datetime, timezone


"""
Estrutura do cache:

{
    "data": {},
    "created_at": "2024-06-01T12:00:00Z",
}
"""
class Cacher:
    def __init__(self, ttl: Optional[int] = None) -> None:
        self.cache_folder = pathlib.Path("cache/")
        self.cache_folder.mkdir(parents=True, exist_ok=True)
        self.ttl = ttl

    def _cache_hash(
            self, 
            **kwargs # Deus proiba um homem usar kwargs...
        ) -> str:
        
        raw = json.dumps(kwargs, sort_keys=True)

        return hashlib.md5(raw.encode()).hexdigest()

    def _cache_file(self, hash: str) -> pathlib.Path:
        return self.cache_folder / f"{hash}"
    
    def get(self, **kwargs) -> Optional[Any]:
        path = self._cache_file(self._cache_hash(**kwargs))
        if not path.exists():
            return None

        entry = json.loads(path.read_text())

        if self.ttl:
            created = datetime.fromisoformat(entry["created_at"])
            age = (datetime.now(timezone.utc) - created).total_seconds()
            if age > self.ttl:
                path.unlink()
                return None

        return entry["data"]

    def set(self, data: Any, **kwargs) -> None:
        entry = {
            "data": data,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        path = self._cache_file(self._cache_hash(**kwargs))
        path.write_text(json.dumps(entry, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    cache = Cacher(ttl=60)
    cache.set(data={"foo": "bar"}, url="https://example.com", key="test")
    test = cache.get(url="https://example.com", key="test")
    print(test)