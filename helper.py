import gzip
import json
import os
import time
import zlib
from typing import Union, Any

import brotli
import zstandard as zstd
from loguru import logger

from config import DEBUG


def convert_keys_to_int(d: dict) -> dict:
    return {int(k) if k.isdigit() else k: v for k, v in d.items()}


def load_json(filename: str) -> Union[dict, list]:
    if os.path.exists(filename):
        with open(filename, mode='r', encoding="utf-8") as f:
            return json.load(f, object_hook=convert_keys_to_int)
    else:
        return {}


def save_json(data: Any, filename: str):
    with open(filename, mode='w', encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def decompress_response(response) -> bytes:
    content_encoding = response.headers.get('Content-Encoding', '').lower()
    content = response.content

    logger.debug(f"Content-Encoding: {content_encoding}")
    logger.debug(f"Content length: {len(content)} bytes")

    try:
        if content_encoding == 'gzip':
            return gzip.decompress(content)

        elif content_encoding == 'deflate':
            return zlib.decompress(content)

        elif content_encoding == 'br':
            if content.startswith(b'{'):
                return content

            try:
                return brotli.decompress(content)
            except brotli.error as e:
                logger.debug(f"Brotli decompression failed: {e}")

                if DEBUG:
                    with open("br_debug", mode="wb") as f:
                        f.write(response.content)

                return content

        elif content_encoding == 'zstd':
            zd = zstd.ZstdDecompressor()
            return zd.decompress(content)

        else:
            logger.debug("No compression detected, returning content as-is")
            return content

    except Exception as e:
        logger.debug(f"Decompression error: {type(e).__name__}: {e}")
        raise


def timestamp_ms():
    return int(time.time() * 1000)
