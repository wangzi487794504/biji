###### springmvc入门

*  它是基于MVC开发模式的框架，用来优化控制器。它是Spring家族的一员。它也具备IOC和AOP。 

  * 什么是MVC?
    它是一种开发模式，它是模型视图控制器的简称。所有的web应用都是基于MVC开发。
    M:模型层，包含实体类，业务逻辑层，数据访问层
    V:视图层，html，javaScript，vue等都是视图层，用来显现数据
    C:控制器，它是用来接收客户端的请求，并返回响应到客户端的组件，Servlet就是组件

* SpringMVC框架的优点

  * 轻量级，基于MVC的框架
  * 易于上手，容易理解，功能强大

  * 它具备IOC和AOP

  * 方便整合Strtus,MyBatis,Hiberate,JPA 等其他框架。、
  * 完全基于注解开发

  * 在Controller, Service, Dao 都可以使用注解。方便灵活。
  * 使用@Controller 创建处理器对象,@Service 创建业务对象，@Autowired 或者@Resource 在控制器类中注入 Service,在Service 类中注入 Dao。

   ![在这里插入图片描述](springmvc%E4%BB%8B%E7%BB%8D%E5%92%8C%E5%85%A5%E9%97%A8.assets/88eb8a4da02845e1a09073637e5a0596.png) 





* SpringMVC是一个实现了MVC架构模式的Web框架，底层基于Servlet实现。
* SpringMVC已经将MVC架构模式实现了，因此只要我们是基于SpringMVC框架写代码，编写的程序就是符合MVC架构模式的。（**MVC的架子搭好了，我们只需要添添补补**）
*  ![image.png](springmvc%E4%BB%8B%E7%BB%8D%E5%92%8C%E5%85%A5%E9%97%A8.assets/image.png) 

* SpringMVC框架帮我们做了什么，与纯粹的Servlet开发有什么区别？

  * 入口控制：SpringMVC框架通过DispatcherServlet作为入口控制器，负责接收请求和分发请求。而在Servlet开发中，需要自己编写Servlet程序，并在web.xml中进行配置，才能接受和处理请求
  * 在SpringMVC中，表单提交时可以自动将表单数据绑定到相应的JavaBean对象中，只需要在控制器方法的参数列表中声明该JavaBean对象即可，无需手动获取和赋值表单数据。而在纯粹的Servlet开发中，这些都是需要自己手动完成的
  *  IoC容器：SpringMVC框架通过IoC容器管理对象，只需要在配置文件中进行相应的配置即可获取实例对象，而在Servlet开发中需要手动创建对象实例。 
  * 统一处理请求：SpringMVC框架提供了拦截器、异常处理器等统一处理请求的机制，并且可以灵活地配置这些处理器。而在Servlet开发中，需要自行编写过滤器、异常处理器等，增加了代码的复杂度和开发难度。 
  *  视图解析：SpringMVC框架提供了多种视图模板，如JSP、Freemarker、Velocity等，并且支持国际化、主题等特性。而在Servlet开发中需要手动处理视图层，增加了代码的复杂度。 

* 特点

  *  轻量级：相对于其他Web框架，Spring MVC框架比较小巧轻便。（只有几个几百KB左右的Jar包文件） 
  * 模块化：请求处理过程被分成多个模块，以模块化的方式进行处理。 

  1. 1. 控制器模块：Controller
     2. 业务逻辑模块：Model
     3. 视图模块：View

  

  * 依赖注入：Spring MVC框架利用Spring框架的依赖注入功能实现对象的管理，实现松散耦合。 

  * 易于扩展：提供了很多口子，允许开发者根据需要插入自己的代码，以扩展实现应用程序的特殊需求。 

  1. * Spring MVC框架允许开发人员通过自定义模块和组件来扩展和增强框架的功能。

  2. * Spring MVC框架与其他Spring框架及第三方框架集成得非常紧密，这使得开发人员可以非常方便地集成其他框架，以获得更好的功能。

  * 易于测试：支持单元测试框架，提高代码质量和可维护性。 （对SpringMVC中的Controller测试时，不需要依靠Web服务器。）
  *  自动化配置：提供自动化配置，减少配置细节。 

  1. * Spring MVC框架基于约定大于配置的原则，对常用的配置约定进行自动化配置。

  * 灵活性：Spring MVC框架支持多种视图技术，如JSP、FreeMarker、Thymeleaf、FreeMarker等，针对不同的视图配置不同的视图解析器即可。

