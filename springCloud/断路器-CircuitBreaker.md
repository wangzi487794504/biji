#### 断路器-CircuitBreaker

* Hystrix是一个用于处理分布式系统的延迟和容错的开源库，在分布式系统里，许多依赖不可避免的会调用失败，比如超时、异常等，Hystrix能够保证在一个依赖出问题的情况下，不会导致热体服务失败，避免级联故障，以提高分布式系统的弹性。

  * 已经进入维护模式

* 服务雪崩

  * 多个微服务之间调用的时候，假设微服务A调用微服务B和微服务C，微服务B和微服务C又调用其它的微服务，这就是所谓的“扇出”。如果扇出的链路上某个微服务的调用响应时间过长或者不可用，对微服务A的调用就会占用越来越多的系统资源，进而引起系统崩溃，所谓的“雪崩效应”.
    对于高流量的应用来说，单一的后端依赖可能会导致所有服务器上的所有资源都在几秒钟内饱和。比失败更糟糕的是，这些应用程序还可能导致服务之间的延迟增加，备份队列，线程和其他系统资源紧张，导致整个系统发生更多的级联故障。这些都表示需要对故障和延迟进行隔离和管理，以便单个依赖关系的失败，不能取消整个应用程序或系统。
    所以，通常当你发现一个模软下的某个实例失败后，这时候这个模块依然还会接收流量，然后这个有问题的模块还调用了其他的模块，这样就会发生级联故障，或者叫雪崩。
  * 解决方法：-有问题的节点，快速熔断（快速返回失败处理或者返回默认兜底数据【服务降级】）。“断路器"本身是一种开关装置，当某个服务单元发生故障之后，通过断路器的故障监控（类似熔断保险丝），向调用方返回一个符合预期的、可处理的备选响应(FallBack)，而不是长时间的等待或者抛出调用方无法处理的异常，这样就保证了服务调用方的线程不会被长时间、不必要地占用，从而避免了故障在分布式系统中的蔓延，乃至雪崩。

* 服务熔断(==服务降级是对功能的控制和限制，而服务熔断则是对请求的拦截和监控.== )

  * 类比保险丝，保险丝闭合状态(CLOSE)可以正常使用，当达到最大服务访问后，直接拒绝访问跳闸限电(OPEN)，此刻调用方会接受服务降级的处理并返回友好兜底提示

  * 一般是某个服务故障或者异常引起，类似现实世界中的 “保险丝” ， 当某个异常条件被触发， 

    直接熔断整个服务，而不是一直等到此服务超时！

* 服务降级( 服务降级策略可有效防止服务雪崩的发生 )

  * 整体资源快不够了，忍痛将某些服务先关掉，待渡过难关，再开启回来。服务器忙，请稍后再试。不让客户端等待并立刻返回一个友好提示，fallback

  * **服务降级处理是在客户端实现完成的，与服务端没有关系**

  * 所谓降级，一般是从整体负荷考虑，就是当某个服务熔断之后，服务器将不再被调用，此时 

    客户端可以自己准备一个本地的fallback回调，返回一个缺省值。这样做，虽然服务水平下降，但好歹可 用，比直接挂掉要强

* 服务限流
  
  * 秒杀高并发等操作，严禁一窝蜂的过来拥挤，大家排队，一秒钟N个，有序进行
* 服务监控
  * 除了隔离依赖服务的调用以外，Hystrix还提供了准实时的调用监控（Hystrix Dashboard），Hystrix会 持续地记录所有通过Hystrix发起的请求的执行信息，并以统计报表和图形的形式展示给用户，包括每秒 执行多少请求，多少成功，多少失败等等。 
  * Netflix通过hystrix-metrics-event-stream项目实现了对以上指标的监控，SpringCloud也提供了Hystrix Dashboard的整合，对监控内容转化成可视化界面！ 
* 服务限时
  *   服务限时是为了控制服务请求的响应时间，避免请求因为等待超时而阻塞影响整个系统的服务。 
  *  举例：在调用外部依赖的服务时，设置每个操作的超时时间，当服务响应的时间过长时，系统不会无限等待，而是及时放弃该请求。 
* 服务预热
  * 服务预热是在请求到来之前，提前初始化和准备资源以加速服务的响应。
  * \- 举例：某个机房突然发生故障，系统会自动将请求转发到其他机房，而在这之前，系统并不会直接将请求转发到这个机房，而是先预热。



