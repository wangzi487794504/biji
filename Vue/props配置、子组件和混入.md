#### props配置

* 可以向组件传递值，而不用写死组件

  ```js
  <script>
  export default {
      name:'SecondVue',
          //可以采用简单的数组形式接受
          //props:['msg']
          //第二种，复杂的，可以指定类型
          // props:{
          //     msg:String
          // }
          ////第三种，最复杂的，可以指定类型，还可以指定默认值
          props:{
              
              msg:{
                  type:String,
                  required:false,
                  default:'aa'
              }
          }
  }
  </script>
  ```

* 注意：这样会渲染失效

  ```js
  import y1 from './FirstVue.vue'
      const y2 = {
         name:'SecondVue',
          props:{
              
              msg:{
                  type:String,
                  required:false,
                  default:'aa'
              }
          }
      };
  export default {
      y2
  }
  ```

* 应该写成这样

  ```js
  <script>
  export default {
      name:'SecondVue',
          props:{
              
              msg:{
                  type:String,
                  required:false,
   default:'aa'
              }
          }
  }
  </script>
  ```

  

* props的属性组件最好不要修改，父组件使用时，会自动变化，如果组件自己想修改，建议使用中间变量



##### 获取子组件

* 使用ref，它既可以拿到子组件，也可以拿到一般的dom元素

  ```js
  <script>
  import HelloWorld from './components/HelloWorld.vue'
  import y2 from './components/SecondVue.vue'
  export default {
    name: 'App',
    components: {
      HelloWorld,
      y2
    },
    methods:{
      yclick(){
        console.log(this.$refs.yfirst);
      }
    }
  }
  </script>
  ```

* 其实使用id，然后documentById也可以，只是在vue中不建议使用





##### 混入

* 代码复用，类似于工具类

  ```js
  export const mix1={
      methods: {
          printInfo(){
              console.log(this.name+','+this.password); 
          }
      },
  }
  ```

* 使用mixins导入，他不会覆盖文件中重名的方法，他的优先级低，如果重名，默认用源文件本身的方法

  ```js
  import {mix1} from '../minin'
  export default {
      name:'SecondVue',
          props:{
              
              msg:{
                  type:String,
                  required:false,
                  default:'aa'
              }
          },
          mixins:[
              mix1
          ]
  }
  ```

  

* 对于钩子函数，重名了会两个都执行，先执行外面的，再执行自己的

* 如果混入太多，可以在main.js中使用全局混入

  ```js
  import { mix1 } from './minin'
  Vue.mixin(mix1)
  ```

  

  