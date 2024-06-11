#### 代理模式、

* 代理模式的作用是：为其他对象提供一种代理以控制对这个对象的访问。在某些情况下，一个客户不想或者不能直接引用一个对象，此时可以通过一个称之为“代理”的第三者来实现间接引用。代理对象可以在客户端和目标对象之间起到中介的作用，并且可以通过代理对象去掉客户不应该看到的内容和服务或者添加客户需要的额外服务。 通过引入一个新的对象来实现对真实对象的操作或者将新的对象作为真实对象的一个替身，这种实现机制即为代理模式，通过引入代理对象来间接访问一个对象，这就是代理模式的模式动机。

* 代理模式中的角色：

  - 代理类（代理主题）
  - 目标类（真实主题）
  - 代理类和目标类的公共接口（抽象主题）：客户端在使用代理类时就像在使用目标类，不被客户端所察觉，所以代理类和目标类要有共同的行为，也就是实现共同的接口。

* 使用代理模式，客户端是察觉不到的

* 代理模式是GoF23种设计模式之一。属于结构型设计模式。

* 代理模式的作用：

  * 第一个作用：当一个对象需要受到保护时，考虑用代理对象去完成某个行为
  * 第二个作用：需要给某个对象的功能进行增强的时候
  * A对象和B对象无法直接进行交互时

* 举例分析，现在有一个业务

  ```java
  public interface OrderService {
      void generate();
      void modify();
      void detail();
  }
  ```

  ```java
  public class OrderServiceImpl implements OrderService {
      @Override
      public void generate() {
          //模拟网页慢
          try {
              Thread.sleep(2000);
          } catch (InterruptedException e) {
              throw new RuntimeException(e);
          }
          System.out.println("订单已生成");
      }
      @Override
      public void modify() {
          //模拟网页慢
          try {
              Thread.sleep(2000);
          } catch (InterruptedException e) {
              throw new RuntimeException(e);
          }
          System.out.println("订单已修改");
      }
      @Override
      public void detail() {
          //模拟网页慢
          try {
              Thread.sleep(2000);
          } catch (InterruptedException e) {
              throw new RuntimeException(e);
          }
          System.out.println("订单详情");
      }
  }
  ```

  

* 项目已上线，并且运行正常，只是客户反馈系统有一些地方运行较慢，要求项目组对系统进行优化。于是项目负责人就下达了这个需求。首先需要搞清楚是哪些业务方法耗时较长，于是让我们统计每个业务方法所耗费的时长。如果是你，你该怎么做呢？

* 如果直接加代码，如下，会违反OCP原则

  ```java
      public void generate() {
          long begin = System.currentTimeMillis();
          try {
              Thread.sleep(1234);
          } catch (InterruptedException e) {
              e.printStackTrace();
          }
          System.out.println("订单已生成");
          long end = System.currentTimeMillis();
          System.out.println("耗费时长"+(end - begin)+"毫秒");
      }
  ```

* 解决方法二：使用子类继承，在子类上重写

  ```java
  public class OrderServiceImplSub extends OrderServiceImpl{
      @Override
      public void generate() {
          long begin = System.currentTimeMillis();
          super.generate();
          long end = System.currentTimeMillis();
          System.out.println("耗时"+(end - begin)+"毫秒");
      }
  
      @Override
      public void detail() {
          long begin = System.currentTimeMillis();
          super.detail();
          long end = System.currentTimeMillis();
          System.out.println("耗时"+(end - begin)+"毫秒");
      }
  
      @Override
      public void modify() {
          long begin = System.currentTimeMillis();
          super.modify();
          long end = System.currentTimeMillis();
          System.out.println("耗时"+(end - begin)+"毫秒");
      }
  }
  ```

  * 这个仍然然有问题
  * 第一个问题：假设系统中有100个这样的业务类，需要提供100个子类，并且之前写好的创建Service对象的代码，都要修改为创建子类对象。
  * 第二个问题：由于采用了继承的方式，导致代码之间的耦合度较高。

