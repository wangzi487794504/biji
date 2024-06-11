#### 动态SQL

* if标签

  ```xml
      <select id="selectMultiCondition" resultType="car">
          <!--
              if标签中test属性的必须的，值为boolean类型，如果为true则把标签内容拼接到sql语句中，反之不拼接
              test中参数的使用：
                  1.当使用了@Param注解时，则使用@Param注解指定的参数名
                  2.当没有使用@Param注解时，则使用param1 param2 param3 arg0 arg1 arg2
                  3.当使用了pojo类，则使用pojo类的属性名
              在mybatis的动态sql中，不能使用&&，只能使用and
          -->
          <!--为了解决参数为空的问题，在where后面加一个恒成立的语句（1=1），这样就需要第一个if前加一个and，来保证sql语句的正确-->
          select * from t_car where 1=1
          <if test="brand !=null and brand!=''">
            and  brand like "%"#{brand}"%"
          </if>
          <if test="guidePrice !=null and guidePrice!=''">
            and  guide_price > #{guidePrice}
          </if>
          <if test="carType !=null and carType!=''">
              and  car_type > #{carType}
          </if>
      </select>
  ```

  ```java
   List<Car> selectMultiCondition(@Param("brand") String brand, @Param("guidePrice") Double guidePrice, @Param("carType") String carType);
  ```

  

* where标签的作⽤：让where⼦句更加动态智能。

  - 所有条件都为空时，where标签保证不会⽣成where⼦句。

  - ⾃动去除某些条件**前⾯**多余的and或or。

    ```xml
    <select id="selectByMultiConditionWithWhere" resultType="car">
        select * from t_car
        <where>
            <if test="brand != null and brand != ''">
                and brand like "%"#{brand}"%"
            </if>
            <if test="guidePrice != null and guidePrice != ''">
                and guide_price > #{guidePrice}
            </if>
            <if test="carType != null and carType != ''">
                and car_type =#{carType}
            </if>
        </where>
    </select>
    ```

* trim标签

  * trim标签的属性：

    - prefix：在trim标签中的语句前添加内容
    - suffix：在trim标签中的语句后添加内容
    - prefixOverrides：前缀覆盖掉（去掉）
    - suffixOverrides：后缀覆盖掉（去掉）

    ```xml
    <!--
        prefix="where" 是在trim标签所有内容的前面添加 where，如果条件都不成立，他会不加
        suffixOverrides="and|or" 是把trim标签中内容的后缀and或or去掉
    -->
    <select id="selectByMultiConditionWithTrim" resultType="car">
        select * from t_car
        <trim prefix="where" suffixOverrides="and|or">
            <if test="brand != null and brand != ''">
                brand like "%"#{brand}"%" and
            </if>
            <if test="guidePrice != null and guidePrice != ''">
                guide_price > #{guidePrice} and
            </if>
            <if test="carType != null and carType != ''">
                car_type =#{carType}
            </if>
        </trim>
    </select>
    ```

    

* set标签

  * 主要使⽤在update语句当中，⽤来⽣成set关键字，同时去掉最后多余的“,”

  * ⽐如我们只更新提交的不为空的字段，如果提交的数据是null或者""，那么这个字段我们将不更新。

    ```xml
    <update id="updateBySet">
    update t_car
    <set>
        <if test="carNum !=null and carNum != ''">car_num=#{carNum},</if>
        <if test="brand !=null and brand != ''">brand=#{brand},</if>
        <if test="guidePrice !=null and guidePrice != ''">guide_price=#{guidePrice},</if>
        <if test="produceTime !=null and produceTime != ''">produce_time=#{produceTime},</if>
        <if test="carType !=null and carType != ''">car_type=#{carType},</if>
    </set>
    where id = #{id};
    </update>
    
    ```

    

* ### choose when otherwise（三个标签必须要一起用）

  ```xml
  <select id="selectByChoose" resultType="Car">
      select * from t_car
      <where>
          <choose>
              <when test="brand != null and brand != ''">
                  brand like "%"#{brand}"%"
              </when>
              <when test="guidePrice != null and guidePrice != ''">
                  guide_price > #{guidePrice}
              </when>
              <otherwise>
                  car_type = #{carType}
              </otherwise>
          </choose>
      </where>
  </select>
  
  ```

  * 相当于

    ```xml
    if () {
    } else if () {
    } else if () {
    } else if () {
    } else {
    }
    至少有一个分支执行
    
    ```

    

