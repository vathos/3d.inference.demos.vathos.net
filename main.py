#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
################################################################################

import os
import json
from time import perf_counter
import logging

import mayavi.mlab as mlab
import trimesh
from imageio import imread
import requests
import numpy as np

from lib.backprojection import backproject, unpack_short
from lib.authentication import get_service_account_token
from lib.api import get_product, get_file, get_configuration

if __name__ == '__main__':

  token = get_service_account_token(os.environ.get('CLIENT_ID'),
                                    os.environ.get('CLIENT_SECRET'))
  product_id = '62dffe3ad8cbdb0012b57fe9'

  # get product data and configuration
  product = get_product(product_id, token)
  configuration = get_configuration(product_id, token)

  # get depth image for visualization purposes and convert to m
  depth_img_compressed = imread('./res/test.png')

  # load mesh
  mesh = trimesh.load(get_file(product['inputFile'], token),
                      file_type='OBJ',
                      color=(0.5, 0.5, 0.5))
  # mesh is in mm
  mesh.apply_scale(0.001)

  # backproject with intrinsic info from product
  K = np.reshape(np.array(product['camera']['intrinsics']), (3, 3), 'F')
  pcl = backproject(0.001 * unpack_short(depth_img_compressed), K)

  # run cloud inference
  inference_url = 'https://staging.api.gke.vathos.net/v1/workflows/votenet'
  files = {'files': open('./res/test.png', 'rb')}
  values = {
      'product': json.dumps(product),
      'configuration': json.dumps(configuration)
  }

  tic = perf_counter()
  inference_response = requests.post(
      inference_url,
      files=files,
      data=values,
      headers={'Authorization': 'Bearer ' + token})

  toc = perf_counter()
  logging.info('Inference took %f s', toc - tic)

  response_json = inference_response.json()

  logging.info('Got %d detections: %s', len(response_json['detections']),
               response_json['detections'])

  mlab.figure()
  mlab.points3d(pcl[:, 0],
                pcl[:, 1],
                pcl[:, 2],
                scale_factor=0.001,
                resolution=3,
                mask_points=5)

  for detection in response_json['detections']:

    # pose is in camera coordinates
    pose = np.reshape(np.array(detection['frame'], dtype='f'), (4, 4), 'F')
    vertices = mesh.vertices @ pose[0:3, 0:3].transpose() + np.ones(
        mesh.vertices.shape) @ np.diag(pose[0:3, 3])

    mlab.triangular_mesh(vertices[:, 0],
                         vertices[:, 1],
                         vertices[:, 2],
                         mesh.faces,
                         color=(0.6, 0.2, 0.2),
                         opacity=0.5)

  mlab.show()
