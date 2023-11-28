from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

users = Table("users", meta_data, 
              Column("id", Integer, primary_key=True),
              Column("name", String(255), nullable=False),
              Column("username", String(255), nullable=False),
              Column("user_passw", String(255), nullable=False))

meta_data.create_all(engine)