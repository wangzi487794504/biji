##### maven构建

* 构建的定义和过程

  * 项目构建是指将源代码、依赖库和资源文件等转换成可执行或可部署的应用程序的过程，在这个过程中包括编译源代码、链接依赖库、打包和部署等多个步骤。

  * 项目构建是软件开发过程中至关重要的一部分，它能够大大提高软件开发效率，使得开发人员能够更加专注于应用程序的开发和维护，而不必关心应用程序的构建细节。

  * 同时，项目构建还能够将多个开发人员的代码汇合到一起，并能够自动化项目的构建和部署，大大降低了项目的出错风险和提高开发效率。常见的构建工具包括Maven、Gradle、Ant等。

    ![1706968569821](maven%E6%9E%84%E5%BB%BA.assets/1706968569821.png)

* 快速生成get和set的jar包，lombok

  ```xml
  <!-- https://mvnrepository.com/artifact/org.projectlombok/lombok -->
  <dependency>
      <groupId>org.projectlombok</groupId>
      <artifactId>lombok</artifactId>
      <version>1.18.30</version>
      <scope>provided</scope>
  </dependency>
  
  ```

  * @Data注解生成set和get

  * @AllArgsConstructor生成有参构造

  * @NoArgsConstructor生成无参构造

    ![1706969106249](maven%E6%9E%84%E5%BB%BA.assets/1706969106249.png)

* maven的命令构造

  ![1706969136991](maven%E6%9E%84%E5%BB%BA.assets/1706969136991.png)
  * mvn compile ，打开pom所在的目录，使用cmd读取，输入该命令，会生成target目录

    ![1706969664452](maven%E6%9E%84%E5%BB%BA.assets/1706969664452.png)

    ![1706969728372](maven%E6%9E%84%E5%BB%BA.assets/1706969728372.png)

  * mvn clean用于删除target目录

    ![1706970083971](maven%E6%9E%84%E5%BB%BA.assets/1706970083971.png)

  * mvn compile只能编译main的代码，对于test类的不会编译，需要使用mvn test-compile来单独编译test的代码

    ![1706970247735](maven%E6%9E%84%E5%BB%BA.assets/1706970247735.png)

  * mvn test会自动执行test包下的所有测试方法

    ![1706970639966](maven%E6%9E%84%E5%BB%BA.assets/1706970639966.png)

    ![1706970608722](maven%E6%9E%84%E5%BB%BA.assets/1706970608722.png)

    * **如果该方法用test命名就会执行不到，因为maven对测试方法名和类名都有要求。类名必须以Test结尾或开头，方法必须以test开头****

    * 执行完测试命令会生成一个测试报告

      ![1707036659824](maven%E6%9E%84%E5%BB%BA.assets/1707036659824.png)

  * mvn package 打包命令，执行此命令会自动执行上面所有的命令，生成打包文件，打包文件不包含测试程序。

    ![1707039845667](maven%E6%9E%84%E5%BB%BA.assets/1707039845667.png)

  * mvn install 将大包的安装到本地的maven仓库

* 坐标解释

  ```xml
          <dependency>
              <groupId>org.junit.jupiter</groupId>
              <artifactId>junit-jupiter-api</artifactId>
              <version>5.8.2</version>
              <scope>test</scope>
          </dependency>
  ```

  * groupId就是从本地仓库文件夹目录

    ![1707040950538](maven%E6%9E%84%E5%BB%BA.assets/1707040950538.png)

* 插件、指令、周期的关系
  * 周期→包含若干命令→包含若干插件
  * 使用周期命令构建，简化构建过程!
  * 最终进行构建的是插件!