##### spring引入mybatis

* 一共分为十一步

  * 第一步：准备数据库表

  - - 使用t_act表（账户表）

  - 第二步：IDEA中创建一个模块，并引入依赖

  - - spring-context
    - spring-jdbc
    - mysql驱动
    - mybatis
    - mybatis-spring：**mybatis提供的与spring框架集成的依赖**
    - 德鲁伊连接池
    - junit

  - 第三步：基于三层架构实现，所以提前创建好所有的包

  - - com.powernode.bank.mapper
    - com.powernode.bank.service
    - com.powernode.bank.service.impl
    - com.powernode.bank.pojo

  - 第四步：编写pojo

  - - Account，属性私有化，提供公开的setter getter和toString。

  - 第五步：编写mapper接口

  - - AccountMapper接口，定义方法

  - 第六步：编写mapper配置文件

  - - 在配置文件中配置命名空间，以及每一个方法对应的sql。

  - 第七步：编写service接口和service接口实现类

  - - AccountService
    - AccountServiceImpl

  - 第八步：编写jdbc.properties配置文件

  - - 数据库连接池相关信息

  - 第九步：编写mybatis-config.xml配置文件

  - - 该文件可以没有，大部分的配置可以转移到spring配置文件中。
    - 如果遇到mybatis相关的系统级配置，还是需要这个文件。

  - 第十步：编写spring.xml配置文件

  - - 组件扫描
    - 引入外部的属性文件
    - 数据源
    - SqlSessionFactoryBean配置

  - - - 注入mybatis核心配置文件路径
      - 指定别名包
      - 注入数据源

  - - Mapper扫描配置器

  - - - 指定扫描的包

  - - 事务管理器DataSourceTransactionManager

  - - - 注入数据源

  - - 启用事务注解

  - - - 注入事务管理器

  - 第十一步：编写测试程序，并添加事务，进行测试