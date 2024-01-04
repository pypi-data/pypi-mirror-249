import jax
import jax.numpy as jnp
from jax import random
import equinox as eqx
import diffrax

key = random.PRNGKey(0)

dim = 4
vf = eqx.nn.MLP(in_size=dim,
              out_size=dim,
              width_size=16,
              depth=3,
              key=key)

# x is an array of points and v are tangent vectors at x
x, v = random.normal(key, (2, 10, dim))

#####################################
# Regular way to do JVPs
#####################################

def f(t, carry, inputs):
  x = carry
  return eqx.filter_vmap(vf)(x)

def F(x):
  solution = diffrax.diffeqsolve(diffrax.ODETerm(f),
                                  diffrax.Tsit5(),
                                  t0=0.0,
                                  t1=1.0,
                                  dt0=0.001,
                                  y0=x,
                                  args=(),
                                  adjoint=diffrax.DirectAdjoint())
  outs = solution.ys
  return jax.tree_util.tree_map(lambda x: x[0], outs)

Fx, dFv = jax.jvp(F, (x,), (v,))

#####################################
# JVPs by augmenting the ODE
#####################################

def f(t, carry, inputs):
  x, v = carry
  dxdt, dvdt = jax.jvp(eqx.filter_vmap(vf), (x,), (v,))
  return dxdt, dvdt

x, v = random.normal(key, (2, 10, dim))

def F_jvp(x, v):
  solution = diffrax.diffeqsolve(diffrax.ODETerm(f),
                                diffrax.Tsit5(),
                                t0=0.0,
                                t1=1.0,
                                dt0=0.001,
                                y0=(x, v),
                                args=(),
                                adjoint=diffrax.RecursiveCheckpointAdjoint())
  outs = solution.ys
  return jax.tree_util.tree_map(lambda x: x[0], outs)

Fx2, dFv2 = F_jvp(x, v)

assert jnp.allclose(Fx, Fx2)
assert jnp.allclose(dFv, dFv2)
