

####jdk8新特性

#####lambda表达式

* 为什么要使用lambda表达式
  * 避免匿名内部类定义过多可以让你的代码看起来很简洁
  * 去掉了一堆没有意义的代码，只留下核心的逻辑。
  
* lambda表达式作为接口实现的对象。也是一个匿名函数

* 格式—>为lambda操作符，它的左边是形参列表，右边是重写方法的方法体

  ```java
      @Test
      public void test1(){
          //只适用于一个后向方法
          Runnable runnable=new Runnable() {
              @Override
              public void run() {
                  System.out.println("背景");
              }
          };
          runnable.run();
          Runnable runnable1=()->{
              System.out.println("上海");
          };
          AA  aa=new AA() {
              @Override
              public void accept(String s) {
                  System.out.println(s);
              }
          };
          AA aa1=(String s)->{
              System.out.println(s);
          };
          //类型推断
          AA aa2=(s)->{
              System.out.println(s);
          };
          //只有一个参数
          AA aa3=s->{
              System.out.println(s);
          };
          Comparator<Integer> comparator=new Comparator<Integer>() {
              @Override
              public int compare(Integer o1, Integer o2) {
                  System.out.println(o1);
                  System.out.println(o2);
                  return o1.compareTo(o2);
              }
          };
          Comparator<Integer> comparator1=(o1,o2)->{
              System.out.println(o1);
              System.out.println(o2);
              return o1.compareTo(o2);
          };
          //只有一条语句时，可以省略大括号，此时return也要删掉
          Comparator<Integer> comparator2=(o1,o2)->o1.compareTo(o2);
      }
  ```

  

* 函数式接口：接口只包含唯一一个抽象方法
  
* 对于函数式接口，可以使用Lambda语法创建该接口对象
  
* 只有函数式接口才能用Lambda语法，一般该接口回加@FunctionalInterface方法

* api函数式声明接口所在的包

  * 在jdk8中，java.util.function下

* 四大核心函数式接口

  ​	<img src="Lamda%E8%A1%A8%E8%BE%BE%E5%BC%8F.assets/1694764617614.png" alt="1694764617614" style="zoom:80%;" />

* 传统接口

  ```java
  //创建线程方式，一继承thread，二，重写run方法,三、调用start开启线程
  public class basic {
  
      public static void main(String[] args) throws InterruptedException, ExecutionException {
          Marry marry = new you();
          marry.HappyMarry();
  
      }
  
  }
  
  interface Marry {
      void HappyMarry();
  }
  
  class you implements Marry {
  
      @Override
      public void HappyMarry() {
          // TODO Auto-generated method stub
          System.out.println("结婚");
      }
  }
  
  ```

* 静态内部类方法

  ```java
  //创建线程方式，一继承thread，二，重写run方法,三、调用start开启线程
  public class basic {
      static class you implements Marry {
  
          @Override
          public void HappyMarry() {
              // TODO Auto-generated method stub
              System.out.println("结婚");
          }
      }
  
      public static void main(String[] args) throws InterruptedException, ExecutionException {
          Marry marry = new you();
          marry.HappyMarry();
  
      }
  
  }
  
  interface Marry {
      void HappyMarry();
  }
  
  ```

* 局部内部类

  ```java
  public class basic {
  
      public static void main(String[] args) throws InterruptedException, ExecutionException {
          class you implements Marry {
  
              @Override
              public void HappyMarry() {
                  // TODO Auto-generated method stub
                  System.out.println("结婚");
              }
          }
          Marry marry = new you();
          marry.HappyMarry();
  
      }
  
  }
  
  interface Marry {
      void HappyMarry();
  }
  ```

* 匿名内部类

  ```java
  public class basic {
  
      public static void main(String[] args) throws InterruptedException, ExecutionException {
          Marry marry = new Marry() {
  
              @Override
              public void HappyMarry() {
                  System.out.println("结婚");
              }
  
          };
          marry.HappyMarry();
  
      }
  
  }
  
  interface Marry {
      void HappyMarry();
  }
  
  ```

  

