# Tensorflow学习

## 1. 基础知识

### 1.1结构分析

* Tensorflow通常被分为构建图阶段和执行图阶段。
* 在构建阶段，数据和执行步骤被描述成一张图。
* 执行阶段，使用会话执行构建好的图中操作。
* 张量，tensorflow中最基本的数据对象，可以理解为数组。
* 结点：提供图当中的执行操作。
* 图和会话：图是tensorflow将计算表示为指令之间的一种依赖关系的表示方法。会话是运行数据流图的机制。

### 1.2 图的基本使用

* 图包含了一组tf.operation的代表的计算单元对象和tf.tensor代表的计算单元之间的流动数据。

* 相关操作

  * 通常tf会创建一个默认图

    ```py
    #获取默认图
    g=tf.get_default_graph()
    ```

  * 创建图

    ```py
    tf.Graph
    ```

    

### 数据类型

* tf.int32,tf.float32,tf.float 64
* tf.bool
* tf.string

#### 1.1.2张量

* 创建张量 tf.constant( 张量内容，dtype=数据类型（可选）)

* 举例  

  ```py
  import tensorflow as tf
  a=tf.constant([1,5],dtype=tf.int64)
  print(a)
  print(a.dtype)
  print(a.shape)#逗号隔开了几个数字说明是几维的，数字表示有几个元素
  ```
  
* 数据类型与形状

  ```py
  import tensorflow as tf
  con_a=tf.constant(3.0)#0维
  con_b=tf.constant([1,2,3,4])#1维
  con_c=tf.constant([[1,2],[3,4]])#2维
  con_c=tf.constant([[[1,2],[3,4]],[[5,6],[7,8]]])#3维
  print(con_a.shape,con_b.shape,con_c.shape)
  ```

* 常用创建

  * tf.ones([2,4])
  * tf.random.normal([3.4],mean=2,stddev=1)#均值，标准差

* 类型转换tf.cast(oine,tf.int32)

* 形状改变

  * 静态形状，不能跨阶数改变形状，已经固定的不能再改变tf.setshape

    ```py
    #定义占位符
    a=tf.compat.v1.placeholder(dtype=tf.float32,shape=[None,None])#两个维度都不确定
    b=tf.compat.v1.placeholder(dtype=tf.float32,shape=[None,10])#第二个维度为10
    c=tf.compat.v1.placeholder(dtype=tf.float32,shape=[2,3])
    a.set_shape([5,6])#以后都不能修改
    ```

    

  * 动态形状，相当于创建一个新的张量tf.reshape(a,[2,3])

#### 1.1.3 常用函数

* tf.cast（张量名，dtype=数据类型）#强制转换数据类型

* tf.reduce_min（张量名）计算张量维度上元素的最小值

* tf.reduce_max(张量名)

* 理解axis，指定操作哪个维度，在二维中，0为行，1为列

  * tf.reduce_mean(张量名，axis=操作轴)   求指定维度的平均值
  * tf.reduce_sum（张量名，axis=操作轴）计算张量沿着指定维度的和

* tf.Variable（）将变量标记为可训练的，被标记的变量会在反向传播中记录梯度信息，常用于训练参数。

  ```py
  w=tf.Variable(tf.random.normal([2,2],mean=0,stssev=1))
  #随机值生成正态分布随机数，标记为可训练。
  ```

* 四则运算：tf.add,tf.subtract,tf.multiply,tf.divide     只有维度相同的张量才能做四则运算。
* 平方、次方、开方:tf.square,tf.pow,tf.sqrt
* 矩阵乘 tf.matmul

* tf.where（）条件语句真返回A，反之返回B

  ```py
  a=tf.constant([1,2,3,1,1])
  b=tf.constant([0,1,3,4,5])
  c=tf.where(tf.greater(a,b),a,b)
  print(c)
  
  console
  tf.Tensor([1 2 3 4 5], shape=(5,), dtype=int32)
  ```

* np.random.RandomState.rand(维度) 返回一个[0,1)之间的随机数。

  ```python
  import numpy as np
  rdm=np.random.RandomState(seed=1)#种子，使每次生成随机数相同
  a=rdm.rand()#返回一个随机标量
  b=rdm.rand(2,3)#返回一个维度为两行三列随机数矩阵
  print(a)
  print(b)
  
  console:
      0.417022004702574
  [[7.20324493e-01 1.14374817e-04 3.02332573e-01]
   [1.46755891e-01 9.23385948e-02 1.86260211e-01]]
  ```

