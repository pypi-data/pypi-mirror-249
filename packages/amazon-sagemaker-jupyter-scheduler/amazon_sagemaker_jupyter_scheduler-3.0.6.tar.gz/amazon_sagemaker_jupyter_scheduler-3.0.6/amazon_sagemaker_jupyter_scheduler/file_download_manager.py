import os
import io
import random
import tarfile
from multiprocessing import Process
from typing import Dict, List, Optional, Type

import fsspec
import botocore
import logging

from urllib.parse import urlparse
from botocore.session import get_session
from jupyter_server.utils import ensure_async

from jupyter_scheduler.exceptions import SchedulerError
from jupyter_scheduler.scheduler import BaseScheduler
from jupyter_scheduler.job_files_manager import JobFilesManager

from amazon_sagemaker_jupyter_scheduler.app_metadata import get_region_name

class SageMakerJobFilesManager(JobFilesManager):
    scheduler = None

    def __init__(self, scheduler: Type[BaseScheduler]):
        self.scheduler = scheduler

    async def copy_from_staging(self, job_id: str, redownload: Optional[bool] = False):
        job = await ensure_async(self.scheduler.get_job(job_id, False))
        staging_paths = await ensure_async(self.scheduler.get_staging_paths(job))
        output_filenames = self.scheduler.get_job_filenames(job)
        output_dir = self.scheduler.get_local_output_path(job)

        p = Process(
            target=Downloader(
                output_formats=job.output_formats,
                output_filenames=output_filenames,
                staging_paths=staging_paths,
                output_dir=output_dir,
                redownload=redownload,
            ).download
        )
        p.start()


class Downloader:
    def __init__(
        self,
        output_formats: List[str],
        output_filenames: Dict[str, str],
        staging_paths: Dict[str, str],
        output_dir: str,
        redownload: bool,
    ):
        self.output_formats = output_formats
        self.output_filenames = output_filenames
        self.staging_paths = staging_paths
        self.output_dir = output_dir
        self.redownload = redownload

    def generate_filepaths(self):
        """A generator that produces filepaths"""
        output_formats = self.output_formats + ["input"]

        for output_format in output_formats:
            input_filepath = self.staging_paths[output_format]
            output_filepath = os.path.join(self.output_dir, self.output_filenames[output_format])
            if not os.path.exists(output_filepath) or self.redownload:
                yield input_filepath, output_filepath

    def parse_s3_url(self, url):
        parsed_url = urlparse(url, allow_fragments=False)
        bucket_name = parsed_url.netloc
        key = parsed_url.path.lstrip('/')
        if parsed_url.query:
            key += '?' + parsed_url.query
        return bucket_name, key

    def get_s3_object_content(self, bucket: str, key: str) -> str:
        s3_client = get_session().create_client(
            "s3",
            region_name=get_region_name(),
        )
        
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response["Body"].read()

    def download_tar(self, archive_format: str = "tar"):
        archive_filepath = self.staging_paths[archive_format]
        read_mode = "r:gz" if archive_format == "tar.gz" else "tar"
        s3_bucket_name, s3_object_key = self.parse_s3_url(archive_filepath)
        archive_file = self.get_s3_object_content(
            bucket=s3_bucket_name, key=s3_object_key
        )
        archive_file_obj = io.BytesIO(archive_file)
        with tarfile.open(fileobj=archive_file_obj, mode=read_mode) as tar:
            filepaths = self.generate_filepaths()
            for input_filepath, output_filepath in filepaths:
                try:
                    input_file = tar.extractfile(member=input_filepath)
                    with fsspec.open(output_filepath, mode="wb") as output_file:
                        output_file.write(input_file.read())
                except Exception as e:
                    pass

    def download(self):
        # ensure presence of staging paths
        if not self.staging_paths:
            return

        # ensure presence of output dir
        output_dir = self.output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if "tar" in self.staging_paths:
            self.download_tar()
        elif "tar.gz" in self.staging_paths:
            self.download_tar("tar.gz")
        else:
            filepaths = self.generate_filepaths()
            for input_filepath, output_filepath in filepaths:
                try:
                    with fsspec.open(input_filepath) as input_file:
                        with fsspec.open(output_filepath, mode="wb") as output_file:
                            output_file.write(input_file.read())
                except Exception as e:
                    pass
