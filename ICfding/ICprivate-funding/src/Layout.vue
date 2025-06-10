<template>
    <el-container class="mainpage">
        <el-aside class="sidebar" :style="{ '--el-aside-width': '17%' }">
            <Navbar></Navbar>
        </el-aside>
        <el-container class="content">
            <el-header height="130px" :style="{ '--el-header-padding': '0' }" class="heading">
                <Header></Header>
                <TagView></TagView>
                <!-- <div class="navbar"></div> -->
            </el-header>
            <el-scrollbar class="app-main">
                <el-main class="main">
                    <router-view>
                        <template #default="{ Component, route }">
                            <keep-alive>
                                <component :is="Component" :key="route.path" v-if="route.meta.keepAlive" />
                            </keep-alive>
                            <component :is="Component" :key="route.path" v-if="!route.meta.keepAlive" />
                        </template>
                    </router-view>
                </el-main>
            </el-scrollbar>
        </el-container>
    </el-container>
</template>

<script setup>
import Header from '@/components/layout/header.vue';
import Navbar from './components/layout/navbar.vue';
import TagView from './components/layout/TagView.vue';

//请求示例
// import { onMounted } from 'vue';
// import { api } from '@/api'

// onMounted(async () => {
//     const [err, res] = await api.notifications()
//     if (!err) {
//         console.log(res);
//     } else {
//         console.log(err)
//     }
// })

</script>

<style scoped>
.mainpage {
    width: 100%;
    height: 100vh;
    padding: 0;
    display: flex;
    flex-direction: row;
    background: #FAFAFA;
}

.sidebar {
    width: 17%;
    height: 100vh;
    padding: 0 10px;
    overflow-y: auto;
    background: #FFF;
    border-right: 1px solid #E1E1E1;
    display: flex;
    justify-content: center;
    align-items: center;
}

.sidebar::-webkit-scrollbar {
    width: 0;
    height: 100%;
}

.content {
    width: 83%;
    height: 100vh;
    overflow-y: auto;
}

.heading {
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 0;
    position: sticky;
    top: 0;
}

.app-main {
    height: calc(100vh - 130px);
}

.main {
    height: calc(100vh - 130px);
    padding: 20px;
}
</style>