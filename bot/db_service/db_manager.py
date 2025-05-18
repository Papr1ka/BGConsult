import asyncpg
from typing import Optional, List, Dict, Any

class DatabaseManager:
    def __init__(self):
        self.pool = None

    async def _ensure_connected(self):
        """Внутренний метод для проверки подключения"""
        if self.pool is None:
            await self.connect()

    async def connect(self, **kwargs):
        """Подключение к БД"""
        self.pool = await asyncpg.create_pool(
            host=kwargs.get('host', 'postgres'),
            port=kwargs.get('port', 5432),
            user=kwargs.get('user', 'admin'),
            password=kwargs.get('password', '12345'),
            database=kwargs.get('database', 'db')
        )

    async def close(self):
        """Закрытие соединения"""
        if self.pool:
            await self.pool.close()
            self.pool = None


    # === Методы для работы с диалогами ===
    async def start_dialog(self, user_id: int, user_name: str) -> int:
        """Создает новый диалог и возвращает его ID"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            dialog_id = await conn.fetchval(
                """
                INSERT INTO dialogs (user_id, user_name, status)
                VALUES ($1, $2, 'active')
                RETURNING dialog_id
                """,
                user_id, user_name
            )
            return dialog_id

    async def end_dialog(self, dialog_id: int):
        """Завершает диалог"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE dialogs
                SET ended_at = NOW(), status = 'closed'
                WHERE dialog_id = $1
                """,
                dialog_id
            )

    # === Методы для работы с сообщениями ===
    async def add_message(self, dialog_id: int, text: str, is_from_user: bool):
        """Добавляет сообщение в диалог"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO messages (dialog_id, text, is_from_user)
                VALUES ($1, $2, $3)
                """,
                dialog_id, text, is_from_user
            )

    async def get_dialog_messages(self, dialog_id: int) -> List[Dict[str, Any]]:
        """Возвращает все сообщения диалога"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT message_id, text, is_from_user, sent_at
                FROM messages
                WHERE dialog_id = $1
                ORDER BY sent_at
                """,
                dialog_id
            )

    # === Методы для работы с оценками ===
    async def add_rating(self, dialog_id: int, score: int, feedback: str = None):
        """Добавляет оценку диалогу"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO ratings (dialog_id, score, feedback)
                VALUES ($1, $2, $3)
                """,
                dialog_id, score, feedback
            )

    async def get_user_dialogs(self, user_id: int) -> List[Dict[str, Any]]:
        """Возвращает все диалоги пользователя"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                """
                SELECT dialog_id, started_at, ended_at, status
                FROM dialogs
                WHERE user_id = $1
                ORDER BY started_at DESC
                """,
                user_id
            )
        
    async def get_active_dialog_by_username(self, username: str) -> Optional[int]:
        """Возвращает ID активного диалога по имени пользователя или None, если нет активных"""
        await self._ensure_connected()
        async with self.pool.acquire() as conn:
            return await conn.fetchval(
                """
                SELECT dialog_id 
                FROM dialogs 
                WHERE user_name = $1 AND status = 'active'
                ORDER BY started_at DESC
                LIMIT 1
                """,
                username
            )
        
db = DatabaseManager()