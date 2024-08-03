#### ReentrantLock 

* 相对于 synchronized 它具备如下特点 

  - 可中断 
  - 可以设置超时时间 
  - 可以设置为公平锁 
  - 支持多个条件变量 

  * 与 synchronized 一样，都支持可重入

    ```java
    // 获取锁
    reentrantLock.lock();
    try {
        // 临界区
    } finally {
        // 释放锁
        reentrantLock.unlock();
    }
    ```

    

* 可重入

  * 可重入是指同一个线程如果首次获得了这把锁，那么因为它是这把锁的拥有者，因此有权利再次获取这把锁 
  * 如果是不可重入锁，那么第二次获得锁时，自己也会被锁挡住

* 可打断  lock.lockInterruptibly()

  ```JAVA
  ReentrantLock lock = new ReentrantLock();
  
  Thread t1 = new Thread(() -> {
      log.debug("启动...");
      
      try {
          //没有竞争就会获取锁
          //有竞争就进入阻塞队列等待,但可以被打断
          lock.lockInterruptibly();
          //lock.lock(); //不可打断
      } catch (InterruptedException e) {
          e.printStackTrace();
          log.debug("等锁的过程中被打断");
          return;
      }
      
      try {
          log.debug("获得了锁");
      } finally {
          lock.unlock();
      }
  }, "t1");
  
  lock.lock();
  log.debug("获得了锁");
  t1.start();
  
  try {
      sleep(1);
      log.debug("执行打断");
      t1.interrupt();
  } finally {
      lock.unlock();
  }
  ```

  

* 可打断是被动的，可以使用锁超时

  * 立刻返回结果 lock.tryLock()
  * 尝试一定时间获取结果lock.tryLock(1, TimeUnit.SECONDS)

  ```java
  ReentrantLock lock = new ReentrantLock();
  
  Thread t1 = new Thread(() -> {
      log.debug("启动...");
      
      try {
          if (!lock.tryLock(1, TimeUnit.SECONDS)) {
              log.debug("获取等待 1s 后失败，返回");
              return;
          }
      } catch (InterruptedException e) {
          e.printStackTrace();
      }
      try {
          log.debug("获得了锁");
      } finally {
          lock.unlock();
      }
  }, "t1");
  
  lock.lock();
  log.debug("获得了锁");
  t1.start();
  
  try {
      sleep(2);
  } finally {
      lock.unlock();
  }
  ```

  







* 哲学家就餐问题

  ```java\
  class Philosopher extends Thread {
      
      Chopstick left;
      Chopstick right;
      
      public Philosopher(String name, Chopstick left, Chopstick right) {
          super(name);
          this.left = left;
          this.right = right;
      }
      
      @Override
      public void run() {
          while (true) {
              // 尝试获得左手筷子
              if (left.tryLock()) {
                  try {
                      // 尝试获得右手筷子
                      if (right.tryLock()) {
                          try {
                              eat();
                          } finally {
                              right.unlock();
                          }
                      }
                  } finally {
                      left.unlock();
                  }
              }
          }
      }
      
      private void eat() {
          log.debug("eating...");
          Sleeper.sleep(1);
      }
      
  }
  ```

  



* 公平锁
  * 公平: 先来就能先执行
  * 不公平: 不保证先来就先执行
  * 公平锁一般没有必要，会降低并发度



* 条件变量

  * synchronized 中也有条件变量，就是我们讲原理时那个 waitSet 休息室，当条件不满足时进入 waitSet 等待 

  * ReentrantLock 的条件变量比 synchronized 强大之处在于，它是支持多个条件变量的，这就好比 

    - synchronized 是那些不满足条件的线程都在一间休息室等消息 
    - 而 ReentrantLock 支持多间休息室，有专门等烟的休息室、专门等早餐的休息室、唤醒时也是按休息室来唤醒 

  * 使用要点

    * await 前需要获得锁 
    * await 执行后，会释放锁，进入 conditionObject 等待 
    * await 的线程被唤醒（或打断、或超时）去重新竞争 lock 锁 
    * 竞争 lock 锁成功后，从 await 后继续执行 

  * 模版

    ```java
            ReentrantLock lock=new ReentrantLock();
            //创建一个条件变量
            Condition condition=lock.newCondition();
            //进入休息室等待
            condition.await();
    ```

  * 案例

    ```java
    static ReentrantLock lock = new ReentrantLock();
    
    static Condition waitCigaretteQueue = lock.newCondition();
    static Condition waitbreakfastQueue = lock.newCondition();
    
    static volatile boolean hasCigrette = false;
    static volatile boolean hasBreakfast = false;
    
    public static void main(String[] args) {
        
        new Thread(() -> {
            try {
                lock.lock();
                while (!hasCigrette) {
                    try {
                        waitCigaretteQueue.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("等到了它的烟");
            } finally {
                lock.unlock();
            }
        }).start();
        
        new Thread(() -> {
            try {
                lock.lock();
                while (!hasBreakfast) {
                    try {
                        waitbreakfastQueue.await();
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                }
                log.debug("等到了它的早餐");
            } finally {
                lock.unlock();
            }
        }).start();
        
        sleep(1);
        sendBreakfast();
        sleep(1);
        sendCigarette();
    }
    
    private static void sendCigarette() {
        lock.lock();
        try {
            log.debug("送烟来了");
            hasCigrette = true;
            waitCigaretteQueue.signal();
        } finally {
            lock.unlock();
        }
    }
    
    private static void sendBreakfast() {
        lock.lock();
        try {
            log.debug("送早餐来了");
            hasBreakfast = true;
            waitbreakfastQueue.signal();
        } finally {
            lock.unlock();
        }
    }
    ```

    





