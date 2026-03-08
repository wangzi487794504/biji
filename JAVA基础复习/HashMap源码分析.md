#### HashMap源码

* HashMap 中有四个构造方法，它们分别如下：

  ```java
      // 默认构造函数。
      public HashMap() {
          this.loadFactor = DEFAULT_LOAD_FACTOR; // all   other fields defaulted
       }
  
       // 包含另一个“Map”的构造函数
       public HashMap(Map<? extends K, ? extends V> m) {
           this.loadFactor = DEFAULT_LOAD_FACTOR;
           putMapEntries(m, false);//下面会分析到这个方法
       }
  
       // 指定“容量大小”的构造函数
       public HashMap(int initialCapacity) {
           this(initialCapacity, DEFAULT_LOAD_FACTOR);
       }
  
       // 指定“容量大小”和“负载因子”的构造函数
       public HashMap(int initialCapacity, float loadFactor) {
           if (initialCapacity < 0)
               throw new IllegalArgumentException("Illegal initial capacity: " + initialCapacity);
           if (initialCapacity > MAXIMUM_CAPACITY)
               initialCapacity = MAXIMUM_CAPACITY;
           if (loadFactor <= 0 || Float.isNaN(loadFactor))
               throw new IllegalArgumentException("Illegal load factor: " + loadFactor);
           this.loadFactor = loadFactor;
           // 初始容量暂时存放到 threshold ，在resize中再赋值给 newCap 进行table初始化
           this.threshold = tableSizeFor(initialCapacity);
       }
  ```

* 内部实现了Entry接口

  ```java
  // 继承自 Map.Entry<K,V>
  static class Node<K,V> implements Map.Entry<K,V> {
         final int hash;// 哈希值，存放元素到hashmap中时用来与其他元素hash值比较
         final K key;//键
         V value;//值
         // 指向下一个节点
         Node<K,V> next;
         Node(int hash, K key, V value, Node<K,V> next) {
              this.hash = hash;
              this.key = key;
              this.value = value;
              this.next = next;
          }
          public final K getKey()        { return key; }
          public final V getValue()      { return value; }
          public final String toString() { return key + "=" + value; }
          // 重写hashCode()方法
          public final int hashCode() {
              return Objects.hashCode(key) ^ Objects.hashCode(value);
          }
  
          public final V setValue(V newValue) {
              V oldValue = value;
              value = newValue;
              return oldValue;
          }
          // 重写 equals() 方法
          public final boolean equals(Object o) {
              if (o == this)
                  return true;
              if (o instanceof Map.Entry) {
                  Map.Entry<?,?> e = (Map.Entry<?,?>)o;
                  if (Objects.equals(key, e.getKey()) &&
                      Objects.equals(value, e.getValue()))
                      return true;
              }
              return false;
          }
  }
  ```

* put方法

  ```java
  public V put(K key, V value) {
      return putVal(hash(key), key, value, false, true);
  }
  
  final V putVal(int hash, K key, V value, boolean onlyIfAbsent,
                     boolean evict) {
      Node<K,V>[] tab; Node<K,V> p; int n, i;
      // table未初始化或者长度为0，进行扩容
      if ((tab = table) == null || (n = tab.length) == 0)
          n = (tab = resize()).length;
      // (n - 1) & hash 确定元素存放在哪个桶中，桶为空，新生成结点放入桶中(此时，这个结点是放在数组中)
      if ((p = tab[i = (n - 1) & hash]) == null)
          tab[i] = newNode(hash, key, value, null);
      // 桶中已经存在元素（处理hash冲突）
      else {
          Node<K,V> e; K k;
          //快速判断第一个节点table[i]的key是否与插入的key一样，若相同就直接使用插入的值p替换掉旧的值e。
          if (p.hash == hash &&
              ((k = p.key) == key || (key != null && key.equals(k))))
                  e = p;
          // 判断插入的是否是红黑树节点
          else if (p instanceof TreeNode)
              // 放入树中
              e = ((TreeNode<K,V>)p).putTreeVal(this, tab, hash, key, value);
          // 不是红黑树节点则说明为链表结点
          else {
              // 在链表最末插入结点
              for (int binCount = 0; ; ++binCount) {
                  // 到达链表的尾部
                  if ((e = p.next) == null) {
                      // 在尾部插入新结点
                      p.next = newNode(hash, key, value, null);
                      // 结点数量达到阈值(默认为 8 )，执行 treeifyBin 方法
                      // 这个方法会根据 HashMap 数组来决定是否转换为红黑树。
                      // 只有当数组长度大于或者等于 64 的情况下，才会执行转换红黑树操作，以减少搜索时间。否则，就是只是对数组扩容。
                      if (binCount >= TREEIFY_THRESHOLD - 1) // -1 for 1st
                          treeifyBin(tab, hash);
                      // 跳出循环
                      break;
                  }
                  // 判断链表中结点的key值与插入的元素的key值是否相等
                  if (e.hash == hash &&
                      ((k = e.key) == key || (key != null && key.equals(k))))
                      // 相等，跳出循环
                      break;
                  // 用于遍历桶中的链表，与前面的e = p.next组合，可以遍历链表
                  p = e;
              }
          }
          // 表示在桶中找到key值、hash值与插入元素相等的结点
          if (e != null) {
              // 记录e的value
              V oldValue = e.value;
              // onlyIfAbsent为false或者旧值为null
              if (!onlyIfAbsent || oldValue == null)
                  //用新值替换旧值
                  e.value = value;
              // 访问后回调
              afterNodeAccess(e);
              // 返回旧值
              return oldValue;
          }
      }
      // 结构性修改
      ++modCount;
      // 实际大小大于阈值则扩容
      if (++size > threshold)
          resize();
      // 插入后回调
      afterNodeInsertion(evict);
      return null;
  }
  ```

  

