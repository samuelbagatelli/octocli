from pydantic import BaseModel, Field, field_validator


class ModelConfig(BaseModel):
    """Configuration for model generation."""

    tablename: str = Field(..., min_length=1, description="Database table name")
    classname: str = Field(..., min_length=1, description="Python class name")
    is_duplicate: bool = Field(
        default=False,
        description="Whether this is a duplicate table model.",
    )

    @field_validator("tablename")
    def validate_tablename(cls, v: str) -> str:
        """Validate table name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError(
                "Table name must contain only alphanumeric characters and underscores"
            )
        return v

    @field_validator("classname")
    def validate_classname(cls, v: str) -> str:
        """Validate class name format."""
        if not v.isalnum() or not v[0].isupper():
            raise ValueError(
                "Class name must be alphanumeric and start with uppercase letter"
            )
        return v
