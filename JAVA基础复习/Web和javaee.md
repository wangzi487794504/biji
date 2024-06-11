#### 系统架构

* 系统架构的形式
  * BS   特殊的CS 优点:升级方便，维护成本低。不需要安装软件，只需要打开浏览器即可。缺点：速度慢，不安全，体验差
  * CS 优点：速度快：大部分数据集成到软件上了，很少量的数据从服务器端传送过来服务器压力小，安全。缺点：升级维护麻烦，每一个客户端软件都需要升级
* WEB服务器软件
  * Tomcat(Web服务器,java实现的，必须要有jre)
  * Jetty（Web服务器）
  * jBOSS（应用服务器）
  * WebLogic应用服务器）
  * WebSphere应用服务器）
* 应用服务器和WEB服务器的关系?
  * 应用服务器实现了java EE的所有规范。(java EE有13个不同的规范。)WEB服务器只实现了Java EE中的Servlet + JSP两个核心的规范。
  * 通过这个讲解说明了:应用服务器是包含WEB服务器的。
  * 用过jBOSS服务器的同学应该很清楚，jBOSS中内嵌了一个Tomcat服务器。



* 关于Tomcat服务器的目录

  *  bin:这个目录是Tomcat服务器的命令文件存放的目录，比如:启动Tomcat，关闭Tomcat等。
  *  conf:这个目录是Tomcat服务器的配置文件存放目录。(server.xml文件中可以配置端口号，默认Tomcat端口是8080) lib:这个目录是Tomcat服务器的核心程序目录，因为Tomcat服务器是Java语言编写的，这里的jar包里面都是class文件。
  * logs:Tomcat服务器的日志目录，Tomcat服务器启动等信息都会在这个目录下生成日志文件。
  *  temp:Tomcat服务器的临时目录。存储临时文件。
  *  webapps:这个目录当中就是用来存放大量的webapp (web application:.web应用)
  * work:这个目录是用来存放JSP文件翻译之后的java文件以及编译之后的class文件。

* 启动Tomcat

  * bin目录下有一个文件: startup.bat,通过它可以启动Tomcat服务器。
  *  xxx.bat文件是个什么文件? bat文件是windows操作系统专用的, bat文件是批处理文件，这种文件中可以编写大量的windows的dos命令，然后执行bat文件就相当于批量的执行dos命令。
  *  startup.sh，这个文件在windows当中无法执行，在Linux环境当中可以使用。在Linux环境下能够执行的是shell命令，大量的shell命令编写在shell文件当中，然后执行这个shell文件可以批量的执行shell命令。
  *  tomcat服务器提供了bat和sh文件，说明了这个tomcat服务器的通用性。
  * 分析startup.bat文件得出，执行这个命令，实际上最后是执行: catalina.bat文件。
  *  catalina.bat文件中有这样一行配置:MAINCLASS=org.apache.catalina.startup.Bootstrap(这个类就是main方法所在的类。)
  *  tomcat服务器就是Java语言写的，既然是java语言写的，那么启动Tomcat服务器就是执行main方法。
  * 启动Tomcat服务器只配置path对应的bin目录是不行的。有两个环境变量需要配置: 
    * JAVA_HOME=JDK的根
    * CATALINA_HOME=Tomcat服务器的根
  * 关闭Tomcat : .stop (shutdown.bat文件重命名为stop.bat，为什么?原因是shutdown命令和windows中的关机命令冲突。所以修改一下。)

* 启动一个web应用

  * 第一步:找到CATALINA_HOME\webapps目录
  * 因为所有的webapp要放到webapps目录下。(没有为什么，这是Tomcat服务器的要求。如果不放到这里，Tomcat服务器找不到你的应用。)
  * 第二步:在CATALINA_HOME\webapps目录下新建一个子目录，起名:oa，这个目录名oa就是你这个webapp的名字。
  * 第三步:在oa目录下新建资源文件，例如: index.html，编写index.html文件的内容。
  * 第四步:启动Tomcat服务器
  * 第五步:打开浏览器，在浏览器地址栏上输入这样的URL:http://127.0.0.1:8080/oa/index.html

* 协议和规范

  <img src="%E7%B3%BB%E7%BB%9F%E6%9E%B6%E6%9E%84.assets/1697086616657.png" alt="1697086616657" style="zoom:80%;" />

