####static和设计模式

* 设计思想：当我们编写一个类时，其实就是在描述其对象的属性和行为，而并没有产生实质上的对象，只有通过new关键字才会产出对象，这时系统才会分配内存空间给对象，其方法才可以供外部调用。我们有时候希望无论是否产生了对象或无论产生了多少对象的情下,特定的数据在内存空间里只有一份。例如，所有的中国人都有个国家名称，每一个中国人都共享这个国家名称。不必在每一个中国人的实例对象中都单独分配一个用于代表国家名称的变量。

* static静态的，用来修饰结构，书香，方法，代码块，内部类

* 成员变量分类：

  * 使用static修饰的成员变量：静态变量，类变量
  * 不使用static修饰的成员变量：非静态变量，实例变量

* 对比静态变量和实例变量

  * 静态变量在内存空间中只有一份，被类的多个对象所共享，实例每一个对象都有一个。
  * **静态变量在jdk6是在方法区的永久代，jdk7之后就放在堆里面。实例自始自终都存在堆空间对象的实体中。**
  * 静态变量：随着类的加载而加载，由于类只加载一次，所以静态变量也只加载一次。实例对象随着对象的创建而加载，每个对象拥有一份实例变量。
  * 静态变量可以被类和对象直接调用，实例只能通过对象调用。
  * 静态变量随着类的消亡而消亡，实例随对象的消亡而消亡

* 实例

  ![1693383642026](static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383642026.png)
  * 在jdk6中

    <img src="static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383669758.png" alt="1693383669758" style="zoom:80%;" />

  * 在jdk7中

    <img src="static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383713892.png" alt="1693383713892" style="zoom:80%;" />![1693383815194](static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383815194.png)

<img src="static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383713892.png" alt="1693383713892" style="zoom:80%;" />![1693383815194](static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1693383815194.png)

* static修饰方法（类方法，静态方法）
  * 随着类的加载而加载
  * 可以通过类直接调用
  * **静态方法内可以调用静态的属性和方法，调用非静态的结构需要通过实例化对象后才能访问 （比如属性和方法）**，非静态方法什么都能调用。
  * static修饰的方法内，==不能使用this和super（因为没有对象这一说了），省略的是类名==
  
* 什么时候需要声明为静态的
  * 判断当前类的实例是否能共享此成员变量，且此成员变量的值是相同的
  * 开发中，常将一些常量声明为静态的，比如Math类中的PI
  
* 什么时候需要方法声明为静态的
  * 方法内操作的变量为静态变量，则此方法建议声明为静态方法
  * 开发中，常常将工具类方法声明为静态方法，比如Arrays类，Math类
  
* **空指针对象也能调用静态类**

  ```java
  public class test1 {
      public static void main(String[] args) {
          //对比是有另外一个类，两个类都要重写，类内部的那个类也要重写
         Customer customer=null;
          System.out.println(customer.aa);
          customer.test();
  
      }
  }
  class Customer {
      public static int aa=5;
      public static void test(){
          System.out.println("Aa");
      }
  }
  5
  Aa
  ```

  





###### 单例模式

* 如果我们要让类在一个虚拟机中只能产生一个对象，我们首先必须将类的构造器的访问权限设置为private，这样，就不能用new操作符在类的外部产生类的对象了，但在类内部仍可以产生该类的对象。因为在类的外部开始还无法得到类的对象，只能调用该类的某个静态方法以返回类内部创建的对象，静态方法只能访问类中的静态成员变量，所以，指向类内部产生的该类对象的变量也必须定义成静态的。

