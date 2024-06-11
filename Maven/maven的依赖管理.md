#### maven的依赖管理

* 自定义标签，用于控制一系列jar的版本

  ```xml
      <properties>
      <!--自定义标签-->
          <junit.version>5.8.2</junit.version>
      </properties>
      <dependencies>
          <!-- https://mvnrepository.com/artifact/org.junit.jupiter/junit-jupiter-api -->
          <dependency>
              <groupId>org.junit.jupiter</groupId>
              <artifactId>junit-jupiter-api</artifactId>
              <version>${junit.version}</version>
              <scope>test</scope>
          </dependency>
          <!-- https://mvnrepository.com/artifact/org.projectlombok/lombok -->
          <dependency>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok</artifactId>
              <version>1.18.30</version>
              <scope>provided</scope>
          </dependency>
  
      </dependencies>
  ```

  

* 依赖范围：通过设置坐标的依赖范围(scope)，可以设置对应jar包的作用范围:**（编译环境、测试环境、运行环境），这三个称为三种 classpath**

  * compile：编译依赖范围，scope元素的缺省值。使用此依赖范围的 Maven依赖，对于三种 classpath均有效，即该Maven依赖在上述三种classpath均会被引入。例如，log4)在编译、测试、运行过程都是必须的。**默认是他**
  * test：测试依赖范围。使用此依赖范围的 Maven依赖，只对测试 classpath 有效。例如，Junit依赖只有在测试阶段才需要。**主程序会找不到这个jar包**
  * provided：已提供依赖范围。使用此依赖范围的 Maven依赖，只对编译 classpath和测试 classpath有效。例如，servlet-apil依赖对于编译、测试阶段而言是需要的，但是运行阶段，由于外部容器已经提供，故不需要 Maven重复引入该依赖。
  * runtime：运行时依赖范围。使用此依赖范围的 Maven依赖，只对测试 classpath、运行 classpath有效。例如，JDBC 驱动实现依赖，其在编译时只需JDK提供的JDBC 接口即可，只有测试、运行阶段才需要实现了JDBC 接口的驱动。
  * system：系统依赖范围，其效果与provided的依赖范围一致。其用于添加非 Maven 仓库的本地依赖，通过依赖元素dependency中的systemPath元素指定本地依赖的路径。鉴于使用其会导致项目的可移植性降低,一般不推荐使用。
  * import：导入依赖范围，该依赖范围只能与dependencyManagement元素配合使用，其功能是将目标pom.xml文件中dependencyManagement的配置导入合并到当前pom.xml 的
    dependencyManagement中。

* maven下载jar失败解决方案

  * 检查是否能访问中央仓库
  * 检查jar版本是否存在
  * 检查上述问题，删除缓存（即本地仓库的目录对应坐标名文件夹的.lastUpdated文件）

* Build标签

  ```xml
      <build>
  <!--       自定义打包名称 <-->
          <finalName>maventest.war</finalName>
  <!--        自定义文件格式保存位置-->
          <resources>
              <resource>
                  <directory>src/main</directory>
                  <includes>
                      <include>**/*.xml</include>
                  </includes>
              </resource>
          </resources>
  <!--        插件下载-->
          <plugins>
              <plugin>
                  <groupId>org.apache.tomcat.maven</groupId>
                  <artifactId>tomcat7-maven-plugin</artifactId>
                  <version>2.2</version>
                  <configuration>
                      <port>8080</port>
                      <path>/</path>
                      <uriEncoding>UTF-8</uriEncoding>
                      <server>tomcat7</server>
                  </configuration>
              </plugin>
          </plugins>
      </build>
  ```

  

* maven依赖的传递特性

  * 假如有Maven项目A，项目B依赖A，项目C依赖B。那么我们可以说C依赖A。也就是说，依赖的关系为:C一>B一>A，那么我们执行项目C时，会自动把B、A都下载导入到C项目的jfar包文件夹中，这就是依赖的传递性。

  

