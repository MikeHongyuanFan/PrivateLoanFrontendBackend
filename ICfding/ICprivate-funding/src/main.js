import { createApp } from "vue";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import "@/router/permission";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";
import i18n from "./locale";

const app = createApp(App);

app.use(ElementPlus);
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.use(router);
app.use(i18n);

app.mount("#app");
