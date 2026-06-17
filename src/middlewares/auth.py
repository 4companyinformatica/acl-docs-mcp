from dbm import sqlite3
import json
from starlette.datastructures import Headers
import aiosqlite
from datetime import datetime, timezone, timedelta
from util.exceptions import *
from settings import settings


class ASGIAuth:
    def __init__(self, app):
        self.app = app

    # TODO: Checar se o lifespan do mcp entra aqui
    async def __call__(self, scope, receive, send):
        # 1. Ignorar tudo que não for requisição HTTP (ex: WebSockets ou Lifespan)
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 2. Rotas públicas liberadas
        if scope["path"] in settings.free_routes:
            await self.app(scope, receive, send)
            return

        # 3. Ler os cabeçalhos usando o helper do Starlette para facilitar
        headers = Headers(scope=scope)
        auth_header = headers.get("authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            await self.middleware_message(
                send, 401, "Token ausente ou malformado. Use 'Bearer <token>'"
            )
            return

        token = auth_header.split(" ")[1]

        # 4. Validar o token
        try:
            is_valid, user_info = await self.verify_token(token)
        except TokenExpiredError:
            await self.middleware_message(send, 401, "Token expirado")
            return

        except sqlite3.DatabaseError as e:
            print(f"[ASGIAuth] DB error: {e}")
            await self.middleware_message(send, 500, "Erro interno do servidor")
            return

        except Exception as e:
            print(f"[ASGIAuth] DB error: {e}")
            await self.middleware_message(send, 500, "Erro interno do servidor")
            return

        if not is_valid:
            await self.middleware_message(send, 401, "Token inválido ou expirado")
            return

        # 5. Injetar o usuário no estado (escopo) da requisição
        # No ASGI, o 'state' do Starlette fica dentro de scope["state"]
        if "state" not in scope:
            scope["state"] = {}
        scope["state"]["user"] = user_info

        # Tudo certo! Passa o controle para o próximo middleware ou app
        await self.app(scope, receive, send)


    # Envia os cabeçalhos da resposta (HTTP 401)
    async def middleware_message(self, send, status_code: int, message: str):
        """Função auxiliar para responder em formato JSON usando o protocolo ASGI"""
        response_body = json.dumps({"error": message}).encode("utf-8")
        await send({"type": "http.response.start", "status": status_code, "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", str(len(response_body)).encode("ascii")),
        ]})
        await send({"type": "http.response.body", "body": response_body})

    async def verify_token(self, token: str) -> tuple[bool, dict | None]:
        db_command = """
        -- Recupera informações relacionadas ao token, se válido
        SELECT user_auth.user_id, user_auth.created_at, user_auth.days_to_expire, user_info.user_name, user_info.user_role
        FROM user_auth
        JOIN user_info ON user_auth.user_id = user_info.user_id
        WHERE user_auth.token = ?
        """

        db_command2 = """
        -- Atualiza a data de último uso do token (opcional, mas útil para monitoramento)
        UPDATE user_auth SET last_used_at = ? WHERE token = ?
        """

        async with aiosqlite.connect(settings.db_path) as db:
            async with db.execute(db_command, (token,)) as cursor:
                result = await cursor.fetchone()
                # retorna tipo: (2, '2026-06-05 20:07:39', 30, 'Bob', 'supervisor')

                if result:
                    # Verificar expiração do token
                    BRT = timezone(timedelta(hours=settings.timezone_utc_offset))
                    rightnow = datetime.now(tz=BRT)
                    created_at = datetime.strptime(result[1], settings.datetime_format).replace(tzinfo=BRT)

                    if result[2] is not None:
                        expire_at = created_at + timedelta(days=result[2])
                        if rightnow > expire_at:
                            raise TokenExpiredError("Token expirado")

                    # Atualizar a data de último uso do token
                    await db.execute(db_command2, (rightnow.strftime(settings.datetime_format), token))
                    await db.commit()

                    return True, {
                        "user_id": result[0],
                        "created_at": result[1],
                        "days_to_expire": result[2],
                        "user_name": result[3],
                        "user_role": result[4]
                    }

        return False, None