* np.vstack(数组1，数组2) 将两个数组垂直方向叠加

  ```python
  a=np.array([1,2,3])
  b=np.array([4,5,6])
  c=np.vstack((a,b))
  print(c)
  
  comsole:
      [[1 2 3]
   [4 5 6]]
  ```

* np.mgrid[起始值：结束值：步长，起始值：结束值：步长，.........]  生成网格坐标点

* x.ravel() 将x变为1维数组

* np.c_[]使返回的间隔数值点配对

  ```python
  x,y=np.mgrid[1:3:1,2:4:0.5]
  print(x)
  print(y)
  
  console:
      x= [[1. 1. 1. 1.]
   [2. 2. 2. 2.]]
  y= [[2.  2.5 3.  3.5]
   [2.  2.5 3.  3.5]]
  ```

* tf.data.Dataset.from_tensor_slices(（features,lables）)标签和特征对应

  ```
  features=tf.constant([12,23,10,17])
  lables=tf.constant([0,1,1,0])
  dataset=tf.data.Dataset.from_tensor_slices((features,lables))
  ```

* tf.GradientTape  实现某个函数对指定参数的求导运算。

  ```py
  with tf.GradientTape() as tape:
      w=tf.Variable(tf.constant(3.0))
      loss=tf.pow(w,2)
      grad=tape.gradient(loss,w)
      print(grad)
  
  console:
  tf.Tensor(6.0, shape=(), dtype=float32)
  ```

* enumerate 是python的内建函数，可遍历每个元素（如列表、元组或者字符串），组合为==索引  元素==，常在for循环中使用

  ```py
  sq=['1','2','3']
  for i,ele in enumerate(sq):
      print(i,ele)
      
  console:
  0 1
  1 2
  2 3
  ```

  

* tf.one_hot(带转换的数据，depth=几分类)  独热编码：在分类问题中，常用于独热编码做标签，标记类别 1是  0非

  ```py
  classes=3  #三分类
  lables=tf.constant([1,0,2])  #最小值为0，最大值为2
  output=tf.one_hot(lables,depth=classes)
  print(output)
  
  console:
  tf.Tensor(
  [[0. 1. 0.]
   [1. 0. 0.]
   [0. 0. 1.]], shape=(3, 3), dtype=float32)
  
  ```

  

* tf.nn.softmax  使输出值转换成符合的概率分布

* assign_sub（）赋值操作，更新参数的值并返回。调用assign_sub前，先用tf.Variable定义变量w为可训练

  ```python
  ww=tf.Variable(4)  #进行ww=ww-1
  w.assign_sub(1)
  print(w)
  
  console
  <tf.Variable 'Variable:0' shape=() dtype=int32, numpy=3>
  ```

* tf.argmax  返回张量沿指定维度最大值的索引，0行1列

  ```py
  test=np.array([[1,2,3],[2,3,4],[5,4,3]])
  print(test)
  print(tf.argmax(test,axis=0))
  print(tf.argmax(test,axis=1))
  
  
  tf.Tensor([2 2 1], shape=(3,), dtype=int64)
  tf.Tensor([2 2 0], shape=(3,), dtype=int64)
  ```

####1.1.4 训练样本的导入

import tensorflow as tf      import numpy as np

* 常见的激活函数
  * sigmoid   tf.nn.sigmoid(x)
  * Tanh   tf.math.tanh(x)
  * Relu   tf.nn.relu(x)
  * Leaky Relu(x) tf.nn.leaky_relu(x)
* 损失函数
  * 均方误差：lose_mse=tf.reduce_mean(tf.square(y_-y))
  * 交叉熵损失函数：tf.losses.categorical_crossentropy(y_,y)
* 欠拟合
  * 增加输入特征项
  * 增加网络参数
  * 减少正则化参数，一般不正则化b，弱化训练数据的噪声
    * L1正则化  通过稀疏参数，减少参数的数量，降低复杂度
    * L2正则化   tf.nn.l2_loss(w1) 通过减少参数值的大小降低复杂度
* 过拟合
  * 数据清洗
  * 增大训练集
  * 采用正则化
  * 增大正则化参数

### 1.2变量

* 必须要初始化，创建变量con_a=tf.Variable(initial_value=30)#定义变量，给一个初始化值

  ```py
  import tensorflow as tf
  con_a=tf.Variable(initial_value=30)#定义变量，给一个初始化值
  con_b=tf.Variable(initial_value=20)#定义变量，给一个初始化值
  sum=tf.add(con_b,con_a)
  #初始化变量
  init=tf.compat.v1.global_variables_initializer()
  with tf.compat.v1.Session as sess:
      sess.run(init)
  ```

  

* 增加变量的命名空间tf.compat.v1.variable_scope("name")