* for each标签

  * 用于循环数组或集合，比如下面的操作

    ```sql
    delete from t_car where id in(1,2,3);
    delete from t_car where id = 1 or id = 2 or id = 3;
    
    insert into t_car values
        (null,'1001','凯美瑞',35.0,'2010-10-11','燃油⻋'),
        (null,'1002','⽐亚迪唐',31.0,'2020-11-11','新能源'),
        (null,'1003','⽐亚迪宋',32.0,'2020-10-11','新能源')
    
    ```

  * 首先定义一个接口，传入数组，他会封装成map，因此为了方便使用，可以使用param注解

    ```java
    int deleteByIds(@Param("ids")Long[] ids);
    ```

  * 编写xml

    ```xml
        <delete id="deleteByIds">
            delete from t_car where id= in(
            <foreach collection="#{ids}" item="id" separator=",">
                #{id}
            </foreach>
            )
        </delete>
    ```

  * 建议使用下面这个

    ```xml
    <!--
        foreach标签的属性：
            collection:指定数组或者集合，默认值为array或arg0.也可以使用@Param注解自行指定
            item:代表数组或集合中的元素
            separator:循环之间的分隔符
            open:在循坏开始之前拼接的内容
            close:在循坏结束之后拼接的内容
    -->
    <delete id="deleteByIds">
        delete from t_car where id in
            <foreach collection="ids" item="id" separator="," open="(" close=")">
                #{id}
            </foreach>
    </delete>
    ```

    

  * 批量插入

    ```java
    int insertBatch(@Param("cars") List<Car> cars);
    ```

    ```java
    <insert id="insertBatch">
        insert into t_car values
        <foreach collection="cars" item="car" separator=",">
            (null,#{car.carNum},#{car.brand},#{car.guidePrice},#{car.produceTime},#{car.carType})
        </foreach>
    </insert>
    
    ```

    

* ### sql标签与include标签

  *  sql标签⽤来声明sql⽚段

  * include标签⽤来将声明的sql⽚段包含到某个sql语句当中

  * 作⽤：代码复⽤。易维护 

    ```xml
    <sql id="carColumnName">
        id,
        car_num      as carNum,
        brand,
        guide_price  as guidePrice,
        produce_time as produceTime,
        car_type     as carType
    </sql>
    
    <select id="selectCarById" resultType="com.ziv.mybatis.pojo.Car">
        select 
        <include refid="carColumnName"/>
        from t_car
        where id = #{id}
    </select>
    
    ```

    



###### 多对一

* 多个表联合查询，用主表包含附表

* 比如通过学生表的外键获取班级表

  ```java
  package wang.zi.jie.bean;
  
  /**
   * ClassName:Class
   * Package:
   * Description:
   *
   * @Aurhor 王子杰
   * @Create 2024/3/7 10:59
   * @Version 1.0
   */
  public class Clazz {
      private Long cid;
      private String cname;
  
      public Long getCid() {
          return cid;
      }
  
      public void setCid(Long cid) {
          this.cid = cid;
      }
  
      public String getCname() {
          return cname;
      }
  
      public void setCname(String cname) {
          this.cname = cname;
      }
  
      @Override
      public String toString() {
          return "Class{" +
                  "cid=" + cid +
                  ", cname='" + cname + '\'' +
                  '}';
      }
  
      public Clazz(Long cid, String cname) {
          this.cid = cid;
          this.cname = cname;
      }
  
      public Clazz() {
      }
  }
  ```

  * 然后在学生类中添加班级类对象

    ```java
    package wang.zi.jie.bean;
    
    /**
     * ClassName:Stu
     * Package:
     * Description:
     *
     * @Aurhor 王子杰
     * @Create 2024/3/7 11:01
     * @Version 1.0
     */
    public class Stu {
        private Long sid;
        private String sname;
        private Clazz clazz;
        public Stu() {
        }
    
        public Long getSid() {
            return sid;
        }
    
        public void setSid(Long sid) {
            this.sid = sid;
        }
    
        public String getSname() {
            return sname;
        }
    
        public void setSname(String sname) {
            this.sname = sname;
        }
    
        public Clazz getClazz() {
            return clazz;
        }
    
        public void setClazz(Clazz clazz) {
            this.clazz = clazz;
        }
    
        @Override
        public String toString() {
            return "Stu{" +
                    "sid=" + sid +
                    ", sname='" + sname + '\'' +
                    ", clazz=" + clazz +
                    '}';
        }
    }
    ```

    ```xml
        <resultMap id="studentResultMap" type="stu">
            <id property="sid" column="sid"></id>
            <result property="sname" column="sname"></result>
            <result property="clazz.cid" column="cid"></result>
            <result property="clazz.cname" column="cname"></result>
        </resultMap>
        <select id="selectById" resultMap="studentResultMap">
            select s.sid,s.sname,c.cid,c.cname from t_stu s left join t_class c on s.cid=c.cid
            where s.sid=#{sid}
        </select>
    ```

    ```java
        @Test
        public void testSelectById(){
            SqlSession sqlSession= SqlSessionUntil.getSqlSession();
            StuMapper mapper = sqlSession.getMapper(StuMapper.class);
            Stu stu = mapper.selectById(1);
            System.out.println(stu);
            sqlSession.commit();
            sqlSession.close();
        }
    ```

  * 方法二：使用association

    ```xml
        <resultMap id="studentResultMapAssiciation" type="stu">
            <id property="sid" column="sid"></id>
            <result property="sname" column="sname"></result>
            <association property="clazz" javaType="clazz">
    <!--     association意思为关联，即一个属性关联另一个属性
                property是bean类的属性名
                javaType是要关联类的类名
         -->
                <id property="cid" column="cid"></id>
                <result property="cname" column="cname"></result>
            </association>
        </resultMap>
    
        <select id="selectByAssociation" resultMap="studentResultMapAssiciation">
            select s.sid,s.sname,c.cid,c.cname from t_stu s left join t_class c on s.cid=c.cid
            where s.sid=#{sid}
        </select>
    ```

  * 方法三：分步使用，复用性更强，可以充分利用延迟加载机制（懒加载）

    ```xml
    <mapper namespace="wang.zi.jie.mapper.ClazzMapper">
        <select id="selectByIdStep2" resultType="clazz">
            select cid,cname from t_class where cid=#{cid}
        </select>
    </mapper>
    
    ```

    ```xml
        <!--  两条SQL语句，实现多对一查询  -->
        <resultMap id="studentSelectStep1" type="stu">
            <id property="sid" column="sid"></id>
            <result property="sname" column="sname"></result>
            <association property="clazz" select="wang.zi.jie.mapper.ClazzMapper.selectByIdStep2" column="cid">
            <!--   指明第二步SQL语句的Id   column会传入到select语句作为参数      -->
            </association>
        </resultMap>
        <select id="selectByIdStep1" resultMap="studentSelectStep1">
            select sid,sname,cid from t_stu where sid=#{id}
        </select>
    ```

    ```java
     public Stu selectByIdStep1(Integer id);
    ```

    ```java
    public interface ClazzMapper {
        Clazz selectByIdStep2(Integer cid);
    }
    ```

    ```java
        @Test
        public void testSelectByStep(){
            SqlSession sqlSession= SqlSessionUntil.getSqlSession();
            StuMapper mapper = sqlSession.getMapper(StuMapper.class);
            Stu stu = mapper.selectByIdStep1(1);
            System.out.println(stu);
            sqlSession.commit();
            sqlSession.close();
        }
    ```

    

