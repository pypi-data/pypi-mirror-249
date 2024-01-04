#  -*- coding: utf-8 -*-
# SPDX-License-Identifier: MPL-2.0
# Copyright 2020-2021 John Mille<john@ews-network.net>

"""Top-level package for AWS CFN Custom resource Resolve parser."""

from __future__ import annotations

import base64
import json
import re

from boto3.session import Session
from botocore.exceptions import ClientError

__author__ = """John Preston"""
__email__ = "john@ews-network.net"
__version__ = "0.3.2"


SECRET_ARN_REGEXP = re.compile(
    r"(?:{{resolve:secretsmanager:)"
    r"(?P<arn>arn:(?P<partition>aws(?:-[a-z]+)?):secretsmanager:(?P<region>[a-z0-9-]+):"
    r"(?P<account_id>\d{12}):"
    r"(?:secret:(?P<secret_id>[a-z0-9A-Z-_./]+)))"
    r"(?P<extra>(?::SecretString:(?P<secret_key>[a-z0-9A-Z-_./]+))(?::(?P<version>[a-z0-9A-Z-]+)?)?)?(?:}})"
)

SECRET_NAME_REGEXP = re.compile(
    r"(?:{{resolve:secretsmanager:)(?P<name>[a-z0-9A-Z-_./]+)"
    r"(?P<extra>(?::SecretString:(?P<secret_key>[a-z0-9A-Z-_./]+))(?:(::)(?P<version>[a-z0-9A-Z-]+)?)?)?(?:}})"
)


def keypresent(key: str, obj: dict) -> bool:
    if obj and isinstance(obj, dict) and key in obj.keys():
        return True
    return False


def keyisset(key: str, obj: dict) -> bool:
    if keypresent(key, obj) and obj[key]:
        return True
    return False


def parse_secret_resolve_string(resolve_str: str) -> tuple:
    """
    Parse the resolve string to find the secret
    Returns key and stage if found/defined.
    """
    key = None
    stage = None
    if SECRET_ARN_REGEXP.match(resolve_str):
        parts = SECRET_ARN_REGEXP.match(resolve_str)
        secret = parts.group("arn")
        if not secret:
            raise ValueError("Unable to find the secret ARN in", resolve_str)
        key = parts.group("secret_key")
        stage = parts.group("version")
    elif SECRET_NAME_REGEXP.match(resolve_str):
        parts = SECRET_NAME_REGEXP.match(resolve_str)
        secret = parts.group("name")
        if not secret:
            raise ValueError("Unable to find the secret name in", resolve_str)
    else:
        raise ValueError(
            "Unable to define secret ARN nor secret name from", resolve_str
        )
    if parts:
        key = parts.group("secret_key")
        stage = parts.group("version")

    return secret, key, stage


def retrieve_secret(
    secret: str, key: str = None, stage: str = None, session: Session = None
) -> str:
    """
    Function to retrieve the secret value.
    If key is provided, returns the key value. Fails if key does not exist.
    If stage is provided, retrieves the secret for given stage. Fails if stage does not exist.

    :param str secret:
    :param str key:
    :param str stage:
    :param boto3.client client:
    :param boto3.session.Session session:
    :return: The secret string or specific key of
    :raises: KeyError  if the key is provided but not present in secret
    :raises: ClientError in case of an error with boto3
    :raises: ResourceNotFoundException,ResourceNotFoundException if specific issue with secret retrieval
    """
    if session is None or not isinstance(session, Session):
        session = Session()
    if stage is None:
        stage = "AWSCURRENT"
    client = session.client("secretsmanager")
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret, VersionStage=stage
        )
        if keyisset("SecretString", get_secret_value_response):
            res = json.loads(get_secret_value_response["SecretString"])
        else:
            res = json.loads(
                base64.b64decode(get_secret_value_response["SecretBinary"])
            )
        if key and keypresent(key, res):
            return res[key]
        elif key and not keypresent(key, res):
            raise KeyError(f"Secret {secret} does not have a key {key}")
        return res
    except client.exceptions as error:
        print(error)
        raise
    except ClientError as error:
        print(error)
        raise


def handle(resolve_str):
    secret_name, key, version = parse_secret_resolve_string(resolve_str)
    secret = retrieve_secret(secret_name, key, version)
    return secret
