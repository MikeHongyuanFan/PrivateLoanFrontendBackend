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
                <!-- Handle items with children (sub-menus) -->
                <div v-if="item.children && item.children.length > 1" class="menu-group">
                    <div class="menu parent-menu" 
                        :class="{active: $route.path.startsWith(item.path)}" 
                        v-if="!item.meta.hidden" 
                        @click="toggleSubMenu(item.path)"
                    >
                        <img :src="item.meta.icon" alt="menu" />
                        <p>{{ $t(item.meta.i18nTitle) }}</p>
                        <el-icon class="expand-icon" :class="{ expanded: expandedMenus.includes(item.path) }">
                            <CaretRight />
                        </el-icon>
                    </div>
                    <!-- Sub-menu items -->
                    <div v-show="expandedMenus.includes(item.path)" class="sub-menu">
                        <div v-for="child in item.children" :key="child.path" 
                            class="menu sub-menu-item"
                            :class="{active: $route.path === child.path}"
                            @click="toSubPage(child)"
                        >
                            <p>{{ child.meta.title }}</p>
                        </div>
                    </div>
                </div>
                <!-- Handle regular menu items -->
                <div v-else class="menu" 
                    :class="{active: $route.path.startsWith(item.path)}" 
                    v-if="!item.meta.hidden" 
                    @click="toPage(item)"
                >
                    <img :src="item.meta.icon" alt="menu" />
                    <p>{{ $t(item.meta.i18nTitle) }}</p>
                </div>
            </template>
        </div>
    </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { constantRoutes } from '@/router'
import { useRouter } from 'vue-router'
import useTagView from '@/hooks/useTagView'
import { CaretRight } from '@element-plus/icons-vue'

const router = useRouter()
const expandedMenus = ref([])

const topList = computed(() => {
    return constantRoutes.filter(route => route.meta?.isTop)
})

const bottomList = computed(() => {
    return constantRoutes.filter(route => !route.meta?.isTop)
})

//将选中的菜单添加到TagView中
const { setTagViewList } = useTagView()

// Toggle sub-menu expansion
const toggleSubMenu = (menuPath) => {
    const index = expandedMenus.value.indexOf(menuPath)
    if (index > -1) {
        expandedMenus.value.splice(index, 1)
    } else {
        expandedMenus.value.push(menuPath)
    }
}

// Navigate to sub-page
const toSubPage = (page) => {
    let tag = {
        name: page?.meta?.title || '',
        path: page?.path || '',
    }
    setTagViewList(tag)
    router.push(page.path)
}

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

.menu-group {
    width: 100%;
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
    position: relative;
}

.parent-menu {
    justify-content: space-between;
    padding-right: 10px;
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
    flex: 1;
}

.expand-icon {
    font-size: 12px;
    color: #384144;
    transition: transform 0.3s ease;
}

.expand-icon.expanded {
    transform: rotate(90deg);
}

.sub-menu {
    width: 100%;
    padding-left: 20px;
}

.sub-menu-item {
    padding: 8px 0;
    padding-left: 30px;
    font-size: 11px;
}

.sub-menu-item p {
    font-size: 11px;
    color: #666;
}

.menu:hover {
    background: #EFEFEF;
}

.active {
    background: #EFEFEF;
}

.sub-menu-item.active {
    background: #E0E9FF;
}

.sub-menu-item.active p {
    color: #2984DE;
    font-weight: 600;
}
</style>