#### HTTP协议

* 缓存机制，目前接触到的
  * 堆内存当中的字符串常量池。
     "abs." 先在字符串常量池中查找，如果有，直接拿来用。如果没有则新建，然后再放入字符串常量池。
  * 堆内存当中的整数型常量池。
    [-128~127]一共256个Integer类型的引用，放在整数型常量池中。没有超出这个范围的话，直接从常量池中取。
  * 线程池
    * tomcat本身支持多线程
    * Tormcat服务器是在用户发送一次清求。就新建—个Thread连程对像吗?
      * 当然不是。实际上是在Tomcat服务醺启坳修时候，会先创建好N多个钰程Thread对象，然后将线程对象放到舂合当中。称为线程池。用户发送清求过来之后，需要有一个对症的连程来处理这个清求。这个时候红程对象就会直油从牒程池中拿,效本比校高。
    * 所有的wEB服务器。或者应用服务器，都是变持多线程的，都有连程池肌制
  * 连接池：JVM是一个进程。MySQL数据库是一个进程。进程和进程之间建立连接，打开通道是很费劲的。是很耗费资源的。怎么办?可以提前先创建好N个Connection连接对象，将连接对象放到一个集合当中，我们把这个放有Connection对象的集合称为连接池。每一次用户连接的时候不需要再新建连接对象，省去了新建的环节，直接从连接池中获取连接对象，大大提升访问效率。
  * redis
  * 像ServletContext存储数据



* HTTP的请求协议
  *  HTTP的请求协议包括:4部分
    * 请求行
    * 请求头
    * 空白行
    * 请求体
  * HTTP的响应协议包括:4部分
    * 状态行
    * 响应头
    * 空白行
    * 响应体
* GET请求是安全的，为什么?因为GET请求只是为了从服务器上获取数据。POST请求是危险的。为什么?因为POST请求是向服务器提交数据，如果这些数据通过后门的方式进入到服务器当中，服务器是很危险的。另外post是为了提交数据，所以一股情况下拦截请求时候。大部分会选择拦截(监听) post请求。
* GET请求支持缓存，浏览器会缓存。任何一个GET请求响应结果都会被浏览器缓存。POST请求不支持缓存。如果GET请求不想被缓存，在路径后面加个每时每刻都在变化的时间参数，即时间戳。
* GET请求有大小限制，POST没有





##### 模板方法设计模式

* 下面这两个，一个为Student，一个为Teacher，描述一天的生活。

  ```java
  /**
   * ClassName:Student
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/21 10:43
   * @Version 1.0
   */
  public class Student {
      /*
      描述学生的一天
       */
      public void day(){
          qiChuang();
          xishu();
          breakfast();
          study();
          dinner();
          sleep();
      }
      public void qiChuang(){
          System.out.println("起床");
      }
      public void xishu(){
          System.out.println("洗漱");
      }
      public void breakfast(){
          System.out.println("吃早餐");
      }
      public void study(){
          System.out.println("学习");
      }
      public void dinner(){
          System.out.println("晚饭");
      }
      public void sleep(){
          System.out.println("睡觉");
      }
  
  }
  
  ```

  ```java
  /**
   * ClassName:Teacher
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/21 10:45
   * @Version 1.0
   */
  public class Teacher {
      /*
     描述老师的一天，存在问题，算法没有重复使用，代码没有复用
      */
      public void day(){
          qiChuang();
          xishu();
          breakfast();
          study();
          dinner();
          sleep();
      }
      public void qiChuang(){
          System.out.println("起床");
      }
      public void xishu(){
          System.out.println("洗漱");
      }
      public void breakfast(){
          System.out.println("吃早餐");
      }
      public void study(){
          System.out.println("教书");
      }
      public void dinner(){
          System.out.println("晚饭");
      }
      public void sleep(){
          System.out.println("睡觉");
      }
  }
  
  ```

  

* 采用模板优化，使用Person模板的优化

  ```java
  package temp;
  
  /**
   * ClassName:Person
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/21 10:54
   * @Version 1.0
   */
  public abstract class Person {
      /*
      模板方法，并且使用final防止被覆盖
       */
      public final void day() {
          qiChuang();
          xishu();
          breakfast();
          study();
          dinner();
          sleep();
      }
  
      public void qiChuang() {
          System.out.println("起床");
      }
  
      public void xishu() {
          System.out.println("洗漱");
      }
  
      public void breakfast() {
          System.out.println("吃早餐");
      }
  
      public abstract void study();
  
      public void dinner() {
          System.out.println("晚饭");
      }
  
      public void sleep() {
          System.out.println("睡觉");
      }
  
  
  }
  
  ```

  ```java
  package temp;
  
  /**
   * ClassName:Student
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/21 10:43
   * @Version 1.0
   */
  public class Student extends Person{
      /*
      描述学生的一天
       */
      @Override
      public void study(){
          System.out.println("学习");
      }
  
  }
  
  ```

  ```java
  package temp;
  
  /**
   * ClassName:Teacher
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/21 10:45
   * @Version 1.0
   */
  public class Teacher extends Person{
      /*
     描述老师的一天，存在问题，算法没有重复使用，代码没有复用
      */
      @Override
      public void study(){
          System.out.println("教书");
      }
  
  }
  
  ```

  