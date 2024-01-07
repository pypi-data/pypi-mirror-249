# import asyncio
import tempfile
import traceback

import boto3
import filetype
from botocore import UNSIGNED
from botocore.client import Config
from botocore.exceptions import ClientError

from ....common.logger import logger
from ....common.storage import BaseStorage

# from ....common.types import CrawlerNop  # CrawlerBackTask,
from ....common.types import CrawlerContent  # , DatapoolContentType
from ..base_plugin import BasePlugin, BasePluginException


class S3Exception(BasePluginException):
    pass


class S3Plugin(BasePlugin):
    def __init__(
        self, storage, aws_access_key_id=None, aws_secret_access_key=None
    ):
        super().__init__(storage)

        logger.info(f"{aws_access_key_id=}")
        logger.info(f"{aws_secret_access_key=}")

        # empty key means bucket is public
        if aws_access_key_id == "":
            self.is_public_bucket = True
            self.s3_client = boto3.client(
                "s3", config=Config(signature_version=UNSIGNED)
            )
            self.s3 = boto3.resource(
                "s3", config=Config(signature_version=UNSIGNED)
            )
        else:
            self.is_public_bucket = False
            self.s3_client = boto3.client(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )
            self.s3 = boto3.resource(
                "s3",
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
            )

    @staticmethod
    def is_supported(url):
        u = BasePlugin.parse_url(url)
        # logger.info( f'============ s3 {u=} =====================================')
        if u.netloc == "s3.console.aws.amazon.com":
            # logger.info( 'netloc ok')
            if u.path[0:12] == "/s3/buckets/":
                # logger.info( 'path ok')
                return True
            # elif u.path[0:6] == '/watch' and u.query[0:2] == 'v=':
            #     self.video_id = u.query[2:13]
            #     return True

        return False

    async def process(self, url):
        logger.info(f"s3::process({url})")

        u = self.parse_url(url)
        self.bucket_name = u.path.split("/")[3]
        logger.info(f"{self.bucket_name=}")

        bucket = self.s3.Bucket(self.bucket_name)

        try:
            tag_id = self._download(BasePlugin.license_filename)
            tag_id = await BasePlugin.parse_tag_in(tag_id.decode())
            logger.info(f"found license: {tag_id}")
        except S3Exception:
            logger.error(
                "bucket does not contain license.txt, cannot process(1)"
            )
            logger.error(traceback.format_exc())
            return
        except ClientError:
            logger.error(
                "bucket does not contain license.txt, cannot process(2)"
            )
            logger.error(traceback.format_exc())
            return

        for obj in bucket.objects.all():
            logger.info(f"{obj=}")

            if obj.key == BasePlugin.license_filename:
                continue

            if self.is_public_bucket is False:
                # THIS IS PURE API ACCESS URL
                obj_url = f"https://s3.console.aws.amazon.com/s3/buckets/{self.bucket_name}/{obj.key}"
            else:
                # THIS IS DIRECT URL ( FOR PUBLIC BUCKETS )
                # TODO: region?
                obj_url = (
                    f"https://{self.bucket_name}.s3.amazonaws.com/{obj.key}"
                )

            storage_id = BaseStorage.gen_id(obj_url)

            content = self._download(obj.key)

            try:
                type = self._get_datapool_content_type(content)

                await self.storage.put(storage_id, content)

                yield CrawlerContent(
                    tag_id=tag_id,
                    type=type,
                    storage_id=storage_id,
                    url=obj_url,
                )
            except S3Exception as e:
                logger.info(f"mime type not supported/detected: {e}")

    def _download(self, key):
        with tempfile.NamedTemporaryFile() as tmp:
            self.s3_client.download_fileobj(self.bucket_name, key, tmp)

            tmp.seek(0, 0)
            return tmp.read()

    def _get_datapool_content_type(self, content):
        type = filetype.guess(content)
        if type is None:
            raise S3Exception("unknown file type")
        return BasePlugin.get_content_type_by_mime_type(type.mime)
