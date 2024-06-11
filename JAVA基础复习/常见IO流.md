



#### 常见IO

* idea默认目录是工程的根

####文件字符输入输出流

* FileReader

```java
    public void test2() throws IOException {
        FileReader fileReader=null;
        try {
            File file = new File("abc.txt");
            fileReader=new FileReader(file);
            int data;
            while ((data=fileReader.read())!=-1){
                System.out.println((char)data);
            }

        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (fileReader!=null){
                fileReader.close();
            }

        }
    }
```



* 优化，减少内存和物理磁盘的接触

  ```java
   public void test2() throws IOException {
          FileReader fileReader=null;
          try {
              File file = new File("abc.txt");
              fileReader=new FileReader(file);
              char [] buffer=new char[5];
              //fileReader.read(buffer);//返回读到的个数，比如有8个字符，第一次读返回5，第二回读则是3，第三次读则是-1
              int len;
              while ((len=fileReader.read(buffer))!=-1){
                  for (int i = 0; i < len; i++) {
                      System.out.println(buffer[i]);
                  }
              }
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              if (fileReader!=null){
                  fileReader.close();
              }
  
          }
  ```
  

  
* 写文件

  ```java
  public void test2() throws IOException {
          FileWriter fileWriter=null;
          try {
              File file = new File("ac.txt");
              fileWriter=new FileWriter(file);//从第一行开始覆盖原数据
  //            fileWriter=new FileWriter(file,true);在尾部添加数据
              fileWriter.write("123\n");
              fileWriter.close();
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              try {
                  if (fileWriter!=null){
                      fileWriter.close();
                  }
              }catch (IOException e){
                  e.printStackTrace();
              }
          }
  
      }
  ```

  

