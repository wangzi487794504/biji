##### mybatis缓存

* 缓存的作⽤：通过减少IO的⽅式，来提⾼程序的执⾏效率。
* mybatis的缓存：将select语句的查询结果放到缓存（内存）当中，下⼀次还是这条select语句的话，直接从缓存中取，不再查数据库。⼀⽅⾯是减少了IO。另⼀⽅⾯不再执⾏繁琐的查找算法。效率⼤⼤提升。
* mybatis缓存包括：
  - ⼀级缓存：将查询到的数据存储到SqlSession中。
  - ⼆级缓存：将查询到的数据存储到SqlSessionFactory中。
  - 或者集成其它第三⽅的缓存：⽐如EhCache【Java语⾔开发的】、Memcache【C语⾔开发的】等。



* 一级缓存

  *  ⼀级缓存默认是开启的。不需要做任何配置。

  * 原理：只要使⽤同⼀个SqlSession对象执⾏同⼀条SQL语句，就会⾛缓存

    ```java
    @Test
    public void testSelectBy(){
        SqlSession sqlSession= SqlSessionUntil.getSqlSession();
        ClazzMapper mapper = sqlSession.getMapper(ClazzMapper.class);
        Clazz clazz = mapper.selectByCidStep(1000);
        System.out.println(clazz);
        ClazzMapper mapper1=sqlSession.getMapper(ClazzMapper.class);
        Clazz clazz1 = mapper1.selectByCidStep(1000);
    
        sqlSession.commit();
        sqlSession.close();
    } 
    ```

  * **它的作用域只在同一个session中，如果是不同的session，就失效了**

  * 缓存失效

    * 执行了sqlSession的clearCache()方法
    * 执行了INSERT或DELETE或UPDATE语句

  * 什么情况不走缓存

    * 第⼀种：不同的SqlSession对象。
    * 第⼆种：查询条件变化了。

* 二级缓存

  * ⼆级缓存的范围是SqlSessionFactory。

  * 使⽤⼆级缓存需要具备以下⼏个条件：

    1. 全局性地开启或关闭所有映射器配置⽂件中已配置的任何缓存。默认就是true，⽆需设置。即默认开启

       ```xml
       <setting name="cacheEnabled" value="true">
       ```

    2.  在需要使⽤⼆级缓存的SqlMapper.xml⽂件中添加配置： 

       ```xml
       <!--默认情况下，二级缓存是开启的。
       只要在对应的SqlMapperx.xml文件中添加如下标签，就表示此文件中使用二级缓存-->
       <cache/>
       
       ```

    3. 使⽤⼆级缓存的实体类对象必须是可序列化的，也就是必须实现java.io.Serializable接⼝

    4.  SqlSession对象关闭或提交之后，⼀级缓存中的数据才会被写⼊到⼆级缓存当中。此时⼆级缓存才可⽤ 

       ```java
           @Test
           public void testSelectBy() throws IOException {
               SqlSessionFactory factory=new SqlSessionFactoryBuilder().build(Resources.getResourceAsStream("mybatis-config.xml"));
               SqlSession sqlSession= factory.openSession();
               SqlSession sqlSession2= factory.openSession();
               ClazzMapper mapper = sqlSession.getMapper(ClazzMapper.class);
               ClazzMapper mapper1=sqlSession2.getMapper(ClazzMapper.class);
       
               Clazz clazz = mapper.selectByCidStep(1000);
               //此时仍然在sqlSession的一级缓存中
               System.out.println(clazz);
               Clazz clazz1 = mapper1.selectByCidStep(1000);
               //此时仍然在sqlSession2的一级缓存中
               //如果不关闭sqlsession对象的话，二级缓存中还是没有数据的
               //运行到这一行代码后，sqlSession的一级缓存写入到二级缓存中
               sqlSession.close();
               sqlSession2.close();
           }
       ```

    5. 此时命中率是0

       ![1709813840816](Mybatis%E7%BC%93%E5%AD%98.assets/1709813840816.png)

       ```java
           @Test
           public void testSelectBy() throws IOException {
               SqlSessionFactory factory=new SqlSessionFactoryBuilder().build(Resources.getResourceAsStream("mybatis-config.xml"));
               SqlSession sqlSession= factory.openSession();
               SqlSession sqlSession2= factory.openSession();
               ClazzMapper mapper = sqlSession.getMapper(ClazzMapper.class);
               ClazzMapper mapper1=sqlSession2.getMapper(ClazzMapper.class);
       
               Clazz clazz = mapper.selectByCidStep(1000);
               //此时仍然在sqlSession的一级缓存中
               System.out.println(clazz);
               //运行到这一行代码后，sqlSession的一级缓存写入到二级缓存中
               sqlSession.close();
               Clazz clazz1 = mapper1.selectByCidStep(1000);
               //如果不关闭sqlsession对象的话，二级缓存中还是没有数据的
               sqlSession2.close();
           }
       
       ```

       ![1709813707827](Mybatis%E7%BC%93%E5%AD%98.assets/1709813707827.png)