* lambda简化

  ```java
  public class basic {
  
      public static void main(String[] args) throws InterruptedException, ExecutionException {
          Marry marry = () -> {
              System.out.println("结婚");
          };
  
          marry.HappyMarry();
  
      }
  
  }
  
  interface Marry {
      void HappyMarry();
  }
  ```

  * 带参数的lanbda

    ```java
    public class basic {
    
        public static void main(String[] args) throws InterruptedException, ExecutionException {
            Marry marry = (int a) -> {
                System.out.println("结婚");
            };
    
            marry.HappyMarry(1);
    
        }
    
    }
    
    interface Marry {
        void HappyMarry(int a);
    }
    
    ```

    

  *  简化一：去掉参数的类型

  * 简化二：去掉括号

  * 简化三：省略花括号

    ```java
    public class basic {
    
        public static void main(String[] args) throws InterruptedException, ExecutionException {
            Marry marry = (int a) -> {
                System.out.println("结婚");
            };
            marry.HappyMarry(1);
            // 去掉参数类型
            Marry marry2 = (a) -> {
                System.out.println("aa");
            };
            marry2.HappyMarry(0);
            // 去掉参数括号
            Marry marry3 = a -> {
                System.out.println("aa");
            };
            marry3.HappyMarry(0);
            // 去掉花括号
            Marry marry4 = a -> System.out.println("aa");
            marry4.HappyMarry(0);
            // 总结，结构体只有一行才能省略代码体，即大括号
            // 必须是函数式接口
            // 多个参数也可以去掉参数类型，要去掉必须全去掉，多个参数括号不能省略
    
        }
    
    }
    
    interface Marry {
        void HappyMarry(int a);
    }
    
    ```

  

###### 方法引用

* 方法引用可以看做基于lambda表达式进一步刻画

  * 当满足一定条件情况下，可以使用方法引用或构造器引用去替换lambda

* 方法引用本质：作为了函数式接口的实例

* 具体使用

  * 情况一：对象：：实例方法

    ```java
    public class test1 {
        @Test
        public void test1(){
            AA  aa=new AA() {
                @Override
                public void accept(String s) {
                    System.out.println(s);
                }
            };
            //lambda表达式
            AA aa1=s->{
                System.out.println(s);
            };
            //方法引用
            AA aa2=System.out::println;//System.out对象调用了println方法，并且形参的类型和println的参数类型一样，并且都为void
            aa2.accept("hee");
    
            Comparator<Integer> comparator=new Comparator<Integer>() {
                @Override
                public int compare(Integer o1, Integer o2) {
                    System.out.println(o1);
                    System.out.println(o2);
                    return o1.compareTo(o2);
                }
            };
            Employee employee=new Employee("AA", 18);
            Supplier<String> stringSupplier=new Supplier<String>() {
                @Override
                public String get() {
                    return employee.getName();
                }
            };
            //lambda表达式
            Supplier<String> stringSupplier2=()->employee.getName();
            //方法引用
            Supplier<String> stringSupplier3=employee::getName;//返回的参数类型和getName方法的参数类型一样，并且返回都是String
        }
    }
    interface Supplier<E>{
        String get();
    }
    class Employee<E> {
        String name;
        int age;
    
        public Employee(String name, int age) {
            this.name = name;
            this.age = age;
        }
    
        public String getName() {
            return name;
        }
    }
    interface AA{
        void accept(String s);
    }
    ```

    * 要求：函数式接口中的抽象方法a与其内部实现时调用的对象的某个方法b的形参列表和返回值类型都相同
    * 必须是非静态的方法，因为需要对象调用，静态的用下面的

  * 情况二：类：：静态方法

    ```java
    @Test
        public void test1(){
            Comparator<Integer> comparator1=new Comparator<Integer>() {
                @Override
                public int compare(Integer o1, Integer o2) {
                    return Integer.compare(o1, o2);
                }
            };
            //lambda表达式
            Comparator<Integer> comparator2=(o1, o2) -> o1.compareTo(o2);
            //对象引用
            Comparator<Integer> comparator3=Integer::compareTo;
            Function<Double,Long> function=new Function<Double, Long>() {
                @Override
                public Long apply(Double aDouble) {
                    return Math.round(aDouble);
                }
            };
            Function<Double,Long> function1=aDouble ->Math.round(aDouble);
            Function<Double,Long> function2=Math::round;
        }
    ```

    * 要求：函数式接口中的抽象方法a与其内部实现时调用的对象的某个方法b的形参列表和返回值类型都相同或一致（即满足自动装箱）

  * 情况三：类：：实例方法

    ```java
        @Test
        public void test1(){
            Comparator<String> comparator1=new Comparator<String>() {
                @Override
                public int compare(String o1, String o2) {
                    return o1.compareTo(o2);
                }
            };
            //lambda表达式
            Comparator<String> comparator2=(o1, o2) -> o1.compareTo(o2);
            //对象引用
            Comparator<String> comparator3=String :: compareTo;
            Function<Employee,String> function=new Function<Employee, String>() {
                @Override
                public String apply(Employee employee) {
                    return employee.getName();
                }
            };
            Function<Employee,String> function1=employee -> employee.getName();
            Function<Employee,String> function2=Employee::getName;
        }
    ```

    

    * 返回类型一样，抽象方法a参数是n，抽象方法b一个是n-1，恰好多的那一个是调用第二个方法的调用者。并且剩下a的n-1个和b的n-1个一样

