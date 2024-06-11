```py

### 1.1入门操作

* 绘制plt.plot(x,y)

* 坐标轴plt.xlabel('x')，plt.yabel('x')

* 显示plt.show()

* 查看样式plt.style.available

* 永久使用某个风格plt.style.use('_mpl-gallery')

* 临时使用

  ```python
  with plt.style.context('_mpl-gallery'):    
      plt.plot(x,y)
  ```

* 保存图片plt.savefig('myfiger.png')

  ```py
  import matplotlib.pyplot as plt
  x=[1,2,3,4]
  y=[1,4,6,9]
  plt.plot(x,y)
  plt.xlabel('x')
  plt.ylabel('squ')
  plt.show()
  #查看样式
  print(plt.style.available[:5])
  #永久使用某个风格
  plt.style.use('_mpl-gallery')
  #临时使用
  with plt.style.context('_mpl-gallery'):
      plt.plot(x,y)
  #保存图片
  plt.savefig('myfiger.png')
  ```

  

### 1.2折线图

* ```py
  import matplotlib.pyplot as plt
  import numpy as np
  x=np.linspace(0,2*np.pi,100)
  plt.plot(x,np.sin(x))
  plt.show()
  ```

  <img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1663654245241.png" alt="1663654245241" style="zoom: 80%;" />

* 绘制多条

  ```py
  x=np.linspace(0,2*np.pi,100)
  plt.plot(x,np.sin(x))
  plt.plot(x,np.cos(x))
  plt.show()
  ```

  <img src="C:\Users\lenovo\AppData\Roaming\Typora\typora-user-images\1663654392791.png" alt="1663654392791" style="zoom:80%;" />

