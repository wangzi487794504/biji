#### 手写Spring框架

* 注解开发的本质原理

  ```java
  public class AnnotationTest {
      @Test
      public void sccanerPackage(){
          String packageName="jie.zi.wang.bean";
          Map<String,Object> beanMap=new HashMap<>();
          //  .这个正则表达式代表任意字符，普通.需要加\.
          String packagePath = packageName.replaceAll("\\.", "/");
          URL url = ClassLoader.getSystemClassLoader().getResource(packagePath);
          String path = url.getPath();
          File file=new File(path);
          File[] files = file.listFiles();
          System.out.println(path);
          Arrays.stream(files).forEach(file1 -> {
  //            System.out.println(file1.getName());
  //            System.out.println(file1.getName().split("\\.")[0]);
              //获取包名加类名，也就是完整的类名
              String className=packageName+"."+file1.getName().split("\\.")[0];
              System.out.println(className);
              //使用反射创建对象
              try {
                  Class<?> aClass = Class.forName(className);
                  boolean present = aClass.isAnnotationPresent(MyAnnotation.class);
                  if (present){
                      MyAnnotation annotation = aClass.getAnnotation(MyAnnotation.class);
                      String id = annotation.value();
                      //有这个注解都要创建对象
                      Object o = aClass.getDeclaredConstructor().newInstance();
                      beanMap.put(id, o); 
                  }
  
              } catch (Exception e) {
                  throw new RuntimeException(e);
              }
          });
  //        System.out.println(packagePath);
      }
  }
  
  ```

  ```java
  @Target(value = {ElementType.TYPE})
  @Retention(value = RetentionPolicy.RUNTIME)
  public @interface MyAnnotation {
      String value();
  }
  ```





* 在spring中，声明bean的注解

  * 负责声明Bean的注解，常见的包括四个：

    - @Component
    - @Controller
    - @Service
    - @Repository

  * 源码如下：

    ```java
    Component注解
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Indexed
    public @interface Component {
        String value() default "";
    }
    ```

    ```java
    Controller
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Component
    public @interface Controller {
        @AliasFor(
            annotation = Component.class
        )
        String value() default "";
    }
    ```

    ```java
    Service
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Component
    public @interface Service {
        @AliasFor(
            annotation = Component.class
        )
        String value() default "";
    }
    ```

    ```java
    Repository
    @Target({ElementType.TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    @Component
    public @interface Repository {
        @AliasFor(
            annotation = Component.class
        )
        String value() default "";
    }
    ```

    * AliasFor说明了只有component是老大，其余都是他的别名
    * 也就是说：这四个注解的功能都一样。用哪个都可以。
    * 只是为了增强程序的可读性，建议：
      - 控制器类上使用：Controller
      - service类上使用：Service
      - dao类上使用：Repository
    * 他们都是只有一个value属性。value属性用来指定bean的id，也就是bean的名字。