#### LinkedHashedMap

* `LinkedHashMap` 是 Java 提供的一个集合类，它继承自 `HashMap`，并在 `HashMap` 基础上维护一条双向链表，使得具备如下特性:

  * 支持遍历时会按照插入顺序有序进行迭代。

  * 支持按照元素访问顺序排序,适用于封装 LRU 缓存工具。

  * 因为内部使用双向链表维护各个节点，所以遍历时的效率和元素个数成正比，相较于和容量成正比的 HashMap 来说，迭代效率会高很多。

    ```java]
    public class LinkedHashMap<K,V>
        extends HashMap<K,V>
        implements Map<K,V>
    {
    ```

    

* `LinkedHashMap` 逻辑结构如下图所示，它是在 `HashMap` 基础上在各个节点之间维护一条双向链表，使得原本散列在不同 bucket 上的节点、链表、红黑树有序关联起来。

  <img src="./assets/linkhashmap-structure-overview.png" alt="LinkedHashMap 逻辑结构" style="zoom:50%;" />

* 插入顺序遍历和访问顺序遍历

  * `LinkedHashMap` 的迭代顺序是和插入顺序一致的,这一点是 `HashMap` 所不具备的

  * 如果想实现LRU，可以使用LinkedHashMap的构造方法将accessOrder设为true

    ```java
        public LinkedHashMap(int initialCapacity,
                             float loadFactor,
                             boolean accessOrder) {
            super(initialCapacity, loadFactor);
            this.accessOrder = accessOrder;
        }
    ```

    * 实现LRU

      * 重写`removeEldestEntry` 方法，该方法会返回一个 boolean 值，告知 `LinkedHashMap` 是否需要移除链表首元素（缓存容量有限）。

      ```java
      public class LRUCache<K, V> extends LinkedHashMap<K, V> {
          private final int capacity;
      
          public LRUCache(int capacity) {
              super(capacity, 0.75f, true);
              this.capacity = capacity;
          }
      
          /**
           * 判断size超过容量时返回true，告知LinkedHashMap移除最老的缓存项(即链表的第一个元素)
           */
          @Override
          protected boolean removeEldestEntry(Map.Entry<K, V> eldest) {
              return size() > capacity;
          }
      }
      ```

* LinkedHashMap 是在 HashMap 的基础上为 bucket 上的每一个节点建立一条双向链表，这就使得转为红黑树的树节点也需要具备双向链表节点的特性，即每一个树节点都需要拥有两个引用存储前驱节点和后继节点的地址,所以对于树节点类 TreeNode 的设计就是一个比较棘手的问题。

  * `LinkedHashMap` 的节点内部类 `Entry` 基于 `HashMap` 的基础上，增加 `before` 和 `after` 指针使节点具备双向链表的特性。
  * `HashMap` 的树节点 `TreeNode` 继承了具备双向链表特性的 `LinkedHashMap` 的 `Entry`。

* get方法

  ```java
  public V get(Object key) {
       Node < K, V > e;
       //获取key的键值对,若为空直接返回
       if ((e = getNode(hash(key), key)) == null)
           return null;
       //若accessOrder为true，则调用afterNodeAccess将当前元素移到链表末尾
       if (accessOrder)
           afterNodeAccess(e);
       //返回键值对的值
       return e.value;
   }
  ```

* 总结：

* `LinkedHashMap` 是 Java 集合框架中 `HashMap` 的一个子类，它继承了 `HashMap` 的所有属性和方法，并且在 `HashMap` 的基础重写了 `afterNodeRemoval`、`afterNodeInsertion`、`afterNodeAccess` 方法。使之拥有顺序插入和访问有序的特性。