#### ArrayList

* 线程不安全，object[]数组,实现List接口

* 对于jdk7

  ```java
  ArrayList<String> list=new ArrayList<String>;
  //底层是初始化数组Object[] elementData=new Object[10];长度为10
  
  list.add("aa");
  //elementData[0]="aa"
  list.add("bb");
  ....
   //当要添加到底十一个元素的时候，底层的elementData数组已满，则需要扩容，默认扩容为原来长度的1.5倍，并将原有数组复制到新的数组中。
  ```

  

* jdk1.8

  ```java
  //底层的初始化Object[] elementData=new Object[]{}
  
  //首次添加元素时会重新初始化
  //其余没有区别
      
   //追源码
   public ArrayList() {
       this.elementData = DEFAULTCAPACITY_EMPTY_ELEMENTDATA;
   }
   private static final Object[] DEFAULTCAPACITY_EMPTY_ELEMENTDATA = {};
  
    public boolean add(E e) {
          ensureCapacityInternal(size + 1);  // Increments modCount!!
          elementData[size++] = e;
          return true;
      }
  
     private void ensureExplicitCapacity(int minCapacity) {
          modCount++;
  
          // overflow-conscious code
          if (minCapacity - elementData.length > 0)
              grow(minCapacity);
      }
      private void grow(int minCapacity) {
          // overflow-conscious code
        int oldCapacity = elementData.length;
          int newCapacity = oldCapacity + (oldCapacity >> 1);
          if (newCapacity - minCapacity < 0)
              newCapacity = minCapacity;
          if (newCapacity - MAX_ARRAY_SIZE > 0)
              newCapacity = hugeCapacity(minCapacity);
          // minCapacity is usually close to size, so this is a win:
          elementData = Arrays.copyOf(elementData, newCapacity);
      }
  
  ```
  
  * 原容量+原容量/2
  * `ArrayList` 继承于 `AbstractList` ，实现了 `List`, `RandomAccess`, `Cloneable`, `java.io.Serializable` 这些接口。
  * `ArrayList` 中可以存储任何类型的对象，包括 `null` 值。不过，不建议向`ArrayList` 中添加 `null` 值， `null` 值无意义，会让代码难以维护比如忘记做判空处理就会导致空指针异常。





* 他的subList方法，是通过内部类SubList实现的

  ```java
          public List<E> subList(int fromIndex, int toIndex) {
              subListRangeCheck(fromIndex, toIndex, size);
              return new SubList(this, offset, fromIndex, toIndex);
          }
  ```

  * 点进去这个内部类，我们可以发现有set方法，他是在原ArrayList的基础上直接操作的。

    ```java
        private class SubList extends AbstractList<E> implements RandomAccess {
            private final AbstractList<E> parent;
            private final int parentOffset;
            private final int offset;
            int size;
    
            SubList(AbstractList<E> parent,
                    int offset, int fromIndex, int toIndex) {
                this.parent = parent;
                this.parentOffset = fromIndex;
                this.offset = offset + fromIndex;
                this.size = toIndex - fromIndex;
                this.modCount = ArrayList.this.modCount;
            }
    
            public E set(int index, E e) {
                rangeCheck(index);
                checkForComodification();
                E oldValue = ArrayList.this.elementData(offset + index);
                ArrayList.this.elementData[offset + index] = e;
                return oldValue;
            }
    ```

  * 所以子列表进行增删改查时就会影响源列表

  * 反过来源列表发生更改也会影响子列表，对于非结构改变（重新设置原有位置上的值）使用子列表不会报错，结构改变（**如增加和删除**）会报`ConcurrentModificationException` 异常

* ArrayList的源码默认是10

* trimToSize方法对 `ArrayList` 对象的容量进行调整，让它的容量和实际存储的元素数量相匹配。

* 移除元素的remove是可以传Null的

  ```java
      public boolean remove(Object o) {
          if (o == null) {
              for (int index = 0; index < size; index++)
                  if (elementData[index] == null) {
                      fastRemove(index);
                      return true;
                  }
          } else {
              for (int index = 0; index < size; index++)
                  if (o.equals(elementData[index])) {
                      fastRemove(index);
                      return true;
                  }
          }
          return false;
      }
  ```

* 他的扩容调用了System.arraycopy方法，Arrays.copy本质也是调用这个方法。

  * 不同点：`arraycopy()` 需要目标数组，将原数组拷贝到你自己定义的数组里或者原数组，而且可以选择拷贝的起点和长度以及放入新数组中的位置 `copyOf()` 是系统自动在内部新建一个数组，并返回该数组

* 此外，它实现了RandomAccess接口，`RandomAccess` 是一个标记接口，用来表明实现该接口的类支持随机访问（即可以通过索引快速访问元素）。