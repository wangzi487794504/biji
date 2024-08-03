#### ES6扩展运算符和优化

* 扩展运算符

  ```js
    <script>
      let arr=[1,2,3,4,5,6]
      //会把arr拆分
      console.log(...arr);
      let o1={
        x:1,
        y:1
      }
      //这会生成一个新的对象，地址不一样
      let o2={...o1}
      //一般用于属性的合并，生成一个全新的对象
      let o3={
        x:1,
        y:1
      }
      let o4={
        j:1,
        k:1
      }
      let o5={...o3,...o4}
      //第二种方式
      let o6={
        k:1,
        ...o3
      }
    </script>
  ```

  

  

  

  

#### 优化计算属性

*  组件中在使用 state 上的数据和 getters 上的数据时，都有固定的前缀：

  * {{this.$store.state.name}}
  * {{this.$store.getters.reverseName}}

*  使用 mapState 和 mapGetters 进行名称映射，可以简化以上的写法 

* 之前的的案例虽然简化了代码，但是还不够简化，因此vuex又优化了计算属性

  * 之前的案例可以改写成

    ```js
    <template>
        <div>
        <h3>字符串翻转</h3>
        <input type="text" v-model="reversedName">
        <br>
        <h3>反转之后的用户名: {{reversedName}}</h3>
      </div>
    </template>
    
    <script>
    export default {
        name:'Name',
        computed:{
            reversedName(){
                return $store.store.getters.reversedName
            }
        }
    }
    </script>
    ```

  * 我们可以发现计算属性的代码是固定的，因此，Vuex借助ES6扩展运算符帮助我们简化了这些代码

    * 之前的vuex.js

      ```js
      const state = {
          //可以看做vue的data
          name:''
      }
      //每一个getter可以看做计算属性
      const getters={
          reversedName(state){
              return state.name.split('').reverse().join('');
          }
      }
      ```

    * 使用

      ```js
      <template>
          <div>
          <h3>字符串翻转</h3>
          <input type="text" v-model="name">
          <br>
          <h3>反转之后的用户名: {{reversedName}}</h3>
        </div>
      </template>
      
      <script>
      import { mapGetters, mapState } from 'vuex';
      
      export default {
          name:'Name',
          computed:{
              // //数组形式，这种表明计算属性的名字和state中的属性名一致
              // ...mapState(['reversedName'])
              //对象形式
              ...mapState({name:'name'}),
              ...mapGetters(['reversedName'])
          }
      }
      ```

    * 如果使用双向绑定，这个代码有问题，因为...mapState是return state.name.split('').reverse().join('');这行代码的简写，相当于只实现了计算属性的get方法，没有实现set方法