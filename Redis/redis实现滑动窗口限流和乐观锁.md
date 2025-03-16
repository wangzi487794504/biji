#### Redis实现滑动窗口限流

* 滑动窗口限流是一种流量控制策略，用于控制在一定时间内允许执行的操作数量或请求频率。它的工作方式类似于一个滑动时间窗口，在窗口内允许的操作数量是固定的，窗口会随着时间的推移不断滑动。

* 滑动窗口限流的主要**优点是可以在时间内平滑地控制流量**，而不是简单地设置固定的请求数或速率。这使得系统可以更**灵活地应对突发流量或峰值流量**，而不会因为固定速率的限制而浪费资源或降低系统性能。

* 利用Redis，我们就可以实现一个简单的滑动窗口限流的功能。因为滑动窗口和时间有关，所以很容易能想到要基于时间进行统计。

* **那么我们只需要在每一次有请求进来的时候，记录下请求的时间戳和请求的数据，然后在统计窗口内请求的数量时，只需要统计窗口内的被记录的数据量有多少条就行了。**

* 在Redis中，我们可以基于ZSET来实现这个功能。假如我们限定login接口一分钟只能调用100次，那么，我们就可以把login接口这个需要做限流的资源名作为key在redis中进行存储，然后value我们现在ZSET这种数据结构，把他的score设置为当前请求的时间戳，member的话建议用请求的详情的hash进行存储（或者UUID、MD5什么的），避免在并发时，时间戳一致出现scode和memberv一样导致被zadd幂等的问题。

  * **使用 ZSet 存储请求记录**：将每次请求的时间戳作为分数（score），请求的唯一标识（如用户 ID、IP 地址等）作为成员（member）存储到 ZSet 中。

  * **移除过期的请求记录**：根据滑动窗口的大小，移除 ZSet 中时间戳早于当前时间减去窗口大小的记录，确保 ZSet 中只包含当前窗口内的请求记录。

  * **统计当前窗口内的请求数量**：通过计算 ZSet 中成员的数量，得到当前窗口内的请求数量。

  * **判断是否限流**：如果当前窗口内的请求数量超过了预设的阈值，则拒绝该请求；否则，允许该请求，并将该请求的记录添加到 ZSet 中。

  * 代码实现

    ```java
    import redis.clients.jedis.Jedis;
    
    public class SlidingWindowRateLimiter {
        private Jedis jedis;
        private String key;
        private int limit;
    
        public boolean allowRequest(String key) {
            //当前时间戳
            long currentTime = System.currentTimeMillis();
            //窗口开始时间是当前时间减60s
            long windowStart = currentTime - 60 * 1000;
            //删除窗口开始时间之前的所有数据
            jedis.zremrangeByScore(key, "-inf", String.valueOf(windowStart));
            //计算总请求数
            long currentRequests = jedis.zcard(key);
        	//窗口足够则把当前请求加入
            if (currentRequests < limit) {
                jedis.zadd(key, currentTime, String.valueOf(currentTime));
                return true;
            }
    
            return false;
        }
    }
    ```

    

* 在 Redisson框架中，已经给我们提供了一个限流器——RRateLimiter，不过他并不是滑动窗口，而是一个令牌桶的算法。





* 乐观锁

  * 所谓乐观锁，其实就是基于CAS的机制，CAS的本质是Compare And Swap，就是需要知道一个key在修改前的值，去进行比较。

  * 在Redis中，想要实现这个功能，我们可以依赖 WATCH 命令。这个命令一旦运行，他会确保只有在 WATCH 监视的键在调用 EXEC 之前没有改变时，后续的事务才会执行。

  * 例如，如果没有 INCRBY，我们可以用下面的方式实现原子的增量操作：

    ```java
    WATCH counter
    GET counter
    MULTI
    SET counter <从 GET 获得的值 + 任何增量>
    EXEC
    ```

    