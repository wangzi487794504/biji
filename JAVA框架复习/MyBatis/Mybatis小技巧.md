#### Mybatis小技巧

* ### #{ }和${ }

  * \#{}：先编译sql语句，再给占位符传值，底层是PreparedStatement实现。可以防⽌sql注⼊，⽐较常⽤。他会给你加一个单引号
  * ${}：先进⾏sql语句拼接，然后再编译sql语句，底层是Statement实现。存在sql注⼊现象。只有在需要进⾏sql语句关键字拼接的情况下才会⽤到。
    * 常用于传升序降序关键字
    * 向SQL语句当中拼接表名，就需要使用${}现实业务当中，可能会存在分表存储数据的情况。因为一张表存的话，数据量太大。查询效率比较低。可以将这些数据有规律的分表存储，这样在查询的时候效率就比较高。因为扫描的数据量变少了。批量删除
    * 也常用于批量删除的SQL语句有两种写法:因为不能有单引号，而#{}会自动加上单引号
    * 第一种or:delete from t_car where id=1 or id=2 or id=3;
    * 第二种int:delete from t_car where id in(1,2,3);





* 模糊查询

  * select *from t_car where brand like'%奔驰多%'，elect *from t_car where brand like'%{#brand}%'会报错，因为它已经被单引号包裹了
    select *from t_car where brand like'%比亚迪%'
  *  name like '%${name}%' 
  * name like concat('%',*#{name},'%')* 
  * name like "%"*#{name}"%"* 

* 别名

  ```xml
      <typeAliases>
  <!--        type是给哪一个属性起别名，alias是别名名字，不区分大小写-->
          <typeAlias type="wang.zi.jie.bean.Car" alias="xxx"></typeAlias>
      </typeAliases>
  ```

  * namespace没有别名一说，必须写全限定类名

  * 如果省略alias，那别名就是类名，即Car

  * typeAliases还有一个package子标签。适用与类很多的文件

    ```xml
        <typeAliases>
    <!--        他会自动给bean包下所有的类起别名，别名就是它的类名-->
            <package name="wang.zi.jie.bean"/>
        </typeAliases>
    ```

* <**mappers**>

  * ```xml
    <!--
        mapper的三个属性：
            resource：从类路径中加载
            url：从指定的全限定资源路径中加载
            class：使⽤映射器接⼝实现类的完全限定类名
            package：将包内的映射器接⼝实现全部注册为映射器
    -->
    <mapper resource="" class="" url=""/>
    <!--
    	package：将包内的映射器接⼝实现全部注册为映射器
    	使用此方法需要将SqlMapper.xml文件和同名接口放在同一个目录下
    -->
    <package name="com.ziv.mybatis.mapper"/>
    ```

  * <mapper resource="CarHapper.xml"/>求类的根路径下必须有:CarMapper.xml

  * <mapper url="file:///d:/carHapper.xml"/> 求在d:/下有CarMapper.xml文件

  * **<mapper class=”全限定接口名，带有包名"/>class:这个位置提供的是mapper接日的全限定接口名，必须带有包名的。**

  * 思考:mapper标签的作用是指定SqlMapper.xml文件的路径，指定接口名有什么用呢?

    * **<mapper class:"con.powernode.mybatis.mapper.CarMapper"/>如果你class指定是:com.powernode.mybatis.mapper.CarHapper刚么mybatis框架会自动去com/powernodemybatis/mapper目录下找CarMapper.xml文件。**

      ![1709641315724](Mybatis%E5%B0%8F%E6%8A%80%E5%B7%A7.assets/1709641315724.png)

  * 注意：resource目录下没有包，所以你也要通过目录建

  * **但本质上都是同一个文件夹在编译后**

    ![1709641896050](Mybatis%E5%B0%8F%E6%8A%80%E5%B7%A7.assets/1709641896050.png)

  * ==package：将包内的映射器接⼝实现全部注册为映射器==

    ```xml
    <!-- 将包内的映射器接口实现全部注册为映射器 -->
    <mappers>
      <package name="com.powernode.mybatis.mapper"/>
    </mappers>
    ```

    

* 自动获取主键

  ```xml
  <!--
      useGeneratedKeys="true" 使用自动生成的主键值
      keyProperty="id" 指定主键值赋值给对象的哪个属性。这个表示将自动生成的主键值赋值给Car的id属性
  -->
  <insert id="insertCarUseGeneratedKey" useGeneratedKeys="true" keyProperty="id">
      insert into t_car(id, car_num, brand, guide_price, produce_time, car_type)
      values (null, #{carNum}, #{brand}, #{guidePrice}, #{produceTime}, #{carType})
  </insert>
  ```

  

