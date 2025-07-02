from pydantic import BaseModel

class LogCreate(BaseModel):
    data: str

    class Config:
        from_attributes = True
