from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

import models, schemas
from database import get_db, engine

from helpers import AddressRepo,validate_address

import uvicorn

from typing import List,Optional
from geopy.distance import geodesic

from log_config import init_loggers

init_loggers()


app = FastAPI(title="Address storing application",
    version="0.1.0",)

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/address', tags=["Address"],response_model=schemas.Address,status_code=201)
async def create_address(address_request: schemas.AddressCreate, db: Session = Depends(get_db)):
    """
    Create an Address and store it in the database
    """
    
    db_item = AddressRepo.fetch_by_address(db, address=address_request.address)
    if db_item:
        raise HTTPException(status_code=400, detail="Address already exists!")

    return await AddressRepo.create(db=db, address=address_request)

@app.get('/address', tags=["Address"])
def get_all_address(distance: Optional[float] = None,lat: Optional[float] = None,lon: Optional[float] = None,db: Session = Depends(get_db)):
    """
    Get all the Address stored in database \n
    If distance is provided then lat and lon needs to be present
    """
    if distance:
        if not lat and not lon:
            raise HTTPException(status_code=400, detail="lon and lat needs to be present if distance is given.")
        db_item = AddressRepo.fetch_all(db)
        if db_item == None :
            raise HTTPException(status_code=404, detail="No Address present in database")
        filtered_addresses = []
        for address in db_item:
            if geodesic((lat, lon), (address.lat, address.lon)).miles <= distance:
                filtered_addresses.append(address)
        if len(filtered_addresses) > 0:
            return filtered_addresses
        else:
            raise HTTPException(status_code=404, detail="No Address present in database falls within the parameters passed")
    else:
        return AddressRepo.fetch_all(db)


@app.get('/address/{address_id}', tags=["Address"],response_model=schemas.Address)
def get_address(address_id: int,db: Session = Depends(get_db)):
    """
    Get the Address with the given ID provided by User stored in database
    """
    db_item = AddressRepo.fetch_by_id(db,address_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Address not found with the given ID")
    return db_item

@app.delete('/address/{address_id}', tags=["Address"])
async def delete_address(address_id: int,db: Session = Depends(get_db)):
    """
    Delete the Address with the given ID provided by User stored in database
    """
    db_item = AddressRepo.fetch_by_id(db,address_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await AddressRepo.delete(db,address_id)
    return "Item deleted successfully!"

@app.put('/address/{address_id}', tags=["Address"],response_model=schemas.AddressUpdate)
async def update_address(address_id: int,address_request: schemas.AddressUpdate, db: Session = Depends(get_db)):
    """
    Update an Address stored in the database
    """
    db_item = AddressRepo.fetch_by_id(db, address_id)
    if db_item:
        update_item_encoded = jsonable_encoder(address_request)
        db_item.address = update_item_encoded['address']
        db_item.state = update_item_encoded['state']
        db_item.city = update_item_encoded['city']
        db_item.lat = update_item_encoded['lat'] 
        db_item.lon = update_item_encoded['lon']
        if not validate_address(db_item):
            raise HTTPException(status_code=400, detail="Validations failed.")
        return await AddressRepo.update(db=db, address_data=db_item)
    else:
        raise HTTPException(status_code=404, detail="Address not found with the given ID")
    

if __name__ == "__main__":
    uvicorn.run("main:app",host="0.0.0.0", port=9000, reload=True)