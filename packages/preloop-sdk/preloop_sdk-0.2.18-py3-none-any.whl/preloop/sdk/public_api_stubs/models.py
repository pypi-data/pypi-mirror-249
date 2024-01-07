import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# Datasource models
class DatasourceType(str, Enum):
    """
    Enum restricting the datasources that are used by Preloop. Please
    expand this enum as we add in more data sources.
    """

    POSTGRES = "postgres"
    MYSQL = "mysql"
    S3 = "s3"


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


class ListDatasourcesRequest(BaseModel):
    datasource_id: uuid.UUID


class ListDatasourcesResult(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    datasource_name: str
    datasource_description: Optional[str] = None
    connection_params: ConnectionParamsSQL
    auth_params: AuthParamsSQL
    datasource_type: DatasourceType
    schema_and_types: Dict
    creation_date: datetime
    last_updated: datetime | None


class _ListDatasourcesResultArray(BaseModel):
    array_list: List[ListDatasourcesResult]


class DeleteDatasourceRequest(BaseModel):
    datasource_id: uuid.UUID


class DeleteDatasourceResult(BaseModel):
    detail: str


class DatasourceIdentifierField(BaseModel):
    datasource_id: uuid.UUID


class ModifiableDatasourceFields(BaseModel):
    datasource_name: Optional[str] = None
    datasource_description: Optional[str] = None
    connection_params: Optional[ConnectionParamsSQL] = None
    auth_params: Optional[AuthParamsSQL] = None


class ModifyDatasourceRequest(BaseModel):
    fields: DatasourceIdentifierField
    modfield: ModifiableDatasourceFields


class ModifyDatasourceResult(BaseModel):
    detail: str


class GetDatasourceRequest(BaseModel):
    datasource_id: uuid.UUID
    filter_expression: str


# Feature models
class ListFeaturesRequest(BaseModel):
    feature_id: uuid.UUID


class ListFeaturesResult(BaseModel):
    message: str
    details: List[Dict[str, Any]] | None


class DeleteFeatureRequest(BaseModel):
    feature_id: uuid.UUID


class DeleteFeatureResult(BaseModel):
    message: str
    details: Dict[str, Any] | List[Dict[str, Any]] | None


class FeatureIdentifierField(BaseModel):
    feature_id: uuid.UUID


class ModifiableFeatureFields(BaseModel):
    feature_name: str
    feature_description: Optional[str] = None
    update_freq: Optional[str] = None


class ModifyFeatureRequest(BaseModel):
    fields: FeatureIdentifierField
    modfield: ModifiableFeatureFields


class ModifyFeatureResult(BaseModel):
    message: str
    details: Dict[str, Any] | List[Dict[str, Any]] | None


class GetFeatureRequest(BaseModel):
    feature_id: str
    version: int | None = None


class CreationMethod(str, Enum):
    PARSER = "parser"
    INCEPTION = "inception"


class UploadFeatureScriptRequest(BaseModel):
    file_path: str
    creation_method: CreationMethod
    scheduling_expression: str | None = None
    versioning: bool = False


class UploadFeatureScriptResult(BaseModel):
    message: str
    details: Dict[str, Any] | List[Dict[str, Any]] | None


class ListFeatureExecutionsRequest(BaseModel):
    execution_id: uuid.UUID


class ListFeatureExecutionsResult(BaseModel):
    message: str
    details: Dict[str, Any] | List[Dict[str, Any]] | None
