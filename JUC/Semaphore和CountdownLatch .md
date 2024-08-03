#### Semaphore

* 信号量，用来限制能同时访问共享资源的线程上限。

  ```java
  public static void main(String[] args) {
      // 1. 创建 semaphore 对象
      Semaphore semaphore = new Semaphore(3);
      // 2. 10个线程同时运行
      for (int i = 0; i < 10; i++) {
          new Thread(() -> {
              // 3. 获取许可
              try {
                  semaphore.acquire();
              } catch (InterruptedException e) {
                  e.printStackTrace();
              }
              try {
                  log.debug("running...");
                  sleep(1);
                  log.debug("end...");
              } finally {
                  // 4. 释放许可
                  semaphore.release();
              }
          }).start();
      }
   }
  ```

* 应用：使用 Semaphore 限流，在访问高峰期时，让请求线程阻塞，高峰期过去再释放许可，当然它只适合限制单机线程数量，并且仅是限制线程数，而不是限制资源数（例如连接数，请对比 Tomcat LimitLatch 的实现） 

* 用 Semaphore 实现简单连接池，对比『享元模式』下的实现（用wait notify），性能和可读性显然更好,注意下面的实现中线程数和数据库连接数是相等的



* 原理

  * 查看构造方法

    ```java
        public Semaphore(int permits) {
            sync = new NonfairSync(permits);
        }
    Semaphore(int permits, boolean fair) {
            sync = fair ? new FairSync(permits) : new NonfairSync(permits);
        }
    ```

  * 查看它实现的Sync

    ```java
        abstract static class Sync extends AbstractQueuedSynchronizer {
            private static final long serialVersionUID = 1192457210091910933L;
    
            Sync(int permits) {
                //数量给了state
                setState(permits);
            }
    ```

  * 查看acquire方法

    ```java
        public void acquire() throws InterruptedException {
            //获取许可数1
            sync.acquireSharedInterruptibly(1);
        }
    ```

  * 查看acquireSharedInterruptibly

    ```java
        public final void acquireSharedInterruptibly(int arg)
                throws InterruptedException {
            if (Thread.interrupted())
                throw new InterruptedException();
            
            if (tryAcquireShared(arg) < 0)
                //返回值小于0，无可用，调用它
                doAcquireSharedInterruptibly(arg);
        }
    ```

  * 查看tryAcquireShared

    ```java
            final int nonfairTryAcquireShared(int acquires) {
                for (;;) {
                    //获取可用的许可数
                    int available = getState();
                    //剩余的许可数
                    int remaining = available - acquires;
                    //remaining < 0成立了他就直接返回了
                    if (remaining < 0 ||
                        //尝试改变
                        compareAndSetState(available, remaining))
                        //返回剩余的
                        return remaining;
                }
            }
    ```

  * 返回值小于0，无可用，调用它doAcquireSharedInterruptibly

    ```java
        private void doAcquireSharedInterruptibly(int arg)
            throws InterruptedException {
            //创建一个头节点
            final Node node = addWaiter(Node.SHARED);
            boolean failed = true;
            try {
                for (;;) {
                    final Node p = node.predecessor();
                    if (p == head) {
                        //老二，还有资格去尝试
                        int r = tryAcquireShared(arg);
                        //没获取到就是-1，不成立if
                        if (r >= 0) {
                            setHeadAndPropagate(node, r);
                            p.next = null; // help GC
                            failed = false;
                            return;
                        }
                    }
                    if (shouldParkAfterFailedAcquire(p, node) &&
                        //让他停下
                        parkAndCheckInterrupt())
                        throw new InterruptedException();
                }
            } finally {
                if (failed)
                    cancelAcquire(node);
            }
        }
    ```

    





##### CountdownLatch 

* 用来进行线程同步协作，等待所有线程完成倒计时。 其中构造参数用来初始化等待计数值，await() 用来等待计数归零，countDown() 用来让计数减一

* 源码

  ```java
  public class CountDownLatch {
  class Sync extends AbstractQueuedSynchronizer {
          private static final long serialVersionUID = 4982264981922014374L;
  
          Sync(int count) {
              setState(count);
          }
  
          int getCount() {
              return getState();
          }
  
          protected int tryAcquireShared(int acquires) {
              //判断==0，等于0获得锁，大于无法获得
              return (getState() == 0) ? 1 : -1;
          }
  
          protected boolean tryReleaseShared(int releases) {
              // Decrement count; signal when transition to zero
              for (;;) {
                  int c = getState();
                  if (c == 0)
                      return false;
                  int nextc = c-1;
                  if (compareAndSetState(c, nextc))
                      //剪成0唤醒阻塞线程
                      return nextc == 0;
              }
          }
  ```








##### CyclicBarrier

* 循环栅栏，用来进行线程协作，等待线程满足某个计数。构造时设置『计数个数』，每个线程执行到某个需要“同步”的时刻调用 await() 方法进行等待，当等待的线程数满足『计数个数』时，继续执行.

* CyclicBarrier 与 CountDownLatch 的主要区别在于 CyclicBarrier 是可以重用的 CyclicBarrier 可以被比喻为『人满发车』（再一次运行又重头开始计数，跑起来之后就重新为设置的个数了）

  ```java
  CyclicBarrier cb = new CyclicBarrier(2); // 个数为2时才会继续执行
  
  new Thread(()->{
      System.out.println("线程1开始.."+new Date());
      try {
          cb.await(); // 当个数不足时，等待，此时2-1=1，还差一个
      } catch (InterruptedException | BrokenBarrierException e) {
          e.printStackTrace();
      }
      System.out.println("线程1继续向下运行..."+new Date());
  }).start();
  
  new Thread(()->{
      System.out.println("线程2开始.."+new Date());
      try { 
          Thread.sleep(2000); 
      } catch (InterruptedException e) {
      }
      try {
          cb.await(); // 2 秒后，线程个数够2，继续运行
      } catch (InterruptedException | BrokenBarrierException e) {
          e.printStackTrace();
      }
      System.out.println("线程2继续向下运行..."+new Date());
  }).start();
  ```

  