* 实现方式

  * 饿汉式

    ```java
    public class test1 {
        public static void main(String[] args) {
            //对比是有另外一个类，两个类都要重写，类内部的那个类也要重写
           Bank bank=Bank.getInstanceof();
           Bank bank1=Bank.getInstanceof();
            System.out.println(bank==bank1);
    
        }
    }
    
    class Bank {
        private Bank() {
    
        }
    
        private static Bank bank = new Bank();
    
        public static Bank getInstanceof() {
            return bank;
        }
    }
    true
    ```

    

  * 懒汉式

    ```java
    public class test1 {
        public static void main(String[] args) {
            GirlFriend girlFriend = GirlFriend.getInstance();
            GirlFriend girlFriend1=GirlFriend.getInstance();
            System.out.println(girlFriend==girlFriend1);
    
        }
    }
    
    class GirlFriend {
        private GirlFriend() {
    
        }
    
        private static GirlFriend girlFriend = null;
    
        public static GirlFriend getInstance() {
            if (girlFriend==null){
                girlFriend=new GirlFriend();
            }
            return girlFriend;
        }
    }
    true
    ```

    

  * 饿汉式立即加载，在类加载时就创建。使用更方便，更快，线程是安全的。缺点是内存中占用时间长，懒汉式可以在需要时再创建，节约内存。内存泄漏（本身是个垃圾，但是没有被垃圾回收器回收）



###### main方法

* 理解一：普通的静态方法

  ```java
  package Common;
  
  public class test1 {
      public static void main(String[] args) {
          String[] arg=new String[]{"AA","AAA"};
          GirlFriend.main(arg);
      }
  }
  
  class GirlFriend {
      public static void main(String[] args) {
          for (int i = 0; i <args.length ; i++) {
              System.out.println(args[i]);
          }
      }
  }
  AA
  AAA
  ```

  

* 理解二：可以看作是程序的入口





###### 代码块

* 用来初始化类或者对象信息（即初始化类或者对象的成员变量）

* 只可以用static修饰，其它修饰符不能修饰

  * 因此可以分为静态代码块和非静态代码块

    ```java
    package Common;
    
    public class test1 {
        public static void main(String[] args) {
            Person person = new Person();
            person.eat();
        }
    }
    
    class Person {
        String name;
        int age;
        public void eat(){
            System.out.println("chi");
        }
        {
            System.out.println("非静态代码块");
        }
        static {
            System.out.println("静态代码块");
        }
    
    
    }
    静态代码块
    非静态代码块
    chi
    
    ```

    

* 静态代码块随着类的加载而执行，由于类的加载只会执行一次，所以静态代码块也只会执行一次

  * 给我们一个时机，类加载的时机，是一个特殊时刻，例如可以用于记录日志
  * 用来初始化类的信息，内部可以声明变量，调用属性或方法，编写输出语句等操作
  * **静态代码块只能调用静态结构，不能调用非静态的**
  * ==静态代码块的执行先于非静态代码块==
  * **如果有多个静态代码块，执行顺序按照从上到下**
  * 只要是代码一定是在方法区

  ```java
  package Common;
  
  public class test1 {
      public static void main(String[] args) {
          System.out.println(Person.aa);
      }
  }
  
  class Person {
      String name;
      int age;
      static int aa=5;
      public void eat(){
          System.out.println("chi");
      }
      {
          System.out.println("非静态代码块");
      }
      static {
          System.out.println("静态代码块");
      }
  }
  静态代码块
  5
  ```

  

* **非静态代码块随对象的创建而执行，每创建一次对象就会执行一次，不在类加载时执行****
  
  * 用来初始化对象的信息，内部可以声明变量，调用属性或方法，编写输出语句等操作
  * 可以调用静态结构，也可以非静态结构
  * **非静态代码块在构造方法执行前执行，这也是sun公司提供的对象创建的时机**
  
* **静态代码块和静态变量谁在前谁先执行，如果前面使用后面的，会报错****

  ```java
  public class test {
      static{
          System.out.println(name);
      }
      static int name;
      public static void main(String[] args) {
  
      }
  }//会报错
  ```

  

* **静态方法是没有先后顺序的**

  <img src="static%E5%92%8C%E8%AE%BE%E8%AE%A1%E6%A8%A1%E5%BC%8F.assets/1703771811858.png" alt="1703771811858" style="zoom:50%;" />



###### 属性赋值过程

