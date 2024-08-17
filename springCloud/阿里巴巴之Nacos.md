#### Nacos

* 组件

  * Sentinel:把流量作为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。

  * Nacos: 一个更易于构建云原生应用的动态服务发现、配置管理和服务管理平台。

  * RocketMQ:-款开源的分布式消息系统， 基于高可用分布式集群技术,提供低延时的、可靠的消息发布与订阅服务。

  * Seata: 阿里巴巴开源产品，一个易于使用的高性能微服务分布式事务解决方案。

  * Alibaba Cloud OSS:阿里云对象存储服务(Object Storage Service,简称OSS) ,是阿里云提供的海量、安全、低成本、高可靠的云存储服务。您可以在任何应用、任何时间、任何地点存储和访问任意类型的数据。

  * Alibaba Cloud SchedulerX:阿里中间件团队开发的一款分布式任务调度产品，提供秒级、精准、高可靠、高可用的定时(基于Cron表达式)任务调度服务。

  * Alibaba Cloud SMS:覆盖全球的短信服务,友好高效、智能的互联化通讯能力,帮助企业迅速搭建客户触达通道。

* Nacos :  Dynamic Naming and Configuration Service 

  * 替代Eureka/Consul做服务注册中心
  * 替代(Config+ Bus)/Consul做服务配置中心和满足动态刷新广播通知

* 注册中心的比较

   <img src="%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BNacos.assets/0f4918b62e401d4fefaeba9b558b34e6.png" alt="img" style="zoom:67%;" />

  *  据说 Nacos 在阿里巴巴内部有超过 10 万的实例运行，已经过了类似双十一等各种大型流量的考验，Nacos默认是AP模式，但也可以调整切换为CP，我们一般用默认AP即可。 

* 进入Nacos官网，下载软件

  * 使用 startup.cmd -m standalone 运行

  * http://127.0.0.1:8848/nacos  访问

  * 给消息提供者增加配置文件（9001服务入住8848的nacos）

    ```yml
    server:
      port :9001
    spring:
      application:
        name: nacos-payment-provider
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848 #配置Nacos地址
    ```

  * 导入服务发现依赖

    ```java
    <!--nacos-discovery-->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-discovery</artifactId>
    </dependency>
    ```

  * 主启动类增加注解

    ```java
    @SpringBootApplication
    @EnableDiscoveryClient
    public class Main9001
    {
        public static void main(String[] args)
        {
            SpringApplication.run(Main9001.class,args);
        }
    }
    ```

  * 启动之后就可以发现存在

    ![1722776902687](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BNacos.assets/1722776902687.png)

    

* 消息的消费者

  * 因为Nacos需要loadbalance作负载均衡，所以需要加这个依赖，其他和上面一样

  * 在请求时，引用**service-url**: **nacos-user-service**

    ```java
    @RestController
    public class OrderNacosController
    {
        @Resource
        private RestTemplate restTemplate;
        @Resource
        private PayFeignSentinelApi payFeignSentinelApi;
    
        @Value("${service-url.nacos-user-service}")
        private String serverURL;
    
        @GetMapping("/consumer/pay/nacos/{id}")
        public String paymentInfo(@PathVariable("id") Integer id)
        {
            String result = restTemplate.getForObject(serverURL + "/pay/nacos/" + id, String.class);
            return result+"\t"+"    我是OrderNacosController83调用者。。。。。。";
        }
        @GetMapping(value = "/consumer/pay/nacos/get/{orderNo}")
        public ResultData getPayByOrderNo(@PathVariable("orderNo") String orderNo)
        {
            return payFeignSentinelApi.getPayByOrderNo(orderNo);
        }
    }
    ```

  

* Nacos的配置服务

  * 建立一个新的module

  * 增加配置依赖 需要在 pom.xml 文件中引入 group ID 为 com.alibaba.cloud 和 artifact ID 为 spring-cloud-starter-alibaba-nacos-config 的 starter： 

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-nacos-config</artifactId>
    </dependency>
    ```

  *  在应用的 /src/main/resources/bootstrap.yaml 配置文件中配置 Nacos Config 地址并引入服务配置： 

    ```yml
    spring:
      application:
        name: nacos-config-client
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848 #Nacos服务注册中心地址
          config:
            server-addr: localhost:8848 #Nacos作为配置中心地址
            file-extension: yaml #指定yaml格式的配置
            group: PROD_GROUP
            namespace: Prod_Namespace
    ```

  * 完成上述两步后，应用会从 Nacos Server 中获取相应的配置，并添加在 Spring Environment 的 PropertySources 中。假设我们通过 Nacos 作为配置中心保存应用服务的部分配置，有以下几种方式实现：

    - BeanAutoRefreshConfigExample：通过将配置信息配置为 bean，支持配置变自动刷新；

    - ConfigListenerExample：监听配置信息；

    - DockingInterfaceExample：对接 Nacos 接口，通过接口完成对配置信息增删改查；

    - ValueAnnotationExample：通过 @Value 注解进行配置信息获取。

      ```java
      @RestController
      @RefreshScope //在控制器类加入@RefreshScope注解使当前类下的配置支持Nacos的动态刷新功能。
      public class NacosConfigClientController
      {
          @Value("${config.info}")
          private String configInfo;
      
          @GetMapping("/config/info")
          public String getConfigInfo() {
              return configInfo;
          }
      }
      ```

      ```yml
      server:
        port: 3377
      
      spring:
        profiles:
      #    active: dev # 表示开发环境
            active: prod # 表示生产环境
      #    active: test # 表示测试环境
      ```

      

  * 配置文件的扫描

    * spring-cloud-starter-alibaba-nacos-config 在加载服务配置时：不仅仅加载了以 dataId 为 ${spring.application.name}.${file-extension:properties } 为前缀的基础配置，还加载了 dataId 为 ${spring.application.name}-${profile}.${file-extension:properties } 的基础配置。

    *  ${spring.application.name}-${spring.profile.active}.${spring.cloud.nacos.config.file-extension} 

      * 以上面的bootstrap配置为例子：spring.application.name是nacos-config-client，spring.profile.active在application配置，是dev，文件格式在bootstrap配置file-extension是yml。所以dataid的文件命名为nacos-config-client-dev-.yml

    * 创建配置

      ![1722785210860](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BNacos.assets/1722785210860.png)

      ​	

    * 配置的东西都可哟获取到，如配置的config.info，而且8848的网页上改了，其他会动态刷新

      ```java
      @RestController
      @RefreshScope //在控制器类加入@RefreshScope注解使当前类下的配置支持Nacos的动态刷新功能。
      public class NacosConfigClientController
      {
          @Value("${config.info}")
          private String configInfo;
      
          @GetMapping("/config/info")
          public String getConfigInfo() {
              return configInfo;
          }
      }
      ```

      

* NameSpace
  *  用于进行租户粒度的配置隔离。不同的命名空间下，可以存在相同的 Group 或 Data ID 的配置。
  * Namespace 的常用场景之一是不同环境的配置的区分隔离， 例如开发测试环境和生产环境的资源（如配置、服务）隔离等。 在没有明确指定 ${spring.cloud.nacos.config.namespace} 配置的情况下， 默认使用的是 Nacos 中 public 命名空间即默认的命名空间。如果需要使用自定义的命名空间，可以通过以下配置来实现： 