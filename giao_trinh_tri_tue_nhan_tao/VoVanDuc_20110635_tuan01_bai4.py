# %% cau 4a
a = []
max = -9999999
for i in range(0,4,1):
    b = float(input("Nhap so: "))
    a.append(b)
    if a[i] > max:
        max = a[i]
print("so lon nhat: ")
print(max)
# %% cau 4b
a = float(input("Nhap a: "))
b = float(input("Nhap b: "))
#ax +b = 0
if a==0:
    if b==0:
        print("Phuong trinh vo so nghiem!")
    else:
        print("Phuong trinh vo nghiem!")
else:
    print("Phuong trinh co nghiem = ",-b/a)
    
