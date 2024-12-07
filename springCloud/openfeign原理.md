#### openfeign原理

* 点击注解

  ```java
  @Retention(RetentionPolicy.RUNTIME)
  @Target(ElementType.TYPE)
  @Documented
  @Import(FeignClientsRegistrar.class)
  public @interface EnableFeignClients {
  ```

  

* 他导入了一个FeignClientsRegistrar

  ```java
  class FeignClientsRegistrar
  		implements ImportBeanDefinitionRegistrar, ResourceLoaderAware, EnvironmentAware {
      	@Override
  	public void registerBeanDefinitions(AnnotationMetadata metadata,
  			BeanDefinitionRegistry registry) {
  		registerDefaultConfiguration(metadata, registry);
          //这里注册了openfeign
  		registerFeignClients(metadata, registry);
  	}
  }
  ```

* 点击这个方法

  ```java
  public void registerFeignClients(AnnotationMetadata metadata,
  			BeanDefinitionRegistry registry) {
  
  		LinkedHashSet<BeanDefinition> candidateComponents = new LinkedHashSet<>();
  		Map<String, Object> attrs = metadata
  				.getAnnotationAttributes(EnableFeignClients.class.getName());
  		AnnotationTypeFilter annotationTypeFilter = new AnnotationTypeFilter(
  				FeignClient.class);
  		final Class<?>[] clients = attrs == null ? null
  				: (Class<?>[]) attrs.get("clients");
  		if (clients == null || clients.length == 0) {
  			ClassPathScanningCandidateComponentProvider scanner = getScanner();
  			scanner.setResourceLoader(this.resourceLoader);
  			scanner.addIncludeFilter(new AnnotationTypeFilter(FeignClient.class));
  			Set<String> basePackages = getBasePackages(metadata);
  			for (String basePackage : basePackages) {
  				candidateComponents.addAll(scanner.findCandidateComponents(basePackage));
  			}
  		}
  		else {
  			for (Class<?> clazz : clients) {
  				candidateComponents.add(new AnnotatedGenericBeanDefinition(clazz));
  			}
  		}
  
  		for (BeanDefinition candidateComponent : candidateComponents) {
  			if (candidateComponent instanceof AnnotatedBeanDefinition) {
  				// verify annotated class is an interface
  				AnnotatedBeanDefinition beanDefinition = (AnnotatedBeanDefinition) candidateComponent;
  				AnnotationMetadata annotationMetadata = beanDefinition.getMetadata();
  				Assert.isTrue(annotationMetadata.isInterface(),
  						"@FeignClient can only be specified on an interface");
  
  				Map<String, Object> attributes = annotationMetadata
  						.getAnnotationAttributes(FeignClient.class.getCanonicalName());
  
  				String name = getClientName(attributes);
  				registerClientConfiguration(registry, name,
  						attributes.get("configuration"));
                  //注册在这里
  				registerFeignClient(registry, annotationMetadata, attributes);
  			}
  		}
  	}
  ```

