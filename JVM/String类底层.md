#### String类底层

* jdk1.9开始，String 再也不用char[]来存储啦，改成了byte[]加上编码标记，节约了一些空间。
  * 因为char是两个字节，对于很多非中文的，他用一个字节就够了，造成许多空间的浪费，而byte可以节约空间，中文就采用两个byte空间
* ==String的String Pool是一个固定大小的Hashtable，默认值大小长度是1009。==如果放进String Pool的String非常多，就会造成Hash冲突严重，从而导致链表会很长，而链表长了后直接会造成的影响就是当调用String.intern时性能会大幅下降。
* 使用-XX : StringTablesize可设置StringTable的长度
* 在jdk6中StringTable是固定的，就是1009的长度，所以如果常量池中的字符串过多就会导致效率下降很快。StringTablesize设置没有要求，在jdk7中要求StringTable的长度默认值是60013
* 在jdk8中，1009是可设置的最小值。



##### String的内存分配

* 在Java语言中有8种基本数据类型和一种比较特殊的类型String。这些类型为了使它们在运行过程中速度更快、更节省内存，都提供了一种常量池的概念。

* 常量池就类似一个Java系统级别提供的缓存。8种基本数据类型的常量池都是系统协调的，String类型的常量池比较特殊。它的主要使用方法有两种。

* 直接使用双引号声明出来的String对象会直接存储在常量池中。

  * 比如:string info = "atguigu.com" ;

* 如果不是用双引号声明的string对象，可以使用string提供的intern ()方法。这个后面重点谈

* Java6及以前，字符串常量池存放在永久代。

* Java 7 中oracle 的工程师对字符串池的逻辑做了很大的改变，即将字符串常量池的位置调整到Java堆内。

  >所有的字符串都保存在堆（Heap）中，和其他普通对象一样，这样可以让你在进行调优应用时仅需要调整堆大小就可以了。
  >字符串常量池概念原本使用得比较多，但是这个改动使得我们有足够的理由让我们重新考虑在Java 7 中使用string.intern ( )。Java8元空间，字符串常量在堆

<img src="String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705633267884.png" alt="1705633267884" style="zoom:50%;" />

<img src="String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705633284836.png" alt="1705633284836" style="zoom:50%;" />

* 常量池追踪

  ```java
  public class StringTest4 {
      public static void main(String[] args) {
          System.out.println();//2293
          System.out.println("1");//2294
          System.out.println("2");
          System.out.println("3");
          System.out.println("4");
          System.out.println("5");
          System.out.println("6");
          System.out.println("7");
          System.out.println("8");
          System.out.println("9");
          System.out.println("10");//2303
          //如下的字符串"1" 到 "10"不会再次加载
          System.out.println("1");//2304
          System.out.println("2");//2304
          System.out.println("3");
          System.out.println("4");
          System.out.println("5");
          System.out.println("6");
          System.out.println("7");
          System.out.println("8");
          System.out.println("9");
          System.out.println("10");//2304
      }
  }
  ```

  ![1705634031889](String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705634031889.png)
  * 可以看见刚开始常量池已经有2159个字符串

    <img src="String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705634126338.png" alt="1705634126338" style="zoom:50%;" />

    ![1705639806300](String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705639806300.png)

  * 执行到第二行已经变成2160





##### 字符串拼接操作

* 常量与常量的拼接结果在常量池，原理是编译期优化

* 常量池中不会存在相同内容的常量。

* **只要其中有一个是变量，结果就在堆中。变量拼接的原理是StringBuilder**

* 如果拼接的结果调用intern ()方法，则主动将常量池中还没有的字符串对象放入池中，并返回此对象地址。

* 面试题一

  ```java
  public void test1(){
          String s1 = "a" + "b" + "c";//编译期优化：等同于"abc"
          String s2 = "abc"; //"abc"一定是放在字符串常量池中，将此地址赋给s2
          /*
           * 最终.java编译成.class,再执行.class
           * String s1 = "abc";
           * String s2 = "abc"
           */
          System.out.println(s1 == s2); //true
          System.out.println(s1.equals(s2)); //true
      }
  ```

  * 这题就是编译器优化，常量与常量的拼接结果在常量池，所以两个都是true



