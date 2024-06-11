#### java控制流程

* Scanner对象:实现程序和人的交互，jdk1.5出来的

* ```java
  	public static void main(String[] args) {
    		// TODO 自动生成的方法存根
         int a=1,b=2,c=3;
        Scanner scanner=new Scanner(System.in);
        if(scanner.hasNext()) {
      	  //等待输入
      	  String str=scanner.next();
      	  System.out.println(str);
        }
        if(scanner.hasNextLine()) {
      	  //等待输入
      	  String str=scanner.nextLine();
      	  System.out.println(str);
        }
        //IO用完就关
        scanner.close();
    	}
    
  第一个输入hello world
  第一个输出hello
  第二个输出world
     因为next读取遇到空格就结束了，剩下的都给nextline了
  ```

  * next():
    1、一定要读取到有效字符后才可以结束输入。
    2、对输入有效字符之前遇到的空白,next(方法会自动将其去掉。

    3、只有输入有效字符后才将其后面输入的空白作为分隔符或者结束符。

    4、next()不能得到带有空格的字符串。

  * nextLine():
    1、以Enter为结束符,也就是说nextLine()方法返回的是输入回车之前的所有字符。

    2、可以获得空白。

  * hasNextInt():获得下一个整数

    ```java
          if(scanner.hasNextInt()) {
        	  //等待输入
        	  int str=scanner.nextInt();
        	  System.out.println(str);
          }
          else {
        	  System.out.println("输入的不是整数");
          }
    ```

* 顺序结构：依次往下执行

* If选择结构,if(boolean类型)

* switch多选择结构

  * switch(){case value:  语句 break;  default :}
  * break和default都不是必须的，没有break会出现分支穿透
  * case之后为 char、byte、 short 或、int、枚举 的常量表达式。（本质是只支持int和String，但是char、byte、 short可以自动类型转换）
  * case后面跟常量，只能进行等于的判断，不能有范围判断
  * jdk1.7以后case后面可以为字符串了，字符串本质还是数字，可以通过java编译成class，再反编译一下，就会发现代码里的字符串用数字替代了。

* 循环结构

  * while循环

  * for循环

    ```java
  int num = 1;
    for(System.out.print(""a");num < 3;System.out.print("c"),num++){
  		System.out.print(b-);
    }
    输出结果abcbc
            for(int k=1;k<10;){
              k++;
                System.out.println(k);
            }
    ```
    
    
  
* do while循环
  
  * jdk1.5之后出现增强for循环
  
    ```java
           int[] numbers= {10,20,30,40,50};
           for(int x:numbers) {
        	   System.out.println(x);
           }
    ```
  
  * break终止所有循环，contine只终止这一次循环，即不执行下面代码
  
  * for,while,do while可以相互转化
  
  * 无限循环for(;;),while(true)
  
    ```java
    for(int j = 1;j <=4;j++){
         for(int i = 1;i <= 10; i++){
                if(i % 4 == 0){
                     //break;
                    continue;
                 }
                System.out.print(i);
          }
          System.out.println();
    }
    结果123567910
        123567910
        123567910
        123567910
    ```
  
    

* 带标签的breake使用

  ```java
  lable:for(int j = 1;j <=4;j++){
       for(int i = 1;i <= 10; i++){
              if(i % 4 == 0){
                   break lable;
                  //continue lable;
   
               }
              System.out.print(i);
        }
        System.out.println();
  }
  ```

  