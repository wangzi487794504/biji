#### Map类

* 存储一对一对数据(key-value)

  <img src="Map%E7%B1%BB.assets/1704978568208.png" alt="1704978568208" style="zoom:67%;" />

* **传入比较器可以改变jdk原有的类的排序方式，比如Integer类，把升序改成降序**

* HashMap:主要实现类1.2时代，线程不安全，执行效率高，可以添加null的key和value，**底层也是数组+单向链表+红黑树存储**

  ```java
      public void test1(){
          Map map=new HashMap();
          map.put(null, null);
      }
  {null=null}
  ```

  * LinkedHashMap:HashMap的子类，在原基础上，增加了一对双向链表，用于记录添加元素的先后顺序，便于遍历

    ```java
    @Test
        public void test1(){
            Map map=new LinkedHashMap();
            map.put("Tom", 23);
            map.put("BB", 23);
            map.put("CC", 23);
            //顺序和添加的顺序一样，因为有双向链表记录
            System.out.println(map);
        }
    ```

    

* Hashtable：古老实现类1.0时代。线程安全，执行效率低，不可以添加null的key或value(一个是null都不行)，存储是数组+单向链表存储

  * 子类：Properties:存储的key-value都是String类型，常用来处理属性文件

* TreeMap:底层使用红黑树，就是排序二叉树，可以按照key-value中的key元素指定属性的大小进行遍历，一是自然排序，二是定制排序



###### HashMap

* key是不相同也无序，和set一样

* 他的默认容量是16，默认加载因子是0.75，即容量达到75%就开始扩容

  *   默认的初始容量是2的幂 ，因为这样会散列均匀，提高集合的存储效率
  * 向Map集合中存，以及从Map集合中取，都是先调用key的hashCode方法，然后再调用equals方法。equals方法有可能调用，也有可能不调用（单向链表没有元素时不会调用）。
  * **从jdk8开始，在哈希表单向链表中数量大于8个会变红黑树数据结构，当红黑树数量小于6时又变回链表**

  ```java
      /**
       * The default initial capacity - MUST be a power of two.
       */
      static final int DEFAULT_INITIAL_CAPACITY = 1 << 4; // aka 16
  
      /**
       * The maximum capacity, used if a higher value is implicitly specified
       * by either of the constructors with arguments.
       * MUST be a power of two <= 1<<30.
       */
      static final int MAXIMUM_CAPACITY = 1 << 30;
  
      /**
       * The load factor used when none specified in constructor.
       */
      static final float DEFAULT_LOAD_FACTOR = 0.75f;
      /**
       * The bin count threshold for using a tree rather than list for a
       * bin.  Bins are converted to trees when adding an element to a
       * bin with at least this many nodes. The value must be greater
       * than 2 and should be at least 8 to mesh with assumptions in
       * tree removal about conversion back to plain bins upon
       * shrinkage.
       */
      static final int TREEIFY_THRESHOLD = 8;
  
      /**
       * The bin count threshold for untreeifying a (split) bin during a
       * resize operation. Should be less than TREEIFY_THRESHOLD, and at
       * most 6 to mesh with shrinkage detection under removal.
       */
      static final int UNTREEIFY_THRESHOLD = 6;
  ```

  

* **HashMap允许key和value为null，但是key只能有一个，HashTable的key和value都不能为null，会空指针异常**

* HashTable是一个线程安全的，但是基本不用，他的初始化容量为11，加载因子0.75

  * 扩容=原容量乘2加1

  ```JAVA
     public Hashtable() {
          this(11, 0.75f);
      }
      protected void rehash() {
          int oldCapacity = table.length;
          Entry<?,?>[] oldMap = table;
  
          // overflow-conscious code
          int newCapacity = (oldCapacity << 1) + 1;
          if (newCapacity - MAX_ARRAY_SIZE > 0) {
              if (oldCapacity == MAX_ARRAY_SIZE)
                  // Keep running with MAX_ARRAY_SIZE buckets
                  return;
              newCapacity = MAX_ARRAY_SIZE;
          }
          Entry<?,?>[] newMap = new Entry<?,?>[newCapacity];
  
          modCount++;
          threshold = (int)Math.min(newCapacity * loadFactor, MAX_ARRAY_SIZE + 1);
          table = newMap;
  
          for (int i = oldCapacity ; i-- > 0 ;) {
              for (Entry<K,V> old = (Entry<K,V>)oldMap[i] ; old != null ; ) {
                  Entry<K,V> e = old;
                  old = old.next;
  
                  int index = (e.hash & 0x7FFFFFFF) % newCapacity;
                  e.next = (Entry<K,V>)newMap[index];
                  newMap[index] = e;
              }
          }
      }
  ```

  

