#### kafka原理

* 生产者发送流程、

  ![1719908437531](kafka%E7%9A%84%E5%8E%9F%E7%90%86.assets/1719908437531.png)
  * 队列是在内存中存储，为双端队列

  * 只有数据积累到batch.size之后，sender才会发送数据。默认16k

  * 如果数据迟迟未达到batch.size，sender等待linger.ms设置的时间到了之后就会发送数据。单位ms，默认值是0ms，表示没有延迟。

  * 所以可以灵活调整这两个参数进行调优。batch.size:  linger.ms:

  * 通过send线程发送

    <img src="kafka%E7%9A%84%E5%8E%9F%E7%90%86.assets/1719908758157.png" alt="1719908758157" style="zoom:50%;" />

    * retries默认尝试次数是int的最大值，也可以手动修改
    * 应答ACK有三种
      * 0:生产者发送过来的数据，不需要等数据落盘应答。
      * 1:生产者发送过来的数据，Leader收到数据后应答。
      * -1(all):生产者发送过来的数据，Leader和ISR队列里面的所有节点收齐数据后应答。-1和all等价。



* 在Kafka中，Topic 是一个存储消息的逻辑概念，可以认为是一个消息集合。每条消息发送到 Kafka 集群的消息都有一个类别。物理上来锁，不同的topic的消息是分开存储的。

   ![img](kafka%E7%9A%84%E5%8E%9F%E7%90%86.assets/52158199321a006e6fd3da60524362e3.png) 

  * 每个Topic 可以有多个生产者向它发送消息，也可以有多个消费者去消费其中的消息。

  

* Partition：每个Topic 可以划分多个分区（每个Topic至少有一个分区），==同一topic 不同分区包含不同分区包含的消息是不同的。每个消息在被添加到分区时，都会被分配一个offset （偏移量），它是消息在此分区中的唯一编号，kafka 通过offset 保证消息在分区内的顺序，offset 的顺序不跨分区，即kafka 只保证同一个分区内的消息是有序的。==

   ![img](kafka%E7%9A%84%E5%8E%9F%E7%90%86.assets/e799d902b15d1b8e9ce5b1a8f05c05a8.png) 

* ##### kafka生产消息分发策略

  * 消息是kafka 最基本的数据单元，在kafaka 中，一条消息由key、value 两部分组成。在发送一条消息时，我们可以指定这个key，那么producer 会根据key 和partition 机制来判断当前这条消息应该发送并存储到哪个partition 中。我们可以根据需要进行扩展producer 和partition 机制。

* ##### 消息默认的分发机制

  * 默认情况下，kafka 采用的时hash 取模的分区算法(DefaultPartitioner)。该默认的分区算法，如果key为null，则会随机分配一个分区，这个随机是在这个参数 “matadata.max.age.ms” 的时间范围内随机选择一个。对于这个时间段内，如果key为null，则只会发送到唯一的分区。这个值在默认情况下是10分钟更新一次。
    *  具体分两种情况：
      1.当消息的key不为空时，直接使用murmur哈希算法从**所有**的分区中来选定一个分区
      2.当消息的key为空时，在**可用**分区中按照轮询算法选定一个分区 

* ##### 关于Metadata类

  *  简单理解就是Topc 、 Partition 和 Broker 的映射关系，每个Topic 的每一个 Partition，需要知道对应的broker 列表是什么、Leader是谁、Follower是谁。这些信息都是存储在Metadata这个类的。 

* #### 消费者的消费原理

  * 在实际的生产过程中，每个topic 都会有多个partitions。

    * 多个partitions的好处在于：
      * 一方面能够对broker 上的数据进行分片有效减少了消息的容量从而提升io性能。
      * 另一方面，为了提高消费端的消费能力，一般会通过多个consumer去消费桶一个topic，也就是消费端的负载均衡机制

  * kafka存在consumer group的概念，组内的所有消费者协调在一起来消费订阅主题的所有分区。当然每一个分区只能由同一个消费组内的consumer 来消费，那么同一个consumer group 里面的consumer 是怎么分配该消费哪个分区的数据呢？如下图：

     ![img](kafka%E7%9A%84%E5%8E%9F%E7%90%86.assets/322af78cb2a439d3d5d70c93254a9424.png)

    * ==3个partition 对应3consumer  结果：每个consumer 会消费一个分区==
    * ==3个partition 对应2个consumer  结果：consumer1会消费partition0/partition1分区，consumer2会消费partition2分区==
    * ==3个partition 对应4个或以上consumer  结果：任然只有3个consumer对应3个partition，其他的consumer无法消费消息（和RocketMQ一样）==

  * 结论

    * `如果consumer 比 partition 多是浪费，因为kafka的设计是在一个partition上是不允许并发的。所以consumer 数不要大于partition数`
    * **如果consumer 比partition 少，一个consumer会对应于多个partition，这里主要要合理分配consumer数量的整数倍，否则会导致partition里面的数据被取的不均匀。最好partition数量是consumer数量的整数倍，所以partition 数量很重要，比如取18 就很容易设定consumer 数量。**
    * 如果consumer从多个partition读取到数据，不保证数据间的顺序性。kafka只保证在一个partition上数据是有序的，但多个partition，根据你读的顺序会有不同。
    * ==增减consumer，broker，partition会导致rebalance，所以rebalance后consumer对应的partition会发生变化==



