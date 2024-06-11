#### 循环依赖

* A对象中有B属性。B对象中有A属性。这就是循环依赖。我依赖你，你也依赖我。

  * 比如：丈夫类Husband，妻子类Wife。Husband中有Wife的引用。Wife中有Husband的引用。

    ![1710224812796](spring%E8%A7%A3%E5%86%B3%E5%BE%AA%E7%8E%AF%E4%BE%9D%E8%B5%96%E7%9A%84%E9%97%AE%E9%A2%98.assets/1710224812796.png)

* 测试一下在singleton+setter的模式下产生的循环依赖，Spring是否能够解决？

  ```java
  public class Husband {
      private String name;
      private Wife wife;
  }
  ```

  ```java
  public class Husband {
      private String name;
      private Wife wife;
      public void setName(String name) {
          this.name = name;
      }
      public String getName() {
          return name;
      }
      public void setWife(Wife wife) {
          this.wife = wife;
      }
      // toString()方法重写时需要注意：不能直接输出wife，输出wife.getName()。要不然会出现递归导致的栈内存溢出错误。因为互相调用了
      @Override
      public String toString() {
          return "Husband{" +
                  "name='" + name + '\'' +
                  ", wife=" + wife.getName() +
                  '}';
      }
  }
  ```

  ```java
  public class Wife {
      private String name;
      private Husband husband;
  
      public void setName(String name) {
          this.name = name;
      }
  
      public String getName() {
          return name;
      }
  
      public void setHusband(Husband husband) {
          this.husband = husband;
      }
  
      // toString()方法重写时需要注意：不能直接输出husband，输出husband.getName()。要不然会出现递归导致的栈内存溢出错误。
      @Override
      public String toString() {
          return "Wife{" +
                  "name='" + name + '\'' +
                  ", husband=" + husband.getName() +
                  '}';
      }
  }
  
  ```

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <beans xmlns="http://www.springframework.org/schema/beans"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://www.springframework.org/schema/beans http://www.springframework.org/schema/beans/spring-beans.xsd">
  
      <bean id="husbandBean" class="com.powernode.spring6.bean.Husband" scope="singleton">
          <property name="name" value="张三"/>
          <property name="wife" ref="wifeBean"/>
      </bean>
      <bean id="wifeBean" class="com.powernode.spring6.bean.Wife" scope="singleton">
          <property name="name" value="小花"/>
          <property name="husband" ref="husbandBean"/>
      </bean>
  </beans>
  ```

  * **在singleton + set注入的情况下，循环依赖是没有问题的。Spring可以解决这个问题。主要原因是在这种模式下，spring管理可以分为两个阶段**

    * 第一个阶段：在spring容器加载的时候，实例化bean，只要任意一个bean实例化之后，马上进行“曝光”【不等属性赋值就曝光】
    * 第二个阶段：曝光之后，、再进行属性赋值（即调用set的方法）

    

* 测试一下在prototype+setter的模式下产生的循环依赖，Spring是否能够解决？

  * **会出现BeanCurrentlyInCreationException**
  * 循环依赖的**所有Bean**的scope="prototype"的时候，产生的循环依赖，Spring是无法解决的，会出现**BeanCurrentlyInCreationException**异常。
  * 两个Bean，如果其中一个是singleton，另一个是prototype，是没有问题的。
  * 原因：因为两个都在new新的对象，而不是像单例模式那样使用已有的

* 测试一下singleton + 构造注入的方式
  * 也是出现问题，因为构造方法没有执行完成，无法进行曝光





* Spring解决循环依赖的机理

  * Spring为什么可以解决set + singleton模式下循环依赖？

    * 根本的原因在于：这种方式可以做到将“实例化Bean”和“给Bean属性赋值”这两个动作分开去完成。

  * ==实例化Bean的时候：调用无参数构造方法来完成。**此时可以先不给属性赋值，可以提前将该Bean对象“曝光”给外界。**==

  * 给Bean属性赋值的时候：调用setter方法来完成。

  * 两个步骤是完全可以分离开去完成的，并且这两步不要求在同一个时间点上完成。

  * 也就是说，Bean都是单例的，我们可以先把所有的单例Bean实例化出来，放到一个集合当中（我们可以称之为缓存），所有的单例Bean全部实例化完成之后，以后我们再慢慢的调用setter方法给属性赋值。这样就解决了循环依赖的问题。

    

    

    

##### 反射机制

* 你知道以下这几条信息：

  - 类名是：wang.zi.jie.beanLife.User2

  - 该类中有String类型的name属性和int类型的age属性。

  - 另外你也知道该类的设计符合javabean规范。（也就是说属性私有化，对外提供setter和getter方法）

  - 你如何通过反射机制给User对象的name属性赋值zhangsan，给age属性赋值20岁。

    ```java
        @Test
        public void testReflect2() throws Exception {
            // 已知类名
            String className = "wang.zi.jie.beanLife.User2";
            // 已知属性名
            String propertyName = "age";
            // 通过反射机制给User对象的age属性赋值20岁
            Class<?> clazz = Class.forName(className);
            Object obj = clazz.newInstance(); // 创建对象
            // 根据属性名获取setter方法名
            String setMethodName = "set" + propertyName.toUpperCase().charAt(0) + propertyName.substring(1);
            // 获取Method
            Method setMethod = clazz.getDeclaredMethod(setMethodName, int.class);
            // 调用Method
            setMethod.invoke(obj, 20);
            System.out.println(obj);
        }
    ```

    

  

