"""SQL models for db_commodity
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float, Date

from mxq_data_science_db.db.models.base import BaseModel


Base = declarative_base()
metadata = Base.metadata

class ANPProcessamentoPetroleo(Base, BaseModel):
    """Table with ANP processamento de petroleo data"""

    __tablename__ = "anp_processamento_petroleo"
    data = Column(Date, primary_key=True)
    uf = Column(String(2), primary_key=True)
    refinaria = Column(String(50), primary_key=True)
    materia_prima = Column(String(30), primary_key=True)
    unidade = Column(String(10), primary_key=True)
    qtd = Column(Float)

class ANPProducao(Base, BaseModel):
    """Table with ANP producao de petroleo, gn"""

    __tablename__ = "anp_producao_petroleo_gn"
    data = Column(Date, primary_key=True)
    uf = Column(String(2), primary_key=True)
    grande_regiao = Column(String(50), primary_key=True)
    localizacao = Column(String(50), primary_key=True)
    produto = Column(String(30), primary_key=True)
    unidade = Column(String(10), primary_key=True)
    qtd = Column(Float)

class ANPProducaoDerivados(Base, BaseModel):
    """Table with ANP producao de derivados data"""

    __tablename__ = "anp_producao_derivados"
    data = Column(Date, primary_key=True)
    uf = Column(String(2), primary_key=True)
    refinaria = Column(String(50), primary_key=True)
    produto = Column(String(30), primary_key=True)
    unidade = Column(String(10), primary_key=True)
    qtd = Column(Float)

class ANPVendaDerivados(Base, BaseModel):
    """Table with ANP venda de derivados data"""

    __tablename__ = "anp_venda_derivados"
    data = Column(Date, primary_key=True)
    uf = Column(String(2), primary_key=True)
    grande_regiao = Column(String(50), primary_key=True)
    produto = Column(String(30), primary_key=True)
    unidade = Column(String(10), primary_key=True)
    qtd = Column(Float)