* value可以重复，也是无序，它的存放位置取决于key

  <img src="Map%E7%B1%BB.assets/1691037128675.png" alt="1691037128675" style="zoom:80%;" />

* key和value组成了一个整体叫Entry，因为key不一样，所以Entry也不一样好，所以Entry是一个Set，所以key所在类要重写equals和hashCode方法

  ![1704452904824](Map%E7%B1%BB.assets/1704452904824.png)

* Entry是Map的一个静态内部类

  ![1704469800988](Map%E7%B1%BB.assets/1704469800988.png)

  * 哈希表HashMap使用不当时无法发挥性能!
  * 假设将所有的hashCode()方法返回值固定为某个值，那么会导致底层哈希表变成了纯单向链表。这种情况我们成为:散列分布不均匀。
  * 什么是散列分布均匀?
    * 假设有100个元素，10个单向链表，那么每个单向链表上有10个节点，这是最好的，是散列分布均匀的。
  * 假设将所有的hashCode()方法返回值都设定为不一样的值，可以吗，有什么问题?
    * 不行，因为这样的话导致底层哈希表就成为―维数组了，没有链表的概念了。也是散列分布不均匀。

* 放在HashMap集合key部分的元素，以及放在HashSet集合中的元素，需要同时重写hashCode和equals方法。

######Map常用方法

* 增put(key,value)  删 remove(key) return value 改 put(key,value)  就是覆盖putAll  查  get(key)，长度 size()，遍历  遍历key用keySet，返回一个Set，遍历value用values()返回是Collection  遍历entry用entrySet,返回是Set    **没有插入，因为根本没有有序**

* 接口里面可以声明接口

  ```java
  package Common;
  
  import org.junit.Test;
  import java.util.*;
  
  public class test1 {
      @Test
      public void test1(){
          HashMap map=new HashMap();
          map.put("Tom", 23);
          map.put("BB", 22);
          map.put("CC", 24);
          map.put(67, 24);
          map.put(new Person("wang", 18), 25);
          //顺序和添加的顺序一样，因为有双向链表记录
          System.out.println(map);
          //长度
          System.out.println(map.size());
          //移除
          int value= (int) map.remove("Tom");//返回是Object
          System.out.println(value);
          //修改
          map.put("BB", 23);
          System.out.println(map);
          //查询
          Object bb = map.get("BB");
          System.out.println(bb);
          //遍历
          Set keySet = map.keySet();
          for (Object obj:keySet
               ) {
              System.out.println(obj);
          }
          Collection values = map.values();
          Iterator iterator = values.iterator();
          while (iterator.hasNext()){
              System.out.println(iterator.next());
          }
          Set entrySet = map.entrySet();
          for (Object obj:entrySet
               ) {
              System.out.println((Map.Entry)obj);
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
  {BB=22, CC=24, Tom=23, 67=24, Person{name='wang', age=18}=25}
  5
  23
  {BB=23, CC=24, 67=24, Person{name='wang', age=18}=25}
  23
  BB
  CC
  67
  Person{name='wang', age=18}
  23
  24
  24
  25
  BB=23
  CC=24
  67=24
  Person{name='wang', age=18}=25
  ```

  

###### TreeMap

* 底层是红黑树

* 他和TreeSet都是中序遍历：左根右

* 对自己定义的类型只能设计排序规则，要实现Comparable接口

  ```java
  private final Comparator<? super K> comparator;
  //构造方法
     public TreeMap() {
          comparator = null;
      }
    public TreeMap(Comparator<? super K> comparator) {
          this.comparator = comparator;
      }
      public V put(K key, V value) {
          Entry<K,V> t = root;
          if (t == null) {
              compare(key, key); // type (and possibly null) check
  
              root = new Entry<>(key, value, null);
              size = 1;
              modCount++;
              return null;
          }
          int cmp;
          Entry<K,V> parent;
          // split comparator and comparable paths
          Comparator<? super K> cpr = comparator;
          if (cpr != null) {
              do {
                  parent = t;
                  cmp = cpr.compare(key, t.key);
                  if (cmp < 0)
                      t = t.left;
                  else if (cmp > 0)
                      t = t.right;
                  else
                      return t.setValue(value);
              } while (t != null);
          }
          else {
              if (key == null)
                  throw new NullPointerException();
              @SuppressWarnings("unchecked")
                  Comparable<? super K> k = (Comparable<? super K>) key;
              do {
                  parent = t;
                  cmp = k.compareTo(t.key);
                  if (cmp < 0)
                      t = t.left;
                  else if (cmp > 0)
                      t = t.right;
                  else
                      return t.setValue(value);
              } while (t != null);
          }
          Entry<K,V> e = new Entry<>(key, value, parent);
          if (cmp < 0)
              parent.left = e;
          else
              parent.right = e;
          fixAfterInsertion(e);
          size++;
          modCount++;
          return null;
      }
  ```

  *  Comparable<? super K> k = (Comparable<? super K>) key;这个代码，如果你没传比较器，就把你添加的这个对象强转为比较器k，然后再调用cmp = k.compareTo(t.key);

