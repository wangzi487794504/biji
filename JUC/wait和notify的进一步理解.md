#### wait和notify的进一步理解

* Owner 线程发现条件不满足，调用 wait 方法，即可进入 WaitSet 变为 WAITING 状态 

* BLOCKED 和 WAITING 的线程都处于阻塞状态，不占用 CPU 时间片 

* BLOCKED 线程会在 Owner 线程释放锁时唤醒 

* WAITING 线程会在 Owner 线程调用 notify 或 notifyAll 时唤醒，但唤醒后并不意味者立刻获得锁，仍需进入EntryList 重新竞争

  ![1722257056780](wait%E5%92%8Cnotify%E7%9A%84%E8%BF%9B%E4%B8%80%E6%AD%A5%E7%90%86%E8%A7%A3.assets/1722257056780.png)

* obj.wait()让进入object 监视器的线程到waitSet等待
* obj.notify()在object 上正在waitSet 等待的线程中挑一个唤醒
* obj.notifyAl1()让object 上正在waitSet等待的线程全部唤醒



* sleep和wait的区别
  * 1) sleep 是 Thread 方法，而 wait 是 Object 的方法 
  * 2) sleep 不需要强制和 synchronized 配合使用，但 wait 需要和 synchronized 一起用 
  * 3) sleep 在睡眠的同时，不会释放对象锁的，但 wait 在等待的时候会释放对象锁 
  * 4) 它们状态 TIMED_WAITING
* 注意点
  * notify 只能随机唤醒一个 WaitSet 中的线程，这时如果有其它线程也在等待，那么就可能唤醒不了正确的线程，称之为【虚假唤醒】 
  * 发生虚假唤醒: 解决方法，改为 notifyAll
  * notify 只能随机唤醒一个 WaitSet 中的线程，这时如果有其它线程也在等待，那么就可能唤醒不了正确的线程，称之为【虚假唤醒】 
  * 发生虚假唤醒: 解决方法，改为 notifyAll







* 保护性暂停

  * 即 Guarded Suspension，用在一个线程等待另一个线程的执行结果 

    - ==有一个结果需要从一个线程传递到另一个线程，让他们关联同一个 GuardedObject==
    - 如果有结果不断从一个线程到另一个线程那么可以使用消息队列（见生产者/消费者） 
    - JDK 中，join 的实现、Future 的实现，采用的就是此模式 
    - 因为要等待另一方的结果，因此归类到同步模式 

  * 超时版本的Guarded Suspension

    ```java
    class GuardedObjectV2 {
        private Object response;
        private final Object lock = new Object();
        
        public Object get(long millis) {
            synchronized (lock) {
                // 1) 记录最初时间
                long begin = System.currentTimeMillis();
                // 2) 已经经历的时间
                long timePassed = 0;
                
                while (response == null) {
                    // 4) 假设 millis 是 1000，结果在 400 时唤醒了，那么还有 600 要等
                    long waitTime = millis - timePassed;
                    log.debug("waitTime: {}", waitTime);
                    
                    if (waitTime <= 0) {
                        log.debug("break...");
                        break; 
                    }
                    
                    try {
                        lock.wait(waitTime);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    
                    // 3) 如果提前被唤醒，这时已经经历的时间假设为 400
                    timePassed = System.currentTimeMillis() - begin;
                    
                    log.debug("timePassed: {}, object is null {}", 
                              timePassed, response == null);
                }
                return response; 
            }
        }
        public void complete(Object response) {
            synchronized (lock) {
                // 条件满足，通知等待线程
                this.response = response;
                log.debug("notify...");
                lock.notifyAll();
            }
        }
    }
    ```

    

  * join原理

    ```java
    public final synchronized void join(long millis)
        throws InterruptedException {
            long base = System.currentTimeMillis();
            long now = 0;
    
            if (millis < 0) {
                throw new IllegalArgumentException("timeout value is negative");
            }
    
            if (millis == 0) {
                while (isAlive()) {
                    wait(0);//一直等待
                }
            } else {
                while (isAlive()) {
                    long delay = millis - now;
                    if (delay <= 0) {
                        break;
                    }
                    wait(delay);
                    now = System.currentTimeMillis() - base;
                }
            }
        }
    ```

    





* **多任务版** **GuardedObject** 

  * 图中 Futures 就好比居民楼一层的信箱（每个信箱有房间编号），左侧的 t0，t2，t4 就好比等待邮件的居民，右 侧的 t1，t3，t5 就好比邮递员 

    * 如果需要在多个类之间使用 GuardedObject 对象，作为参数传递不是很方便，因此设计一个用来解耦的中间类， 这样不仅能够解耦【结果等待者】和【结果生产者】，还能够同时支持多个任务的管理

      ![1722268379798](wait%E5%92%8Cnotify%E7%9A%84%E8%BF%9B%E4%B8%80%E6%AD%A5%E7%90%86%E8%A7%A3.assets/1722268379798.png)





