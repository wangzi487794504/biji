#### 多redis的配置

* 虽然实际的项目中，不太可能出现一个项目连接多个redis实例的情况，但是，当真的出现了，也是允许的，这种时候，就不能直接使用默认的，需要我们自己来声明ConnectionFactory和 RedisTemplate。

* 配置文件信息

  ```properties
  spring:
    redis:
      host: 127.0.0.1
      port: 6379
      password:
      lettuce:
        pool:
          max-active: 32
          max-wait: 300
          max-idle: 16
          min-idle: 8
      database: 0
    local-redis:
      host: 127.0.0.1
      port: 6379
      database: 0
      password:
      lettuce:
        pool:
          max-active: 16
          max-wait: 100
          max-idle: 8
          min-idle: 4
  ```

  

* 对应的配置类，采用Lettuce，基本设置如下，套路都差不多，先读取配置，初始化ConnectionFactory，然后创建RedisTemplate实例，设置连接工厂

  ```java
  @Configuration
  public class RedisAutoConfig {
  
      @Bean
      public LettuceConnectionFactory defaultLettuceConnectionFactory(RedisStandaloneConfiguration defaultRedisConfig,
              GenericObjectPoolConfig defaultPoolConfig) {
          LettuceClientConfiguration clientConfig =
                  LettucePoolingClientConfiguration.builder().commandTimeout(Duration.ofMillis(100))
                          .poolConfig(defaultPoolConfig).build();
          return new LettuceConnectionFactory(defaultRedisConfig, clientConfig);
      }
  
      @Bean
      public RedisTemplate<String, String> defaultRedisTemplate(
              LettuceConnectionFactory defaultLettuceConnectionFactory) {
          RedisTemplate<String, String> redisTemplate = new RedisTemplate<>();
          redisTemplate.setConnectionFactory(defaultLettuceConnectionFactory);
          redisTemplate.afterPropertiesSet();
          return redisTemplate;
      }
  
      @Bean
      @ConditionalOnBean(name = "localRedisConfig")
      public LettuceConnectionFactory localLettuceConnectionFactory(RedisStandaloneConfiguration localRedisConfig,
              GenericObjectPoolConfig localPoolConfig) {
          LettuceClientConfiguration clientConfig =
                  LettucePoolingClientConfiguration.builder().commandTimeout(Duration.ofMillis(100))
                          .poolConfig(localPoolConfig).build();
          return new LettuceConnectionFactory(localRedisConfig, clientConfig);
      }
  
      @Bean
      @ConditionalOnBean(name = "localLettuceConnectionFactory")
      public RedisTemplate<String, String> localRedisTemplate(LettuceConnectionFactory localLettuceConnectionFactory) {
          RedisTemplate<String, String> redisTemplate = new RedisTemplate<>();
          redisTemplate.setConnectionFactory(localLettuceConnectionFactory);
          redisTemplate.afterPropertiesSet();
          return redisTemplate;
      }
  
      @Configuration
      @ConditionalOnProperty(name = "host", prefix = "spring.local-redis")
      public static class LocalRedisConfig {
          @Value("${spring.local-redis.host:127.0.0.1}")
          private String host;
          @Value("${spring.local-redis.port:6379}")
          private Integer port;
          @Value("${spring.local-redis.password:}")
          private String password;
          @Value("${spring.local-redis.database:0}")
          private Integer database;
  
          @Value("${spring.local-redis.lettuce.pool.max-active:8}")
          private Integer maxActive;
          @Value("${spring.local-redis.lettuce.pool.max-idle:8}")
          private Integer maxIdle;
          @Value("${spring.local-redis.lettuce.pool.max-wait:-1}")
          private Long maxWait;
          @Value("${spring.local-redis.lettuce.pool.min-idle:0}")
          private Integer minIdle;
  
          @Bean
          public GenericObjectPoolConfig localPoolConfig() {
              GenericObjectPoolConfig config = new GenericObjectPoolConfig();
              config.setMaxTotal(maxActive);
              config.setMaxIdle(maxIdle);
              config.setMinIdle(minIdle);
              config.setMaxWaitMillis(maxWait);
              return config;
          }
  
          @Bean
          public RedisStandaloneConfiguration localRedisConfig() {
              RedisStandaloneConfiguration config = new RedisStandaloneConfiguration();
              config.setHostName(host);
              config.setPassword(RedisPassword.of(password));
              config.setPort(port);
              config.setDatabase(database);
              return config;
          }
      }
  
  
      @Configuration
      public static class DefaultRedisConfig {
          @Value("${spring.redis.host:127.0.0.1}")
          private String host;
          @Value("${spring.redis.port:6379}")
          private Integer port;
          @Value("${spring.redis.password:}")
          private String password;
          @Value("${spring.redis.database:0}")
          private Integer database;
  
          @Value("${spring.redis.lettuce.pool.max-active:8}")
          private Integer maxActive;
          @Value("${spring.redis.lettuce.pool.max-idle:8}")
          private Integer maxIdle;
          @Value("${spring.redis.lettuce.pool.max-wait:-1}")
          private Long maxWait;
          @Value("${spring.redis.lettuce.pool.min-idle:0}")
          private Integer minIdle;
  
          @Bean
          public GenericObjectPoolConfig defaultPoolConfig() {
              GenericObjectPoolConfig config = new GenericObjectPoolConfig();
              config.setMaxTotal(maxActive);
              config.setMaxIdle(maxIdle);
              config.setMinIdle(minIdle);
              config.setMaxWaitMillis(maxWait);
              return config;
          }
  
          @Bean
          public RedisStandaloneConfiguration defaultRedisConfig() {
              RedisStandaloneConfiguration config = new RedisStandaloneConfiguration();
              config.setHostName(host);
              config.setPassword(RedisPassword.of(password));
              config.setPort(port);
              config.setDatabase(database);
              return config;
          }
      }
  }
  ```

  