* 可以按照key-value大小进行排序

* 使用自然排序或定制排序

  ```java
   @Test
      public void test1(){
          TreeMap treeMap=new TreeMap();
          treeMap.put("AA", 15);
          treeMap.put("CC", 14);
          treeMap.put("BB", 16);
          Set entrySet = treeMap.entrySet();
          //会按key排序
          for (Object entry:entrySet
               ) {
              System.out.println(entry);
          }
      }
  AA=15
  BB=16
  CC=14
  ```

  * 要求添加的key是同一个类型
  
    ```java
    
    public class test1 {
        @Test
        public void test1(){
            TreeMap treeMap=new TreeMap();
            Person person=new Person("AA", 18);
            Person person1=new Person("Jach", 19);
            Person person2=new Person("Tom", 19);//年龄一样了，这个进不去
            Person person3=new Person("Jerry", 17);
            treeMap.put(person, 15);
            treeMap.put(person1, 14);
            treeMap.put(person2, 16);
            treeMap.put(person3, 16);
            Set entrySet = treeMap.entrySet();
            //会按key排序
            for (Object entry:entrySet
                 ) {
                System.out.println(entry);
            }
            System.out.println(treeMap.containsKey(new Person("sss", 18)));//true
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
        //只比较年龄
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
        //姓名和年龄都比较
    //    @Override
    //    public int compareTo(Object o) {
    //        if (this==o){
    //            return 0;
    //        }
    //        if (o instanceof Person){
    //            Person person= (Person) o;
    //            int value= this.age-person.age;
    //            if (value!=0){
    //                return value;
    //            }
    //            return -this.name.compareTo(person.name);
    //        }
    //        throw  new RuntimeException("类型不匹配");
    //    }
    }
    ```
  
    

* 定制排序

  ```java
  public class test1 {
     
      @Test
      public void test1(){
          Comparator comparator=new Comparator() {
              @Override
              public int compare(Object o1, Object o2) {
                  if (o1 instanceof  Person && o2 instanceof Person){
                      Person person= (Person) o1;
                      Person  person1= (Person) o2;
                      int value=person.getName().compareTo(person1.getName());
                      if (value!=0){
                          return value;
                      }
                      return  person.getAge()-person1.getAge();
                  }
                  throw new RuntimeException("类型不匹配");
              }
          };
          TreeMap treeMap=new TreeMap(comparator);
          Person person=new Person("AA", 18);
          Person person1=new Person("Jach", 19);
          Person person2=new Person("Tom", 19);//年龄一样了，这个进不去
          Person person3=new Person("Jerry", 17);
          treeMap.put(person, 15);
          treeMap.put(person1, 14);
          treeMap.put(person2, 16);
          treeMap.put(person3, 16);
          Set entrySet = treeMap.entrySet();
          //会按key排序
          for (Object entry:entrySet
               ) {
              System.out.println(entry);
          }
          System.out.println(treeMap.containsKey(new Person("sss", 18)));//true
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
      //只比较年龄
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
      //姓名和年龄都比较
  //    @Override
  //    public int compareTo(Object o) {
  //        if (this==o){
  //            return 0;
  //        }
  //        if (o instanceof Person){
  //            Person person= (Person) o;
  //            int value= this.age-person.age;
  //            if (value!=0){
  //                return value;
  //            }
  //            return -this.name.compareTo(person.name);
  //        }
  //        throw  new RuntimeException("类型不匹配");
  //    }
  }
  
  ```

  

##### Properties

* **class** Properties **extends** Hashtable<Object,Object> 
* 被称为属性类对象，是线程安全的

```java
  @Test
    public void test1() throws IOException {
        File file=new File("info.properties");
        System.out.println(file.getAbsolutePath());
        FileInputStream inputStream=new FileInputStream(file);
        Properties properties=new Properties();
        properties.load(inputStream);
        //读取数据
        String name = properties.getProperty("name");
        String age = properties.getProperty("age");
        System.out.println("name="+name+"  age="+age);
    }
```