* park和unpark方法

  * 它们是 LockSupport 类中的方法，调用到最后也是unsafe的native方法

    ```java
    // 暂停当前线程
    LockSupport.park(); 
    // 恢复某个线程的运行
    LockSupport.unpark(暂停线程对象)
    ```

  * 先park再unpark

    ```java
    Thread t1 = new Thread(() -> {
        log.debug("start...");
        sleep(1);
        log.debug("park...");
        LockSupport.park();
        log.debug("resume...");
    },"t1");
    t1.start();
    
    sleep(2);
    log.debug("unpark...");
    LockSupport.unpark(t1);
    18:42:52.585 c.TestParkUnpark [t1] - start... 
    18:42:53.589 c.TestParkUnpark [t1] - park... 
    18:42:54.583 c.TestParkUnpark [main] - unpark... 
    18:42:54.583 c.TestParkUnpark [t1] - resume...
    ```

  * 先unpark再park

    ```java
    Thread t1 = new Thread(() -> {
        log.debug("start...");
        sleep(2);
        log.debug("park...");
        LockSupport.park();
        log.debug("resume...");
    }, "t1");
    t1.start();
    
    sleep(1);
    log.debug("unpark...");
    LockSupport.unpark(t1);
    18:43:50.765 c.TestParkUnpark [t1] - start... 
    18:43:51.764 c.TestParkUnpark [main] - unpark... 
    18:43:52.769 c.TestParkUnpark [t1] - park... 
    18:43:52.769 c.TestParkUnpark [t1] - resume...
    ```

  * **与 Object 的 wait & notify 相比 **

    - ==wait，notify 和 notifyAll 必须配合 Object Monitor 一起使用，而 park，unpark 不必==
    - park & unpark 是以线程为单位来【阻塞】和【唤醒(指定)】线程，而 notify 只能随机唤醒一个等待线程，notifyAll是唤醒所有等待线程，就不那么【精确】 
    - park & unpark 可以先 unpark，而 wait & notify 不能先 notify 

  * 原理

    * 每个线程都有自己的一个(C代码实现的) Parker 对象，由三部分组成 `_counter` ， `_cond`(condition条件变量)  和 `_mutex` (互斥锁)。

    * 打个比喻 

      - 线程就像一个旅人，Parker 就像他随身携带的背包，条件变量就好比背包中的帐篷。`_counter` 就好比背包中的备用干粮（0 为耗尽，1 为充足） 
      - 调用 park 就是要看需不需要停下来歇息 

      - - 如果备用干粮耗尽(_counter为0)，那么钻进帐篷歇息(等待补充干粮,否则容易半路饿死)
        - 如果备用干粮充足(_counter为1)，那么不需停留，继续前进(兜里有粮,心里不慌) 

      - 调用 unpark，就好比令干粮充足(使 _counter为1) 

      - - 如果这时线程还在帐篷，就唤醒让他继续前进 
        - 如果这时线程还在运行，那么下次他调用 park 时，仅是消耗掉备用干粮，不需停留,继续前进 

      - - - 因为背包空间有限，多次调用 unpark 仅会补充一份备用干粮,也就是**多次unpark后只会让紧跟着的一次park失效**

    * 先park再unpark原理

      <img src="wait%E5%92%8Cnotify%E7%9A%84%E8%BF%9B%E4%B8%80%E6%AD%A5%E7%90%86%E8%A7%A3.assets/1722301490596.png" alt="1722301490596" style="zoom:67%;" />

      * 当前线程调用 Unsafe.park() 方法 
      * 检查 _counter ，本情况为 0，这时，获得 _mutex 互斥锁 
      *  线程进入 _cond 条件变量阻塞 
      *  设置 _counter = 0

      <img src="wait%E5%92%8Cnotify%E7%9A%84%E8%BF%9B%E4%B8%80%E6%AD%A5%E7%90%86%E8%A7%A3.assets/1722301545495.png" alt="1722301545495" style="zoom:67%;" />

      * 调用 Unsafe.unpark(Thread_0) 方法，设置 _counter 为 1 
      *  唤醒 _cond 条件变量中的 Thread_0 
      * Thread_0 恢复运行 
      * 设置 _counter 为 0

    * 先unpark再park

      <img src="wait%E5%92%8Cnotify%E7%9A%84%E8%BF%9B%E4%B8%80%E6%AD%A5%E7%90%86%E8%A7%A3.assets/1722301841581.png" alt="1722301841581" style="zoom:67%;" />

      * 调用 Unsafe.unpark(Thread_0) 方法，设置 _counter 为 1 
      * 当前线程调用 Unsafe.park() 方法 
      * 检查 _counter ，本情况为 1，这时线程无需阻塞，继续运行 
      * 设置 _counter 为 0 

* 定位死锁

  * 先用jps查看所有的进程ID
  * 再用jstack查看该ID的所有线程
  * Jconsole也可以查看