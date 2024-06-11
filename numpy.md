# numpy学习

* 一个开源的python的科学计算库
* 使用Numpy可以方便数组、矩阵使用计算

### 1.1 数组常用API

* np.array

  ```python
  import numpy as np
  list=[1,2,3,4,5]
  array_list=np.array(list)
  print(array_list)
  type(array_list)
  console:
      [1 2 3 4 5]
      <class 'numpy.ndarray'>
  ```
  * 数组.dtype   类型

  * 数组.itemsize

  * 数组.shape  维度

  * 数组.size    大小

    ```py
    import numpy as np
    list=[1,2,3,4,5]
    array_list=np.array(list)
    print(array_list)
    print(type(array_list))
    print(array_list.dtype)
    print(array_list.shape)
    print(array_list.size)
    print(array_list.ndim)
    console
    [1 2 3 4 5]
    <class 'numpy.ndarray'>
    int32
    (5,)
    5
    1
    ```

    

* 数组.fill(a)赋值为a

* 索引与切片

  ```py
  print(array_list[0])
  print(array_list[1:3])
  comsole
  
  1
  [2 3]
  ```

  

* 矩阵格式，多维度     每一行都取到，用：

  ```py
  import numpy as np
  array_list=np.array([[1,2,3],                      
                      [4,5,6],
                      [7,8,9]])
  print(array_list)
  print(array_list.shape)
  print(array_list.size)
  print(array_list.ndim)
  #矩阵取值
  print(array_list[1,2])
  #赋值
  array_list[1,2]=6
  #取一行
  print(array_list[1])
  #取一列
  print(array_list[:,1])
  print(array_list[:,0:2])// 取0列和第二列
  [[1 2 3]
   [4 5 6]
   [7 8 9]]
  (3, 3)
  9
  2
  6
  [4 5 6]
  [2 5 8]
  [[1 2]
   [4 5]
   [7 8]]
  
  ```

* 数组是指针，如果直接等于则使用同一个地址。如果避免使用array.copy()

* 构造等差数列 np.arange(开始，结束，步长)

  ```python
  print(np.arange(0,100,10))
  [ 0 10 20 30 40 50 60 70 80 90]
  ```

  

* 随意选择数组值，使用布尔值当索引

  ```py
  import numpy as np
  array_list=np.arange(0,40,10)
  mask=np.array([0,0,1,1],dtype=bool)
  print(array_list[mask])
  
  console:
  [20 30]
  ```

* 使用np.where查看大于某个数在哪个位置

  ```py
  print(array_list>=20)
  print(np.where(array_list>=20))
  
  console
  [False False  True  True]
  (array([2, 3], dtype=int64),)
  ```

### 1.2 数组类型

* ```python
  import numpy as np
  array_list=np.array([1,2,3,4,5],dtype=float)
  array_list=np.array([1,2,3,4,5],dtype=np.float)
  array_list=np.array([1,2,3,4,5],dtype=np.object)#支持各种结构
  ```

* 重新给个类型

  ```py
  np.asarray(array_list,float)
  ```

  

### 1.3 数值计算

* 求总和np.sum，可以选择一个维度，axis=0按列求和，1按行，-1最后一个维度

  ```py
  import numpy as np
  array_list=np.array([[1,2,3],[4,5,6]])
  print(np.sum(array_list))
  print(np.sum(array_list,axis=0))
  print(np.sum(array_list,axis=1))
  
  21
  [5 7 9]
  [ 6 15]
  ```

  

* 乘积

  ```py
  import numpy as np
  array_list=np.array([[1,2,3],[4,5,6]])
  print(np.prod(array_list))
  print(np.prod(array_list,axis=0))
  print(np.prod(array_list,axis=1))
  
  720
  [ 4 10 18]
  [  6 120]
  ```

* 最大最小max，最大最小索引值argmin, argmax
* 求均值 np.mean
* 标准差 np.std
* 方差np.var
* 限制 np.clip，如array.clip(2,4)大于4的值都是4，小于2都是2
* 四舍五入 array.round(decimals=),np.round，设置精度

### 1.4 排序操作

* np.lexsort

  ```py
  #排序函数,按照第一列进行升序，第三列进行降序
  ar3=np.array([[1,0,6],[1,7,0],[2,3,1],[2,4,0]])
  index=np.lexsort([-1*ar3[:,0],ar3[:,2]])
  print(ar3[index])
  
  [[2 4 0]
   [1 7 0]
   [2 3 1]
   [1 0 6]]
  
  ```

* np.linspace(0,10,10)#0-10之间平均选取十个数

* 数组维度  array.reshape

* 转置np.transpose

* 去掉空轴np.square()

* 新增维度np.newaxis

  ```py
  import numpy as np
  arra=np.array(10)
  print(arra.shape)
  arra.shape=2,5#给他变成两行五列
  print(arra)
  #方法二
  arra.reshape(1,10)
  #新增一轴
  arra=arra[np.newaxis,:]
  #新增两个维度
  arra=arra[np.newaxis,np.newaxis,:]
  #去掉空轴
  np.square()
  #转置
  np.transpose
  ```

  

* 数组的连接np.concatenate，可以指定维度

  ```py
  import numpy as np
  arra=np.array([[1,2,3],[4,5,6]])
  arra2=np.array([[4,5,6],[3,2,1]])
  #必须采用元组的形式
  print(np.concatenate((arra,arra2)))
  print(np.vstack((arra,arra2)))#相当于轴在0
  print(np.hstack((arra,arra2)))#相当于轴在1
  #拉平成一维
  print(arra.flatten())
  
  #拉平方法2
  arra.ravel()
  ```

