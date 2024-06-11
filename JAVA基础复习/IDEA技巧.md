##### IDEA技巧

* 更换添加jdk

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691294995221.png" alt="1691294995221" style="zoom: 50%;" />

* 选择jdk，限制使用版本的新特性(限制1.8就不能使用超过1.8的新特性)，编译之后的输出路径

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295138914.png" alt="1691295138914" style="zoom:50%;" />

* Toolbar

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295211225.png" alt="1691295211225" style="zoom:50%;" />

<img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295229890.png" alt="1691295229890" style="zoom:50%;" />

* 启动自动打开最后一个工程

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295355466.png" alt="1691295355466" style="zoom:50%;" />

* 检查更新

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295418304.png" alt="1691295418304" style="zoom:50%;" />

* 设置背景，主题，颜色，字体，大小

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295532073.png" alt="1691295532073" style="zoom:50%;" />

* 设置代码字体大小

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295659863.png" alt="1691295659863" style="zoom:50%;" />

* 多行注释快捷键 ctrl+shift+/，修改注释的颜色

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691295783779.png" alt="1691295783779" style="zoom:50%;" />



* 代码提示不区分大小写Match case:

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691296262932.png" alt="1691296262932" style="zoom:50%;" />

* 自动导包 add 和optimize打钩

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691296364024.png" alt="1691296364024" style="zoom:50%;" />

* 改文件字编码方式，一般用utf8，世界语通用，中国用的是GBK

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691296911606.png" alt="1691296911606" style="zoom:50%;" />

* 修改文件头的注释

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691297732305.png" alt="1691297732305" style="zoom:50%;" />



* 设置自动编译，勾选build和compile

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691297812089.png" alt="1691297812089" style="zoom:50%;" />

* 快速重启，清除缓存

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691297984189.png" alt="1691297984189" style="zoom:50%;" />

* 取消双加搜索

  <img src="IDEA%E6%8A%80%E5%B7%A7.assets/1691298040410.png" alt="1691298040410" style="zoom:50%;" />

##### 快捷键

* 多行注释快捷键 ctrl+shift+/
* psvm
* sout
* foreach
* 导包alt+enter
* ctrl+alt+左箭头回到上一次光标的位置
* ctrl+alt+t选择包裹的方法
* ctrl+shift+/格式化注释
* ctrl+p查看方法参数
* alt+shift+上下 上下移动光标选中的代码
* alt+insert构造器快捷键
* shift+enter向下一行生成空行
* ctrl+alt+enter向上生成空行
* ctrl+alt+u生成类继承树
* ctrl+alt+enter在上一行输入代码
* ctrl+h查看继承树
* ctrl+n搜索类
* ctrl+f12查看类的所有方法
* ctrl+h放在一个类上，查看所有的继承关系
* ctrl+alt+l快速格式化
* 模板：再设置，editor,live Templates
* 遍历数组变量，直接变量.for
* 打印一个变量，直接变量.sout
* 删除一行 ctrl+y
* 退出窗口 esc
* 创建文件alt +insert
* 切换打开的不同文件 alt+左右箭头
* 运行 ctrl+shift+f10
* 窗口 alt+数字





###### 工程与模块管理

* 工程---模块---包---类



#### windows

* tab可以自动补全
* cd \回到根目录
* alt+tab切换应用
* win+d切换到左面
* win+l 锁屏

###### 调试

* Show Execution Point：如果光标在其它页面，点这个按钮回到当前代码运行的地方
* Step Over：步过，一行一行地往下走，如果这一行上有方法不会进入方法，源码也是只走下一行，不会从源码跑到自己写的代码里。
* Step Into：步入，如果当前行有方法，可以进入方法内部，一般用于进入自定义方法内，不会进入官方类库的方法
* Force Step Into：强制步入，能进入任何方法，查看底层源码的时候可以用这个进入官方类库的方法
* Step Out：步出，从步入的方法内退出到方法调用处，此时方法已执行完毕，只是还没有完成赋值
* Drop Frame：回退到上一个断点
* Run to Cursor：运行到光标处，你可以将光标定位到你需要查看的那一行，然后使用这个功能，代码会运行至光标行，而不需要打断点
* Evaluate Expression：计算表达式，这个表达式不仅可以是一般变量或参数，也可以是方法，当你的一行代码中调用了几个方法时，就可以通过这种方式查看查看某个方法的返回值；也可以改变变量的值，这样就能灵活赋值
  