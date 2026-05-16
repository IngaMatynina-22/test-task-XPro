from fastapi import HTTPException, status

class CategoryNotFound(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id {category_id} was not found.",
        )