* 复制文件

  ```java
   public void test2() throws IOException {
          FileWriter fileWriter=null;
          FileReader fileReader=null;
          try {
              File file = new File("abc.txt");
              File desc = new File("ac.txt");
              fileWriter=new FileWriter(file);
              fileReader=new FileReader(desc);
              char[] buffer=new char[5];
              int length;
              while ((length = fileReader.read(buffer))!=-1){
                  System.out.println(buffer[0]);
                  fileWriter.write(String.valueOf(buffer));
              }
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              try {
                  if (fileWriter!=null){
                      fileWriter.close();
                  }
                  if (fileReader!=null){
                      fileReader.close();
                  }
              }catch (IOException e){
                  e.printStackTrace();
              }
          }
  
      }
  ```

  * **这里有问题，比如有8个字符，第一次读返回5，第二回读虽然长度是3，但是buffer的5个空间都有，所以如果要转成字符串必然要截断才可以/**new  String(“buffer",0,length),length为返回的长度，这样才可以**
  * **第二个问题： `FileWriter`类在执行`write()`方法时，并不会立即将数据写入磁盘，而是将数据存储在缓冲区。因此，通过调用`flush()`方法，可以确保缓冲区的数据被立即写入到文件中。  需要在`fileWriter.write(String.valueOf(buffer));`之后添加`fileWriter.flush();` **

* 注意：设计到流的关闭，应该有trycatch，而不是抛出异常
  * 对于输入流，File的对象文件必须存在，负责会报文件没发现异常
  * 对于输出，可以不存在，没有会自动创建文件



##### 文件字节输入输出流

* 字符流无法处理非文本文件，此时必须用字节流

  ```java
   public void test2() throws IOException {
          FileInputStream fileInputStream=null;
          FileOutputStream fileOutputStream=null;
          try {
              File srcFile=new File("HH.png");
              File destFile=new File("HH_copy.png");
              fileInputStream=new FileInputStream(srcFile);
              fileOutputStream=new FileOutputStream(destFile);
              byte[] buffer=new byte[1024];
              int length ;
              //读到的位置什么也没有返回的数据就是-1
              while ((length = fileInputStream.read(buffer))!=-1){
                  fileOutputStream.write(buffer,0,length);
              }
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              try{
                  if (fileInputStream==null){
                      fileInputStream.close();
                  }
                  if (fileOutputStream==null){
                      fileOutputStream.close();
                  }
              }catch (Exception e){
                  e.fillInStackTrace();
              }
          }
      }
  ```

  * fileOutputStream=**new** FileOutputStream(destFile,**true**);是在原来内容上追加，不加默认清除重写。

  * 他的构造方法

    ```java
        public FileInputStream(String name) throws FileNotFoundException {
            this(name != null ? new File(name) : null);
        }
        public FileInputStream(File file) throws FileNotFoundException {
            String name = (file != null ? file.getPath() : null);
            SecurityManager security = System.getSecurityManager();
            if (security != null) {
                security.checkRead(name);
            }
            if (name == null) {
                throw new NullPointerException();
            }
            if (file.isInvalid()) {
                throw new FileNotFoundException("Invalid file path");
            }
            fd = new FileDescriptor();
            fd.attach(this);
            path = name;
            open(name);
        }
    ```

  * 所以File srcFile=new File("HH.png");  fileInputStream=new FileInputStream(srcFile);和fileInputStream=new FileInputStream("HH.png")都可以

* 注意：**对于字符流，只能用来操作文本文件，不能用来处理非文本文件。**对于字符流适合非文本文件，单纯复制文本文件也可以，但是要输出会乱码，==复制没有问题，因为排序没乱。==

* **说明：**
  * **文本文件.txt .java .c .py .cpp等**
  * 非文本:doc,xls,mp3,mp4,jpg,avi,pdf等
  
* 其他方法

  ```java
      public void test2() throws IOException {
          FileInputStream fileInputStream=null;
          FileOutputStream fileOutputStream=null;
          try {
              File srcFile=new File("HH.png");
              fileInputStream=new FileInputStream(srcFile);
              byte[] buffer=new byte[1024];
              int length ;
              //读到的位置什么也没有返回的数据就是-1
              while ((length = fileInputStream.read(buffer))!=-1){
                  //查看还剩下几个字节
                  System.out.println(fileInputStream.available());
                  //这个方法可以这样用，用一个byte直接读完，不适合太大的文件
                  byte[] buffer2=new byte[fileInputStream.available()];
                  //skip跳过多少字节不读
                  fileInputStream.skip(5);
                  System.out.println(new String(buffer,0,length));
              }
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              try{
                  if (fileInputStream==null){
                      fileInputStream.close();
                  }
                  if (fileOutputStream==null){
                      fileOutputStream.close();
                  }
              }catch (Exception e){
                  e.fillInStackTrace();
              }
          }
      }
  ```

  

  

##### 缓冲流(这种就是包装流)

* 4个缓冲流，就是把File替换成Buffered

* 默认缓冲为8192kb

* BufferedInputStream（包裹了FileInputStream）,BufferedOutputStream（FileOutputStream）,BufferedReader(FileReader),BufferedWriter(FileWriter)所以前两个是字节，后两个字符

* 这四个考虑到和磁盘交互太密集，弄了一个缓冲区，提升了效率

* 方法BufferedInputStreamread(byte[] buffer) ,BufferedOutputStreamwriter(byte[] buffer,0,len)

* BufferedReade中read(char[] buffer) BufferedWriter 中writer(char[] buffer,0,len)

* BufferedReader可以读一行readLine()，但是读一行最后不带换行符

* 外层流关闭，会自动关闭内层流，就不需要手动关闭了

  ```java
    public void test2() throws IOException {
          FileInputStream fileInputStream=null;
          FileOutputStream fileOutputStream=null;
          BufferedInputStream bufferedInputStream=null;
          BufferedOutputStream bufferedOutputStream=null;
          try {
              File srcFile=new File("HH.png");
              File destFile=new File("HH_copy.png");
              fileInputStream=new FileInputStream(srcFile);
              bufferedInputStream=new BufferedInputStream(fileInputStream);
              fileOutputStream=new FileOutputStream(destFile);
              bufferedOutputStream=new BufferedOutputStream(fileOutputStream);
              byte[] buffer=new byte[1024];
              int length ;
              while ((length = bufferedInputStream.read(buffer))!=-1){
                  bufferedOutputStream.write(buffer,0,length);
              }
          } catch (IOException e) {
              e.printStackTrace();
          } finally {
              try{
                  if (fileInputStream==null){
                      bufferedInputStream.close();
  //                    外层流关闭，会自动关闭内层流，就不需要手动关闭了
  //                    fileInputStream.close();
  
                  }
                  if (fileOutputStream==null){
                      bufferedOutputStream.close();
                      //外层流关闭，会自动关闭内层流，就不需要手动关闭了
  //                    fileOutputStream.close();
  
                  }
              }catch (Exception e){
                  e.fillInStackTrace();
              }
          }
      }
  ```

  

##### 转换流

* 为了解决的问题：**解码和编码要用相同的字符集**
* 转换流java.io.InputStreamReader，是Reader的子类，是从字节流到字符流的桥梁。它读取字节，并使用指定的字符集将其解码为字符。它的字符集可以由名称指定，也可以接受平台的默认字符集。
* 作用：实现字节与字符的转换
* InputStreamReader将一个输入型的字节流转换成输入型的字符流
* OutputStreamReader将一个输出型的字符流转换成输出型的字节流

* 注意：utf8和gbk都向下兼容了asc码

  ```java
    public void test2() throws IOException {
          File file = new File("abc.txt");
          FileInputStream fileInputStream=new FileInputStream(file);//字节流
          InputStreamReader inputStreamReader=new InputStreamReader(fileInputStream,"utf-8");//封装成字符流
          char [] buffer=new char[1024];
          int len;
          while ((len=inputStreamReader.read(buffer))!=-1){
              System.out.println(String.valueOf(buffer,0,len));
  
          }
          inputStreamReader.close();//封装层关，内层会自动关
      }
  ```

  

* 复制文件并修改编码格式

  ```java
     @Test
      public void test2() throws IOException {
          //复制功能
          File file = new File("abc.txt");
          File file1 = new File("ac.txt");
          FileInputStream fileInputStream=new FileInputStream(file);//字节流
          FileOutputStream fileOutputStream=new FileOutputStream(file1);
          InputStreamReader inputStreamReader=new InputStreamReader(fileInputStream,"utf-8");//封装成字符流
          OutputStreamWriter outputStreamWriter=new OutputStreamWriter(fileOutputStream,"gbk");
  
          char [] buffer=new char[1024];
          int len;
          while ((len=inputStreamReader.read(buffer))!=-1){
              outputStreamWriter.write(buffer, 0,len );
  
          }
          inputStreamReader.close();//封装层关，内层会自动关
          outputStreamWriter.close();
      }
  ```

  

* 编码方式
  * ascii，ASCII码(American Standard Code for Information Interchange，美国信息交换标准代码)︰上个世纪60年代，美国制定了一套字符编码，对英语字符与二进制位之间的关系，做了统一规定。这被称为AsclI码。ASclI码用于显示现代英语，主要包括控制字符（回车键、退格、换行键等）和可显示字符(英文大小写字符、阿拉伯数字和西文符号)。主要用来存储a、b、c等英文字符和1、2、3、常用的标点符号。每个字符占用1个字节。总共128个
  * iso-8859-1:拉丁码表，别名Latin-1用于显示欧洲使用的语言，包括荷兰语、德语、意大利语、葡萄牙语等SO-8859-1使用单字节编码，兼容ASCI编码。
  * GBxxxx字符集:
    * GB就是国标的意思，是为了显示中文而设计的一套字符集。
    * GB2312:简体中文码表。一个小于127的字符的意义与原来相同，**即向下兼容ASCII码**。==但两个大于12字符连在一起时，就表示一个汉字，这样大约可以组合了包含7000多个简体汉字，==此外数学符号、罗希腊的字母、日文的假名们都编进去了，这就是常说的"全角"字符，而原来在127号以下的那些符号就叫"半角"字符了。
    * GBK:最常用的中文码表。是在GB2312标准基础上的扩展规范，使用了双字节编码方案，共收录了21003个汉字.完全兼容GB2312标准，同时支持繁体汉字以及日韩汉字等。
    * GB18030:最新的中文码表。收录汉字70244个，采用多字节编码，每个字可以由1个、2个或4个字节组成。支持中国国内少数民族的文字，同时支持繁体汉字以及日韩汉字等。
  * UTF
    * Unicode是字符集，UTF-8、uf16、UTF-32是三种将数字转换到程序数据的编码方案。顾名思义，UTF-8就是每次8个位传输数据，而UTF-16就是每次16个位。其中，UTF-8是在互联网上使用最广的一种Unicode的实现方式。
    * 互联网工程工作小组（IETF）要求所有互联网协议都必须支持UTF-8编码。所以，我们开发web应用，也要使用UTF-8编码。UTF-8是一种变长的编码方式。它使用1-4个字节为每个字符编码，编码规则;
      * 128个uS-ASC字符，只需一个字节编码。
      * 拉丁文等字符，需要二个字节编码。
      * 大部分常用字(含中文)，使用三个字节编码。
      * 其他极少使用的unicode辅助字符，使用四字节编码。
    * utf-8实现了世界主要语言的字符，使用1-4不等字节表示一个字符，中文字符使用三个字节，向下兼容ascii，意味着英文字符、1、2、3、标点符号仍然使用1个字节。
  * 在内存中的字符
    * 内存中一个char占用两个字节，但是在物理磁盘中随着编码方式的不同可能是一个字节，两个字节或者三个字节。内存中使用的是Unicode字符集。

##### 数据流

* DataOutputStream:允许应用程序将基本数据类型、String类型的变量写入输出流中

* DatalnputStream:允许应用程序以与机器无关的方式从底层输入流中读取基本数据类型、String类型的变量

  ```java
      public void test2() throws IOException {
          DataOutputStream dos=new DataOutputStream(new FileOutputStream("ac"));
          byte b=100;
          int b2=100;
          short b3=100;
          char b4='a';
          boolean sex=true;
          double d=3.14;
          dos.writeBoolean(sex);
          dos.writeByte(b);
          dos.writeDouble(d);
          dos.writeInt(b2);
      }
  ```

  

<img src="%E5%B8%B8%E8%A7%81IO%E6%B5%81.assets/1692345185761.png" alt="1692345185761" style="zoom:80%;" />

* DataOutputStream写的文件，只能使用DataInputStream去读。并且读的时候你需要提前知道写入的顺序。读的顺序需要和写的顺序一致。才可以正常取出数据。

######对象流（也是包装流）

* DataOutputStream中的方法:将上述的方法的read改为相应的write

* 数据流的弊端:**只支持Java基本数据类型和字符串的读写，而不支持其它Java对象的类型。**而
  ObjectOutputStream和ObjectInputStream既支持Java基本数据类型的数据读写，又支持Java对象的读写，所以重点介绍对象流ObjectOutputStream和ObjectinputStream.

* 对象的序列化机制：对象序列化机制允许把内存中的Java对象转换成平台无关的二进制流，从而允许把这种二进制流持久地保存在磁盘上，或通过网络将这种二进制流传输到另一个网络节点。丁当其它程序获取了这种二进制流，就可以恢复成原来的Java对象。

  * 序列化过程：ObjectOutputStream，将内存中的java对象保存在文件中或通过网络传输出去

  * 反序列化过程：将文件中得数据或网络传输过来得数据还原为内存中的java对象

    ```java
        public void test2() throws IOException {
            //复制功能
            File file = new File("abc.txt");
            ObjectOutputStream objectOutputStream=new ObjectOutputStream(new FileOutputStream(file));
            //写出序列化过程
            objectOutputStream.writeUTF("江山如此多娇，引无数英雄竞折腰");
            objectOutputStream.flush();
            objectOutputStream.close();//已经被序列化了
    
            //反序列化
            ObjectInputStream objectInputStream=new ObjectInputStream(new FileInputStream(file));
            String str=objectInputStream.readUTF();
            System.out.println(str);
        }
    ```

    

* 自定义类的序列化和反序列化过程
  * **自定义类不实现Serializable会报错，Serializable属于标识接口，内部什么方法都没有**

  * 要求自定义类声明一个全局常量

    ```java
        public void test2() throws IOException, ClassNotFoundException {
            //复制功能
            File file = new File("abc.txt");
            ObjectOutputStream objectOutputStream=new ObjectOutputStream(new FileOutputStream(file));
            //写出序列化过程
            Person person=new Person("zhangsan", 18, new MyDate(2023,5,4));
            objectOutputStream.writeObject(person);
            objectOutputStream.flush();
            objectOutputStream.close();
    
            //反序列化
            ObjectInputStream objectInputStream=new ObjectInputStream(new FileInputStream(file));
            Person s = (Person) objectInputStream.readObject();
            System.out.println(s.toString());
            objectInputStream.close();
        }
    }
    class Person implements Serializable{
        private String name;
        private int age;
        private MyDate myDate;
    }
    class  MyDate implements Serializable{
        private int year;
        private int month;
        private int day;
    }
    
    结果：Person{name='zhangsan', age=18, myDate=MyDate{year=2023, month=5, day=4}}
    ```

    * **存多个对象必须要用List集合，负责会报错**，比如两个person对象

* 注意点：如果不声明全局常量，系统会自动生成针对该类唯一的一个常量，但是如果有方法的增加修改删除，就会反序列化失败，因为常量变了。

* 自定义类的成员类型也得是可序列化的，基本数据类型是天然可序列化的，其他的必须继承Serializable，负责会报错。

* 对于某个属性如果不想进行序列化，就加上transient关键词，就变成了瞬时的，游离的

  ```java
    @Test
      public void test2() throws IOException, ClassNotFoundException {
          //复制功能
          File file = new File("abc.txt");
          ObjectOutputStream objectOutputStream=new ObjectOutputStream(new FileOutputStream(file));
          //写出序列化过程
          Person person=new Person("zhangsan", 18, new MyDate(2023,5,4));
          objectOutputStream.writeObject(person);
          objectOutputStream.flush();//刷新
          objectOutputStream.close();
  
          //反序列化
          ObjectInputStream objectInputStream=new ObjectInputStream(new FileInputStream(file));
          Person s = (Person) objectInputStream.readObject();
          System.out.println(s.toString());
          objectInputStream.close();
      }
  }
  class Person implements Serializable{
      transient private String name;
      private int age;
      private MyDate myDate;
  
      public  Person(){
  
      }
  
      public Person(String name, int age, MyDate myDate) {
          this.name = name;
          this.age = age;
          this.myDate=myDate;
      }
  }
  结果：Person{name='null', age=18, myDate=MyDate{year=2023, month=5, day=4}}
  ```

  * 序列化版本号
    * java语言中是采用什么机制来区分类的?第一:首先通过类名进行比对，如果类名不一样，肯定不是同一个类。第二:如果类名一样，再怎么进行类的区别?靠序列化版本号进行区分。
    * /Java虚拟机看到Serializable接口之后，会自动生成一个序列化版本号。
    * 这里没有手动写出来,java虚拟机会默认提供这个序列化版本号。
    * 建议将序列化版本号手动的写出来。不建议自动生成
    * ![1704614829611](%E5%B8%B8%E8%A7%81IO%E6%B5%81.assets/1704614829611.png)
    * 类似于上面，最好全球唯一

##### 标准输入流输出流

* System.in：标准的输入流，默认从键盘输入

  ```java
  源码中为 public final static InputStream in = null;
  不能修改怎么有set方法
  通用的检查：需要使用安全器校验权限
      private static void checkIO() {
          SecurityManager sm = getSecurityManager();
          if (sm != null) {
              sm.checkPermission(new RuntimePermission("setIO"));
          }
      }
  再调用 private static native void setIn0(InputStream in);
  底层调用了c/c++的代码
  ```

* System.out：标准的输出流(PrinStream)，默认从显示器输出，即从控制台输出

* 通过调用如下的方法，修改输入流和输出流的位置

  * setIn(InputStream is)

  * setOut(PrintStream ps)

    ```java
        public void test2() throws IOException, ClassNotFoundException {
          PrintStream ps=new PrintStream("ac.txt");
          ps.println(1);
          ps.println(1.5);
          System.setOut(ps);
            System.out.println("aa");
            ps.close();
        }//就会输出到文件里而不是控制台
    ```

    

##### 打印流

* PrintStream，不需要手动关闭,System.out对象就是这个

  ````java
  public void test2() throws IOException, ClassNotFoundException {
        PrintStream ps=new PrintStream("ac.txt");
        ps.println(1);
        ps.println(1.5);
        ps.close();
   }
  ````

* 日志输出

  ```java
      public void log(String msg) throws FileNotFoundException {
          PrintStream out=new PrintStream(new FileOutputStream("abc.txt",true));
          System.setOut(out);
          //日期当前时间
          Date nowTime=new Date();
          SimpleDateFormat simpleDateFormat=new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
          String strTime=simpleDateFormat.format(nowTime);
          System.out.println(strTime+":"+msg);
      }
  ```

  

##### apache-common包的使用

* 介绍：lo技术开发中，代码量很大，而且代码的重复率较高，为此Apache软件基金会，开发了Io技术的工具类commonsIo，大大简化了IO开发。|TApahce软件基金会属于第三方，(Oracle公司第一方，我们自己第二方，其他都是第三方)）

  ```java
      @Test
      public void test2() throws IOException, ClassNotFoundException {
          File file=new File("HH.png");
          File file1=new File("HH_copy2.png");
          FileUtils.copyFile(file,file1);
      }
  ```






#### IO和Properties的联合使用

* java规范中有要求﹔属性配置文件建议以.properties结尾，但这不是必须的。

  ```java
      public void test2() throws IOException {
          FileInputStream inputStream=new FileInputStream("info.properties");
          Properties properties=new Properties();
          properties.load(inputStream);
          //等号左边是key，等号右边是value
          String name=properties.getProperty("name");
      }
  ```

  

