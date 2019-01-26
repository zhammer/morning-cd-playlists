import json
import os
from typing import Dict, List

from aws_xray_sdk.core import patch as xray_patch

import sentry_sdk
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

from playlists.delivery import util
from playlists.use_playlists import add_listen_to_playlist


if os.environ.get('AWS_EXECUTION_ENV'):
    # setup sentry
    sentry_sdk.init(
        dsn='https://20880ec2d150490cb8f8f9dd60dc2205@sentry.io/1359131',
        integrations=[AwsLambdaIntegration()]
    )

    # setup xray patching
    libraries = ('requests', 'boto3', 'botocore', 'psycopg2')
    xray_patch(libraries)


def consumer(event: Dict, context: Dict) -> None:
    playlists_context = util.create_default_context()
    for listen_id in _pluck_listen_ids(event):
        add_listen_to_playlist(playlists_context, listen_id)


def _pluck_listen_ids(aws_event: Dict) -> List[str]:
    """Pluck the listen ids from a batched sqs event.

    >>> _pluck_listen_ids({'Records': [{'body': '{"listen_id": "5"}'}]})
    ['5']
    """
    message_bodies = [json.loads(record['body']) for record in aws_event['Records']]
    return [message_body['listen_id'] for message_body in message_bodies]
