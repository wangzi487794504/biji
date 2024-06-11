* 第一个

  ```vue
  
  <body>
      <div id="wang"></div>
      <script>
          //创建一个Vue实例
          //为什么要NEW，直接调用Vue函数不行吗
          //答：不行，会报没有对象错误，可以看源码
          //options为选项，这个options参数必须是一个纯粹的JS对象：即{}，这个里面可以写keyvalue对，用于指定配置项
          //template只是其中一个配置项，称为模板语句
          //Vue框架自己制定的一些具有特殊含义的特殊符号，要遵循他的规则以及js代码,会被编译转换成纯粹的js代码
          //         function Vue(options) {
          //       if (!(this instanceof Vue)) {
          //           warn$2('Vue is a constructor and should be called with the `new` keyword');
          //       }
          //       this._init(options);
          //   }
          const myVue = new Vue({
                  template: '<>Hello Vue</h1>'
              })
              //将vue实例挂载到id为app的
              //也可以写成myVue.$mount(document.getElementById('app'))
  
          myVue.$mount('#app')
      </script>
  </body>
  ```

  

* data选项

  ```vue
  <body>
      <div id="wang"></div>
      <script>
          /*d
              data选项给template提供数据支持，它是Vue实例的数据对象
              官网给出的api
              类型：Object | Function
              限制：组件的定义只接受 function。
              如果是对象，Vue 实例的数据对象。Vue 会递归地把 data 的 property 转换为 getter/setter，
              从而让 data 的 property 能够响应数据变化。对象必须是纯粹的对象 (含有零个或多个的 key/value 对)
              data数据是如何插入到模板中的，采用{{data的key}}，vue特有的，这称为插值语法
  
          */
          const myVue = new Vue({
              template: `<h1>最近哈哈哈{{name}},上市与{{time}}，主角{{lead.name}}
                  ,其他演员：{{actors[0].name}},{{actors[1].name}}
                  </h1>`,
              data:{
                  name:'狂飙',
                  time:'2022年',
                  lead:{
                      name:'高齐强',
                      age:'40'
                  },
                  actors:[
                      {
                          name:"anxin"
                      },
                      {
                          name:"高企蓝"
                      }
                  ]
              }
          }).$mount('#wang');
      </script>
  </body>
  ```

  