###### 构造器引用

* 格式：类名：：new 

  ```java
     @Test
      public void test1(){
          Supplier supplier=new Supplier() {
              @Override
              public Employee get() {
                  return new Employee();
              }
          };
          Supplier supplier1=Employee::new;
          Function<Integer,Employee> function=new Function<Integer, Employee>() {
              @Override
              public Employee apply(Integer integer) {
                  return new Employee("a", 18);
              }
          };
          Function<Integer,Employee> function1=Employee::new;//apply方法是Integer，则他调用的构造器也是Integer的构造器
          
          BiFunction<Integer,String,Employee> function2=new BiFunction<Integer, String, Employee>() {
              @Override
              public Employee apply(Integer integer, String s) {
                  return new Employee(s,integer);
              }
          };
          Function<Integer,Employee> function3=Employee::new;//apply方法是Integer和String，则他调用的构造器也是Integer和String的构造器
      }
  interface Supplier{
      Employee get();
  }
  class Employee<E> {
      String name;
      int age;
  
      public Employee(String name, int age) {
          this.name = name;
          this.age = age;
      }
      public Employee(){
  
      }
  
      public Employee(Integer integer) {
      }
  
      public String getName() {
          return name;
      }
  }
  ```

  * 具体调用哪一个构造器取决于函数式接口方法的·形参列表

###### 数组引用

* 格式：数组名[]：：new

  ```java
     @Test
      public void test1(){
          Supplier supplier=new Supplier() {
              @Override
              public Employee get() {
                  return new Employee();
              }
          };
          Supplier supplier1=Employee::new;
          Function<Integer,Employee[]> function=new Function<Integer, Employee[]>() {
              @Override
              public Employee[] apply(Integer integer) {
                  return new Employee[integer];
              }
          };
          Function<Integer,Employee[]> function1=Employee[]::new;
      }
  ```

  

###### StreamAPI

* Stream APl ( java.util.stream)把真正的函数工编程风格引入到Java中。这是目前为止对Java类库最好的补充，因为stream API可以极大提供Java程序员的生产力，让程序员写出高效率、干净、简洁的代码。

