# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from email.policy import default
from apps import db
from sqlalchemy.exc import SQLAlchemyError
from apps.exceptions.exception import InvalidUsage
import datetime as dt
from sqlalchemy.orm import relationship
from enum import Enum

class CURRENCY_TYPE(Enum):
    usd = 'usd'
    eur = 'eur'

class Product(db.Model):

    __tablename__ = 'products'

    id            = db.Column(db.Integer,      primary_key=True)
    name          = db.Column(db.String(128),  nullable=False)
    info          = db.Column(db.Text,         nullable=True)
    price         = db.Column(db.Integer,      nullable=False)
    currency      = db.Column(db.Enum(CURRENCY_TYPE), default=CURRENCY_TYPE.usd, nullable=False)

    date_created  = db.Column(db.DateTime,     default=dt.datetime.utcnow())
    date_modified = db.Column(db.DateTime,     default=db.func.current_timestamp(),
                                               onupdate=db.func.current_timestamp())
    
    def __init__(self, **kwargs):
        super(Product, self).__init__(**kwargs)

    def __repr__(self):
        return f"{self.name} / ${self.price}"

    @classmethod
    def find_by_id(cls, _id: int) -> "Product":
        return cls.query.filter_by(id=_id).first() 

    def save(self) -> None:
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)

    def delete(self) -> None:
        try:
            db.session.delete(self)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            db.session.close()
            error = str(e.__dict__['orig'])
            raise InvalidUsage(error, 422)
        return


#__MODELS__
class Vehicle(db.Model):

    __tablename__ = 'Vehicle'

    id = db.Column(db.Integer, primary_key=True)

    #__Vehicle_FIELDS__
    numberplate = db.Column(db.Text, nullable=True)
    bodytype = db.Column(db.String(255),  nullable=True)
    driver = db.Column(db.String(255),  nullable=True)
    model = db.Column(db.String(255),  nullable=True)
    year = db.Column(db.String(255),  nullable=True)

    #__Vehicle_FIELDS__END

    def __init__(self, **kwargs):
        super(Vehicle, self).__init__(**kwargs)


class Driver(db.Model):

    __tablename__ = 'Driver'

    id = db.Column(db.Integer, primary_key=True)

    #__Driver_FIELDS__
    driver_id = db.Column(db.Integer, nullable=True)
    first_name = db.Column(db.Text, nullable=True)
    last_name = db.Column(db.Text, nullable=True)
    license_number = db.Column(db.Text, nullable=True)
    phone_number = db.Column(db.Integer, nullable=True)

    #__Driver_FIELDS__END

    def __init__(self, **kwargs):
        super(Driver, self).__init__(**kwargs)


class Company(db.Model):

    __tablename__ = 'Company'

    id = db.Column(db.Integer, primary_key=True)

    #__Company_FIELDS__
    contact_email = db.Column(db.Text, nullable=True)

    #__Company_FIELDS__END

    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)



#__MODELS__END
