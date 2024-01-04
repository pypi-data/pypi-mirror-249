import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable
import einops
import equinox as eqx
from abc import ABC, abstractmethod
from jaxtyping import Array, PRNGKeyArray
import generax.util.misc as misc
import generax.util as util
import lineax as lx

################################################################################################################

def compute_vol_change(z: Array,
                       transform: eqx.Module,
                       method: str = 'brute_force',
                       key: PRNGKeyArray = None,
                       **kwargs) -> Array:
  """Compute the volume change of the transformation.

  **Arguments**:

  - `z`: An element of the base space
  - `method`: How to compute the log determinant.  Options are:
    - `brute_force`: Compute the entire Jacobian
    - `iterative`: Use conjugate gradient (https://arxiv.org/pdf/2106.01413.pdf)
  - `key`: A `jax.random.PRNGKey` for initialization.  Needed for some methods

  **Returns**:
  The log determinant of J^TJ
  """

  def jvp(v_flat):
    v = v_flat.reshape(z.shape)
    _, (Jv) = jax.jvp(transform, (z,), (v,))
    return Jv.ravel()

  if method == 'brute_force':
    z_dim = util.list_prod(z.shape)
    eye = jnp.eye(z_dim)
    J = jax.vmap(jvp)(eye)
    return -0.5*jnp.linalg.slogdet(J.T@J)[1]

  elif method == 'iterative':

    def vjp(v_flat):
      v = v_flat.reshape(z.shape)
      _, vjp = jax.vjp(transform, z)
      return vjp(v)[0].ravel()

    def vjp_jvp(v_flat):
      return vjp(jvp(v_flat))

    v = random.normal(key, shape=z.shape)

    operator = lx.FunctionLinearOperator(vjp_jvp, v, tags=lx.positive_semidefinite_tag))
    solver = lx.CG(rtol=1e-6, atol=1e-6)
    out = lx.linear_solve(operator, v, solver).value

    z_dim = util.list_prod(z.shape)
    eye = jnp.eye(z_dim)
    J = jax.vmap(jvp)(eye)
    JTJ = J.T@J
    comp = jnp.linalg.inv(JTJ)@v

    import pdb; pdb.set_trace()

if __name__ == '__main__':
  from debug import *
  import matplotlib.pyplot as plt
  jax.config.update("jax_enable_x64", True)

  key = random.PRNGKey(0)
  x = random.normal(key, shape=(4, 8, 8, 2))