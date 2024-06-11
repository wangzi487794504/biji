##### 什么是maven

* maven结构

  ![1706947528712](maven%E5%85%A5%E9%97%A8.assets/1706947528712.png)
  * bin:含有Maven的运行脚本
  * boot:含有plexus-classworlds类加载器框架
  * conf:含有Maven的核心配置文件
  * lib:含有Maven运行时所需要的Java类库
  * LICENSE、NOTICE、README.txt:针对Maven版本，第三方软件等简要介绍

* 环境变量

  * 配置bin到path

  * 验证成功

    ![1706947730835](maven%E5%85%A5%E9%97%A8.assets/1706947730835.png)

* 修改配置文件

  * 我们需要需改maven/conf/settings.xml配置文件，来修改maven的一些默认配置。我们主要休要修改的有三个配置:

    * 1.依赖本地缓存位置(本地仓库位置)

    * 2.maven下载镜像\

      ```xml
        <mirrors>
      	 <mirror>
            <id>alimaven</id>
            <name>aliyun maven</name>
            <url>http://maven.aliyun.com/nexus/content/groups/public/</url>
            <mirrorOf>central</mirrorOf>        
          </mirror>
        </mirrors>
      ```

      * 配置中央仓库镜像

    * 3.maven选用编译硕目的jdk版本

      * 在**profiles**标签中配置

* GAVP

  * Maven工程相对之前的项目，多出一组gavp属性，gav需要我们在创建项目的时候指定，p有默认值，我们先行了解下这组属性的含义:
  * Maven中的GAVP是指Groupld、Artifactld、Version、Packaging等四个属性的缩写，其中前三个是必要的，而Packaging属性为可选项。这四个属性主要为每个项目在maven仓库中做一个标识，类似人的姓-名!有了具体标识，方便后期项目之间相互引用依赖等!
  * 规则
    *  GroupID格式: com.{公司/BU}.业务线.[子业务线]，最多4级。
      * 说明:{公司/BU}例如: alibaba/taobao/tmallaliexpress 等BU一级;子业务线可选。
      * 举例: com.taobao.tddl 或 com.alibaba.sourcing.multilang
    *  ArtifactID格式:产品线名-模块名。语义不重复不遗漏，先到仓库中心去查证一下。
      * 举例: tc-client / uic-api / tair-tool / bookstore
    * Version版本号格式推荐:主版本号.次版本号.修订号
      * 主版本号:当做了不兼容的API修改，或者增加了能改变产品方向的新功能。
      * 次版本号:当做了向下兼容的功能性新增（新增类、接口等)）。
      * 修订号:修复bug，没有修改方法签名的功能加强，保持API兼容性。例如:初始一1.0.0修改bug → 1.0.1功能调整一1.1.1等
    * Packaging定义规则:
      * 指示将项目打包为什么类型的文件，idea根据packaging值，识别maven项目类型!
      * packaging属性为jar(默认值)，代表普通的Java工程，打包以后是.Jar结尾的文件。
      * packaging 属性为 war，代表Java的web工程，打包以后.war结尾的文件。
      * packaging 属性为pom，代表不会打包，用来做继承的父工程。

* 创建maven文件

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <project xmlns="http://maven.apache.org/POM/4.0.0"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
      <!--这是pom的版本-->
      <modelVersion>4.0.0</modelVersion>
      <groupId>com.wzj.maven</groupId>
      <artifactId>module_maven</artifactId>
      <!--版本，SNAPSHOT是快照-->
      <version>1.0-SNAPSHOT</version>
      <!--打包方式，不写默认值为jar-->
      <packaging>war</packaging>
  </project>
  ```

  * 导入jar包，从https://mvnrepository.com/

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <project xmlns="http://maven.apache.org/POM/4.0.0"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
             xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
        <!--这是pom的版本-->
        <modelVersion>4.0.0</modelVersion>
        <groupId>com.wzj.maven</groupId>
        <artifactId>module_maven</artifactId>
        <!--版本，SNAPSHOT是快照-->
        <version>1.0-SNAPSHOT</version>
        <!--打包方式-->
        <packaging>war</packaging>
        <dependencies>
            <!-- https://mvnrepository.com/artifact/org.junit.jupiter/junit-jupiter-api -->
            <dependency>
                <groupId>org.junit.jupiter</groupId>
                <artifactId>junit-jupiter-api</artifactId>
                <version>5.8.2</version>
                <scope>test</scope>
            </dependency>
        </dependencies>
    </project>
    ```

    

* web工程的创建

  * 第一种，创建普通的java的maven，然后在pom中设置打包方式为war包，自动转换为web项目。然后在module添加web.xml，一定要在maven给你的webapp目录下

    <img src="maven%E5%85%A5%E9%97%A8.assets/1706966412307.png" alt="1706966412307" style="zoom:50%;" />

    * 添加web.xml

      <img src="maven%E5%85%A5%E9%97%A8.assets/1706966484779.png" alt="1706966484779" style="zoom:50%;" />

    * 最终结果

      <img src="maven%E5%85%A5%E9%97%A8.assets/1706966513320.png" alt="1706966513320" style="zoom:50%;" />

  * 方法二：使用插件，在module直接右键选择这个插件

    ![1706966781200](maven%E5%85%A5%E9%97%A8.assets/1706966781200.png)

  * 方法三，直接使用idea自带的maven骨架，缺点是生成的web.xml的版本低，是二点几

    ![1706967490385](maven%E5%85%A5%E9%97%A8.assets/1706967490385.png)



* maven使用tomcat，在运行配置中选择tomcat即可

  ![1706967875001](maven%E5%85%A5%E9%97%A8.assets/1706967875001.png)
  * war模式：将WEB工程以war包的形式上传到Tomcat服务器 ，存放于服务器的webapps目录下；
    war模式这种可以称之为是发布模式，看名字也知道，这是先打成war包，再发布；
  * **war exploded模式：**将WEB工程以当前文件夹的位置关系上传到服务器；也就是说不会再Tomcat服务器的webapps目录下。war exploded模式这种可以称之为开发调试模式，默认是项目所在目录的target目录下。





* Maven项目工程结构

  * Maven是一个强大的构建工具，它提供一种标准化的项目结构，可以帮助开发者更容易地管理项目的依赖、构建、测试和发布等任条。以下是Maven Web程序的文件结构及每个文件的作用:

    ![1706968222572](maven%E5%85%A5%E9%97%A8.assets/1706968222572.png)

