##### String事务

* 什么是事务

- - 在一个业务流程当中，通常需要多条DML（insert delete update）语句共同联合才能完成，这多条DML语句必须同时成功，或者同时失败，这样才能保证数据的安全。
  - 多条DML要么同时成功，要么同时失败，这叫做事务。
  - 事务：Transaction（tx）

* 事务的四个处理过程：

- - 第一步：开启事务 (start transaction)
  - 第二步：执行核心业务代码
  - 第三步：提交事务（如果核心业务处理过程中没有出现异常）(commit transaction)
  - 第四步：回滚事务（如果核心业务处理过程中出现异常）(rollback transaction)

- 事务的四个特性：

- - A 原子性：事务是最小的工作单元，不可再分。
  - C 一致性：事务要求要么同时成功，要么同时失败。事务前和事务后的总量不变。
  - I 隔离性：事务和事务之间因为有隔离性，才可以保证互不干扰。
  - D 持久性：持久性是事务结束的标志



### Spring实现事务的两种方式

- 编程式事务(就是在代码中编写，基本不用)

- - 通过编写代码的方式来实现事务的管理。

- 声明式事务

- - 基于注解方式
  - 基于XML配置方式

* PlatformTransactionManager接口：spring事务管理器的核心接口。在**Spring6**中它有两个实现：

  - DataSourceTransactionManager：支持JdbcTemplate、MyBatis、Hibernate等事务管理。
  - JtaTransactionManager：支持分布式事务管理。

* 如果要在Spring6中使用JdbcTemplate，就要使用DataSourceTransactionManager来管理事务。（Spring内置写好了，可以直接用。）

