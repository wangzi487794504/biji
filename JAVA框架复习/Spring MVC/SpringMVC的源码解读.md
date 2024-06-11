##### Spring MVC执行源码解读

* 使用伪代码讲述

  ```java
  //前端控制器最核心的类
  public class DispatcherServlet extends FrameworkServlet{
      //前端控制器最核心的方法，处理请求
      protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
          HttpServletRequest processedRequest = request;
          HandlerExecutionChain mappedHandler = null;
          boolean multipartRequestParsed = false;
          WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
  		 // 根据请求对象request获取
          // 这个对象是在每次发送请求时都创建一个，是请求级别的
          // 该对象中描述了本次请求应该执行的拦截器是哪些，顺序是怎样的，要执行的处理器是哪个
          //HandlerExecutionChain一次请求对应一个对象
          HandlerExecutionChain mappedHandler = getHandler(processedRequest);
          
          //根据处理器获取处理器适配对象，Handler就是我们写的Controller
          HandlerAdapter ha = this.getHandlerAdapter(mappedHandler.getHandler());
          
          //执行所有拦截器的preHandle方法
          if (!mappedHandler.applyPreHandle(processedRequest, response)) {
               return;
          }
          
          //调用处理器方法，返回ModelAndView对象
          //在调用处理器方法之前会进行数据绑定，将表单提交的数据绑定到处理器方法上。（底层是通过WebDataBinder完成的）
          mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
          
          //执行拦截器的postHandle方法
          mappedHandler.applyPostHandle(processedRequest, response, mv);
          
          //处理分发结果，本质上就是显示结果到浏览器
          this.processDispatchResult(processedRequest, response, mappedHandler, mv, (Exception)dispatchException);
      }
      
      private void processDispatchResult(HttpServletRequest request, HttpServletResponse response, @Nullable HandlerExecutionChain mappedHandler, @Nullable ModelAndView mv, @Nullable Exception exception) throws Exception {
  		//渲染
          this.render(mv, request, response);
          //执行该请求所对应的所有拦截器的afterCompletion方法
          mappedHandler.triggerAfterCompletion(request, response, (Exception)null);
      }
      
      protected void render(ModelAndView mv, HttpServletRequest request, HttpServletResponse response) throws Exception {
          //通过视图解析器进行解析返回试图对象
          view = this.resolveViewName(viewName, mv.getModelInternal(), locale, request);
          //调用视图对象的渲染
          view.render(mv.getModelInternal(), request, response);
      }
      
      //
      protected View resolveViewName(String viewName, @Nullable Map<String, Object> model, Locale locale, HttpServletRequest request) throws Exception {
  		//视图解析器
          ViewResolver viewResolver = (ViewResolver)var5.next();
          //通过视图解析器返回View
          View view = viewResolver.resolveViewName(viewName, locale);      
          return null;
      }
  }
  //每一个接口都有自己的实现类，例如View接口的实现类：Themleaf View，InterResourceView
  public interface View {
  	//视图接口
      void render(@Nullable Map<String, ?> model, HttpServletRequest request, HttpServletResponse response) throws Exception;
  }
  
  //视图解析器接口，他的实现类也很多，如ThymeleafView、InternalResourceView
  public interface ViewResolver {
      @Nullable
      View resolveViewName(String viewName, Locale locale) throws Exception;
  }
  ```



