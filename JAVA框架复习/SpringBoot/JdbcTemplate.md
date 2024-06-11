##### JdbcTemplate

* 使用 JdbcTemplate 我们提供自定义 SQL, Spring 执行这些 SQL 得到记录结果集。

* ==SpringBoot中提供了操作数据库的两个模板类，JdbcTemplate 和 NamedParameterJdbcTemplate 类，是自动配置的，可以使用@Autowire 注入到自己的 Bean 中。开箱即用==

* 点击DataSourceAutoConfiguration

  ```java
  @AutoConfiguration(before = SqlInitializationAutoConfiguration.class)
  @ConditionalOnClass({ DataSource.class, EmbeddedDatabaseType.class })
  @ConditionalOnMissingBean(type = "io.r2dbc.spi.ConnectionFactory")
  @EnableConfigurationProperties(DataSourceProperties.class)
  @Import(DataSourcePoolMetadataProvidersConfiguration.class)
  public class DataSourceAutoConfiguration {
      
  }
  
  //点击DataSourceProperties，这个就是配置参数
  @ConfigurationProperties(prefix = "spring.datasource")
  public class DataSourceProperties implements BeanClassLoaderAware, InitializingBean {
  
  	private ClassLoader classLoader;
  	private boolean generateUniqueName = true;
  	private String name;
  	private Class<? extends DataSource> type;
  	private String driverClassName;
  	private String url;
  }
  ```

* **Spring Boot 支持多种数据库连接池，优先使用 HikariCP，其次是 Tomcat pooling，再次是 Commons DBCP2，如果以上都没有，最后会使用 Oracle UCP 连接池。**当项目中 starter 依赖了 spring-boot-starter-jdbc 或者 spring-boot-starter-data-jpa 默认添加 HikariCP 连接池依赖，也就是默认使用 HikariCP 连接池。

* JdbcTemplateAutoConfiguration 自动配置了 JdbcTemplate 对象，交给 JdbcTemplateConfiguration 创建了JdbcTemplate 对象。并对 JdbcTemplate 做了简单的初始设置（QueryTimeout，maxRows 等）。

  ```java
  @AutoConfiguration(after = DataSourceAutoConfiguration.class)
  @ConditionalOnClass({ DataSource.class, JdbcTemplate.class })
  @ConditionalOnSingleCandidate(DataSource.class)
  @EnableConfigurationProperties(JdbcProperties.class)
  @Import({ DatabaseInitializationDependencyConfigurer.class, JdbcTemplateConfiguration.class,
  		NamedParameterJdbcTemplateConfiguration.class })
  public class JdbcTemplateAutoConfiguration {
  
  }
  
  
  @Configuration(proxyBeanMethods = false)
  @ConditionalOnMissingBean(JdbcOperations.class)
  class JdbcTemplateConfiguration {
  
  	@Bean
  	@Primary
  	JdbcTemplate jdbcTemplate(DataSource dataSource, JdbcProperties properties) {
  		JdbcTemplate jdbcTemplate = new JdbcTemplate(dataSource);
  		JdbcProperties.Template template = properties.getTemplate();
  		jdbcTemplate.setFetchSize(template.getFetchSize());
  		jdbcTemplate.setMaxRows(template.getMaxRows());
  		if (template.getQueryTimeout() != null) {
  			jdbcTemplate.setQueryTimeout((int) template.getQueryTimeout().getSeconds());
  		}
  		return jdbcTemplate;
  	}
  
  }
  ```



* **SpringBoot 能够自动执行 DDL，DML 脚本。两个脚本文件名称默认是 schema.sql 和 data.sql(创建在resource下)。脚本文件在类路径中自动加载。**
* 自动执行脚本还涉及到 spring.sql.init.mode 配置项：

- - always：总是执行数据库初始化脚本，每次启动SpringBoot项目，脚本文件都会执行一次
  - never：禁用数据库初始化

- ```properties
  pring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
  spring.datasource.url=jdbc:mysql://127.0.0.1:3306/mvc
  spring.datasource.username=root
  spring.datasource.password=123456
  
  #设置执行数据库脚本
  #always这个是项目每启动一次就执行，never是不执行
  spring.sql.init.mode=never
  ```





* JdbcTemplate 提供了丰富、实用的方法，主要有以下几种类型的方法：