* 案例引入

  ```java
  @Repository("accountDao")
  public class AccountDaoImpl implements AccountDao {
      @Resource(name = "jdbcTemplate")
      private JdbcTemplate jdbcTemplate;
      @Override
      public Account seleceByActno(String actno) {
          String sql="select actno,balance from t_user where actno=?";
          Account account = jdbcTemplate.queryForObject(sql, new BeanPropertyRowMapper<>(Account.class), actno);
          return account;
      }
      @Override
      public int updata(Account account) {
          String sql="update t_user set balance=? where actno=?";
          int count = jdbcTemplate.update(sql, account.getBalance(), account.getActno());
          return count;
      }
  }
  ```

  ```java
  @Service("accountService")
  public class AccountServiceImpl implements AccountService {
      @Resource(name = "accountDao")
      private AccountDao accountDao;
      @Override
      @Transactional  //写在类上就是类的所有方法都执行事务
      public void transfer(String fromActno, String toActno, double money) {
          int count=0;
          Account account = accountDao.seleceByActno(fromActno);
          if (account.getBalance()<money){
              throw new RuntimeException("余额不足");
          }
          //余额充足
          Account account1 = accountDao.seleceByActno(toActno);
          account.setBalance(account.getBalance()-money);
          account1.setBalance(account1.getBalance()+money);
          count = accountDao.updata(account);
          count +=accountDao.updata(account1);
          if (count==2){
              System.out.println("转账成功");
          }
          else {
              throw new RuntimeException("转账失败");
          }
      }
  }
  ```

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xmlns:aop="http://www.springframework.org/schema/aop"
         xmlns:tx="http://www.springframework.org/schema/tx"
         xmlns:context="http://www.springframework.org/schema/context"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
          http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd
          http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
  http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd">
  
      <context:component-scan base-package="wang.zi.jie"></context:component-scan>
      <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
          <property name="driverClassName" value="com.mysql.cj.jdbc.Driver"></property>
          <property name="username" value="root"></property>
          <property name="password" value="123456"></property>
          <property name="url" value="jdbc:mysql://127.0.0.1:3306/mvc"></property>
      </bean>
      <!--    配置jdbcTemplate-->
      <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
          <property name="dataSource" ref="dataSource"></property>
      </bean>
  <!--    配置事务管理器-->
      <bean id="txManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
          <property name="dataSource" ref="dataSource"></property>
      </bean>
  <!--    开启事务注解驱动器-->
      <tx:annotation-driven transaction-manager="txManager"></tx:annotation-driven>
  </beans>
  ```

  * 需要增加一些约束文件



* 事务的传播行为

  * 什么是事务的传播行为，举例：

    * 在service类中有a()方法和b()方法，a()方法上有事务，b()方法上也有事务，当a()方法执行过程中调用了b()方法，事务是如何传递的？合并到一个事务里？还是开启一个新的事务？这就是事务传播行为。
    * 事务传播行为在spring框架中被定义为枚举类型：

  * spring支持七种传播范围

    * REQUIRED：支持当前事务，如果不存在就新建一个(默认)**【没有就新建，有就加入】**
    * SUPPORTS：支持当前事务，如果当前没有事务，就以非事务方式执行**【有就加入，没有就不管了】**
    * MANDATORY：必须运行在一个事务中，如果当前没有事务正在发生，将抛出一个异常**【有就加入，没有就抛异常】**
    * REQUIRES_NEW：开启一个新的事务，如果一个事务已经存在，则将这个存在的事务挂起**【不管有没有，直接开启一个新事务，开启的新事务和之前的事务不存在嵌套关系，之前事务被挂起】**
    * NOT_SUPPORTED：以非事务方式运行，如果有事务存在，挂起当前事务**【不支持事务，存在就挂起】**
    * NEVER：以非事务方式运行，如果有事务存在，抛出异常**【不支持事务，存在就抛异常】**
    * NESTED：如果当前正有一个事务在进行中，则该方法应当运行在一个嵌套式事务中。被嵌套的事务可以独立于外层事务进行提交或回滚。如果外层事务不存在，行为就像REQUIRED一样。**【有事务的话，就在这个事务里再嵌套一个完全独立的事务，嵌套的事务可以独立的提交和回滚。没有事务就和****REQUIRED一样。****】**

  * 默认是REQUIRED（**这些操作就是让你选择究竟是同一个事务还是不同事务，同一个事务就会全部回滚，不同事务只会回滚出现异常的那个，剩下那个不回滚**）

  * 举例：

    ```java
    @Service("accountService")
    public class AccountServiceImpl implements AccountService {
        @Resource(name = "accountDao")
        private AccountDao accountDao;
        @Override
        @Transactional  //写在类上就是类的所有方法都执行事务
        public void transfer(String fromActno, String toActno, double money) {
            int count=0;
            Account account = accountDao.seleceByActno(fromActno);
            if (account.getBalance()<money){
                throw new RuntimeException("余额不足");
            }
            //余额充足
            Account account1 = accountDao.seleceByActno(toActno);
            account.setBalance(account.getBalance()-money);
            account1.setBalance(account1.getBalance()+money);
            count = accountDao.updata(account);
            count +=accountDao.updata(account1);
            if (count==2){
                System.out.println("转账成功");
            }
            else {
                throw new RuntimeException("转账失败");
            }
        }
        @Resource(name = "accountService2")
        private AccountService accountService;
        @Override
        @Transactional(propagation = Propagation.REQUIRED)
        public void save(Account account) {
            accountDao.insert(account);//他保存04账户
            //这里调用dao的insert方法
            Account account1=new Account("act003",1000.0);//他保存03账户
            //一号service执行save方法时去调用二号
            accountService.save(account1);
        }
    }
    ```

    ```java
    @Service("accountService2")
    public class AccountServiceImpl2 implements AccountService {
        @Resource(name = "accountDao")
        private AccountDao accountDao;
        @Override
        public void transfer(String fromActno, String toActno, double money) {
    
        }
        @Override
        @Transactional(propagation = Propagation.REQUIRED)
        public void save(Account account) {
            accountDao.insert(account);
        }
    }
    ```

    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <beans xmlns="http://www.springframework.org/schema/beans"
           xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xmlns:aop="http://www.springframework.org/schema/aop"
           xmlns:tx="http://www.springframework.org/schema/tx"
           xmlns:context="http://www.springframework.org/schema/context"
           xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
            http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd
            http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
    http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd">
    
        <context:component-scan base-package="wang.zi.jie"></context:component-scan>
        <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
            <property name="driverClassName" value="com.mysql.cj.jdbc.Driver"></property>
            <property name="username" value="root"></property>
            <property name="password" value="123456"></property>
            <property name="url" value="jdbc:mysql://127.0.0.1:3306/mvc"></property>
        </bean>
        <!--    配置jdbcTemplate-->
        <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
            <property name="dataSource" ref="dataSource"></property>
        </bean>
    <!--    配置事务管理器-->
        <bean id="txManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
            <property name="dataSource" ref="dataSource"></property>
        </bean>
    <!--    开启事务注解驱动器-->
        <tx:annotation-driven transaction-manager="txManager"></tx:annotation-driven>
    </beans>
    ```

    ```xml\
    <?xml version="1.0" encoding="UTF-8"?>
    <configuration>
        <loggers>
            <!--
                level指定日志级别，从低到高的优先级：
                    ALL < TRACE < DEBUG < INFO < WARN < ERROR < FATAL < OFF
            -->
            <root level="DEBUG">
                <appender-ref ref="spring6log"/>
            </root>
        </loggers>
        <appenders>
            <!--输出日志信息到控制台-->
            <console name="spring6log" target="SYSTEM_OUT">
                <!--控制日志输出的格式-->
                <PatternLayout pattern="%d{yyyy-MM-dd HH:mm:ss SSS} [%t] %-3level %logger{1024} - %msg%n"/>
            </console>
        </appenders>
    ```

    

    ![1710484351966](spring%E4%BA%8B%E5%8A%A1.assets/1710484351966.png)
    * 可以发现日志显示创建了new transaction，然后第二个业务也加入到第一个participating in existing transaction

    

    

    

    

    

