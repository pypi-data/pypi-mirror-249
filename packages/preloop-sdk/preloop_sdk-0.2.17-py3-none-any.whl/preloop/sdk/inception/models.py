from enum import Enum

from pydantic import BaseModel, Field


class DataSourceType(str, Enum):
    """
    Enum restricting the datasources that are used by Preloop
    """

    POSTGRES = "postgres"


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
    datasource_type: DataSourceType
    connection_params: ConnectionParamsSQL
    auth_params: AuthParamsSQL


class PostgresDatasource(Datasource):
    datasource_type: DataSourceType = DataSourceType.POSTGRES
    connection_params: ConnectionParamsPostgres
    auth_params: AuthParamsPostgres
