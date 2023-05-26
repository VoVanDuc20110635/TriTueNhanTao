#%% cau 1
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.pyplot as ppl
import numpy as np
import math
X = np.linspace(-2,2,100)
Y = np.linspace(-2,2,100)
x, y = np.meshgrid(X,Y)
z = x*math.e**(-x**2 - y**2)
fig = ppl.figure()
ax = fig.gca(projection='3d')
surf1 = ax.plot_surface(x,y,z, cmap = cm.hsv)
fig.colorbar(surf1)
ax.set_title("z(x,y) = x*e^(-x^2 - y^2)")
ppl.show()
# %% cau 4
import sympy as sp
x,u,v = sp.symbols("x,u,v")
eq1 = sp.Eq(5*x**2 + 6*x, 37)
eq2 = sp.Eq(2*x**3 - x, 0)
eq3 = sp.Eq(u*x**2 + v*x, 0)
print("5*x**2 + 6*x - 37 = 0 co nghiem: ", sp.solve(eq1,x))
print("2*x**3 - x = 0 co nghiem: ", sp.solve(eq2,x))
print("u*x**2 + v*x = 0 co nghiem: ", sp.solve(eq3,x))
print("u*x**2 + v*x = 0 co nghiem: ", sp.solve(eq3,u))
print("u*x**2 + v*x = 0 co nghiem: ", sp.solve(eq3,v))

# %% cau 6
import sympy as sp
import numpy as np
x,u,v = sp.symbols("x,u,v")
eq1 = sp.sin(u*x)*sp.cos(v*x)
dif = sp.diff(eq,x)
print("Phuong trinh ban dau: ",eq1)
print("Phuong trinh dao ham theo x: ",dif)
print("Phuong trinh dao ham bac 2 theo x: ",sp.diff(dif,x))
print("Phuong trinh dao ham theo u: ",sp.diff(eq1,u))

# %%