* 点击这个方法

  ```java
  private void registerFeignClient(BeanDefinitionRegistry registry,
  			AnnotationMetadata annotationMetadata, Map<String, Object> attributes) {
  		String className = annotationMetadata.getClassName();
      //他在这里实现了FeignClientFactoryBean
  		BeanDefinitionBuilder definition = BeanDefinitionBuilder
  				.genericBeanDefinition(FeignClientFactoryBean.class);
  		validate(attributes);
  		definition.addPropertyValue("url", getUrl(attributes));
  		definition.addPropertyValue("path", getPath(attributes));
  		String name = getName(attributes);
  		definition.addPropertyValue("name", name);
  		String contextId = getContextId(attributes);
  		definition.addPropertyValue("contextId", contextId);
  		definition.addPropertyValue("type", className);
  		definition.addPropertyValue("decode404", attributes.get("decode404"));
  		definition.addPropertyValue("fallback", attributes.get("fallback"));
  		definition.addPropertyValue("fallbackFactory", attributes.get("fallbackFactory"));
  		definition.setAutowireMode(AbstractBeanDefinition.AUTOWIRE_BY_TYPE);
  
  		String alias = contextId + "FeignClient";
  		AbstractBeanDefinition beanDefinition = definition.getBeanDefinition();
  		beanDefinition.setAttribute(FactoryBean.OBJECT_TYPE_ATTRIBUTE, className);
  
  		// has a default, won't be null
  		boolean primary = (Boolean) attributes.get("primary");
  
  		beanDefinition.setPrimary(primary);
  
  		String qualifier = getQualifier(attributes);
  		if (StringUtils.hasText(qualifier)) {
  			alias = qualifier;
  		}
  
  		BeanDefinitionHolder holder = new BeanDefinitionHolder(beanDefinition, className,
  				new String[] { alias });
  		BeanDefinitionReaderUtils.registerBeanDefinition(holder, registry);
  	}
  ```

* 点击FeignClientFactoryBean

  ```java
  class FeignClientFactoryBean
  		implements FactoryBean<Object>, InitializingBean, ApplicationContextAware {
  
  	/***********************************
  	 * WARNING! Nothing in this class should be @Autowired. It causes NPEs because of some
  	 * lifecycle race condition.
  	 ***********************************/
  
  	private Class<?> type;
  
  	private String name;
  
  	private String url;
  
  	private String contextId;
  
  	private String path;
  
  	private boolean decode404;
  
  	private boolean inheritParentContext = true;
  
  	private ApplicationContext applicationContext;
  
  	private Class<?> fallback = void.class;
  
  	private Class<?> fallbackFactory = void.class;
  
  	private int readTimeoutMillis = new Request.Options().readTimeoutMillis();
  
  	private int connectTimeoutMillis = new Request.Options().connectTimeoutMillis();
      
  	@Override
  	public Object getObject() throws Exception {
  		return getTarget();
  	}
      <T> T getTarget() {
  		FeignContext context = applicationContext.getBean(FeignContext.class);
  		Feign.Builder builder = feign(context);
  
  		if (!StringUtils.hasText(url)) {
  			if (!name.startsWith("http")) {
  				url = "http://" + name;
  			}
  			else {
  				url = name;
  			}
  			url += cleanPath();
  			return (T) loadBalance(builder, context,
  					new HardCodedTarget<>(type, name, url));
  		}
  		if (StringUtils.hasText(url) && !url.startsWith("http")) {
  			url = "http://" + url;
  		}
  		String url = this.url + cleanPath();
  		Client client = getOptional(context, Client.class);
  		if (client != null) {
  			if (client instanceof LoadBalancerFeignClient) {
  				// not load balancing because we have a url,
  				// but ribbon is on the classpath, so unwrap
  				client = ((LoadBalancerFeignClient) client).getDelegate();
  			}
  			if (client instanceof FeignBlockingLoadBalancerClient) {
  				// not load balancing because we have a url,
  				// but Spring Cloud LoadBalancer is on the classpath, so unwrap
  				client = ((FeignBlockingLoadBalancerClient) client).getDelegate();
  			}
  			builder.client(client);
  		}
  		Targeter targeter = get(context, Targeter.class);
          //是调用这个方法的target
  		return (T) targeter.target(this, builder, context,
  				new HardCodedTarget<>(type, name, url));
  	}
  
  ```

* 这个一个接口

  ```java
  interface Targeter {
  
  	<T> T target(FeignClientFactoryBean factory, Feign.Builder feign,
  			FeignContext context, Target.HardCodedTarget<T> target);
  
  }
  ```

* 我们去找他的实现类，默认使用default

  ​	![image-20241109133920305](openfeign%E5%8E%9F%E7%90%86.assets/image-20241109133920305.png)

  ```java
  class DefaultTargeter implements Targeter {
  
  	@Override
  	public <T> T target(FeignClientFactoryBean factory, Feign.Builder feign,
  			FeignContext context, Target.HardCodedTarget<T> target) {
  		return feign.target(target);
  	}
  
  }
  ```

