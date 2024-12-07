#### spring的aop原理

* 简单来说代理对象生成的过程:容器启动的时候会往容器中注入两个bean，一个 Advisor，它包含advice和pointcut
  * advice 就是一个拦截器，拦截到执行的方法后就去做事务处理
  * pointcut 会拦截使用 @Transaction 的方法。
  * 一个后置处理器，它是实现了BeanPostProcessor的bean，重写了postProcessAfterlnitialization 方法，这个后置处理器会遍历容器中所有的bean，判断当前容器里面有没有满足自己的Advisor，如果有就基于此生成代理对象。

* 先进入到**class** CglibAopProxy **implements** AopProxy, Serializable {

  ```java
  //里面有一个
  private static class DynamicAdvisedInterceptor implements MethodInterceptor, Serializable {
      try {
  				if (this.advised.exposeProxy) {
  					// Make invocation available if necessary.
  					oldProxy = AopContext.setCurrentProxy(proxy);
  					setProxyContext = true;
  				}
  				// Get as late as possible to minimize the time we "own" the target, in case it comes from a pool...
  				target = targetSource.getTarget();
  				Class<?> targetClass = (target != null ? target.getClass() : null);
          //获取拦截器和一些通知，像前置通知就是在这里，组成了拦截器链
  				List<Object> chain = this.advised.getInterceptorsAndDynamicInterceptionAdvice(method, targetClass);
  				Object retVal;
  				// Check whether we only have one InvokerInterceptor: that is,
  				// no real advice, but just reflective invocation of the target.
  				if (chain.isEmpty() && CglibMethodInvocation.isMethodProxyCompatible(method)) {
  					// We can skip creating a MethodInvocation: just invoke the target directly.
  					// Note that the final invoker must be an InvokerInterceptor, so we know
  					// it does nothing but a reflective operation on the target, and no hot
  					// swapping or fancy proxying.
  					Object[] argsToUse = AopProxyUtils.adaptArgumentsIfNecessary(method, args);
  					retVal = invokeMethod(target, method, argsToUse, methodProxy);
  				}
  				else {
  					// We need to create a method invocation...
  					retVal = new CglibMethodInvocation(proxy, target, method, args, targetClass, chain, methodProxy).proceed();
  				}
  				retVal = processReturnType(proxy, target, method, retVal);
  				return retVal;
  			}
  }
  ```

  ![image-20241108091012656](spring%E7%9A%84aop%E5%8E%9F%E7%90%86.assets/image-20241108091012656.png)

* AOP的本质就是拦截器，放在目标方法之前或者之后执行。ExopseINvocationInterceptor是入口

* 会调用proceed方法

  ```java
  public Object proceed() throws Throwable {
  		// We start with an index of -1 and increment early.
  		if (this.currentInterceptorIndex == this.interceptorsAndDynamicMethodMatchers.size() - 1) {
  			return invokeJoinpoint();
  		}
  
  		Object interceptorOrInterceptionAdvice =
  				this.interceptorsAndDynamicMethodMatchers.get(++this.currentInterceptorIndex);
  		if (interceptorOrInterceptionAdvice instanceof InterceptorAndDynamicMethodMatcher) {
  			// Evaluate dynamic method matcher here: static part will already have
  			// been evaluated and found to match.
  			InterceptorAndDynamicMethodMatcher dm =
  					(InterceptorAndDynamicMethodMatcher) interceptorOrInterceptionAdvice;
  			Class<?> targetClass = (this.targetClass != null ? this.targetClass : this.method.getDeclaringClass());
  			if (dm.methodMatcher.matches(this.method, targetClass, this.arguments)) {
  				return dm.interceptor.invoke(this);
  			}
  			else {
  				// Dynamic matching failed.
  				// Skip this interceptor and invoke the next in the chain.
  				return proceed();
  			}
  		}
  		else {
  			// It's an interceptor, so we just invoke it: The pointcut will have
  			// been evaluated statically before this object was constructed.
  			return ((MethodInterceptor) interceptorOrInterceptionAdvice).invoke(this);
  		}
  	}
  ```

  * 拦截器执行invoke方法，帮助我们触发调用

    ```java
    	@Override
    	@Nullable
    	public Object invoke(MethodInvocation mi) throws Throwable {
    		try {
    			return mi.proceed();
    		}
    		finally {
    			invokeAdviceMethod(getJoinPointMatch(), null, null);
    		}
    	}
    ```

  * 真正执行目标方法

    ```java
    		protected Object invokeJoinpoint() throws Throwable {
    			if (this.methodProxy != null) {
    				try {
    					return this.methodProxy.invoke(this.target, this.arguments);
    				}
    				catch (CodeGenerationException ex) {
    					logFastClassGenerationFailure(this.method);
    				}
    			}
    			return super.invokeJoinpoint();
    		}
    ```

    