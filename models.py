from sqlalchemy import Column, Integer, String, Text, DateTime
from app import db


class Comments(db.Model):
    """ Model for the table 'comment' """
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    username = Column(String(150), nullable=False)
    time = Column(DateTime, index=True)
    text = Column(Text)
    filename = Column(Text)
    label = Column(String(20), index=True)

