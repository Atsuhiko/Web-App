import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime
from setting import Base
from setting import ENGINE

class Result(Base):
    """
    ユーザモデル
    """
    __tablename__ = 'results'
    id = Column('id', Integer, primary_key = True, autoincrement=True)
    bad = Column('bad', Float)
    happy = Column('happy', Float)
    filepath = Column('filepath', String(100))

def main(args):
    """
    メイン関数
    """
    Base.metadata.create_all(bind=ENGINE)

if __name__ == "__main__":
    main(sys.argv)