* #### CircuitBreaker

  * circuit Breaker只是一套规范和接口，落地实现者是Resilience4J
  * CircuitBreaker的目的是保护分布式系统免受故障和异常，提高系统的可用性和健壮性。
  * Resilience4j是一个专为函数式编程设计的轻量级容错库。Resilience4j提供高阶函数（装饰器)，以通过断路器、速率限制器、重试或隔板增强任何功能接口、lambda 表达式或方法引用。您可以在任何函数式接口、lambda 表达式或方法引用上堆叠多个装饰器。优点是您可以选择您需要的装饰器，而没有其他选择。

* CircuitBreaker断路器

  * 断路器有三个普通状态:关闭(CLOSED)、开启(OPEN)、半开(HALF_OPEN)，还有两个特殊状态:禁用(DISABLED)、强制开启(FORCED_OPEN)。

  * 当熔断器关闭时，所有的请求都会通过熔断器。

    * ==如果失败率超过设定的阈值，熔断器就会从关闭状态转换到打开状态，这时所有的请求都会被拒绝。==
    * ==当经过一段时间后，熔断器会从打开状态转换到半开状态，这时仅有一定数量的请求会被放入，并重新计算失败率==。
    * 如果失败率超过阈值，则变为打开状态，如果失败率低于阈值，则变为关闭状态。

  * 断路器使用滑动窗口来存储和统计调用的结果。你可以选择基于``调用数量的滑动窗口``或者基于``时间的滑动窗口。``

  * **基于访问数量的滑动窗口统计了最近N次调用的返回结果。居于时间的滑动窗口统计了最近N秒的调用返回结果。**

  * 除此以外，熔断器还会有两种特殊状态:DISABLED(始终允许访问）和FORCED_OPEN(始终拒绝访问)。这两个状态不会生成熔断器事件（除状态装换外)，并且不会记录事件的成功或者失败。
    。退出这两个状态的唯一方法是触发状态转换或者重置熔断器。

  * 断路器配置解析

    * failure-rate-threshold 以百分比配置失败率峰值
    * ==sliding-window-type 断路器的滑动窗口期类型。可以基于“次数”（COUNT_BASED）或者“时间”（TIME_BASED）进行熔断，默认是COUNT_BASED。==
    * sliding-window-size 若COUNT_BASED，则10次调用中有50%失败（即5次）打开熔断断路器；若为TIME_BASED则，此时还有额外的两个设置属性，含义为：在N秒内（sliding-window-size）100%（slow-call-rate-threshold）的请求超过N秒（slow-call-duration-threshold）打开断路器。

    * slowCallRateThreshold 以百分比的方式配置，断路器把调用时间大于slowCallDurationThreshold的调用视为慢调用，当慢调用比例大于等于峰值时，断路器开启，并进入服务降级。
    * slowCallDurationThreshold  配置调用时间的峰值，高于该峰值的视为慢调用。

    * permitted-number-of-calls-in-half-open-state   运行断路器在HALF_OPEN状态下时进行N次调用，如果故障或慢速调用仍然高于阈值，断路器再次进入打开状态。

    * minimum-number-of-calls  在每个滑动窗口期样本数，配置断路器计算错误率或者慢调用率的最小调用数。比如设置为5意味着，在计算故障率之前，必须至少调用5次。如果只记录了4次，即使4次都失败了，断路器也不会进入到打开状态。

    * wait-duration-in-open-state  从OPEN到HALF_OPEN状态需要等待的时间。按照COUNT_BASED(计数的滑动窗口)

  * 配置文件配置

    ```yml
    resilience4j:
      timelimiter:
        configs:
          default:
            timeout-duration: 10s #神坑的位置，timelimiter 默认限制远程1s，超于1s就超时异常，配置了降级，就走降级逻辑
      circuitbreaker:
        configs:
          default:
            failureRateThreshold: 50 #设置50%的调用失败时打开断路器，超过失败请求百分⽐CircuitBreaker变为OPEN状态。
            slowCallDurationThreshold: 2s #慢调用时间阈值，高于这个阈值的视为慢调用并增加慢调用比例。
            slowCallRateThreshold: 30 #慢调用百分比峰值，断路器把调用时间⼤于slowCallDurationThreshold，视为慢调用，当慢调用比例高于阈值，断路器打开，并开启服务降级
            slidingWindowType: COUNT_BASED  # 滑动窗口的类型
            slidingWindowSize: 2 #滑动窗口的大小配置，配置TIME_BASED表示2秒
            minimumNumberOfCalls: 2 #断路器计算失败率或慢调用率之前所需的最小样本(每个滑动窗口周期)。
            permittedNumberOfCallsInHalfOpenState: 2 #半开状态允许的最大请求数，默认值为10。
            waitDurationInOpenState: 5s #从OPEN到HALF_OPEN状态需要等待的时间
            recordExceptions:
              - java.lang.Exception
        instances:
          cloud-payment-service:#这个服务使用default配置
            baseConfig: default
    ```

  * 在调用请求的地方使用注解(==name一定要和配置文件的对应==)

    ```java
        @GetMapping(value = "/feign/pay/circuit/{id}")
        @CircuitBreaker(name = "cloud-payment-service", fallbackMethod = "myCircuitFallback")
        public String myCircuitBreaker(@PathVariable("id") Integer id)
        {
            return payFeignApi.myCircuit(id);
        }
        //myCircuitFallback就是服务降级后的兜底处理方法，上面请求挂了就用它兜底
        public String myCircuitFallback(Integer id,Throwable t) {
            // 这里是容错处理逻辑，返回备用结果
            return "myCircuitFallback，系统繁忙，请稍后再试-----/(ㄒoㄒ)/~~";
        }
    ```



