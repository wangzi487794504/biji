#### MySQL优化

* MySQL数据库的优化手段通常包括但不限于：

  - SQL查询优化：这是最低成本的优化手段，通过优化查询语句、适当添加索引等方式进行。并且效果显著。
  - 库表结构优化：通过规范化设计、优化索引和数据类型等方式进行库表结构优化，需要对数据库结构进行调整和改进
  - 系统配置优化：根据硬件和操作系统的特点，调整最大连接数、内存管理、IO调度等参数
  - 硬件优化：升级硬盘、增加内存容量、升级处理器等硬件方面的投入，需要购买和替换硬件设备，成本较高

* 通过以下命令可以查看数据库的基本情况

  * 这些结果反映了从 MySQL 服务器启动到当前时刻，所有的 SELECT 查询总数。对于 MySQL 性能优化来说，通过查看 `Com_select` 的值可以了解 SELECT 查询在整个 MySQL 服务期间所占比例的情况：

    - 如果 `Com_select` 次数过高，可能说明查询表中的每条记录都会返回过多的字段。
    - 如果 `Com_select` 次数很少，同时insert或delete或update的次数很高，可能说明服务器运行的应用程序过于依赖写入操作和少量读取操作。

    ```sql
    show global status like 'Com_select';
    show global status like 'Com_insert';
    show global status like 'Com_delete';
    show global status like 'Com_update';
    
    show global status like 'Com___';
    ```

    ![1711673885257](Mysql%E4%BC%98%E5%8C%96.assets/1711673885257.png)

  * 也可以使用模糊查询，查询全部

    ```sql
    show global status like 'Com_______';
    ```

    ![1711674064351](Mysql%E4%BC%98%E5%8C%96.assets/1711674064351.png)

* 慢查询设置

  * 慢查询日志文件可以将查询较慢的DQL语句记录下来，便于我们定位需要调优的select语句。

  * 通过以下命令查看慢查询日志功能是否开启（默认关闭）：

    ```sql
    show variables like 'slow_query_log';
    ```

  * 慢查询日志功能默认是关闭的。请修改my.ini文件来开启慢查询日志功能，在my.ini的[mysqld]后面添加如下配置

    ![image.png](Mysql%E4%BC%98%E5%8C%96.assets/image.png)

    * slow_query_log=1表示开启慢查询日志功能，long_query_time=3表示：只要SELECT语句的执行耗时超过3秒则将其记录到慢查询日志中。
    * 重启mysql服务。再次查看是否开启慢查询日志功能

  * 尝试执行一个慢查询语句，时间超过三秒的

    ```sql
    select empno,ename,sleep(4) from emp where ename='smith';
    ```

    

    * 慢查询日志文件默认存储在：C:\dev\mysql-8.0.36-winx64\data 目录下，默认的名字是：计算机名-slow.log
    * 通过该文件可以清晰的看到哪些DQL语句属于慢查询

* show profiles

  * 通过show profiles可以查看一个SQL语句在执行过程中具体的耗时情况。帮助我们更好的定位问题所在。

  * 查看当前数据库是否支持 profile操作：

    ```sql
    select @@have_profiling;
    ```

  * 查看profiling是否开启，在navicat for mysql默认是开启的，在dos默认是关闭的

    ```sql
     select @@profiling;
    ```

  * 开启 profiling

    ```sql
    set profiling=1;
    ```

  * 查看所有语句的耗时情况

    ```sql
    show profiles;
    ```

    * 举例

      ```sql
      select empno,ename from emp;
      select empno,ename from emp where empno=7369;
      select count(*) from emp;
      show profiles;
      ```

      ![1711681155056](Mysql%E4%BC%98%E5%8C%96.assets/1711681155056.png)

  * 查询具体某一句

    ```sql
    show profile for query 19;
    ```

  * 查看过程中cpu的使用情况

    ```sql
    show profile cpu for query 4;
    ```

