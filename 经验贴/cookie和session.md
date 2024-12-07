#### cookie和session

* 当服务器tomcat第一次接收到客户端的请求时，会开辟一块独立的session空间，建立一个session对象，同时会生成一个session id，通过响应头的方式保存到客户端浏览器的cookie当中。以后客户端的每次请求，都会在请求头部带上这个session id，这样就可以对应上服务端的一些会话的相关信息，比如用户的登录状态。
* 如果没有客户端的Cookie，Session是无法进行身份验证的。
* 当服务端从单体应用升级为分布式之后，cookie+session这种机制要怎么扩展?
  * session黏贴: 在负载均衡中，通过一个机制保证同一个客户端的所有请求都会转发到同一个tomcat实例当中。
    * 问题:当这个tomcat实例出现问题之后，请求就会被转发到其他实例，这时候用户的session信息就丢了。
  * 2、session复制:当一个tomcat实例上保存了session信息后，主动将session 复制到集群中的其他实例。
    * 问题: 复制是需要时间的，在复制过程中，容易产生session信息丢失。
  * 3、session共享: 就是将服务端的session信息保存到一个第三方中，比如Redis

![1725545548779](cookie%E5%92%8Csession.assets/1725545548779.png)

* 报文自动注册
* 设备编号，设备标签

![1725546210354](cookie%E5%92%8Csession.assets/1725546210354.png)

![1725546323717](cookie%E5%92%8Csession.assets/1725546323717.png)

报警时间记录。五分钟不能报两次

es的geo  ，报送频率很高（infludb）

![1725548660378](cookie%E5%92%8Csession.assets/1725548660378.png)

![1725548719500](cookie%E5%92%8Csession.assets/1725548719500.png)

![1725548743593](cookie%E5%92%8Csession.assets/1725548743593.png)

![1725548797441](cookie%E5%92%8Csession.assets/1725548797441.png)





项目的初步介绍：

项目描述：利用物联网技术设计了一套照护系统。该系统旨在自动进行健康数据及居住环境的监测与记录，以实现智能化的照护，从而减少护理人员工作量，提高护理人员的工作效率。

技术栈：本系统分为硬件设计和软件设计部分。硬件设计采用STM32F103ZET6作为控制核心，集成了多个传感器模块。软件设计采用SpringCloud Alibaba+SSM+SpringSecurity+JWT+rocketMQ+Redis+个推Api+百度地图API+Nginx+oauth2+MySQL+LayUI+Uniapp+Echarts+MinIO+xxI-job+elasticsearch。

功能：体温测量功能、手势识别功能、摄像头采样及人脸对比功能、环境温湿度监控功能、滴液监测功能、照护呼叫功能、语音查询功能。

模块：监控模块（监控数据）、呼叫管理、系统管理，

#####数据安全保证方案

* 硬件采集数据，通过发布订阅的方式激活设备，激活id为激活日期（精确到秒）+设备的mac，硬件可以通过按键调整TFT显示屏的报警阈值，也可以通过网页下发的方式接收信息。

* 硬件传感器如果不工作，则控制核心获取不到数据，向服务器发送设备经纬度和异常缺失字段，此时维护一个数据库，如果连续超过3次不工作或者一个月总数超过50次不工作，则进入维护订单。

* 消息确认双检测：MQ消息确认机制，前端发送时间戳，比较每次时间戳的间隔+网络延迟。

* 服务器发送信息，硬件核心不工作，此时无法发布消息，服务端定时扫描任务。对于无法工作的进入到数据库寻找经纬度维护。

* 摄像头使用ov7670，发送到minio。



问题一：elasticsearch怎么保证和mysql数据同步

* 方案一：同步调用，在微服务中更新mysql的语句后更新elasticsearch，简单但是耦合度高
* 方案二：异步调用，发送到mq，事件监听mq。低耦合，依赖mq
* 方案三：监听binlog，完全解除服务间耦合。开启binlog增加数据库负担、实现复杂度高
  * 原理：canal 模拟 MySQL slave 的交互协议，伪装自己为 MySQL slave ，向 MySQL master 发送 dump 协议MySQL master 收到 dump 请求，开始推送 binary log 给 slave (即 canal )canal 解析 binary log 对象(原始为 byte 流)

问题二：redis和mysql的双写一致性怎么保证

* 三个经典的缓存模式
  * 方案一：旁路缓存。读的时候，先读缓存，缓存命中的话，直接返回数据。缓存没有命中的话，就去读数据库，从数据库取出数据，放入缓存后，同时返回响应。更新的时候，先更新数据库，然后再删除缓存。 
  * 方案二：读写穿透，一般用于秒杀
  * 方案三：异步缓存写入： 只更新缓存，不直接更新数据库，通过批量异步的方式来更新数据库 
* 3种方案保证数据库与缓存的一致性（ ***缓存是通过牺牲强一致性来提高性能的\*。我们只能保证弱一致性和最终一致性** ）
  *  如果有写操作的时候，「先操作数据库，再操作缓存」 。延时双删策略。为了保证删除成功（使用队列也行，重复删除，16次后进入死信队列，去监听死信队列，然后进行自己的业务上的逻辑）， 使用binlog异步删除 
  *  可以使用阿里的canal将binlog日志采集发送到MQ队列里面，然后编写一个简单的缓存删除消息者订阅binlog日志，根据更新log删除缓存，并且通过ACK机制确认处理这条更新log，保证数据缓存一致性 
