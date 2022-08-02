# -*- coding: utf-8 -*-
################################################################################
#
# Copyright (c) 2020, Vathos GmbH
#
# All rights reserved.
#
################################################################################

import mayavi.mlab as mlab

def vis_extrinsics(data, scale=1.0, annotation=''):
  r"""
  Draws a coordinate frame.
  """
  xaxis = mlab.quiver3d([data[0, 3]], [data[1, 3]], [data[2, 3]], [data[0, 0]],
                        [data[1, 0]], [data[2, 0]],
                        mode='arrow',
                        scale_factor=scale,
                        color=(1, 0, 0))
  yaxis = mlab.quiver3d([data[0, 3]], [data[1, 3]], [data[2, 3]], [data[0, 1]],
                        [data[1, 1]], [data[2, 1]],
                        mode='arrow',
                        scale_factor=scale,
                        color=(0, 1, 0))
  zaxis = mlab.quiver3d([data[0, 3]], [data[1, 3]], [data[2, 3]], [data[0, 2]],
                        [data[1, 2]], [data[2, 2]],
                        mode='arrow',
                        scale_factor=scale,
                        color=(0, 0, 1))
  mlab.text3d(data[0, 3] + scale * data[0, 2],
              data[1, 3] + scale * data[1, 2],
              data[2, 3] + scale * data[2, 2],
              annotation,
              scale=scale * 0.25,
              color=(0.4, 0.4, 0.4))
  return xaxis, yaxis, zaxis