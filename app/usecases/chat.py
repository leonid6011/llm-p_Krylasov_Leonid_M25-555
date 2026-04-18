from app.db.models import ChatMessage
from app.repositories.chat_messages import ChatMessageRepository
from app.services.openrouter_client import OpenRouterClient


class ChatUseCase:
    def __init__(self,
                 chat_repo: ChatMessageRepository,
                 openrouter: OpenRouterClient,
                ) -> None:
        self._chat_repo = chat_repo
        self._openrouter = openrouter

    async def ask(self,
                  user_id: int,
                  prompt: str,
                  system: str | None = None,
                  max_history: int = 10,
                  temperature: float = 0.7,
                  ) -> str:
        messages: list[dict] = []

        if system:
            messages.append({"role": "system", "content": system})

        history = await self._chat_repo.get_last_n(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": prompt})

        await self._chat_repo.add(user_id=user_id, role="user", content=prompt)

        answer = await self._openrouter.chat(
            messages=messages,
            temperature=temperature,
        )

        await self._chat_repo.add(user_id=user_id, role="assistant", content=answer)

        return answer

    async def get_history(self, user_id: int, limit: int = 50) -> list[ChatMessage]:
        return await self._chat_repo.get_all(user_id=user_id, limit=limit)

    async def clear_history(self, user_id: int) -> None:
        await self._chat_repo.delete_all(user_id=user_id)
