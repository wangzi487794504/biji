##### 注解开发Servlet

* web.xml配置信息太多，而且基本不修改。如果能配置到java程序里就会简单很多
* servlet3.0之后推出了注解开发，目前都是注解+配置文件的开发模式，不经常修改的放到注解，可能会被修改的的放到配置文件中。
* servlet注册注解：@WebServlet属性有：
  * name名字，对应<**servlet-name**>genertictest2</**servlet-name**>
  * urlPatterns：是一个数组，表示映射路径，可以有多个，对应<**url-pattern**>/getest2</**url-pattern**>
  * loadOnStartup：启动时加载servlet，对应<**load-on-startup**></**load-on-startup**>
  * initParams,对应<**init-param**>
        <**param-name**>wamg</**param-name**>
        <**param-value**>zijie</**param-value**>
    </**init-param**>
  * value：和urlPatterns作用一样
  * 当注解中一个属性为数组，但只有一个值的情况下，大括号可以省略。如果属性名是一个value的情况下，value都可以省略。

* 通过反射获取注解信息

  ```java
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

  

* 避免类爆炸
  * 一个单标的CRUD，就写了6个Servlet,如果一个复杂的业务系统，这种开发方式，会导致类爆炸。(类的数量太大)。怎么解决这个类爆炸?可以使用模板方法设计模式。
  * 以前的没计是一个请求一个Servlet类。1000个请求对应1000个Servlet类。导致类爆炸。可以这样做:—个请求对应一个方法。—个业务对应一个Servlet类。