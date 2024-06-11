#### bean的作用域

* 探究是不是单例模式

  ```java
      @Test
      public void testSpringScope(){
          ApplicationContext context=new ClassPathXmlApplicationContext("SpringScope.xml");
          SpringBean bean = context.getBean("SpringBean", SpringBean.class);
          System.out.println(bean);
          SpringBean bean2 = context.getBean("SpringBean", SpringBean.class);
          System.out.println(bean2);
          SpringBean bean3 = context.getBean("SpringBean", SpringBean.class);
          System.out.println(bean3);
      }
  输出结果
  
  wang.zi.jie.bean.SpringBean@7d64e326
  wang.zi.jie.bean.SpringBean@7d64e326
  wang.zi.jie.bean.SpringBean@7d64e326
  ```

* 注释掉所有对象创建，发现spring自己就已经创建好了

  ```java
      @Test
      public void testSpringScope(){
          ApplicationContext context=new ClassPathXmlApplicationContext("SpringScope.xml");
  //        SpringBean bean = context.getBean("SpringBean", SpringBean.class);
  //        System.out.println(bean);
  //        SpringBean bean2 = context.getBean("SpringBean", SpringBean.class);
  //        System.out.println(bean2);
  //        SpringBean bean3 = context.getBean("SpringBean", SpringBean.class);
  //        System.out.println(bean3);
      }
  输出：SpringBean构造方法被调用了
  ```

  ```java
  public class SpringBean {
      public SpringBean(){
          System.out.println("SpringBean构造方法被调用了");
      }
  }
  ```

* 解决方法，在配置文件中加入scope属性

  ```xml
  <bean class="wang.zi.jie.bean.SpringBean" id="SpringBean" scope="prototype"></bean>
  ```

  * 这样在spring实例化的时候并不会创建对象实例（创建城为对象原型）

* scope有八个值（四个常用）：prototype（多例），singleton（单例），request（请求域），session（会话域）

  * 后面这两个只有在web项目才会生效

    ![1710078413454](bean%E7%9A%84%E4%BD%9C%E7%94%A8%E5%9F%9F.assets/1710078413454.png)

* 自定义bean（基本没有人使用）

  * 第一步：自定义Scope。（实现Scope接口）

  - - spring内置了线程范围的类：org.springframework.context.support.SimpleThreadScope，可以直接用。

  - 第二步：将自定义的Scope注册到Spring容器中。

    ```xml
    <bean class="org.springframework.beans.factory.config.CustomScopeConfigurer">
      <property name="scopes">
        <map>
          <entry key="myThread">
            <bean class="org.springframework.context.support.SimpleThreadScope"/>
          </entry>
        </map>
      </property>
    </bean>
    ```

  - 第三步：使用

    ```xml
    <bean id="sb" class="com.powernode.spring6.beans.SpringBean" scope="myThread" />
    ```





##### 设计模式

* 设计模式是一种可以被重复利用的解决方案

* 工厂模式是解决对象创建问题的，所以工厂模式属于创建型设计模式。这里为什么学习工厂模式呢？这是因为Spring框架底层使用了大量的工厂模式。

* 工厂模式有三种形态

  * 第一种：**简单工厂模式（Simple Factory）：不属于23种设计模式之一。简单工厂模式又叫做：静态 工厂方法模式。简单工厂模式是工厂方法模式的一种特殊实现。**
  * 第二种：工厂方法模式（Factory Method）：是23种设计模式之一。
  * 第三种：抽象工厂模式（Abstract Factory）：是23种设计模式之一。

* 简单工厂模式

  * 简单工厂模式的角色包括三个：

    - 抽象产品 角色
    - 具体产品 角色
    - 工厂类 角色

    ```java
    public class WeaponFactroy {
        public static Weapon get(String weaponType){
            if (weaponType == null || weaponType.trim().length() == 0) {
                return null;
            }
            Weapon weapon = null;
            if ("TANK".equals(weaponType)) {
                weapon = new Tank();
            } else if ("FIGHTER".equals(weaponType)) {
                weapon = new Fighter();
            } else if ("DAGGER".equals(weaponType)) {
                weapon = new Dagger();
            } else {
                throw new RuntimeException("不支持该武器！");
            }
            return weapon;
        }
    }
    ```

    ```java
    public abstract class Weapon {
        /**
         * 所有的武器都有攻击行为
         */
        public abstract void attack();
    }
    ```

    ```java
    public class Tank extends Weapon {
        @Override
        public void attack() {
            System.out.println("坦克开炮");
        }
    }
    ```

    ```java
    public class Client {
        public static void main(String[] args) {
            Weapon weapon1 = WeaponFactory.get("TANK");
            weapon1.attack();
    
            Weapon weapon2 = WeaponFactory.get("FIGHTER");
            weapon2.attack();
    
            Weapon weapon3 = WeaponFactory.get("DAGGER");
            weapon3.attack();
        }
    }
    ```

  * 简单工厂模式的优点：

    - 客户端程序不需要关心对象的创建细节，需要哪个对象时，只需要向工厂索要即可，初步实现了责任的分离。客户端只负责“消费”，工厂负责“生产”。生产和消费分离。

    简单工厂模式的缺点：

    - 缺点1：工厂类集中了所有产品的创造逻辑，形成一个无所不知的全能类，有人把它叫做上帝类。显然工厂类非常关键，不能出问题，一旦出问题，整个系统瘫痪。
    - 缺点2：不符合OCP开闭原则，在进行系统扩展时，需要修改工厂类。

