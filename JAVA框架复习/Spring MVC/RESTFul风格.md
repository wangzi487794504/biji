#### RESTFul风格-



* REST对请求方式的约束是这样的

  * 查询必须发送GET请求
  * 新增必须发送POST请求
  * 修改必须发送PUT请求
  * 删除必须发送DELETE请求

* REST对URL的约束是这样的：

  * 传统的URL：get请求，/springmvc/getUserById?id=1
  * REST风格的URL：get请求，/springmvc/user/1

* RESTFul对URL的约束和规范的核心是：**通过采用**`**不同的请求方式**`**+** `**URL**`**来确定WEB服务中的资源。**

*  RESTFul 的支持路径变量

  *  {变量名} {myname:[a-z]+}: 正则皮 a-z 的多个字面，路径变量名称“myname”。@PathVariable(“myname”) 

  * {*myname}: 匹配多个路径一直到 uri 结尾

    ```java
    @GetMapping("/order/{*id}")
    {*id} 匹配 /order 开始的所有请求， id 表示 order 后面直到路径末尾的所有内容。
    id 自定义路径变量名称。与@PathVariable 一样使用
     GET http://localhost:8080/order/1001
     GET http://localhost:8080/order/1001/2023-02-16
    @GetMapping("/order/{*id}")
    public String path4(@PathVariable("id") String orderId, HttpServletRequest request){
    return "/order/{*id}请求="+request.getRequestURI() + "，id="+orderId;
    }
    注意：@GetMapping("/order/{*id}/{*date}")无效的， {*..}后面不能在有匹配规则了
    ```

    

* **RESTful 的英文全称是 Representational State Transfer（表述性状态转移）。简称REST。**

  * 表述性（Representational）是：URI + 请求方式。
  * 状态（State）是：服务器端的数据。
  * 转移（Transfer）是：变化。
  * 表述性状态转移是指：通过 URI + 请求方式 来控制服务器端数据的变化。

  ![1712998301690](RESTFul%E9%A3%8E%E6%A0%BC.assets/1712998301690.png)

* 传统的URL是基于动作的，而 RESTful URL 是基于资源和状态的，因此 RESTful URL 更加清晰和易于理解，这也是 REST 架构风格被广泛使用的主要原因之一

* RESTFul规范中规定，如果要进行保存操作，需要发送PUT请求。**如何发送PUT请求？**

  * **第一步：首先你必须是一个POST请求。**

  * **第二步：在发送POST请求的时候，提交这样的数据：**`**_method=PUT**`

    ```java
    public class HiddenHttpMethodFilter extends OncePerRequestFilter {
        private static final List<String> ALLOWED_METHODS;
        public static final String DEFAULT_METHOD_PARAM = "_method";
        private String methodParam = "_method";
    ```

  * **第三步：在web.xml文件配置SpringMVC提供的过滤器：HiddenHttpMethodFilter**

    ```java
       protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
            HttpServletRequest requestToUse = request;
            if ("POST".equals(request.getMethod()) && request.getAttribute("jakarta.servlet.error.exception") == null) {
                String paramValue = request.getParameter(this.methodParam);
                if (StringUtils.hasLength(paramValue)) {
                    //无论你大小写最终都是大写
                    String method = paramValue.toUpperCase(Locale.ENGLISH);
                    if (ALLOWED_METHODS.contains(method)) {
                        requestToUse = new HttpMethodRequestWrapper(request, method);
                    }
                }
            }
    
            filterChain.doFilter((ServletRequest)requestToUse, response);
        }
    ```

    

* DELETE请求和PUT请求实现方式相同。首先你必须是一个POST请求，然后需要期缴_method=delete

* 举例：

  * 后端

    ```java
    @Controller
    public class UserController {
        @RequestMapping(value = "/api/user/{id}", method = RequestMethod.GET)
        public String getById(@PathVariable("id") Integer id){
            System.out.println("根据用户id查询用户信息，用户id是" + id);
            return "ok";
        }
        @RequestMapping(value="/user",method = RequestMethod.POST)
        public String save(User user){
            System.out.println("正在保存用户信息");
            System.out.println(user);
            return "ok";
        }
        @RequestMapping(value = "/user",method = RequestMethod.PUT)
        public String modify(User user){
            System.out.println("正在修改信息");
            return "ok";
        }
        @RequestMapping(value = "/user/{id}",method = RequestMethod.DELETE)
        public String del(@PathVariable("id") String id){
            System.out.println("正在删除信息"+id);
            return "ok";
        }
    }
    ```

  * 前端

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Title</title>
    </head>
    <body>
    <h1>测试index编程风格</h1>
    <a href="@{/api/user/1}"></a>
    <form th:action="@{/user}" method="post">
        用户名：<input type="text" name="username"><br>
        密码：<input type="password" name="password"><br>
        年龄：<input type="text" name="age"><br>
        <input type="submit" th:value="保存">
    </form>
    <form th:action="@{/user}" method="post">
    <!--    隐藏域-->
        <input type="hidden" name="_method" value="put">
        用户名：<input type="text" name="username"><br>
        密码：<input type="password" name="password"><br>
        年龄：<input type="text" name="age"><br>
        <input type="submit" th:value="保存">
    </form>
    <a th:href="@{/user/120}" onclick="del(event)">删除用户id信息</a>
    <form  id="deleteForm" method="post">
        <!--    隐藏域-->
        <input type="hidden" name="_method" value="delete">
    </form>
    <script>
        function del(event){
            delForm=document.getElementById("deleteForm");
            //给action赋值
            delForm.action=event.target.href;
            delForm.submit();
            event.preventDefault();
        }
    </script>
    </body>
    </html>
    ```

  * web.xml配置

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
             version="6.0">
      <!--SpringMVC提供的前端控制器-->
      <servlet>
        <servlet-name>springmvc</servlet-name>
        <servlet-class>org.springframework.web.servlet.DispatcherServlet</servlet-class>
        <init-param>
          <param-name>contextConfigLocation</param-name>
          <param-value>classpath:springmvc.xml</param-value>
        </init-param>
      </servlet>
      <servlet-mapping>
        <servlet-name>springmvc</servlet-name>
        <url-pattern>/</url-pattern>
      </servlet-mapping>
      <filter>
        <filter-name>hiddenHttpMethodFilter</filter-name>
        <filter-class>org.springframework.web.filter.HiddenHttpMethodFilter</filter-class>
      </filter>
      <filter-mapping>
        <filter-name>hiddenHttpMethodFilter</filter-name>
        <url-pattern>/*</url-pattern>
      </filter-mapping>
      <filter>
        <filter-name>characterfilter</filter-name>
        <filter-class>org.springframework.web.filter.CharacterEncodingFilter</filter-class>
        <!--        配置初始化参数-->
        <init-param>
          <param-name>encoding=utf-8</param-name>
          <param-value>true</param-value>
        </init-param>
        <init-param>
          <param-name>forceRequestEncoding</param-name>
          <param-value>true</param-value>
        </init-param>
        <init-param>
          <param-name>forceResponseEncoding</param-name>
          <param-value>true</param-value>
        </init-param>
      </filter>
      <filter-mapping>
        <filter-name>characterfilter</filter-name>
        <url-pattern>/*</url-pattern>
      </filter-mapping>
    </web-app>
    ```

    