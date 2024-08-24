#### LoadBalance

* Spring Cloud Ribbon是基于Netflix Ribbon实现的一套客户端―负载均衡的工具。

* 简单的说，Ribbon是Netflix发布的开源项目，主要功能是提供客户端的软件负载均衡算法和服务调用。Ribon客户端组件提供一系列完善的配置项如连接超时，重试等。简单的说，就是在配置文件中列出Load Balancer〈简称LB）后面所有的机器，Ribbon会自动的帮助你基于某种规则（如简单轮询，随机连接等）去连接这些机器。我们很容易使用Ribon实现自定义的负毂均衡算法。

* ribbon也进入维护了

* 作为替换者：==SpringCloud LoadBalancer（默认策略是轮询）==

  * LoadBalancer和Nginx区别

    * Nginx是服务器负载均衡，客户端所有请求都会交给nginx，然后由nginx实现转发请求，即负载均衡是由服务端实现的。
    * Loadbalancer本地负载均衡，在调用微服务接口时候，会在注册中心上：获取注册信息雕务列表之后级存到JVM本地，从而在本地实现RPC远程服务调用技术。

  * 默认是轮询和随机

    ```java
    public class RandomLoadBalancer implements ReactorServiceInstanceLoadBalancer
    ```

  * 自定义算法只要实现它ReactorServiceInstanceLoadBalancer

    ```java
    public interface ReactorServiceInstanceLoadBalancer extends ReactorLoadBalancer<ServiceInstance> {
    }
    ```

  * 阿里巴巴也是继承它实现的**public class** NacosLoadBalancer **implements** ReactorServiceInstanceLoadBalancer 

  * 随机的使用

    ```java
    @Configuration
    @LoadBalancerClient(
            //下面的value值大小写一定要和consul里面的名字一样，必须一样
            value = "cloud-payment-service",configuration = RestTemplateConfig.class)
    public class RestTemplateConfig
    {
        @Bean
        @LoadBalanced
        public RestTemplate restTemplate()
        {
            return new RestTemplate();
        }
        @Bean
        ReactorLoadBalancer<ServiceInstance> randomLoadBalancer(Environment environment,
                                                                LoadBalancerClientFactory loadBalancerClientFactory) {
            String name = environment.getProperty(LoadBalancerClientFactory.PROPERTY_NAME);
    
            return new RandomLoadBalancer(loadBalancerClientFactory.getLazyProvider(name, ServiceInstanceListSupplier.class), name);
        }
    }
    ```

    