* ##### 消费者分区分配策略

  * 以下情况出发分配**rebalance**分配操作

    > - 同一个consumer group 内新增了消费者
    > - 消费者离开当前所属的consumer group，比如主机停机或宕机等
    > - topic 新增了分区（也就是分区熟练发生了变化）

  * afka提供了3分配策略（可自定义）

    > PARTITION_ASSIGNMENT_STRATEGY_CONFIG

    > - Range（**默认**，范围）
    > - RoundRobin（轮询）
    > - StickyAssignor（沾性）

    *  RangeAssignor ： Range 策略是对每个主题而言的，首先对同一个主题里面的分区按照序号进行排序，并对消费者按照字符顺序进行排序 

      ```doc
      假设  n = 分区数 / 消费数 ； m = 分区数 % 消费者数量
      那么前 m 个消费者每个分配 n + 1 个分区
      后面的（消费者数量 - m）个消费者每个分配n个分区
      
      例如：11个分区，3个消费者 
      A1-0 将消费 0,1,2,3 分区
      A2-0 将消费 4,5,6,7 分区
      A3-0 将消费 8,9,10 分区
      结果：A1-0 和 A2-0 多消费一个分区，没什么
      
      例如：2个主题（T1和T2），分别有10个分区
      A1-0 将消费T1主题的 0,1,2,3 分区，以及T2主题的0,1,2,3分区
      A2-0 将消费 4,5,6 分区，以及T2主题的4,5,6 分区
      A3-0 将消费 7,8,9 分区，以及T2主题的7,8,9 分区
      结果：A1-0 比其他分区多了2个分区，这就是RangeAssignor很明显的弊端。
      
      ```

    *  RoundRobinAssignor ：轮询分区策略就是：

      > - 把所有partition 和所有consumer线程都列出来，然后按照hashcode进行排序
      > - 最后通过轮询算法分配partition给消费线程。

      * **如果所有consumer实例的订阅是相同的，那么partition会均匀分布**。

        **使用轮询分区策略，必须满足两个条件**：

        > 1、每个主题的消费者实例具有相同数量的流
        >
        > 2、每个消费者订阅的主题必须是相同的。

    *  StrickyAssignor 

      kafka在0.11.x 版本支持了StrickyAssignor，翻译过来就是粘带策略，它有两个目的

      > 1、分区的分配尽可能的均匀
      >
      > 2、分区的分配尽可能和上次分配保持相同
      >
      > 当两者冲突时，第一个目标优先于第二目标

      ```doc
      假设消费组有3个消费者，C0、C1、C3，它们分别订阅了4个Topic（t0，t1，t2，t3），并且每个主题有两个分区（p0,p1），也就是说，整个消费组订阅了8个分区：t0p0、t0p1、t1p0、t1p1、t2p0、t2p1、t3p0、t3p1
      那么最终的分配场景结果为：
      C0: t0p0 t1p1 t3p0
      C1: t0p1 t2p0 t3p1
      C2: t1p0 t2p1
      这样的分配策略类似轮询策略，但是其实不是，因为如果C1 这个消费者挂了，就必然会造成重新分区（reblance），如果是轮询，那么结果应该是
      C0: t0p0 t1p1 t2p0 t3p0
      C2: t0p1 t2p0 t2p1 t3p1
      但是不是如此，因为他要满足粘带策略，所以他会满足 “分区的分配尽可能和上次分配保持相同”，所以分配结果是
      C0: t0p0 t1p1 t3p0 + t2p0 
      C2: t1p0 t2p1 + t0p1 t3p1
      ```

    * ##### Coordinator

      *   `每个consumer group 都会选择一个broker作为自己的coordinator，他是负责监控整个消费组里的各个分区的心跳，以及判断是否宕机，和开启rebalance的。` 

      * 提供了一个角色：coordinator 来执行对于Consumer group的管理，==当consumer group的第一个consumer 启动的时候，它会去和kafka server确定谁是它们的coordinator。之后该group 内的所有成员都会和该coordinator进行协调通信。==

        每个KafkaServer都有一个GroupCoordinator实例，管理多个消费者组，主要用于offset位移管理和Consumer Rebalance。

      *  消费者向kafka 集群中的任意一个broker发送一个GroupCoordinatorRequest请求，==服务端会返回一个负载最小的broker节点的id，并将该broker设置为coordinator==

    * ##### joinGroup

      * 表示加入到consumer group 中，在这一步中，所有的成员都会向coordinator 发送 joinGroup的请求。一旦所有成员都发送了joinGroup请求，那么coordinator 会选择一个consumer担任leader 角色，并把组成员信息和订阅信息发送消费者

      *  **consumer的leader选举** 

        *  选举算法比较简单，如果消费组内没有leader，那么第一个加入消费组的消费者就是消费者leader，如果这个时候leader 消费者退出消费组，那么会重新选举一个leader，这个选举很随意，类似随机算法 

      * 在rebalance 之前，需要保证coordinator 是已经确定好了的，整个rebalance 分为两个步骤

        * 1、Join Group

        * 2、Synchronizing Group State

          ```doc
          完成分区分配后，就进入了Synchronizing Group State 阶段，主要逻辑是向GroupCoordinator发送SyncGroupRequest请求，并且处理SyncGroupResponse响应，简单来说，就是leader将消费者对应的partition分配方案同步给consumer Group中的所有consumer
          
          每个消费者都会向coordinator发送syncGroup请求，不过只有leader节点会发送分配方案，其他消费者只是打打酱油而已。当leader 把方案发给coordinator以后，coordinator会把结果设置到SyncGroupResponse中。这样所有成员都会知道自己应该消费哪个分区
          
          consumer group 的分区分配方案是在客户端执行的，kafka将这个权利下方给客户端主要是因为这样做可以有更好的灵活性
          ```