* Servlet本质
  * 充当SUN公司的角色，制定Servlet规范
  * javax.servlet.Servlet接口
  * 充当Tomcat服务器的开发者
  * 充当Webapp的开发者
  *  BankServlet implements Servlet UserListServlet implements Servleto UserLoginServlet implements Servlet·通过我们的分析:对于我们javaweb程序员来说，我们只需要做两件事:
    * 编写一个类实现Servlet接口。将编写的类配置到配置文件中
    * 在配置文件中:指定请求路径和类名的关系。
  * 注意:这个配置文件的文件名不能乱来。固定的。这个配置文件的存放路径不能乱来。固定的。
  * 文件名、文件路径都是SUN公司制定的Servlet规范中的明细。
  * 严格意义上来说Servlet其实并不是简单的一个接口:
  * Servlet规范中规定了:
    * 一个合格的webapp应该是一个怎样的目录结构。
    * 一个合格的webapp应该有一个怎样的配置文件。
    * 一个合格的webapp配置文件路径放在哪里。
    * 一个合格的webapp中java程序放在哪里。这些都是Servlet规范中规定的。
    * Tomcat服务器要遵循Servlet规范。JavaWEB程序员也要遵循这个Servlet规范。这样Tomcat服务器和webapp才能解耦合。



###### Servlet实现

* servlet
  * 第一步:在webapps目录下新建一个目录，起名crm (这个crm就是webapp的名字)。当然，也可以是其它项目，比如银行项目，可以创建一个目录bank，办公系统可以创建—个oa。注意:crm就是这个webapp的根
  * 第二步:在webapp的根下新建一个目录: WEB-INF
    注意:这个目录的名字是Servlet规范中规定的，必须全部大写，必须一模一样。必须的必须。
  * 第三步:在WEB-INF目录下新建一个目录: classes
    注意:**这个目录的名字必须是全部小写的classes。**这也是Servlet规范中规定的。另外这个目录下一定存放的是Java程序编译，之后的class文件(这里存放的是字节码文件)。
  * 第四步:在WEB-INF目录下新建—个目录:lib
    注意:这个目录不是必须的。但如果一个webapp需要第三方的jar包的话，这个jar包要放到这个lib目录下，**这个目录的名字也不能随意编写，必须是全部小写的lib。**例如java语言连接数据库需要数据库的驱动jar包。那么这个jar包就一定要放到lib目录下。这Servlet规范中规定的。
  * 第五步:在WEB-INF目录下新建—个文件: web.xml
    注意:这个文件是必须的，这个文件名必须叫做web.xml。这个文件必须放在这里。**一个合法的webapp，web.xml文件是必须的，这个web.xml文件就是一个配置文件，在这个配置文件中描述了请求路径和Servlet类之间的对照关系。**这个文件最好从其他的webapp中拷贝，最好别手写。没必要。复制粘贴
  * 第六步:编写一个Java程序，这个java程序也不能随意开发，这个java程序必须实现Servlet接口。这个Servlet接口不在JDK当中。(因为Servlet不是JavaSE了。Servlet属于JavaEE，是另外的一套类库。) **Servlet接口(Servlet.class文件）是Oracle提供的。(最原始的是sun公司提供的。)Servlet接口是JavaEE的规范中的一员。**Tomcat服务器实现了Servlet规范，所以Tomcat服务器也需要使用Servlet接口。Tomcat服务器中应该有这个接口，Tomcat服务器的CATALINA_HOMENlib目录下有一个servlet-api.jar，解压这个servlet-api.jar之后，你会看到里面有一个Servlet.class文件。
  * 第七步:编译我们编写的HelloServlet
    重点:你怎么能让你的HelloServlet编译通过呢?配置环境变量CLASSPATHCLASSPATH=.;C:ldevlapache-tomcat-10.0.12Nliblservlet-api.jar
  * 第八步：将编译好的class文件复制到classes文件夹中
  * 第九步:在web.xml文件中编写配置信息，让"请求路径"和"Servlet类名"关联在一起。这一步用专业术语描述:在web.xml文件中注册Servlet类。
* javaEE版本
  * JavaEE目前最高版本是 JavaEE8
  * JavaEE被Oracle捐献了，Oracle将JavaEE规范捐献给Apache了。Apache把java换名了，以后不叫JavaEE了，以后叫做jakarta EE，以后没有JavaEE了。以后都叫做Jakarta EE。
  * JavaEE8版本升级之后的"javaEE 9"，不再是"javaEE9"这个名字了，叫做jakartaEE9，JavaEE8的时候对应的Servlet类名是:javax.servlet.Servlet
  * jakartaEE的时候对应的Servlet类名是: jakarta.servlet.Servlet(包名都换了)
  * **如果你之前的项目还是在使用javax.servlet.Servlet，那么你的项目无法直接部署到Tomcat10+版本上。你只能部署到Tomcat9-版本上。在Tomcat9以及Tomcat9之前的版本中还是能够识别javax.servlet这个包。**