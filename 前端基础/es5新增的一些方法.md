##### es5方法

* 数组方法

  * foreach ,map,filter,some,any

  * 遍历

    ```js
            var arr=[1,2,3]
            arr.forEach(function(value,index,array){
                console.log("每一个数组元素"+value);
                console.log("每一个数组元素索引号"+index);
                console.log("数组本身"+array);
            })
            //比如，求和
            arr.forEach(function(value,index,array){
                sum+=value;
            })
    ```

  * 筛选

    ```js
            //筛选，返回一个新数组
            var arr2=[12,64,4,88];
            var newArr=arr2.filter(function(value,index,array){
                return value>=20
            })
    ```

  * some 查看满足条件，返回的是布尔值

    ```js
            //查看满足条件，返回的是布尔值
            var newArr2=arr.some(function(value){
                return value>=20
            })
            var arr3=['a','bb','cccc']
            var flag=arr3.some(function(value){
                return value=='bb'
            }
    ```

    * 如果查找值有一个满足，就退出循环
    * filiter是返回所有满足条件的元祖，并且元素返回出来，some只查一个，返回是一个布尔值

  * 注意：在for each写了return，他也是遍历完才结束

* 字符串方法

  * trim删除一个·字符串两端的空白字符。并且返回一个新的字符串，并不影响原字符串本身

* 定义新属性或者修改原属性

  * 以前是使用对象.属性添加或者修改

    ```js
            //以前新增属性
            var obj={
                id:1,
                pane:'小米'
            }
            obj.num=100;
    ```

  * 现在有一个功能更强的方法

    ```js
            //现在可以通过Object.defineProperty(obj,prop,descriptor)定义对象中新属性或修改原属性
            //obj：必需的。需定义或修改的属性的名字
            //prop：必需。需要定义或修改的属性的名字
            //descriptor必须。目标属性所拥有的特性，以对象的形式书写。value设置属性的值，默认undefined
            //writable:值是否可以重写，默认为false。enumerable：目标属性是否可以被枚举，默认是false
            //configurable：目标属性是否可以被删除或可以再次修改，默认false
            Object.defineProperty(obj,'num',{
                value:1000,
                writable:true,
                descriptor:false,
                configurable:true
            })
    ```

* 对象方法

  * Object.keys()用于获取对象自身所有的属性

    ```js
    Object.keys(obj)
    ```

    * 效果类似于 for…in
    * 返回一个有属性名组成的数组

    ```js
            //以前新增属性
            var obj={
                id:1,
                pane:'小米'
            }
            var arr=Object.keys(obj)
            arr.forEach(function(value){
                console.log(value);
            })
    ```

    
