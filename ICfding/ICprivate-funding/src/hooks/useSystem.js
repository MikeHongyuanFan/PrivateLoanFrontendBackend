import { ref } from "vue";
import router from "@/router";
const userInfo = ref({});

export default function useSystem() {
  let user = localStorage.getItem("userInfo");
  if (user) {
    user = JSON.parse(user);
    setUserInfo(user);
  }

  function setUserInfo(data) {
    userInfo.value = data;
    localStorage.setItem("userInfo", JSON.stringify(data));
  }

  function logOut() {
    localStorage.removeItem("userInfo");
    userInfo.value = {};
    router && router.replace("/login");
  }
  return {
    userInfo,
    logOut,
    setUserInfo,
  };
}
