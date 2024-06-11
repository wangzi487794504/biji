##### 配置文件

* spring的配置文件默认是在WEB-INF，但是可以修改，通过初始化方法加载。这样就和以前一样了

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
           version="4.0">
      <!--配置前端控制器-->
      <servlet>
          <servlet-name>springmvc</servlet-name>
          <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
          <!--手动设置springmvc配置文件的路径及名字-->
          <init-param>
              <param-name>contextConfigLocation</param-name>
              <param-value>classpath:springmvc.xml</param-value>
          </init-param>
          <!--为了提高用户的第一次访问效率，建议在web服务器启动时初始化前端控制器-->
          <load-on-startup>1</load-on-startup>
      </servlet>
      <servlet-mapping>
          <servlet-name>springmvc</servlet-name>
          <url-pattern>/</url-pattern>
      </servlet-mapping>
  </web-app>
  ```



##### ResuestMapping

* `@RequestMapping` 注解是 Spring MVC 框架中的一个控制器映射注解，用于将请求映射到相应的处理方法上。具体来说，它可以将指定 URL 的请求绑定到一个特定的方法或类上，从而实现对请求的处理和响应。

*  @RequestMapping：用于将 web 请求映射到控制器类的方法。此方法处理请求。

  * 可用在类上或方法上。 在类和方法同时组合使用。 重要的属性 value：别名 path 表示请求的 uri， 在类和方法方法同时使用 value，方法上的继承类上的 value 值。 
  * method：请求方式，支持 GET, POST, HEAD, OPTIONS, PUT, PATCH, DELETE, TRACE。 值为：RequestMethod[] method() ， RequestMethod 是 enum 类型。 
  * **快捷注解 @GetMapping: 表示 get 请求方式的@RequestMapping **
  * @PostMapping:表示 post 请求方式的@RequestMapping 
  * @PutMapping：表示 put 请求方式的@RequestMapping 
  * @DeleteMapping: 表示 delete 请求方式的@RequestMapp 
  *  `对于请求方式 get，post，put，delete 等能用 HttpMethod 表示，Spring Boot3 之前他是 enum，Spring Boot3 他是 class public enum HttpMethod Spring Boot3 之前他是 enum public final class HttpMethod Spring Boot3 他是 class`

* 通过RequestMapping的源码可以看到RequestMapping注解只能出现在类上或者方法上。

* 如果两个Controller的RequestMapping相同，都是"/detail"

  ```txt
  org.springframework.beans.factory.BeanCreationException: 
  Error creating bean with name 'org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping': 
  Ambiguous mapping. Cannot map 'userController' method 
  com.powernode.springmvc.controller.UserController#toDetail()
  to { [/detail]}: There is already 'productController' bean method
  com.powernode.springmvc.controller.ProductController#toDetail() mapped.
  ```

  * 解决方案
    * 第一种方案：将方法上RequestMapping的映射路径修改的不一样。
    * 第二种方案：在类上添加RequestMapping的映射路径，以类上的RequestMapping作为命名空间，来加以区分两个不同的映射。**（类上就是给类里面的所有的方法都加一个路径）**

* RequestMapping的属性

  ```java
  public @interface RequestMapping {
      String name() default "";
  
      @AliasFor("path")
      String[] value() default {};
  
      @AliasFor("value")
      String[] path() default {};
  
      RequestMethod[] method() default {};
  
      String[] params() default {};
  
      String[] headers() default {};
  
      String[] consumes() default {};
  
      String[] produces() default {};
  }
  ```

  * value属性是该注解最核心的属性，value属性填写的是请求路径，也就是说通过该请求路径与对应的控制器的方法绑定在一起。另外通过源码可以看到value属性是一个字符串数组：
  
  * 既然是数组，就表示可以提供多个路径，也就是说，在SpringMVC中，多个不同的请求路径可以映射同一个控制器的同一个方法：
  
  * 注解源码发现path和value是一样的，只不过value可以省略
  
  * ==请求路径支持模糊匹配（Ant风格的value）==
    * ?，代表任意一个字符（除/  ? 等）不能空着，必须要有字符
    * *，代表0到N个任意字符  （除/  ? 等）
    * **，代表0到N个任意字符，并且路径中可以出现路径分隔符 /
    * 注意：** 通配符在使用时，左右不能出现字符，只能是 /**，如果左右两边都有，效果等同于一个\*      。在spring5支持，spring6不支持
    *  正则表达式： 支持正则表达式 
    
  * **value中的占位符**
  
    * 传统风格的占位符：uri?name1=value1&name2=value2&name3=value
  
    * restful风格：uri/value1/value2/value3
  
      ```java
      @RequestMapping(value="/testRESTful/{id}/{username}/{age}")
      public String testRESTful(
              @PathVariable("id")
              int id,
              @PathVariable("username")
              String username,
              @PathVariable("age")
              int age){
          System.out.println(id + "," + username + "," + age);
          return "testRESTful";
      }
      ```
  
  * method属性的作用
  
    * 在Servlet当中，如果后端要求前端必须发送一个post请求，后端可以通过重写doPost方法来实现。后端要求前端必须发送一个get请求，后端可以通过重写doGet方法来实现。当重写的方法是doPost时，前端就必须发送post请求，当重写doGet方法时，前端就必须发送get请求。如果前端发送请求的方式和后端的处理方式不一致时，会出现405错误。
  
    * HTTP状态码405，这种机制的作用是：限制客户端的请求方式，以保证服务器中数据的安全。
  
      ```java
      public enum RequestMethod {
          GET,
          HEAD,
          POST,
          PUT,
          PATCH,
          DELETE,
          OPTIONS,
          TRACE
      ```
  
    * 举例：如果要求post请求
  
      ```java
      @RequestMapping(value = "/login", method = RequestMethod.POST)
      public String login(){
          return "success";
      }
      ```
  
    * method 是一个数组，可以支持多种请求方式
  
    * 衍生注解：对于以上的程序来说，SpringMVC提供了另一个注解，使用这个注解更加的方便，它就是：PostMapping，使用该注解时，不需要指定method属性，因为它默认采用的就是POST处理方式
  
      ```java
      //@RequestMapping(value="/login", method = RequestMethod.POST)
      @PostMapping("/login")
      public String testMethod(){
          return "testMethod";
      }
      ```
  
    * **GET：获取资源，只允许读取数据，不影响数据的状态和功能。使用 URL 中传递参数或者在 HTTP 请求的头部使用参数，服务器返回请求的资源。**
  
    * **POST：向服务器提交资源，可能还会改变数据的状态和功能。通过表单等方式提交请求体，服务器接收请求体后，进行数据处理。**
  
    * **PUT：更新资源，用于更新指定的资源上所有可编辑内容。通过请求体发送需要被更新的全部内容，服务器接收数据后，将被更新的资源进行替换或修改。**
  
    * **DELETE：删除资源，用于删除指定的资源。将要被删除的资源标识符放在 URL 中或请求体中。**
  
    * **HEAD：请求服务器返回资源的头部，与 GET 命令类似，但是所有返回的信息都是头部信息，不能包含数据体。主要用于资源检测和缓存控制。**
  
    * PATCH：部分更改请求。当被请求的资源是可被更改的资源时，请求服务器对该资源进行部分更新，即每次更新一部分。
  
    * OPTIONS：请求获得服务器支持的请求方法类型，以及支持的请求头标志。“OPTIONS *”则返回支持全部方法类型的服务器标志。
  
    * TRACE：服务器响应输出客户端的 HTTP 请求，主要用于调试和测试。
  
    * CONNECT：建立网络连接，通常用于加密 SSL/TLS 连接。
  
    * 注意：
  
      1. 使用超链接以及原生的form表单只能提交get和post请求，put、delete、head请求可以使用发送ajax请求的方式来实现。
      2. 使用超链接发送的是get请求
      3. 使用form表单，如果没有设置method，发送get请求
      4. 使用form表单，设置method="get"，发送get请求
      5. 使用form表单，设置method="post"，发送post请求
      6. 使用form表单，设置method="put/delete/head"，发送get请求。（针对这种情况，可以测试一下）
  
    * Get和Post请求选择
  
      * 如果你是想从服务器上获取资源，建议使用GET请求，如果你这个请求是为了向服务器提交数据，建议使用POST请求。
      * 大部分的form表单提交，都是post方式，因为form表单中要填写大量的数据，这些数据是收集用户的信息，一般是需要传给服务器，服务器将这些数据保存/修改等。
      * 如果表单中有敏感信息，建议使用post请求，因为get请求会回显敏感信息到浏览器地址栏上。（例如：密码信息）
      * 做文件上传，一定是post请求。要传的数据不是普通文本。
      * 其他情况大部分都是使用get请求
  
  * ==params属性==
  
    * **params属性也是一个数组，不过要求请求参数必须和params数组中要求的所有参数完全一致后，才能映射成功**
  
    * 四种使用方式
  
      * @RequestMapping(value="/login", params={**"username"**, "password"}) 表示：请求参数中必须包含 username 和 password，才能与当前标注的方法进行映射。
      * @RequestMapping(value="/login", params={**"!username"**, "password"}) 表示：请求参数中不能包含username参数，但必须包含password参数，才能与当前标注的方法进行映射。
      * @RequestMapping(value="/login", params={**"username=admin"**, "password"}) 表示：请求参数中必须包含username参数，并且参数的值必须是admin，另外也必须包含password参数，才能与当前标注的方法进行映射。
      * @RequestMapping(value="/login", params={**"username!=admin"**, "password"}) 表示：请求参数中必须包含username参数，但参数的值不能是admin，另外也必须包含password参数，才能与当前标注的方法进行映射。
      * 注意：如果前端提交的参数，和后端要求的请求参数不一致，则出现400错误
  
    * 测试
  
      ```java
      @RequestMapping(value="/testParams", params = {"username", "password"})
      public String testParams(){
          return "testParams";
      }
      ```
  
      * 即要求必须要有这两个参数，其他的没有要求
  
    * headers属性
  
      * headers和params原理相同，用法也相同。当前端提交的请求头信息和后端要求的请求头信息一致时，才能映射成功。
  
        ```java
        @RequestMapping(value="/testHeaders", headers = {"Referer=http://localhost:8888/springmvc/"})
        public String testHeaders(){
            return "testHeaders";
        }
        ```
  
      