* 肯定是优先最近原则，一级缓存优先级高

* 二级缓存的相关配置

  * eviction：指定从缓存中移除某个对象的淘汰算法。默认采⽤LRU策略。
    * a. LRU：Least Recently Used。最近最少使⽤。优先淘汰在间隔时间内使⽤频率最低的对象。(其实还有⼀种淘汰算法LFU，最不常⽤。)
    * b. FIFO：First In First Out。⼀种先进先出的数据缓存器。先进⼊⼆级缓存的对象最先被淘汰。
    * c. SOFT：软引⽤。淘汰软引⽤指向的对象。具体算法和JVM的垃圾回收算法有关。
    * d. WEAK：弱引⽤。淘汰弱引⽤指向的对象。具体算法和JVM的垃圾回收算法有关。
  * flushInterval：
    * a. ⼆级缓存的刷新时间间隔。单位毫秒。如果没有设置。就代表不刷新缓存，只要内存⾜够⼤，⼀直会向⼆级缓存中缓存数据。除⾮执⾏了增删改。
  * readOnly：
    * a. true：多条相同的sql语句执⾏之后返回的对象是共享的同⼀个。性能好。但是多线程并发可能会存在安全问题。
    * b. false：多条相同的sql语句执⾏之后返回的对象是副本，调⽤了clone⽅法。性能⼀般。但安全。
  * size：
    * a. 设置⼆级缓存中最多可存储的java对象数量。默认值1024。

* Mybatis集成EhCache

  * 集成EhCache是为了代替mybatis⾃带的⼆级缓存。⼀级缓存是⽆法替代的。

  * mybatis对外提供了接⼝，也可以集成第三⽅的缓存组件。⽐如EhCache、Memcache等。都可以。

  * EhCache是Java写的。Memcache是C语⾔写的。所以mybatis集成EhCache较为常⻅，按照以下步骤操作，就可以完成集成：

    *  第⼀步：引⼊mybatis整合ehcache的依赖。 

      ```xml
      <!--mybatis集成ehcache的组件-->
      <dependency>
          <groupId>org.mybatis.caches</groupId>
          <artifactId>mybatis-ehcache</artifactId>
          <version>1.2.2</version>
      </dependency>
      <!--ehcache需要slf4j的⽇志组件,log4j不好使-->
      <dependency>
          <groupId>ch.qos.logback</groupId>
          <artifactId>logback-classic</artifactId>
          <version>1.2.11</version>
          <scope>test</scope>
      </dependency>
      
      ```

    * 第⼆步：在类的根路径下新建echcache.xml⽂件，并提供以下配置信息。

      ```xml
      <?xml version="1.0" encoding="UTF-8"?>
      <ehcache xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
               xsi:noNamespaceSchemaLocation="http://ehcache.org/ehcache.xsd"
               updateCheck="false">
          <!--磁盘存储:将缓存中暂时不使⽤的对象,转移到硬盘,类似于Windows系统的虚拟内存-->
          <diskStore path="e:/ehcache"/>
      
          <!--defaultCache：默认的管理策略-->
          <!--eternal：设定缓存的elements是否永远不过期。如果为true，则缓存的数据始终有效，如果为false那么还要根据timeToIdleSeconds，timeToLiveSeconds判断-->
          <!--maxElementsInMemory：在内存中缓存的element的最⼤数⽬-->
          <!--overflowToDisk：如果内存中数据超过内存限制，是否要缓存到磁盘上-->
          <!--diskPersistent：是否在磁盘上持久化。指重启jvm后，数据是否有效。默认为false-->
          <!--timeToIdleSeconds：对象空闲时间(单位：秒)，指对象在多⻓时间没有被访问就会失效。只对eternal为false的有效。默认值0，表示⼀直可以访问-->
          <!--timeToLiveSeconds：对象存活时间(单位：秒)，指对象从创建到失效所需要的时间。只对eternal为false的有效。默认值0，表示⼀直可以访问-->
          <!--memoryStoreEvictionPolicy：缓存的3 种清空策略-->
          <!--FIFO：first in first out (先进先出)-->
          <!--LFU：Less Frequently Used (最少使⽤).意思是⼀直以来最少被使⽤的。缓存的元素有⼀个hit 属性，hit 值最⼩的将会被清出缓存-->
          <!--LRU：Least Recently Used(最近最少使⽤). (ehcache 默认值).缓存的元素有⼀个时间戳，当缓存容量满了，⽽⼜需要腾出地⽅来缓存新的元素的时候，那么现有缓存元素中时间戳离当前时间最远的元素将被清出缓存-->
          <defaultCache eternal="false" maxElementsInMemory="1000" overflowToDisk="false" diskPersistent="false"
                        timeToIdleSeconds="0" timeToLiveSeconds="600" memoryStoreEvictionPolicy="LRU"/>
      
      </ehcache>
      
      ```

    *  第三步：修改SqlMapper.xml⽂件中的标签，添加type属性。 

      ```xml
      <cache type="org.mybatis.caches.ehcache.EhcacheCache"/>
      
      ```

      

