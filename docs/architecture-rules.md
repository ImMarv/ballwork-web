Core rules for the modulith system.
---
1. Modules shall not import from each other.
2. The API layer shall not contain any business logic.
3. Services shall not know about FastAPI.
4. Repositories shall be the only DB access per module.
5. Shared is read only.