* 可以给类的非静态属性赋值的位置有

  * 默认初始化1

  * 显式初始化2

  * 构造器中初始化3

  * 有了对象后，通过对象.属性或对象.方法进行赋值4

  * 代码块中初始化5

    ```java
    public class test1 {
        public static void main(String[] args) {
            Oreder oreder = new Oreder();
            System.out.println(oreder.orderId);
        }
    }
    
    class Oreder {
        int orderId=1;
        {
            orderId=2;
        }
    }
    2的证代码块在默认后面
        
    package Common;
    
    public class test1 {
        public static void main(String[] args) {
            Oreder oreder = new Oreder();
            System.out.println(oreder.orderId);
        }
    }
    
    class Oreder {
        int orderId=1;
        {
            orderId=2;
        }
        public Oreder(){
            orderId=3;
        }
    }
    3所以在构造器前面,执行完代码块再执行构造方法
    
    package Common;
    
    public class test1 {
        public static void main(String[] args) {
            Oreder oreder = new Oreder();
            System.out.println(oreder.orderId);
        }
    }
    class Oreder {
        {
            orderId=2;
        }
        int orderId=1;
    }
    1
    ```

  * 综上按先后为1-(2-5他两谁在代码前面谁就先被调用)-3-4



* 在字节码文件中，**声明了几个构造器就会有几个<init>方法，编写的代码中的构造器就会以<init>方法的方式呈现**

  * <init>包括实例变量的显示赋值，代码块中的赋值和构造器中的代码
  * <init>用来初始化当前创建对象的信息的

* 实例变量很多，开发如何选

  * 显示赋值，比较适合于每个对象的属性
  * ==构造器赋值：比较适合每个对象属性值不相同的场景==
  * 代码块赋值：一行代码没法赋完值


```java
package Common;
public class test1 {
    public static void main(String[] args) {
        new Leaf();
    }
}
class Root {
    static {
        System.out.println("root静态代码块");
    }

    {
        System.out.println("root非静态代码块");
    }

    public Root() {
        System.out.println("root普通初始化方法");
    }
}

class Mid extends Root {
    static {
        System.out.println("Mid静态代码块");
    }

    {
        System.out.println("Mid非静态代码块");
    }

    public Mid() {
        System.out.println("Mid普通初始化方法");
    }

    public Mid(String msg) {
        this();
        System.out.println("Mid带参数初始化方法，参数为" + msg);
    }
}

class Leaf extends Mid {
    static {
        System.out.println("Leaf静态代码块");

    }
    {
        System.out.println("Leaf非静态代码块");
    }

    public Leaf() {
        super("msg");
        System.out.println("Leaf普通初始化方法");
    }
}
Leaf静态代码块
Leaf非静态代码块
Mid静态代码块
Mid非静态代码块
root静态代码块
root非静态代码块
root普通初始化方法
Mid普通初始化方法
Mid带参数初始化方法，参数为msg
Leaf普通初始化方法
```

* 题目二

  ```java
  package Common;
  public class test1 {
      static int x,y,z;
      static {
          int x=5;//局部变量
          x--;
      }
      static {
          x--;
      }
      public static void method(){
          y=z++ + ++z;
      }
      public static void main(String[] args) {
          System.out.println("x="+x);
          z--;
          method();
          System.out.println("z="+z);
          System.out.println("result"+(z+y + ++z));
      }
  }
  
  x=-1
  z=1
  result3
  
  ```
  
  
  
* 题目三

  ```java
  package Common;
  
  public class test1 {
      public static void main(String[] args) {
          Mid mid = new Mid();
      }
  }
  
  class Root {
      int i=100;
      {
          System.out.println("base");
      }
  
      public Root() {
          method(i);
      }
      public void method(int i){
          System.out.println("base"+i);
      }
  }
  
  class Mid extends Root {
      int j=70;
      {
          System.out.println("sub");
      }
  
      public Mid() {
          super.method(j);
      }
      public void method(int j){
          System.out.println("sub"+j);
      }
  }
  base
  sub100//方法被覆盖了，调用的是子类的方法
  sub
  base70
  ```

  