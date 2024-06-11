#### es6的类与对象

* 在js6中新增了类的概念，可以使用class关键字神功一个雷，之后采用这个类来实例化对象

  * 创建类语法

    ```html
        <script>
            //创建类
            class Star{
            }
            //使用类
            new Star();
        </script>
    ```

  * 构造函数：constructor  注意：类里面的所有函数都不需要加function

    * 只要new一个实例，自动调用constructor  方法，并接受传过来的参数，同时返回实例对象

    ```html
        <script>
            //创建类
            class Star{
                constructor(uname){
                    this.uname=uname
                }
            }
            //使用类
            var liudehua=new Star('liudehua');
            console.log(liudehua.uname)
        </script>
    ```

  * 添加共有的方法

    ```html
        <script>
            //创建类
            class Star{
                constructor(uname){
                    this.uname=uname
                }
                //多个函数之间不能添加逗号分隔
                sing(){
                    console.log("aa")
                }
            }
            //使用类
            var liudehua=new Star('liudehua');
            console.log(liudehua.uname)
        </script>
    ```

* 类的继承

  * 语法

    ```html
        <script>
            class Father{
                constructor(x,y){
                    this.x=x
                    this.y=y
                }
                money(){
                    console.log(100)
                }
                sum(){
                    console.log(this.x+this.y)
                }
            }
            class Son extends Father{
                //继承父类的构造方法
                constructor(x,y){
                    super(x,y);//调用父类中的构造函数
                }
            }
            new Son(1,2).money();
        </script>
    ```

  * super除了父类调用构造函数，也能也能调用子类的

  * 方法调用原则：就近原则

  * ==super必须放到this前面==

* 注意事项

  * 必须先有类，才能new对象，即类的代码必须在实例化的前面

  * 共有的属性和方法一定要加this

  * 类中的this问题：constructor这里的this指向的是实例对象，方法中的this指向的是调用者

    ```html
    <body>
        <button >点击</button>
        <script>
            class Father{
                constructor(x,y){
                    // constructor这里的this指向的是实例对象
                    this.x=x
                    this.y=y
                }
                sum(){
                    console.log(this)
                    //这里的this指向的是btn这个调用按钮
                    console.log(this.x+this.y)
                }
                dianji(){
                    console.log(this);
                    this.button=document.querySelector('button')
                    this.button.onclick=this.sum();
                }
            }
            class Son extends Father{
                //继承父类的构造方法
                constructor(x,y){
                    super(x,y);//调用父类中的构造函数
                }
            }
            var fa=new Father(2,3)
            fa.dianji();
            new Son(1,2);
        </script>
    </body>
    ```

  * 方法三的解决办法：使用全局变量

    ```html
            var _that
            class Father{
                constructor(x,y){
                    _that=this
                    // constructor这里的this指向的是实例对象
                    this.x=x
                    this.y=y
                    this.uname='aa'
                }
                sum(){
                    console.log(this)
                    //这里的this指向的是btn这个调用按钮
                    console.log(_that.uname);
                    console.log(this.x+this.y)
                }
                dianji(){
                    console.log(this);
                    this.button=document.querySelector('button')
                    this.button.onclick=this.sum();
                }
            }
    ```

    

