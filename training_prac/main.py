
from training_prac.models.database import engine, BaseModel

if __name__ == '__main__':
    BaseModel.metadata.drop_all(engine)
    BaseModel.metadata.create_all(engine)