* 查询explain

  * explain命令可以查看一个DQL语句的执行计划，根据执行计划可以做出相应的优化措施。提高执行效率。

    ```sql
    explain select * from emp where empno=7369;
    ```

    * select_type:反映了mysql查询语句的类型。常用值包括：

      - SIMPLE：表示查询中不包含子查询或UNION操作。这种查询通常包括一个表或是最多一个联接（JOIN）
      - PRIMARY：表示当前查询是一个主查询。（主要的查询）
      - UNION：表示查询中包含UNION操作
      - SUBQUERY：子查询
      - DERIVED：派生表（表示查询语句出现在from后面）

    * table：反映了这个查询操作的是哪个表

    * type:反映了查询表中数据时的访问类型，常见的值：

      1. NULL：效率最高，一般不可能优化到这个级别，只有查询时没有查询表的时候，访问类型是NULL。例如：select 1;
      2. system：通常访问系统表的时候，访问类型是system。一般也很难优化到这个程序。
      3. const：根据主键或者唯一性索引查询，索引值是常量值时。explain select * from emp where empno=7369;  empno是主键，7369是常量
      4. eq_ref：根据主键或者唯一性索引查询。索引值不是常量值。
      5. ref：使用了非唯一的索引进行查询。
      6. range：使用了索引，扫描了索引树的一部分。
      7. index：表示用了索引，但是也需要遍历整个索引树。
      8. all：全表扫描

      * 效率最高的是NULL，效率最低的是all，从上到下，从高到低。

      ```sql
    #查看type级别
      explain select * from emp where ename='smith';
    ```
  
    ![1711764942017](Mysql%E4%BC%98%E5%8C%96.assets/1711764942017.png)
  
    * 可以看到这个级别是all
  
    * 添加一个索引，可以发现级别就到了ref
  
      ```sql
        #添加一个索引
        create index inx_emp_ename on emp(ename);
        ```

        ![1711765152393](Mysql%E4%BC%98%E5%8C%96.assets/1711765152393.png)

    * possible_keys：这个查询可能会用到的索引

    * key：实际用到的索引
  
    * key_len：反映索引中在查询中使用的列所占的总字节数

    * rows：查询扫描的预估计行数。

    * Extra：给出了与查询相关的额外信息和说明。这些额外信息可以帮助我们更好地理解查询执行的过程。
  
  * id反映出一条select语句执行顺序，id越大优先级越高。id相同则按照自上而下的顺序执行。
  
    ```sql
    explain select e.ename,d.dname from emp e join dept d on e.deptno=d.deptno join salgrade s on e.sal between s.losal and s.hisal;
    ```
  
    ![1711681956472](Mysql%E4%BC%98%E5%8C%96.assets/1711681956472.png)
  
    * 优先级一样，采用自上而下的执行顺序
  
    ```sql
    explain select e.ename,d.dname from emp e join dept d on e.deptno=d.deptno where e.sal=(select sal from emp where ename='ford');
    ```
  
    ![1711682034806](Mysql%E4%BC%98%E5%8C%96.assets/1711682034806.png)
  
    * 子查询的优先级高



##### 索引优化

* sql脚本初始化到数据库中（初始化100W条记录）：t_vip.sql根据id查询（id是主键，有索引）：

  * 首先根据id查询（id有索引），这个id对应的name是dae943da

    ```sql
    select *from t_vip where id=900000;
    ```

    ![1711766742442](Mysql%E4%BC%98%E5%8C%96.assets/1711766742442.png)

  * 再根据name查询

    ```sql
    select *from t_vip where name='dae943da';
    ```

    <img src="Mysql%E4%BC%98%E5%8C%96.assets/1711766833332.png" alt="1711766833332" style="zoom: 80%;" />

  * 此时给name添加一个索引

    ```sql
    create index idx_uservip_name on t_vip(name);
    select *from t_vip where name='dae943da';
    ```







