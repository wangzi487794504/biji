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