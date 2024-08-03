#### Redis开发经验

* Redis命名的基本格式，应该遵循基本格式

  * [业务名称]:数据名:id

  * 长度不超过44字节

  * 不包含特殊字符

  * 优点：

    * 可读性强
    * 避免key冲突
    * 方便管理
    * 更节省内存: key是string类型，底层编码包含int、embstr和raw三种（==可以使用object encoding key名字==）。embstr在小于44字节使用，采用连续内存空间，内存占用更小

* BigKey

  * BigKey通常以Key的大小和Key中成员的数量来综合判定，例如:.
    * Key本身的数据量过大:一个String类型的Key，它的值为5 MB。
    *  Key中的成员数过多: 一个ZSET类型的Key，它的成员数量为10,000个。
    *  Key中成员的数据量过大：一个Hash类型的Key，它的成员数量虽然只有1,000个但这些成员的Value(值〉总大小为100 MB
  * 推荐值:
    * 单个key的value小于10KB
    * 对于集合类型的key，建议元素数量小于1000
  * BigKey的危害
    * 网络阻塞
      * 对BigKey执行读请求时，少量的QPS就可能导致带宽使用率被占满，导致Redis实例，乃至所在物理机变慢
    * 数据倾斜
      * BigKey所在的Redis实例内存使用率远超其他实例，无法使数据分片的内存资源达到均衡
    * Redis阻塞
      * 对元素较多的hash、list、zset等做运算会耗时较旧，使主线程被阻塞
    * CPU压力
      * 对BigKey的数据序列化和反序列化会导致CPU的使用率飙升，影响Redis实例和本机其它应用
  * 如何发现bigkey
    * redis-cli --bigkeys
      * 利用redis-cl提供的--bigkeys参数，可以遍历分析所有key，并返回Key的整体统计信息与每个数据的Top1的big keyscan扫描
      * 自己编程，利用scan指令扫描Redis中的所有key，利用strlen、hlen等命令判断key的长度（此处不建议使用MEMORY USAGE)第三方工具
      * 利用第三方工具，如Redis-Rdb-Tools分析RDB快照文件，全面分析内存使用情况网络监控
      * 自定义工具，监控进出Redis的网络数据，超出预警值时主动告警
  * 如何删除BigKey
    * BigKey内存占用较多，即便时删除这样的key也需要耗费很长时间，导致Redis主线程阻塞，引发一系列问题。
    * redis 3.0及以下版本
      * 如果是集合类型，则遍历BigKey的元素，先逐个删除子元素，最后删除BigKeyRedis 
    * 4.0以后
      * Redis在4.0后提供了异步删除的命令:unlink

* 恰当的数据类型

  ![1721569145587](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721569145587.png)
  * 例2∶假如有hash类型的key，其中有100万对field和value,field是自增id，这个key存在什么问题?如何优化?

    ![1721569215362](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721569215362.png)

    * 问题一：hash的entry数量超过500时，会使用哈希表而不是ZipList，内存占用较多。

    * 可以通过hash-max-ziplist-entries配置entry上限。但是如果entry过多就会导致BigKey问题

    * 方法：打散Hash：拆分为小的hash，将 id / 100 作为key，将id % 100 作为field，这样每100个元素为一个Hash

      ![1721569889419](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721569889419.png)

* 批处理优化：在处理中，数据传输是最费时间的

  * 在Redis中，提供了很多Mxxx命令，可以实现批量插入数据==(这个是原子操作)==

    * 如mset
    * hmset

  * MSET虽然可以批处理，但是却只能操作部分数据类型，因此如果有对复杂数据类型的批处理需要，建议使用Pipeline功能:（==他不是原生的命令，并且这个不是原子操作。最好不要带太多的命令，保证带宽==）

    ![1721570946731](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721570946731.png)

* 集群下的批处理

  * 如MSET或Pipeline这样的批处理需要在一次请求中携带多条命令，而此时如果Redis是一个集群，那批处理命令的多个key必须落在一个插槽中，否则就会导致执行失败。

    ![1721571366421](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721571366421.png)





