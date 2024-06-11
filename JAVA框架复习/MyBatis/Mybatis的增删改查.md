#### Mybatis

* 在JDBC中传参是要用？，在mybatis中是用#{}

* sqlSession的封装

  * 它是常用的对象，应该使用一个工具池进行封装

    ```java
    public class SqlSessionUntil {
        private static SqlSessionFactoryBuilder builder=new SqlSessionFactoryBuilder();
        private static SqlSessionFactory sqlSessionFactory;
        static {
            try {
                sqlSessionFactory= builder.build(Resources.getResourceAsStream("mybatis-config.xml"));
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
        }
        private SqlSessionUntil(){
    
        }
        public static SqlSession getSqlSession() {
            //一个sqlSessionFactory对应配置文件中的environment标签，对应了一个数据库
    
            SqlSession sqlSession = sqlSessionFactory.openSession();
            return sqlSession;
        }
    }
    ```

    * 一个sqlSessionFactory对应配置文件中的environment标签，对应了一个数据库，所以不需要频繁创建

* 动态的SQL语句

  ```java
      @Test
      public void testCarInsert() {
          SqlSession sqlSession = SqlSessionUntil.getSqlSession();
          Map<String,Object> map=new HashMap();
          map.put("k1", "1111");
          map.put("k2", "比亚迪汉");
          map.put("k3", 10.0);
          map.put("k4", "2020-11-11");
          map.put("k5", "电车");
          //第一个参数是sql的id，第二个参数是封装数据的对象，映射文件写map集合的key
          sqlSession.insert("insertCar",map);
          sqlSession.commit();
          sqlSession.close();
      }
  ```

  ```xml
  <mapper namespace="aaaaa">
      <insert id="insertCar">
          insert into t_car(id,car_num,brand,guide_price,produce_time,car_type)
          values (null,#{k1},#{k2},#{k3},#{k4},#{k5})
      </insert>
  </mapper>
  ```

  * 他的底层就是通过map.get(key)方法实现的，如果找不到或key写错了，map.get(key)返回的是null，sql语句仍然会正确的运行（**除非你在建表的时候选择了不许为null**）

    

  * 也可以使用Java bean实现传值，它的xml文件#{}是他的get方法去掉get单词后的剩余部分第一个单词小写，所以他找的是get方法，**本质上是通过get方法获取值**

    ```xml
    <?xml version="1.0" encoding="UTF-8" ?>
    <!DOCTYPE mapper
            PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
            "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
    <mapper namespace="aaaaa">
        <insert id="insertCar">
            insert into t_car(id,car_num,brand,guide_price,produce_time,car_type)
            values (null,#{car_num},#{brand},#{guide_price},#{produce_time},#{car_type})
        </insert>
    </mapper>
    ```

    ```java
     @Test
        public void testCarBeanInsert(){
            SqlSession sqlSession = SqlSessionUntil.getSqlSession();
            Car car=new Car(null,"111","奔驰", 12.0, "2020-11-12","电车");
            int count = sqlSession.insert("insertCar", car);
            System.out.println(count);
            sqlSession.commit();
            sqlSession.close();
        }
    ```

    * 严格意义上来说:如果使用POJO对象传递值的话，#{}这个大括号中到底写什么?
      * **写的是get方法的方法名去掉get，然后将剩下的单词首字母小写，然后放进去。**
      * 例如:getUsername()-->#{username}
      * 例如:getEmail()-->#{email}

* 删除

  * xml配置：因为只有一个占位符，可以随便起名

    ```xml
        <delete id="deleteCar">
            delete from t_car where id=#{abc}
        </delete>
    ```

  * java，他传入的是Object，会自动帮你装箱

    ```java
        @Test
        public void deleteCar(){
            SqlSession sqlSession=SqlSessionUntil.getSqlSession();
            int count = sqlSession.delete("deleteCar", 18);
            System.out.println(count);
            sqlSession.commit();
            sqlSession.close();
        }
    ```

    

* 查询

  * 查询需要返回一个结果集，如果不指定结果集，会报 A query was run and no Result Maps were found for the Mapped Statement 'aaa.selectOneCar'.  It's likely that neither a Result Type nor a Result Map was specified.

  * 需要使用**resultType**告诉返回什么类型

    ```xml
        <select id="selectOneCar" resultType="wang.zi.jie.bean.Car">
            select * from t_car where id=#{id}
        </select>
    ```

    

  * 如果返回类型是null，考虑car_num、guide_price、produce_time、car_type这是查询结果的列名。这些列名和Car类中的属性名对不上。（bean的属性名和数据库列名对不上）。解决方法，起别名，别名和属性名一致
  
    ```xml
        select id,car_num as carNum, brand, guide_price as guidePrice,
        produce_time as produceTime, car_type as carType
        from t_car
    ```
  
    ```java
        public void selectOneCar(){
            SqlSession sqlSession=SqlSessionUntil.getSqlSession();
            Car oneCar = sqlSession.selectOne("selectOneCar", 1);
            System.out.println(oneCar);
            sqlSession.commit();
            sqlSession.close();
        }
    ```
  
    
  
* 查询全部

  ```java
      @Test
      public void selectAll(){
          SqlSession sqlSession=SqlSessionUntil.getSqlSession();
          List<Object> cars = sqlSession.selectList("selectOneAll");
          cars.forEach(car->System.out.println(car));
          sqlSession.commit();
          sqlSession.close();
      }
  ```

  ```xml
      <select id="selectAll" resultType="wang.zi.jie.bean.Car">
          select * from t_car
      </select>
  ```

  

* ### SQL Mapper 的namespace

  * 在SQL Mapper配置⽂件中标签的namespace属性可以翻译为命名空间，这个命名空间主要是为了防⽌sqlId冲突的。

  * 当有两个不同的Mapper.xml文件中的sql语句id相同的时候，就需要使用命名空间加id的形式。

  * 假设命名空间为aaa

    ```java
    <mapper namespace="aaa">
        <insert id="insertCar">
            insert into t_car(id,car_num,brand,guide_price,produce_time,car_type)
            values (null,#{car_num},#{brand},#{guide_price},#{produce_time},#{car_type})
        </insert>
    </mapper>
    ```

    * List<Object> cars = sqlSession.selectList(**"aaa.selectOneAll"**);查询写法，可以避免id冲突
    * 即namespqce.id，这个才是完整写法