* 事务隔离级别

  * 事务隔离级别类似于教室A和教室B之间的那道墙，隔离级别越高表示墙体越厚。隔音效果越好。

    数据库中读取数据存在的三大问题：（三大读问题）

    - **脏读：读取到没有提交到数据库的数据，叫做脏读。（即A事务刚写到缓存里的数据就能被事务B读到）**
    - **不可重复读：在同一个事务当中，第一次和第二次读取的数据不一样。**
    - **幻读：读到的数据是假的。（脑子想象的数据与真实数据不同，就是多线程并发）**

    事务隔离级别包括四个级别：

    - 读未提交：READ_UNCOMMITTED

    - - 这种隔离级别，存在脏读问题，所谓的脏读(dirty read)表示能够读取到其它事务未提交的数据。

    - 读提交：READ_COMMITTED（**mysql默认级别**）

    - - 解决了脏读问题，其它事务提交之后才能读到，但存在不可重复读问题。

    - 可重复读：REPEATABLE_READ（**orcle默认级别**）

    - - 解决了不可重复读，可以达到可重复读效果，只要当前事务不结束，读取到的数据一直都是一样的。但存在幻读问题。

    - 序列化：SERIALIZABLE

    - - 解决了幻读问题，事务排队执行。不支持并发。

    ![1710486594496](spring%E4%BA%8B%E5%8A%A1.assets/1710486594496.png)

    * 读未提交意味着在内存中有

* 测试

  * 一个提交演示

    ```java
    @Service("i1")
    public class IsolationService1 {
    
        @Resource(name = "accountDao")
        private AccountDao accountDao;
    
        // 1号
        // 负责查询
        // 当前事务可以读取到别的事务没有提交的数据。
        @Transactional(isolation = Isolation.READ_UNCOMMITTED)
        // 对方事务提交之后的数据我才能读取到。
    //    @Transactional(isolation = Isolation.READ_COMMITTED)
        public void getByActno(String actno) {
            Account account = accountDao.seleceByActno(actno);
            System.out.println("查询到的账户信息：" + account);
        }
    }
    ```

    ```java
    @Service("i2")
    public class IsolationService2 {
        @Resource(name = "accountDao")
        private AccountDao accountDao;
        // 2号
        // 负责insert
        @Transactional
        public void save(Account act) {
            accountDao.insert(act);
            // 睡眠一会
            try {
                Thread.sleep(1000 * 20);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    ```

    ```java
      @Test
        public void testIsolation1(){
            ApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml");
            IsolationService1 i1 = applicationContext.getBean("i1", IsolationService1.class);
            i1.getByActno("act-004");
        }
    
        @Test
        public void testIsolation2(){
            ApplicationContext applicationContext = new ClassPathXmlApplicationContext("spring.xml");
            IsolationService2 i2 = applicationContext.getBean("i2", IsolationService2.class);
            Account act = new Account("act-004", 1000.0);
            i2.save(act);
        }
    ```

    * 可以发现在内存中能获取到信息

      ![1710501846381](spring%E4%BA%8B%E5%8A%A1.assets/1710501846381.png)

* 事务超时

  * @Transactional(timeout = 10) 设置超时时间是10秒钟。默认是-1，没有超时时间。

  * 超时时间只计算DML时间，而不是整个方法的运行时间

    ```java
        @Transactional(timeout = 10)
        public void save(Account act) {
            accountDao.insert(act);
            // 睡眠一会
            try {
                Thread.sleep(1000 * 20);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    ```

    * 想这个只计算accountDao.insert(act);，下面代码不会被计算的。**它是在最后一条DML语句执行之前的代码都计入时间，之后的不计入（这是一个坑）**
    * **当然，如果想让整个方法的所有代码都计入超时时间的话，可以在方法最后一行添加一行无关紧要的DML语句。**
    * 超时后会自动回滚