* 第一个SpringMVC

  * 创建工程，设置maven

    ```xml
        <dependencies>
    <!--        sprinhmvc-->
            <dependency>
                <groupId>org.springframework</groupId>
                <artifactId>spring-webmvc</artifactId>
                <version>6.1.4</version>
            </dependency>
    <!--        servlet-->
            <dependency>
                <groupId>jakarta.servlet</groupId>
                <artifactId>jakarta.servlet-api</artifactId>
                <version>6.0.0</version>
                <scope>provided</scope>
            </dependency>
    <!--        logback-->
            <dependency>
                <groupId>ch.qos.logback</groupId>
                <artifactId>logback-classic</artifactId>
                <version>1.2.3</version>
            </dependency>
    <!--        thymeleaf和spring整合-->
            <dependency>
                <groupId>org.thymeleaf</groupId>
                <artifactId>thymeleaf-spring6</artifactId>
                <version>3.1.2.RELEASE</version>
            </dependency>
        </dependencies>
    ```

  * 配置web.xml

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
             version="4.0">
        <!--SpringMVC提供的前端控制器-->
        <servlet>
            <servlet-name>springmvc</servlet-name>
            <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        </servlet>
        <servlet-mapping>
            <servlet-name>springmvc</servlet-name>
            <url-pattern>/</url-pattern>
        </servlet-mapping>
    
    </web-app>
    ```

    * DispatcherServlet是SpringMVC框架为我们提供的最核心的类，它是整个SpringMVC框架的前端控制器，负责接收HTTP请求、将请求路由到处理程序、处理响应信息，最终将响应返回给客户端。DispatcherServlet是Web应用程序的主要入口点之一
      * 接收客户端的HTTP请求：DispatcherServlet监听来自Web浏览器的HTTP请求，然后根据请求的URL将请求数据解析为Request对象。
      * 处理请求的URL：DispatcherServlet将请求的URL（Uniform Resource Locator）与处理程序进行匹配，确定要调用哪个控制器（Controller）来处理此请求
      *  调用相应的控制器：DispatcherServlet将请求发送给找到的控制器处理，控制器将执行业务逻辑，然后返回一个模型对象（Model）
      *  渲染视图：DispatcherServlet将调用视图引擎，将模型对象呈现为用户可以查看的HTML页面
      * 返回响应给客户端：DispatcherServlet将为用户生成的响应发送回浏览器，响应可以包括表单、JSON、XML、HTML以及其它类型的数据

  * 写controler

    ```java
    @Controller
    public class FirstController {
        @RequestMapping(value = "/test")
        public String hh(){
            System.out.println("aa");
            return "firth";
        }
    }
    ```

    

  * 编写mvc配置文件,SpringMVC框架有它自己的配置文件，该配置文件的名字默认为：<servlet-name>-servlet.xml，(就是web.xml你给类起的name+-servlet.xml；)默认存放的位置是WEB-INF 目录下：

    ```js
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:context="http://www.springframework.org/schema/context"
           xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd http://www.springframework.org/schema/context https://www.springframework.org/schema/context/spring-context.xsd">
            <context:component-scan base-package="wang.zi.jie.controller"></context:component-scan>
    <!--    配置视图解释器-->
        <bean id="thymeleafViewResolver" class="org.thymeleaf.spring6.view.ThymeleafViewResolver">
            <!--作用于视图渲染的过程中，可以设置视图渲染后输出时采用的编码字符集-->
            <property name="characterEncoding" value="UTF-8"/>
            <!--如果配置多个视图解析器，它来决定优先使用哪个视图解析器，它的值越小优先级越高-->
            <property name="order" value="1"/>
            <!--当 ThymeleafViewResolver 渲染模板时，会使用该模板引擎来解析、编译和渲染模板-->
            <property name="templateEngine">
                <bean class="org.thymeleaf.spring6.SpringTemplateEngine">
                    <!--用于指定 Thymeleaf 模板引擎使用的模板解析器。模板解析器负责根据模板位置、模板资源名称、文件编码等信息，加载模板并对其进行解析-->
                    <property name="templateResolver">
                        <bean class="org.thymeleaf.spring6.templateresolver.SpringResourceTemplateResolver">
                            <!--设置模板文件的位置（前缀）-->
                            <property name="prefix" value="/WEB-INF/templates/"/>
                            <!--设置模板文件后缀（后缀），Thymeleaf文件扩展名不一定是html，也可以是其他，例如txt，大部分都是html-->
                            <property name="suffix" value=".html"/>
                            <!--设置模板类型，例如：HTML,TEXT,JAVASCRIPT,CSS等-->
                            <property name="templateMode" value="HTML"/>
                            <!--用于模板文件在读取和解析过程中采用的编码字符集-->
                            <property name="characterEncoding" value="UTF-8"/>
                        </bean>
                    </property>
                </bean>
            </property>
        </bean>
    </beans>
    ```

  * 在WEB-INFO编写模板

    ```js
    <!DOCTYPE html>
    <html lang="en" xmlns:th="http://www.thymeleaf.org">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
    </head>
    <body>
        <h1>第一个mvc</h1>
    </body>
    ```

    