* maven传递的原则

  * 在A依赖B，B依赖C的前提下，C是否能够传递到A，取决于B依赖C时使用的依赖范围以及配置·

    * B依赖C时使用compile范围:可以传递

    * B依赖C时使用test或provided范围:不能传递，所以需要这样的jar包时，就必须在需要的地方明确配置依赖才可以。

    * B依赖C时，若配置了<**optional**>true</**optional**>标签，则不能传递

      ```xml
              <dependency>
                  <groupId>org.projectlombok</groupId>
                  <artifactId>lombok</artifactId>
                  <version>1.18.30</version>
                  <optional>true</optional>
              </dependency>
      ```

      

  * **不建议修改maven仓库给的坐标的作用范围**

* maven的依赖冲突

  * 短路优先原则
    * A—>B—>C—>D—>E—>X(version 0.0.1)
    * A—F—>X(version 0.0.2)
    * 则A依赖于X(version 0.0.2)。
  * 依赖路径长度相同情况下，则先声明优先”(第二原则)
  * A—>E—>X(version 0.0.1)
  * A—>F—>X(version 0.0.2)
  * 在<depencies></depencies>中，先声明的，路径相同，会优先选择!

* 手动选择依赖

  ```xml
      <dependencies>
          <!-- https://mvnrepository.com/artifact/org.projectlombok/lombok -->
          <dependency>
              <groupId>org.projectlombok</groupId>
              <artifactId>lombok</artifactId>
              <version>1.18.30</version>
              <scope>provided</scope>
  <!--            依赖排除-->
              <exclusions>
                  <exclusion>
                      <groupId></groupId>
                      <artifactId></artifactId>
                  </exclusion>
              </exclusions>
          </dependency>
      </dependencies>
  ```

  

##### maven的继承

* 继承
  * Maven继承是指在Maven的项目中，让一个项目从另一个项目中继承配置信息的机制。继承可以让我们在多个项目中共享同一配置信息简化项目的管理和维护工作。
* 继承作用
  * 在父工程中统—管理项目中的依赖信息。
  * 它的背景是:
    * 对一个比较大型的项目进行了模块拆分。
    * 一个project下面，创建了很多个module。
    * 每一个module都需要配置自己的依赖信息。
  * 在每一个module中各自维护各自的依赖信息很容易发生出入，不易统一管理。
  * 使用同一个框架内的不同jar包，它们应该是同一个版本，所以整个项目中使用的框架版本需要统一。使用框架时所需要的jar包组合（或者说依赖信息组合）需要经过长期摸索和反复调试，最终确定一个可用组合。
  * 这个耗费很大精力总结出来的方案不应该在新的项目中重新摸索。
  * 通过在父工程中为整个项目维护依赖信息的组合既保证了整个项目使用规范、准确的jar包;又能够将以往的经验沉淀下来，节约时间和精力。



* maven工程的依赖关系

  * 因为父工程的不需要打包，所以打包方式为pom文件

  * 首先，在父工程下面new一个子工程

    ![1707225867055](maven%E7%9A%84%E4%BE%9D%E8%B5%96%E7%AE%A1%E7%90%86.assets/1707225867055.png)

  * 子工程的pom，可以发现子工程只有<artifactId>maven_child</artifactId>，因为他剩下两个坐标和父工程一样。

    ```xml
        <parent>
            <groupId>com.wzj.maven</groupId>
            <artifactId>module_maven</artifactId>
            <version>1.0-SNAPSHOT</version>
        </parent>
        <artifactId>maven_child</artifactId>
        <packaging>war</packaging>
        <name>maven_child Maven Webapp</name>
    ```

    

  * 父工程的依赖无条件的继承给子工程，与依赖作用范围无关。但是可能2子工程不需要，为了解决这个问题，需要使用另外一个标签dependencyManagement，这样子工程需要手动选择继承哪些依赖

    ```xml
        <dependencyManagement>
            <dependencies>
                <!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
                <dependency>
                    <groupId>com.alibaba</groupId>
                    <artifactId>druid</artifactId>
                    <version>1.2.8</version>
                </dependency>
            </dependencies>
        </dependencyManagement>
    ```

    

  * 子工程的选择，正常使用依赖标签，但是不指定版本即可，会自动继承父类的版本

    ```xml
        <dependencies>
            </dependency>
                <!-- https://mvnrepository.com/artifact/com.alibaba/druid -->
                <dependency>
                    <groupId>com.alibaba</groupId>
                    <artifactId>druid</artifactId>
                </dependency>
        </dependencies>
    ```

    

* maven的聚合

  * Maven聚合是指将多个项目组织到一个父级项目中，以便一起构建和管理的机制。聚合可以帮助我们更好地管理一组相关的子项目，同时简化它们的构建和部署过程。

  * 聚合作用

    * 1.管理多个子项目:通过聚合，可以将多个子项目组织在一起，方便管理和维护。
    * 2.构建和发布一组相关的项目:通过聚合，可以在一个命令中构建和发布多个相关的项目，简化了部署和维护工作。
    * 3.优化构建顺序:通过聚合，可以对多个项目进行顺序控制，避免出现构建依赖混乱导致构建失败的情况。
    * 4.统—管理依赖项:通过聚合，可以在父项目中管理公共依赖项和插件，避免重复定义。

  * 聚合命令，在父文件的pom中添加，在创建子工程idea默认在父工程添加

    ```xml
        <modules>
    <!--        这是一个子工程路径-->
            <module>maven_child</module>
        </modules>
    ```

    

