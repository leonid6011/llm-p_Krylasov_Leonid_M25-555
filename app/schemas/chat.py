from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str
    system: str | None = None
    max_history: int = Field(default=10, ge=0, le=100)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    answer: str


class ChatMessagePublic(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    role: str
    content: str
    created_at: str

    @classmethod
    def from_orm_model(cls, msg) -> "ChatMessagePublic":
        return cls(
            id=msg.id,
            role=msg.role,
            content=msg.content,
            created_at=str(msg.created_at),
        )


class ChatHistoryResponse(BaseModel):
    items: list[ChatMessagePublic]
