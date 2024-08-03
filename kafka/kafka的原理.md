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