#### Collections工具类

* 参考操作数组的工具类: Arrays，Collections是一个操作Set、T和Map等集合的工具类。

* 他可以把线程不安全的转为线程安全的，synchronizedList方法

  ```java
      public static void main(String[] args) {
          List collection=new ArrayList();
          String a=new String("abc");
          String b=new String("def");
          String c=new String("abc");
          collection.add(a);
          collection.add(b);
          Collections.synchronizedList(collection);
      }
  ```

  

* 常用方法

  * collections 中提供了一系列静态的方法对集合元素进行排序、查询和修改等操作，还提供了对集合对象设置不可变、对集合对象实现同步控制等方法(均为static方法)∶
* 排序需要保证实现comparable接口
  * 排序操作:

    * reverse(List):反转List 中元素的顺序

    * shuffle(List):对List集合元素进行随机排序
    * sort(List):根据元素的自然顺序对指定List集合元素按升序排序
    * sort(List，Comparator):根据指定的Comparator产生的顺序对List集合元素进行排序 
    * swap(List，int，int):将指定list集合中的i处元素和j处元素进行交换
* 查找
  
  * Object max(Collection):根据元素的自然顺序，返回给定集合中的最大元素
    * Obiect max(Collection，Comparator):根据Comparator指定的顺序，返回给定集合中的最大元素
    * 等等
  
* 区分Collection和Collections

  * Collection是集合框架，用于存储一个一个元素的接口，有List,Map这些子类

  * Collections是一个操作Set、Tree和Map等集合的工具类

    ```JAVA
     @Test
        public void test1() throws IOException {
            List list=Arrays.asList(45,25,26,32,25);
            System.out.println(list);
            Collections.reverse(list);
            System.out.println(list);
            Collections.sort(list);
            System.out.println(list);
            Collections.sort(list, new Comparator() {
                @Override
                public int compare(Object o1, Object o2) {
                    if (o1 instanceof Integer && o2 instanceof  Integer){
                        Integer integer= (Integer) o1;
                        Integer integer1= (Integer) o2;
                        return -(integer.intValue()-integer1.intValue());
                    }
                    throw new RuntimeException("类型不匹配");
                }
            });
            System.out.println(list);
            Object obj=Collections.max(list);
            System.out.println(obj);
            System.out.println(Collections.frequency(list, 25));
    
            //难点
    //        List dest=new ArrayList();
            List dest=Arrays.asList(new Object[5]);
            /*
            源码private static final int DEFAULT_CAPACITY = 10;
            但是size是0
             */
            System.out.println(dest.size());
            System.out.println(list.size());//5
            Collections.copy(dest, list);//会报错，看异常位置会显示大小不匹配，要想不报错dest就得长度至少为5
            /*
            源码public static <T> void copy(List<? super T> dest, List<? extends T> src) {
            int srcSize = src.size();
            if (srcSize > dest.size())
                throw new IndexOutOfBoundsException("Source does not fit in dest");
             */
    
        }
    ```

    

* 练习斗地主

  ```java
  public class test1 {
      public static void main(String[] args) {
          String [] num={"A","2","3","4","5","6","7","8","9","10","J","Q","K"};
          String[] color={"方块","梅花","红桃","黑桃"};
          ArrayList list=new ArrayList();
          for (int i = 0; i < color.length; i++) {
              for (int j = 0; j < num.length; j++) {
                  list.add(color[i]+num[j]);
  
              }
          }
          list.add("大王");
          list.add("小王");
  
          //洗牌
          Collections.shuffle(list);
          //发牌
          ArrayList list1=new ArrayList();
          ArrayList list2=new ArrayList();
          ArrayList list3=new ArrayList();
          //斗地主别忘了留下地主牌
          ArrayList dizhu=new ArrayList();
          for (int i = 0; i <list.size() ; i++) {
              if (i>=(list.size()-3)){
                  dizhu.add(list.get(i));
              }
              else if (i%3==0){
                  list1.add(list.get(i));
              }
              else if (i%3==1){
                  list2.add(list.get(i));
              }
              else {
                  list3.add(list.get(i));
              }
          }
          //显示
          System.out.println("第一个人");
          System.out.println(list1);
          System.out.println("第二个人");
          System.out.println(list2);
          System.out.println("第三个人");
          System.out.println(list3);
          System.out.println("底牌");
          System.out.println(dizhu);
      }
  }
  第一个人
  [黑桃7, 红桃K, 红桃4, 红桃7, 方块3, 方块J, 黑桃J, 红桃8, 梅花Q, 梅花4, 梅花3, 梅花A, 黑桃8, 梅花5, 方块4, 方块2, 方块8]
  第二个人
  [梅花J, 黑桃5, 黑桃2, 梅花10, 梅花9, 红桃J, 梅花6, 方块Q, 梅花8, 方块5, 黑桃K, 方块A, 红桃9, 方块6, 黑桃3, 方块7, 梅花7]
  第三个人
  [方块10, 黑桃Q, 红桃Q, 红桃3, 梅花K, 黑桃4, 方块K, 梅花2, 方块9, 黑桃9, 红桃6, 红桃10, 黑桃A, 红桃5, 小王, 黑桃6, 大王]
  底牌
  [红桃A, 红桃2, 黑桃10]
  ```

  



###### 面试题

* List,Set,Map是否继承自collection接口？  map不是
* 说说List,Set,Map三者的区别
* 写出List,map,set接口的实现类，并说出其特点
* 常见集合类的区别和使用场景
* 集合的父类是谁？哪些是安全的
  * 集合的哪些是线程不安全的  不安全ArrayList、HashMap、HashSet安全的Vector\Hashtable
* 集合说一下哪些线程是不安全的
* 遍历集合的方式有哪些
  * 迭代器Iterator用来遍历Collection，不能用来遍历Map
  * 增强for
  * 一般的for，可以遍历list
* List接口有哪些实现
* ArrayList和Linkedlist的区别有哪些
* ArrayList与Vector的区别，为什么要用ArrayList取代Vector
* java.util.ArrayList常用的方法有哪些
* ArrayList是有序还是无序，为什么  有序，底层是数组
* Set集合有哪些实现类，有什么特点
* List和Set的区别
* Set中的元素是不能重复的，那么用什么方法来区别是重复与否呢？用==还是equals，有什么区别
* TreeSet两种排序方式在使用的时候怎么起作用
* TreeSet的数据结构
* 说一说java的集合Map有哪些Map
* final怎么用，修饰Map可以继续添加数据吗  可以
* Set和Map的比较
  * HashSet底层是hashMap
  * LinkedHashset底层就是LinkedHashMap
  * TreeSet底昙就是TeeMap
* HashMap说一下线程安全吗
* Hashtable是怎么实现的，为什么线程安全?(
  * 数组+单向链表;底层方法使用synchronized修饰
* HashMap和LinkedHashMap的区别
* HashMap和TreeMap的区别  底层的数悬结构截然不同。
* HashMap里面实际装的是什么?
  * JDK7: HashMap内部声明了Entry，实现了Map中的Entry接口。(key，value作为Entry的两个属性出现)J
  * JDK8: HashMap内部声明了Node，实现了Map中的Entry接口。(key，value作为Node的两个属性出现)
* HashMap的key存储在哪里?和value存储在一起吗?那么value存储在哪里?说具体点?
* 自定义类型可以作为Key么?
  * 可以，但是要实现equals和hashcode
* 集合的工具类是谁？用过工具类的哪些方法
  * Collections
* Collection和Collections区别
* ArrayList如何实现排序
  * Collections.sort
* HashMap是否线程安全，怎么解决HashMap线程不安全