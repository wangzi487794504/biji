#### Mybatis逆向工程

*  所谓的逆向⼯程是：根据数据库表逆向⽣成Java的pojo类，SqlMapper.xml⽂件，以及Mapper接⼝类等。 
* 要完成这个⼯作，需要借助别⼈写好的逆向⼯程插件。
* 思考：使⽤这个插件的话，需要给这个插件配置哪些信息？
  - pojo类名、包名以及⽣成位置。
  - SqlMapper.xml⽂件名以及⽣成位置。
  - Mapper接⼝名以及⽣成位置。
  - 连接数据库的信息。
  - 指定哪些表参与逆向⼯程。

* 逆向工程的实现

  *  第一步：pom中添加逆向工程依赖 

    ```xml
    <!--配置-->
    <!--定制构建过程-->
    <build>
        <!--可配置多个插件-->
        <plugins>
            <!--其中的⼀个插件：mybatis逆向⼯程插件-->
            <plugin>
                <!--插件的GAV坐标-->
                <groupId>org.mybatis.generator</groupId>
                <artifactId>mybatis-generator-maven-plugin</artifactId>
                <version>1.4.1</version>
                <!--允许覆盖-->
                <configuration>
                    <overwrite>true</overwrite>
                </configuration>
                <!--插件的依赖-->
                <dependencies>
                    <!--mysql驱动依赖-->
                    <dependency>
                        <groupId>mysql</groupId>
                        <artifactId>mysql-connector-java</artifactId>
                        <version>8.0.30</version>
                    </dependency>
                </dependencies>
            </plugin>
        </plugins>
    </build>
    
    ```

    

  *  第二步：配置generatorConfig.xml，该⽂件名必须叫做：generatorConfig.xml，该⽂件必须放在类的根路径下 

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE generatorConfiguration
            PUBLIC "-//mybatis.org//DTD MyBatis Generator Configuration 1.0//EN"
            "http://mybatis.org/dtd/mybatis-generator-config_1_0.dtd">
    
    <generatorConfiguration>
        <!--
          targetRuntime有两个值：
              MyBatis3Simple：⽣成的是基础版，只有基本的增删改查。
              MyBatis3：⽣成的是增强版，除了基本的增删改查之外还有复杂的增删改查。
        -->
        <context id="DB2Tables" targetRuntime="MyBatis3">
            <!--防⽌⽣成重复代码-->
            <plugin type="org.mybatis.generator.plugins.UnmergeableXmlMappersPlugin"/>
            <commentGenerator>
                <!--是否去掉⽣成⽇期-->
                <property name="suppressDate" value="true"/>
                <!--是否去除注释-->
                <property name="suppressAllComments" value="true"/>
            </commentGenerator>
            <!--连接数据库信息-->
            <jdbcConnection driverClass="com.mysql.cj.jdbc.Driver"
                            connectionURL="jdbc:mysql://localhost:3306/ziv_mybatis"
                            userId="root"
                            password="root">
            </jdbcConnection>
            <!-- ⽣成pojo包名和位置 -->
            <javaModelGenerator targetPackage="com.ziv.mybatis.pojo" targetProject="src/main/java">
                <!--是否开启⼦包-->
                <property name="enableSubPackages" value="true"/>
                <!--是否去除字段名的前后空⽩-->
                <property name="trimStrings" value="true"/>
            </javaModelGenerator>
            <!-- ⽣成SQL映射⽂件的包名和位置 -->
            <sqlMapGenerator targetPackage="com.ziv.mybatis.mapper" targetProject="src/main/resources">
                <!--是否开启⼦包-->
                <property name="enableSubPackages" value="true"/>
            </sqlMapGenerator>
            <!-- ⽣成Mapper接⼝的包名和位置 -->
            <javaClientGenerator
                    type="xmlMapper"
                    targetPackage="com.ziv.mybatis.mapper"
                    targetProject="src/main/java">
                <property name="enableSubPackages" value="true"/>
            </javaClientGenerator>
            <!-- 表名和对应的实体类名-->
            <table tableName="t_car" domainObjectName="Car"/>
        </context>
    </generatorConfiguration>
    
    
    ```

    

  *  第四步：运行插件 ，双击

    <img src="Mybatis%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B.assets/1709816101098.png" alt="1709816101098" style="zoom:50%;" />

  * 自动生成，包什么都不用建

    <img src="Mybatis%E9%80%86%E5%90%91%E5%B7%A5%E7%A8%8B.assets/1709816134556.png" alt="1709816134556" style="zoom:50%;" />



###### mybatis分页

* mysql的limit后⾯两个数字：

  - 第⼀个数字：startIndex（起始下标。下标从0开始。）
  - 第⼆个数字：pageSize（每⻚显示的记录条数）

* 前端页码pageNum要传送给服务器。每页显示的记录条数pageSize也要传送给服务器。

* 公式：limit (pageNumpageNum-1)*pageSize,pageSize

* 分页插件PageHelper插件

  * 第一步：引入依赖

    ```xml
    <dependency>
        <groupId>com.github.pagehelper</groupId>
        <artifactId>pagehelper</artifactId>
        <version>5.3.2</version>
    </dependency>
    ```

  * 在mybatis-config.xml中配置插件

    ```xml
    <plugins>
        <plugin interceptor="com.github.pagehelper.PageInterceptor"></plugin>
    </plugins>
    ```

    

##### 注解开发

* 