* 最左前缀原则

  * 先创建一张表

    ```sql
    create table t_customer(
    	id int primary key auto_increment,
    	name varchar(255),
    	age int,
    	gender char(1),
    	email varchar(255)
    );
    ```

  * 为我们添加数据

    ```sql
    insert into t_customer values(null, 'zhangsan', 20, 'M', 'zhangsan@123.com');
    insert into t_customer values(null, 'lisi', 22, 'M', 'lisi@123.com');
    insert into t_customer values(null, 'wangwu', 18, 'F', 'wangwu@123.com');
    insert into t_customer values(null, 'zhaoliu', 22, 'F', 'zhaoliu@123.com');
    insert into t_customer values(null, 'jack', 30, 'M', 'jack@123.com');
    ```

  * 添加一个复合索引

    ```sql
    create index idx_name_age_gender on t_customer(name,age,gender);
    ```

    **最左前缀原则：当查询语句条件中包含了这个复合索引最左边的列 name 时（不是name的位置在最左边，而是必须有name这个字段，其他两个字段不会触发这个索引），此时索引才会起作用。**

  * 验证1：

    ```sql
    #这个是完全使用索引，索引长度777
    explain select * from t_customer where name='zhangsan' and age=20 and gender='M';
    ```

    ![1711768288074](Mysql%E4%BC%98%E5%8C%96.assets/1711768288074.png)

  * 验证2：

    ```sql
    #这个是部分使用索引，索引长度为773，说明gender在索引中占4个字节
    explain select * from t_customer where name='zhangsan' and age=20;
    ```

    ![1711768757762](Mysql%E4%BC%98%E5%8C%96.assets/1711768757762.png)

  * 验证3：

    ```sql
    #这个也是局部索引，索引长度为768，说明age为5个字节
    explain select * from t_customer where name='zhangsan';
    ```

  * 验证4：之和有没有name有关，和位置无关

    ```sql
    explain select * from t_customer where age=20 and gender='M' and name='zhangsan';
    ```

    ![1711769102510](Mysql%E4%BC%98%E5%8C%96.assets/1711769102510.png)

  * 验证5：

    ```sql
    #不遵守最左原则
    explain select * from t_customer where gender='M' and age=20;
    ```

    ![1711769268992](Mysql%E4%BC%98%E5%8C%96.assets/1711769268992.png)

  * 验证6

    ```sql
    #部分使用索引，但是只能使用name的,gender不可以使用，因为没有age，导致gender无法使用索引
    explain select * from t_customer where name='zhangsan' and  gender='M';
    ```

    ![1711769637081](Mysql%E4%BC%98%E5%8C%96.assets/1711769637081.png)

  * 验证7：当使用范围查找的时候，范围条件右侧的列不会使用索引

    ```sql
    #age有了范围判断,age和后面的索引就都失效了
    explain select * from t_customer where name='zhangsan' and age>20 and gender='M';
    ```

    ![1711770567678](Mysql%E4%BC%98%E5%8C%96.assets/1711770567678.png)

  * 验证8：当使用范围查找的时候，范围条件只要有等号，右侧的列正常使用索引

    ```sql
    explain select * from t_customer where name='zhangsan' and age>=20 and gender='M';
    ```

    ![1711770631772](Mysql%E4%BC%98%E5%8C%96.assets/1711770631772.png)

