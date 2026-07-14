##### 手写Vue

* 读源码

  * 起点，搜索Vue(

    ```js
    
      function Vue(options) {
          if (!(this instanceof Vue)) {
              warn$2('Vue is a constructor and should be called with the `new` keyword');
          }
          this._init(options);
      }
    ```

  *  this._init(options);打断点，刷新，进入这个方法内部

    ```js
    如果是函数，则调用getData(data, vm)来获取data
    如果不是函数，则直接将data返回，给data变量，并且同时将data赋值给vm._data
    data = vm._data = isFunction(data) ? getData(data, vm) : data || {};
    ```

    * vm.\_data是直接指向了底层真是的data对象、，通过_data访问的name和age是不会走数据代理机制的，它是给vue内部使用的
    * 程序员如果不想走代理机制读取，可以使用$data读取

  * 用来判断美元或下划线开始

    ```js
      function isReserved(str) {
          var c = (str + '').charCodeAt(0);
          return c === 0x24 || c === 0x5f;
      }
    ```

  * 数据代理

    ```js
    proxy(vm, "_data", key);
    ```

    ```js
      function proxy(target, sourceKey, key) {//target是vm，sourceKey是_data，key是"age"
          sharedPropertyDefinition.get = function proxyGetter() {
              return this[sourceKey][key];
          };
          sharedPropertyDefinition.set = function proxySetter(val) {
              this[sourceKey][key] = val;
          };
          Object.defineProperty(target, key, sharedPropertyDefinition);
      }
    ```

  * data可以使一个函数，也可以是一个对象，组件的时候用函数

    ```js
                //data可以使一个函数，也可以是一个对象，组件的时候用函数
                data:{
                    msg:'hello',
                    name:'jackson',
                    age:30
                }
                //函数必须要返回对象
                data(){
                    return{
                        mas:'s'
                    }
                }
    ```

    

* 手写vue实现数据代理和方法代理

  ```js
  //定义一个类
  class Vue{
      //定义构造函数
      //option是一个js对象
      constructor(options){
          //获取所有的属性名
          Object.keys(options.data).forEach((param,index)=>{
              console.log(param,index);
              //去掉美元符和下划线
              if (param.charAt(0) != '_' && param.charAt(0) != '$')
              Object.defineProperty(this, param,{
                  get(){
                      //读属性有两种方式，一种是对象.属性名  另一种是对象['属性名']
                      return options.data[param]
                  },
                  set(val){
                      options.data[param]=val;    
                  }
              })
          })
          //获取所有的方法名
          Object.keys(options.methods).forEach((methodName,index)=>{
              console.log(methodName);
              this[methodName] = options.methods[methodName]
          })
      }
  }
  ```

  