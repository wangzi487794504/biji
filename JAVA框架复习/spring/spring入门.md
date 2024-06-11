##### Spring第一天

* 问题引入

  ```java
  public class UserDaoImpl implements UserDao {
      @Override
      public void deleteUserById() {
          System.out.println("mysql正在删除用户信息");
      }
  }
  ```

  ```java
  public class UserServiceImpl implements UserService {
      //这个地方写死了
      private UserDao userDao=new UserDaoImpl();
      @Override
      public void deleteUser() {
          userDao.deleteUserById();
      }
  }
  ```

  ```java
  public class UserAction {
      private UserService userService=new UserServiceImpl();
      public void deleteUser(){
          userService.deleteUser();
      }
  }
  ```

  

*  OCP开闭原则

  * 开闭原则是这样说的：
  * 在软件开发过程中应当对扩展开放，对修改关闭。也就是说，如果在进行功能扩展的时候，添加额外的类是没问题的，但因为功能扩展而修改之前运行正常的程序。这是忌讳的，不被允许的。
    因为一旦修改之前运行正常的程序，就会导致项目整体要进行全方位的重新测试。这是相当麻烦的过程。
  * 导致以上问题的主要原因是：代码和代码之间的耦合度太高。

* 依赖倒置原则DIP

  * 依赖倒置原则(Dependence Inversion Principle)，简称DIP，主要倡导面向抽象编程，面向接口编程，不要面向具体编程，让上层不再依赖下层，下面改动了，上面的代码不会受到牵连。

  * 这样可以大大降低程序的耦合度，耦合度低了，扩展力就强了，同时代码复用性也会增强。

    ![1709868130455](spring%E5%85%A5%E9%97%A8.assets/1709868130455.png)

  * **只要上依赖下就违背该原则**



* 使用控制反转解决 （Inversion of Control） 
  * 反转：
    *  第一件事：我不在程序中采用硬编码的方式来new对象了。（new对象我不管了，new对象的权利交出去了。）            
    * 第二件事：我不在程序中采用硬编码的方式来维护对象的关系了。（对象之间关系的维护权，我也不管了，交出去了。） 
  *  控制反转：是一种编程思想。或者叫做一种新型的设计模式。由于出现的比较新，没有被纳入GoF23种设计模式范围内。 
* Spring框架
  * Spring框架实现了控制反转IoC这种思想
  * Spring框架可以帮你new对象。
  *  Spring框架可以帮你维护对象和对象之间的关系。
      * Spring是一个实现了IoC思想的容器。
     * **控制反转的实现方式有多种，其中比较重要的叫做：依赖注入(Dependency Injection，简称DI)。**
          * 控制反转是思想。依赖注入是这种思想的具体实现。
          * 依赖注入DI，又包括常见的两种方式：
               第一种：set注入（==执行set方法给属性赋值==）
               第二种：构造方法注入（==执行构造方法给属性赋值==）
          * 依赖注入 中 “依赖”是什么意思？ “注入”是什么意思？
                  * 依赖：A对象和B对象的关系。
                  * 注入：是一种手段，通过这种手段，可以让A对象和B对象产生关系。
                  * 依赖注入：对象A和对象B之间的关系，靠注入的手段来维护。而注入包括：set注入和构造注入。

*  Spring特点
  * 轻量
    * 从大小与开销两方面而言Spring都是轻量的。
    * 完整的Spring框架可以在一个大小只有1MB多的JAR文件里发布。
    * 并且Spring所需的处理开销也是微不足道的。
  * Spring是非侵入式的：Spring应用中的对象不依赖于Spring的特定类。
  * 控制反转
    * Spring通过一种称作控制反转（IoC）的技术促进了解耦合。
    * 当应用了IoC，一个对象依赖的其它对象会通过被动的方式传递进来，而不是这个对象自己创建或者查找依赖对象。
    * 你可以认为IoC与JNDI相反——不是对象从容器中查找依赖，而是容器在对象初始化时不等对象请求就主动将依赖传递给它。
  * 面向切面
    * Spring提供了面向切面编程的丰富支持，允许通过分离应用的业务逻辑与系统级服务（例如审计（auditing）和事务（transaction）管理）进行内聚性的开发。
    * 应用对象只实现它们应该做的——完成业务逻辑——仅此而已。它们并不负责（甚至是意识）其它的系统级关注点，例如日志或事务支持。
  * 容器
    * Spring包含并管理应用对象的配置和生命周期，在这个意义上它是一种容器.
    * 你可以配置你的每个bean如何被创建——基于一个可配置原型（prototype），你的bean可以创建一个单独的实例或者每次需要时都生成一个新的实例——以及它们是如何相互关联的。
    * 然而，Spring不应该被混同于传统的重量级的EJB容器，它们经常是庞大与笨重的，难以使用。
  * 框架
    * Spring可以将简单的组件配置、组合成为复杂的应用。
    * 在Spring中，应用对象被声明式地组合，典型地是在一个XML文件里。
    * Spring也提供了很多基础功能（事务管理、持久化框架集成等等），将应用逻辑的开发留给了你。
    * 所有Spring的这些特征使你能够编写更干净、更可管理、并且更易于测试的代码。它们也为Spring中的各种模块提供了基础支持。