* 索引失效的情况

  * 有一张表

    ```sql
    create table t_emp(
      id int primary key auto_increment,
      name varchar(255),
      sal int,
      age char(2)
    );
    ```

  * 数据和索引

    ```sql
    insert into t_emp values(null, '张三', 5000,'20');
    insert into t_emp values(null, '张飞', 4000,'30');
    insert into t_emp values(null, '李飞', 6000,'40');
    create index idx_t_emp_name on t_emp(name);
    create index idx_t_emp_sal on t_emp(sal);
    create index idx_t_emp_age on t_emp(age);
    ```

    

  * 索引列参加了运算，索引失效

    ```sql
    explain select * from t_emp where sal > 5000;#这种会使用
    explain select * from t_emp where sal*10 > 50000;#这种会失效
    ```

    

  * 索引列进行模糊查询时以** % 开始的**，索引失效

    ```sql
    explain select * from t_emp where name like '张%';#这个不会失效
    explain select * from t_emp where name like '%飞';#这个会失效
    explain select * from t_emp where name like '%飞%';#这个也会失效
    ```

    

  * 索引列是字符串类型，但查询时省略了单引号，索引失效

    ```sql
    #age为字符串类型
    explain select * from t_emp where age='20';#这个不会失效
    explain select * from t_emp where age=20;#这个会失效
    ```

    

  * 查询条件中有or，只要有未添加索引的字段，索引失效

    ```sql
    alter table t_emp drop index idx_t_emp_sal;
    explain select * from t_emp where name='张三' or sal=5000;#这个会失效
    ```

    

  * 当查询的符合条件的记录在表中占比较大，索引失效

    * 赋值一张新表,并给sal添加索引

      ```sql
      create table emp2 as select * from emp;
      alter table emp2 add index idx_emp2_sal(sal);
      ```

    * 验证1：因为基本都是大于800的，所以不会使用索引

      ```sql
      explain select * from emp2 where sal > 800;
      ```

      ![1711775305476](Mysql%E4%BC%98%E5%8C%96.assets/1711775305476.png)

    * 验证二：当符合记录的占比较少，会使用索引

      ```sql
      explain select * from emp2 where sal > 2000;
      ```

      ![1711775393418](Mysql%E4%BC%98%E5%8C%96.assets/1711775393418.png)

  * 关于is null和is not null的索引失效问题：

    * 给emp2的comm字段添加一个索引将emp2表的comm字段值全部更新为NULL：

      ```sql
      create index idx_emp2_comm on emp2(comm);
      update emp2 set comm=null;
      ```

    * 验证is null走不走索引（**原理还是因为更新为null占得比重比较大**）

      ```sql
      explain select * from emp2 where comm is null;
      ```

      ![1711776419168](Mysql%E4%BC%98%E5%8C%96.assets/1711776419168.png)

    * 此时 is not null就会走索引

      ```sql
      explain select * from emp2 where comm is not null;
      ```

      ![1711776600618](Mysql%E4%BC%98%E5%8C%96.assets/1711776600618.png)

    * 但是数据如果都不是空，结果与上面的相反





* 指定索引

  * 当一个字段上既有单列索引，又有复合索引时，我们可以通过以下的SQL提示来要求该SQL语句执行时采用哪个索引：

    * use index(索引名称)：建议使用该索引，只是建议，底层mysql会根据实际效率来考虑是否使用你推荐的索引。
    * ignore index(索引名称)：忽略该索引
    * force index(索引名称)：强行使用该索引

  * ==当两种索引都有，优先选择复合索引==

  * 建议使用单列索引

    ```sql
    explain select * from t_customer use index(idx_name) where name='zhangsan';
    ```

  * 忽略单例索引

    ```sql
    explain select * from t_customer ignore index(idx_name_age_gender) where name='zhangsan';
    ```

  * 强制使用单例索引

    ```sql
    explain select * from t_customer force index(idx_name) where name='zhangsan';
    ```





* 覆盖索引

  * 覆盖索引强调的是：在select后面写字段的时候，这些字段尽可能是索引所覆盖的字段，这样可以避免回表查询。尽可能避免使用 select *，因为select * 很容易导致回表查询。（本质就是：能在索引上检索的，就不要再次回表查询了。

  * 首先创建一张表，设置索引和查询

    ```sql
    drop table if exists emp3;
    create table emp3 as select * from emp;
    alter table emp3 add constraint emp3_pk primary key(empno);
    create index idx_emp3_ename_job on emp3(ename,job);
    explain select empno,ename,job from emp3 where ename='KING';
    ```

    ![1711778033797](Mysql%E4%BC%98%E5%8C%96.assets/1711778033797.png)

  * 如果查询的字段没有在索引中，就会回表查询

    ```sql
    explain select empno,ename,job,sal from emp3 where ename='KING';
    ```

    ![1711778297531](Mysql%E4%BC%98%E5%8C%96.assets/1711778297531.png)

    * Extra没有显示就说明回表了

  * 面试题

    ```sql
    面试题：t_user表字段如下：id,name,password,realname,birth,email。表中数据量500万条，请针对以下SQL语句给出优化方案：
    select id,name,realname from t_user where name='鲁智深';
    ```

    如果只给name添加索引，底层会进行大量的回表查询，效率较低，建议给name和realname两个字段添加联合索引，这样大大减少回表操作，提高查询效率。

