#### Vue3

* vue2工程是怎么创建的?
  * 通过vue-cii脚手架来完成创建的。
  * vue-c1i脚手架是基于webpack项目构建工具实现的
* vue3工程也可以通过vue-cli创建。但目前更加流行的方式不是采用vue-cli来创建。目前比较流行的方式是:采用另一个脚手架create-vue来完成vue3工程的创建。
  * create-vue这个脚手架是基于vite项目构建工:.具来实现的。(vite和lwebpack一样，都是项目构建工具。)
* vite创建
  * 使用 create vue 创建 Vue3 工程
    * (1) 官方指导：https://cn.vuejs.org/guide/quick-start.html
    * (2) 安装 create-vue 脚手架并创建 vue3 项目：npm init vue@latest
    * 执行时，如果检测到没有安装 create-vue 脚手架时会安装脚手架。如果检测到已经安装过脚手架，则直接创建项目。 
  *  和 vue-cli 脚手架创建的区别
    * == (1) index.html 文件不再放到 public 目录下了。 vite 官方的解释是：让 index.html 成为入口。（vue-cli 脚手架生成的项目入口是：main.js ==
    *  ue-cli 的配置文件 vue.config.js。create-vue 脚手架的配置文件：vite.config.js
      * vite.config.js 能配置什么？可以参考 vite 官网：https://cn.vitejs.dev/config/ 例如配置代理服务器和以前就不太一样了。 