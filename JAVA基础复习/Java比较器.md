#### 对象排序

* 自然排序，继承Comparable接口

  * 继承才能比较，负责会报错

    ```java
    package Common;
    
    import org.junit.Test;
    
    import java.text.ParseException;
    import java.text.SimpleDateFormat;
    import java.time.*;
    import java.time.format.DateTimeFormatter;
    import java.time.temporal.TemporalAccessor;
    import java.util.Arrays;
    
    public class test1 {
        public static void main(String[] args) {
    
        }
    
        @Test
        //新旧方法对比
        public void test2() throws ParseException {
            Person[] arr=new Person[3];
            arr[0]=new Person("bb",15);
            arr[1]=new Person("aa",14);
            arr[2]=new Person("cc",16);
            Arrays.sort(arr);
            for (int i = 0; i <arr.length ; i++) {
                System.out.println(arr[i]);
            }
    
        }
    }
    class Person implements Comparable{
        private String name;
        private int age;
    
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }
    
        public String getName() {
            return name;
        }
    
        public int getAge() {
            return age;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    
        public void setAge(int age) {
            this.age = age;
        }
    
        @Override
        public String toString() {
            return "Person{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }
        @Override
        public int compareTo(Object o) {
            //先比较地址是否一样，地址一样肯定大小一样
            if (o==this){
                return 0;
            }
            //如果返回是正数，则大，相等0
            if (o instanceof Person){
                Person p= (Person) o;
                int value = Double.compare(this.age, p.age);
                //从小到大排序，如果是从大到小就加个负号
                return value;
            }
            throw new RuntimeException("类型不匹配");
        }
    }
    ```

  * 具体的类A实现Comparable接口

  * 重写Comparable接口中的compareTo(Object obj)方法，在此方法中指明比较类A的对象的大小的标准创建类A的多个实例，进行大小的比较或排序。

* 定制排序

  * 当元素的类型没有实现java.lang.Comparatm接口而又不方便修改代码（例如:一些第三方的类，你只有.class文件，没有源文件)

  * 如果一个类，实现了Comparable接口，也指定了两个对象的比较大小的规则，但是此时此刻我不想按照它预定义的方法比较大小，但是我又不能随意修改，因为会影响其他地方的使用，怎么办?

  * JDK在设计类库之初，也考虑到这种情况，所以又增加了一个java.utilL.Comparator接口。强行对多个对象进行整体排序的比较。

  * 重写compare(Object o1,Object o2)方法，比较o1和o2的大小:如果方法返回正整数，则表示o1大于o2;如果返回0，表示相等;返回负整数，表示o1小于o2。

  * 可以将Comparator传递给sort方法(如Collections.sort或Arrays.sort)，从而允许在排序顺序上实现精确控制。

    ```java
    package Common;
    
    import org.junit.Test;
    
    import java.text.ParseException;
    import java.text.SimpleDateFormat;
    import java.time.*;
    import java.time.format.DateTimeFormatter;
    import java.time.temporal.TemporalAccessor;
    import java.util.Arrays;
    import java.util.Calendar;
    import java.util.Comparator;
    import java.util.Date;
    
    public class test1 {
        public static void main(String[] args) {
    
        }
    
        @Test
        //新旧方法对比
        public void test2() throws ParseException {
            Person[] arr=new Person[3];
            arr[0]=new Person("bb",15);
            arr[1]=new Person("aa",14);
            arr[2]=new Person("cc",16);
            //创建一个实现Comparator 接口的实现类对象
            Comparator comparator=new Comparator() {
                @Override
                //在这里比
                public int compare(Object o1, Object o2) {
                    if (o1 instanceof Person && o2 instanceof Person){
                        Person person= (Person) o1;
                        Person person2= (Person) o2;
                        return Double.compare(person.getAge(), person2.getAge());
    
                    }
                   throw new  RuntimeException("类型不匹配");
                }
            };
            Arrays.sort(arr,comparator);
            for (int i = 0; i <arr.length ; i++) {
                System.out.println(arr[i]);
            }
    
        }
    }
    class Person {
        private String name;
        private int age;
    
        public Person(String name, int age) {
            this.name = name;
            this.age = age;
        }
    
        public String getName() {
            return name;
        }
    
        public int getAge() {
            return age;
        }
    
        public void setName(String name) {
            this.name = name;
        }
    
        public void setAge(int age) {
            this.age = age;
        }
    
        @Override
        public String toString() {
            return "Person{" +
                    "name='" + name + '\'' +
                    ", age=" + age +
                    '}';
        }
    }
    
    Person{name='aa', age=14}
    Person{name='bb', age=15}
    Person{name='cc', age=16}
    ```

  * 创建一个实现了Comparator接口的实现类A

  * 实现类A要求重写Comparator接口中的抽象方法compare(0bject o1,0bject o2)，在此方法中指明要比较大小的对象的大小关系。（比如，String类Producl类)

  * 创建此实现类A的对象，并将此对象传入到相关方法的参数位置即可。(比如:Arrays.sort(..,类A的实例))

* 两种方法对比

  * 角度一：自然排序是单一的、唯一的，定制排序是灵活的、多样的
  * 角度二：自然排序只要实现接口是一劳永逸的，定制排序是临时的
  * 角度三：自然排序对象的接口是是Comparable，对应的抽象方法是compareTo(Object obj),定制排序是Comparator，实现的抽象方法是compare(Object obj1,Object obj2)