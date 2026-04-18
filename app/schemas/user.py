from pydantic import BaseModel


class UserPublic(BaseModel):
    model_config = {"from_attributes": True}

    id: int
    email: str
    role: str
