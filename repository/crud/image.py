from model.image import Image
from repository.base import crud


class ImageRepository(crud.CRUDRepository):
    def __init__(self):
        super().__init__(Image)