* 面试题二

  ```java
  public void test2(){
          String s1 = "javaEE";
          String s2 = "hadoop";
  
          String s3 = "javaEEhadoop";
          String s4 = "javaEE" + "hadoop";//编译期优化
          //如果拼接符号的前后出现了变量，则相当于在堆空间中new String()，具体的内容为拼接的结果：javaEEhadoop
          String s5 = s1 + "hadoop";
          String s6 = "javaEE" + s2;
          String s7 = s1 + s2;
  
          System.out.println(s3 == s4);//true
          System.out.println(s3 == s5);//false
          System.out.println(s3 == s6);//false
          System.out.println(s3 == s7);//false
          System.out.println(s5 == s6);//false
          System.out.println(s5 == s7);//false
          System.out.println(s6 == s7);//false
          //intern():判断字符串常量池中是否存在javaEEhadoop值，如果存在，则返回常量池中javaEEhadoop的地址；
          //如果字符串常量池中不存在javaEEhadoop，则在常量池中加载一份javaEEhadoop，并返回次对象的地址。
          String s8 = s6.intern();
          System.out.println(s3 == s8);//true
      }
  ```

  * 这里考的就是涉及到变量就会new一个对象。如果拼接符号的前后出现了变量，则相当于在堆空间中new String()，具体的内容为拼接的结果
  * 'intern():判断字符串常量池中是否存在javaEEhadoop值，如果存在，则返回常量池中javaEEhadoop的地址
  * 如果字符串常量池中不存在javaEEhadoop，则在常量池中加载一份javaEEhadoop，并返回对象的地址。

* 字节码层面讲解

  ```java
   public void test3(){
          String s1 = "a";
          String s2 = "b";
          String s3 = "ab";
          String s4 = s1 + s2;//
          System.out.println(s3 == s4);//false
      }
  ```

  ```class
  0 ldc #14 <a>
   2 astore_1
   3 ldc #15 <b>
   5 astore_2
   6 ldc #16 <ab>
   8 astore_3
   9 new #9 <java/lang/StringBuilder>
  12 dup
  13 invokespecial #10 <java/lang/StringBuilder.<init>>
  16 aload_1
  17 invokevirtual #11 <java/lang/StringBuilder.append>
  20 aload_2
  21 invokevirtual #11 <java/lang/StringBuilder.append>
  24 invokevirtual #12 <java/lang/StringBuilder.toString>
  27 astore 4
  29 getstatic #3 <java/lang/System.out>
  32 aload_3
  33 aload 4
  35 if_acmpne 42 (+7)
  38 iconst_1
  39 goto 43 (+4)
  42 iconst_0
  43 invokevirtual #4 <java/io/PrintStream.println>
  46 return
  ```

  * 可以看到变量拼接使用new #9 <java/lang/StringBuilder>
  * 然后调用两次append方法：17 invokevirtual #11 <java/lang/StringBuilder.append>
    20 aload_221 invokevirtual #11 <java/lang/StringBuilder.append>添加这两个字符串
  * 最后通过toString方法生成字符串24 invokevirtual #12 <java/lang/StringBuilder.toString>

* 代码层面理解

  ```java
         /*
          如下的s1 + s2 的执行细节：(变量s是临时定义的）
          ① StringBuilder s = new StringBuilder();
          ② s.append("a")
          ③ s.append("b")
          ④ s.toString()  --> 约等于 new String("ab")
  
          补充：在jdk5.0之后使用的是StringBuilder,在jdk5.0之前使用的是StringBuffer
           */
  ```

  

* 注意点

  ```java
      public void test4(){
          final String s1 = "a";
          final String s2 = "b";
          String s3 = "ab";
          String s4 = s1 + s2;
          System.out.println(s3 == s4);//true
      }
  ```

  *  字符串拼接操作不一定使用的是StringBuilder
  * **如果拼接符号左右两边都是字符串常量或常量引用（即final修饰的），则仍然使用编译期优化，即非StringBuilder的方式。**
  * ==针对于final修饰类、方法、基本数据类型、引用数据类型的量的结构时，还是常量。final修饰后已经为常量了==



