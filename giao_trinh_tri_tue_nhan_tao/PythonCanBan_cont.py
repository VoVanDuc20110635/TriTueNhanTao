#%% matplotlib, example 1
import matplotlib
from matplotlib.lines import _LineStyle
import matplotlib.pyplot as plt
import numpy as np 
x = np.array([1, 3, 4, 5, 3])
y = np.array([1, 2, 2, 4, 2])
plt.plot(x,y)

x = np.array([1, 3])
y = np.array([2,3])
plt.plot(x,y)

plt.show()

#%% matplotlib, example 2
x = np.arange(-5,4,0.1)
y = 2*x**2 + 3*x + 6 
plt.plot(x,y, color='g', linewidth=4)

y = 5*x**3 + 2*x**2 + 3*x + 6 
plt.plot(x,y, color='r', linestyle='--')

plt.axis([-5, 4, -20, 60])
plt.legend(['Ham bac 2', 'Ham bac 3'])
plt.title('Polynomial functions')
plt.xlabel('Time')
plt.ylabel('No. of connections')
plt.grid()
plt.show()

#%% matplotlib, example 3
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm, projections 

X = np.linspace(-1, 1, 50)
Y = np.linspace(-1, 1, 50)
X, Y = np.meshgrid(X, Y)
#Z = 7*np.ones(X.shape)
#Z = -X**2 + -Y**2 
Z = -X**3 + -Y**3

# pip install pyqt5
%matplotlib qt 
fig = plt.figure()
ax = fig.gca(projection='3d')
surf1 = ax.plot_surface(X, Y, Z,
    #rcount=10, ccount=10,
    cmap = cm.jet)

fig.colorbar(surf1)
ax.set_xlabel('Ox')
ax.set_ylabel('Oy')
ax.set_zlabel('Oz')
ax.set_title('Test 3D plot')

plt.show()

# %% OOP in Python
class Car:
    def __init__(self, brand, type, year, color):
        self.brand = brand
        self.type = type
        self.year = year 
        self.color = color 
        self.started = False 

    def StartEngine(self, key):
        if key == '123':
            print('Engine started.')
            self.started = True
        else:
            print('Wrong key!')

    def AutoDrive(self):
        if self.started: 
            print('AutoDrive mode activated.')
        else:
            print('Please start the engine first!')

car1 = Car('Toyota', 'Sedan', 2020, 'white')
car1.StartEngine('123')
car1.AutoDrive()
print(car1.color)

car2 = Car('Ford', 'SUV', 2021, 'black')
car2.StartEngine('123')
car2.AutoDrive()
print(car2.brand)

# %%
class ElectricCar(Car):
    def __init__(self, brand, type, year, color):
        Car.__init__(self,brand, type, year, color)
        self.type = type + '_electric'

    def Charge(self):
        print('Charging...')

    def AutoDrive(self):
        print('New autodrive mode activated.')

car3 = ElectricCar('Vinfast', 'Sedan', 2022, 'navy blue')
car3.StartEngine('123')
car3.AutoDrive()
car3.Charge()
car3.type 

# %%
