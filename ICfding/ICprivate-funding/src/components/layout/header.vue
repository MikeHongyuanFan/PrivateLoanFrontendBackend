<template>
    <div class="header">
        <div class="title">
            <h1>{{ pageTitle }}</h1>
            <el-breadcrumb :separator-icon="ArrowRight">
                <el-breadcrumb-item v-for="(crumb, index) in breadcrumbs" :key="index" :to="{ path: crumb.path }"
                    :replace="true">
                    {{ crumb.label }}
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="tool">
            <div class="search">
                <img src="/src/assets/icons/search.png" alt="search" />
                <input v-model="search" @keyup.enter="onEnter" placeholder="search..." />
            </div>
            <el-select class="language" v-model="language" size="large" placeholder="" @change="handleLanguageChange">
                <template #prefix>
                    <div class="pre">
                        <img :src="language === 'en' ? engIcon : chsIcon" alt="flag" class="flag" />
                    </div>
                </template>
                <el-option value="en">
                    <img src="@/assets/icons/eng.png" alt="eng" class="flag" />
                </el-option>
                <el-option value="zh">
                    <img src="@/assets/icons/chs.png" alt="chs" class="flag" />
                </el-option>
            </el-select>
            <el-popover placement="bottom" trigger="hover" width="160" popper-class="user-popover">
                <div class="actions">
                    <div class="action_user">{{ userInfo.name || userInfo.email }}</div>
                    <div class="action" @click="goToSetting">
                        <el-icon>
                            <Edit />
                        </el-icon>
                        <p>Account Setting</p>
                    </div>
                    <div class="action" @click="logOut">
                        <el-icon>
                            <Delete />
                        </el-icon>
                        <p>Logout</p>
                    </div>
                </div>
                <template #reference>
                    <div class="user">
                        <div class="tag">TD</div>
                        <div class="user_info">
                            <h2>{{ userInfo.name || userInfo.email }}</h2>
                            <p>{{ userInfo?.location || user.location }} - {{ userInfo.role }}</p>
                        </div>
                    </div>
                </template>
            </el-popover>
        </div>
    </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router'
import { ref, computed, onMounted } from 'vue'
import { ArrowRight } from '@element-plus/icons-vue'
import { useLocale } from '@/hooks/useLocale'
import engIcon from '@/assets/icons/eng.png'
import chsIcon from '@/assets/icons/chs.png'

import useSystem from '@/hooks/useSystem'

const { userInfo, logOut } = useSystem()
const router = useRouter()
const route = useRoute()
const user = ref({
    name: 'Thomas',
    location: 'Sydney CBD',
    role: 'Admin'
})
const search = ref("")
const language = ref('en')
const { handleLanguageChange } = useLocale()

onMounted(() => {
    const navigatorLanguage = (navigator.language || 'en').toLocaleLowerCase() // 这是获取浏览器的语言
    let lang = localStorage.getItem('lang') || navigatorLanguage.split('-')[0] || 'en'
    language.value = lang
})

const pageTitle = computed(() => route.meta.title || '')
const breadcrumbs = computed(() => route.meta.breadcrumb || [])
const goToSetting = () => {
    router.push({ path: '/setting', query: { tab: 'second' } })
}
const onEnter = () => {
    if (!search.value) return
    router.push({
        path: '/application/index',
        query: { search: search.value }
    })
    search.value = ""
}
</script>

<style lang="scss" scoped>
.header {
    height: 100px;
    padding: 0 20px;
    background: #fff;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
}

.title {
    width: 30%;
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 5px;
}

h1 {
    color: #384144;
    font-size: 1.5rem;
    font-style: normal;
    font-weight: 600;
    line-height: normal;
    margin: 0;
}

.el-breadcrumb-item {
    color: #7A858E;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 400;
    line-height: normal;
}

.tool {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 20px;
}

.search {
    width: 250px;
    height: 32px;
    padding: 0 10px;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 10px;
    border-radius: 15px;
    border: 1px solid #E1E1E1;
}

.language {
    width: 60px;

    :deep(.el-select__wrapper) {
        min-height: 32px;
        padding: 0 7px;
        border-radius: 23px;
        gap: 3px;
    }
}

.flag {
    width: 25px;
    height: 25px;
}

.pre {
    display: flex;
    flex-direction: row;
    align-items: center;
}


.search img {
    width: 24px;
    height: 24px;
}

input {
    border: none;
    width: 90%;
    background: #FFF;
    outline: none;
}

.user {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    gap: 5px;
    cursor: pointer;
}

.tag {
    width: 30px;
    height: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;
    background: #2984DE;
    color: #FFF;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 500;
    line-height: 12px;
}

.user_info {
    display: flex;
    flex-direction: column;
    align-items: start;
    gap: 5px;
}

h2 {
    color: #384144;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 600;
    line-height: 12px;
    margin: 0;
}

p {
    color: #7A858E;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.75rem;
    font-style: normal;
    font-weight: 400;
    line-height: 12px;
    margin: 0;
}

.actions {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.action_user {
    width: 100%;
    padding-bottom: 10px;
    border-bottom: 1.5px solid #E1E1E1;
    color: var(--Color, #272727);
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: 19px;
}

.action {
    display: flex;
    flex-direction: row;
    justify-content: start;
    gap: 10px;
    align-items: center;
    cursor: pointer;
    margin-bottom: 10px;
}

.action:hover {
    color: #2984DE;
}

.action p:hover {
    color: #2984DE;
}
</style>