* 使用静态代理模式解决

  ```java
  public class OrderServiceProxy  implements OrderService {
      //将目标对象作为代理对象的一个属性，这种关系叫做关联关系，比继承关系耦合度低
      private OrderService orderService;
      //创建代理对象的时候
      public OrderServiceProxy(OrderService orderService) {
          this.orderService = orderService;
      }
      //代理类
      @Override
      public void generate() {//代理
          long begin=System.currentTimeMillis();
          orderService.generate();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
      @Override
      public void modify() {
          long begin=System.currentTimeMillis();
          orderService.modify();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
      @Override
      public void detail() {
          long begin=System.currentTimeMillis();
          orderService.detail();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
  }
  ```

  ```java
      @Test
      public void test1(){
          OrderService target=new OrderServiceImpl();
          OrderService proxy=new OrderServiceProxy(target);
          //调用代理方法
          proxy.generate();
      }
  ```

  * 使用静态代理进行增强，优点：符合OCP开闭原则，同时采用的是关联关系，所以程序的耦合度较低
  * 缺点：如果系统中业务接口很多，一个接口对应一个代理类，显然也是不合理的，会导致类爆炸。怎么解决这个问题？动态代理可以解决。

* 动态代理

  * 在程序运行阶段，在内存中动态生成代理类，被称为动态代理，目的是为了减少代理类的数量。解决代码复用的问题。
  * 在内存当中动态生成类的技术常见的包括：
    - JDK动态代理技术：只能代理接口。
    - CGLIB动态代理技术：CGLIB(Code Generation Library)是一个开源项目。是一个强大的，高性能，高质量的Code生成类库，它可以在运行期扩展Java类与实现Java接口。它既可以代理接口，又可以代理类，**底层是通过继承的方式实现的**。性能比JDK动态代理要好。**（底层有一个小而快的字节码处理框架ASM。）**
    - Javassist动态代理技术：Javassist是一个开源的分析、编辑和创建Java字节码的类库。是由东京工业大学的数学和计算机科学系的 Shigeru Chiba （千叶 滋）所创建的。它已加入了开放源代码JBoss 应用服务器项目，通过使用Javassist对字节码操作为JBoss实现动态"AOP"框架

  

  

  

* Proxy类全名：java.lang.reflect.Proxy。这是JDK提供的一个类（所以称为JDK动态代理）。主要是通过这个类在内存中生成代理类的字节码。

  * 其中newProxyInstance()方法有三个参数：
    * 第一个参数：类加载器。在内存中生成了字节码，要想执行这个字节码，也是需要先把这个字节码加载到内存当中的。所以要指定使用哪个类加载器加载。**并且jdk要求目标类的类加载器必须和代理类的类加载器使用同一个**
    * 第二个参数：接口类型。代理类和目标类实现相同的接口，所以要通过这个参数告诉JDK动态代理生成的类要实现哪些接口。
    * 第三个参数：调用处理器。这是一个JDK动态代理规定的接口，接口全名：java.lang.reflect.InvocationHandler。显然这是一个回调接口，也就是说调用这个接口中方法的程序已经写好了，就差这个接口的实现类了。这个实现类编写的就是增强程序

  ```java
  public class OrderServiceProxy  implements OrderService {
      //将目标对象作为代理对象的一个属性，这种关系叫做关联关系，比继承关系耦合度低
      private OrderService orderService;
      //创建代理对象的时候
      public OrderServiceProxy(OrderService orderService) {
          this.orderService = orderService;
      }
      //代理类
      @Override
      public void generate() {//代理
          long begin=System.currentTimeMillis();
          orderService.generate();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
      @Override
      public void modify() {
          long begin=System.currentTimeMillis();
          orderService.modify();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
      @Override
      public void detail() {
          long begin=System.currentTimeMillis();
          orderService.detail();
          long end=System.currentTimeMillis();
          System.out.println("耗时多少毫秒"+(end-begin));
      }
  }
  ```

  ```java
  public class Client {
      public static void main(String[] args) {
          OrderService target=new OrderServiceImpl();
          //创建代理对象，第一个参数是类加载器，第二个参数是代理类要实现的接口，第三个是调用处理器
          //Proxy.newProxyInstance做了两件事，第一在内存中生成了class字节，第二创建了对象
          Object o = Proxy.newProxyInstance(target.getClass().getClassLoader(),
                  target.getClass().getInterfaces(),
                  new TimerInvocationHandler(target));
          OrderService orderService = (OrderService) o;
          //下面这行代码执行才会调用invoke方法（即调用代理类的代理方法才会执行invoke）
          orderService.generate();
      }
  }
  ```

  

* 封装成util类

  ```java
  /**
   * ClassName:ProxyUtil封装成一个工具类，这样就不用写了
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2024/3/14 15:03
   * @Version 1.0
   */
  public class ProxyUtil {
      public static Object newProxyInstance(Object target){
          Object o = Proxy.newProxyInstance(target.getClass().getClassLoader(),
                  target.getClass().getInterfaces(),
                  new TimerInvocationHandler(target));
          return o;
      }
  }
  ```



* CGlib