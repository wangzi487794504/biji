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