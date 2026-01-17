import enum


class Status(enum.Enum):
    UPLOADED = "uploaded"
    VALIDATING = "validating"
    READY = "ready"
    FAILED = "failed" # файл есть, но не прошёл проверку


class FileFormat(enum.Enum):
    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"


class JobType(enum.Enum):
    METRICS = "metrics"
    NORMALIZE ="normalize"
    ANOMALIES = "anomalies"


class JobStatus(enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class EventType(enum.Enum):
    CREATED = "created"
    STARTED = "started"
    PROCESSING = "processing"
    FINISHED = "finished"
    FAILED = "failed"


