#### Tomcat线程池

* tomcat在哪里用到线程池呢

  ![1722477492961](Tomcat%E7%BA%BF%E7%A8%8B%E6%B1%A0.assets/1722477492961.png)

* LimitLatch 用来限流，可以控制最大连接个数，类似 J.U.C 中的 Semaphore 后面再讲 

* Acceptor 只负责【接收新的 socket 连接】 

* Poller 只负责监听 socket channel 是否有【可读的 I/O 事件】 

* 一旦可读，封装一个任务对象（socketProcessor），提交给 Executor 线程池处理 

* Executor 线程池中的工作线程最终负责【处理请求】 

* 扩展了ThreadPoolExecutor

  * Tomcat 线程池扩展了 ThreadPoolExecutor，行为稍有不同 

    - 如果总线程数达到 maximumPoolSize 

    - - 这时不会立刻抛 RejectedExecutionException 异常 
      - 而是再次尝试将任务放入队列，如果还失败，才抛出 RejectedExecutionException 异常 

  * Tomcat源码

    ```java
    public void execute(Runnable command, long timeout, TimeUnit unit) {
        submittedCount.incrementAndGet();
        try {
            //执行execute
            super.execute(command);
        } catch (RejectedExecutionException rx) {
            //如果满了，也不会直接拒绝
            if (super.getQueue() instanceof TaskQueue) {
                //获取阻塞队列
                final TaskQueue queue = (TaskQueue)super.getQueue();
                try {
                    //再次尝试将任务放入队列
                    if (!queue.force(command, timeout, unit)) {
                        submittedCount.decrementAndGet();
                        //如果还失败，才抛出 RejectedExecutionException 异常 
                        throw new RejectedExecutionException("Queue capacity is full.");
                    }
                } catch (InterruptedException x) {
                    submittedCount.decrementAndGet();
                    Thread.interrupted();
                    throw new RejectedExecutionException(x);
                }
            } else {
                submittedCount.decrementAndGet();
                throw rx;
            }
        }
    }
    ```

  * 队列调用的是带时间的poll方法

    ```java
    public boolean force(Runnable o, long timeout, TimeUnit unit) throws InterruptedException {
        if ( parent.isShutdown() ) 
            throw new RejectedExecutionException(
            "Executor not running, can't force a command into the queue"
        );
        return super.offer(o,timeout,unit); //forces the item onto the queue, to be used if the task 
        is rejected
    }
    ```

  * Connector配置，默认就在serve.xml中配置，单独是一个标签

    ![1722478071527](Tomcat%E7%BA%BF%E7%A8%8B%E6%B1%A0.assets/1722478071527.png)

  * Executor线程配置

    ![1722478426826](Tomcat%E7%BA%BF%E7%A8%8B%E6%B1%A0.assets/1722478426826.png)

