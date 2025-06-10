import router from "@/router";
import useSystem from "@/hooks/useSystem";
const { userInfo } = useSystem();
router.beforeEach((to, _, next) => {
  if (userInfo.value?.access) {
    if (to.path === "/login") {
      // 如果登录，并准备进入 Login 页面，则重定向到主页
      next({ path: "/" });
    } else {
      next();
    }
  } else {
    if (to.path === "/login") {
      next();
    } else {
      next("/login");
    }
  }
});