- - （1）execute 方法：可以用于执行任何 SQL 语句，常用来执行 DDL 语句。

    ```java
    @SpringBootTest
    class JdbcApplicationTests {
        @Resource
        private JdbcTemplate jt;
        @Test
        void contextLoads() {
            String sql = "select count(*) as ct from article";
            Integer count = jt.queryForObject(sql, Integer.class);
            System.out.println(count);
        }
    }
    ```

    * 查询一行

      ```java
          @Test
          void testQuery() {
              // 查询单行数据
              // 在SQL语句中使用?充当占位符
              String sql = "select * from article where id = ?";
              // 参数1：SQL
              // 参数2：查询结果返回值要转换成的类型
              //    BeanPropertyRowMapper 将查询结果集封装到指定类型的对象中，
              //          属性的赋值规则：列名与属性名称完全匹配或驼峰自动映射
              // 参数3：可变参数，SQL中占位符的填充数据
              // 使用该方法必须保证可以查出数据，并且结果只能是一行数据，否则会报错
              ArticlePO articlePO = jt.queryForObject(sql, new BeanPropertyRowMapper<>(ArticlePO.class), 1);
              // ArticlePO(id=1, userId=2101, title=SpringBoot 核心注解, summary=核心注解的主要作用, readCount=8976,
              // createTime=2023-01-16T12:11:12, updateTime=2023-01-16T12:11:19)
              System.out.println(articlePO);
          }
      ```

    * 这个BeanPropertyRowMapper实现了RowMapper接口，因此可以自定义实现类，只要实现RowMapper接口即可

      ```java
      @FunctionalInterface
      public interface RowMapper<T> {
          @Nullable
          T mapRow(ResultSet rs, int rowNum) throws SQLException;
      }
      ```

      ```java
      //自己实现    
      @Test
          public void testMapper(){
              String sql = "select * from article where id = 1";
              // T mapRow(ResultSet rs, int rowNum) throws SQLException;
              jt.queryForObject(sql, (rs,rownum)->{
                  var id = rs.getInt("id");
                  var userId = rs.getInt("user_id");
                  var title = rs.getString("title");
                  var summary = rs.getString("summary");
                  var readCount = rs.getInt("read_count");
                  var createTime = new Timestamp(rs.getTimestamp("create_time").getTime()).toLocalDateTime();
                  var updateTime = new Timestamp(rs.getTimestamp("update_time").getTime()).toLocalDateTime();
                  // 返回查询结果返回值转换成的类型的对象
                  return new ArticlePO(id, userId, title, summary, readCount, createTime, updateTime);
              });
          }
      ```

      

  - （2）update、batchUpdate 方法：用于执行新增、修改与删除等语句。

    ```java
    @Test
    void testUpdate() {
        String sql = """
        update article
        set title = ?
        where id = ?
        """;
        // 返回影响数据库的条数
        // 参数1：SQL
        // 参数2：可变参数，SQL中占位符的填充数据
        int count = jdbcTemplate.update(sql, "Java", 2);
        System.out.println(count); // 1
    }
    ```

    

  - （3）query 和 queryForXXX 方法：用于执行查询相关的语句。

  - （4）call 方法：用于执行数据库存储过程和函数相关的语句。



* #### NamedParameterJdbcTemplate

  * 使用JdbcTemplate访问数据库，占位符使用?，向占位符填充数据时，只能按照占位符的顺序按位填充

  * `NamedParameterJdbcTemplate 可以在 SQL 语句部分**使用“:命名参数”作为占位符,** 对参数命名`

  * ==NamedParameterJdbcTemplate的使用方式和JdbcTemplate一样，但是**NamedParameterJdbcTemplate** 能够接受**命名的参数**，通过具名的参数提供代码的可读性，JdbcTemplate 使用的是参数索引的方式。==

  * NamedParameterJdbcTemplate是对JdbcTemplate包装，执行SQL访问数据库时还是通过JdbcTemplate，NamedParameterJdbcTemplate可以将SQL转换为JdbcTemplate可以执行的SQL

  * NamedParameterJdbcTemplate他其实封装了JdbcTemplate

    ```java
    public class NamedParameterJdbcTemplate implements NamedParameterJdbcOperations {
        public static final int DEFAULT_CACHE_LIMIT = 256;
        private final JdbcOperations classicJdbcTemplate;
        private volatile ConcurrentLruCache<String, ParsedSql> parsedSqlCache = new ConcurrentLruCache(256, NamedParameterUtils::parseSqlStatement);
    
        public NamedParameterJdbcTemplate(DataSource dataSource) {
            Assert.notNull(dataSource, "DataSource must not be null");
            this.classicJdbcTemplate = new JdbcTemplate(dataSource);
        }
    ```

  * 举例

    ```java
        @Test
        void testNameParam() {
            // 使用“:命名参数”作为占位符
            String sql = " select count(*) as ct from article " +
                    "where user_id=:uid and read_count > :num ";
            // 使用Map提供填充数据，key为命名参数名，value填充的值
            Map<String, Object> params = new HashMap<>();
            params.put("uid", 2101);
            params.put("num", 10);
            // 参数1：SQL
            // 参数2：填充占位符的数据
            // 参数3：返回值值封装的类型
            Integer count = namedParameterJdbcTemplate.queryForObject(sql, params, Integer.class);
            System.out.println(count); // 1
        }
    ```

  