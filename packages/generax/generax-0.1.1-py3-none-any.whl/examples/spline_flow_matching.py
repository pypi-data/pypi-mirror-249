import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable, Iterator
from jaxtyping import Array, PRNGKeyArray
from generax.trainer import Trainer
import generax.util.misc as misc
import matplotlib.pyplot as plt
import equinox as eqx
import generax as gx

class FlowTransform(gx.TimeDependentRepeat):

  def __init__(self,
               input_shape: Tuple[int],
               n_flow_layers: int = 3,
               working_size: int = 16,
               hidden_size: int = 32,
               n_blocks: int = 4,
               filter_shape: Optional[Tuple[int]] = (3, 3),
               cond_shape: Optional[Tuple[int]] = None,
               coupling_split_dim: Optional[int] = None,
               reverse_conditioning: Optional[bool] = False,
               create_net: Optional[Callable[[PRNGKeyArray], Any]] = None,
               *,
               key: PRNGKeyArray,
               **kwargs):

    def init_transform(transform_input_shape, key):
      flow = gx.RationalQuadraticSpline(input_shape=transform_input_shape,
                           cond_shape=cond_shape,
                           K=8,
                           key=key)
      return flow

    def _create_net(net_input_shape, net_output_size, key):
      return TimeDependentResNet(input_shape=net_input_shape,
                    working_size=working_size,
                    hidden_size=hidden_size,
                    out_size=net_output_size,
                    n_blocks=n_blocks,
                    filter_shape=filter_shape,
                    cond_shape=cond_shape,
                    key=key)
    create_net = create_net if create_net is not None else _create_net

    def make_single_flow_layer(key: PRNGKeyArray) -> gx.TimeDependentSequential:
      k1, k2, k3 = random.split(key, 3)

      layers = []
      layer = gx.TimeDependentCoupling(init_transform,
                       create_net,
                       input_shape=input_shape,
                       cond_shape=cond_shape,
                       split_dim=coupling_split_dim,
                       reverse_conditioning=reverse_conditioning,
                       key=k1)
      layers.append(layer)
      layers.append(gx.TimeDependentWrapper(gx.CaleyOrthogonalMVP(input_shape=input_shape,
                              cond_shape=cond_shape,
                              key=k2)))
      layers.append(gx.TimeDependentWrapper(gx.ShiftScale(input_shape=input_shape,
                               cond_shape=cond_shape,
                               key=k3)))
      return gx.TimeDependentSequential(*layers, **kwargs)

    super().__init__(make_single_flow_layer, n_flow_layers, key=key)


################################################################################################################

if __name__ == '__main__':
  from debug import *
  from generax.distributions.base import *
  from generax.nn import *
  import generax as gx
  import generax.util as util
  # jax.config.update("jax_enable_x64", True)

  key = random.PRNGKey(0)

  # Get the dataset
  from sklearn.datasets import make_moons, make_swiss_roll
  data, y = make_moons(n_samples=100000, noise=0.1)
  data = data - data.mean(axis=0)
  data = data/data.std(axis=0)
  p1 = gx.EmpiricalDistribution(data)

  train_ds = p1.train_iterator(key, batch_size=64)

  data = next(train_ds)
  x = data['x']
  x_shape = x.shape[1:]

  # Construct the flow
  flow = gx.TimeDependentNormalizingFlow(transform=FlowTransform(input_shape=x_shape,
                                                                 key=key,
                                                                 n_flow_layers=3,
                                                                 n_blocks=4,
                                                                 hidden_size=32,
                                                                 working_size=16),
                                         prior=gx.Gaussian(input_shape=x_shape))

  # Build the probability path that we'll use for learning.
  # The target probability path is the expectation of cond_ppath
  # with the expectation taken over the dataset.
  cond_ppath = gx.TimeDependentNormalizingFlow(transform=gx.ConditionalOptionalTransport(input_shape=x_shape, key=key),
                                            prior=Gaussian(input_shape=x_shape))

  # Construct the loss function
  def loss(flow, data, key):

    def unbatched_loss(data, key):
      k1, k2 = random.split(key, 2)

      # Sample
      x1 = data['x']
      x0 = cond_ppath.prior.sample(k1)
      t = random.uniform(k2)

      # Compute f_t(x_0; x_1)
      def ft(t):
        return cond_ppath.to_data_space(t, x0, x1)
      xt, ut = jax.jvp(ft, (t,), (jnp.ones_like(t),))

      # Compute the parametric vector field
      vt = flow.vector_field(t, xt)

      ll = flow.log_prob(jnp.array(1.0), x1)

      # Compute the loss
      return jnp.sum((ut - vt)**2), ll

    unbatched_loss(util.unbatch(data), key)

    keys = random.split(key, data['x'].shape[0])
    objective, ll = jax.vmap(unbatched_loss)(data, keys)
    objective = objective.mean()
    aux = dict(objective=objective.mean(),
               ll=ll.mean())
    return objective, aux

  # x = data['x']
  # z = flow.to_base_space(jnp.array(0.0), x[0])
  # z = eqx.filter_vmap(flow.to_base_space)(jnp.zeros(x.shape[0]), x)
  # import pdb; pdb.set_trace()

  # loss(flow, data, key)
  # import pdb; pdb.set_trace()

  # Create the optimizer
  optimizer = gx.default_optimizer(lr=1e-3,
                                   clip_norm=15.0,
                                   warmup=1000)

  # Create the trainer and optimize
  trainer = Trainer(checkpoint_path='tmp/flow/spline_fm')
  flow = trainer.train(model=flow,
                       objective=loss,
                       evaluate_model=lambda x: x,
                       optimizer=optimizer,
                       num_steps=20000,
                       double_batch=-1,
                       data_iterator=train_ds,
                       checkpoint_every=5000,
                       test_every=-1,
                       retrain=True,
                       just_load=False)

  # Pull samples from the model
  keys = random.split(key, 1000)
  samples = eqx.filter_vmap(flow.sample)(jnp.ones(keys.shape[0]), keys)

  fig, ax = plt.subplots(1, 1)
  ax.scatter(*samples.T)
  plt.savefig('examples/spline_fm_samples.png')
  # plt.show()
  import pdb; pdb.set_trace()