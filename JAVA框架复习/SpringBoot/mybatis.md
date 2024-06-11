##### mybatis

* 举例

  * 首先创建bean层

    ```java
    @Data
    public class Article {
        private Integer id;
        private Integer userId;
        private String title;
        private String summary;
        private Integer readCount;
        private LocalDateTime createTime;
        private LocalDateTime updateTime;
    }
    ```

  * 然后创建mapper接口(这里使用了jdk15的文本块，也就是三个双引号)

    ```java
    public interface ArticleMapper {
        @Select("""
    select id, user_id, title, summary, read_count, create_time, update_time
            from article where id = #{articleId}
    """)
        //查询结果ResultAet和POJO对象的属性映射
        @Results(id="BaseArticleMap",value = {
                @Result(id = true,column = "id",property = "id"),
                @Result(column = "user_id",property = "userId"),
                @Result(column = "title",property = "title"),
                @Result(column = "summary",property = "summary"),
                @Result(column = "read_count",property = "readCount"),
                @Result(column = "create_time",property = "createTime"),
                @Result(column = "update_time",property = "updateTime"),
        })
        Article selectById(@Param("articleId") Integer id);
        //插入
        @Insert("""
    insert into article(user_id,title,summary,read_count,create_time,update_time) values (#{userId}
    ,#{title},#{summary},#{readCount},#{createTime},#{updateTime})
    """)
        int insertArticle(Article article);
        //mybatis3.4可以使用使用参数名作为占位符 #={readcount}
        @Update("update article set read_count=#={readCount} where id=#={id}")
        int updataReadCount(Integer id,Integer readCount);
        //删除
        @Delete("delete from article where id=#={id}")
        int deleteById(Integer id);
    }
    ```

  * 配置数据库以及进行驼峰映射和下划线连接映射

    ```properties
    spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
    spring.datasource.url=jdbc:mysql://127.0.0.1:3306/mvc
    spring.datasource.username=root
    spring.datasource.password=123456
    #使其支持驼峰和下划线命名
    mybatis.configuration.map-underscore-to-camel-case=true
    ```

  * 测试类进行测试

    ```java
    @SpringBootTest
    class MybatisTestApplicationTests {
        //mybatis底层实现了静态代理
        @Autowired
        private ArticleMapper mapper;
        @Test
        void contextLoads() {
            Article article = mapper.selectById(1);
            System.out.println(article);
        }
    }
    ```

  * 也可以使用注解使得实体类与数据库列名匹配

    ```java
    public interface ArticleMapper {
        @Select("""
    select id, user_id, title, summary, read_count, create_time, update_time
            from article where id = #{articleId}
    """)
        //查询结果ResultAet和POJO对象的属性映射
        @Results(id="BaseArticleMap",value = {
                @Result(id = true,column = "id",property = "id"),
                @Result(column = "user_id",property = "userId"),
                @Result(column = "title",property = "title"),
                @Result(column = "summary",property = "summary"),
                @Result(column = "read_count",property = "readCount"),
                @Result(column = "create_time",property = "createTime"),
                @Result(column = "update_time",property = "updateTime"),
        })
        Article selectById(@Param("articleId") Integer id);
    }
    ```

    

  * 总结：需要加入mybatis的starter,mysql驱动。创建实体类和mapper接口

    * 在启动上面，加入@MapperScan
    * 在application配置文件中定义数据库连接、mybatis设置，日志，透风明明
    * 在3.4版本，可以使用#=，就可以省略@param注解
    * 注解中的映射：@result

