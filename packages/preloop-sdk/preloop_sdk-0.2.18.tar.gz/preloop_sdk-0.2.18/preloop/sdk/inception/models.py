from enum import Enum

from pydantic import BaseModel, Field


class ConnectionParamsSQL(BaseModel):
    user_name: str
    host_name: str
    port_number: int
    database_name: str
    table_name: str
    schema_name: str | None = None


class ConnectionParamsPostgres(ConnectionParamsSQL):
    pass


class AuthParamsSQL(BaseModel):
    password: str


class AuthParamsPostgres(AuthParamsSQL):
    pass


class Datasource(BaseModel):
    datasource_name: str
    datasource_description: str = Field(
        title="The description of the datasource", max_length=400, default="Description of this datasource."
    )
    connection_params: ConnectionParamsSQL
    auth_params: AuthParamsSQL


class PostgresDatasource(Datasource):
    connection_params: ConnectionParamsPostgres
    auth_params: AuthParamsPostgres