* ReentrantLock原理

  * 没有发生竞争时，占有锁

  * 第一个竞争出现时，发生排队

    <img src="ReentrantLock%20.assets/1722498116585.png" alt="1722498116585" style="zoom:67%;" />

    ```java
        public final void acquire(int arg) {
            if (!tryAcquire(arg) &&
                // 当 tryAcquire 返回为 false 时, 先调用 addWaiter, 接着 acquireQueued
                acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
                selfInterrupt();
        }
    ```

    ```java
        private Node addWaiter(Node mode) {
            Node node = new Node(Thread.currentThread(), mode);
            // Try the fast path of enq; backup to full enq on failure
            //将当前线程关联到一个 Node 对象上, 模式为独占模式
            Node pred = tail;
            //// 如果 tail 不为 null, cas 尝试将 Node 对象加入 AQS 队列尾部
            if (pred != null) {
                //双向链表
                node.prev = pred;
                if (compareAndSetTail(pred, node)) {
                    pred.next = node;
                    return node;
                }
            }
            // 尝试将 Node 加入 AQS
            enq(node);
            return node;
        }
    ```

    ```java
        private Node enq(final Node node) {
            for (;;) {
                Node t = tail;
                if (t == null) {
                    // 还没有, 设置 head 为哨兵节点（不对应线程，状态为 0）
                    if (compareAndSetHead(new Node())) {
                        tail = head;
                    }
                } else {
                    // cas 尝试将 Node 对象加入 AQS 队列尾部
                    node.prev = t;
                    if (compareAndSetTail(t, node)) {
                        t.next = node;
                        return t;
                    }
                }
            }
        }
    ```

    

    * Thread-1 执行了 

      1. CAS 尝试将 state 由 0 改为 1，结果失败 

      2. 进入 tryAcquire 逻辑，这时 state 已经是1，结果仍然失败 

      3. 接下来进入 addWaiter 逻辑，构造 Node 队列 

      - - 图中黄色三角表示该 Node 的 waitStatus 状态，其中 0 为默认正常状态 
        - Node 的创建是懒惰的 
        - 其中第一个 Node 称为 Dummy（哑元）或哨兵，用来占位，并不关联线程

      ```java
              final boolean nonfairTryAcquire(int acquires) {
                  //获取当前线程
                  final Thread current = Thread.currentThread();
                  //得到state数目
                  int c = getState();
                  //如果c==0，进入然后占领
                  if (c == 0) {
                      //这里体现了非公平性，没有问队列
                      if (compareAndSetState(0, acquires)) {
                          setExclusiveOwnerThread(current);
                          return true;
                      }
                  }
                  //如果不为零，判断该线程是不是主人线程，是就进去，锁重入
                  else if (current == getExclusiveOwnerThread()) {
                      int nextc = c + acquires;
                      if (nextc < 0) // overflow
                          throw new Error("Maximum lock count exceeded");
                      setState(nextc);
                      return true;
                  }
                  return false;
              }
      ```

      ![1722498921044](ReentrantLock%20.assets/1722498921044.png)

  * 当前线程进入 acquireQueued 逻辑 

    1. acquireQueued 会在一个死循环中不断尝试获得锁，失败后进入 park 阻塞 

    2. 如果自己是紧邻着 head（排第二位），那么再次 tryAcquire 尝试获取锁，当然这时 state 仍为 1，失败 

    3. 进入 shouldParkAfterFailedAcquire 逻辑，将前驱 node，即 head 的 waitStatus 改为 -1，这次返回 false

       ![img](ReentrantLock%20.assets/image.png)

       ```java
       final boolean acquireQueued(final Node node, int arg) {
               boolean failed = true;
               try {
                   boolean interrupted = false;
                   //在一个死循环不断尝试
                   for (;;) {
                       //获得前一个节点
                       final Node p = node.predecessor();
                       //前一个节点是头结点，尝试再去获取锁
                       if (p == head && tryAcquire(arg)) {
                           //轮到自己了，把自己设置为头结点
                           setHead(node);
                           p.next = null; // help GC
                           failed = false;
                           return interrupted;
                       }
                       if (shouldParkAfterFailedAcquire(p, node) &&
                           parkAndCheckInterrupt())
                           interrupted = true;
                   }
               } finally {
                   if (failed)
                       cancelAcquire(node);
               }
           }
       ```

       ```java
           private static boolean shouldParkAfterFailedAcquire(Node pred, Node node) {
               //获取上一个节点的状态
               int ws = pred.waitStatus;
               //如果上一个线程都在阻塞，那就直接阻塞
               if (ws == Node.SIGNAL)
                   return true;
               if (ws > 0) {
                   do {
                       node.prev = pred = pred.prev;
                   } while (pred.waitStatus > 0);
                   pred.next = node;
               } else {
                   // 这次还没有阻塞
                   // 但下次如果重试不成功, 则需要阻塞，这时需要设置上一个节点状态为 Node.SIGNAL
                   compareAndSetWaitStatus(pred, ws, Node.SIGNAL);
               }
               return false;
           }
       ```

    4. shouldParkAfterFailedAcquire 执行完毕回到 acquireQueued ，再次 tryAcquire 尝试获取锁，当然这时state 仍为 1，失败 

    5. 当再次进入 shouldParkAfterFailedAcquire 时，这时因为其前驱 node 的 waitStatus 已经是 -1，这次返回true 

    6. 进入 parkAndCheckInterrupt， Thread-1 park（灰色表示）

  * 再次有多个线程经历上述过程竞争失败，变成这个样子

    ![1722500062280](ReentrantLock%20.assets/1722500062280.png)

  * Thread-0 释放锁，进入 tryRelease 流程，如果成功 

    - 设置 exclusiveOwnerThread 为 null 

    - state = 0

      ![1722500098021](ReentrantLock%20.assets/1722500098021.png)

  * 当前队列不为 null，并且 head 的 waitStatus = -1，进入 unparkSuccessor 流程。找到队列中离 head 最近的一个 Node（没取消的），unpark 恢复其运行，本例中即为 Thread-1 ，回到 Thread-1 的 acquireQueued 流程

    ![1722500157402](ReentrantLock%20.assets/1722500157402.png)

  * 如果加锁成功（没有竞争），会设置 

    - exclusiveOwnerThread 为 Thread-1，state = 1 
    - head 指向刚刚 Thread-1 所在的 Node，该 Node 清空 Thread 
    - 原本的 head 因为从链表断开，而可被垃圾回收 

  * 如果这时候有其它线程来竞争（非公平的体现），例如这时有 Thread-4 来了

    * Thread-4 被设置为 exclusiveOwnerThread，state = 1 

    * Thread-1 再次进入 acquireQueued 流程，获取锁失败，重新进入 park 阻塞 

      ![1722500227727](ReentrantLock%20.assets/1722500227727.png)

    

