#### redis主从一致性

* 为了提高Redis的可用性，我们会搭建集群或者主从，现在以主从为例

* 此时我们去写命令，写在主机上，主机会将数据同步给从机，但是假设主机还没来得及把数据写入到从机去的时候，主机宕机了

* 哨兵会发现主机宕机了，于是选举一个slave(从机)变成master(主机)，而此时新的master(主机)上并没有锁的信息，那么其他线程就可以获取锁，又会引发安全问题

* 为了解决这个问题。Redisson提出来了MutiLock锁，使用这把锁的话，那我们就不用主从了，每个节点的地位都是一样的，都可以当做是主机，==那我们就需要将加锁的逻辑写入到每一个主从节点上，只有所有的服务器都写入成功，此时才是加锁成功，假设现在某个节点挂了，那么他去获取锁的时候，只要有一个节点拿不到，都不能算是加锁成功，就保证了加锁的可靠性==

* redis集群搭建

  * 建立三个redis

    ```java
            RLock lock1=redissonClient.getLock("order");
            RLock lock2=redissonClient.getLock("order");
            RLock lock3=redissonClient.getLock("order");
            //创建联锁multiLock
            lock=redissonClient.getMultiLock(lock1,lock2,lock3);
    ```

  * **public class** Redisson **implements** RedissonClient。我们查看getMultiLock

    ```java
        @Override
        public RLock getMultiLock(RLock... locks) {
            return new RedissonMultiLock(locks);
        }
    ```

  * 点击RedissonMultiLock。它是放到一个集合当中。每次加锁要给集合所有的都加锁

    ```java
        final List<RLock> locks = new ArrayList<>();
        
        /**
         * Creates instance with multiple {@link RLock} objects.
         * Each RLock object could be created by own Redisson instance.
         *
         * @param locks - array of locks
         */
        public RedissonMultiLock(RLock... locks) {
            if (locks.length == 0) {
                throw new IllegalArgumentException("Lock objects are not defined");
            }
            this.locks.addAll(Arrays.asList(locks));
        }
    ```

  * RedissonMultiLock类的tryLock()

    ```java
     public boolean tryLock(long waitTime, long leaseTime, TimeUnit unit) throws InterruptedException {
    //        try {
    //            return tryLockAsync(waitTime, leaseTime, unit).get();
    //        } catch (ExecutionException e) {
    //            throw new IllegalStateException(e);
    //        }
            long newLeaseTime = -1;
            if (leaseTime != -1) {
                if (waitTime == -1) {
                    newLeaseTime = unit.toMillis(leaseTime);
                } else {
                    //重连是2倍
                    newLeaseTime = unit.toMillis(waitTime)*2;
                }
            }
    ```

    



* 不可重入Redis分布式锁
  - 原理：利用SETNX的互斥性；利用EX避免死锁；释放锁时判断线程标识
  - 缺陷：不可重入、无法重试、锁超时失效
* 可重入Redis分布式锁
  - 原理：利用Hash结构，记录线程标识与重入次数；利用WatchDog延续锁时间；利用信号量控制锁重试等待
  - 缺陷：Redis宕机引起锁失效问题
* Redisson的multiLock
  - 原理：多个独立的Redis节点，必须在所有节点都获取重入锁，才算获取锁成功