from sqlalchemy.orm import Session

import models, schemas

import logging

log = logging.getLogger("Address_logging")

class AddressRepo:
    
 async def create(db: Session, address: schemas.AddressCreate):
        db_item = models.Address(address=address.address,
                                 city=address.city,
                                 state=address.state,
                                 lat=address.lat,
                                 lon=address.lon)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
 def fetch_by_id(db: Session,_id):
     return db.query(models.Address).filter(models.Address.id == _id).first()
 
 def fetch_by_address(db: Session,address):
     return db.query(models.Address).filter(models.Address.address == address).first()
 
 def fetch_all(db: Session, skip: int = 0, limit: int = 100):
     return db.query(models.Address).offset(skip).limit(limit).all()
 
 async def delete(db: Session,address_id):
     db_item= db.query(models.Address).filter_by(id=address_id).first()
     db.delete(db_item)
     db.commit()
     
     
 async def update(db: Session,address_data):
    updated_item = db.merge(address_data)
    db.commit()
    return updated_item


def validate_address(address: models.Address) -> None:
    # Validate the address
    if not address.address:
        log.error('Address is required')
        return False
    if not address.city:
        log.error('City is required')
        return False
    if not address.state:
        log.error('State is required')
    if not (-90 <= address.lat <= 90):
        log.error('Latitude must be between -90 and 90')
        return False
    if not (-180 <= address.lon <= 180):
        log.error('Latitude must be between -180 and 180')
        return False
    return True