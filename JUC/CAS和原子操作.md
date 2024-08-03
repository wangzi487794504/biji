#### CAS和原子操作

* CAS 的底层是 `lock cmpxchg` 指令（X86 架构），在单核 CPU 和多核 CPU 下都能够保证【比较-交换】的原子性。
  - 在多核状态下，某个核执行到带 lock 的指令时，CPU 会让总线锁住，当这个核把此指令执行完毕，再开启总线。这个过程中不会被线程的调度机制所打断，保证了多个线程对内存操作的准确性，是原子的。
* CAS 必须借助 volatile 才能读取到共享变量的最新值来实现【比较并交换】的效果
* 无锁情况下，即使重试失败，线程始终在高速运行，没有停歇，而 synchronized 会让线程在没有获得锁的时候，发生上下文切换，进入阻塞。

- - 打个比喻, 线程就好像高速跑道上的赛车，高速运行时，速度超快，一旦发生上下文切换，就好比赛车要减速、熄火,等被唤醒又得重新打火、启动、加速... 恢复到高速运行，代价比较大 
  - - 但无锁情况下，因为线程要保持运行，需要额外 CPU 的支持，CPU 在这里就好比高速跑道，没有额外的跑道，线程想高速运行也无从谈起，虽然不会进入阻塞，但由于没有分到时间片，仍然会进入可运行状态，还是会导致上下文切换。



* 结合 CAS 和 volatile 可以实现无锁并发，适用于线程数少、多核 CPU 的场景下。 

  - CAS 是基于乐观锁的思想：最乐观的估计，不怕别的线程来修改共享变量，就算改了也没关系，我吃亏点再重试呗。 
  - synchronized 是基于悲观锁的思想：最悲观的估计，得防着其它线程来修改共享变量，我上了锁你们都别想改，我改完了解开锁，你们才有机会。 
  - CAS 体现的是无锁并发、无阻塞并发，请仔细体会这两句话的意思 

  - - 因为没有使用 synchronized，所以线程不会陷入阻塞，这是效率提升的因素之一 
    - 但如果竞争激烈，可以想到重试必然频繁发生，反而效率会受影响

  - J.U.C 并发包提供了： 

    - AtomicBoolean 

    - AtomicInteger 

    - AtomicLong 

      ```java
      AtomicInteger i = new AtomicInteger(0);
      
      // 获取并自增（i = 0, 结果 i = 1, 返回 0），类似于 i++
      System.out.println(i.getAndIncrement());
      
      // 自增并获取（i = 1, 结果 i = 2, 返回 2），类似于 ++i
      System.out.println(i.incrementAndGet());
      
      // 自减并获取（i = 2, 结果 i = 1, 返回 1），类似于 --i
      System.out.println(i.decrementAndGet());
      
      // 获取并自减（i = 1, 结果 i = 0, 返回 1），类似于 i--
      System.out.println(i.getAndDecrement());
      
      // 获取并加值（i = 0, 结果 i = 5, 返回 0）
      System.out.println(i.getAndAdd(5));
      
      // 加值并获取（i = 5, 结果 i = 0, 返回 0）
      System.out.println(i.addAndGet(-5));
      
      // 获取并更新（i = 0, p 为 i 的当前值, 结果 i = -2, 返回 0）
      // 其中函数中的操作能保证原子，但函数需要无副作用
      System.out.println(i.getAndUpdate(p -> p - 2));
      
      // 更新并获取（i = -2, p 为 i 的当前值, 结果 i = 0, 返回 0）
      // 其中函数中的操作能保证原子，但函数需要无副作用
      System.out.println(i.updateAndGet(p -> p + 2));
      
      // 获取并计算（i = 0, p 为 i 的当前值, x 为参数1, 结果 i = 10, 返回 0）
      // 其中函数中的操作能保证原子，但函数需要无副作用
      // getAndUpdate 如果在 lambda 中引用了外部的局部变量，要保证该局部变量是 final 的
      // getAndAccumulate 可以通过 参数1 来引用外部的局部变量，但因为其不在 lambda 中因此不必是 final
      System.out.println(i.getAndAccumulate(10, (p, x) -> p + x));
      
      // 计算并获取（i = 10, p 为 i 的当前值, x 为参数1, 结果 i = 0, 返回 0）
      // 其中函数中的操作能保证原子，但函数需要无副作用
      System.out.println(i.accumulateAndGet(-10, (p, x) -> p + x));
      ```

