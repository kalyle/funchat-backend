from sqlalchemy import or_, Column, Integer, BigInteger

from . import db
from sqlalchemy.orm import Session, Query
from flask_sqlalchemy.model import Model


class BaseModel(db.Model):
    __abstract__ = True
    query: Query

    id = Column(Integer, primary_key=True, autoincrement=True)
    create_time = Column(BigInteger)
    update_time = Column(BigInteger)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=int(id)).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_limit(cls, find_data: dict, many=True):
        data = cls.get_limits(cls, find_data)
        return (
            cls.query.filter_by(**data).all()
            if many
            else cls.query.filter_by(**data).first()
        )

    @classmethod
    def find_by_or_limit(cls, find_data):
        data = cls.get_limits(cls, find_data)
        return cls.query.filter_by(or_(**data)).all()

    @classmethod
    def update_to_db(cls, id, update_data: dict):
        session: Session = db.session
        data = cls.get_limits(cls, update_data)

        try:
            cls.query.filter_by(id=id).update(data)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

    @classmethod
    def update_by_limit(cls, id, update_data: dict):
        session: Session = db.session
        data = cls.get_limits(cls, update_data)

        try:
            cls.query.filter_by(id=id).update(data)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            return False

    def save_to_db(self) -> int:
        session: Session = db.session
        session.add(self)
        try:
            session.commit()
            return self.id
        except Exception as e:
            # logger
            session.rollback()

    def delete_from_db(self) -> None:
        session: Session = db.session
        session.delete(self)
        try:
            session.commit()
        except:
            session.rollback()

    @staticmethod
    def get_limits(cls: Model, data: dict):
        model_columns = set(column.name for column in cls.__table__.columns)
        return {k: v for k, v in data.items() if k in model_columns}

    @classmethod
    def paginate_by_query(cls, query_dict: dict):
        cls.query.filter()
