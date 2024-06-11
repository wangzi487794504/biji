#### 注解和Junit

* Annotation(注解)是从JDK5.0开始引入的新技术

* Annotation的作用:

  * 不是程序本身，可以对程序作出解释.(这一点和注释(comment)没什么区别)可以被其他程序(比如:编译器等)读取.

* Annotation的格式:

  * 注解是以"@注释名"在代码中存在的，还可以添加一些参数值﹐例如:@SuppressWarnings(value="unchecked").

* Annotation在哪里使用?

  * 可以附加在package , class , method , field等上面﹐相当于给他们添加了额外的辅助信息，我们可以通过反射机制编程实现对这些元数据的访问

* 内置注解

  * @override :定义在java.lang.Override 中,此注释只适用于修辞方法，表示一个方法声明打算重写超类中的另一个方法声明.

  * @Deprecated:定义在java.lang.Deprecated中,此注释可以用于修辞方法﹐属性﹐类,表示不鼓励程序员使用这样的元素﹐通常是因为它很危险或者存在更好的选择．

    <img src="%E6%B3%A8%E8%A7%A3.assets/1690094779156.png" alt="1690094779156" style="zoom:80%;" />

    

  * @SuppressWarnings∶定义在java.lang.SuppressWarnings中,用来抑制编译时的警告信息.

  * 与前两个注释有所不同,你需要添加一个参数才能正确使用,这些参数都是已经定义好了的.选择性的使用就好了﹒

    * @SuppressWarnings("all")
    * √@SuppressWarnings("unchecked")
    * √ @SuppressWarnings(value={"unchecked","deprecation")

* 元注解

  * 元注解的作用就是负责注解其他注解，Java定义了4个标准的meta-annotation类型,他们被用来提供对其他annotation类型作说明．

  * 这些类型和它们所支持的类在java.lang.annotation包中可以找到.(@Target , @Retention ,@Documented , @Inherited )

  * @Target:用于描述注解的使用范围(即:被描述的注解可以用在什么地方)

    ```java
    import java.io.FileInputStream;
    import java.io.FileOutputStream;
    import java.io.IOException;
    import java.io.InputStream;
    import java.lang.annotation.ElementType;
    import java.lang.annotation.Target;
    import java.net.HttpURLConnection;
    import java.net.MalformedURLException;
    import java.net.URL;
    
    public class Coma {
        @MyAnnotation
        public static void name() {
            System.out.println("aa");
        }
    
        public static void main(String[] args) throws IOException {
            name();
        }
    }
    
    // 定义注解
    @Target(value = ElementType.METHOD) // 定义它可以在方法上,放类上就报错
    @interface MyAnnotation {
    
    }
    
    ```

    * 用在类上

      ```java
      import java.io.FileInputStream;
      import java.io.FileOutputStream;
      import java.io.IOException;
      import java.io.InputStream;
      import java.lang.annotation.ElementType;
      import java.lang.annotation.Target;
      import java.net.HttpURLConnection;
      import java.net.MalformedURLException;
      import java.net.URL;
      
      @MyAnnotation
      public class Coma {
          @MyAnnotation
          public static void name() {
              System.out.println("aa");
          }
      
          public static void main(String[] args) throws IOException {
              name();
          }
      }
      
      // 定义注解
      @Target(value = { ElementType.METHOD, ElementType.TYPE }) // 定义它可以在方法上,放类上就报错
      @interface MyAnnotation {
      
      }
      
      ```

      

  * @Retention:表示需要在什么级别保存该注释信息﹐用于描述注解的生命周期

    (SOURCE< CLAsS < RUNTIME)

  * @Document:说明该注解将被包含在javadoc中

  * @Inherited:说明子类可以继承父类中的该注解

    ```JAVA
    import java.io.FileInputStream;
    import java.io.FileOutputStream;
    import java.io.IOException;
    import java.io.InputStream;
    import java.lang.annotation.Documented;
    import java.lang.annotation.ElementType;
    import java.lang.annotation.Inherited;
    import java.lang.annotation.Retention;
    import java.lang.annotation.RetentionPolicy;
    import java.lang.annotation.Target;
    import java.net.HttpURLConnection;
    import java.net.MalformedURLException;
    import java.net.URL;
    
    @MyAnnotation
    public class Coma {
        @MyAnnotation
        public static void name() {
            System.out.println("aa");
        }
    
        public static void main(String[] args) throws IOException {
            name();
        }
    }
    
    // 定义注解
    @Target(value = { ElementType.METHOD, ElementType.TYPE }) // 定义它可以在方法上,放类上就报错
    // 表示在什么时间有效,RUNTIME范围最大
    @Retention(value = RetentionPolicy.RUNTIME)
    @Documented
    @Inherited
    @interface MyAnnotation {
    
    }
    
    ```

    

* 自定义注解

  * 使用@interface自定义注解时﹐自动继承了java.lang.annotation.Annotation接口

  * 分析:

    * interface用来声明一个注解,格式: public interface 注解名{定义内容}
    * 其中的每一个方法实际上是声明了一个配置参数.
    * 方法的名称就是参数的名称.
    * 返回值类型就是参数的类型(返回值只能是基本类型,Class , string , enum ).
    * 可以通过default来声明参数的默认值
    * 如果只有一个参数成员，一般参数名为value
    * 注解元素必须要有值﹐我们定义注解元素时,经常使用空字符串,0作为默认值．

    ```java
    import java.io.FileInputStream;
    import java.io.FileOutputStream;
    import java.io.IOException;
    import java.io.InputStream;
    import java.lang.annotation.Documented;
    import java.lang.annotation.ElementType;
    import java.lang.annotation.Inherited;
    import java.lang.annotation.Retention;
    import java.lang.annotation.RetentionPolicy;
    import java.lang.annotation.Target;
    import java.net.HttpURLConnection;
    import java.net.MalformedURLException;
    import java.net.URL;
    
    @MyAnnotation2("aa")
    public class Coma {
        @MyAnnotation(name = "wang", age = 18, schools = { "安徽大学" })
        public static void name() {
            System.out.println("aa");
        }
    
        public static void main(String[] args) throws IOException {
            name();
        }
    }
    
    // 定义注解
    @Target(value = { ElementType.METHOD, ElementType.TYPE }) // 定义它可以在方法上,放类上就报错
    // 表示在什么时间有效,RUNTIME范围最大
    @Retention(value = RetentionPolicy.RUNTIME)
    @Documented
    @Inherited
    @interface MyAnnotation {
        // 这是注解的参数：参数类型+参数名();，也可以加default定义一个默认值
        String name()
    
        default "";
    
        int age();
    
        // 如果默认值为-1，代表不存在
        int id()
    
        default -1;
    
        String[] schools() default { "清华", "北大" };
    }
    
    @Target(value = { ElementType.METHOD, ElementType.TYPE }) // 定义它可以在方法上,放类上就报错
    // 表示在什么时间有效,RUNTIME范围最大
    @Retention(value = RetentionPolicy.RUNTIME)
    @Documented
    @Inherited
    @interface MyAnnotation2 {
        // 一个参数一般用value,用value当参数可以省略不写，不成文规定
        String value();
    }
    
    ```


* 获取注解的方法

  ```java
  isAnnotation()：判断clazz类是否是一个注解
  clazz.isAnnotationPresent(Class<? extends Annotation> annotationclass)：判断clazz类上是否标注了annotationclass注解。
  package wang.zi.jie;
  
  import javax.servlet.annotation.WebServlet;

  /**
   * ClassName:test
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2023/10/31 9:22
   * @Version 1.0
   */
  public class test {
      public static void main(String[] args) throws ClassNotFoundException {
          Class<?> aClass = Class.forName("wang.zi.jie.HelloServlet");
          boolean present = aClass.isAnnotationPresent(WebServlet.class);
          System.out.println(present);
          if (present){
              WebServlet annotation = aClass.getAnnotation(WebServlet.class);
              String[] value = annotation.value();
              System.out.println(value.length);
              for (int i = 0; i < value.length; i++) {
                  System.out.println(value[i]);
              }
  
          }
          System.out.println("Hello world!");
      }
  }
  
  
  ```
  





######Junit测试

* 黑盒测试:不需要写代码，给输入值，看程序是否能够输出期望的值。

* 白盒测试:需要写代码的。关注程序具体的执行流程。

* 注意

  * **所在的类必须是public的，非抽象的，包含唯一的无参构造器（只能有一个构造器）。**
  * **@Test标记的方法本身必须是public，非抽象的，非静态的，void无返回值，()无参数的。****

* 优点：可以灵活的编写测试代码，可以针对某个方法执行测试，也支持一键完成对全部方法的自动化测试，且各自独立不需要程序员去分析测试的结果，会自动生成测试报告出来。

* 步骤：

  * 将Junit框架的jar包导入到项目中(注意:IDEA集成了Junit框架，不需要我们自己手工导入了)
  * 为需要测试的业务类，定义对应的测试类，并为每个业务方法，编写对应的测试方法(必须:公共、无参、无返回值)
  * 测试方法上必须声明@Test注解，然后在测试方法中，编写代码调用被测试的业务方法进行测试;
  * 开始测试:选中测试方法，右键选择“jUnit运行”，如果测试通过则是绿色;如果测试失败，则是红色

* 测试类命名方式：业务名+Test

* 测试方法的命名方式：test+被测试方法的方法名

* 断言机制：通过预测结果进行正确性测试

  ```java
  public class TestLog {
      @Test
      public void testLog(){
          //传入当前类的全路径
          Logger logger = Logger.getLogger("wang.zi.jie.TestLog");
          logger.info("aa");//INFO级别的
          logger.log(Level.INFO, "aa");
          String name="张三";
          int nums[]=new int[]{1,3,5,6,7,8};
          int age=18;
          logger.log(Level.INFO,"学生的姓名{0}，年龄{1}",new Object[]{name,age});
          Assert.assertEquals("数组长度", 5, nums.length);
       
      }
  ```

  

* 运行所有测试类，右键项目

  <img src="%E6%B3%A8%E8%A7%A3%E5%92%8CJunit.assets/1709186247035.png" alt="1709186247035" style="zoom:50%;" />



* junit常见注解

  ![1709186300576](%E6%B3%A8%E8%A7%A3%E5%92%8CJunit.assets/1709186300576.png)

* 上面是junit4，下面是junit5

  <img src="%E6%B3%A8%E8%A7%A3%E5%92%8CJunit.assets/1709188001266.png" alt="1709188001266" style="zoom:67%;" />