* 前缀索引

  * 如果一个字段类型是varchar或text字段，字段中存储的是文本或者大文本，直接对这种长文本创建索引，会让索引体积很大，怎么优化呢？可以将字符串的前几个字符截取下来当做索引来创建。这种索引被称为前缀索引，例如：

    * 将ename字段的前两个字符当做索引

      ```sql
      drop table if exists emp4;
      create table emp4 as select * from emp;
      create index idx_emp4_ename_2 on emp4(ename(2));
      ```

  * 到底选择前几个字符：对于索引来说，索引值越唯一，唯一性越好，性能越高

    ```sql
    select count(distinct substring(ename,1,前几个字符)) / count(*) from emp4;
    ```

    * 以上查询结果越接近1，表示索引的效果越好。（原理：做索引值的话，索引值越具有唯一性效率越高）

* 单列索引和复合索引怎么选择

  * 当查询语句的条件中有多个条件，建议将这几个列创建为复合索引，因为创建单列索引很容易回表查询。

  * 注意：创建索引时应考虑最左前缀原则，主字段并且具有很强唯一性的字段建议排在第一位

    ```sql
    create index idx_emp_ename_job on emp(ename,job);
    ```

    * ename升序拍，相同的在按照第二个job排

* 索引创建原则

  * 表数据量庞大，通常超过百万条数据。
  * 经常出现在where，order by，group by后面的字段建议添加索引。
  * 创建索引的字段尽量具有很强的唯一性。
  * 如果字段存储文本，内容较大，一定要创建前缀索引。
  * 尽量使用复合索引，使用单列索引容易回表查询。
  * ==如果一个字段中的数据不会为NULL，建议建表时添加not null约束，这样优化器就知道使用哪个索引列更加有效。==
  * 不要创建太多索引，当对数据进行增删改的时候，索引需要重新重新排序。
  * 如果很少的查询，经常的增删改不建议加索引。





##### SQL优化

* order by优化

  * 先创建一张表

    ```sql
    drop table if exists workers;
    
    create table workers(
      id int primary key auto_increment,
      name varchar(255),
      age int,
      sal int
    );
    
    insert into workers values(null, '孙悟空', 500, 50000);
    insert into workers values(null, '猪八戒', 300, 40000);
    insert into workers values(null, '沙和尚', 600, 40000);
    insert into workers values(null, '白骨精', 600, 10000);
    ```

  * explain查看一个带有order by的语句时，，Extra列会显示：using filesort，区别是什么

    * using index:表示使用索引，因为索引是提前排好序的，效率很高
    * using filesort：表示使用文件排序，对表中的数据进行排序，排序是将硬盘的文件数据读取到内存中，在内存中排好序，这个效率是最低的，应该去避免。

  * 当name没有索引时，使用order by

    ```sql
    explain select id,name from workers order by name;
    ```

    ![1711780759832](Mysql%E4%BC%98%E5%8C%96.assets/1711780759832.png)

  * 当添加索引时

    ```sql
    create index ti_name on workers(name);
    explain select id,name from workers order by name;
    ```

    ![1711780863217](Mysql%E4%BC%98%E5%8C%96.assets/1711780863217.png)

  * 如果要通过age和sal两个字段进行排序，最好给age和sal两个字段添加复合索引，不添加复合索引时：按照age升序排，如果age相同则按照sal升序

    ```sql
    create index t_age_sal on workers(age,sal);
    explain select id,age,sal from workers order by age,sal;
    ```

    ![1711783137749](Mysql%E4%BC%98%E5%8C%96.assets/1711783137749.png)

  * 都升序：会反向索引扫描

    ```sql
    explain select id,age,sal from workers order by age desc,sal desc;
    ```

  * 如果一个升序一个降序：就会出现回表

    ```sql
    explain select id,age,sal from workers order by age desc,sal;
    ```

    ![1711783305453](Mysql%E4%BC%98%E5%8C%96.assets/1711783305453.png)

    * 解决办法，创建一个升序，一个降序的索引

      ```sql
      #我在使用时没有效果
      create index t_ageasc_saldesc on workers(age asc,sal desc);
      explain select id,age,sal from workers order by age asc,sal desc;
      ```

  * order by 优化原则总结：

    1. 排序也要遵循最左前缀法则。

    2. 使用覆盖索引。

    3. 针对不同的排序规则，创建不同索引。（如果所有字段都是升序，或者所有字段都是降序，则不需要创建新的索引）

    4. 如果无法避免filesort，要注意排序缓存的大小，默认缓存大小256KB，可以修改系统变量 sort_buffer_size 

       ```sql
       #修改这个变量
       show variables like 'sort_buffer_size';
       ```