* 基于时间的滑动窗口

  * 基于时间的滑动窗口是通过有N个桶的环形数组实现。

  * 如果滑动窗口的大小为10秒，这个环形数组总是有10个桶，每个桶统计了在这一秒发生的所有调用的结果(部分统计结果)，数组中的第一个桶存储了当前这一秒内的所有调用的结果，其他的桶存储了之前每秒调用的结果。

  * 滑动窗口不会单独存储所有的调用结果，而是对每个桶内的统计结果和总的统计值进行增量的更新，当新的调用结果被记录时，总的统计值会进行增量更新。

  * 检索快照（总的统计值)的时间复杂度为O(1)，因为快照已经预先统计好了，并且和滑动窗口大小无关。

  * 关于此方法实现的空间需求(内存消耗)约等于O(n)。由于每次调用结果(元组)不会被单独存储，只是对N个桶进行单独统计和一次总分的统计。

  * 每个桶在进行部分统计时存在三个整型，为了计算，失败调用数，慢调用数，总调用数。还有一个long类型变量，存储所有调用的响应时间。

  * 配置文件

    ```yml
    # Resilience4j CircuitBreaker 按照时间：TIME_BASED 的例子
    resilience4j:
      timelimiter:
        configs:
          default:
            timeout-duration: 10s #神坑的位置，timelimiter 默认限制远程1s，超于1s就超时异常，配置了降级，就走降级逻辑
      circuitbreaker:
        configs:
          default:
            failureRateThreshold: 50 #设置50%的调用失败时打开断路器，超过失败请求百分⽐CircuitBreaker变为OPEN状态。
            slowCallDurationThreshold: 2s #慢调用时间阈值，高于这个阈值的视为慢调用并增加慢调用比例。
            slowCallRateThreshold: 30 #慢调用百分比峰值，断路器把调用时间⼤于slowCallDurationThreshold，视为慢调用，当慢调用比例高于阈值，断路器打开，并开启服务降级
            slidingWindowType: TIME_BASED # 滑动窗口的类型
            slidingWindowSize: 2 #滑动窗口的大小配置，配置TIME_BASED表示2秒
            minimumNumberOfCalls: 2 #断路器计算失败率或慢调用率之前所需的最小样本(每个滑动窗口周期)。
            permittedNumberOfCallsInHalfOpenState: 2 #半开状态允许的最大请求数，默认值为10。
            waitDurationInOpenState: 5s #从OPEN到HALF_OPEN状态需要等待的时间
            recordExceptions:
              - java.lang.Exception
        instances:
          cloud-payment-service:
            baseConfig: default
    ```