* Stream是Java8中处理集合的关键抽象概念，它可以指定你希望对集合进行的操作，可以执行非常复杂的查找、过滤和映射数据等操作。使用Stream API对集合数据进行操作，就类似于使用sQL执行的数据库查询。也可以使用Stream API来并行执行操作。简言之，Stream API提供了一种亭效且易于使用的处理数据的方式。

* 说明：

  * Stream自己不会存储元素。
  * Stream不会改变源对象。相反。**他们会返回一个持有结果的新Stream.即不会改变原对象**
  * 操作是延迟执行的。这意味着他们会等到需要结果的时候才执行。即一旦执行终止操作，就执行中间操作链。并产生结果。
  * —旦执行了终止操作，就不能再调用其它中间操作或终止操作了。

* Stream API vs 集合框架

  * stream API关注的是多个数据的计算(排序、查找、过滤、映射、遍历等)，面向CPU的。集合关注的数据的存储,向下内存的。
  * Stream API之于集合,类似于SQL之于数据表的查询。

* Stream执行流程

  * 步骤一：获取Stream流，三种方式获取

    ```java
    public class test1 {
        @Test
        public void test1(){
            //通过集合
            List<Employee> employees = EmplyeeData.getEmployees();
            //获取一个顺序流
            Stream<Employee> stream=employees.stream();
            //获取一个并行流
            Stream<Employee> stream1=employees.parallelStream();
    
            //通过数组创建
            Integer[] integers=new Integer[]{1,2,3,4,5};
            Stream<Integer> integerStream= Arrays.stream(integers);
            //基本数据类型的数组创建
            int [] ints=new int[]{1,2,3,4,5};
            IntStream intStream=Arrays.stream(ints);
            //通过Stream方式获取：Stream.of
            Stream<String> stream2=Stream.of("aa","bb");
    
        }
    }
    class Employee {
        String name;
        int age;
        int id;
        double salary;
    
        public Employee(int id,String name, int age,double salary) {
            this.id=id;
            this.name = name;
            this.age = age;
            this.salary=salary;
        }
        public Employee(){
    
        }
    
        public Employee(Integer integer) {
        }
    
        public String getName() {
            return name;
        }
    }
    class EmplyeeData {
        public static List<Employee> getEmployees() {
            List<Employee> list = new ArrayList<>();
            list.add(new Employee(1001, "马化腾", 34, 6000.38));
            list.add(new Employee(1002, "马云", 2, 9876.12));
            list.add(new Employee(1003, "刘强东", 33, 3000.82));
            list.add(new Employee(1004, "雷军", 26, 7657.37));
            list.add(new Employee(1005, "李彦宏", 65, 5555.32));
            list.add(new Employee(1006, "比尔盖茨", 42, 9500.43));
            list.add(new Employee(1007, "任正非", 26, 4333.32));
            list.add(new Employee(1008, "扎克伯格", 35, 2500.32));
            return list;
        }
    }
    ```

  * 中间操作

    * 筛选与切片

      ![1694832073720](jdk8%E6%96%B0%E7%89%B9%E6%80%A7.assets/1694832073720.png)

    ```java
  public class test1 {
        @Test
        public void test1(){
            //通过集合
            List<Employee> employees = EmplyeeData.getEmployees();
            //获取一个顺序流
            Stream<Employee> stream=employees.stream();
            //查询员工工资大于7000的员工信息
            stream.filter(employee -> employee.getSalary()>7000).forEach(System.out::println);
            System.out.println();
            //要想调用其它操作，你必须再重新生成一个新的stream
            //查看前两条
            employees.stream().limit(2).forEach(System.out::println);
            //先过滤再查看前两条
            System.out.println();
            employees.stream().filter(employee -> employee.getSalary()>7000).limit(2).forEach(System.out::println);
    
            //跳过元素
            employees.stream().skip(2).forEach(System.out::println);
            //去重,通过hashcode和equals去除
            employees.stream().distinct().forEach(System.out::println);
    
            //函数映射
            List<String> list= Arrays.asList("aa","bb","cc");
            list.stream().map(s -> s.toUpperCase()).forEach(System.out::println);
            list.stream().map(String ::toUpperCase).forEach(System.out::println);//类：实例
            //获取员工姓名长度大于3
            employees.stream().filter(s-> s.getName().length()>3).forEach(System.out::println);
    
            //排序
            Integer[] integers=new Integer[]{2,1,5,4,6};
            Arrays.asList(integers).stream().sorted().forEach(System.out::println);//不会改变integers
            //自定义的类排序必须实现compare或者传入一个定制排序
            employees.stream().sorted((em1,em2)->Double.compare(em1.getSalary(),em2.getSalary())).forEach(System.out::println);
        }
    }
    class Employee {
        String name;
        int age;
        int id;
        double salary;
    
        public Employee(int id,String name, int age,double salary) {
            this.id=id;
            this.name = name;
            this.age = age;
            this.salary=salary;
        }
        public Employee(){
    
        }
    
        public Employee(Integer integer) {
        }
    
        public String getName() {
            return name;
        }
    
        public double getSalary() {
            return salary;
        }
    
        @Override
        public String toString() {
            return "Employee{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    ", id=" + id +
                    ", salary=" + salary +
                    '}';
        }
    
        @Override
        public int hashCode() {
            return Objects.hash(salary);
        }
    
        @Override
        public boolean equals(Object obj) {
            System.out.println("aa");
            if (this==obj){
                return true;
            }
            Employee employee= (Employee) obj;
            System.out.println(employee.getSalary()==this.getSalary());
            return employee.getSalary()==this.getSalary();
        }
    }
    class EmplyeeData {
        public static List<Employee> getEmployees() {
            List<Employee> list = new ArrayList<>();
            list.add(new Employee(1001, "马化腾", 34, 6000.38));
            list.add(new Employee(1002, "马云", 2, 9876.12));
            list.add(new Employee(1003, "刘强东", 33, 3000.82));
            list.add(new Employee(1004, "雷军", 26, 7657.37));
            list.add(new Employee(1005, "李彦宏", 65, 5555.32));
            list.add(new Employee(1006, "比尔盖茨", 42, 9500.43));
            list.add(new Employee(1007, "任正非", 26, 4333.32));
            list.add(new Employee(1008, "扎克伯格", 35, 2500.32));
            list.add(new Employee(1009, "马斯克", 35, 2500.32));
            return list;
        }
    }
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    
    Employee{name='马化腾', age=34, id=1001, salary=6000.38}
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='刘强东', age=33, id=1003, salary=3000.82}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='李彦宏', age=65, id=1005, salary=5555.32}
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    Employee{name='任正非', age=26, id=1007, salary=4333.32}
    Employee{name='扎克伯格', age=35, id=1008, salary=2500.32}
    Employee{name='马斯克', age=35, id=1009, salary=2500.32}
    Employee{name='马化腾', age=34, id=1001, salary=6000.38}
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    Employee{name='刘强东', age=33, id=1003, salary=3000.82}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='李彦宏', age=65, id=1005, salary=5555.32}
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    Employee{name='任正非', age=26, id=1007, salary=4333.32}
    Employee{name='扎克伯格', age=35, id=1008, salary=2500.32}
    aa
    true
    AA
    BB
    CC
    AA
    BB
    CC
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    Employee{name='扎克伯格', age=35, id=1008, salary=2500.32}
    1
    2
    4
    5
    6
    Employee{name='扎克伯格', age=35, id=1008, salary=2500.32}
    Employee{name='马斯克', age=35, id=1009, salary=2500.32}
    Employee{name='刘强东', age=33, id=1003, salary=3000.82}
    Employee{name='任正非', age=26, id=1007, salary=4333.32}
    Employee{name='李彦宏', age=65, id=1005, salary=5555.32}
    Employee{name='马化腾', age=34, id=1001, salary=6000.38}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    
    Process finished with exit code 0
    
    
    ```
  
    
  
  * 终止操作
  
    * 终止操作的方法返回值类型就不再是Stream了，因此一旦执行终止操作，就结束整个Stream操作了。一旦执行终止操作。就执行中间操作链。最终产生结果并结束stream。即不执行终止操作，他们就不执行中间操作
    
      ```java
      public class test1 {
          @Test
          public void test1(){
              //通过集合
              List<Employee> employees = EmplyeeData.getEmployees();
              //可以没有中间操作，直接终止操作
              //是否所有的员工年龄都大于17
              System.out.println(employees.stream().allMatch(employee -> employee.getAge()>17));
              //是否存在员工年龄大于17
              System.out.println(employees.stream().anyMatch(employee -> employee.getAge()>17));
              //返回第一个元素
              System.out.println(employees.stream().findFirst());
              //获取元素的个数
              System.out.println(employees.stream().count());
              //工资最高
              employees.stream().max((e1,e2)->Double.compare(e1.salary, e2.salary));
      
              //针对于集合，jdk1.8也提供一个foreach
              //所有有四种遍历List 1.Iterator2.增强for 3.一般for 4.forEach
              employees.forEach(System.out::println);
          }
      }
      class Employee {
          String name;
          int age;
          int id;
          double salary;
      
          public Employee(int id,String name, int age,double salary) {
              this.id=id;
              this.name = name;
              this.age = age;
              this.salary=salary;
          }
          public Employee(){
      
          }
      
          public Employee(Integer integer) {
          }
      
          public String getName() {
              return name;
          }
      
          public double getSalary() {
              return salary;
          }
          public int getAge(){
              return age;
          }
      
          @Override
          public String toString() {
              return "Employee{" +
                      "name='" + name + '\'' +
                      ", age=" + age +
                      ", id=" + id +
                      ", salary=" + salary +
                      '}';
          }
      
          @Override
          public int hashCode() {
              return Objects.hash(salary);
          }
      
          @Override
          public boolean equals(Object obj) {
              System.out.println("aa");
              if (this==obj){
                  return true;
              }
              Employee employee= (Employee) obj;
              System.out.println(employee.getSalary()==this.getSalary());
              return employee.getSalary()==this.getSalary();
          }
      }
      class EmplyeeData {
          public static List<Employee> getEmployees() {
              List<Employee> list = new ArrayList<>();
              list.add(new Employee(1001, "马化腾", 34, 6000.38));
              list.add(new Employee(1002, "马云", 2, 9876.12));
              list.add(new Employee(1003, "刘强东", 33, 3000.82));
              list.add(new Employee(1004, "雷军", 26, 7657.37));
              list.add(new Employee(1005, "李彦宏", 65, 5555.32));
              list.add(new Employee(1006, "比尔盖茨", 42, 9500.43));
              list.add(new Employee(1007, "任正非", 26, 4333.32));
              list.add(new Employee(1008, "扎克伯格", 35, 2500.32));
              list.add(new Employee(1009, "马斯克", 35, 2500.32));
              return list;
          }
      }
      
      ```
    
  * reduce
  
    ```java
        @Test
        public void test1(){
            //通过集合
            List<Employee> employees = EmplyeeData.getEmployees();
            //reduce将流中的元素反复结合在一起，得到一个值，返回T
            List<Integer> list= Arrays.asList(1,2,3,4);
            //identity相当于初始值，即种子，在此基础上做相关的操作
            System.out.println(list.stream().reduce(0,(x1,x2)->x1+x2));//10
            System.out.println(list.stream().reduce(0,(x1,x2)->Integer.sum(x1, x2)));//10
            System.out.println(list.stream().reduce(10,Integer::sum));//20
    
        }
    ```
  
    
  
  * collect
  
    ```java
        @Test
        public void test1(){
            //通过集合
            List<Employee> employees = EmplyeeData.getEmployees();
            //查找收入大于5000,并返回一个新的List
            List<Employee> collect = employees.stream().filter(employee -> employee.getSalary() > 5000).collect(Collectors.toList());
            collect.forEach(System.out::println);
        }
    Employee{name='马化腾', age=34, id=1001, salary=6000.38}
    Employee{name='马云', age=2, id=1002, salary=9876.12}
    Employee{name='雷军', age=26, id=1004, salary=7657.37}
    Employee{name='李彦宏', age=65, id=1005, salary=5555.32}
    Employee{name='比尔盖茨', age=42, id=1006, salary=9500.43}
    ```
  
    