* 服务端的优化
  * Redis的持久化虽然可以保证数据安全，但也会带来很多额外的开销，因此持久化请遵循下列建议:
    * 用来做缓存的Redis实例尽量不要开启持久化功能
    * 建议关闭RDB持久化功能，使用AOF持久化(RDB时间太长)
    * ==利用脚本定期在slave节点做RDB，实现数据备份（手动RDB）==
    * 设置合理的rewrite阈值，避免频繁的bgrewrite
    * 配置no-appendfsync-on-rewrite = yes，禁止在rewrite期间做aof，避免因AOF引起的阻塞
    * Redis实例的物理机要预留足够内存，应对fork和rewxite
    * 单个Redis实例内存上限不要太大，例如4G或8G。可以加快fork的速度、减少主从同步、数据迁移压力
    * 不要与CPU密集型应用部署在一起
    * 不要与高硬盘负载应用一起部署。例如:数据库、消息队列



* 慢查询：在Redis执行时耗时超过某个闻值的命令，称为慢查询。

  ![1721609264043](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721609264043.png)
  * 慢查询的阈值可以通过配置指定：
    * slowlog-log-slower-than:慢查询阈值，单位是微秒。默认是10000，建议1000

  * 慢查询会被放入慢查询日志中，日志的长度有上限，可以通过配置指定:
    * slowlog-max-len:慢查询日志（本质是一个队列)的长度。默认是128，建议1000
  * 在命令行中获取/添加配置：config get/set slowlog-log-slower-than（配置名），重启就会消失
  * 查看慢查询日志列表（RESP软件也可以查看）:
    * slowlog len:查询慢查询日志长度
    * slowlog get [n]:读取n条慢查询日志
    * slowlog reset:清空慢查询列表

* 命令及安全配置

  * Redis会绑定在0.0.0.0:6379，这样将会将Redis服务暴露到公网上，而Redis如果没有做身份认证，会出现严重的安全漏洞.漏洞重现方式: https://cloud.tencent.com/developer/article/1039000
  * 漏洞出现的核心的原因有以下几点:
    *  Redis未设置密码
    * 利用了Redis的config set命令动态修改Redis配置
    * 使用了Root账号权限启动Redis
  * 为了避免这样的漏洞，这里给出一些建议:
    * Redis一定要设置密码
    * 禁止线上使用下面命令: keys、flushall、flushdb、config set等命令。可以利用rename-command禁用。
    * bind:限制网卡，禁止外网网卡访问
    * 开启防火墙
    * 不要使用Root账户启动Redis
    * 尽量不是有默认的端口

* 内存配置

  * 当Redis内存不足时，可能导致Key频繁被删除、响应时间变长、QPS不稳定等问题。当内存使用率达到90%以上时就需要我们警惕，并快速定位到内存占用的原因。

    ![1721610436259](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721610436259.png)

    * 常用内存命令
    * Info memory
    * Memory xxx
    * 可视化工具也可以查看

  * 内存缓冲区

    * 复制缓冲区:主从复制的repl_backlog_buf，如果太小可能导致频繁的全量复制，影响性能。通过repl-backlog-size来设置，默认1mb

    * AOF缓冲区:AOF刷盘之前的缓存区域，AOF执行rewrite的缓冲区。无法设置容量上限

    * 客户端缓冲区:分为输入缓冲区和输出缓冲区，输入缓冲区最大1G且不能设置。输出缓冲区可以设置

      ![1721611118420](redis%E4%BC%98%E9%9B%85%E5%9C%B0%E8%AE%BE%E8%AE%A1.assets/1721611118420.png)

      * 也可以通过client list查看

* 集群优化

  * 在Redis的默认配置中，如果发现任意一个插槽不可用，则整个集群都会停止对外服务:
  * 为了保证高可用特性，这里建议将cluster-require-full-coverage配置为false
  * 集群节点之间会不断的互相Ping来确定集群中其它节点的状态。每次Ping携带的信息至少包括:
    * 插槽信息
    * 集群状态信息
  * 集群中节点越多，集群状态信息数据量也越大，10个节点的相关信息可能达到1kb，此时每次集群互通需要的带宽会非常高。
    * 解决途径:
      * 避免大集群，集群节点数不要太多，最好少于1000，如果业务庞大，则建立多个集群。
      * 避免在单个物理机中运行太多Redis实例
      * 配置合适的cluster-node-timeout值
  * 集群虽然具备高可用特性，能实现自动故障恢复，但是如果使用不当，也会存在一些问题:
    * 集群完整性问题
    * 集群带宽问题
    * 数据倾斜问题
    * 客户端性能问题
    * 命令的集群兼容性问题
    * lua和事务问题
    * 单体Redis (主从Redis）已经能达到万级别的QPS，并且也具备很强的高可用特性。如果主从能满足业务需求的情况下，尽量不搭建Redis集群。