*  consumer group rebalance过程 

  * ==对于每个consumer group 子集，都会在服务端对应一个GroupCoordinator进行管理，GroupCoordinator会在Zookeeper上添加watcher，当消费者加入或者退出consumer group时，会修改Zookeeper上保存的数据，从而触发 GroupCoordinator开始Rebalance操作==
  * 当消费者准备加入某个Consumer Group 或者 GroupCoordinator发生故障转移时，消费者并不知道GroupCoordinator 在网络中的位置，这个时候就需要确定GroupCoordinator，==消费者会向集群中的任意一个Broker节点发送ConsumerMetadataRequest请求，收到请求的broker会返回一个response作为响应，其中包含管理当前ConsumerGroup的GroupCoordinator。==
  * 消费者会根据broker的返回信息，连接到groupCoordinator，并且发送HeartbeatRequest，发送心跳的目的是要告诉GroupCoordinator这个消费者是正常在线的。当消费者在指定时间内没有发送心跳请求，则Group Coordinator会触发Rebalance操作
  * 发起join group请求的两种情况：
    * 如果GroupCoordinator返回的心跳包数据包含异常，说明GroupCoordinator因为前面说的几种情况导致了Rebalance操作，那这个时候，Consumer会发送join Group 请求。
    * 新加入到consumer group的consumer 确定好了GroupCoordinator以后，消费者会向GroupCoordinator发起join group 请求，GroupCoordinator会收集全部消费者信息之后，来确定可用的消费者，==并从中选取一个消费者成为consumer group leader==。并把相应的信息（分区分配策略、leader_id、……）封装成response 返回给所有消费者，但是只有group leader 会受到当前consumer group 中的所有消费者信息。当消费者确定自己是group leader 以后，会根据消费者的信息以及选定分区分配策略进行分区分配
      接着进入Synchronizing Group State 阶段，每个消费者会发送SyncGroupState 请求到Group Coordinator，但是`只有Group Leader 的请求会存在分区分配结果`，GroupCoordinator会根据Group Leader 的分区分配结果形成SyncGroupResponse返回给所有的Consumer。Consumer 根据分配的结果，执行响应的操作。

* ##### offset

  * offset就是用来确定消费端的消费位置，每个topic可以划分多个分区（每个topic 至少有一个分区），同意topic 下的不同分区包含的消息是不同的。每个消息在被添加到分区时，都会被分配一个offset（偏移量），它是消息在此分区中的唯一编号。
  * kafka通过offset 保证消息在分区内的顺序，offset 的顺序不跨分区，即kafka 只保证在同一个分区内的消息是有序的。
  * 对于应用层的消费者来说，每次消费一个消息并且提交以后，会保存当前消费到的最近的一个offset。那么offset保存在哪里？
    * 在kafka中，提供了一个consumer_offset_*的一个topic，把offset信息写入到这个topic中。
    * consumer_offset——里保存了每个consumer group 某一时刻提交的offset信息。
    * __consumer_offsets 默认有50个分区。
  * 计算公式：Math.abs(“gourpid”.hashCode()) % groupMetadataTopicPartitionCount

    * 由于默认情况下groupMetadataTopicPartitionCount 有50个分区，如果计算的结果是35，那么意味着当前的consumer_group的位移信息保存在__consumer_offsets的第35个分区
      