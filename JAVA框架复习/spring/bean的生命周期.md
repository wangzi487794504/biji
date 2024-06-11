##### bean的生命周期

* Bean生命周期可以粗略的划分为五大步：

  - 第一步：实例化Bean（无参构造）
  - 第二步：Bean属性赋值（set方法赋值）
  - 第三步：初始化Bean（调用bean的init方法）
  - 第四步：使用Bean
  - 第五步：销毁Bean(调用bean的destory方法)

* 需要手动指定初始化方法和销毁方法（这两个方法都是自己手动写）

  ```java
  public class User {
      private String name;
      public void setName(String name){
          System.out.println("第二步：给对象的属性赋值");
          this.name=name;
      }
      public User(){
          System.out.println("第一步，无参数构造方法执行");
      }
      public void initBean(){
          System.out.println("第三步：初始化bean");
      }
      public void destoryBean(){
          System.out.println("第五步：销毁bean");
      }
  }
  ```

  ```xml
      <bean id="sb" class="wang.zi.jie.beanLife.User" init-method="initBean" destroy-method="destoryBean">
          <property name="name" value="aaa"></property>
      </bean>
  
  ```

  ```java
      @Test
      public void testBeanFactory3(){
          ApplicationContext context=new ClassPathXmlApplicationContext("spring2.xml");
          User sb = context.getBean("sb", User.class);
          System.out.println("第四步：销毁bean"+sb);
          //必须关闭spring容器，才会销毁对象，只有ClassPathXmlApplicationContext类才有close()方法。
          ClassPathXmlApplicationContext classPathXmlApplicationContext = (ClassPathXmlApplicationContext) context;
          classPathXmlApplicationContext.close();
      }
  第一步，无参数构造方法执行
  第二步：给对象的属性赋值
  第三步：初始化bean
  第四步：销毁beanwang.zi.jie.beanLife.User@40db2a24
  第五步：销毁bean
  ```

  

* Bean生命周期之七步

  * 在以上的5步中，第3步是初始化Bean，如果你还想在初始化前和初始化后添加代码，可以加入“Bean后处理器”。
  * 编写一个类实现BeanPostProcessor类，并且重写before和after方法
  * 七步：
    * 第一步：实例化Bean（无参构造）
    * 第二步：Bean属性赋值（set方法赋值）
    * 第三步：初始化Bean（调用bean的init方法）
    * 第四步：使用Bean处理器的before方法
    * 第五步：使用Bean
    * 第六步：使用Bean的after方法
    * 第七步：销毁Bean(调用bean的destory方法)

  ```java
  public class LogUserBean implements BeanPostProcessor {
      @Override
      public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
          System.out.println("执行后处理器的before方法");
          return BeanPostProcessor.super.postProcessBeforeInitialization(bean, beanName);
      }
      //第一个参数bean对象，第二个参数bean名字
      @Override
      public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
          System.out.println("执行后处理器的after方法");
          return BeanPostProcessor.super.postProcessAfterInitialization(bean, beanName);
      }
  }
  ```

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  <!--    配置Bean后处理器，注意这个bean后处理器用于整个配置文件中所有的bean-->
      <bean class="wang.zi.jie.beanLife.LogUserBean"></bean>
      <bean id="sb" class="wang.zi.jie.beanLife.User" init-method="initBean" destroy-method="destoryBean">
          <property name="name" value="aaa"></property>
      </bean>
  
  </beans>
  ```

  

* bean生命周期之10步

  * 如果根据源码跟踪，可以划分更细粒度的步骤

    <img src="bean%E7%9A%84%E7%94%9F%E5%91%BD%E5%91%A8%E6%9C%9F.assets/1710221905751.png" alt="1710221905751" style="zoom: 67%;" />

  * Aware相关的接口包括：BeanNameAware、BeanClassLoaderAware、BeanFactoryAware

    - 当Bean实现了BeanNameAware，Spring会将Bean的名字传递给Bean。
    - 当Bean实现了BeanClassLoaderAware，Spring会将加载该Bean的类加载器传递给Bean。
    - 当Bean实现了BeanFactoryAware，Spring会将Bean工厂对象传递给Bean。

  * 添加这三个位的特点：都是在检查你的bean是否实现了特定的接口.如果实现了这个接口，则Spring容器会调用接口中的方法

    * 点位1：使用Bean处理器的before方法前（第一个点位有三个接口）
    * 点位2：使用Bean处理器的before方法后
    * 点位三：使用bean后，销毁bean前

    ```JAVA
    public class User implements BeanNameAware, BeanClassLoaderAware, BeanFactoryAware, InitializingBean,DisposableBean {
        private String name;
        public void setName(String name){
            System.out.println("第二步：给对象的属性赋值");
            this.name=name;
        }
        public User(){
            System.out.println("第一步，无参数构造方法执行");
        }
        public void initBean(){
            System.out.println("第三步：初始化bean");
        }
        public void destoryBean(){
            System.out.println("第五步：销毁bean");
        }
    
        @Override
        public void setBeanClassLoader(ClassLoader classLoader) {
            System.out.println("bean类的加载器是："+classLoader);
        }
    
        @Override
        public void setBeanFactory(BeanFactory beanFactory) throws BeansException {
            System.out.println("bean类的生产工厂是："+beanFactory);
        }
    
        @Override
        public void setBeanName(String name) {
            System.out.println("bean类的名字是："+name);
        }
    
        @Override
        public void afterPropertiesSet() throws Exception {
            System.out.println("InitializingBean执行");
        }
    
        @Override
        public void destroy() throws Exception {
            
        }
    }
    ```

    

* 注意：spring容器只对singlen的bean进行完整的生命周期管理，如果是prototype作用域的bean，spring容器只负责将bean初始化管理（只负责前8步）



* 自己new的对象怎么让spring管理

  ```java
  public class User2 {
  }
  ```

  ```java
      @Test
      public void testBeanFactory4(){
          User2 user2=new User2();
          System.out.println(user2);
          //将自己new的放入spring容器来管理
          DefaultListableBeanFactory factory=new DefaultListableBeanFactory();
          factory.registerSingleton("userBean", user2);
          //从Spring容器中获取
          Object userBean = factory.getBean("userBean");
          System.out.println(userBean);
      }
  ```

  