* 可重入原理

  * 通过state计数的增加减少来实现可重入

    ```java
    static final class NonfairSync extends Sync {
        // ...
        
        // Sync 继承过来的方法, 方便阅读, 放在此处
        final boolean nonfairTryAcquire(int acquires) {
            final Thread current = Thread.currentThread();
            int c = getState();
            if (c == 0) {
                if (compareAndSetState(0, acquires)) {
                    setExclusiveOwnerThread(current);
                    return true;
                }
            }
            // 如果已经获得了锁, 线程还是当前线程, 表示发生了锁重入
            else if (current == getExclusiveOwnerThread()) {
                // state++
                int nextc = c + acquires;
                if (nextc < 0) // overflow
                    throw new Error("Maximum lock count exceeded");
                setState(nextc);
                return true;
            }
            return false;
        }
        
        // Sync 继承过来的方法, 方便阅读, 放在此处
        protected final boolean tryRelease(int releases) {
            // state-- 
            int c = getState() - releases;
            if (Thread.currentThread() != getExclusiveOwnerThread())
                throw new IllegalMonitorStateException();
            boolean free = false;
            // 支持锁重入, 只有 state 减为 0, 才释放成功
            if (c == 0) {
                free = true;
                setExclusiveOwnerThread(null);
            }
            setState(c);
            return free;
        }
    }
    ```

    

* 可打断原理
  * 不可打断模式：在此模式下，即使它被打断，仍会驻留在 AQS 队列中，一直要等到获得锁后方能得知自己被打断了

