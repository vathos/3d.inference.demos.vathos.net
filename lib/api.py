# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""
Gets data from the REST-API.
"""

from io import BytesIO

import requests


def get_configuration(product_id, token):
  """Get the most recent inference configuration."""
  url = f'https://staging.api.gke.vathos.net/v1/configurations?product={product_id}&service=votenet.workflows.vathos.net'
  response = requests.get(url, headers={'Authorization': 'Bearer ' + token})
  configurations = response.json()

  if len(configurations) == 0:
    return None
  else:
    # last is the newest
    return configurations[-1]['data']


def get_product(product_id, token):
  """Downloads product data."""
  url = 'https://staging.api.gke.vathos.net/v1/products/' + product_id \
     + '?%24populate%5B0%5D=grips&%24populate%5B1%5D=states&%24populate%5B1%5D=camera'
  product_response = requests.get(url,
                                  headers={'Authorization': 'Bearer ' + token})
  return product_response.json()


def get_file(file_id, token):
  """Downloads a file from the REST API."""
  http_request = requests.get('https://staging.api.gke.vathos.net/v1/blobs/' +
                              file_id,
                              headers={'Authorization': 'Bearer ' + token},
                              stream=True)
  http_request.raw.decode_content = True

  return BytesIO(http_request.content)