* 工厂方法模式

  * 一个工厂对应生产一种产品,这样工厂就不是全能类了

  * 工厂方法模式的角色包括：

    - **抽象工厂角色**
    - **具体工厂角色**
    - 抽象产品角色
    - 具体产品角色

    ```java
    public class Dagger extends Weapon2 {
        @Override
        public void attack() {
            System.out.println("砍");
        }
    }
    ```

    ```java
    public abstract class Weapon2 {
        /**
         * 所有的武器都有攻击行为
         */
        public abstract void attack();
    }
    ```

    ```java
    public abstract class WeaponFactroy {
        public abstract Weapon2 get();
    }
    ```

    ```java
    public class DaggerFactory extends WeaponFactroy{
        @Override
        public Weapon2 get() {
            return new Dagger();
        }
    }
    ```

  * 我们可以看到在进行功能扩展的时候，不需要修改之前的源代码，显然工厂方法模式符合OCP原则。

  * 工厂方法模式的优点：

    - 一个调用者想创建一个对象，只要知道其名称就可以了。 
    - 扩展性高，如果想增加一个产品，只要扩展一个工厂类就可以。
    - 屏蔽产品的具体实现，调用者只关心产品的接口。

  * 工厂方法模式的缺点：

    - 每次增加一个产品时，都需要增加一个具体类和对象实现工厂，使得系统中类的个数成倍增加，在一定程度上增加了系统的复杂度，同时也增加了系统具体类的依赖。这并不是什么好事。



##### bean的实例化方式

* 第一种：构造方法实例化

  ```java
  public class User {
      public User(){
          System.out.println("bean的无参数");
      }
  }
  ```

  ```xml
      <bean id="sb" class="wang.zi.jie.bean.User"></bean>
  ```

  

* 第二种：通过简单工厂模式实例化

  ```java
  public class Star {
      public Star(){
          System.out.println("star的无参构造执行了");
      }
  }
  ```

  ```java
  public class StarFactory {
      public static Star get(){
          return new Star();
      }
  }
  ```

  ```xml
  <!--    获取StarFactory的静态方法get-->
      <bean id="star" class="wang.zi.jie.bean.StarFactory" factory-method="get"></bean>
  ```

  ```java
   @Test
      public void testBeanFactory(){
          ApplicationContext context=new ClassPathXmlApplicationContext("spring.xml");
          Star star = context.getBean("star", Star.class);
          System.out.println(star);
      }
  ```

  

* 第三种：通过factory-bean实例化

  ```java
  public class Gun {
      //工厂方法模式具体产品
      public Gun() {
          System.out.println("Gun的无参构造执行了");
      }
  }
  ```

  ```java
  public class GunFactory {
      public Gun get(){
          return new Gun();
      }
  }
  ```

  ```xml
  <!--    通过factory-bean属性+factory-method属性共同完成-->
  <!--    告诉spring方法，通过哪个方法获取bean-->
      <bean id="gunFactory" class="wang.zi.jie.bean.GunFactory"></bean>
      <bean id="gun" factory-bean="gunFactory" factory-method="get"></bean>
  ```

  

* 第四种：通过FactoryBean接口实例化

  * 以上的第三种方式中，factory-bean是我们自定义的，factory-method也是我们自己定义的。

  * **在Spring中，当你编写的类直接实现FactoryBean接口之后，factory-bean不需要指定了，factory-method也不需要指定了。**

  * factory-bean会自动指向实现FactoryBean接口的类，factory-method会自动指向getObject()方法。

    ```java
    public class Preson {
        public Preson(){
            System.out.println("person的无参构造执行了");
        }
    }
    ```

    ```java
    public class PersonFactoryBean implements FactoryBean {
        @Override
        public Object getObject() throws Exception {
            return new Preson();
        }
    
        @Override
        public Class<?> getObjectType() {
            return null;
        }
        //下面这个方法有默认实现
        @Override
        public boolean isSingleton() {
            return FactoryBean.super.isSingleton();
        }
    ```

    ```xml
        <bean id="person" class="wang.zi.jie.bean.PersonFactoryBean"></bean>
    ```





###### BeanFactory和FactoryBean的区别

* Spring IoC容器的顶级对象，BeanFactory被翻译为“Bean工厂”，在Spring的IoC容器中，“Bean工厂”负责创建Bean对象。

* FactoryBean：它是一个Bean，是一个能够**辅助Spring**实例化其它Bean对象的一个Bean。

* 在Spring中，Bean可以分为两类：

  - 第一类：普通Bean
  - 第二类：工厂Bean（记住：工厂Bean也是一种Bean，只不过这种Bean比较特殊，它可以辅助Spring实例化其它Bean对象。）

* 第三种实例化方式的使用场景

  ```java
  public class Student {
      public Date date;
  
      public void setDate(Date date) {
          this.date = date;
      }
  
      @Override
      public String toString() {
          return "Student{" +
                  "date=" + date +
                  '}';
      }
  }
  ```

  ```java
  public class DteFactory implements FactoryBean {
      public String birth;
      public DteFactory(String birth) {
          this.birth = birth;
      }
      @Override
      public Date getObject() throws Exception {
          SimpleDateFormat format=new SimpleDateFormat("yyyy-MM-dd");
          Date date = format.parse(birth);
          return date;
      }
      @Override
      public Class<?> getObjectType() {
          return null;
      }
  }
  ```

  ```xml
      <bean id="dataFactory" class="wang.zi.jie.bean.DteFactory">
          <constructor-arg name="birth" value="2024-10-21"></constructor-arg>
      </bean>
      <bean id="student" class="wang.zi.jie.bean.Student">
          <property name="date" ref="dataFactory"></property>
      </bean>
  ```

  