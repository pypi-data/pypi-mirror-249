import jax
import jax.numpy as jnp
from jax import random
from functools import partial
from typing import Optional, Mapping, Tuple, Sequence, Union, Any, Callable
import einops
import equinox as eqx
from abc import ABC, abstractmethod
import diffrax
from jaxtyping import Array, PRNGKeyArray

################################################################################################################

class Polynomial(eqx.Module):

  coeff: Array
  deg: int = eqx.field(static=True)

  def __init__(self, coeff: Array):
    """
    The coefficients are expected to be in the order of increasing degree.
    p(x) = coeff[0] + coeff[1]*x + coeff[2]*x^2 + ...
    """
    assert coeff.ndim == 1
    self.coeff = coeff
    self.deg = self.coeff.shape[0]

  def get_area(self, start: float=0.0, end: float=1.0) -> Array:
    return self.moment_0(end) - self.moment_0(start)

  @staticmethod
  def from_points(x: Array,
                  y: Array,
                  deg: int) -> 'Polynomial':
    coeff = jnp.polyfit(x, y, deg)
    return Polynomial(coeff[::-1])

  def __call__(self, x: Array) -> Array:
    """
    Evaluate p(x)
    """
    return jnp.polyval(self.coeff[::-1], x)

  def get_moment(self, n: int) -> 'Polynomial':
    """
    \int x^n*p(x) dx
    """
    coeff = self.coeff/(n + 1 + jnp.arange(self.deg))
    coeff = jnp.pad(coeff, (n + 1, 0), mode='constant')
    return Polynomial(coeff)

################################################################################################################

if __name__ == '__main__':
  from debug import *

  key = random.PRNGKey(0)
  points = random.normal(key, (10, 2))
  points = points.at[:,0].set(jnp.sort(points[:,0]))

  p = Polynomial.from_points(points[:,0], points[:,1], 3)
  intxpdx = p.get_moment(0)
  intx2pdx = p.get_moment(1)

  t = jnp.linspace(-2, 2, 100)

  int1 = eqx.filter_vmap(p.moment_0())(t)
  int1_comp2 = eqx.filter_vmap(intxpdx)(t)

  int2 = eqx.filter_vmap(p.moment_1())(t)
  int2_comp2 = eqx.filter_vmap(intx2pdx)(t)

  import pdb; pdb.set_trace()