* 上面代码更深入版本

  * 第一个类HandlerExecutionChain

    ```java
    public class HandlerExecutionChain {
        private static final Log logger = LogFactory.getLog(HandlerExecutionChain.class);
        //这是最重要的三个
        private final Object handler;
        //将所有的拦截器按照顺序放到了ArrayList集合中
        private final List<HandlerInterceptor> interceptorList;
        private int interceptorIndex;
    }
    ```

  * HandlerMethod是什么？

    * HandlerMethod是最核心的执行目标，翻译为处理器方法
    * 注意：HandleMethod是在web服务器启动时初始化spring容器的时候就创建好了。比较重要的属性有beanName(就是控制层的名字)和Method（即使控制层类中的哪个方法）

  * do

    ```java
        protected HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
            if (this.handlerMappings != null) {
                Iterator var2 = this.handlerMappings.iterator();
    
                while(var2.hasNext()) {
                    HandlerMapping mapping = (HandlerMapping)var2.next();
                    //这个才是最重要的
                    HandlerExecutionChain handler = mapping.getHandler(request);
                    if (handler != null) {
                        return handler;
                    }
                }
            }
    
           
    ```

    * HandlerExecutionChain mappedHandler =**this**.getHandler(processedRequest);本质上是HandlerExecutionChain handler = mapping.getHandler(request);、
    
    * HandlerMapping mapping是一个接口，专门负责映射的。就是本质上根据请求路径去映射处理器方法。有很多实现类：RequestMappingHandlerMapping，他会在循环遍历中去找。
    
      ```java
          protected HandlerExecutionChain getHandler(HttpServletRequest request) throws Exception {
              if (this.handlerMappings != null) {
                  //循环找对应的映射处理器方法
                  Iterator var2 = this.handlerMappings.iterator();
                  while(var2.hasNext()) {
                      HandlerMapping mapping = (HandlerMapping)var2.next();
                      HandlerExecutionChain handler = mapping.getHandler(request);
                      if (handler != null) {
                          return handler;
                      }
                  }
              }
      
              return null;
          }
      ```
    
      * 他的父类的父类是AbstractHandlerMethodMapping
    
        ```java
        public class RequestMappingHandlerMapping extends RequestMappingInfoHandlerMapping
        		implements MatchableHandlerMapping, EmbeddedValueResolverAware{
            //他有一个注册
            	protected void registerHandlerMethod(Object handler, Method method, T mapping) {
                //它是注册的，不是每一次请求就创建一个对象，而是在服务器中创建
        		this.mappingRegistry.register(mapping, handler, method);
        	}
        }
            
        public abstract class RequestMappingInfoHandlerMapping extends AbstractHandlerMethodMapping<RequestMappingInfo> {
            //他有一个方法
            	protected HandlerMethod createHandlerMethod(Object handler, Method method) {
        		if (handler instanceof String beanName) {
                    
                    //在服务器启动后执行
        			return new HandlerMethod(beanName,
        					obtainApplicationContext().getAutowireCapableBeanFactory(),
        					obtainApplicationContext(),
        					method);
        		}
        		return new HandlerMethod(handler, method);
        	}
            
            
            		public void register(T mapping, Object handler, Method method) {
        			this.readWriteLock.writeLock().lock();
        				HandlerMethod handlerMethod = createHandlerMethod(handler, method);
        this.pathLookup.add(path, mapping);
        				}
        }
        ```
    
        * 他把HandlerExecutionChain handler = mapping.getHandler(request);。这个HandlerExecutionChain 不仅封装了handler
    
  * 分析HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());
  
    * 底层使用了适配器模式，每一个处理器（我们自己写的Controller），都有自己适合的处理器适配器
  
    * 在SpringMVC当中处理器适配器也有很多种，其中一个比较有名的，常用的处理器适配器是：RequestMappingHandleAdapter
  
    * HandlerAdapter也是一个接口：其中有一个常用的实现类：RequestMappingHandlerAdapter
  
    * 在服务器启动阶段，所有的HandlerAdapter接口的实现类都会创建出来。List<HandlerAdapter> handlerAdapters
  
    * HandlerAdapter是适配器，是对HandlerMethod进行的配置
  
    * 在DispatcherServlet类中，如下代码：
  
      ```	java
      	protected HandlerAdapter getHandlerAdapter(Object handler) throws ServletException {
      		if (this.handlerAdapters != null) {
      			for (HandlerAdapter adapter : this.handlerAdapters) {
      				if (adapter.supports(handler)) {
      					return adapter;
      				}
      			}
      		}
      		throw new ServletException("No adapter for handler [" + handler +
      				"]: The DispatcherServlet configuration needs to include a HandlerAdapter that supports this handler");
      	}
      ```
  
  * 分析**if** (!mappedHandler.applyPreHandle(processedRequest, response)) {**return**;}
  
    ````java
    	boolean applyPreHandle(HttpServletRequest request, HttpServletResponse response) throws Exception {
    		for (int i = 0; i < this.interceptorList.size(); i++) {
    			HandlerInterceptor interceptor = this.interceptorList.get(i);
    			if (!interceptor.preHandle(request, response, this.handler)) {
    				triggerAfterCompletion(request, response, null);
    				return false;
    			}
    			this.interceptorIndex = i;
    		}
    		return true;
    	}
    ````
  
    * 遍历List集合，从List集合中去除每一个HandlerInterceptor对象，调用preHandle，i++，可见是顺序调用
  
  * 分析调用处理器方法：mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
  
    * ha是处理器适配器HandlerAdapter，mv是ModelAndView对象，这个方法是最核心的，调用请求路径对应的HandlerMethod
  
      ```java
      public class RequestMappingHandlerAdapter extends AbstractHandlerMethodAdapter
      		implements BeanFactoryAware, InitializingBean {
                  
              //有这麽一个方法
          	protected ModelAndView handleInternal(HttpServletRequest request,HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {
                  
                  mav = invokeHandlerMethod(request, response, handlerMethod);
              }
          
          
             //还有这麽一个方法
          protected ModelAndView invokeHandlerMethod(HttpServletRequest request,HttpServletResponse response, HandlerMethod handlerMethod) throws Exception {
            //获取一个数据绑定工厂  
            WebDataBinderFactory binderFactory = getDataBinderFactory(handlerMethod);
      		ModelFactory modelFactory = getModelFactory(handlerMethod, binderFactory);
      		//获取一个handlerMethod
      		ServletInvocableHandlerMethod invocableMethod = createInvocableHandlerMethod(handlerMethod);
              
              //设置参数
              invocableMethod.setDataBinderFactory(binderFactory);
                       invocableMethod.setParameterNameDiscoverer(this.parameterNameDiscoverer);
      		invocableMethod.setMethodValidator(this.methodValidator);
              //可调用的方法执行
              invocableMethod.invokeAndHandle(webRequest, mavContainer);
          }
      }
      ```
  
      * 在HandlerAdapter中做的核心事情;
        * 将前端提交的form数据通过HttpMessageConverter，将其转换成POJO对象。并将数据绑定到Handler
  
  * 分析代码：mappedHandler.applyPostHandle(processedRequest, response, mv);
  
    * 这行代码执行的是HandlerExecutionChain的applyPostHandle方法
  
      ```java
      	void applyPostHandle(HttpServletRequest request, HttpServletResponse response, @Nullable ModelAndView mv)
      			throws Exception {
      		for (int i = this.interceptorList.size() - 1; i >= 0; i--) {
      			HandlerInterceptor interceptor = this.interceptorList.get(i);
      			interceptor.postHandle(request, response, this.handler, mv);
      		}
      	}
      ```
  
  * 分析代码：processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);
  
    ```java
    private void processDispatchResult(HttpServletRequest request, HttpServletResponse response,
    			@Nullable HandlerExecutionChain mappedHandler, @Nullable ModelAndView mv,
    			@Nullable Exception exception) throws Exception {
        //调用render方法
        render(mv, request, response);
        //调用triggerAfterCompletion方法
        mappedHandler.triggerAfterCompletion(request, response, null);
    }
    ```
  
