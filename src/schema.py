from pydantic import BaseModel, Field


class InferenceInput(BaseModel):
    """
    Parses and validates input for inference endpoint.
    """

    # pylint: disable=too-few-public-methods

    num_of_bed: int = Field(..., example=2, title="Number of beds in the house")
    num_of_bath: int = Field(..., example=3, title="Number of bathrooms in the house")
    acre_lot: float = Field(..., example=0.12, title="Land size of the house compound")
    zip_code: int = Field(..., example=795, title="Zip code of house area")
    house_size: float = Field(..., example=2520.0, title="House size")
    state: str = Field(..., example="Puerto Rico", title="House location(State)")
    city: str = Field(..., example="Adjuntas", title="House location(City)")


class InferenceOutput(BaseModel):
    """
    Parses and validates output of inference endpoint.
    """

    # pylint: disable=too-few-public-methods
    price: float = Field(..., example=50000.456, title="Price in USD")

    class Config:
        orm_mode = True