* append方法和字符串拼接对比   

  ```java
      public void test6(){
          long start = System.currentTimeMillis();
  //        method1(100000);//4014
          method2(100000);//7
          long end = System.currentTimeMillis();
  
          System.out.println("花费的时间为：" + (end - start));
      }
      public void method1(int highLevel){
          String src = "";
          for(int i = 0;i < highLevel;i++){
              src = src + "a";//每次循环都会创建一个StringBuilder、String
          }
  //        System.out.println(src);
      }
      public void method2(int highLevel){
          //只需要创建一个StringBuilder
          StringBuilder src = new StringBuilder();
          for (int i = 0; i < highLevel; i++) {
              src.append("a");
          }
  //        System.out.println(src);
      }
  ```

  * 使用method1方法每次循环都会创建一个StringBuilder、String，非常耗时，method2只需要创建一个StringBuilder
  * ==使用String的字符串拼接方式：内存中由于创建了较多的StringBuilder和String的对象，内存占用更大；如果进行GC，需要花费额外的时间==
  * **改进的空间：在实际开发中，如果基本确定要前前后后添加的字符串长度不高于某个限定值highLevel的情况下,建议使用构造器实例化：**        
    *   StringBuilder s = new StringBuilder(highLevel);//new char[highLevel]

##### intern方法的理解

* public native String intern();

* 如何保证变量s指向的是字符串常量池中的数据呢，有两种方式

  * String s=“aa”;   字面量的方式
  * 方式二： 调用intern()
     *         String s = new String("shkstart").intern();
     *         String s = new StringBuilder("shkstart").toString().intern();

* 面试题一：new string ( " ab")会创建几个对象?看字节码

  ```java
      public static void main(String[] args) {
          String str = new String("ab");
      }
  ```

  ```class
   0 new #2 <java/lang/String>
   3 dup
   4 ldc #3 <ab>
   6 invokespecial #4 <java/lang/String.<init>>
   9 astore_1
  10 return
  ```

  * 先new了，再在常量池建立“ab”

* **难点 面试题二：String str = new String("a") + new String("b")创建了几个对象**

  ```java
   *  对象1：new StringBuilder()
   *  对象2： new String("a")
   *  对象3： 常量池中的"a"
   *  对象4： new String("b")
   *  对象5： 常量池中的"b"
   *  深入剖析： StringBuilder的toString():
   *      对象6 ：new String("ab")
   *       强调一下，toString()的调用，在字符串常量池中，没有生成"ab"
  ```

  ```class
   0 new #2 <java/lang/StringBuilder>
   3 dup
   4 invokespecial #3 <java/lang/StringBuilder.<init>>
   7 new #4 <java/lang/String>
  10 dup
  11 ldc #5 <a>
  13 invokespecial #6 <java/lang/String.<init>>
  16 invokevirtual #7 <java/lang/StringBuilder.append>
  19 new #4 <java/lang/String>
  22 dup
  23 ldc #8 <b>
  25 invokespecial #6 <java/lang/String.<init>>
  28 invokevirtual #7 <java/lang/StringBuilder.append>
  31 invokevirtual #9 <java/lang/StringBuilder.toString>
  34 astore_1
  35 return
  
  ```

  * <java/lang/StringBuilder>       <java/lang/String>        ldc #5 <a>     new #4 <java/lang/String>

    ldc #8 <b>     invokevirtual #9 <java/lang/StringBuilder.toString>

  * **注意：toString()的调用，在字符串常量池中，没有生成"ab"，这是难点**’‘

* ==**只有双引号的一定会在常量池中创建字符串，而StringBuild的append和toString传入的是char，不会创建在常量池。s.intern();调用此方法之前，字符串常量池中已经存在了"1",因此不返回地址更新，s到常量池是两个对象组成。s3.intern();//他不会在常量池新建了，他指向了了s3和常量池中间的那个对象，jdk6是因为是会二次创建，而不是指向s3的中间对象**==

  ![1705664842931](String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705664842931.png)

* 总结String的intern()的使用

  * jdk1.6中，将这个字符串对象尝试放入串池。
    * 如果串池中有，则并不会放入。返回已有的串池中的对象的地址
    * 如果没有，会把此对象复制一份，放入串池，并返回串池中的对象地址
  * Jdk1.7起，将这个字符串对象尝试放入串池。
    * 如果串池中有，则并不会放入。返回已有的串池中的对象的地址
    * 如果没有，则会把对象的引用地址复制一份，放入串池，并返回串池中的引用地址

