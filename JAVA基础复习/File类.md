#### File类

* 位于java.io包下，他不是一个流，继承的是Object，所以它没有读和写的功能

* File类的一个对象，对应于文件目录,是文件与目录名的一种表示方式

* 路径表示方式

  * 绝对路径，包括盘符在内的文件或文件目录的完整路径 \\\与/等价
  * 相对路径:比如在idea中，使用单元测试方法相对于当前module，main相对于project

* 三种构造方法

  ```java
          File file = new File("F:\\keil5stm32/main.txt");//现在还是内存里的一个对象，还没有在物理层面创建
          File file1 = new File("abc");
          File file2 = new File("F:\\keil5stm32/", "aa");//在父目录下面创建一个子的，参数一一定是个文件目录，参数二文件目录或文件，就看有没有后缀
          new File(file2,"f");//变成了F:\keil5stm32\aa\f
  ```

* 常用方法

  ```java
      public void test1() throws IOException {
  //        File file = new File("F:\\keil5stm32/main.txt");//现在还是内存里的一个对象，还没有在物理层面创建
          File file1 = new File("abc.txt");
          System.out.println(file1.getName());//abc
          System.out.println(file1.getAbsolutePath());//G:\ideaspace\basic\abc
          System.out.println(file1.getAbsoluteFile());//G:\ideaspace\basic\abc
          System.out.println(file1.getParent());//获取父目录null，因为是相对路径
          System.out.println(file1.getPath());//abc
          System.out.println(file1.length());//0
          System.out.println(file1.lastModified());//0最后一次的修改时间
  
  
      }
  
  //上面的代码不会在磁盘中建立文件
  手动建立新建一个文件并输入4个数字后
    abc.txt
  G:\ideaspace\basic\abc.txt
  G:\ideaspace\basic\abc.txt
  null
  abc.txt
  4
  1692190948749
  ```

  

* 遍历方法,list返回String数组，仅仅是名字，而listFiles是返回File类的引用

  ```java
      public void test1() throws IOException {
          /*
          列出目录的下一集
           */
          File file1 = new File("F:\\keil5stm32");
          //返回String数组，返回File目录的所有子文件和子目录
          String[] files=file1.list();
          for (String file : files) {
              System.out.println(file);
          }
          //返回File数组，返回File目录的所有子文件和子目录
          File[] files1 = file1.listFiles();
          for (File file : files1) {
              System.out.println(file1.getName());
          }
      }
  CORE
  OBJ
  STM32F10x_FWLib
  USER
  数码管
  keil5stm32
  keil5stm32
  keil5stm32
  keil5stm32
  keil5stm32
  ```

  

* 重命名

  ```java
      @Test
      public void test1() throws IOException {
          /*
          列出目录的下一集
           */
          File file1 = new File("abc.txt");
          //重命名
          File file2 = new File("aa.txt");
          boolean b = file1.renameTo(file2);//要求file1必须存在且修改后的文件名字必须不冲突
          System.out.println(b);
  
      }
  ```

  

* 一些判断的方法

  ```java
      @Test
      public void test1() throws IOException {
          /*
          列出目录的下一集
           */
          File file1 = new File("abc.txt");
          //判断存在，可读,可写，隐藏,是不是目录
          System.out.println(file1.exists());
          System.out.println(file1.canRead());
          System.out.println(file1.canWrite());
          System.out.println(file1.isHidden());
          System.out.println(file1.isDirectory());
  
      }
  true
  true
  true
  false
  false
  ```

  

* 创建删除的方法

  ```java
      @Test
      public void test1() throws IOException {
          /*
          列出目录的下一集
           */
          File file1 = new File("ac.txt");
          //文件创建删除（不进回收站），文件目录删除（删除他文件目录里不能有任何东西）
          if (!file1.exists()){
              boolean isSucceed = file1.createNewFile();
              if (isSucceed){
                  System.out.println("创建成功");
              }else {
                  System.out.println("此文件已经存在");
                  boolean delete = file1.delete();
                  if (delete){
                      System.out.println("文件删除成功");
                  }
                  else {
                      System.out.println("删除失败");
                  }
              }
          }
          //生成目录，区别mkdirs可以生成多级目录，父目录不在会自动创建
          File file = new File("io");
          boolean mkdir = file.mkdir();
          File file2 = new File("io2");
          boolean mkdirs = file.mkdirs();
          //删除
          boolean delete = file.delete();
          System.out.println(delete);
  
      }
  ```

  

* 练习题：过滤器的实现

  ```java
      @Test
      public void test1() throws IOException {
          /*
          列出目录的下一集
           */
          File file1 = new File("D:\\360MoveData\\Users\\lenovo\\Desktop\\cjr\\src\\main\\resources\\static\\img");
          //方式一
          String[] list = file1.list();
          for (String s : list) {
              if (s.contains(".png")){
                  System.out.println(s);
              }
          }
          //方式二
          String[] list1 = file1.list(new FilenameFilter() {
              @Override
              public boolean accept(File dir, String name) {
                  //name为子文件或子文件目录的名称
                  boolean b = name.endsWith(".png");
                  if (b) {
                      return true;
                  }
                  return false;
              }
          });
          for (String s : list1) {
              System.out.println(s);
          }
  
      }
  ```

  