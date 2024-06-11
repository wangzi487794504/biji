#### IO流

* 在java中，对于数据的输入输出以“流”的方式进行，可以看做是一种数据的流动

  * input外部磁盘到内存（程序）
  * output内存到物理存储

* 流的分类

  * 按流向分为输入流和输出流
  * 按操作的数据单位分为字节流和字符流
    * 字节流以字节为单位，以InputStream和OutputStream结尾，字节就是byte（8个二进制位），**什么都可以读取**
    * ‘c’在windows上是一个字节，但在java里的char是两个字节，但是没有什么关系，一个是真是存储，一个是java分配空间
    * 字符流以字符为单位，以Reader,Writer结束，字符就是char，只能读取纯文本
  * 根据IO的角色不同分为节点流和处理流
    * 节点流：直接从数据源或目的地读写数据
    * 处理流：不直接连到数据源或者目的地，而是连接已经存在的流之上，通过对数据的处理提供更强大的读写功能。

* 流的API，四大家族，Stream结尾的都是字节流。Reader和Writer结尾的都是字符流。**注意：看结尾**

  * **这四个都是抽象类，继承Object，实现接口Closeable（他有个方法叫做close）**
  * 所有输出流还有一个Flushable 接口（他有一个flush方法，用于刷新，把管道未输出的强行清空）
  
* 

  * | 抽象基类 |   输入流    |    输出流    |
    | :------: | :---------: | :----------: |
    |  字节流  | InputStream | OutputStream |
    |  字符流  |   Reader    |    Writer    |

    

  * 其他流都是在此基础上派生出来的，一般掌握这16个

    <img src="IO%E6%B5%81%E5%8E%9F%E7%90%86.assets/1692236427178.png" alt="1692236427178" style="zoom:80%;" />

  * 基本用派生流，蓝色为重点

    ![1704543247737](IO%E6%B5%81%E5%8E%9F%E7%90%86.assets/1704543247737.png)
  
  

* jdk7语法

  * try-with-resources（资源自动关闭）

  * 凡是实现了AutoCloseable接口的流都可以使用try-with-resources，都会自动关闭，所有流都实现了这个接口

    ```java
        public void test() {
                try(FileInputStream in =new FileInputStream("aa.txt")){
    
                }catch(FileNotFoundException e){
                    System.out.println(e.getMessage());
                }catch(IOException e){
                    System.out.println(e.getMessage());
                }
        }
    ```

    * 这样会自动关闭

  * 也可以写多个

    ```java
        public void test() {
            try (FileInputStream in = new FileInputStream("aa.txt");
                    FileInputStream in2 = new FileInputStream("bb.txt")) {
            } catch (FileNotFoundException e) {
                System.out.println(e.getMessage());
            } catch (IOException e) {
                System.out.println(e.getMessage());
            }
        }
    ```

    