* 初次尝试

  * 引入context约束

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:context="http://www.springframework.org/schema/context"
           xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd">
    <!--    指定给Spring框架要扫描哪些包-->
        <context:component-scan base-package="wang.zi.jie.bean"></context:component-scan>
    </beans>
    ```

    ```java
    @Component("userBean")
    public class User {
    }
    ```

    ```java
        @Test
        public void test1(){
            ApplicationContext context=new ClassPathXmlApplicationContext("spring.xml");
            User userBean = context.getBean("userBean", User.class);
        }
    ```

    * 如果注解不赋值，默认为类名首字母变小写就是bean的名字

* 多个包，可以用都好隔开

  ```xml
   <context:component-scan base-package="wang.zi.jie.bean,wang.zi.jie.bean2"></context:component-scan>
  ```

  * 也可以指定共同父包，只是牺牲效率了

* 选择性实例化bean

  * 方法1

    ```xml
    <!--    指定给Spring框架要扫描哪些包-->
        <context:component-scan base-package="wang.zi.jie.bean2" use-default-filters="false">
    <!--     只有他Repository生效   -->
            <context:include-filter type="annotation" expression="org.springframework.stereotype.Repository"/>
        </context:component-scan>
    
    <!--   use-default-filters="false"不再spring默认实例化规则，
    即使有Component、Controller、Service、Repository这些注解标注，也不再实例化。 -->
    ```

  * 方法二：和他本质一样，排除不要的
  
    ```xml
        <context:component-scan base-package="wang.zi.jie.bean2" >
    <!--     只有他Controller不生效   -->
            <context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/>
        </context:component-scan>
    ```
  
    

###### 负责注入的注解

* 如何给Bean的属性赋值。给Bean属性赋值需要用到这些注解
  * @Value
  * @Autowired
  * @Qualifier
  * @Resource

* 当属性的类型是简单类型时，可以使用@Value注解进行注入。

  ```java
  @Component
  public class User {
      @Value(value = "zhangsan")
      private String name;
      @Value("20")
      private int age;
      @Override
      public String toString() {
          return "User{" +
                  "name='" + name + '\'' +
                  ", age=" + age +
                  '}';
      }
  }
  ```

  * **不需要提供set方法,当然value注解也可以实现在方法上****

    ```java
    @Component
    public class User {  
        private String name;
        private int age;
        @Value("李四")
        public void setName(String name) {
            this.name = name;
        }
        @Value("30")
        public void setAge(int age) {
            this.age = age;
        }
        @Override
        public String toString() {
            return "User{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
    ```

  * 也可以放在构造方法上

    ```java
    @Component
    public class User {
    
        private String name;
    
        private int age;
    
        public User(@Value("隔壁老王") String name, @Value("33") int age) {
            this.name = name;
            this.age = age;
        }
    
        @Override
        public String toString() {
            return "User{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
    ```

    

* @Autowired注解可以用来注入**非简单类型**。被翻译为：自动连线的，或者自动装配。

  单独使用@Autowired注解，**默认根据类型装配**。【默认是byType】

  * 查看源码

    ```java
    @Target({ElementType.CONSTRUCTOR, ElementType.METHOD, ElementType.PARAMETER, ElementType.FIELD, ElementType.ANNOTATION_TYPE})
    @Retention(RetentionPolicy.RUNTIME)
    @Documented
    public @interface Autowired {
    	boolean required() default true;
    }
    ```

  * 源码中有两处需要注意：

    - 第一处：该注解可以标注在哪里？

    - - 构造方法上
      - 方法上
      - 方法的形参上
      - 属性上
      - 注解上

    - 第二处：该注解有一个required属性，默认值是true，表示在注入的时候要求被注入的Bean必须是存在的，如果不存在则报错。如果required属性设置为false，表示注入的Bean存在或者不存在都没关系，存在的话就注入，不存在的话，也不报错。
    - **当有参数的构造方法只有一个时，@Autowired注解可以省略**

  * 测试1：在属性上使用

    ```java
    public interface OrderDao {
        void insert();
    }
    ```

    ```jav
    @Repository
    public class OrderDaoImpl implements OrderDao {
        @Override
        public void insert() {
            System.out.println("OrderDao的insert执行了");
        }
    }
    ```

    ```java
    @Service
    public class OrderService {
        //根据类型自动装配
        @Autowired
        private OrderDao orderDao;
        public void generate(){
            orderDao.insert();
        }
    }
    ```

    ```java
        @Test
        public void test2(){
            ApplicationContext context=new ClassPathXmlApplicationContext("spring.xml");
            OrderService orderService = context.getBean("orderService", OrderService.class);
            orderService.generate();
        }
    ```

    * 缺点：有多个实现类就会报错，**要解决这个问题，就得结合@Qualifier注解**

      ```java
      @Service
      public class OrderService {
          //根据类型自动装配
          @Autowired
          @Qualifier(value = "orderDaoImpl")
          private OrderDao orderDao;
          public void generate(){
              orderDao.insert();
          }
      }
      ```

    * 利用Qualifier选择使用哪一个实现类



* @Resource注解也可以完成非简单类型注入。那它和@Autowired注解有什么区别？

  - **@Resource注解是JDK扩展包中的，也就是说属于JDK的一部分。所以该注解是标准注解，更加具有通用性。(JSR-250标准中制定的注解类型。JSR是Java规范提案。)**
  - ==@Autowired注解是Spring框架自己的。==
  - **==@Resource注解默认根据名称装配byName，未指定name时，使用属性名作为name。通过name找不到的话会自动启动通过类型byType装配。==**
  - **@Autowired注解默认根据类型装配byType，如果想根据名称装配，需要配合@Qualifier注解一起用。**
  - @Resource注解用在属性上、setter方法上。
  - @Autowired注解用在属性上、setter方法上、构造方法上、构造方法参数上。

* @Resource注解属于JDK扩展包，所以不在JDK当中，需要额外引入以下依赖：【**如果是JDK8的话不需要额外引入依赖。高于JDK11或低于JDK8需要引入以下依赖。**】

*  如果你是Spring6+版本请使用这个依赖 

  ```xml
  <dependency>
    <groupId>jakarta.annotation</groupId>
    <artifactId>jakarta.annotation-api</artifactId>
    <version>2.1.1</version>
  </dependency>
  ```

  *  一定要注意：**如果你用Spring6，要知道Spring6不再支持JavaEE，它支持的是JakartaEE9。（Oracle把JavaEE贡献给Apache了，Apache把JavaEE的名字改成JakartaEE了，大家之前所接触的所有的  javax.\*  包名统一修改为  jakarta.\*包名了。）**

* 如果你是spring5-版本请使用这个依赖 

  ```xml
  <dependency>
    <groupId>javax.annotation</groupId>
    <artifactId>javax.annotation-api</artifactId>
    <version>1.3.2</version>
  </dependency>
  ```

  

* 测试

  ```java
  @Service
  public class StudentService {
      @Resource(name = "studentDaoImpl")
      private StudentDao studentDao;
      public void deleteService(){
          studentDao.deleteById();
      }
  }
  ```

  ```java
  @Repository
  public class StudentDaoImpl implements StudentDao {
      @Override
      public void deleteById() {
          System.out.println("学生");
      }
  }
  ```

  * **首先通过名字进行装配，没有名字把属性名当做名字去找有没有这个名字的实现类，这个也找不到，最后才通过类型匹配**





* 全注解开发

  * 需要建一个类代替配置文件

    ```java
    @Configuration
    @ComponentScan({"wang.zi.jie"})
    public class SpringConfig {
    }
    ```

    ```java
        @Test
        public void test4(){
            AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(SpringConfig.class);
            context.getBean("userBean",User.class);
        }
    ```

    