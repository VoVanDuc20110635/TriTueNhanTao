#%% Vi du 1
2**3

# %%
import math
from re import I 
math.sqrt(16)

# %% if, vi du 1
so = int(input('Nhap 1 so nguyen:'))
if so%2 == 0:
    print(so, 'la so chan.')
else:
    print(so, 'la so le.')

# %% if, vi du 2
diem = float(input('Nhap diem:'))
if diem>=8:
    print('Loai gioi.')
elif diem>=6.5 : # and diem<8
    print('Loai kha')
elif diem>=5.0 : # and diem<6.5
    print('Loai trung binh')
else:
    print('Loai kem')


# %% while, vi du 1
N = -1
while N<=0:
    N = int(input('Xin nhap so nguyen duong:'))

print(N)

# Tinh N!
giai_thua = 1
i = 1
while i<=N:
    giai_thua *= i 
    i += 1

print('N! =', giai_thua)

# %% list, vi du 1
list1  = [3, -5, 2, 8, 15]
list2 = ['An', 'Hoa', 'Thanh']
print(list1)
list3 = list1 + list2
print(list3)

# %% for, vi du 1
list1  = [3, -5, 2, -8, 15, 12, -3]
print('Phan tu am:')
for phan_tu in list1:
    if phan_tu<0:
        print(phan_tu)

print('Indices cua phan tu am')
for i in range(0,7,1): #[0,1,2,3,4,5,6]
    if list1[i] < 0:
        print(i)

# %% numpy, vi du 1
import numpy as np
arr1 = np.array([3, -5, 2, -8, 15, 12, -3])
print(arr1) 
np.abs(arr1)
np.sin(arr1)
np.random.randint(1,10)

# %% numpy, vi du 2: BMI (kg/m2) (19-25)
list_khoi_luong = [50, 62, 48, 57, 76]
list_chieu_cao = [1.6, 1.65, 1.55, 1.5, 1.8]
list_BMI = []
for i in range(0,len(list_khoi_luong)):
    bmi = list_khoi_luong[i]/list_chieu_cao[i]**2
    list_BMI.append(round(bmi,2))
print(list_BMI)
#list_khoi_luong / list_chieu_cao**2

arr_khoi_luong = np.array([50, 62, 48, 57, 76])
arr_chieu_cao = np.array([1.6, 1.65, 1.55, 1.5, 1.8])
arr_BMI = arr_khoi_luong / arr_chieu_cao**2
print(arr_BMI.round(2))

# %% numpy, vi du 3
x = np.arange(-5,6,1)
#x = [-5, -4, -3, -2, -1]
y = 5*x**2 - 2*x + 1
print(y)

# %% Functions, vi du 1
def DienTich(ban_kinh):
    '''
    Ham tinh dien tich hinh tron.
    Input: ban kinh 
    Output: dien tich
    '''
    import math 
    dien_tich = math.pi*ban_kinh**2
    return dien_tich

area = DienTich(5)
print(area)

# %%
def LocData(list_data, min_val=0):
    '''
    Ham tra ve nhung phan tu lon hon 1 nguong.
    Input: list du lieu list_data, nguong min_val
    Output: list cac phan tu trong list_data > min_val
    '''
    list_gia_tri = []
    list_id = []
    for i in range(0, len(list_data)):
        if list_data[i]>=min_val:
            list_gia_tri.append(list_data[i])
            list_id.append(i)
    return list_gia_tri, list_id

list1 = [5, -2, 16, -5, 7, -3, 4]
_, list_id = LocData(list1)
print(list_id)

# %% Lambda functions
import math
dien_tich = lambda ban_kinh : math.pi*ban_kinh**2
dien_tich(5)

dien_tich_hcn = lambda w, h: w*h 
dien_tich_hcn(4, 10)

# %%