* group by优化

  * 创建表，group by在没有索引的情况下查询

    ```sql
    create table empx3 as select * from emp;
    explain select job,count(*) from empx3 group by job;
    ```

    ![1711785161802](Mysql%E4%BC%98%E5%8C%96.assets/1711785161802.png)

    * 他使用了一个临时表，效率较低

  * 使用索引可以提高分组效率

    ```sql
    create index idx_empx_job on empx(job);
    explain select job,count(*) from empx3 group by job;
    ```

    ![1711785739104](Mysql%E4%BC%98%E5%8C%96.assets/1711785739104.png)

  * 再来看看group by是否需要遵守最左前缀法则：给deptno和sal添加复合索引

    ```sql
    create index idx_empx_deptno_sal on empx3(deptno, sal);
    explain select deptno,count(*) from empx3 group by deptno;
    explain select sal, count(*) from empx3 group by sal;#没有使用，所以遵守
    ```

  * 如果将部门编号deptno（复合索引的最左列）添加到where条件中，效率会不会提升：

    ```sql
    explain select sal, count(*) from empx3 where deptno=10 group by sal;
    ```

    ![1711785976289](Mysql%E4%BC%98%E5%8C%96.assets/1711785976289.png)







* limit优化

  * 数据量特别庞大时，取数据时，越往后效率越低，怎么提升？mysql官方给出的解决方案是：使用覆盖索引+子查询的形式来提升效率。

    ![image.png](Mysql%E4%BC%98%E5%8C%96.assets/image-1711786089492.png)

    ![image.png](Mysql%E4%BC%98%E5%8C%96.assets/image-1711786104273.png)

    ![image.png](Mysql%E4%BC%98%E5%8C%96.assets/image-1711786116072.png)

  * 使用覆盖索引id：速度有所提升，然后进行子查询取其他列的数据



* 主键优化

  * 主键设计原则：

    1. 主键值不要太长，==二级索引叶子结点上存储的是主键值，主键值太长，容易导致索引占用空间较大。==
    2. 尽量使用auto_increment生成主键。尽量不要使用`uuid做主键，因为uuid不是顺序插入。它是无序插入`
    3. 最好不要使用业务主键，因为业务的变化会导致主键值的频繁修改，==主键值不建议修改，因为主键值修改，聚集索引一定会重新排序。==
    4. 在插入数据时，主键值最好是顺序插入，不要乱序插入，因为乱序插入可能会导致B+树叶子结点频繁的进行页分裂与页合并操作，效率较低。
       1. 主键值对应聚集索引，插入主键值如果是乱序的，B+树叶子结点需要不断的重新排序，重排过程中还会频繁涉及到**页分裂和页合并**的操作，效率较低。
       2. B+树上的每个节点都存储在页（page）中。==一个页面中存储一个节点。==
       3. MySQL的InnoDB存储引擎==一个页可以存储16KB的数据。==
       4. ==如果主键值不是顺序插入的话，会导致频繁的页分裂和页合并。==在一个B+树中，页分裂和页合并是树的自动调整机制的一部分。当一个页已经满了，再插入一个新的关键字时就会触发页分裂操作，将页中的关键字分配到两个新的页中，同时调整树的结构。相反，当一个页中的关键字数量下降到一个阈值以下时，就会触发页合并操作，将两个相邻的页合并成一个新的页。如果主键值是随机的、不是顺序插入的，那么页的利用率会降低，页分裂和页合并的次数就会增加。由于页的分裂和合并是比较耗时的操作，频繁的分裂和合并会降低数据库系统的性能。因此，为了优化B+树的性能，可以将主键值设计成顺序插入的，这样可以减少页的分裂和合并的次数，提高B+树的性能。在实际应用中，如果对主键值的顺序性能要求不是特别高，也可以采用一些技术手段来减少页分裂和合并，例如B+树分裂时采用“延迟分裂”技术，或者通过调整页的大小和节点的大小等方式来优化B+树的性能。

