#### CopyOnSet

* `CopyOnWriteArraySet` 是它的马甲 底层实现采用了 `写入时拷贝` 的思想，增删改操作会将底层数组拷贝一份，更改操作在新数组上执行，这时不影响其它线程的**并发读**，**读写分离**。 以新增为例：

  ```java
  public boolean add(E e) {
      synchronized (lock) {
          // 获取旧的数组
          Object[] es = getArray();
          int len = es.length;
          // 拷贝新的数组（这里是比较耗时的操作，但不影响其它读线程）
          es = Arrays.copyOf(es, len + 1);
          // 添加新元素
          es[len] = e;
          // 替换旧的数组
          setArray(es);
          return true;
      }
  }
  ```

  * 这里的源码版本是 Java 11，在 Java 1.8 中使用的是可重入锁而不是 synchronized

  ```java
  public void forEach(Consumer<? super E> action) {
      Objects.requireNonNull(action);
      for (Object x : getArray()) {
          @SuppressWarnings("unchecked") E e = (E) x;
          action.accept(e);
      }
  }
  ```

* get弱一致性

   ![image.png](CopyOnSet.assets/image.png) 

* 不要觉得弱一致性就不好 
  - 数据库的 MVCC 都是弱一致性的表现 
  - 并发高和一致性是矛盾的，需要权衡