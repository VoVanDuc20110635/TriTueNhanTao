#%% cau 1
import numpy as np
arr = np.array([-2, 6, 3, 10, 15, 48])
print(arr[2:5:2])
print(arr[1::2])
print(arr[3:5:1])
print(arr[-1:-4:-1])
# %% cau 2
import numpy as np
arr = np.array([[1,9,3],[4,5,6]])
print(arr.max())
print(arr.max(1))
print(arr.max(0))

# %% cau 3
def GiaiPhuongTrinh(bac, a, b, c = 0):
    if bac ==1:
        if a ==0:
            if b==0:
                print("Phuong trinh vo so nghiem")
            else:
                print("Phuong trinh vo nghiem")
        else:
            print("Phuong trinh co nghiem: ",-b/(a))
    else:
        if a ==0:
            if b ==0:
                if c ==0:
                    print("Phuong trinh vo so nghiem")
                else:
                    print("Phuong trinh vo nghiem")
            else:
                print("Phuong trinh co nghiem: ",-c/(b))
        else:
            delta = (b * b) - 4 * a* c
            if delta < 0:
                print("Phuong trinh vo nghiem")
            elif delta == 0:
                print("Phuong trinh co nghiem kep: ", -b/(2 * a))
            else:
                print("Phuong trinh co nghiem x1 = ", (-b - np.sqrt(delta))/(2 * a))
                print("Phuong trinh co nghiem x2 = ", (-b + np.sqrt(delta))/(2 * a))
bac = int(input("Nhap bac phuong trinh: "))
if bac==1:
    a = int(input("Nhap a: "))
    b = int(input("Nhap b: "))
    GiaiPhuongTrinh(bac,a,b)
else: 
    a = int(input("Nhap a: "))
    b = int(input("Nhap b: "))
    c = int(input("Nhap c: "))
    GiaiPhuongTrinh(bac,a,b,c)
# %% cau 5
import numpy
def SapXepTang(myList, giaTriBool = "True"):
    if giaTriBool == "True":
        for j in range(0, len(myList)):
            min = myList[j]
            mark = -1
            for i in range(j, len(myList)):
                if (min >= myList[i]):
                    min = myList[i]
                    mark = i
            temp = myList[mark]
            myList[mark] = myList[j]
            myList[j] = temp
    else:
        for j in range(-1, -len(myList)-1, -1):
            min = myList[j]
            mark = -1
            for i in range(j, -len(myList)-1, -1):
                if (min >= myList[i]):
                    min = myList[i]
                    mark = i
            temp = myList[mark]
            myList[mark] = myList[j]
            myList[j] = temp
    print(myList)
arr = numpy.array([3,6,4,1,9,6])
print(arr)
isTang = input("Nhap tang (True) hoac giam (False): ")
SapXepTang(arr,isTang)

# %%