* insert优化

  * 批量插入：数据量较大时，不要一条一条插入，可以批量插入，当然，建议一次插入数据不超过1000条

    ```sql
    insert into t_user(id,name,age) values (1,'jack',20),(2,'lucy',30),(3,'timi',22);
    ```

  * mysql默认是自动提交事务，只要执行一条DML语句就自动提交一次，因此，当插入大量数据时，建议手动开启事务和手动提交事务。不建议使用数据库事务自动提交机制。

  * 主键值建议采用顺序插入，顺序插入比乱序插入效率高。

  * 超大数据量插入可以考虑使用mysql提供的load指令，load指令可以将csv文件中的数据批量导入到数据库表当中，并且效率很高，过程如下：

    * 在登入数据库输入参数

      ```sql
      mysql --local-infile -uroot -p1234
      ```

    * 开启local_infile功能

      ```sql
      set global local_infile = 1;
      ```

    * 第三步：执行load指令

      ```sql
      use powernode;
      create table t_temp(
        id int primary key,
        name varchar(255),
        password varchar(255),
        birth char(10),
        email varchar(255)
      );
      load data local infile 'E:\\powernode\\05-MySQL高级\\resources\\t_temp-100W.csv' into table t_temp fields terminated by ',' lines terminated by '\n';
      ```

      * 字段采用逗号隔开，行采用\n隔开

* count优化

  * 分组函数count的使用方式：

    - count(主键)

      - 原理：将每个主键值取出，累加

    - count(常量值)

      - 原理：获取到每个常量值，累加（就是行数）

        ```sql
        select  count(1000) from emp;
        ```

        ![1711787441316](Mysql%E4%BC%98%E5%8C%96.assets/1711787441316.png)

    - count(字段)

      - 原理：取出字段的每个值，判断是否为NULL，不为NULL则累加。

    - count(*)

      - 原理：不用取值，底层mysql做了优化，直接统计总行数，效率最高。

    * 结论：如果你要统计一张表中数据的总行数，建议使用 count(*)

  * 注意：

    - 对于InnoDB存储引擎来说，count计数的实现原理就是将表中每一条记录取出，然后累加。如果你想真正提高效率，可以自己使用额外的其他程序来实现，**例如每向表中插入一条记录时，在redis数据库中维护一个总行数，这样获取总行数的时候，直接从redis中获取即可，这样效率是最高的。**
    - 对于MyISAM存储引擎来说，当一个select语句没有where条件时，获取总行数效率是极高的，不需要统计，因为MyISAM存储引擎维护了一个单独的总行数。

* update优化

  * 存储引擎是InnoDB时，表的行级锁是针对索引添加的锁，如果索引失效了，或者不是索引列时，会提升为表级锁。
  * 什么是行级锁？A事务和B事务，开启A事务后，通过A事务修改表中某条记录，修改后，在A事务未提交的前提下，B事务去修改同一条记录时，无法继续，直到A事务提交，B事务才可以继续。
  * 行级锁是对索引列加锁，以上更新语句的where条件是id，id是主键，==当然有索引，所以使用了行级锁，如果索引失效，或者字段上没有索引，则会升级为表级锁==
  * 因此，为了更新的效率，建议update语句中where条件中的字段是添加索引的。

  

  

  

