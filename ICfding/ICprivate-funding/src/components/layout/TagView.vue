<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router'
import { Close } from '@element-plus/icons-vue'
import useTagView from '@/hooks/useTagView'
const routes = useRoute()
const router = useRouter()
const { tagViewList, selectTagView, setTagViewList, removeTagViewList, updateTagViewCurrent } = useTagView()

onMounted(() => {
    let tag = {
        name: routes?.meta?.title || '',
        path: routes?.path || '',
    }
    setTagViewList(tag)
})

const closeTag = (item) => {
    removeTagViewList(item)
    router.push({
        path: tagViewList.value[selectTagView.value].path
    })
}

const handleShowView = (item, index) => {
    updateTagViewCurrent(index)
    router.push(item?.path || '/')
}
</script>

<template>
    <el-scrollbar class="scroll-view">
        <div class="tag-view">
            <div :class="selectTagView === index ? 'item active' : 'item'" v-for="(item, index) in tagViewList"
                :key="index" @click="handleShowView(item, index)">
                {{ item?.name || '' }}
                <el-icon class="icon" @click.prevent.stop="closeTag(item)">
                    <Close />
                </el-icon>
            </div>
        </div>
    </el-scrollbar>
</template>

<style lang="scss" scoped>
.scroll-view {
    height: 30px;
}

.tag-view {
    width: 100%;
    height: 30px;
    background: #F5F7FB;
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    padding: 6px 0;

    .item {
        display: flex;
        justify-content: center;
        align-items: center;
        color: #7A858E;
        padding: 0 20px;
        cursor: pointer;
        font-size: 12px;
    }

    .icon {
        margin-left: 10px;
    }

    .item+.item {
        border-left: 1.5px solid #7A858E;
    }

    .active {
        color: #000;
        font-size: 12px;
    }
}
</style>