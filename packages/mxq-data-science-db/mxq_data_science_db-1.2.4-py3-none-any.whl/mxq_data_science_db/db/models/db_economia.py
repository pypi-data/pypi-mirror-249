"""SQL models for db_economia
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, TIMESTAMP, Integer, ForeignKey, Float, Date

from mxq_data_science_db.db.models.base import BaseModel


Base = declarative_base()
metadata = Base.metadata


class Agregado(Base, BaseModel):
    """Dimension table with metada dados from IBGE agregados"""

    __tablename__ = "ibge_agregado"

    id = Column(Integer, primary_key=True)
    nome = Column(String(200), nullable=False)
    url = Column(String(100), nullable=False)
    periodicidade = Column(String(50), nullable=False)
    inicio = Column(Integer, nullable=False)
    fim = Column(Integer, nullable=False)


class DadosIBGE(Base, BaseModel):
    """Nova tabela com os dados dos indicadores do IBGE"""

    __tablename__ = "ibge_dados"
    agregado = Column(Integer, ForeignKey("ibge_agregado.id"), primary_key=True)
    variavel = Column(String(200), primary_key=True)
    categoria = Column(String(100), primary_key=True)
    classificacao = Column(String(100), primary_key=True)
    localidade = Column(String(50), primary_key=True)
    data = Column(TIMESTAMP, primary_key=True)
    unidade = Column(String(50), primary_key=True)
    valor = Column(Float)


class Cambio(Base, BaseModel):
    """Tabela com cambio"""

    __tablename__ = "cambio"
    data = Column(Date, nullable=False, primary_key=True)
    base = Column(String(3), nullable=False, primary_key=True)
    moeda = Column(String(3), nullable=False, primary_key=True)
    valor = Column(Float)