* 从图片角度看执行流程

   <img src="SpringMVC%E7%9A%84%E6%BA%90%E7%A0%81%E8%A7%A3%E8%AF%BB.assets/%E6%9C%AA%E5%91%BD%E5%90%8D%E6%96%87%E4%BB%B6.png" alt="img" style="zoom:150%;" /> 

* tomcat启动时做了什么

  * 核心类的继承关系：DispatcherServlet ==extends== FrameworkServlet ==extends== HttpServletBean ==extends== HttpServlet ==extends== GenericServlet implements Servlet  **到HttpServlet就都是Servlet规范里的，前面的都是spring自己的**

  * DispatcherServlet 的构造方法，DispatcherServlet 被构建出来，会执行init()方法，他没有实现，就会找父类的init()方法

    ```jav
    	public DispatcherServlet() {
    		super();
    		setDispatchOptionsRequest(true);
    	}
    ```

  * 在GenericServlet 有两个init（）方法。下面这个被实现了子类

    ```java
        public void init(ServletConfig config) throws ServletException {
            this.config = config;
            this.init();
        }
        public void init() throws ServletException {
    
        }
    ```

  * HttpServletBean：**public abstract class** HttpServletBean **extends** HttpServlet **implements** EnvironmentCapable, EnvironmentAware 

    ```java
    	public final void init() throws ServletException {
    
    		// Set bean properties from init parameters.
    		PropertyValues pvs = new ServletConfigPropertyValues(getServletConfig(), this.requiredProperties);
    		if (!pvs.isEmpty()) {
    			try {
    				BeanWrapper bw = PropertyAccessorFactory.forBeanPropertyAccess(this);
    				ResourceLoader resourceLoader = new ServletContextResourceLoader(getServletContext());
    				bw.registerCustomEditor(Resource.class, new ResourceEditor(resourceLoader, getEnvironment()));
    				initBeanWrapper(bw);
    				bw.setPropertyValues(pvs, true);
    			}
    			catch (BeansException ex) {
    				if (logger.isErrorEnabled()) {
    					logger.error("Failed to set bean properties on servlet '" + getServletName() + "'", ex);
    				}
    				throw ex;
    			}
    		}
    
    		// Let subclasses do whatever initialization they like.
    		initServletBean();
    	}
    ```

    * 他有一个initServletBean();里面没有内容，我们找到被重写的这个方法

      ```java
      	protected void initServletBean() throws ServletException {
      	}
      ```

    * 我们可以追到**public abstract class** FrameworkServlet **extends** HttpServletBean **implements** ApplicationContextAware {}重写了这些方法

      ```java
      	protected final void initServletBean() throws ServletException {
      		getServletContext().log("Initializing Spring " + getClass().getSimpleName() + " '" + getServletName() + "'");
      		if (logger.isInfoEnabled()) {
      			logger.info("Initializing Servlet '" + getServletName() + "'");
      		}
      		long startTime = System.currentTimeMillis();
      
      		try {
                  //这是一个初始化，是一个适用于Web项目的上下文对象
      			this.webApplicationContext = initWebApplicationContext();
      			initFrameworkServlet();
      		}
      	}
      ```

    * 我们可以追到his.webApplicationContext = initWebApplicationContext();

      ```java
      	protected WebApplicationContext initWebApplicationContext() {
      		WebApplicationContext rootContext =				WebApplicationContextUtils.getWebApplicationContext(getServletContext());
      		WebApplicationContext wac = null;
      		if (this.webApplicationContext != null) {
      			wac = this.webApplicationContext;
      			if (wac instanceof ConfigurableWebApplicationContext cwac && !cwac.isActive()) {
      				if (cwac.getParent() == null) {
      					cwac.setParent(rootContext);
      				}
      				configureAndRefreshWebApplicationContext(cwac);
      			}
      		}
      		if (wac == null) {
      			wac = findWebApplicationContext();
      		}
      		if (wac == null) {
      			wac = createWebApplicationContext(rootContext);
      		}
      
      		if (!this.refreshEventReceived) {
      			synchronized (this.onRefreshMonitor) {
                      //有一个这个方法
      				onRefresh(wac);
      			}
      		}
      		if (this.publishContext) {
      			String attrName = getServletContextAttributeName();
      			getServletContext().setAttribute(attrName, wac);
      		}
      		return wac;
      	}
      ```

    * onRefresh(wac);点击去，发现没有实现，去找子类的实现，在**public class** DispatcherServlet **extends** FrameworkServlet 实现了

      ```java
      	protected void onRefresh(ApplicationContext context) {
      		initStrategies(context);
  	}
      	protected void initStrategies(ApplicationContext context) {
      		initMultipartResolver(context);
      		initLocaleResolver(context);
      		initThemeResolver(context);
              //初始化了他的list
      		initHandlerMappings(context);
      		initHandlerAdapters(context);
      		initHandlerExceptionResolvers(context);
      		initRequestToViewNameTranslator(context);
      		initViewResolvers(context);
      		initFlashMapManager(context);
      	}
      ```
    
    * 点击initHandlerMappings(context);
    
      ```java
      private void initHandlerMappings(ApplicationContext context) {
      		this.handlerMappings = null;
      
      		if (this.detectAllHandlerMappings) {
      			// Find all HandlerMappings in the ApplicationContext, including ancestor contexts.
      			Map<String, HandlerMapping> matchingBeans =
      					BeanFactoryUtils.beansOfTypeIncludingAncestors(context, HandlerMapping.class, true, false);
      			if (!matchingBeans.isEmpty()) {
      				this.handlerMappings = new ArrayList<>(matchingBeans.values());
      				// We keep HandlerMappings in sorted order.
      				AnnotationAwareOrderComparator.sort(this.handlerMappings);
      			}
      		}
      		else {
      			try {
      				HandlerMapping hm = context.getBean(HANDLER_MAPPING_BEAN_NAME, HandlerMapping.class);
      				this.handlerMappings = Collections.singletonList(hm);
      			}
      			catch (NoSuchBeanDefinitionException ex) {
      				// Ignore, we'll add a default HandlerMapping later.
      			}
      		}
      
      ```
    
      

