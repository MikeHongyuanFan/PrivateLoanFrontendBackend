<template>
    <div class="nav">
        <div class="top">
            <img src="/src/assets/logo.png" alt="logo" class="logo" @click="toHome" />
            <template v-for="item in topList" :key="item.path">
                <div class="menu" 
                    :class="{active: item.path === '/' ? $route.path.startsWith('/dashboard') : $route.path.startsWith(item.path)}" 
                    v-if="!item.meta.hidden" 
                    @click="toPage(item)"
                >
                    <img :src="item.meta.icon" alt="menu" />
                    <p>{{ $t(item.meta.i18nTitle) }}</p>
                </div>
            </template>
        </div>
        <div class="bottom">
            <template v-for="item in bottomList" :key="item.path">
                <div class="menu" :class="{active: $route.path.startsWith(item.path)}" v-if="!item.meta.hidden" @click="toPage(item)">
                    <img :src="item.meta.icon" alt="menu" />
                    <p>{{ $t(item.meta.i18nTitle) }}</p>
                </div>
            </template>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { constantRoutes } from '@/router'
import { useRouter } from 'vue-router'
import useTagView from '@/hooks/useTagView'

const router = useRouter()

const topList = computed(() => {
    return constantRoutes.filter(route => route.meta?.isTop)
})

const bottomList = computed(() => {
    return constantRoutes.filter(route => !route.meta?.isTop)
})

//将选中的菜单添加到TagView中
const { setTagViewList } = useTagView()

//todo someThing 这里的菜单应该从配置的路由中取，可优化项，暂时先这么写
const toPage = (page) => {
    let tag = {
        name: page?.meta?.title || '',
        path: page?.redirect || page?.path || '',
    }
    setTagViewList(tag)
    router.push(page.path)
}
const toHome = () => {
    router.push('/')
}
</script>

<style scoped>
.nav {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.logo {
    width: 65%;
    margin-top: 27px;
    margin-bottom: 15px;
    cursor: pointer;
}

.top {
    width: 100%;
    display: flex;
    flex-direction: column;
}

.bottom {
    width: 100%;
    display: flex;
    flex-direction: column;
    margin-bottom: 27px;
}

.menu {
    width: 100%;
    padding: 10px 0;
    border-radius: 5px;
    display: flex;
    flex-direction: row;
    justify-content: start;
    align-items: center;
    gap: 10px;
    cursor: pointer;
}

.menu img {
    width: 20px;
    height: 20px;
    margin-left: 10px;
}

.menu p {
    color: #384144;
    font-size: 12px;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    margin: 0;
}

.menu:hover {
    background: #EFEFEF;
}

.active {
    background: #EFEFEF;
}
</style>