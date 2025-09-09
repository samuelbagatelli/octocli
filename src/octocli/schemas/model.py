from pydantic import BaseModel


class ModelConfig(BaseModel):
    tablename: str
    classname: str
    is_duplicate: bool = False