* 结果映射resultMap

  * 使用results可以使数据库的列名与属性名映射，但是每一次写太麻烦，可以使用resultMap进行结果复用

    ```java
    public interface ArticleDao {
        @Select("select id,user_id,title,summary,read_count,create_time, update_time from article" +
                "where user_id =#={userId}")
        @Results(id="BaseArticleMap",value = {
                @Result(id = true,column = "id",property = "id"),
                @Result(column = "user_id",property = "userId"),
                @Result(column = "title",property = "title"),
                @Result(column = "summary",property = "summary"),
                @Result(column = "read_count",property = "readCount"),
                @Result(column = "create_time",property = "createTime"),
                @Result(column = "update_time",property = "updateTime"),
        })
        List<ArticleDao> selectList(Integer userId);
        @Select("select id,user_id,title,summary,read_count,create_time, update_time from article" +
                "where id =#={id}")
        //可以复用
        @ResultMap("BaseArticleMap")
        List<ArticleDao> selectById(Integer id);
    }
    ```

  * 方法二：可以在xml中定义，<resultMap id="xxx">，代码中使用@ResultMap(value=”xml的id”)

    ```java
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE mapper
            PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
            "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    <mapper namespace="wang.zi.jie.bean.Article">
        <resultMap id="ArticleBaseMapper" type="wang.zi.jie.bean.Article">
            <id column="id" property="id"></id>
            <result column="user_id" property="userId"></result>
            <result column="title" property="title"></result>
            <result column="summary" property="summary"></result>
            <result column="read_count" property="readCount"></result>
            <result column="create_time" property="createTime"></result>
            <result column="update_time" property="updateTime"></result>
        </resultMap>
    </mapper>
    ```

    * 在application配置文件中添加

      ```properties
      #指定本地的映射
      mybatis.mapper-locations=classpath:/mappers/**/*.xml
      ```

* SQL提供者

  *  我们能在方法上面直接编写 SQL 语句。使用 Text Block 编写长的语句。方法上编写 SQL 显的不够简洁。 MyBatis 提供了 SQL 提供者的功能。将 SQL 以方法的形式定义在单独的类中。 Mapper 接口通过引用 SQL 提供者中的方法名称，表示要执行的 SQL。 

  *  SQL 提供者有四类@SelectProvider，@InsertProvider，@UpdateProvider，@DeleteProvider 

  * SQL提供者首先创建提供者类，自定义的，类中声明静态方法， 方法体是 SQL 语句并返回 SQL。 

    ```java
    public class SqlProvider {
        public static String selectArticle(){
            return "select * from article where od=#={id";
        }
        public static String updateSql(){
            return "update article set update_time=#={newTime}";
        }
        public static String insertSQL(){
            return """
    insert into article(user_id,title,summary,read_count,create_time,update_time) values (#={userId}
    ,#={title},#={summary},#={readCount},#={createTime},#={updateTime})
    """;
        }
        public static String deleteById(){
            return "delete from article where id=#={id}";
        }
    }
    ```

  * 使用上述注解引用类与方法

    ```java
    public interface ArticleReposity {
        @Select("")
        @Results(id = "BaseMapper", value = {
                @Result(id = true, column = "id", property = "id"),
                @Result(column = "user_id", property = "userId"),
                @Result(column = "read_count", property = "readCount"),
                @Result(column = "create_time", property = "createTime"),
                @Result(column = "update_time", property = "updateTime"),
        })
        Article articleMapper();
        //查询
        @ResultMap("BaseMapper")
        @SelectProvider(type = SqlProvider.class,method = "selectArticle")
        Article selectById(Integer id);
        //更新
        @UpdateProvider(type = SqlProvider.class,method = "updateTime")
        int updateTime(Integer id, LocalDateTime newTime);
        @InsertProvider(type = SqlProvider.class,method = "insertSQL")
        int insertArticle(Article article);
        @DeleteProvider(value = SqlProvider.class,method = "deleteById")
        int deleteById(Integer id);
    }
    ```

  * 可以分别创建 Insert 的提供者， Update 提供者，Delete 提供者，Select 查询者。 每个查询者只提供一种操 作。Select 提供者的方法只提供 Select 语句。





* 一对一

  *  首先建立两张表的bean，并把一个表的bean作为另外一个表的属性

    ```java
    @Data
    public class Article {
        private Integer id;
        private Integer userId;
        private String title;
        private String summary;
        private Integer readCount;
        private LocalDateTime createTime;
        private LocalDateTime updateTime;
        //增加一个一对一关系
        private ArticleDetail articleDetail;
    }
    @Data
    public class ArticleDetail {
        private Integer id;
        private Integer articleId;
        private String content;
    }
    ```

  * 把子语句作为对象传入

    ```java
    public interface ArticleOneToOneMapper {
        //一对一查询
        @Select("""
    select id,article_id,content from article_detail
    where article_id = #{articleId}
    """)
        @Results({
                @Result(id = true, column = "id", property = "id"),
                @Result(column = "article_id", property = "articleId"),
                @Result(column = "content", property = "content")
        })
        ArticleDetail selectDeatil(Integer articleId);
        //查询文章详情包括内容
        @Select("""
    select id,user_id,title,summary,read_count,create_time,update_time,from article where id = #{id}
    """)
        @Results({
                @Result(id = true, column = "id", property = "id"),
                @Result(column = "user_id", property = "userId"),
                @Result(column = "read_count", property = "readCount"),
                @Result(column = "create_time", property = "createTime"),
                @Result(column = "update_time", property = "updateTime"),
                @Result(column = "id", property = "articleDetail",
                        one = @One(select =
                                "com.bjpowernode.orm.repository.ArticleOneToOneMapper.queryContent",
                                fetchType = FetchType.LAZY))
        })
        Article queryAllArticle(Integer id);
    }
    ```

    

