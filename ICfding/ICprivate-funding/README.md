# Vue 3 + Vite

This template should help get you started developing with Vue 3 in Vite. The template uses Vue 3 `<script setup>` SFCs, check out the [script setup docs](https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup) to learn more.

Learn more about IDE Support for Vue in the [Vue Docs Scaling up Guide](https://vuejs.org/guide/scaling-up/tooling.html#ide-support).

## locale
- 该文件夹是存放语言包的文件夹
- 每个语言包下的index是单独的入口，把子模块的语言包都引入进来，比如system模块
- 在页面使用`$t('xx.xxxx')`语法来获取语言包中的值
- 比如获取system模块下的dashboard的值，`$t('system.dashboard')`
