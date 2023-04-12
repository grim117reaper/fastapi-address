from pydantic import BaseModel


class AddressBase(BaseModel):
    address: str
    city: str
    state: str
    lat : float
    lon : float

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    
    class Config:
        orm_mode=True

class Address(AddressBase):
    id: int

    class Config:
        orm_mode = True