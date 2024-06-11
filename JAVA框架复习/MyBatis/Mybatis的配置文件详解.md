#### Mybatis的配置文件

```xml
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <settings>
        <setting name="logImpl" value="SLF4J"/>
    </settings>
    default表示默认使用的环境。-->
默认环境什么意思?当你使用mybatis创建SqlSessionFactory对象的时候，没有指定环境的话，默认使用哪个环境
    <environments default="development">
        <environment id="development">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:3306/mvc?serverTimezone=UTC&amp;allowPublicKeyRetrieval=true&amp;useSSL=false"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
<!--        指定mappping文件的路径，resource是从根目录查找，url是从绝对路径查找，一般不用，必须要加上file:///
，file:///是本地文件传输协议-->
        <mapper resource="CarMapping.xml"/>
<!--        <mapper url="file:///G:\ideaspace\MyBatisStudy\maven_001\src\main\resources\CarMapping.xml"/>-->
    </mappers>
</configuration>
```



```java
<!DOCTYPE configuration
        PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-config.dtd">
<configuration>
    <!--java.util.Properties类，是一个Map集合，key和valve都是String类型-->
    <!--作properties标签中可以配置很多属性-->
<!--    这种已经被淘汰了，现在是使用引入外部文件的方式-->
<!--    <properties>-->
<!--        <property name="jdbc.driver" value="com.mysql.cj.jdbc.Driver"/>-->
<!--        <property name="jdbc.url" value="jdbc:mysql://127.0.0.1:3306/mvc?serverTimezone=UTC&amp;allowPublicKeyRetrieval=true&amp;useSSL=false"/>-->
<!--        <property name="jdbc.username" value="root"/>-->
<!--        <property name="jdbc.password" value="123456"/>-->
<!--    </properties>-->
<!--    这种常用-->
<!--    <properties resource="jdbc.properties"></properties>-->
<!--    也可以使用绝对路径-->
    <properties url="file:///d:/jdbc.properties"></properties>
    <settings>
        <setting name="logImpl" value="SLF4J"/>
    </settings>
    <!--可以配置多个environment环境标签-->
    <environments default="development">
        <!--default 属性指明默认使用哪个环境配置-->
        <!--一般一个数据库会对应一个SqlSessionFactory对象-->
        <!--一个环境environment会与对应一个SqlSessionFactory对象-->
        <!--开发环境配置-->
        <environment id="development">
            <!--
    transactionManager标签：
        1.作用：配置事务管理器。指定mybatis具体使用什么方式去管理事务。
        2.type属性有两个值(不区分大小写)：
            a) JDBC：使用原生的JDBC代码来管理事务
                conn.setAutoCommit(false);
                ...
                conn.commit();
            b) MANAGED：mybatis不再负责事务的管理，将事务交给其他容器管理，如spring。
                     当mybatis找不到容器的支持时：没有事务
        3.mybatis中提供了一个事务管理器接口：Transaction
            该接口下有两个实现类：
                JdbcTransaction
                ManagedTransaction
            type中写哪个，底层机会实例化哪个对象
-->
            <transactionManager type="JDBC"/>
            <!--
    dataSource配置：
        1.dataSource被称为数据源。
        2.dataSource作用：为程序提供Connection对象。(只要是给程序提供Connection对象的，都可以叫做数据源)
        3.数据源实际上是一套规范。JDK中有这套规范：javax.sql.DataSource (这个数据源的规范，实际上就是JDK规定的)
        4.我们也可以自己实现javax.sql.DataSource接口，编写数据源组件。
            比如自己写一个数据库连接池
        5.常见的数据源组件(也称常见的数据库连接池)：
            druid c3p0 dbcp...
        6.type属性用来指定数据源的类型，就是指定用什么方式来获取Connection对象
            type有三个值，必须三选一：
            UNPOOLED:不使用数据库连接池技术。每次都创建新的Connection对象
            POOLED:使用mybatis自己的数据库连接池
            JNDI:继承第三方的数据库连接池

            JNDI是一套规范，大部分web容器都是先了JNDI规范
                例如：Tomcat、Jetty、WebLogic、WehSphere
            JNDI是Java命名目录接口。Tomcat服务器实现了这个规范。

-->
            <dataSource type="POOLED">
<!--                使用美元符号大括号的方式-->
                <property name="driver" value="${jdbc.driver}"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:3306/mvc?serverTimezone=UTC&amp;allowPublicKeyRetrieval=true&amp;useSSL=false"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
            </dataSource>
        </environment>
        <environment id="developmentother">
            <transactionManager type="JDBC"/>
            <dataSource type="POOLED">
                <!--提醒:正常使用连接池的话，池中有很多参数是需要设置的。设置好参数，可以让连接池发挥的更好。事半功倍的效果。-->
<!--具体连接池当中的参数如何配置呢?需要反复的根据当前业务情况进行测试。-->
                <!--poolMaximumActiveConnections:连接池当中最多的正在使用的连接对象的数量上限。最多有多少个连接可以活动。默认值10-->
                <property name="driver" value="com.mysql.cj.jdbc.Driver"/>
                <property name="url" value="jdbc:mysql://127.0.0.1:3306/zs?serverTimezone=UTC&amp;allowPublicKeyRetrieval=true&amp;useSSL=false"/>
                <property name="username" value="root"/>
                <property name="password" value="123456"/>
                <property name="poolMaximumActiveConnections " value="10"/>
                <property name="poolMaximumCheckoutTime" value="30000"/>
            </dataSource>
        </environment>
    </environments>
    <mappers>
<!--        指定mappping文件的路径，resource是从根目录查找，url是从绝对路径查找，一般不用，必须要加上file:///
，file:///是本地文件传输协议-->
        <mapper resource="CarMapping.xml"/>
<!--        <mapper url="file:///G:\ideaspace\MyBatisStudy\maven_001\src\main\resources\CarMapping.xml"/>-->
    </mappers>
</configuration>
```

