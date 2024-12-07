###### 源码分析

* 先进入到自动配置类LoadBalancerAutoConfiguration，满足两个条件才会生效，一是有RestTemplate（在spring-boot-starter-web中存在这个类），二是有LoadBalancerClient的bean（BlockingLoadBalancerClientAutoConfiguration）。

  ```java
  @Configuration(proxyBeanMethods = false)
  @ConditionalOnClass(RestTemplate.class)
  @ConditionalOnBean(LoadBalancerClient.class)
  @EnableConfigurationProperties(LoadBalancerRetryProperties.class)
  public class LoadBalancerAutoConfiguration {
      	@LoadBalanced
  	@Autowired(required = false)
  	private List<RestTemplate> restTemplates = Collections.emptyList();
  
  	@Autowired(required = false)
  	private List<LoadBalancerRequestTransformer> transformers = Collections.emptyList();
  
  	@Bean
  	public SmartInitializingSingleton loadBalancedRestTemplateInitializerDeprecated(
  			final ObjectProvider<List<RestTemplateCustomizer>> restTemplateCustomizers) {
  		return () -> restTemplateCustomizers.ifAvailable(customizers -> {
  			for (RestTemplate restTemplate : LoadBalancerAutoConfiguration.this.restTemplates) {
  				for (RestTemplateCustomizer customizer : customizers) {
  					customizer.customize(restTemplate);
  				}
  			}
  		});
  	}
      //
  	@Bean
  	@ConditionalOnMissingBean
  	public LoadBalancerRequestFactory loadBalancerRequestFactory(
  			LoadBalancerClient loadBalancerClient) {
  		return new LoadBalancerRequestFactory(loadBalancerClient, this.transformers);
  	}
  
  	@Configuration(proxyBeanMethods = false)
  	@ConditionalOnMissingClass("org.springframework.retry.support.RetryTemplate")
  	static class LoadBalancerInterceptorConfig {
  
  		@Bean
  		public LoadBalancerInterceptor loadBalancerInterceptor(
  				LoadBalancerClient loadBalancerClient,
  				LoadBalancerRequestFactory requestFactory) {
  			return new LoadBalancerInterceptor(loadBalancerClient, requestFactory);
  		}
          //restTemplate的定制，注入了一个loadBalancerInterceptor
  		public RestTemplateCustomizer restTemplateCustomizer(
  				final LoadBalancerInterceptor loadBalancerInterceptor) {
  			return restTemplate -> {
  				List<ClientHttpRequestInterceptor> list = new ArrayList<>(
  						restTemplate.getInterceptors());
  				list.add(loadBalancerInterceptor);
  				restTemplate.setInterceptors(list);
  			};
  		}
  	
  }
  ```

* restTemplate的定制，注入了一个loadBalancerInterceptor拦截器，在executor方法中，会执行拦截器的intercept()方法，如果没有拦截器，就会构造clienthttprequest对象并发起请求。如果有，就会进入到拦截器。通过choose方法选择一个实例。

* 它默认就两个轮询策略，随机和轮询。如过自定义，就实现ReactorServiceInstanceLoadBalancer接口



* 总结：
  * 1.服务注册：调用方和被调用方都需要服务注册
  * 2.服务发现：获取可用的实例清单并存储在serviceInfoMap变量中。
  * 3.读取serviceInfoMap的可用实例列表，根据负载均衡选择具体的调用实例
  * 4.根据调用实例的信息拼接HTTP地址并向某一个具体的实例发起HTTP请求。