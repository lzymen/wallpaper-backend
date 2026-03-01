from sqlalchemy.ext.declarative import declarative_base

# 所有 models/*.py 里的模型都要继承这个 Base
Base = declarative_base()