* 面试题三

  ```java
      public static void main(String[] args) {
          String x = "ab";
          String s = new String("a") + new String("b");//new String("ab")
          //在上一行代码执行完以后，字符串常量池中并没有"ab"
  
          String s2 = s.intern();//jdk6中：在串池中创建一个字符串"ab"
                                 //jdk8中：串池中没有创建字符串"ab",而是创建一个引用，指向new String("ab")，将此引用返回
  
          System.out.println(s2 == "ab");//jdk6:true  jdk8:true
          System.out.println(s == "ab");//jdk6:false  jdk8:true
      }
  ```

  * jdk6中：在串池中创建一个字符串"ab"

  * jdk8中：串池中没有创建字符串"ab",而是创建一个引用，指向new String("ab")，将此引用返回

    <img src="String%E7%B1%BB%E5%BA%95%E5%B1%82.assets/1705668613537.png" alt="1705668613537" style="zoom:67%;" />

* 使用intern方法能够提升效率：因为可以使用
* String s3 = new String(String.valueOf(9000));像这种不进常量池
  * **只有双引号才进常量池**
  *   0 bipush 10
      2 anewarray #2 <java/lang/Integer>
      5 dup
      6 iconst_0
      7 iconst_1
      8 invokestatic #3 <java/lang/Integer.valueOf>
     11 aastore
     12 dup
     13 iconst_1
     14 iconst_2
     15 invokestatic #3 <java/lang/Integer.valueOf>
     18 aastore
     19 dup
     20 iconst_2
     21 iconst_3
     22 invokestatic #3 <java/lang/Integer.valueOf>
     25 aastore
     26 dup
     27 iconst_3
     28 iconst_4
     29 invokestatic #3 <java/lang/Integer.valueOf>
     32 aastore
     33 dup
     34 iconst_4
     35 iconst_5
     36 invokestatic #3 <java/lang/Integer.valueOf>
     39 aastore
     40 dup
     41 iconst_5
     42 bipush 6
     44 invokestatic #3 <java/lang/Integer.valueOf>
     47 aastore
     48 dup
     49 bipush 6
     51 bipush 7
     53 invokestatic #3 <java/lang/Integer.valueOf>
     56 aastore
     57 dup
     58 bipush 7
     60 bipush 8
     62 invokestatic #3 <java/lang/Integer.valueOf>
     65 aastore
     66 dup
     67 bipush 8
     69 bipush 9
     71 invokestatic #3 <java/lang/Integer.valueOf>
     74 aastore
     75 dup
     76 bipush 9
     78 bipush 10
     80 invokestatic #3 <java/lang/Integer.valueOf>
     83 aastore
     84 astore_1
     85 invokestatic #4 <java/lang/System.currentTimeMillis>
     88 lstore_2
     89 iconst_0
     90 istore 4
     92 iload 4
     94 ldc #6 <10000000>
     96 if_icmpge 121 (+25)
     99 getstatic #7 <com/atguigu/java2/StringIntern2.arr>
    102 iload 4
    104 aload_1
    105 iload 4
    107 aload_1
    108 arraylength
    109 irem
    110 aaload
    111 invokestatic #8 <java/lang/String.valueOf>
    114 aastore
    115 iinc 4 by 1
    118 goto 92 (-26)
    121 invokestatic #4 <java/lang/System.currentTimeMillis>
    124 lstore 4
    126 getstatic #9 <java/lang/System.out>
    129 new #10 <java/lang/StringBuilder>
    132 dup
    133 invokespecial #11 <java/lang/StringBuilder.<init>>
    136 ldc #12 <花费的时间为：>
    138 invokevirtual #13 <java/lang/StringBuilder.append>
    141 lload 4
    143 lload_2
    144 lsub
    145 invokevirtual #14 <java/lang/StringBuilder.append>
    148 invokevirtual #15 <java/lang/StringBuilder.toString>
    151 invokevirtual #16 <java/io/PrintStream.println>
    154 ldc2_w #17 <1000000>
    157 invokestatic #19 <java/lang/Thread.sleep>
    160 goto 170 (+10)
    163 astore 6
    165 aload 6
    167 invokevirtual #21 <java/lang/InterruptedException.printStackTrace>
    170 invokestatic #22 <java/lang/System.gc>
    173 return