* 进入到feign

  ```java
  public abstract class Feign {
      public <T> T target(Target<T> target) {
        return build().newInstance(target);
      }
  
      public Feign build() {
        Client client = Capability.enrich(this.client, capabilities);
        Retryer retryer = Capability.enrich(this.retryer, capabilities);
        List<RequestInterceptor> requestInterceptors = this.requestInterceptors.stream()
            .map(ri -> Capability.enrich(ri, capabilities))
            .collect(Collectors.toList());
        Logger logger = Capability.enrich(this.logger, capabilities);
        Contract contract = Capability.enrich(this.contract, capabilities);
        Options options = Capability.enrich(this.options, capabilities);
        Encoder encoder = Capability.enrich(this.encoder, capabilities);
        Decoder decoder = Capability.enrich(this.decoder, capabilities);
        InvocationHandlerFactory invocationHandlerFactory =
            Capability.enrich(this.invocationHandlerFactory, capabilities);
        QueryMapEncoder queryMapEncoder = Capability.enrich(this.queryMapEncoder, capabilities);
  
        SynchronousMethodHandler.Factory synchronousMethodHandlerFactory =
            new SynchronousMethodHandler.Factory(client, retryer, requestInterceptors, logger,
                logLevel, decode404, closeAfterDecode, propagationPolicy, forceDecoding);
        ParseHandlersByName handlersByName =
            new ParseHandlersByName(contract, options, encoder, decoder, queryMapEncoder,
                errorDecoder, synchronousMethodHandlerFactory);
          //它是调用一个反射的openfeign
        return new ReflectiveFeign(handlersByName, invocationHandlerFactory, queryMapEncoder);
      }
    }
  }
  ```

* 进入ReflectiveFeign

  ```java
  public class ReflectiveFeign extends Feign {
        ReflectiveFeign(ParseHandlersByName targetToHandlersByName, InvocationHandlerFactory factory,QueryMapEncoder queryMapEncoder) {
      this.targetToHandlersByName = targetToHandlersByName;
      this.factory = factory;
      this.queryMapEncoder = queryMapEncoder;
    }
      //获取实例的方法
      public <T> T newInstance(Target<T> target) {
      Map<String, MethodHandler> nameToHandler = targetToHandlersByName.apply(target);
      Map<Method, MethodHandler> methodToHandler = new LinkedHashMap<Method, MethodHandler>();
      List<DefaultMethodHandler> defaultMethodHandlers = new LinkedList<DefaultMethodHandler>();
  
      for (Method method : target.type().getMethods()) {
        if (method.getDeclaringClass() == Object.class) {
          continue;
        } else if (Util.isDefault(method)) {
          DefaultMethodHandler handler = new DefaultMethodHandler(method);
          defaultMethodHandlers.add(handler);
          methodToHandler.put(method, handler);
        } else {
          methodToHandler.put(method, nameToHandler.get(Feign.configKey(target.type(), method)));
        }
      }
      InvocationHandler handler = factory.create(target, methodToHandler);
      T proxy = (T) Proxy.newProxyInstance(target.type().getClassLoader(),
          new Class<?>[] {target.type()}, handler);
  
      for (DefaultMethodHandler defaultMethodHandler : defaultMethodHandlers) {
        defaultMethodHandler.bindTo(proxy);
      }
      return proxy;
    }
  }
  ```

