from sqlalchemy import Column, Integer, String, Float

from database import Base
    
class Address(Base):
    __tablename__ = "address"
    
    id = Column(Integer, primary_key=True,index=True)
    city = Column(String(80), nullable=False,index=True)
    state = Column(String(80), nullable=False,index=True)
    lat = Column(Float(precision=2), nullable=False)
    lon = Column(Float(precision=2), nullable=False)
    address = Column(String(200), nullable=False, unique=True)
    def __repr__(self):
        return 'ItemModel(id=%s, city=%s, state=%s, longitute=%s, latitude=%s, address=%s, )' % (self.id, self.city, self.state, self.lat, self.lon, self.address)