* 懒加载就是尽可能少查，不用就不查，association标签开启延迟加载语句：fetchType="lazy"

  ```xml
      <resultMap id="studentSelectStep1" type="stu">
          <id property="sid" column="sid"></id>
          <result property="sname" column="sname"></result>
          <association property="clazz" select="wang.zi.jie.mapper.ClazzMapper.selectByIdStep2" column="cid" fetchType="lazy">
          <!--   指明第二步SQL语句的Id   column会传入到select语句作为参数      -->
          </association>
      </resultMap>
      <select id="selectByIdStep1" resultMap="studentSelectStep1">
          select sid,sname,cid from t_stu where sid=#{id}
      </select>
  ```

  * 延迟加载的全局开关，默认fasle

    ```xml
    <settings>
        <setting name="lazyLoadingEnabled" value="true"/>
    </settings>
    
    ```

    ```java
        @Test
        public void testSelectByStep(){
            SqlSession sqlSession= SqlSessionUntil.getSqlSession();
            StuMapper mapper = sqlSession.getMapper(StuMapper.class);
            Stu stu = mapper.selectByIdStep1(1);
    //        System.out.println(stu);
            //只查看学生的名字，那这第二步就不会执行，等你需要再执行
            System.out.println(stu.getSname());
            //下一步需要了，现在才开始执行第二步
            System.out.println(stu.getClazz().getCname());
            sqlSession.commit();
            sqlSession.close();
        }
    ```

  * 如果开启全局后，某些地方不想让他延迟加载，就用fetchType="eager"。

  * **实际开发全局延迟加载要打开，某一个不需要的情况屏蔽即可**

##### 一对多查询

* 两种方式：一是使用集合存储，二是使用分步查询

* 集合查询

  ```xml
      <resultMap id="clazzResultMap" type="clazz">
          <id property="cid" column="cid"></id>
          <result property="cname" column="cname"></result>
  <!--        ofType告诉集合中元素的数据类型-->
          <collection property="stus" ofType="stu">
              <id property="sid" column="sid"></id>
              <result property="sname" column="sname"></result>
          </collection>
      </resultMap>
      <select id="selectByCidStep" resultMap="clazzResultMap">
          select c.cid, c.cname, s.sid, s.sname
          from t_class c left join t_stu s on c.cid = s.cid
          where c.cid = #{cid}
      </select>
  ```

  ```java
  Clazz selectByCidStep(Integer cid);
  ```

  

* 分步查询

  ```xml
      <resultMap id="selectByStep1ResultMap" type="clazz">
          <id property="cid" column="cid"></id>
          <result property="cname" column="cname"></result>
          <collection property="stus" select="wang.zi.jie.mapper.StuMapper.selectByCid" column="cid"></collection>
      </resultMap>
      <select id="selectByStep1" resultMap="selectByStep1ResultMap" >
          select cid,cname from t_class where cid=#{cid}
      </select>
  ```

  ```java
   Clazz selectByStep1(Integer cid);
  ```

  ```java
  List<Stu> selectByCid(Integer cid);
  ```

  ```java
      <select id="selectByCid" resultType="stu">
          select * from t_stu where cid=#{cid}
      </select>
  ```

  