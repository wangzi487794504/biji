#### MyBatis

* JDBC的不足：

  * SQL语句写在java代码中，修改SQL语句不方便，违反开发原则OCP，对扩展开放，对修改关闭
  * 传值到bean是繁琐的

* MyBatis

  * ORM思想 O(Object)对象 R(Relational)关系型数据库 M（Mapping）映射
  * MyBatis是一个半自动化的ORM，因为MyBatis框架中SQL语句是需要程序员自己编写的。

* 开发第一个mybatis程序

  * resources日录：放在这个目录当中的，一般都是资源文件，配置文件。直接放到resources目录下的资源，等同于放到了类的根路径下。

  * 打包方式：jar包

  * 开发步骤

    * 第一步:打包方式jar

    * 第二步:引入依赖

      * mybatis依赖、 mysql驱动依赖

    * 第三步:编写mybatis核心配置文件:mybatis-config.xml

      * 注意:第一:这个文件名不是必须叫做mybatis-config.xml，可以用其他的名字。只是大家都采用这个名字。
      * 第二:这个文件存放的位置也不是固定的，可以随意，但一般情况下，会放到类的根路径下。
      * 从XML 中构建 SqlSessionFactory通过官方的这句话，你能想到什么呢?
      * 第一:在MyBatis中一定是有一个很重要的对象，这个对象是:SqlSessionFactory对象。
      * 第二:SqlSessionFactory对象的创建需要XML。XML是什么?它一定是一个配置文件。

    * 第四步：编写xxxMapper.xml

      * mybatis主要有两个配置文件
      * 其中一个是:mybatis-config.xml，这是核心配置文件，主要配置连接数据库的信息等。**这个只有一个**
      * 另一个是:xxxMapper.xml，这个文件是专门用来编写SQL语句的配置文件。**这个可以有多个**

    * 第五步:在mybatis-config.xml文件中指定XxxxMapper.xml文件的路径:
      <mapper resource="CarMapper.xml"/>注意:resource属性会自动从类的根路径下开始查找资源。

    * 第六步：编写MyBatis程序

      ```java
      public class Main {
          public static void main(String[] args) throws IOException {
              System.out.println("Hello world!");
              SqlSessionFactoryBuilder sqlSessionFactoryBuilder=new SqlSessionFactoryBuilder();
              //你可以随便创建一个流去读取mybatis-config.xml，这里使用mybatis自带的，默认从根目录查找
              //InputStream inputStream=new FileInputStream("")
              InputStream inputStream= Resources.getResourceAsStream("mybatis-config.xml");
              SqlSessionFactory sqlSessionFactory = sqlSessionFactoryBuilder.build(inputStream);
              SqlSession sqlSession = sqlSessionFactory.openSession();
              //执行sql语句
              //sqlSession.insert("传入的是id");
              int count = sqlSession.insert("a");
              System.out.println(count);
              //必须要手动提交
              sqlSession.commit();
          }
      }
      ```

      

      * 在MyBatis当中，负责执行SQL语句的那个对象叫做什么呢?SqlSession
      * SqlSession是专门用来执行SQL语句的，是一个Java程序和数据库之间的一次会话。
      * 要想获取SqlSession对象，需要先获取SqlSessionFactory对象，通过SqlSessionFactory工厂来生产SqlSession对象。
      * 怎么获职SqlsessionFactory对象呢?需要首先获取SqlSessionFactoryBuilder对象。通过SqlSessionFactoryBuilder对象的build方法，来获取一个SqlSessionFactory对象

* Mybatis的一些细节

  * sql语句的分号可以省略，不省略也不会报错

  * 方法名称中遇到resource，基本都是从根目录开始

  * InputStream is = new FileInputStream("d:\\mybatis-config.xml");采用这种方式也可以。

    * 缺点:可移植性太差，程序不够健壮。可能会移植到其他的操作系统当中。导致以上路径无效，还需要修改java代码中的路径。这样违背了0CP原则。验证了:
      mybatis核心配置文件的名字，不一定是:mybatis-config.xml。可以是其它名字。

  * mybatis核心配置文件存放的路径，也不一定是在类的根路径下。可以放到其它位置。但为了项目的移植性，健壮性，最好将这个配置文件放到类路径下面。

  * **InputStream is = classLoader.getsystemclassLoader().getResourceAsStream("mybatis-config.xml");ClassLoader.getSystemClassloader()获取系统的类加载器。这种方式也可以。其实Resources.getResourceAsStream实现代码就是classloader****

    <img src="MyBatis%E5%85%A5%E9%97%A8.assets/1709110839294.png" alt="1709110839294" style="zoom:50%;" />

* mybatis事务管理

  * 在mybatis-config.xml中，可以使用下面的配置对事务进行管理

    *  在 MyBatis 中有两种类型的事务管理器（也就是 type="[JDBC|MANAGED]"）： <transactionManager type="JDBC"/>

    * JDBC – 这个配置直接使用了 JDBC 的提交和回滚设施，它依赖从数据源获得的连接来管理事务作用域。**即使用的是connection.commit()方法**

      ```java
          public Transaction newTransaction(DataSource ds, TransactionIsolationLevel level, boolean autoCommit) {
              return new JdbcTransaction(ds, level, autoCommit, this.skipSetAutoCommitOnClose);
          }
      ```

      * 是JdbcTransaction事务

    * MANAGED – 这个配置几乎没做什么。它从不提交或回滚一个连接，而是让容器来管理事务的整个生命周期（比如 JEE 应用服务器的上下文）。**即mybatis不再负责事务的管理了。事务管理交给其它容器来负责。例如:spring。**

      * 这个就没有管理事务，默认为true

* 关于mybatis常见的日志组件有哪些，mybatis已经集成了一些日志组件

  * 其中STDOUT_LOGGING是标准日志，mybatis已经实现了这种标准日志。mybatis框架本身已经实现了这种标准。只要开启即可。怎么开启呢?在mybatis-config.xml文件中使用settings标签进行配置开启。

    ```xml
        <settings>
            <setting name="logImpl" value="STDOUT_LOGGING"/>
        </settings>
    ```

    ![1709125045426](MyBatis%E5%85%A5%E9%97%A8.assets/1709125045426.png)

  * 除了STDOUT_LOGGING，其余的都需要导入jar包

    * logback实现了SLF4J的规范