* 仓库隔离

  * 简单说就是限并发、依赖隔离、负载保护:用来限制对于下游服务的最大并发数量的限制。

  * 避免故障扩散：当一个服务失败或变慢时，隔离可防止该服务的问题通过整个系统传播，从而提高系统的稳定性和可用性。

  * 资源限制：通过对并发请求的限制，隔离可以确保每个服务或功能所需的资源不会被其他服务的问题所耗尽。

  * 提高系统容错性：通过实现隔离，可以避免在高负载或故障情况下影响整个系统的稳定性，从而提高系统的容错能力。

  * 性能管理：通过隔离不同资源的使用，可以更好地管理系统的性能和资源分配，确保重要功能和关键服务的优先级得到

  * 导入pom依赖

    ```xml
    <!--resilience4j-bulkhead-->
    <dependency>
        <groupId>io.github.resilience4j</groupId>
        <artifactId>resilience4j-bulkhead</artifactId>
    </dependency>
    ```

  * 配置文件：设置并行量

    ```yml
    
    resilience4j:
      bulkhead:
        configs:
          default:
            maxConcurrentCalls: 2 # 隔离允许并发线程执行的最大数量
            maxWaitDuration: 1s # 当达到并发调用数量时，新的线程的阻塞时间，我只愿意等待1秒，过时不候进舱壁兜底fallback
        instances:
          cloud-payment-service:
            baseConfig: default
      timelimiter:
        configs:
          default:
            timeout-duration: 20s
    ```

    







* 限流(RateLimiter)

  * 限流 就是限制最大访问流量。系统能提供的最大并发是有限的，同时来的请求又太多，就需要限流。 比如商城秒杀业务，瞬时大量请求涌入，服务器忙不过就只好排队限流了，和去景点排队买票和去医院办理业务排队等号道理相同。

  * 所谓限流，就是通过对并发访问/请求进行限速，或者对一个时间窗口内的请求进行限速，以保护应用系统，一旦达到限制速率则可以拒绝服务、排队或等待、降级等处理。

  * 常见的限流算法

    *  漏斗算法(Leaky Bucket) 

      * 一个固定容量的漏桶，按照设定常量固定速率流出水滴，类似医院打吊针，不管你源头流量多大，我设定匀速流出。如果流入水滴超出了桶的容量，则流入的水滴将会溢出了(被丢弃)，而漏桶容量是不变的。
      * 这里有两个变量，一个是桶的大小，支持流量突发增多时可以存多少的水(burst)，另一个是水桶漏洞的大小(rate)。因为漏桶的漏出速率是固定的参数，所以，即使网络中不存在资源冲突(没有发生拥塞)，漏桶算法也不能使流突发(burst）到端口速率。因此，漏桶算法对于存在突发特性的流量来说缺乏效率。

    *  令牌桶算法(Token Bucket) ==默认使用==

      ![1722661359229](%E6%96%AD%E8%B7%AF%E5%99%A8-CircuitBreaker.assets/1722661359229.png)

    *  滚动时间窗(tumbling time window) 

      * 允许固定数量的请求进入(比如1秒取4个数据相加，超过25值就over)超过数量就拒绝或者排队，等下一个时间段进入。
      * 由于是在一个时间间隔内进行限制，如果用户在上个时间间隔结束前请求（但没有超过限制)，同时在当前时间间隔刚开始请求（(同样没超过限制)，在各自的时间间隔内，这些请求都是正常的。下图统计了3次，but由于计数器算法存在时间临界点缺陷，因此在时间临界点左右的极短时间段内容易遭到攻击。
      * 假如设定1分钟最多可以请求100次某个接口，如120000-12:00:59时间段内没有数据请求但12:00:59-12.01:00时间段内突然并发10o次请求，紧接着瞬间跨入下一个计数周期计数器清零;在12:10100-12:01:01内又有100次请求。那么也就是说在时间临界点左右可能同时有2倍的峰值进行请求，从而造成后台处理请求加倍过载的bug，导致系统运营能力不足，甚至导致系统崩溃。（只能控制数量，不能控制速率）

    *  滑动时间窗口(sliding time window) 

      * 顾名思义，该时间窗口是滑动的。所以，从概念上讲，这里有两个方面的概
      * 窗口:需要定义窗口的大小
      * 滑动:需要定义在窗口中滑动的大小，但理论上讲滑动的大小不能超过窗口大小
      * 滑动窗口算法是把固定时间片进行划分并且随着时间移动，移动方式为开始时间点变为时间列表中的第2个时间点，结束时间点增加一个时间点，不断重复，通过这种方式可以巧妙的避开计数器的临界点的问题。