* 为什么需要原子引用类型？     对引用类型也实现CAS功能

  - AtomicReference 

    ```java
    class DecimalAccountSafeCas implements DecimalAccount {
        AtomicReference<BigDecimal> ref;
        
        public DecimalAccountSafeCas(BigDecimal balance) {
            ref = new AtomicReference<>(balance);
        }
        
        @Override
        public BigDecimal getBalance() {
            return ref.get();
        }
        
        @Override
        public void withdraw(BigDecimal amount) {
            while (true) {
                BigDecimal prev = ref.get();
                BigDecimal next = prev.subtract(amount);
                if (ref.compareAndSet(prev, next)) {
                    break;
                }
            }
        }  
    }
    ```

    

  - AtomicMarkableReference **(使用布尔值判断有没有修改过，有时候，并不关心引用变量更改了几次，只是单纯的关心**是否更改过，解决不掉ABA问题，只关心有没有修改过**)**

  - AtomicStampedReference **(**主线程仅能判断出共享变量的值与最初值 A 是否相同，不能感知到这种从 A 改为 B 又 改回 A 的情况，如果主线程希望只要有其它线程【动过了】共享变量，那么自己的 cas 就算失败，这时，仅比较值是不够的，需要再加一个版本号 **)**

    ```java
    static AtomicStampedReference<String> ref = new AtomicStampedReference<>("A", 0);
    
    public static void main(String[] args) throws InterruptedException {
        log.debug("main start...");
        // 获取值 A
        String prev = ref.getReference();
        // 获取版本号
        int stamp = ref.getStamp();
        log.debug("版本 {}", stamp);
        // 如果中间有其它线程干扰，发生了 ABA 现象
        other();
        sleep(1);
        // 尝试改为 C
        log.debug("change A->C {}", ref.compareAndSet(prev, "C", stamp, stamp + 1));
    }
    
    private static void other() {
        new Thread(() -> {
            log.debug("change A->B {}", ref.compareAndSet(ref.getReference(), "B", 
                                                          ref.getStamp(), ref.getStamp() + 1));
            log.debug("更新版本为 {}", ref.getStamp());
        }, "t1").start();
        
        sleep(0.5);
        
        new Thread(() -> {
            log.debug("change B->A {}", ref.compareAndSet(ref.getReference(), "A", 
                                                          ref.getStamp(), ref.getStamp() + 1));
            log.debug("更新版本为 {}", ref.getStamp());
        }, "t2").start();
    }
    ```



* 原子数组
  * AtomicIntegerArray 
  * AtomicLongArray 
  * AtomicReferenceArray
  
* 字段原子更新器

  * AtomicReferenceFieldUpdater // 域字段 

  * AtomicIntegerFieldUpdater 

  * AtomicLongFieldUpdater 

  * 利用字段更新器，可以针对对象的某个域（Field）进行原子操作，只能配合 volatile 修饰的字段使用，否则会出现异常 Exception in thread "main" java.lang.IllegalArgumentException: Must be volatile type

    ```java
    public class Test5 {
        private volatile int field;
        
        public static void main(String[] args) {
            AtomicIntegerFieldUpdater fieldUpdater =AtomicIntegerFieldUpdater.newUpdater(Test5.class, "field");
            
            Test5 test5 = new Test5();
            fieldUpdater.compareAndSet(test5, 0, 10);
            // 修改成功 field = 10
            System.out.println(test5.field);
            // 修改成功 field = 20
            fieldUpdater.compareAndSet(test5, 10, 20);
            System.out.println(test5.field);
            // 修改失败 field = 20
            fieldUpdater.compareAndSet(test5, 10, 30);
            System.out.println(test5.field);
        }
    }
    ```

