#### 有序性

* volatile 修饰的变量，可以禁用指令重排

* **volatile 的底层实现原理是**内存屏障，Memory Barrier（Memory Fence）** 

  - **对 volatile 变量的 写指令后会加入写屏障 :** 保证在该屏障之前的，对共享变量的改动，都同步到主存当中

    ```java
    public void actor2(I_Result r) {
        num = 2;
        ready = true; // ready 是 volatile 赋值带写屏障
        // 写屏障
    }
    ```

    

  - **对 volatile 变量的 读指令前会加入读屏障 :** 在该屏障之后，对共享变量的读取，加载的是主存中最新数据

    ```java
    public void actor1(I_Result r) {
        // 读屏障
        // ready 是 volatile 读取值带读屏障
        if(ready) {
            r.r1 = num + num;
        } else {
            r.r1 = 1;
        }
    }
    ```

  - ==写屏障会确保指令重排序时，不会将写屏障之前的代码排在写屏障之后==

  - ==读屏障会确保指令重排序时，不会将读屏障之后的代码排在读屏障之前==

* volatile 只能保证可见性和有序性

  * 写屏障仅仅是保证之后的读能够读到最新的结果，但不能保证读跑到它前面去 
  * 而有序性的保证也只是保证了本线程内相关代码不被重排序



* 单例模式出现的问题

  ```java
  public final class Singleton {
      private Singleton() { }
      private static Singleton INSTANCE = null;
      
      public static Singleton getInstance() { 
          if(INSTANCE == null) { // t2
              // 首次访问会同步，而之后的使用没有 synchronized
              synchronized(Singleton.class) {
                  if (INSTANCE == null) { // t1
                      INSTANCE = new Singleton(); 
                  } 
              }
          }
          return INSTANCE;
      }
  }
  ```

  * 以上的实现特点是： 

    - 懒惰实例化 
    - 首次使用 getInstance() 才使用 synchronized 加锁，后续使用时无需加锁
    - 有隐含的，但很关键的一点：第一个 if 使用了 INSTANCE 变量，是在同步块之外

  * 但是由于第一个if没有被锁，会出现指令重排的问题

    * ==最大的问题是new的过程不是一个指令，他有可能先赋值后初始化，在赋值后，其他的线程执行了第一个if语句，结果不为Null==

    * 就是要保证最后一步会被赋值

      ```java
      public final class Singleton {
          private Singleton() { }
          private static volatile Singleton INSTANCE = null;
          
          public static Singleton getInstance() {
              // 实例没创建，才会进入内部的 synchronized代码块
              if (INSTANCE == null) { 
                  synchronized (Singleton.class) { // t2
                      // 也许有其它线程已经创建实例，所以再判断一次
                      if (INSTANCE == null) { // t1
                          INSTANCE = new Singleton();
                      }
                  }
              }
              return INSTANCE;
          }
      }
      ```

      

  * ==synchronized是可以保证有序，前提是你必须全部把这个变量交给synchronized管理==



* happens-before 

  * happens-before 规定了对共享变量的写操作对其它线程的读操作可见，它是可见性与有序性的一套规则总结，抛开以下 happens-before 规则，JMM 并不能保证一个线程对共享变量的写，对于其它线程对该共享变量的读可见 

  * 情况1.线程解锁 m 之前对变量的写，对于接下来对 m 加锁的其它线程对该变量的读可见

    ```java
    static int x;
    static Object m = new Object();
    
    new Thread(()->{
        synchronized(m) {
            x = 10;
        }
    },"t1").start();
    
    new Thread(()->{
        synchronized(m) {
            System.out.println(x);
        }
    },"t2").start();
    ```

  * 情况2.线程对 volatile 变量的写，对接下来其它线程对该变量的读可见

    ```java
    volatile static int x;
    
    new Thread(()->{
        x = 10;
    },"t1").start();
    
    new Thread(()->{
        System.out.println(x);
    },"t2").start();
    ```

  * 情况3.线程 start 前对变量的写，对该线程开始后对该变量的读可见

    ```java
    static int x; 
    x = 10;
    
    new Thread(()->{
        System.out.println(x);
    },"t2").start();
    ```

  * 情况4.线程结束前对变量的写，对其它线程得知它结束后的读可见（比如其它线程调用 t1.isAlive() 或 t1.join()等待它结束）

    ```java
    static int x;
    
    Thread t1 = new Thread(()->{
        x = 10;
    },"t1");
    t1.start();
    
    t1.join();
    System.out.println(x);
    ```

  * 情况5.线程 t1 打断 t2（interrupt）前对变量的写，对于其他线程得知 t2 被打断后对变量的读可见（通过t2.interrupted 或 t2.isInterrupted）

    ```java
    static int x;
    
    public static void main(String[] args) {
        Thread t2 = new Thread(()->{
            while(true) {
                if(Thread.currentThread().isInterrupted()) {
                    System.out.println(x);
                    break;
                }
            }
        },"t2");
        t2.start();
        
        new Thread(()->{
            sleep(1);
            x = 10;
            t2.interrupt();
        },"t1").start();
        
        while(!t2.isInterrupted()) {
            Thread.yield();
        }
        System.out.println(x);
    }
    ```

  * 情况6: 对变量默认值（0，false，null）的写，对其它线程对该变量的读可见 

  * 情况7: 具有传递性，如果 `x hb-> y` 并且 `y hb-> z` 那么有 `x hb-> z` ，配合 volatile 的防指令重排，有下面的例子

    ```java
    volatile static int x;
    static int y;
    
    new Thread(()->{ 
        y = 10;
        x = 20;
    },"t1").start();
    
    new Thread(()->{
        // x=20 对 t2 可见, 同时 y=10 也对 t2 可见
        System.out.println(x); 
    },"t2").start();
    ```

    变量都是指成员变量或静态成员变量 