* 看看怎么获取这个适配器Map<String, MethodHandler> nameToHandler = targetToHandlersByName.apply(target);

  ```java
  public Map<String, MethodHandler> apply(Target target) {
        List<MethodMetadata> metadata = contract.parseAndValidateMetadata(target.type());
        Map<String, MethodHandler> result = new LinkedHashMap<String, MethodHandler>();
        for (MethodMetadata md : metadata) {
          BuildTemplateByResolvingArgs buildTemplate;
          if (!md.formParams().isEmpty() && md.template().bodyTemplate() == null) {
            buildTemplate =
                new BuildFormEncodedTemplateFromArgs(md, encoder, queryMapEncoder, target);
          } else if (md.bodyIndex() != null) {
            buildTemplate = new BuildEncodedTemplateFromArgs(md, encoder, queryMapEncoder, target);
          } else {
            buildTemplate = new BuildTemplateByResolvingArgs(md, queryMapEncoder, target);
          }
          if (md.isIgnored()) {
            result.put(md.configKey(), args -> {
              throw new IllegalStateException(md.configKey() + " is not a method handled by feign");
            });
          } else {
            result.put(md.configKey(),
                factory.create(target, md, buildTemplate, options, decoder, errorDecoder));
          }
        }
        return result;
      }
  ```

* 进入create

  ```java
      public Map<String, MethodHandler> apply(Target target) {
        List<MethodMetadata> metadata = contract.parseAndValidateMetadata(target.type());
        Map<String, MethodHandler> result = new LinkedHashMap<String, MethodHandler>();
        for (MethodMetadata md : metadata) {
          BuildTemplateByResolvingArgs buildTemplate;
          if (!md.formParams().isEmpty() && md.template().bodyTemplate() == null) {
            buildTemplate =
                new BuildFormEncodedTemplateFromArgs(md, encoder, queryMapEncoder, target);
          } else if (md.bodyIndex() != null) {
            buildTemplate = new BuildEncodedTemplateFromArgs(md, encoder, queryMapEncoder, target);
          } else {
            buildTemplate = new BuildTemplateByResolvingArgs(md, queryMapEncoder, target);
          }
          if (md.isIgnored()) {
            result.put(md.configKey(), args -> {
              throw new IllegalStateException(md.configKey() + " is not a method handled by feign");
            });
          } else {
            result.put(md.configKey(),
                factory.create(target, md, buildTemplate, options, decoder, errorDecoder));
          }
        }
        return result;
      }
  ```

* 点击这个里面的create,**final class** SynchronousMethodHandler **implements** MethodHandler ，继承了MethodHandler ，里面有个invoke方法，这是jdk代理后的方法

  ```java
  final class SynchronousMethodHandler implements MethodHandler {
          public MethodHandler create(Target<?> target,
                                  MethodMetadata md,
                                  RequestTemplate.Factory buildTemplateFromArgs,
                                  Options options,
                                  Decoder decoder,
                                  ErrorDecoder errorDecoder) {
        return new SynchronousMethodHandler(target, client, retryer, requestInterceptors, logger,
            logLevel, md, buildTemplateFromArgs, options, decoder,
            errorDecoder, decode404, closeAfterDecode, propagationPolicy, forceDecoding);
      }
  }
  ```

* 创建的是SynchronousMethodHandler，在回到newInstance，里面有一个InvocationHandler，点击InvocationHandler handler = **factory**.create(target, methodToHandler);

  ```java
  public interface InvocationHandlerFactory {
  
    InvocationHandler create(Target target, Map<Method, MethodHandler> dispatch);
  
    /**
     * Like {@link InvocationHandler#invoke(Object, java.lang.reflect.Method, Object[])}, except for a
     * single method.
     */
    interface MethodHandler {
  
      Object invoke(Object[] argv) throws Throwable;
    }
  
    static final class Default implements InvocationHandlerFactory {
  
      @Override
      public InvocationHandler create(Target target, Map<Method, MethodHandler> dispatch) {
        return new ReflectiveFeign.FeignInvocationHandler(target, dispatch);
      }
    }
  }
  
  ```

