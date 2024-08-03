#### 读写锁

* **ReentrantReadWriteLock**

  * 当读操作远远高于写操作时，这时候使用 `读写锁` 让 `读-读` 可以并发，提高性能。 

    类似于数据库中的 `select ... from ... lock in share mode` 

  * 读锁保护数据的 `read()` 方法，写锁保护数据的 `write()` 方法

    ```java
    class DataContainer {
        private Object data;
        private ReentrantReadWriteLock rw = new ReentrantReadWriteLock();
        private ReentrantReadWriteLock.ReadLock r = rw.readLock();
        private ReentrantReadWriteLock.WriteLock w = rw.writeLock();
        
        public Object read() {
            log.debug("获取读锁...");
            r.lock();
            try {
                log.debug("读取");
                sleep(1);
                return data;
            } finally {
                log.debug("释放读锁...");
                r.unlock();
            }
        }
        public void write() {
            log.debug("获取写锁...");
            w.lock();
            try {
                log.debug("写入");
                sleep(1);
            } finally {
                log.debug("释放写锁...");
                w.unlock();
            }
        }
    }
    ```

    

  * 在多个线程读时可以一起进去

  * 读写或写写会阻塞等待

    * 重入时不支持升级：即持有读锁的情况下去获取写锁，会导致获取写锁永久等待
    * 重入时支持降级：即持有写锁的情况下去获取读锁

  * 一个线程即读又写会阻塞

  * 读锁不支持条件变量,写锁支持

* 应用之缓存，更新时，是先清缓存还是先更新数据库 

  * 先清缓存

    ![1722497463455](%E8%AF%BB%E5%86%99%E9%94%81%E5%92%8C%E4%BF%A1%E5%8F%B7%E9%87%8F%E6%9C%BA%E5%88%B6.assets/1722497463455.png)

  * 先更新数据库

    ![1722497767927](%E8%AF%BB%E5%86%99%E9%94%81%E5%92%8C%E4%BF%A1%E5%8F%B7%E9%87%8F%E6%9C%BA%E5%88%B6.assets/1722497767927.png)

  

