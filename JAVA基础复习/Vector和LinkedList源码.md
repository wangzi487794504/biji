#### Vector源码

* 底层初始化的数组，长度为10，Object[] elementData=new Object[10];

* 当超过十个元素后，需要扩容，默认为原来的两倍。

* 线程安全的

* 代码

  ```java
        Vector vector=new Vector();
          vector.add("aa");
          vector.add("bb");
  ```

* 源码分析

  ```java
      private void checkPackageAccess(Class<?> cls, ProtectionDomain pd) {
          final SecurityManager sm = System.getSecurityManager();
          
          
     public Vector() {
          this(10);
      }
          
     public Vector(int initialCapacity) {
          this(initialCapacity, 0);
      }
          
          
     public Vector(int initialCapacity, int capacityIncrement) {
          super();
          if (initialCapacity < 0)
              throw new IllegalArgumentException("Illegal Capacity: "+
                                                 initialCapacity);
          this.elementData = new Object[initialCapacity];
          this.capacityIncrement = capacityIncrement;
         
         
        public synchronized boolean add(E e) {
          modCount++;
          ensureCapacityHelper(elementCount + 1);
          elementData[elementCount++] = e;
          return true;
      }
         
         
         
         private void ensureCapacityHelper(int minCapacity) {
          // overflow-conscious code
          if (minCapacity - elementData.length > 0)
              grow(minCapacity);
      }   
  ```

  <img src="Vector%E6%BA%90%E7%A0%81.assets/1692169946618.png" alt="1692169946618" style="zoom:50%;" />

* 扩容源码

  ```java
     private void grow(int minCapacity) {
          // overflow-conscious code
          int oldCapacity = elementData.length;
          int newCapacity = oldCapacity + ((capacityIncrement > 0) ?
                                           capacityIncrement : oldCapacity);
          if (newCapacity - minCapacity < 0)
              newCapacity = minCapacity;
          if (newCapacity - MAX_ARRAY_SIZE > 0)
              newCapacity = hugeCapacity(minCapacity);
          elementData = Arrays.copyOf(elementData, newCapacity);
      }
  ```

  

###### LinkedList

* 使用的是双向链表

  ```java
  public class LinkedList<E>
      extends AbstractSequentialList<E>
      implements List<E>, Deque<E>, Cloneable, java.io.Serializable
  {
    //...
  }
  ```

  * `List` : 表明它是一个列表，支持添加、删除、查找等操作，并且可以通过下标进行访问。
  * `Deque` ：继承自 `Queue` 接口，具有双端队列的特性，支持从两端插入和删除元素，方便实现栈和队列等数据结构。
  * `Cloneable` ：表明它具有拷贝能力，可以进行深拷贝或浅拷贝操作。
  * `Serializable` : 表明它可以进行序列化操作，也就是可以将对象转换为字节流进行持久化存储或网络传输，非常方便。

* 不需要考虑扩容问题

* 代码

  ```java
    LinkedList<String> linkedList=new LinkedList<>();
          linkedList.add("aa");
          linkedList.add("bb");
  ```

* 源码

  ```java
  首先先检查类
          public Class<?> loadClass(String name) throws ClassNotFoundException {
          return loadClass(name, false);
      }
  
  初始化
          public LinkedList() {
      }
  
  添加元素
          public boolean add(E e) {
          linkLast(e);
          return true;
      }
      深入追
              void linkLast(E e) {
          final Node<E> l = last;//final修饰不能改变地址aa
          final Node<E> newNode = new Node<>(l, e, null);//也通过final定义了bb指aa
          last = newNode;//这个没有final修饰,新的给last，此时last为bb
          if (l == null)
              first = newNode;
          else
              l.next = newNode;
          size++;
          modCount++;
      }
          private static class Node<E> {
          E item;
          Node<E> next;
          Node<E> prev;
  
          Node(Node<E> prev, E element, Node<E> next) {
              this.item = element;
              this.next = next;
              this.prev = prev;
          }
      }
  
  ```

  

* Vector基本不用

* ArrayList使用数组结构，查找和添加的效率高，时间复杂度为o(1)，删除和插入操作效率低，复杂度为o(n)

* LinkedList插入和删除效率高，采用双向链表，为0(1)，查找和添加的效率低，为o(n)