* 三级缓存
  * nginx带一个 三级
  * 进程中一个
  * redis一个 二级
* MQ的数据不丢失， 一致性问题、

如何保证消息不被重复消费、如何保证消息可靠性传输等 



自己觉得有什么问题

* 硬件数据确保不丢失
  * 警报事件发送同步消息，要求同步确认
  * 平常数据异步确认
  * 温度数据多个传感器批量发送（也可以使用tag标签单独发送）
* 稳定性和异常检测
* 队列信息太多，mysql难消费

硬件的数据是一定时间一起来，不是慢慢来：senmtinal选择排队等待，而不是直接拒接，和慢慢预热

熔断策略： **慢调用比例** 

![1726135778239](cookie%E5%92%8Csession.assets/1726135778239.png)

 理想 作业帮 饿了么 捜狐 贝壳找房  维信诺  星际悦动  九号公司 拓竹科技 北森 博思软件  喜马拉雅  网易有道 小鹏汽车（搜java，职位要求有个mqtt） 菜鸟集团  高德  三七互娱  度小满  海悟集团  联营医疗 联合飞机    宇视科技  迪普科技  科华技术 柠檬微趣  **浩鲸科技 万得** 海信集团  奇安信  货拉拉  宇视  叠纸游戏

 理想 作业帮  捜狐 贝壳找房    星际悦动  九号公司 拓竹科技 北森 博思软件  喜马拉雅  

 网易有道 小鹏汽车（搜java，职位要求有个mqtt）**浩鲸科技 万得** 海信集团   货拉拉 奇安信  菜鸟集团  高德  三七互娱  度小满  海悟集团  联营医疗 联合飞机    宇视科技  迪普科技  科华技术 柠檬微趣   宇视  叠纸游戏

兴业银行[兴业招聘官网 (cib.com.cn)](https://job.cib.com.cn/#/createResume?isWrite=N&historyPath=%2FpositionDetails%2F1016354301425111040&positionId=1016354301425111040&resumeModelId)

长虹集团校园招聘

大智慧

比亚迪  华橙网络

|              公司               |                           投递链接                           |
| :-----------------------------: | :----------------------------------------------------------: |
|            天猫养车             |                 tmyczp@list.alibaba-inc.com                  |
|            影子科技             | [广州影子科技有限公司 (zhiye.com)](https://yingzi.zhiye.com/jobs?queryId=11f1867d-9c38-4b08-94fe-353398a3e6f7) |
|              哈罗               | [校园招聘-哈啰 (zhiye.com)](https://hellobike.m.zhiye.com/#/jobs?jc=2) |
|                                 | [西安纽扣软件科技有限公司 (xinrenxinshi.com)](https://s.xinrenxinshi.com/recruitGate/detail#/ey=1CF1E65B891E736DD01C9BAACE2C&jobId=681c9326afe14607afd6e87bf5f9844e) |
|            中兴新云             | <img src="cookie%E5%92%8Csession.assets/image-20241009103235675.png" alt="image-20241009103235675" style="zoom:25%;" /> |
| 苏州苏高新数字科技有<br/>限公司 |                    yawen.tao@morelinks.cn                    |
|            盒马科技             | <img src="cookie%E5%92%8Csession.assets/image-20241009104658807.png" alt="image-20241009104658807" style="zoom: 80%;" /> |
|              虎牙               | [虎牙直播-校园招聘 (mokahr.com)](https://app.mokahr.com/campus_apply/huya/4112#/job/3bc824bd-b151-432d-aac3-2ddf120671ce) |
|              华硕               | [华硕科技（苏州）有限公司 (zhiye.com)](https://asustek.zhiye.com/campus/detail?jobAdId=221c40cf-37fe-4dd0-97fd-caed3d7b12ea) |
|              海康               | [校园招聘 (hikvision.com)](https://campushr.hikvision.com/school?schoolType=nozxf&activeTab=0#) |
|            大华股份             | [大华股份招聘官网 (dahuatech.com)](https://job.dahuatech.com/#/CampusPosition?id=11) |
|            中国平安             | [中国平安校园招聘 (pingan.com)](https://campus.pingan.com/positionDetail?positionId=22951a227d14314788e3a48e7257e83f) |
|            海柔创新             | [海柔创新 (zhiye.com)](https://hairobotics.zhiye.com/campus/detail?jobAdId=bbbce8f5-09b7-4e85-8ed5-e7bd393bd667) |
|            锐明技术             | [校招职位 (zhiye.com)](https://streamax.zhiye.com/campus/jobs?1=[{"id"%3A"1"%2C"label"%3A"研发设计类"}]) |
|                                 | [华诺星空技术股份有限公司 (novasky.cn)](http://www.novasky.cn/Campus/index.aspx?page=2) |
|            科远智慧             |             https://sciyon.zhiye.com/campus/jobs             |
|              途牛               | [校招职位 (zhiye.com)](https://tuniu.zhiye.com/campus/jobs)  |
|                                 |      https://mp.weixin.qq.com/s/b_zVUkNV213a9cjMeb7hCQ       |



10月10日 10点：携程笔试