* 只读事务

  * @Transactional(readOnly = true)，就不能增删改。在该事务执行过程中只允许select语句执行，delete insert update均不可执行。
  * 该特性的作用是：**启动spring的优化策略。提高select语句执行效率。**
  * 如果该事务中确实没有增删改操作，建议设置为只读事务。

* 异常回滚事务

  * 可以选择当发生哪些异常才回滚事务
  * @Transactional(rollbackFor = RuntimeException.class)表示只有发生RuntimeException异常或该异常的子类异常才回滚。
  * 也可以设置哪些异常不回滚
    * @Transactional(noRollbackFor = NullPointerException.class)

* 事务的全注解开发

  ```java
  @Configuration
  @ComponentScan("wang.zi.jie")//组件扫描
  @EnableTransactionManagement //开启事务注解
  public class SpringConfig6 {
      //Spring框架看到bean注解后会调用这个被标注的方法，这个方法的返回值是java对象，这个java对象会自动纳入Spring容器
      //这个对象被视为一个bean，名字是dataSource
      @Bean(name="dataSource")
      public DruidDataSource getDataSource(){
          DruidDataSource dataSource=new DruidDataSource();
          dataSource.setDriverClassName("com.mysql.cj.jdbc.Driver");
          dataSource.setUrl("jdbc:mysql://127.0..0.1:3306/mvc");
          dataSource.setUsername("root");
          dataSource.setPassword("123456");
          return dataSource;
      }
      @Bean(name = "jdbcTemplate")//spring在调用方法是会自动传入dataSource对象
      public JdbcTemplate getJdbcTemplate(DataSource dataSource){
          JdbcTemplate jdbcTemplate = new JdbcTemplate();
          jdbcTemplate.setDataSource(dataSource);
          return jdbcTemplate;
      }
  
      @Bean
      public DataSourceTransactionManager getDataSourceTransactionManager(DataSource dataSource){
          DataSourceTransactionManager dataSourceTransactionManager = new DataSourceTransactionManager();
          dataSourceTransactionManager.setDataSource(dataSource);
          return dataSourceTransactionManager;
      }
  }
  ```

  



##### xml的声明式事务

```java
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xmlns:aop="http://www.springframework.org/schema/aop"
       xmlns:tx="http://www.springframework.org/schema/tx"
       xmlns:context="http://www.springframework.org/schema/context"
       xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd
        http://www.springframework.org/schema/aop http://www.springframework.org/schema/aop/spring-aop.xsd
        http://www.springframework.org/schema/context http://www.springframework.org/schema/context/spring-context.xsd
http://www.springframework.org/schema/tx http://www.springframework.org/schema/tx/spring-tx.xsd">

    <context:component-scan base-package="wang.zi.jie"></context:component-scan>
    <bean id="dataSource" class="com.alibaba.druid.pool.DruidDataSource">
        <property name="driverClassName" value="com.mysql.cj.jdbc.Driver"></property>
        <property name="username" value="root"></property>
        <property name="password" value="123456"></property>
        <property name="url" value="jdbc:mysql://127.0.0.1:3306/mvc"></property>
    </bean>
    <!--    配置jdbcTemplate-->
    <bean id="jdbcTemplate" class="org.springframework.jdbc.core.JdbcTemplate">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
<!--    配置事务管理器-->
    <bean id="txManager" class="org.springframework.jdbc.datasource.DataSourceTransactionManager">
        <property name="dataSource" ref="dataSource"></property>
    </bean>
<!--    开启事务注解驱动器-->
    <tx:annotation-driven transaction-manager="txManager"></tx:annotation-driven>
    
    <tx:advice id="txAdvice" transaction-manager="txManager">
        <tx:attributes>
<!--            之前所讲的属性都可以配置-->
            <tx:method name="transfer" propagation="REQUIRED"/>
<!--            也支持模糊匹配，就是所有的以save开头的方法-->
            <tx:method name="save*" propagation="REQUIRED" rollback-for="java.lang.Throwable"></tx:method>
        </tx:attributes>
    </tx:advice>
<!--    配置切面-->
    <aop:config>
<!--        切点-->
        <aop:pointcut id="txPointcut" expression="execution(* wang.zi.jie..*(..))"/>
<!--        切面=通知加上切点-->
        <aop:advisor advice-ref="txAdvice" pointcut-ref="txPointcut"></aop:advisor>
    </aop:config>
</beans>
```