* 里面有一个FeignInvocationHandler，其实返回的就是SynchronousMethodHandler

  ```java
      FeignInvocationHandler(Target target, Map<Method, MethodHandler> dispatch) {
        this.target = checkNotNull(target, "target");
        this.dispatch = checkNotNull(dispatch, "dispatch for %s", target);
      }
  
      @Override
      public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        if ("equals".equals(method.getName())) {
          try {
            Object otherHandler =
                args.length > 0 && args[0] != null ? Proxy.getInvocationHandler(args[0]) : null;
            return equals(otherHandler);
          } catch (IllegalArgumentException e) {
            return false;
          }
        } else if ("hashCode".equals(method.getName())) {
          return hashCode();
        } else if ("toString".equals(method.getName())) {
          return toString();
        }
  
        return dispatch.get(method).invoke(args);
      }
  ```

* 进入到SynchronousMethodHandler，这里是真正的请求

  ```java
    public Object invoke(Object[] argv) throws Throwable {
      RequestTemplate template = buildTemplateFromArgs.create(argv);
      Options options = findOptions(argv);
      Retryer retryer = this.retryer.clone();
      while (true) {
        try {
          return executeAndDecode(template, options);
        } catch (RetryableException e) {
          try {
            retryer.continueOrPropagate(e);
          } catch (RetryableException th) {
            Throwable cause = th.getCause();
            if (propagationPolicy == UNWRAP && cause != null) {
              throw cause;
            } else {
              throw th;
            }
          }
          if (logLevel != Logger.Level.NONE) {
            logger.logRetry(metadata.configKey(), logLevel);
          }
          continue;
        }
      }
    }
  
    Object executeAndDecode(RequestTemplate template, Options options) throws Throwable {
      Request request = targetRequest(template);
  
      if (logLevel != Logger.Level.NONE) {
        logger.logRequest(metadata.configKey(), logLevel, request);
      }
  
      Response response;
      long start = System.nanoTime();
      try {
        response = client.execute(request, options);
        // ensure the request is set. TODO: remove in Feign 12
        response = response.toBuilder()
            .request(request)
            .requestTemplate(template)
            .build();
      } catch (IOException e) {
        if (logLevel != Logger.Level.NONE) {
          logger.logIOException(metadata.configKey(), logLevel, e, elapsedTime(start));
        }
        throw errorExecuting(request, e);
      }
      long elapsedTime = TimeUnit.NANOSECONDS.toMillis(System.nanoTime() - start);
  
  
      if (decoder != null)
        return decoder.decode(response, metadata.returnType());
  
      CompletableFuture<Object> resultFuture = new CompletableFuture<>();
      asyncResponseHandler.handleResponse(resultFuture, metadata.configKey(), response,
          metadata.returnType(),
          elapsedTime);
  
      try {
        if (!resultFuture.isDone())
          throw new IllegalStateException("Response handling not done");
  
        return resultFuture.join();
      } catch (CompletionException e) {
        Throwable cause = e.getCause();
        if (cause != null)
          throw cause;
        throw e;
      }
    }
  ```

  

* 总结：先使用@EnableFeignClients，他导入了FeignClientsRegistrar，有一个registerBeanDefinitions获取注解信息，最后调用registerFeignClients，回调用registerFeignClient，这个方法里有**url**，**path**，**name**，**contextId**，**fallback**，封装了一个BeanDefinitionBuilder，这个build传入的是FeignClientFactoryBean，他有一个getTarget方法，他调用了Targeter接口的target方法，传入了(FeignClientFactoryBean factory, Feign.Builder feign,FeignContext context, Target.HardCodedTarget<T> target)。他的一个实现类是DefaultTargeter，这个target会调用feign.target(target)，这个方法会调用newInstance方法，newInstance这个方法又会new一个ReflectiveFeign类，这个类也有newInstance方法。他调用 **targetToHandlersByName**.apply(target)返回一个适配器。apply中使用SynchronousMethodHandler.Factory的create方法返回SynchronousMethodHandler适配器。这个SynchronousMethodHandler适配器有invoke方法封装了一个RequestTemplate，调用了executeAndDecode方法执行execute方法返回请求的执行结果。