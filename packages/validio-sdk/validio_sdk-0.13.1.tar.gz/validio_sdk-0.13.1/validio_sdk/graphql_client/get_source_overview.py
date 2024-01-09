from datetime import datetime
from typing import Annotated, Any, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import CredentialId, CronExpression, SourceId

from .base_model import BaseModel
from .enums import CatalogAssetType, FileFormat, StreamingSourceMessageFormat


class GetSourceOverview(BaseModel):
    source: Optional[
        Annotated[
            Union[
                "GetSourceOverviewSourceSource",
                "GetSourceOverviewSourceAwsAthenaSource",
                "GetSourceOverviewSourceAwsKinesisSource",
                "GetSourceOverviewSourceAwsRedshiftSource",
                "GetSourceOverviewSourceAwsS3Source",
                "GetSourceOverviewSourceDatabricksSource",
                "GetSourceOverviewSourceGcpBigQuerySource",
                "GetSourceOverviewSourceGcpPubSubLiteSource",
                "GetSourceOverviewSourceGcpPubSubSource",
                "GetSourceOverviewSourceGcpStorageSource",
                "GetSourceOverviewSourceKafkaSource",
                "GetSourceOverviewSourcePostgreSqlSource",
                "GetSourceOverviewSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetSourceOverviewSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceSourceStats"
    catalog_asset: Optional["GetSourceOverviewSourceSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )


class GetSourceOverviewSourceSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceSourceStatsSchemaCoverage" = Field(
        alias="schemaCoverage"
    )


class GetSourceOverviewSourceSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceAwsAthenaSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceAwsAthenaSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceAwsAthenaSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceAwsAthenaSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceAwsAthenaSourceConfig"


class GetSourceOverviewSourceAwsAthenaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceAwsAthenaSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceAwsAthenaSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceAwsAthenaSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceAwsAthenaSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceAwsAthenaSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceOverviewSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceAwsKinesisSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceAwsKinesisSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceAwsKinesisSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceAwsKinesisSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceAwsKinesisSourceConfig"


class GetSourceOverviewSourceAwsKinesisSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceAwsKinesisSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceAwsKinesisSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceAwsKinesisSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceAwsKinesisSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceAwsKinesisSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "GetSourceOverviewSourceAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceOverviewSourceAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceOverviewSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceAwsRedshiftSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceAwsRedshiftSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceAwsRedshiftSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceAwsRedshiftSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceAwsRedshiftSourceConfig"


class GetSourceOverviewSourceAwsRedshiftSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceAwsRedshiftSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceAwsRedshiftSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceAwsRedshiftSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceAwsRedshiftSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceOverviewSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceAwsS3SourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceAwsS3SourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceAwsS3SourceStats"
    catalog_asset: Optional["GetSourceOverviewSourceAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    config: "GetSourceOverviewSourceAwsS3SourceConfig"


class GetSourceOverviewSourceAwsS3SourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceAwsS3SourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceAwsS3SourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceAwsS3SourceStatsSchemaCoverage" = Field(
        alias="schemaCoverage"
    )


class GetSourceOverviewSourceAwsS3SourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceAwsS3SourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["GetSourceOverviewSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceOverviewSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceOverviewSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceDatabricksSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceDatabricksSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceDatabricksSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceDatabricksSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceDatabricksSourceConfig"


class GetSourceOverviewSourceDatabricksSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceDatabricksSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceDatabricksSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceDatabricksSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceDatabricksSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceDatabricksSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceOverviewSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceGcpBigQuerySourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceGcpBigQuerySourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceGcpBigQuerySourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceGcpBigQuerySourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceGcpBigQuerySourceConfig"


class GetSourceOverviewSourceGcpBigQuerySourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceGcpBigQuerySourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceGcpBigQuerySourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceGcpBigQuerySourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceGcpBigQuerySourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceOverviewSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceGcpPubSubLiteSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceGcpPubSubLiteSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceGcpPubSubLiteSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceGcpPubSubLiteSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceGcpPubSubLiteSourceConfig"


class GetSourceOverviewSourceGcpPubSubLiteSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceGcpPubSubLiteSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceGcpPubSubLiteSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceGcpPubSubLiteSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceGcpPubSubLiteSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceGcpPubSubLiteSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceOverviewSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceOverviewSourceGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceOverviewSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceGcpPubSubSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceGcpPubSubSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceGcpPubSubSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceGcpPubSubSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceGcpPubSubSourceConfig"


class GetSourceOverviewSourceGcpPubSubSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceGcpPubSubSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceGcpPubSubSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceGcpPubSubSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceGcpPubSubSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceGcpPubSubSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "GetSourceOverviewSourceGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceOverviewSourceGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceOverviewSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceGcpStorageSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceGcpStorageSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceGcpStorageSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceGcpStorageSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceGcpStorageSourceConfig"


class GetSourceOverviewSourceGcpStorageSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceGcpStorageSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceGcpStorageSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceGcpStorageSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceGcpStorageSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceGcpStorageSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["GetSourceOverviewSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class GetSourceOverviewSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class GetSourceOverviewSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceKafkaSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceKafkaSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceKafkaSourceStats"
    catalog_asset: Optional["GetSourceOverviewSourceKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    config: "GetSourceOverviewSourceKafkaSourceConfig"


class GetSourceOverviewSourceKafkaSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceKafkaSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceKafkaSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceKafkaSourceStatsSchemaCoverage" = Field(
        alias="schemaCoverage"
    )


class GetSourceOverviewSourceKafkaSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceKafkaSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional[
        "GetSourceOverviewSourceKafkaSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class GetSourceOverviewSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class GetSourceOverviewSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourcePostgreSqlSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourcePostgreSqlSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourcePostgreSqlSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourcePostgreSqlSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourcePostgreSqlSourceConfig"


class GetSourceOverviewSourcePostgreSqlSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourcePostgreSqlSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourcePostgreSqlSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourcePostgreSqlSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourcePostgreSqlSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourcePostgreSqlSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class GetSourceOverviewSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    credential: "GetSourceOverviewSourceSnowflakeSourceCredential"
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")
    data_quality: "GetSourceOverviewSourceSnowflakeSourceDataQuality" = Field(
        alias="dataQuality"
    )
    stats: "GetSourceOverviewSourceSnowflakeSourceStats"
    catalog_asset: Optional[
        "GetSourceOverviewSourceSnowflakeSourceCatalogAsset"
    ] = Field(alias="catalogAsset")
    config: "GetSourceOverviewSourceSnowflakeSourceConfig"


class GetSourceOverviewSourceSnowflakeSourceCredential(BaseModel):
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    resource_namespace: str = Field(alias="resourceNamespace")


class GetSourceOverviewSourceSnowflakeSourceDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float


class GetSourceOverviewSourceSnowflakeSourceStats(BaseModel):
    schema_coverage: "GetSourceOverviewSourceSnowflakeSourceStatsSchemaCoverage" = (
        Field(alias="schemaCoverage")
    )


class GetSourceOverviewSourceSnowflakeSourceStatsSchemaCoverage(BaseModel):
    coverage: float
    covered_count: int = Field(alias="coveredCount")
    total_count: int = Field(alias="totalCount")


class GetSourceOverviewSourceSnowflakeSourceCatalogAsset(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    asset_type: CatalogAssetType = Field(alias="assetType")


class GetSourceOverviewSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


GetSourceOverview.model_rebuild()
GetSourceOverviewSourceSource.model_rebuild()
GetSourceOverviewSourceSourceCredential.model_rebuild()
GetSourceOverviewSourceSourceDataQuality.model_rebuild()
GetSourceOverviewSourceSourceStats.model_rebuild()
GetSourceOverviewSourceSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceAwsAthenaSource.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceCredential.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceDataQuality.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceStats.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceAwsAthenaSourceConfig.model_rebuild()
GetSourceOverviewSourceAwsKinesisSource.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceCredential.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceDataQuality.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceStats.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceConfig.model_rebuild()
GetSourceOverviewSourceAwsKinesisSourceConfigMessageFormat.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSource.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceCredential.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceDataQuality.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceStats.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceAwsRedshiftSourceConfig.model_rebuild()
GetSourceOverviewSourceAwsS3Source.model_rebuild()
GetSourceOverviewSourceAwsS3SourceCredential.model_rebuild()
GetSourceOverviewSourceAwsS3SourceDataQuality.model_rebuild()
GetSourceOverviewSourceAwsS3SourceStats.model_rebuild()
GetSourceOverviewSourceAwsS3SourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceAwsS3SourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceAwsS3SourceConfig.model_rebuild()
GetSourceOverviewSourceAwsS3SourceConfigCsv.model_rebuild()
GetSourceOverviewSourceDatabricksSource.model_rebuild()
GetSourceOverviewSourceDatabricksSourceCredential.model_rebuild()
GetSourceOverviewSourceDatabricksSourceDataQuality.model_rebuild()
GetSourceOverviewSourceDatabricksSourceStats.model_rebuild()
GetSourceOverviewSourceDatabricksSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceDatabricksSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceDatabricksSourceConfig.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySource.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceCredential.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceDataQuality.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceStats.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceGcpBigQuerySourceConfig.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSource.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceCredential.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceDataQuality.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceStats.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceConfig.model_rebuild()
GetSourceOverviewSourceGcpPubSubLiteSourceConfigMessageFormat.model_rebuild()
GetSourceOverviewSourceGcpPubSubSource.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceCredential.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceDataQuality.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceStats.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceConfig.model_rebuild()
GetSourceOverviewSourceGcpPubSubSourceConfigMessageFormat.model_rebuild()
GetSourceOverviewSourceGcpStorageSource.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceCredential.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceDataQuality.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceStats.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceConfig.model_rebuild()
GetSourceOverviewSourceGcpStorageSourceConfigCsv.model_rebuild()
GetSourceOverviewSourceKafkaSource.model_rebuild()
GetSourceOverviewSourceKafkaSourceCredential.model_rebuild()
GetSourceOverviewSourceKafkaSourceDataQuality.model_rebuild()
GetSourceOverviewSourceKafkaSourceStats.model_rebuild()
GetSourceOverviewSourceKafkaSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceKafkaSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceKafkaSourceConfig.model_rebuild()
GetSourceOverviewSourceKafkaSourceConfigMessageFormat.model_rebuild()
GetSourceOverviewSourcePostgreSqlSource.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceCredential.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceDataQuality.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceStats.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourcePostgreSqlSourceConfig.model_rebuild()
GetSourceOverviewSourceSnowflakeSource.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceCredential.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceDataQuality.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceStats.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceStatsSchemaCoverage.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceCatalogAsset.model_rebuild()
GetSourceOverviewSourceSnowflakeSourceConfig.model_rebuild()
