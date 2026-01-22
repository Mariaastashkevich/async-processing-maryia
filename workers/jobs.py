import shutil
from datetime import datetime, timezone
import json
import uuid
from sqlalchemy import update
from pathlib import Path
from typing import cast, Any

from db.db_session_cm import db_session
from db.enums import JobStatus
from db.models.jobs import JobsOrm
from repositories.sqlalchemy.datasets import SqlAlchemyDatasetRepository
from repositories.sqlalchemy.jobs import SqlAlchemyJobRepository
from services.settings import settings
from services.storage.s3_client import S3Client
from services.storage.storage_service import StorageService
from workers.celery_app import celery_app
from workers.processing.anomalies import detect_anomalies
from workers.processing.metrics import compute_metrics
from workers.processing.normalize import normalize


@celery_app.task
def run_job(job_id: str):
    job_uuid = uuid.UUID(job_id)
    should_stop = False
    print("DB URL:", settings.DATABASE_URL_psycopg)

    storage = StorageService(
        S3Client(
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.MINIO_ROOT_USER,
            aws_secret_access_key=settings.MINIO_ROOT_PASSWORD,
            region_name=settings.S3_REGION,
        ),
        temp_dir=settings.STORAGE_TMP_DIR,
    )

    with db_session() as session:
        job_repo = SqlAlchemyJobRepository(session)
        dataset_repo = SqlAlchemyDatasetRepository(session)

        job = job_repo.get(job_uuid)
        if job is None:
            return

        if job.job_status == JobStatus.CANCELED:
            should_stop = True
        else:
            dataset = dataset_repo.get(job.dataset_id)
            if dataset is None:
                job.job_status = JobStatus.FAILED
                job.error_message = "Dataset not found"
                job.finished_at = datetime.now(timezone.utc)
                should_stop = True
            else:
                # job.job_status = JobStatus.RUNNING
                # job.started_at = datetime.now(timezone.utc)
                session.execute(
                    update(JobsOrm)
                    .where(JobsOrm.id == job_uuid)
                    .values(
                        job_status=JobStatus.RUNNING,
                        started_at=datetime.utcnow(),
                    )
                )
                session.commit()

                try:
                    file_path = storage.download_to_temp(
                        uri=dataset.storage_uri,
                        job_id=str(job.id),
                    )

                    job_dir = settings.STORAGE_TMP_DIR / str(job.id)

                    match job.job_type.value:
                        case "metrics":
                            data = compute_metrics(
                                dataset_path=file_path,
                                params=cast(dict[str, Any], job.params),
                            )
                            metrics_path = job_dir / "metrics.json"
                            metrics_path.write_text(json.dumps(data, indent=2))

                            storage.upload_file(
                                bucket=settings.S3_JOB_RESULTS_BUCKET,
                                key=f"{job.id}/metrics.json",
                                file_name=metrics_path,
                            )
                            job.result_uri = f"s3://{settings.S3_JOB_RESULTS_BUCKET}/{job.id}/metrics.json"

                        case "anomalies":
                            data = detect_anomalies(
                                dataset_path=file_path,
                                params=cast(dict[str, Any], job.params),
                            )
                            anomalies_path = job_dir / "anomalies.json"
                            anomalies_path.write_text(json.dumps(data, indent=2))

                            storage.upload_file(
                                bucket=settings.S3_JOB_RESULTS_BUCKET,
                                key=f"{job.id}/anomalies.json",
                                file_name=anomalies_path,
                            )
                            job.result_uri = f"s3://{settings.S3_JOB_RESULTS_BUCKET}/{job.id}/anomalies.json"

                        case "normalize":
                            normalized_path = normalize(
                                dataset_path=file_path,
                                params=cast(dict[str, Any], job.params),
                            )
                            storage.upload_file(
                                bucket=settings.S3_JOB_RESULTS_BUCKET,
                                key=f"{job.id}/normalized.csv",
                                file_name=normalized_path,
                            )
                            job.result_uri = f"s3://{settings.S3_JOB_RESULTS_BUCKET}/{job.id}/normalized.csv"

                    job.job_status = JobStatus.COMPLETED
                    job.finished_at = datetime.now(timezone.utc)

                except Exception as exc:
                    job.job_status = JobStatus.FAILED
                    job.error_message = str(exc)
                    job.finished_at = datetime.now(timezone.utc)

                finally:
                    shutil.rmtree(settings.STORAGE_TMP_DIR / str(job.id), ignore_errors=True)


    if should_stop:
        return









