#### List

* 有序（有下标）通过下标索引可以指定位置，可重复
* List可以用索引下标遍历，类似于数组

* 方法

  * 增add addAll    删 remove(int index)  remove(Obe=ject obj)     改set(int index,Object ele)   查 get(int index)，插入 add(int index,Object obj) addAll()，长度 size()，遍历 iterator 增强for循环，indexOf第一次出现时的索引，lastIndexOf最后一次出现时的索引。

    ```java
        @Test
        public void test1(){
            List collection=new ArrayList();
            collection.add("AA");
            collection.add(123);//自动装箱
            collection.add(new Person("aa",18));
            System.out.println(collection);//这种打印本质都是toString方法，一定在其祖宗上有实现
            System.out.println(collection.toString());
    
            collection.add(2,"cc");
            System.out.println(collection);
    
            collection.remove(2);//删除索引
            System.out.println(collection);
    
            //删除数据必须要传入对象
            collection.remove(Integer.valueOf(2));
    
            Iterator iterator = collection.iterator();
            while (iterator.hasNext()){
                System.out.println(iterator.next());
            }
            for (Object obj:collection) {//jdk5新特性
                System.out.println(obj);
            }
        }
    ```

    

##### List实现类

* 子接口
  * ArrayList:List主要实现类，jdk1.2实现，线程不安全，效率高，底层使用的Object[]数组存储，先指定长度，超过之后扩容再复制，查询o(n)，插入o(n)
  
    ```java
        private static final int DEFAULT_CAPACITY = 10;
    
        /**
         * Shared empty array instance used for empty instances.
         */
        private static final Object[] EMPTY_ELEMENTDATA = {};
    ```
  
  * Vector:古老的实现类，基本不用了，jdk1.0实现，线程安全，效率低，底层使用的Object[]数组存储
  
  * LinkedList：底层采用双向链表实现，插入删除效率高



##### 面试题

* 三个实现类的区别

* 题目，从键盘录入信息，保存到集合List

  ```java
  
  public class test1 {
      public static void main(String[] args) {
          Scanner scanner=new Scanner(System.in);
          System.out.println("请录入学生信息");
          ArrayList list=new ArrayList();
          while (true){
              System.out.println("1:继续录入。 0:结束录入");
              int i = scanner.nextInt();
              if (i==0){
                  break;
              }
              System.out.println("请输入学生姓名");
              String name = scanner.next();
              System.out.println("请输入学生年龄");
              int age = scanner.nextInt();
              list.add(new Person(name,age));
          }
          System.out.println("遍历学生信息");
          for (Object obj:list
               ) {
              Person person= (Person) obj;
              System.out.println("name:"+person.getName()+" age="+person.getAge());
          }
          
      }
  }
  class Person {
      private String name;
      private int age;
  
      public Person(String name, int age) {
          this.name = name;
          this.age = age;
      }
  
      public String getName() {
          return name;
      }
  
      public int getAge() {
          return age;
      }
  
      public void setName(String name) {
          this.name = name;
      }
  
      public void setAge(int age) {
          this.age = age;
      }
  
      @Override
      public String toString() {
          return "Person{" +
                  "name='" + name + '\'' +
                  ", age=" + age +
                  '}';
      }
  
      @Override
      public boolean equals(Object o) {
          if (this == o) return true;
          if (o == null || getClass() != o.getClass()) return false;
          Person person = (Person) o;
          return age == person.age &&
                  Objects.equals(name, person.name);
      }
  
  //    @Override
  //    public int hashCode() {
  //        return Objects.hash(name, age);
  //    }
  }
  
     请录入学生信息
  1:继续录入。 0:结束录入
  1
  请输入学生姓名
  wang
  请输入学生年龄
  18
  1:继续录入。 0:结束录入
  1
  请输入学生姓名
  zi
  请输入学生年龄
  19
  1:继续录入。 0:结束录入
  1
  请输入学生姓名
  jie
  请输入学生年龄
  17
  1:继续录入。 0:结束录入
  0
  遍历学生信息
  name:wang age=18
  name:zi age=19
  name:jie age=17
  
  Process finished with exit code 0
       
  ```

  

