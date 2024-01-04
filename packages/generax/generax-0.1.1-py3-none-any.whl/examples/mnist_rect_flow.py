import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable, Iterator
from jaxtyping import Array, PRNGKeyArray
from generax.trainer import Trainer
import generax.util.misc as misc
import matplotlib.pyplot as plt
import generax.util as util
import equinox as eqx
from torch.utils.data import Dataset, DataLoader, RandomSampler
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import generax as gx

def get_dataset_iter(dtype=jnp.bfloat16):

  training_data = datasets.MNIST(
      root="data",
      train=True,
      download=True,
      transform=ToTensor()
  )

  random_sampler = RandomSampler(training_data, replacement=True)
  train_dataloader = DataLoader(training_data, batch_size=64, sampler=random_sampler, drop_last=True)

  def get_train_ds() -> Iterator[Mapping[str, Array]]:
    train_iter = iter(train_dataloader)
    while True:
      for batch in train_dataloader:
        images, labels = batch
        x = images.numpy().transpose(0, 2, 3, 1).astype(dtype)
        yield dict(x=x)

  train_ds = get_train_ds()
  return train_ds

################################################################################################################

def create_coupling_layer(input_shape: Tuple[int],
                          key: PRNGKeyArray):

  # Determine how we'll split the input
  transform_input_shape, net_input_shape = gx.Coupling.get_split_shapes(input_shape)

  # Construct the transform
  transform = gx.RationalQuadraticSpline(input_shape=transform_input_shape,
                                         key=key,
                                         K=8)

  # Construct the conditioning network
  net_output_size = gx.Coupling.get_net_output_shapes(input_shape, transform)
  net = gx.Encoder(input_shape=net_input_shape,
                    dim=32,
                    dim_mults=(1, 4),
                    resnet_block_groups=8,
                    attn_heads=4,
                    attn_dim_head=32,
                    out_size=net_output_size,
                    cond_shape=None,
                    key=key)

  # Construct the coupling layer
  layer = gx.Coupling(transform,
                      net,
                      input_shape=input_shape,
                      cond_shape=None,
                      key=key)
  return layer

def create_flow_block(input_shape: Tuple[int],
                      key: PRNGKeyArray):

  # Create a list of coupling layers
  layers = []
  for i in range(3):
    k1, k2, k3, key = random.split(key, 4)
    layer = create_coupling_layer(input_shape=input_shape,
                                  key=k1)
    layers.append(layer)
    layers.append(gx.OneByOneConv(input_shape=input_shape,
                                  key=k2))
    layers.append(gx.ShiftScale(input_shape=input_shape,
                                key=k3))

  # Create the flow
  flow = gx.Sequential(*layers)
  return flow

def create_flow(input_shape: Tuple[int],
                key: PRNGKeyArray):

  # Create a list of flow blocks
  blocks = []
  for i in range(3):
    key, _ = random.split(key, 2)
    block = create_flow_block(input_shape=input_shape,
                              key=key)
    blocks.append(block)

  # Create the flow
  flow = gx.Sequential(*blocks)
  return flow

################################################################################################################

class InvertibleDownsample(gx.InjectiveTransform):

  haar: gx.HaarWavelet
  nice1: gx.Coupling
  nice2: gx.Coupling
  slice: gx.Slice

  def __init__(self,
               *_,
               input_shape: Tuple[int],
               key: PRNGKeyArray,
               **kwargs):
    """**Arguments**:

    - `input_shape`: The input shape.
    """
    output_shape = (input_shape[0]//2, input_shape[1]//2, input_shape[2])
    super().__init__(input_shape=input_shape,
                     output_shape=output_shape,
                     **kwargs)

    self.haar = gx.HaarWavelet(input_shape=input_shape)
    haar_output_shape = self.haar.output_shape

    def init_transform(transform_input_shape, key):
      return gx.Shift(input_shape=transform_input_shape,
                      key=key)

    def create_net(net_input_shape, net_output_size, key):
      H, W, C = net_input_shape
      return gx.UNet(input_shape=net_input_shape,
                    dim=32,
                    out_channels=net_output_size//(H*W),
                    dim_mults=(1, 4),
                    resnet_block_groups=8,
                    attn_heads=4,
                    attn_dim_head=32,
                    time_dependent=False,
                    key=key)

    k1, k2 = random.split(key, 2)
    self.nice1 = gx.Coupling(init_transform,
                       create_net,
                       input_shape=haar_output_shape,
                       split_dim=1,
                       reverse_conditioning=False,
                       key=k1)
    self.nice2 = gx.Coupling(init_transform,
                       create_net,
                       input_shape=haar_output_shape,
                       split_dim=1,
                       reverse_conditioning=True,
                       key=k2)

    self.slice = gx.Slice(input_shape=haar_output_shape,
                          output_shape=output_shape)

  def __call__(self,
               x: Array,
               y: Optional[Array] = None,
               inverse: bool = False,
               **kwargs) -> Array:
    """**Arguments**:

    - `x`: The input to the transformation
    - `y`: The conditioning information
    - `inverse`: Whether to inverse the transformation

    **Returns**:
    (z, log_det)
    """
    if inverse == False:
      h1, log_det1 = self.haar(x)
      h2, log_det2 = self.nice1(h1)
      h3, log_det3 = self.nice2(h2)
      z, _ = self.slice(h3)

    else:
      h3, _ = self.slice(x, inverse=True)
      h2, log_det3 = self.nice2(h3, inverse=True)
      h1, log_det2 = self.nice1(h2, inverse=True)
      z, log_det1 = self.haar(h1, inverse=True)

    return z, log_det1 + log_det2 + log_det3

################################################################################################################

if __name__ == '__main__':
  from debug import *
  import generax.util as util
  import matplotlib.pyplot as plt

  dtype = jnp.float64
  if dtype == jnp.float64:
    jax.config.update("jax_enable_x64", True)

  train_ds = get_dataset_iter(dtype=dtype)
  data = next(train_ds)
  x = data['x']
  x_shape = x.shape[1:]
  key = random.PRNGKey(0)

  layer = InvertibleDownsample(input_shape=(28, 28, 1),
                            key=key)
  x_original = x
  x = eqx.filter_vmap(layer.project)(x)

  z, log_det1 = layer(x[0])
  x_reconstr, log_det2 = layer(z, inverse=True)
  assert jnp.allclose(x[0], x_reconstr)
  assert jnp.allclose(log_det1, -log_det2)
  import pdb; pdb.set_trace()