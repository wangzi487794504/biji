#### Sentinal

*  Spring Cloud Alibaba 集成的开箱即用限流降级方案来自 [Sentinel](https://github.com/alibaba/Sentinel)，其以流量为切入点，从流量控制、熔断降级、系统负载保护等多个维度保护服务的稳定性。 

* Sentinel分为两个部分

  * 核心库(Java客户端)不依赖任何框架/库,能够运行于所有Java运行时环境，同时对Dubbo / Spring Cloud等框架也有较好的支持。
  * 控制台(Dashboard) 基于Spring Boot开发,打包后可以直接运行，不需要额外的Tomcat等应用容器。
  * 前台的端口号是8080，后台的端口号是8719

* 下载jar包

  * 登录 [Releases · alibaba/Sentinel (github.com)](https://github.com/alibaba/Sentinel/releases) 

  * 注意：8080不能被占用

  * 使用java -jar运行

    * 注意不能有中文，中文会一直在请求
    * 登录127.0.0.1:8080查看
    * 账号和密码都是sentinel

  * springcloud接入

    ```xml
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    ```

  * 配置文件

    ```yml
    server:
      port: 8401
    spring:
      application:
        name: cloudalibaba-sentinel-service
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848         #Nacos服务注册中心地址
        sentinel:
          transport:
            dashboard: localhost:8080 #配置Sentinel dashboard控制台服务地址
            port: 8719 #默认8719端口，假如被占用会自动从8719开始依次+1扫描,直至找到未被占用的端口
          web-context-unify: false # controller层的方法对service层调用不认为是同一个根链路
    ```

  * 先访问一下请求，他才能扫描到 [127.0.0.1:8401/testA](http://127.0.0.1:8401/testA) ，它是懒加载，有流量才加载

    ![1722823958627](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/1722823958627.png)

* 流量控制

  *  Sentinel能够对流量进行控制，主要是监控应用的QPS流量或者并发线程数等指标，如果达到指定的阈值时，就会被流量进行控制，以避免服务被瞬时的高并发流量击垮，保证服务的高可靠性。参数见最下方： 

    * 资源名：资源的唯一名称，默认就是请求的接口路径，可以自行修改，但是要保证唯一。

    * 针对来源：具体针对某个微服务进行限流，默认值为default，表示不区分来源，全部限流。

    * 阈值类型：QPS表示通过QPS进行限流，并发线程数表示通过并发线程数限流。

    * 单机阈值：与阈值类型组合使用。如果阈值类型选择的是QPS，表示当调用接口的QPS达到阈值时，进行限流操作。如果阈值类型选择的是并发线程数，则表示当调用接口的并发线程数达到阈值时，进行限流操作。

    * 是否集群：选中则表示集群环境，不选中则表示非集群环境。

    * QPS（Queries Per Second）表示每秒查询数，它衡量每秒处理的请求数。
      * QPS 与并发线程数的区别：

        * QPS 衡量每秒处理的请求数，而 并发线程数 衡量同时处理的请求数。
        * QPS 限制的是请求速率，而 并发线程数 限制的是同时处理的请求数。
        * QPS 更适合于限制对服务器资源有较高要求的请求，例如数据库查询和 API 调用。并发线程数 更适合于限制对服务器资源要求较低的请求，例如静态文件服务和缓存读取。

* 流控模式

  *  流量控制主要有两种统计类型，一种是统计线程数，另外一种则是统计 QPS。类型由 `FlowRule.grade` 字段来定义。其中，0 代表根据并发数量来限流，1 代表根据 QPS 来进行流量控制。其中线程数、QPS 值，都是由 `StatisticSlot` 实时统计获取的。 

  * 并发线程数控制

    *  线程数限流用于保护业务线程数不被耗尽。例如，当应用所依赖的下游应用由于某种原因导致服务不稳定、响应延迟增加，对于调用者来说，意味着吞吐量下降和更多的线程数占用，极端情况下甚至导致线程池耗尽。为应对高线程占用的情况，业内有使用隔离的方案，比如通过不同业务逻辑使用不同线程池来隔离业务自身之间的资源争抢（线程池隔离），或者使用信号量来控制同时请求的个数（信号量隔离）。这种隔离方案虽然能够控制线程数量，但无法控制请求排队时间。当请求过多时排队也是无益的，直接拒绝能够迅速降低系统压力。Sentinel线程数限流不负责创建和管理线程池，而是简单统计当前请求上下文的线程个数，如果超出阈值，新的请求会被立即拒绝。 

  * QPS流量控制

    * 当 QPS 超过某个阈值的时候，则采取措施进行流量控制。流量控制的手段包括下面 3 种，对应 `FlowRule` 中的 `controlBehavior` 字段：

      1. 直接拒绝（`RuleConstant.CONTROL_BEHAVIOR_DEFAULT`）方式。该方式是默认的流量控制方式，当QPS超过任意规则的阈值后，新的请求就会被立即拒绝，拒绝方式为抛出`FlowException`。这种方式适用于对系统处理能力确切已知的情况下，比如通过压测确定了系统的准确水位时。

         ![1722825673000](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/1722825673000.png)

      2. 冷启动（`RuleConstant.CONTROL_BEHAVIOR_WARM_UP`）方式。该方式主要用于系统长期处于低水位的情况下，当流量突然增加时，直接把系统拉升到高水位可能瞬间把系统压垮。通过"冷启动"，让通过的流量缓慢增加，在一定时间内逐渐增加到阈值上限，给冷系统一个预热的时间，避免冷系统被压垮的情况。

  * 基于调用关系的流量控制

    *  调用关系包括调用方、被调用方；方法又可能会调用其它方法，形成一个调用链路的层次关系。Sentinel 通过 `NodeSelectorSlot` 建立不同资源间的调用的关系，并且通过 `ClusterNodeBuilderSlot` 记录每个资源的实时统计信息。 

    * 具有关系的资源流量控制：关联流量控制

      *  当两个资源之间具有资源争抢或者依赖关系的时候，这两个资源便具有了关联。比如对数据库同一个字段的读操作和写操作存在争抢，读的速度过高会影响写得速度，写的速度过高会影响读的速度。如果放任读写操作争抢资源，则争抢本身带来的开销会降低整体的吞吐量。可使用关联限流来避免具有关联关系的资源之间过度的争抢，举例来说，`read_db` 和 `write_db` 这两个资源分别代表数据库读写，我们可以给 `read_db` 设置限流规则来达到写优先的目的：设置 `FlowRule.strategy` 为 `RuleConstant.RELATE` 同时设置 `FlowRule.ref_identity` 为 `write_db`。这样当写库操作过于频繁时，读数据的请求会被限流。 （也常用在上下文系统关联）

        ![1722826507119](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/1722826507119.png)

        

    * 根据调用链路入口限流：链路限流

      *  `NodeSelectorSlot` 中记录了资源之间的调用链路，这些资源通过调用关系，相互之间构成一棵调用树。这棵树的根节点是一个名字为 `machine-root` 的虚拟节点，调用链的入口都是这个虚节点的子节点。 

        ![1722827381235](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/1722827381235.png)

* 流控效果
  * 预热
    *  当流量突然增大的时候，我们常常会希望系统从空闲状态到繁忙状态的切换的时间长一些。 即如果系统在此之前长期处于空闲的状态，我们希望处理请求的数量是缓步的增多，经过预期的时间以后，到达系统处理请求个数的最大值。Warm Up (冷启动,预热)模式就是为了实现这个目的。
    * 这个场景主要用于启动需要额外开销的场景，例如建立数据库连接等。
    * 公式:阈值除以冷却因子coldFactor(默认值为3)，经过预热时长后才会达到阈值 
  * 排队等待
    *  匀速器（`RuleConstant.CONTROL_BEHAVIOR_RATE_LIMITER`）方式。这种方式严格控制了请求通过的间隔时间，也即是让请求以均匀的速度通过，对应的是漏桶算法。 



* 熔断规则
  * Sentinel 熔断降级会在调用链路中某个资源出现不稳定状态时（例如调用超时或异常比例升高），对这个资源的调用进行限制，让请求快速失败，避免影响到其它的资源而导致级联错误。当资源被降级后，在接下来的降级时间窗口之内，对该资源的调用都自动熔断（默认行为是抛出 DegradeException）。
  * 三种熔断策略
    * 慢调用比例 (`SLOW_REQUEST_RATIO`)：选择以慢调用比例作为阈值，需要设置允许的慢调用 RT（即最大的响应时间），请求的响应时间大于该值则统计为慢调用。当单位统计时长（`statIntervalMs`）内请求数目大于设置的最小请求数目，并且慢调用的比例大于阈值，则接下来的熔断时长内请求会自动被熔断。经过熔断时长后熔断器会进入探测恢复状态（HALF-OPEN 状态），若接下来的一个请求响应时间小于设置的慢调用 RT 则结束熔断，若大于设置的慢调用 RT 则会再次被熔断。
      *  注意异常降级仅针对业务异常，对Sentinel限流降级本身的异常( BlockException) 不生效。为了统计异常比例或异常数，需要通过Tracer.trace(ex) 记录业务异常。 
    * 异常比例 (`ERROR_RATIO`)：当单位统计时长（`statIntervalMs`）内请求数目大于设置的最小请求数目，并且异常的比例大于阈值，则接下来的熔断时长内请求会自动被熔断。经过熔断时长后熔断器会进入探测恢复状态（HALF-OPEN 状态），若接下来的一个请求成功完成（没有错误）则结束熔断，否则会再次被熔断。异常比率的阈值范围是 `[0.0, 1.0]`，代表 0% - 100%。
    * 异常数 (`ERROR_COUNT`)：当单位统计时长内的异常数目超过阈值之后会自动进行熔断。经过熔断时长后熔断器会进入探测恢复状态（HALF-OPEN 状态），若接下来的一个请求成功完成（没有错误）则结束熔断，否则会再次被熔断。
  
* 常见的注解

  *  @SentinelResource是一个流量防卫防护组件注解,用于指定防护资源，对配置的资源进行流量控制、熔断降级等功能。 

    * 注解源码

      ```java
      @Target({ElementType.METHOD, ElementType.TYPE})
      @Retention(RetentionPolicy.RUNTIME)
      @Inherited
      public @interface SentinelResource {
       
          //资源名称，不重复就行
          String value() default "";
       
          //entry类型，标记流量的方向，取值IN/OUT，默认是OUT
          EntryType entryType() default EntryType.OUT;
          //资源分类
          int resourceType() default 0;
       
          //处理BlockException的函数名称,函数要求：
          //1. 必须是 public
          //2.返回类型 参数与原方法一致
          //3. 默认需和原方法在同一个类中。若希望使用其他类的函数，可配置blockHandlerClass ，并指定blockHandlerClass里面的方法。
          String blockHandler() default "";
       
          //存放blockHandler的类,对应的处理函数必须static修饰。
          Class<?>[] blockHandlerClass() default {};
       
          //用于在抛出异常的时候提供fallback处理逻辑。 fallback函数可以针对所
          //有类型的异常（除了 exceptionsToIgnore 里面排除掉的异常类型）进行处理。函数要求：
          //1. 返回类型与原方法一致
          //2. 参数类型需要和原方法相匹配
          //3. 默认需和原方法在同一个类中。若希望使用其他类的函数，可配置fallbackClass ，并指定fallbackClass里面的方法。
          String fallback() default "";
       
          //存放fallback的类。对应的处理函数必须static修饰。
          String defaultFallback() default "";
       
          //用于通用的 fallback 逻辑。默认fallback函数可以针对所有类型的异常进
          //行处理。若同时配置了 fallback 和 defaultFallback，以fallback为准。函数要求：
          //1. 返回类型与原方法一致
          //2. 方法参数列表为空，或者有一个 Throwable 类型的参数。
          //3. 默认需要和原方法在同一个类中。若希望使用其他类的函数，可配置fallbackClass ，并指定 fallbackClass 里面的方法。
          Class<?>[] fallbackClass() default {};
       
       
          //需要trace的异常
          Class<? extends Throwable>[] exceptionsToTrace() default {Throwable.class};
       
          //指定排除忽略掉哪些异常。排除的异常不会计入异常统计，也不会进入fallback逻辑，而是原样抛出。
          Class<? extends Throwable>[] exceptionsToIgnore() default {};
      }
      ```

    * 按SentinelResource资源名称限流+自定义限流返回

      ```java
      @GetMapping("/rateLimit/byResource")
          @SentinelResource(value = "byResourceSentinelResource",blockHandler = "handleException")
          public String byResource()
          {
              return "按资源名称SentinelResource限流测试OK";
          }
          public String handleException(BlockException exception)
          {
              return "服务不可用@SentinelResource启动"+"\t"+"o(╥﹏╥)o";
          }
      ```

    * 在页面上配置byResourceSentinelResource的限流规则

  * 按SentinelResource资源名称限流+自定义限流返回+服务降级处理

    * 编写代码(在原有方法参数的后面加上阻塞和异常)

      ```java
          @GetMapping("/rateLimit/doAction/{p1}")
          @SentinelResource(value = "doActionSentinelResource",
                  blockHandler = "doActionBlockHandler", fallback = "doActionFallback")
          public String doAction(@PathVariable("p1") Integer p1) {
              if (p1 == 0){
                  throw new RuntimeException("p1等于零直接异常");
              }
              return "doAction";
          }
      
          public String doActionBlockHandler(@PathVariable("p1") Integer p1,BlockException e){
              log.error("sentinel配置自定义限流了:{}", e);
              return "sentinel配置自定义限流了";
          }
      
          public String doActionFallback(@PathVariable("p1") Integer p1,Throwable e){
              log.error("程序逻辑异常了:{}", e);
              return "程序逻辑异常了"+"\t"+e.getMessage();
          }
      ```

    * 和上面一样，在页面注册doActionSentinelResource

    * 违背页面注册的逻辑的会执行block的方法

    * ==blockHandler主要针对sentinel配置后出现的违规情况处理（当 Sentinel 规则被触发时（例如流量或资源限制超出==），Sentinel 会调用 blockHandler 来处理违规请求）

    * ==fallback主要针对程序异常了JVM抛出的异常服务降级，两者可以同时共存（异常处理）==

* 热点参数限流

  * 何为热点？热点即经常访问的数据。很多时候我们希望统计某个热点数据中访问频次最高的 Top K 数据，并对其访问进行限制。比如：

    - 商品 ID 为参数，统计一段时间内最常购买的商品 ID 并进行限制
    - 用户 ID 为参数，针对一段时间内频繁访问的用户 ID 进行限制

  *  热点参数限流会统计传入参数中的热点参数，并根据配置的限流阈值与模式，对包含热点参数的资源调用进行限流。热点参数限流可以看做是一种特殊的流量控制，仅对包含热点参数的资源调用生效。 

  *  Sentinel 利用 LRU 策略统计最近最常访问的热点参数，结合令牌桶算法来进行参数级别的流控。热点参数限流支持集群模式。 

  * 代码实现

    ```java
    @GetMapping("/testHotKey")
    @SentinelResource(value = "testHotKey",blockHandler = "dealHandler_testHotKey")
    public String testHotKey(@RequestParam(value = "p1",required = false) String p1, @RequestParam(value = "p2",required = false) String p2){
        return "------testHotKey";
    }
    public String dealHandler_testHotKey(String p1,String p2,BlockException exception)
    {
        return "-----dealHandler_testHotKey";
    }
    ```

  * 如果想限制第一个参数的流量（ @SentinelResource注解的方法参数索引，0代表第一个参数，1代表第二个参数，以此类推 ）

     ![img](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/115d34b7a9e2d6bfe4dd510d4f4600c5.png) 

  * 只要请求带了第一个参数都会被限流

     ![img](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/65b392c770c095ff35039eddf63ce314.png) 

* 参数例外项

  *  我们期望p1参数当它是某个特殊值时（比如vip）进行特权放行，增加他的阈值

  * 要求参数必须为基本数据类型

  * 比如给值为5的特权

     ![img](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/d45a673cf05f518e9983c02b6759d6e3.png) 

* 授权规则

  * 实现RequestOriginParser接口

    ```java
    public class MyRequestOriginParser implements RequestOriginParser
    {
        @Override
        public String parseOrigin(HttpServletRequest httpServletRequest) {
            return httpServletRequest.getParameter("serverName");
        }
    }
    ```

    * MyRequestOriginParser 是一个 Java 类，它实现了 RequestOriginParser 接口。
    * RequestOriginParser 接口用于从 HTTP 请求中解析请求的来源，或称为来源服务器。
    * parseOrigin 方法：parseOrigin 方法负责从给定的 HTTP 请求中解析请求的来源。
    * 在 MyRequestOriginParser 类中，parseOrigin 方法从 HTTP 请求中提取 serverName 参数，并将其返回作为请求的来源。serverName 参数通常包含发起请求的服务器的名称或主机名。

  * 在页面上配置黑名单

     ![img](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/5e26b8ef570b58ce9ead2d3afb928932.png) 





- 规则持久化

  - 一旦我们重启微服务应用，sentinel规则将消失， 生产环境需要将配置规则进行持久化将限流配置规则持久化进Nacos保存，只要刷新8401某个rest地址，sentinel控制台的流控规则就能看到，只要Nacos里面的配置不删除，针对8401上sentinel上的流控规则持续有效

  - 添加依赖

    ```xml
    <!--SpringCloud ailibaba sentinel-datasource-nacos -->
    <dependency>
        <groupId>com.alibaba.csp</groupId>
        <artifactId>sentinel-datasource-nacos</artifactId>
    </dependency>
    ```

  - 增加配置

    ```yml
    server:
      port: 8401
     
    spring:
      application:
        name: cloudalibaba-sentinel-service #8401微服务提供者后续将会被纳入阿里巴巴sentinel监管
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848         #Nacos服务注册中心地址
        sentinel:
          transport:
            dashboard: localhost:8080 #配置Sentinel dashboard控制台服务地址
            port: 8719 #默认8719端口，假如被占用会自动从8719开始依次+1扫描,直至找到未被占用的端口
            web-context-unify: false # controller层的方法对service层调用不认为是同一个根链路
          datasource:
             ds1:
               nacos:
                 server-addr: localhost:8848
                 dataId: ${spring.application.name}
                 groupId: DEFAULT_GROUP
                 data-type: json
                 rule-type: flow #com.alibaba.cloud.sentinel.datasource.RuleType
    ```

    * ds1：数据源的名称，可以任意定义。
    * nacos：指定数据源类型为 Nacos。
    * server-addr：Nacos 服务器地址。
    * dataId：Nacos 中的 dataId，通常设置为 Spring Boot 应用的名称。
    * groupId：Nacos 中的 groupId，通常设置为 DEFAULT_GROUP。
    * data-type：Nacos 中数据的类型，这里设置为 json。
    * rule-type：Sentinel 规则类型，这里设置为 flow，表示该数据源包含流控规则。
      *  com.alibaba.cloud.sentinel.datasource.RuleType 是一个枚举类，定义了 Sentinel 支持的规则类型。在您的配置中，rule-type 被设置为 flow，表示该数据源包含流控规则。 
        * flow：流控规则
        * degrade：降级规则
        * system：系统规则
        * authority：授权规则
        * param-flow：参数流控规则

- OpenFeign和Sentinel集成实现fallback服务降级

  - 之前的问题
    - 通过OpenFeign调用 9001微服务，正常访问OK
    - 通过OpenFeign调用 9001微服务，异常访问error
    - 访问者要有fallback服务降级的情况，不要持续访问9001加大微服务负担，但是通过feign接口调用的又方法各自不同，如果每个不同方法都加一个fallback配对方法，会导致代码膨胀不好管理，工程埋雷
    
  - 把fallback交给openfeign处理
  
     ![img](%E9%98%BF%E9%87%8C%E5%B7%B4%E5%B7%B4%E4%B9%8BSentinal.assets/b09aa19a2d090f76ef7bc891e9d78b36.png) 
  
  - 给服务提供者导入依赖
  
    ```xml
    <!--openfeign-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>
    <!--alibaba-sentinel-->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    <!-- 引入自己定义的api通用包 -->
    <dependency>
        <groupId>com.atguigu.cloud</groupId>
        <artifactId>cloud-api-commons</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>
    ```
  
  - 移除handler
  
    ```java
    @RestController
    public class PayAlibabaController
    {
        @Value("${server.port}")
        private String serverPort;
     
        @GetMapping(value = "/pay/nacos/{id}")
        public String getPayInfo(@PathVariable("id") Integer id)
        {
            return "nacos registry, serverPort: "+ serverPort+"\t id"+id;
        }
     
        @GetMapping("/pay/nacos/get/{orderNo}")
        //这里移除了fallback
        @SentinelResource(value = "getPayByOrderNo",blockHandler = "handlerBlockHandler")
        public ResultData getPayByOrderNo(@PathVariable("orderNo") String orderNo)
        {
            //模拟从数据库查询出数据并赋值给DTO
            PayDTO payDTO = new PayDTO();
     
            payDTO.setId(1024);
            payDTO.setOrderNo(orderNo);
            payDTO.setAmount(BigDecimal.valueOf(9.9));
            payDTO.setPayNo("pay:"+IdUtil.fastUUID());
            payDTO.setUserId(1);
     
            return ResultData.success("查询返回值："+payDTO);
        }
        public ResultData handlerBlockHandler(@PathVariable("orderNo") String orderNo,BlockException exception)
        {
            return ResultData.fail(ReturnCodeEnum.RC500.getCode(),"getPayByOrderNo服务不可用，" +
                    "触发sentinel流控配置规则"+"\t"+"o(╥﹏╥)o");
        }
    }
    ```
  
  - 公共模块
  
    ```xml
    <!--openfeign-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>
    <!--alibaba-sentinel-->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    ```
  
  - 公共模块定义openfeign
  
    ```java
    @FeignClient(value = "nacos-payment-provider",fallback = PayFeignSentinelApiFallBack.class)
    public interface PayFeignSentinelApi
    {
        @GetMapping("/pay/nacos/get/{orderNo}")
        public ResultData getPayByOrderNo(@PathVariable("orderNo") String orderNo);
    }
    ```
  
  - 公共模块实现接口
  
    ```java
    package com.atguigu.cloud.apis;
     
    import com.atguigu.cloud.resp.ResultData;
    import com.atguigu.cloud.resp.ReturnCodeEnum;
    import org.springframework.stereotype.Component;
     
    /
     * @auther zzyy
     * @create 2023-11-30 20:22
     */
    @Component
    public class PayFeignSentinelApiFallBack implements PayFeignSentinelApi
    {
        @Override
        public ResultData getPayByOrderNo(String orderNo)
        {
            return ResultData.fail(ReturnCodeEnum.RC500.getCode(),"对方服务宕机或不可用，FallBack服务降级o(╥﹏╥)o");
        }
    }
    ```
  
  - 消费者的pom
  
    ```xml
    <!-- 引入自己定义的api通用包 -->
    <dependency>
        <groupId>com.atguigu.cloud</groupId>
        <artifactId>cloud-api-commons</artifactId>
        <version>1.0-SNAPSHOT</version>
    </dependency>
    <!--openfeign-->
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-openfeign</artifactId>
    </dependency>
    <!--alibaba-sentinel-->
    <dependency>
        <groupId>com.alibaba.cloud</groupId>
        <artifactId>spring-cloud-starter-alibaba-sentinel</artifactId>
    </dependency>
    ```
  
  - 消费者的yml
  
    ```yml
    server:
      port: 83
     
    spring:
      application:
        name: nacos-order-consumer
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848
    #消费者将要去访问的微服务名称(nacos微服务提供者叫什么你写什么)
    service-url:
      nacos-user-service: http://nacos-payment-provider
     
    # 激活Sentinel对Feign的支持
    feign:
      sentinel:
        enabled: true
    ```
  
  - 消费者的主启动类加上注解
  
    ```java
    @EnableDiscoveryClient
    @SpringBootApplication
    @EnableFeignClients
    public class Main83
    {
        public static void main(String[] args)
        {
            SpringApplication.run(Main83.class,args);
        }
    }
    ```
  
  - 消费者的controller
  
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
     
        @GetMapping(value = "/consumer/pay/nacos/get/{orderNo}")
        public ResultData getPayByOrderNo(@PathVariable("orderNo") String orderNo)
        {
            return payFeignSentinelApi.getPayByOrderNo(orderNo);
        }
    }
    ```
  
    







* GateWay和Sentinel集成实现服务限流

  * 导入依赖

    ```java
    <dependency>
        <groupId>org.springframework.cloud</groupId>
        <artifactId>spring-cloud-starter-gateway</artifactId>
    </dependency>
    <dependency>
        <groupId>com.alibaba.csp</groupId>
        <artifactId>sentinel-transport-simple-http</artifactId>
        <version>1.8.6</version>
    </dependency>
    <dependency>
        <groupId>com.alibaba.csp</groupId>
        <artifactId>sentinel-spring-cloud-gateway-adapter</artifactId>
        <version>1.8.6</version>
    </dependency>
    <dependency>
        <groupId>javax.annotation</groupId>
        <artifactId>javax.annotation-api</artifactId>
        <version>1.3.2</version>
        <scope>compile</scope>
    </dependency>
    ```

  * 配置yml

    ```yml
    server:
      port: 9528
     
    spring:
      application:
        name: cloudalibaba-sentinel-gateway     # sentinel+gataway整合Case
      cloud:
        nacos:
          discovery:
            server-addr: localhost:8848
        gateway:
          routes:
            - id: pay_routh1 #pay_routh1                #路由的ID(类似mysql主键ID)，没有固定规则但要求唯一，建议配合服务名
              uri: http://localhost:9001                #匹配后提供服务的路由地址
              predicates:
              - Path=/pay/                      # 断言，路径相匹配的进行路由
    ```

    