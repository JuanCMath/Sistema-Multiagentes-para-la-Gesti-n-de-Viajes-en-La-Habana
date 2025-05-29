from sqlalchemy import create_engine, Column, Integer, String, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
engine = create_engine("sqlite:///src/database/viajes.db")
Session = sessionmaker(bind=engine)

def init_db():
    inspector = inspect(engine)
    tablas_esperadas = {"viajes"}
    tablas_existentes = set(inspector.get_table_names())
    if not tablas_esperadas.issubset(tablas_existentes):
        print("Inicializando base de datos...")
        Base.metadata.create_all(engine)
    else:
        print("Base de datos ya inicializada.")

class Viaje(Base):
    __tablename__ = "viajes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    destino = Column(String, nullable=False)
    fecha = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)

init_db()