* 第一个spring程序

  ```java
  public class User {
  }
  ```

  ```java
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  
  
  <!--    bean的id和class属性：
  id属性：代表对象的唯一标识。可以看做一个人的身份证号。
  class属性：用来指定要创建的java对象的类名，这个类名必须是全限定类名（带包名）。-->
      <bean id="userBean" class="wang.zi.jie.bean.User">
  
      </bean>
  </beans>
  ```

  ```java
      @Test
      public void testSpring1(){
          //获取Spring容器对象
          //ApplicationContext翻译成应用上下文，其实就是Spring容器
          //ApplicationContext是一个接口
          //ApplicationContext有很多实现类，其中一个实现类叫ClassPathXmlApplicationContext
          //ClassPathXmlApplicationContext专门从类路径加载spring配置文件的上下文对象
          ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml");
          Object userBean = applicationContext.getBean("userBean");
          System.out.println(userBean);
      }
  ```

  

* 它的本质使用java反射调用·User的无参数构造方法构建对象，**如果不提供无参构造就会报错**

* 他会把创建好的对象存到Map(String，Object)

  <img src="spring%E5%85%A5%E9%97%A8.assets/1709883575143.png" alt="1709883575143" style="zoom:50%;" />

* spring配置文件可以随便起名字，因为是要通过给他字符串来扫描的

* 配置文件可以有多个

  ```java
  ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml","beans.xml","bao/aa.xml");
  ```

* 也可以获取java自带的类

  ```xml
  <bean id="date" class="java.util.Date"></bean>
  ```

  ```java
  Object date = applicationContext.getBean("date");
  ```

  * **如果bean的id不存在，不会返回null，而是直接报错**

  ```JAVA
          //如果不想返回Object，可以传入一个class对象
          Date date = applicationContext.getBean("date", Date.class);
  ```

* 从目录中加载配置文件

  ```java
  ApplicationContext context=new FileSystemXmlApplicationContext("d:/spring6.xml");
  ```

  

* BeanFactory

  ```java
      @Test
      public void testBeanFactory(){
          //ApplicationContext的超级父接口是BeanFactory（能生成bean对象的一个工厂对象）
          //BeanFactory是IOC容器的顶级接口
          //Spring的IOC底层是使用了工厂模式
          //Spring的IOC底层实现：XML解析+工厂模式+反射机制
          BeanFactory beanFactory=new ClassPathXmlApplicationContext("spring.xml");
          beanFactory.getBean("userBean");
      }
  ```

  

* 在加载配置文件时就已经创建了对象

  ```java
      @Test
      public void testInitBean(){
          //并不是getbean才创建User对象，在new ClassPathXmlApplicationContext就已经创建了
          ClassPathXmlApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml");
      }
  ```

  ```java
  public class User {
      public User() {
          System.out.println("初始化方法");
      }
  }
  ```

  输出：初始化方法





* Spring6启用Log4j2日志框架

  * 第一步，引入依赖

    ```xml
    <!--log4j2的依赖-->
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-core</artifactId>
      <version>2.19.0</version>
    </dependency>
    <dependency>
      <groupId>org.apache.logging.log4j</groupId>
      <artifactId>log4j-slf4j2-impl</artifactId>
      <version>2.19.0</version>
    </dependency>
    ```

    

  * 第二步，配置文件（文件名固定为：log4j2.xml，文件必须放到类根路径下。）

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    
    <configuration>
    
        <loggers>
            <!--
                level指定日志级别，从低到高的优先级：
                    ALL < TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF
            -->
            <root level="DEBUG">
                <appender-ref ref="spring6log"/>
            </root>
        </loggers>
    
        <appenders>
            <!--输出日志信息到控制台-->
            <console name="spring6log" target="SYSTEM_OUT">
                <!--控制日志输出的格式-->
                <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss SSS} [%t] %-3level %logger{1024} - %msg%n"/>
            </console>
        </appenders>
    
    </configuration>
    ```

    