###### Optional类

* 到目前为止，臭名昭著的空指针十异常是导致Java应用程序失败订最常见原因。以前，为了解决空指针异常,Google在著名的Guava项目引入了Optional类，通过检查空值的方式避兔空指针异常。受到Google的启发，Optional类已经成为Java 8类库的一部分。

* Optional<T>类(java.util.Optional)是一个容器类，它可以保存类型T的值，代表这个值存在。或者仅仅保存null，表示这个值不存在。如果值存在，则isPresent()方法会返回true，调用get方法会返回该对象。
  Optional提供很多有用的方法，这样我们就不用显式进行空值检测。

  ```java
      @Test
      public void test1() {
          String star = "迪丽热巴";
          System.out.println(star.toString());//如果star为null，就会报空指针
          //使用Optional避免空指针问题
          //1.实例化
          Optional<String> optional=Optional.ofNullable(star);
          /*源码
              public static <T> Optional<T> ofNullable(T value) {
          return value == null ? (Optional<T>) EMPTY
                               : new Optional<>(value);
      }
           */
          //取出来
          //1.get
          System.out.println(optional.get());//取出内部value，为null会报异常
          //2.orElse方法
          String otherStar="杨幂";
          //如果star为null，则用otherStar，如果不为null，则用star
          String finalStar=optional.orElse(otherStar);
          System.out.println(finalStar.toString());
      }
  ```

  