* 阻塞原理

  * 每个条件变量其实就对应着一个等待队列，其实现类是 ConditionObject 

  * 开始 Thread-0 持有锁，调用 await，进入 ConditionObject 的 addConditionWaiter 流程 

    创建新的 Node 状态为 -2（Node.CONDITION），关联 Thread-0，加入等待队列尾部

    ![1722503833983](ReentrantLock%20.assets/1722503833983.png)

    ```java
            public final void await() throws InterruptedException {
                if (Thread.interrupted())
                    throw new InterruptedException();
                //加入到条件变量的等待队列，这里没有空的头结点
                Node node = addConditionWaiter();
                //清除所有的锁
                int savedState = fullyRelease(node);
                int interruptMode = 0;
                while (!isOnSyncQueue(node)) {
                    LockSupport.park(this);
                    if ((interruptMode = checkInterruptWhileWaiting(node)) != 0)
                        break;
                }
                if (acquireQueued(node, savedState) && interruptMode != THROW_IE)
                    interruptMode = REINTERRUPT;
                if (node.nextWaiter != null) // clean up if cancelled
                    unlinkCancelledWaiters();
                if (interruptMode != 0)
                    reportInterruptAfterWait(interruptMode);
            }
    ```

    ```java
            private Node addConditionWaiter() {
                Node t = lastWaiter;
                // If lastWaiter is cancelled, clean out.
                if (t != null && t.waitStatus != Node.CONDITION) {
                    unlinkCancelledWaiters();
                    t = lastWaiter;
                }
                Node node = new Node(Thread.currentThread(), Node.CONDITION);
                //空的当头结点
                if (t == null)
                    firstWaiter = node;
                else
                    t.nextWaiter = node;
                lastWaiter = node;
                return node;
            }
    ```

    ```java
        final int fullyRelease(Node node) {
            boolean failed = true;
            try {
                int savedState = getState();
                if (release(savedState)) {
                    failed = false;
                    return savedState;
                } else {
                    throw new IllegalMonitorStateException();
                }
            } finally {
                if (failed)
                    node.waitStatus = Node.CANCELLED;
            }
        }
    ```

    ```java
        public final boolean release(int arg) {
            if (tryRelease(arg)) {
                Node h = head;
                if (h != null && h.waitStatus != 0)
                    //唤醒下一个节点
                    unparkSuccessor(h);
                return true;
            }
            return false;
        }
    ```

    

* 唤醒原理

  * 假设 Thread-1 要来唤醒 Thread-0

    ![1722502433108](ReentrantLock%20.assets/1722502433108.png)

    * 在ConditionObject中

      ```java
              public final void signal() {
                  //调用线程是不是锁的持有者，只有owner线程才有资格唤醒
                  if (!isHeldExclusively())
                      //不是，直接抛异常
                      throw new IllegalMonitorStateException();
                  //找队首元素
                  Node first = firstWaiter;
                  if (first != null)
                      //不为空，释放队首元素
                      doSignal(first);
              }
      ```

    * 进入 ConditionObject 的 doSignal 流程，取得等待队列中第一个 Node，即 Thread-0 所在 Node

      ![1722503641742](ReentrantLock%20.assets/1722503641742.png)

      ```java
              private void doSignal(Node first) {
                  do {
                      //下一个结点有就设置为first，没有就设置为null
                      if ( (firstWaiter = first.nextWaiter) == null)
                          lastWaiter = null;
                      //不指向任何节点，从条件变量队列中里面断开了
                      first.nextWaiter = null;
                  }
                  //transferForSignal把这个节点转移到竞争锁的链表中
                  while (!transferForSignal(first) &&
                        //转移失败，就尝试获取下一个结点
                        ) != null);
              }
      ```

    * 执行 transferForSignal 流程，将该 Node 加入 AQS 队列尾部，将 Thread-0 的 waitStatus 改为 0，Thread-3 的waitStatus 改为 -1

      ![1722503435636](ReentrantLock%20.assets/1722503435636.png)

      ```java
          final boolean transferForSignal(Node node) {
              /*
               * If cannot change waitStatus, the node has been cancelled.
               */
              //从条件变量的改成0
              if (!compareAndSetWaitStatus(node, Node.CONDITION, 0))
                  //不成功返回false
                  return false;
              //enq把节点加入到等待队列的尾部，成功了就返回前驱节点
              Node p = enq(node);
              int ws = p.waitStatus;
              //把0改为-1，因为不是最后一个了
              if (ws > 0 || !compareAndSetWaitStatus(p, ws, Node.SIGNAL))
                  LockSupport.unpark(node.thread);
              return true;
          }
      ```

      