* 读写锁原理

  * 读写锁用的是同一个 Sycn 同步器，因此等待队列、state 等也是同一个 

  *  t1 成功上锁，流程与 ReentrantLock 加锁相比没有特殊之处，不同是写锁状态占了 state 的低 16 位，而读锁使用的是 state 的高 16 位 

    * 执行顺序，先执行acquire

      ```java
          public final void acquire(int arg) {
              if (!tryAcquire(arg) &&
                  acquireQueued(addWaiter(Node.EXCLUSIVE), arg))
                  selfInterrupt();
          }
      ```

    * 调用tryAcquire方法，子类重写的有一些不同，这是写锁的lock

      ```java
              protected final boolean tryAcquire(int acquires) {
                  Thread current = Thread.currentThread();
                  int c = getState();
                  int w = exclusiveCount(c);
                  //既有可能加了读锁，又有可能加了写锁。分别是c的高低16位
                  if (c != 0) {
                      //w =0表示是写锁为0，说明加的是读锁，那和写锁是互斥，并且判断锁是不是自己加的（重入）
                      if (w == 0 || current != getExclusiveOwnerThread())
                          return false;
                      if (w + exclusiveCount(acquires) > MAX_COUNT)
                          throw new Error("Maximum lock count exceeded");
                      // Reentrant acquire
                      setState(c + acquires);
                      return true;
                  }
                  //c==0，判断公平锁还是非公平
                  if (writerShouldBlock() ||
                      //改值看是否成功
                      !compareAndSetState(c, c + acquires))
                      return false;
                  //这里就是加写锁
                  setExclusiveOwnerThread(current);
                  return true;
              }
      ```

    * 查看读写的lock

      * t2 执行 r.lock，这时进入读锁的 sync.acquireShared(1) 流程，首先会进入tryAcquireShared 流程。如果有写锁占据，那么 tryAcquireShared 返回 -1 表示失败 

        tryAcquireShared 返回值表示

        - -1 表示失败
        - 0 表示成功，但后继节点不会继续唤醒 
        - 正数表示成功，而且数值是还有几个后继节点需要唤醒，读写锁返回 1

      ```java
              public void lock() {
                  sync.acquireShared(1);
              }
      ```

      ```java
          public final void acquireShared(int arg) {\
              //获取一个整数，大于等于0说明成功
              if (tryAcquireShared(arg) < 0)
                  doAcquireShared(arg);
          }
      ```

      ```java
             protected final int tryAcquireShared(int unused) {
                  Thread current = Thread.currentThread();
                  int c = getState();
                 //查看写锁是不是不为0
                  if (exclusiveCount(c) != 0 &&
                      //查看加写锁是不是自己
                      getExclusiveOwnerThread() != current)
                      return -1;
                 //获得高16位读锁
                  int r = sharedCount(c);
                  if (!readerShouldBlock() &&
                      r < MAX_COUNT &&
                      //加了65536，让高16位加1
                      compareAndSetState(c, c + SHARED_UNIT)) {
                      if (r == 0) {
                          firstReader = current;
                          firstReaderHoldCount = 1;
                      } else if (firstReader == current) {
                          firstReaderHoldCount++;
                      } else {
                          HoldCounter rh = cachedHoldCounter;
                          if (rh == null || rh.tid != getThreadId(current))
                              cachedHoldCounter = rh = readHolds.get();
                          else if (rh.count == 0)
                              readHolds.set(rh);
                          rh.count++;
                      }
                      return 1;
                  }
                  return fullTryAcquireShared(current);
              }
      
      ```

    * 这时会进入 sync.doAcquireShared(1) 流程，首先也是调用 addWaiter 添加节点，不同之处在于节点被设置为Node.SHARED 模式而非 Node.EXCLUSIVE 模式，注意此时 t2 仍处于活跃状态

      ![1722516293536](%E8%AF%BB%E5%86%99%E9%94%81%E5%92%8C%E4%BF%A1%E5%8F%B7%E9%87%8F%E6%9C%BA%E5%88%B6.assets/1722516293536.png)

      ```java
      private void doAcquireShared(int arg) {
          //共享的节点类型
              final Node node = addWaiter(Node.SHARED);
              boolean failed = true;
              try {
                  boolean interrupted = false;
                  for (;;) {
                      final Node p = node.predecessor();
                      if (p == head) {
                          //尝试去竞争锁
                          int r = tryAcquireShared(arg);
                          if (r >= 0) {
                              setHeadAndPropagate(node, r);
                              p.next = null; // help GC
                              if (interrupted)
                                  selfInterrupt();
                              failed = false;
                              return;
                          }
                      }
                      //竞争失败
                      if (shouldParkAfterFailedAcquire(p, node) &&
                          //在这里等待被线程唤醒
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
              protected final int tryAcquireShared(int unused) {
                  Thread current = Thread.currentThread();
                  int c = getState();
                  if (exclusiveCount(c) != 0 &&
                      getExclusiveOwnerThread() != current)
                      return -1;
                  int r = sharedCount(c);
                  if (!readerShouldBlock() &&
                      r < MAX_COUNT &&
                      //这里是加每个1
                      compareAndSetState(c, c + SHARED_UNIT)) {
                      if (r == 0) {
                          firstReader = current;
                          firstReaderHoldCount = 1;
                      } else if (firstReader == current) {
                          firstReaderHoldCount++;
                      } else {
                          HoldCounter rh = cachedHoldCounter;
                          if (rh == null || rh.tid != getThreadId(current))
                              cachedHoldCounter = rh = readHolds.get();
                          else if (rh.count == 0)
                              readHolds.set(rh);
                          rh.count++;
                      }
                      return 1;
                  }
                  return fullTryAcquireShared(current);
              }
      ```

      

    * t2 会看看自己的节点是不是老二，如果是，还会再次调用 tryAcquireShared(1) 来尝试获取锁 

      如果没有成功，在 doAcquireShared 内 for (;;) 循环一次，把前驱节点的 waitStatus 改为 -1，再 for (;;) 循环一次尝试 tryAcquireShared(1) 如果还不成功，那么在 parkAndCheckInterrupt() 处 park

    * 这种状态下，假设又有 t3 加读锁和 t4 加写锁，这期间 t1 仍然持有锁，就变成了下面的样子

      ![1722516864964](%E8%AF%BB%E5%86%99%E9%94%81%E5%92%8C%E4%BF%A1%E5%8F%B7%E9%87%8F%E6%9C%BA%E5%88%B6.assets/1722516864964.png)

      ```JAVA
              protected final boolean tryRelease(int releases) {
                  if (!isHeldExclusively())
                      throw new IllegalMonitorStateException();
                  int nextc = getState() - releases;
                  //剪成0才解开锁
                  boolean free = exclusiveCount(nextc) == 0;
                  if (free)
                      setExclusiveOwnerThread(null);
                  setState(nextc);
                  return free;
              }
      ```

      ```java
          public final boolean release(int arg) {
              if (tryRelease(arg)) {
                  Node h = head;
                  if (h != null && h.waitStatus != 0)
                      unparkSuccessor(h);
                  return true;
              }
              return false;
          }
      ```

    * 这时 t2 已经恢复运行，接下来 t2 调用 setHeadAndPropagate(node, 1)，它原本所在节点被置为头节点

      * 事情还没完，在 setHeadAndPropagate 方法内还会检查下一个节点是否是 shared，如果是则调用 doReleaseShared() 将 head 的状态从 -1 改为 0 并唤醒老二，这时 t3 在 doAcquireShared 内parkAndCheckInterrupt() 处恢复运行

      ```java
          private void setHeadAndPropagate(Node node, int propagate) {
              Node h = head; // Record old head for check below
              setHead(node);
              if (propagate > 0 || h == null || h.waitStatus < 0 ||
                  (h = head) == null || h.waitStatus < 0) {
                  //拿到当前节点的下一个
                  Node s = node.next;
                  //查看节点是不是共享状态，是进入这个
                  if (s == null || s.isShared())
                      doReleaseShared();
              }
          }
      ```

      ```java
          private void doReleaseShared() {
              for (;;) {
                  Node h = head;
                  if (h != null && h != tail) {
                      int ws = h.waitStatus;
                      if (ws == Node.SIGNAL) {
                          //头结点从-1改为0，避免其他线程干扰
                          if (!compareAndSetWaitStatus(h, Node.SIGNAL, 0))
                              continue;            
                          //唤醒下一个结点
                          unparkSuccessor(h);
                      }
                      else if (ws == 0 &&
                               !compareAndSetWaitStatus(h, 0, Node.PROPAGATE))
                          continue;                // loop on failed CAS
                  }
                  if (h == head)                   // loop if head changed
                      break;
              }
          }
      ```





##### StampedLock

* 该类自 JDK 8 加入，是为了进一步优化读性能，它的特点是在使用读锁、写锁时都必须配合【戳】使用加解读锁 

  ```java
  //读锁
  long stamp = lock.readLock();
  lock.unlockRead(stamp);
  //写锁
  long stamp = lock.writeLock();
  lock.unlockWrite(stamp);
  ```

* 乐观读，StampedLock 支持 `tryOptimisticRead()` 方法（乐观读），读取完毕后需要做一次 `戳校验` 如果校验通过，表示这期间确实没有写操作，数据可以安全使用，如果校验没通过，需要重新获取读锁，保证数据安全。==有竞争才加锁，负责用乐观办法就行==

  ```java
  long stamp = lock.tryOptimisticRead();
  // 验戳
  if(!lock.validate(stamp)){
      // 锁升级
  }
  ```

* StampedLock 不支持条件变量 

* StampedLock 不支持锁重入