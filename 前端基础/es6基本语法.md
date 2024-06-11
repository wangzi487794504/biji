##### es6基本语法

* let
  * 只在块级有效，不存在变量提升
  
  * 存在暂时性死区：就是需要先声明后使用
  
    ![1712114670393](es6%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95.assets/1712114670393.png)
  
    * 循环中不会执行这个函数，的等到循环结束，等到调用才会执行。而函数内部并没有定义i的代码，根据作用域链查找原则，要去上一层查找，上一层就是全局i
  
  * ![1712114461838](es6%E5%9F%BA%E6%9C%AC%E8%AF%AD%E6%B3%95.assets/1712114461838.png)
  
    * 他会去自己的块级作用域去寻找i
    * 每一次循环都会产生一个块级作用域（==因为一个循环对应一个大括号==），每一个块级作用域的变量都是不同的
  
* const

  * 声明常量，内存地址不能修改，声明时必须要给初始值，不存在变量提升
  * 具有块级作用域
  * 常量赋值后，值不能修改

* 数组解构

  * ES6允许从数组中提取值，按照对应的位置，对变量赋值，对象也可以实现解构

    ```js
            let [a,b,c]=[1,2,3]
            console.log(a);
            console.log(b);
            console.log(c);
            //数组解构
            let ary=[1,2.3];
            let [d,e,f]=ary;
    ```

    * 解构不成功就是undefined

* 对象解构

  * 变量的名字匹配对象的属性

    ```js
            let person={name:'lisi',age:30,sex:'男'}
            let {name,age,sex}=person
    ```

  * 也可以起别名

    ```js
            let person={name:'lisi',age:30,sex:'男'}
            let {name:myname,age:mysge,sex:mysex}=person
    ```

* 箭头函数()=>{}

  * 用来简化函数定义语法

  * 函数体重只要一句代码，切点啊执行结果就是返回值，可以省略大括号

    ```js
    const sum=(n1,n2)=> n1+n2;
    ```

  * 如果只有一个参数，可以省略小括号

  * 箭头函数不绑定this关键字，箭头函数中的this，指向的是函数定义未知的上下文this

* 剩余参数

  * 将不定数量的参数表示成一个数组

    ```js
     function aa(a,...arg){
                //此时arg就是一个数组
      };
    ```

    * 这个支持箭头函数，arguments不支持箭头函数

      ```js
      function say(name,message){
      	alert('Hello'+arguments[0]+','+arguments[1]);
      }
      ```

  * 可以和解构配合在一起使用

    ```js
            let students=['s','v','c']
            let [s1,...s2]=students;
    ```

* 扩展运算符

  * 扩展运算符可以讲数组或者1对象转换为逗号分隔的参数序列

    ```js
    lert ary=[1,2,3]
    console.log(...ary)//1 2 3
    ```

  * 合并数组

    ````js
            let students=['s','v','c']
            let students2=['a','b','c']
            let ary1=[...students,...students2]
    ````

    也可以用下面这个方法

    ```js
            let students=['s','v','c']
            let students2=['a','b','c']
            students.push(students2)
    ```

  * 将伪数组扩展为真正的数组

    ```js
            let divs=document.getElementsByTagName('div')
            rdivs=[...divs]
    ```

    也可以用Arrary.form()方法

    ```js
            var ar={
                "0":"a",
                "2":"b",
                "3":"c"
            }
            var arr=Array.from(ar)
    ```

    还可以接收函数

    ```js
            var ar={
                "0":1,
                "2":2,
                "3":3
            }
            var arr=Array.from(ar,item=>item*2)
    ```

* find方法

  * 找出第一个符合条件的数组成员，如果没有找到返回undefined

    ```js
            var ary2=[{
                id:1,
                name:'李四'
            },{
                id:2,
                name:'zhangsan'
            }]
            let target=ary2.find(item=>item.id==2)
    ```

  * findIndex找到一个符合条件的索引位置，找不到-1

    ```js
            var ary2=[{
                id:1,
                name:'李四'
            },{
                id:2,
                name:'zhangsan'
            }]
            let target=ary2.findIndex(item=>item.id==2)
    ```

    

  * includes() 查看数组中是否包含指定的值

    ```js
    [1,2,3].includes(2)//true
    ```

    * 以前用indexof

    

  * 模板字符串：使用反引号创建，在字符串中可以解析变量

    ```js
            let name='张三'
            let muban=`模板字符串${name}`
    ```

    模板字符自带换行

    ```js
            let html={
                name:'zhansan',
                age:'20'
            }
            let htmlmuban=`
                <div>
                    <span>${html.name}</span>
                    <span>${html.age}</span>
                </div>
            `
    ```

    模板字符串可以调用函数

    ```js
            function aa2(a,...arg){
            };
            let fmuban=`${aa2()} 哈哈哈哈`;
    ```

    

    

* String的扩展方法

  * startsWith  //看是不是在头部，返回布尔类型

  * endsWith //看是不是在尾部，返回布尔类型

  * repeat（）将原字符串重复n次，返回一个新的字符串

    ```js
    'x'.repeat(3)//'xxx'
    ```

  

  

* Set数据结构

  * 不存储重复值

  * Set本身是一个构造函数，用来生成实例

    ```js
            const s=new Set();
            const set=new Set([1,2,3,]);
           console.log(set.size);//3
    ```

  * 作用：数组去重

    ```js
            const set=new Set([1,2,3,2,3]);
            //会把重复值去掉
            console.log(set.size);//3
    ```

  * 常用方法：add() 返回Set结构本身,delete()返回布尔值,has(value)返回布尔值，表示是否存在，clear()清除所有成员

  * 遍历：foreach，没有返回值

    ```js
    s.foreach(value=>console.log(value))
    ```

    

  