* 一对多·

  * mapper代码

    ```java
    ublic interface ArticleOneToManyMapper {
    @Select("""
    select id,article_id,content from comment
    where article_id = #{articleId}
    """)
    @Results(id="CommentMapper",value = {
    @Result(id = true, column = "id", property = "id"),
    @Result(column = "article_id", property = "articleId"),
    @Result(column = "content", property = "content")
    })
    List<CommentPO> queryComments(Integer articleId);
    @Select("""
    select id, user_id,title,summary,
    read_count,create_time,update_time
    from article
    where id = #{id}
    """)
    @Results(id="ArticleBaseMapper",value={
    @Result(id = true, column = "id", property = "id"),
    @Result(column = "user_id", property = "userId"),
    @Result(column = "read_count", property = "readCount"),
    @Result(column = "create_time", property = "createTime"),
    @Result(column = "update_time", property = "updateTime"),
    @Result(column = "id", property = "comments",
    many = @Many(select =
    "com.bjpowernode.orm.repository.ArticleOneToManyMapper.queryComments", fetchType =
    FetchType.LAZY))
    })
    ArticleEntity queryArticleAndComments(Integer id);
    }
    ```

    

* mybatis配置参考

  * 具体配置参考 https://mybatis.org/mybatis-3/zh/configuration.html#settings

  *  设置内容比较多时，可以将设置放到 MyBatis 主配置文件，mybatis.config-location 加载主配置文件

    ```xml
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE configuration
    PUBLIC "-//mybatis.org//DTD Config 3.0//EN"
    "https://mybatis.org/dtd/mybatis-3-config.dtd">
    <configuration>
    <settings>
    <setting name="cacheEnabled" value="true"/>
    www.bjpowernode.com 78 / 200 Copyright©动力节点
    <setting name="lazyLoadingEnabled" value="true"/>
    <setting name="mapUnderscoreToCamelCase" value="true"/>
    </settings>
    <typeAliases>
    <package name="com.bjpowernode.po"/>
    </typeAliases>
    </configuration>
    ```

    

* 连接池

  *  HikariCP 连接池 https://github.com/brettwooldridge/HikariCP/wiki 

  * 连接池配置： https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing 

  * MySQL 连接池配置建议 https://github.com/brettwooldridge/HikariCP/wiki/MySQL-Configuration 

    ```yml
    spring:
    datasource:
    type: com.zaxxer.hikari.HikariDataSource
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/blog?serverTimezone=Asia/Shanghai
    username: root
    password: 123456
    hikari:
    auto-commit: true
    # # connections = ((cpu 核心数 * 2) + 磁盘数量) 近似值。 默认 10
    maximum-pool-size: 10
    #最小连接数，默认 10，不建议设置。默认与 maximum-pool-size 一样大小。推荐使用
    固定大小的连接池
    minimum-idle: 10
    #获取连接时，检测语句
    connection-test-query: select 1
    ###
    # 连接超时，默认 30 秒。
    # 控制客户端在获取池中 Connection 的等待时间，
    # 如果没有连接可用的情况下超过该时间，则抛出 SQLException 异常，
    ###
    connection-timeout: 20000
    #其他属性
    data-source-properties:
    cachePrepStmts: true
    dataSource.cachePrepStmtst: true
    dataSource.prepStmtCacheSize: 250
    dataSource.prepStmtCacheSqlLimit: 2048
    dataSource.useServerPrepStmts: tru
    ```

    