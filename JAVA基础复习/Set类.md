#### Set

* 相对比collection，它的方法一模一样，没有新增方法

* 存储无序，不可重复，是放到了HashMap的key部分

* 实现类

  * HashSet：主要实现类，底层是HashMap，用数组+单向链表+红黑树,jdk8当中

  * HashSet相同，指equals和hashcode都相同

    ```java
     public void test1(){
            Set collection=new HashSet();
            collection.add("AA");
            collection.add(123);//自动装箱
            collection.add(new Person("aa",18));
            System.out.println(collection);
            Iterator iterator = collection.iterator();
            while (iterator.hasNext()){
                System.out.println(iterator.next());
            }
            for (Object obj:collection) {//jdk5新特性
                System.out.println(obj);
            }
            System.out.println(collection.contains(new Person("aa", 18)));//false,加hashcode就会为true
        }
    ```

    

  * LinkedHashSet，是HashSet子类,用数组+单向链表+红黑树基础上添加了一组双向链表用于记录添加元素的先后顺序，可以按照添加元素的顺序进行遍历，便于频繁的查询操作。

  * TreeSet：底层使用红黑树，**可以按照添加的元素的指定属性大小进行排序遍历**

* 使用场景

  * 过滤重复数据，频率使用较少

* **解释HashCode**

  * 首先理解无序性，无序性不是随机性，也不是添加顺序和遍历元素顺序不一致。无序性是指与添加元素属性的位置有关，不像ArrayList是紧密排列的，它是先通过hashcode算出编号，编号决定了位置排列，就是判断元素是否相同的时候不仅equals方法要满足，hashcode也要相同。先判断hsah,==如果方法里不重写hashcode方法，就会使用Object里的hascode，这时两个new的对象的hashcode就会不一样==
  * 再理解不可重复性

* **添加到HashSet/LinkedHashSet中元素的要求，不适用于TreeSet**

  * 要求元素重写equals方法和hashcode方法，用idea自动生成即可。



##### TreeSet

* 无序（存的顺序和输出顺序不同）不可重复，可以自动按照元素大小排序

* **加入的必须是同一个类型，这样才能比较大小，要不然会报ClassCastException，**它是一种二叉树，它是按照元素比大小的方法生成树，比大小的方法是继承Comparable接口，实现了compareTo方法，就按这个方法比大小（这是自然排序）。或者使用定制排序也可以

* 它和equals和hascode方法无关。

  ```java
  
  public class test1 {
      public static void main(String[] args) {
        
      }
      @Test
      public void test1(){
          TreeSet collection=new TreeSet();
          Person person=new Person("AA", 18);
          Person person1=new Person("BB", 17);
          Person person2=new Person("cc",19);
          Person person3=new Person("dd",19);//会加不进去，他不比较equals
          collection.add(person);
          collection.add(person1);
          collection.add(person2);
          collection.add(person3);
          System.out.println(collection);
          Iterator iterator = collection.iterator();
          while (iterator.hasNext()){
              System.out.println(iterator.next());
          }
      }
  }
  class Person implements Comparable{
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
          System.out.println("equals方法");
          if (this == o) return true;
          if (o == null || getClass() != o.getClass()) return false;
          Person person = (Person) o;
          return age == person.age &&
                  Objects.equals(name, person.name);
      }
  
      @Override
      public int hashCode() {
          return Objects.hash(name, age);
      }
  
      @Override
      public int compareTo(Object o) {
          if (this==o){
              return 0;
          }
          if (o instanceof Person){
              Person person= (Person) o;
              return this.age-person.age;
          }
          throw  new RuntimeException("类型不匹配");
      }
  }
  [Person{name='BB', age=17}, Person{name='AA', age=18}, Person{name='cc', age=19}]
  Person{name='BB', age=17}
  Person{name='AA', age=18}
  Person{name='cc', age=19}
  ```

  

