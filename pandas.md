## pandas

### 1.1入门

* ```py
  import pandas as pd
  df=pd.read_csv('train.csv')
  print(df)
  #获取执行前几条数据
  df.head(10)#获取前十条，不写默认五条
  
  #获取信息
  df.info
  #获取列名
  print(df.columns)
  
  #查看类型
  print(df.dtypes)
  
  #查看数值
  print(df.values)
  
  #拿指定的数据列
  print(df['Age'])
  ```

* df.describe()统计分析

  ```py
  print(df.describe())
  
  count   891.000000  891.000000  891.000000  ...  891.000000  891.000000  891.000000
  mean    446.000000    0.383838    2.308642  ...    0.523008    0.381594   32.204208
  std     257.353842    0.486592    0.836071  ...    1.102743    0.806057   49.693429
  min       1.000000    0.000000    1.000000  ...    0.000000    0.000000    0.000000
  25%     223.500000    0.000000    2.000000  ...    0.000000    0.000000    7.910400
  50%     446.000000    0.000000    3.000000  ...    0.000000    0.000000   14.454200
  75%     668.500000    1.000000    3.000000  ...    1.000000    0.000000   31.000000
  max     891.000000    1.000000    3.000000  ...    8.000000    6.000000  512.329200
  ```

### 1.2索引

* 定位到某一列df['Age']

* 定位两列print(df[['Age','Fare']])

* 获取具体一行数据，需要loc用lable来定位,iloc用位置定位print(df.iloc[0])

  * 拿0-5

* 设置索引df.set_index('Name')

* 修改数据df.loc['Allen, Mr. William Henry','Fare']=1000

* pd.DataFrame

  ```py
  df=pd.DataFrame({'key':['a','b','c','a'],'value':[0,5,10,15]})
  print(df)
  
    key  value
  0   a      0
  1   b      5
  2   c     10
  3   a     15
  ```

  

* 计算a,b,c的value

  * ```py\
    #方法1
    for key in {'a','b','c'}:
        print(key,df[df['key']==key].sum())
    ```

  * ```py
    #方法2
    print(df.groupby('key').sum())
    ```

  * ```py
    print(df.groupby('key').aggregate(np.sum))
    ```

* 求男女年龄平均值

  ```py
  print(df.groupby('Sex')['Age'].mean())
  
  Sex
  female    27.915709
  male      30.726645
  ```

  

* 求幸存可能性

  ```py
  print(df.groupby('Survived').mean())
  
  Survived                                                                 
  0          447.016393  2.531876  30.626179  0.553734  0.329690  22.117887
  1          444.368421  1.950292  28.343690  0.473684  0.464912  48.395408
  ```

### 1.3数值运算

* 求和默认按列

  ```py
  print(df.sum())
  ```

* 按行求和df.sum(axis=1)

* df.sum(axis='columns')指定具体的轴

* 数值运算操作

  ```py
  print(df.mean(axis=1))
  print(df.min())
  print(df.max())
  #均值
  print(df.median())
  
  ```

* 二元统计

  ```py
  #协方差
  print(df.cov())
  #相关系数
  print(df.corr())
  #统计不同年龄段人数
  print(df['Age'].value_counts)
  #升序
  df['Age'].value_counts(ascending=True)
  #分为几组bins
  df['Age'].value_counts(ascending=True,bins=5)
  
  #计算整体
  df['Age'].count()
  ```

  