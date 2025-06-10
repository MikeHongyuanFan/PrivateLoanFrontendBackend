import { ref } from "vue";
import { useRouter } from "vue-router";
const tagViewList = ref([]);
const selectTagView = ref(0);
export default function useTagView() {
  const router = useRouter();

  //添加tagViewList
  function setTagViewList(item) {
    const findIndex = tagViewList.value.findIndex((i) => {
      return i.path === item.path;
    });

    if (findIndex === -1) {
      tagViewList.value = [...tagViewList.value, item];
      selectTagView.value = tagViewList.value.length - 1;
    } else {
      selectTagView.value = findIndex;
    }
  }

  //移除tagViewList
  function removeTagViewList(item) {
    tagViewList.value = tagViewList.value.filter((i) => {
      return i.path !== item.path;
    });
    const findIndex = tagViewList.value.findIndex((i) => {
      return i.path === tagViewList.value[selectTagView.value]?.path;
    });
    if (findIndex === -1) {
      selectTagView.value = tagViewList.value.length - 1;
    }
    if (tagViewList.value.length === 0) {
      setTagViewList({
        name: "Overview",
        path: "/",
      });
      selectTagView.value = 0;
      router.push("/");
    }
  }

  //更新当前选中，暂时没有设置选中样式
  function updateTagViewCurrent(index) {
    selectTagView.value = index;
  }

  return {
    tagViewList,
    selectTagView,
    setTagViewList,
    removeTagViewList,
    updateTagViewCurrent,
  };
}
