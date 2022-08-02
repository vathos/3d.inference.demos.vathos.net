# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
################################################################################
"""
Uncompression and backprojection of depth images.
"""

import numpy as np


def unpack_short(rgb):
  """Unpacks two byte channels into a single channel of type short."""
  return rgb[:, :, 0] + 256 * rgb[:, :, 1]


def backproject(depth, K):
  """Backprojects a depth image into a point cloud."""
  size = depth.shape[::-1]

  u, v = np.meshgrid(np.arange(0, size[0]), np.arange(0, size[1]))

  xyz_image = np.zeros(depth.shape + (3,))

  xyz_image[:, :, 0] = depth / K[0, 0] * (u - K[0, 2])
  xyz_image[:, :, 1] = depth / K[1, 1] * (v - K[1, 2])
  xyz_image[:, :, 2] = depth

  pcl = np.reshape(xyz_image, (xyz_image.shape[0] * xyz_image.shape[1], 3))

  # filter out 0
  pcl = pcl[np.where(pcl[:, 2] > 0)[0], :]

  return pcl