### 1.4数组的生成

* np.arange

  ```py
  import numpy as np
  print(np.arange(0,20,2))
  
  [ 0  2  4  6  8 10 12 14 16 18]
  
  ```

  

* np.linspace (开始，结尾，个数)等距离分布

* np.logspace

  ```py
  import numpy as np
  arra=np.arange(10)
  print(np.arange(2,20,2))
  print(np.arange(2,20,2))
  print(np.linspace(0,10,50))
  print(np.logspace(0,10,10))#默认以10为底
  
  [ 2  4  6  8 10 12 14 16 18]
  [ 2  4  6  8 10 12 14 16 18]
  [ 0.          0.20408163  0.40816327  0.6122449   0.81632653  1.02040816
    1.2244898   1.42857143  1.63265306  1.83673469  2.04081633  2.24489796
    2.44897959  2.65306122  2.85714286  3.06122449  3.26530612  3.46938776
    3.67346939  3.87755102  4.08163265  4.28571429  4.48979592  4.69387755
    4.89795918  5.10204082  5.30612245  5.51020408  5.71428571  5.91836735
    6.12244898  6.32653061  6.53061224  6.73469388  6.93877551  7.14285714
    7.34693878  7.55102041  7.75510204  7.95918367  8.16326531  8.36734694
    8.57142857  8.7755102   8.97959184  9.18367347  9.3877551   9.59183673
    9.79591837 10.        ]
  [1.00000000e+00 1.29154967e+01 1.66810054e+02 2.15443469e+03
   2.78255940e+04 3.59381366e+05 4.64158883e+06 5.99484250e+07
   7.74263683e+08 1.00000000e+10]
  ```

* 查看帮助文档 help(方法)

* 构造网格，即二维。x,y=np.meshgrid(arra,arra)

* np.r_构造行向量

* np.c_构造列向量

  ```py
  print(np.r_[0:10:1])#行向量
  print(np.c_[0:10:1])#列向量
  [0 1 2 3 4 5 6 7 8 9]
  [[0]
   [1]
   [2]
   [3]
   [4]
   [5]
   [6]
   [7]
   [8]
   [9]]
  ```

  

* 构造全零或全1的矩阵,np.zeros,np.ones,

  ```py
  print(np.zeros(3))
  print(np.zeros((3,3)))
  print(np.ones(3))
  #构造为8的矩阵
  print(np.ones(3))*8
  [0. 0. 0.]
  [[0. 0. 0.]
   [0. 0. 0.]
   [0. 0. 0.]]
  [1. 1. 1.]
  
  ```

*  np.empty随机生成一个矩阵

* 填充 np.fill

* 生成单位矩阵np.identity(行列)

  ```py
  print(np.identity(5))
  [[1. 0. 0. 0. 0.]
   [0. 1. 0. 0. 0.]
   [0. 0. 1. 0. 0.]
   [0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 1.]]
  ```

  

### 1.5四则运算与随机生成

```py
x=np.array([5,5])
y=np.array([5,5])
z=np.array([[5],[5]])
#点乘
print(np.multiply(x,y))
#相乘
print(np.dot(x,z))

[25 25]
[50]
```

* np.random构造随机的浮点数

* np.random.randint构造int的随机数，左闭右开

* np.random.random_sample()生成0-1

* np.random.randint(0,10,3)在0-10中取三个数

* np.random.normal(mu,sigma,10)高斯分布，一个均值一个标准差

* np.set_printoptions(precision=3)精度设置

* np.random.shuffle(x)打乱顺序，重新洗牌

* np.random.seed(0)随机种子，防止每次生成不一样，下面生成就是一样的

  ```PY
  import numpy as np
  print(np.arange(0,20,2))
  print(np.identity(5))
  #构造随机的浮点数
  print(np.random.rand(3,2))
  #构造int的随机数，左闭右开
  print(np.random.randint(10,size=(5,4)))
  #生成0-1
  print(np.random.random_sample())
  #在0-10中取三个数
  print(np.random.randint(0,10,3))
  #高斯分布，一个均值一个标准差
  mu ,sigma=0,0.1
  print(np.random.normal(mu,sigma,10))
  
  #精度设置
  np.set_printoptions(precision=3)
  
  #打乱顺序，重新洗牌
  x=np.arange(10)
  print(np.random.shuffle(x))
  
  #随机种子，防止每次生成不一样，下面生成就是一样的
  np.random.seed(0)
  
  
  [ 0  2  4  6  8 10 12 14 16 18]
  [[1. 0. 0. 0. 0.]
   [0. 1. 0. 0. 0.]
   [0. 0. 1. 0. 0.]
   [0. 0. 0. 1. 0.]
   [0. 0. 0. 0. 1.]]
  [[0.23822367 0.29114883]
   [0.1323263  0.11557916]
   [0.61503079 0.82140204]]
  [[0 0 3 4]
   [8 0 8 2]
   [0 5 7 1]
   [5 6 5 9]
   [4 1 8 6]]
  0.4744755364532415
  [5 4 7]
  [-0.02822102  0.1351528  -0.13620004 -0.05116635  0.12549979  0.01083219
   -0.01201235 -0.04266113 -0.10190628 -0.01876089]
  None
  ```

### 1.6文件操作

* 读取数据np.loadtxt
* 保存数据

