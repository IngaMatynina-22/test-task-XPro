from fastapi import HTTPException, status


class ProductNotFound(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} was not found.",
        )


class ProductImageNotFound(HTTPException):
    def __init__(self, product_image_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product image with id {product_image_id} was not found.",
        )


class ProductCategoryNotFound(HTTPException):
    def __init__(self, product_category_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product category with id {product_category_id} was not found.",
        )


class ProductAttributeNotFound(HTTPException):
    def __init__(self, product_attribute_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product attribute with id {product_attribute_id} was not found.",
        )