* 原子累加器LongAdder

  * 比较 AtomicLong 与 LongAdder

  * LongAdder 是并发大师  Doug Lea （大哥李）的作品，设计的非常精巧 。LongAdder 类有几个关键域

    ```java
    // 累加单元数组, 懒惰初始化
    transient volatile Cell[] cells;
    // 基础值, 如果没有竞争, 则用 cas 累加这个域
    transient volatile long base;
    // 在 cells 创建或扩容时, 置为 1, 表示加锁
    transient volatile int cellsBusy;
    
    ```

  * cellsBusy作为锁的实现机制

    ```java
    // 不要用于实践！！！
    public class LockCas {
        private AtomicInteger state = new AtomicInteger(0);
        public void lock() {
            while (true) {
                if (state.compareAndSet(0, 1)) {
                    break;
                }
            }
        }
        public void unlock() {
            log.debug("unlock...");
            state.set(0);
        }
    }
    ```

  * 使用，有点Lock锁的味道

    ```java
    // 不要用于实践！！！
    public class LockCas {
        private AtomicInteger state = new AtomicInteger(0);
        
        public void lock() {
            while (true) {
                if (state.compareAndSet(0, 1)) {
                    break;
                }
            }
        }
        
        public void unlock() {
            log.debug("unlock...");
            state.set(0);
        }
    }
    ```

  * cell为累加单元，需要防止缓存行为共享问题

    ```java
    // 防止缓存行伪共享  
    // 这个注解最重要
    @sun.misc.Contended
    static final class Cell {
        volatile long value;   
        Cell(long x) { 
            value = x; 
        }
        // 最重要的方法, 用来 cas 方式进行累加, prev 表示旧值, next 表示新值
        final boolean cas(long prev, long next) {
            return UNSAFE.compareAndSwapLong(this, valueOffset, prev, next);
        }
    // 省略不重要代码
    }
    ```

  * 关于缓存伪共享

    ![1722388415064](CAS%E5%92%8C%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C.assets/1722388415064.png)

    ![1722388453057](CAS%E5%92%8C%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C.assets/1722388453057.png)

  * 因为 CPU 与 内存的速度差异很大，需要靠预读数据至缓存来提升效率。

    ==而缓存以缓存行为单位，每个缓存行对应着一块内存，一般是 64 byte（8 个 long）== 

    ==缓存的加入会造成数据副本的产生，即同一份数据会缓存在不同核心的缓存行中==

    `CPU 要保证数据的一致性，如果某个 CPU 核心更改了数据，其它 CPU 核心对应的整个缓存行必须失效`

    ![1722388529747](CAS%E5%92%8C%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C.assets/1722388529747.png)

  * 因为 Cell 是数组形式，在内存中是连续存储的，一个 Cell 为 24 字节（16 字节的对象头和 8 字节的 value），因此缓存行可以存下 2 个的 Cell 对象。

  * 这样问题来了： 

    - Core-0 要修改 Cell[0] 
    - Core-1 要修改 Cell[1] 
    - 无论谁修改成功，都会导致对方 Core 的缓存行失效，比如 Core-0 中 `Cell[0]=6000, Cell[1]=8000` 要累加Cell[0]=6001, Cell[1]=8000 ，这时会让 Core-1 的缓存行失效 ; 
    - 同理 Core-1修改Cell[1]也会让 Core-0 的缓存行失效.

  * 解决方法

    * `@sun.misc.Contended` 用来解决这个问题，它的原理是在使用此注解的对象或字段的前后各增加 128 字节大小的padding，从而让 CPU 将对象预读至缓存时占用不同的缓存行，这样，不会造成对方缓存行的失效

      ![1722389394973](CAS%E5%92%8C%E5%8E%9F%E5%AD%90%E6%93%8D%E4%BD%9C.assets/1722389394973.png)













* UnSafe类

  * Unsafe对象提供了非常底层的，操作内存、程的方法，Unsafe对象不能直接调用，只能通过反射获得

    ```JAVA
    public class TwoSum {
        public static void main(String[] args) throws NoSuchFieldException, InstantiationException, IllegalAccessException {
            //这样会报Exception in thread "main" java.lang.SecurityException: Unsafe
            //Unsafe unsafe = Unsafe.getUnsafe();
            //方法一
            Field theUnsafe = Unsafe.class.getDeclaredField("theUnsafe");
            theUnsafe.setAccessible(true);
            Unsafe unsafe = (Unsafe) theUnsafe.get(null);
            // 1. 获取域的偏移地址
            long idOffset = unsafe.objectFieldOffset(Teacher.class.getDeclaredField("id"));
            long nameOffset = unsafe.objectFieldOffset(Teacher.class.getDeclaredField("name"));
            Teacher t = new Teacher();
            System.out.println(t);
            // 2. 执行 cas 操作
            unsafe.compareAndSwapInt(t, idOffset, 0, 1);
            unsafe.compareAndSwapObject(t, nameOffset, null, "张三");
            // 3. 验证
            System.out.println(t);
        }
    }
    @Data
    class Teacher {
        volatile int id;
        volatile String name;
    }
    ```

    