* 如果compareTo或者compare方法对于两个插入的对象返回值为0，即在这个函数中，他们两个一样，则只能插入一个。所以是自己设计的比大小规则

  ```java
  
  public class test1 {
      public static void main(String[] args) {
  
      }
      @Test
      public void test1(){
  
          Comparator comparator=new Comparator() {
              @Override
              public int compare(Object o1, Object o2) {
                  if (o1 instanceof Person&& o2 instanceof Person){
                      Person person= (Person) o1;
                      Person person1= (Person) o2;
                      return -(person.getAge()-person1.getAge());
                  }
                  throw  new RuntimeException("对象不匹配");
              }
          };
          TreeSet collection=new TreeSet(comparator);
          Person person=new Person("AA", 18);
          Person person1=new Person("BB", 17);
          Person person2=new Person("cc",19);
          Person person3=new Person("dd",19);//会加不进去，他不比较equals
          collection.add(person);
          collection.add(person1);
          collection.add(person2);
          collection.add(person3);
  
          System.out.println(collection);
          Iterator iterator = collection.iterator();
          while (iterator.hasNext()){
              System.out.println(iterator.next());
          }
      }
  }
  class Person implements Comparable{
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
          System.out.println("equals方法");
          if (this == o) return true;
          if (o == null || getClass() != o.getClass()) return false;
          Person person = (Person) o;
          return age == person.age &&
                  Objects.equals(name, person.name);
      }
  
      @Override
      public int hashCode() {
          return Objects.hash(name, age);
      }
  
      @Override
      public int compareTo(Object o) {
          if (this==o){
              return 0;
          }
          if (o instanceof Person){
              Person person= (Person) o;
              return this.age-person.age;
          }
          throw  new RuntimeException("类型不匹配");
      }
  }
  [Person{name='cc', age=19}, Person{name='AA', age=18}, Person{name='BB', age=17}]
  Person{name='cc', age=19}
  Person{name='AA', age=18}
  Person{name='BB', age=17}
  ```

  

* 注意，只要调用构造方法传入了Comparator，就是定制排序





##### 练习题

* 去重

  ```java
  public class test1 {
      public static void main(String[] args) {
          ArrayList arrayList=new ArrayList();
          arrayList.add(34);
          arrayList.add(34);
          arrayList.add(34);
          arrayList.add(34);
          arrayList.add(22);
          arrayList.add(22);
          arrayList.add(22);
          arrayList.add(22);
          arrayList.add(45);
          arrayList.add(45);
          arrayList.add(45);
          List list=duplicateList(arrayList);
          System.out.println(list);
      }
      public static List duplicateList(List list){
          HashSet set=new HashSet();
          for (Object s:list
               ) {
              set.add(s);
          }
          List list1=new ArrayList();
          for (Object obj:set
               ) {
              list1.add(obj);
          }
          return list1;
      }
  }
  [34, 22, 45]
  ```

  

* 编写一个程序，获取10个1至20的随机数，要求随机数不能重复，并把最终的随机数输出到控制台

  ```java
  public class test1 {
      public static void main(String[] args) {
          Random random=new Random();
          HashSet set=new HashSet();
          while (true){
              set.add(random.nextInt(20));
              if (set.size()==10){
                  break;
              }
          }
          for (Object obj:set
               ) {
              System.out.println(obj);
          }
      }
  }
  ```

  

![1691029165459](Set%E7%B1%BB.assets/1691029165459.png)

* 如图，修改属性再删除会删除不到，因为他是按修改的属性去计算hashcode的位置，比如原属性是aa，计算出存储位置为1，现在修改为cc，然后再删除，会删除不掉，因为删除时会按cc计算存储位置，但是它的存储位置目前在aa的位置。

  ```java
  public class test1 {
      public static void main(String[] args) {
          HashSet set=new HashSet();
          Person person=new Person("AA", 18);
          Person person1=new Person("BB", 17);
          set.add(person);
          set.add(person1);
          //此时修改person的属性
          person.setAge(19);
          set.remove(person);//原理,删除时hashcode映射的位置不对
          System.out.println(set);//[Person{name='AA', age=19}, Person{name='BB', age=17}]
          //再添加一个19，原理：这里是hashcode不同
          set.add(new Person("AA", 19));//[Person{name='AA', age=19}, Person{name='BB', age=17}, Person{name='AA', age=19}]
          System.out.println(set);
          //再来添加一个18，原理：这里是hashcode相同，但是equals不同
          set.add(new Person("AA", 18));
          System.out.println(set);
      }
  }
  class Person implements Comparable{
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
          System.out.println("equals方法");
          if (this == o) return true;
          if (o == null || getClass() != o.getClass()) return false;
          Person person = (Person) o;
          return age == person.age &&
                  Objects.equals(name, person.name);
      }
  
      @Override
      public int hashCode() {
          return Objects.hash(name, age);
      }
  
      @Override
      public int compareTo(Object o) {
          if (this==o){
              return 0;
          }
          if (o instanceof Person){
              Person person= (Person) o;
              return this.age-person.age;
          }
          throw  new RuntimeException("类型不匹配");
      }
  }
  [Person{name='AA', age=19}, Person{name='BB', age=17}]
  [Person{name='AA', age=19}, Person{name='BB', age=17}, Person{name='AA', age=19}]
  equals方法
  [Person{name='AA', age=19}, Person{name='BB', age=17}, Person{name='AA', age=18}, Person{name='AA', age=19}]
  ```

  