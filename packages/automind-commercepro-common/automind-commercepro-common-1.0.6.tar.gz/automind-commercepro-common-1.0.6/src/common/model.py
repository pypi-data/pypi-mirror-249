from pydantic import BaseModel


class Model(BaseModel):
    def model_dto(self) -> dict:
        """Returns a database compatible representation of this object."""
        dto = self.model_dump(exclude_none=True)
        return dto
