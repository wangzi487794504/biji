#### redis客户端

* 目前主流的Redis的Java客户端有三种
  - Jedis和Lettuce：这两个主要是提供了Redis命令对应的API，方便我们操作Redis，而SpringDataRedis又对这两种做了抽象和封装，因此我们后期会直接以SpringDataRedis来学习。
  - Redisson：是在Redis基础上实现了分布式的可伸缩的java数据结构，例如Map、Queue等，而且支持跨进程的同步机制：Lock、Semaphore等待，比较适合用来实现特殊的功能需求。



* Jedis的使用

  * 导入pom

    ```xml
            <dependency>
                <groupId>redis.clients</groupId>
                <artifactId>jedis</artifactId>
                <version>5.0.0</version>
            </dependency>
    ```

  * 测试

    ```java
    public class JedisTest {
        private Jedis jedis=null;
        @Before
        public void beforeInit(){
            jedis = new Jedis("47.103.213.244",6379);
            jedis.auth("123456");
            jedis.select(0);
        }
        @Test
        public  void test1(){
            jedis.set("name", "wangzijie");
            String name = jedis.get("name");
            System.out.println(name);
        }
        @After
        public void close(){
            if (jedis!=null){
                jedis.close();
            }
        }
    }
    ```

  * 连接池

    * `Jedis`本身是线程不安全的，并且频繁的创建和销毁连接会有性能损耗，因此我们推荐大家使用Jedis连接池代替Jedis的直连方式。

    * 新建一个`com.blog.util`，用于存放我们编写的工具类

    * 但后面我们使用`SpringDataRedis`的时候，可以直接在`yml`配置文件里配置这些内容

      ```java
      public class JedisConnectionFactory {
          private static final JedisPool jedisPool;
          static {
              //配置连接池
              JedisPoolConfig config=new JedisPoolConfig();
              config.setMaxTotal(8);
              config.setMaxIdle(8);
              config.setMinIdle(6);
              config.setMaxWait(Duration.ofSeconds(2));
              jedisPool=new JedisPool(config,"47.103.213.244",6379,1000,"123456");
          }
          public static Jedis getJedis(){
              return jedisPool.getResource();
          }
      }
      ```



* SpringDataRedis
  * SpringData是Spring中数据操作的模块，包含对各种数据库的集成，其中对Redis的集成模块就叫做SpringDataRedis
  * 官网地址：https://spring.io/projects/spring-data-redis
    - 提供了对不同Redis客户端的整合（Lettuce和Jedis）
    - 提供了RedisTemplate统一API来操作Redis
    - 支持Redis的发布订阅模型
    - 支持Redis哨兵和Redis集群
    - 支持基于Lettuce的响应式编程
    - 支持基于JDK、JSON、字符串、Spring对象的数据序列化及反序列化
    - 支持基于Redis的JDKCollection实现
  * SpringDataRedis中提供了RedisTemplate工具类，其中封装了各种对Redis的操作。并且将不同数据类型的操作API封装到了不同的类型中：