##### String jdk11

* 在命令行不用再先javac再java，可以直接java会运行，但是不会再文件夹中生成class文件了

![1694917816316](jdk8%E6%96%B0%E7%89%B9%E6%80%A7.assets/1694917816316.png)

##### String jdk12

![1694917863967](jdk8%E6%96%B0%E7%89%B9%E6%80%A7.assets/1694917863967.png)

* 实现了Constable接口

* 增加了一些方法

  ![1694917906816](jdk8%E6%96%B0%E7%89%B9%E6%80%A7.assets/1694917906816.png)

##### jdk17

* 标记删除了Applet API,JDK9标记为过时



##### jdk9

* 以前标识符可以用下划线“__”命名，9开始就不可以了



##### GC特性

* JDK9以后默认的垃圾回收器是G1GC.jdk8是Parallel GC
* jdk10 full cc
  * G1最大的亮点就是可以尽量的避免full gc。但毕竟是"尽量”，在有些情况下，G1就要进行full gc了，比如如果它无法足够快的回收内存的时候，它就会强制停止所有的应用线程然后清理。
    在Java10之前，一个单线程版的标记-清除-压缩算法被用于full gc。为了尽量减少full gc带来的影响，在Java10中，就把之前的那个单线程版的标记-清除-压缩的full gc算法改成了支持多个线程同时fullgc。这样也算是减少了full gc所带来的停顿,从而提高性能。
    你可以通过-xX :ParallelGCThreads参数来指定用于并行Gc的线程数。
* JDK11:ZGC，官方Orcle发布
* jdk12可中断的G1 Mixed GC，增强了G1，自动返回未用堆内存给操作系统
* JDK12 Shenandoah GC:低停顿GC  RedHat公司发布
* JDK13: ZGc:将未使用的堆内存归还给操作系统
* JDK14:  ZGC on macOs和windows
* JDK15: ZGC转正
* JDK16:ZGC并发处理

