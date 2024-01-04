import logging,os
from localstack import config
DB_ENGINE='postgres'
ASSETS_BUCKET_NAME='snowflake-assets'
ASSETS_KEY_PREFIX='uploads/'
logger=logging.getLogger('snowflake_local')
logger.setLevel(logging.INFO)
if config.DEBUG:logger.setLevel(logging.DEBUG)
SF_LOG=os.getenv('SF_LOG','').strip()
TRACE_LOG=SF_LOG.lower()=='trace'
S3_ENDPOINT=os.getenv('SF_S3_ENDPOINT','').strip()or's3.localhost.localstack.cloud:4566'