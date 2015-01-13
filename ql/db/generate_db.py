from ql.db import Base
from ql.db import sql_api

engine = sql_api.get_engine()
Base.metadata.create_all(engine)
