<template>
    <div class="setting">
        <div class="tabbar">
            <el-tabs v-model="activeName" class="tabs" >
                <!-- <el-tab-pane name="1">
                    <template #label>
                        <div class="label">General Setting</div>
                    </template>
                </el-tab-pane> -->
                <el-tab-pane name="2">
                    <template #label>
                        <div class="label">Account Setting</div>
                    </template>
                </el-tab-pane>
                <!-- <el-tab-pane name="3">
                    <template #label>
                        <div class="label">Notification</div>
                    </template>
                </el-tab-pane>
                <el-tab-pane name="4">
                    <template #label>
                        <div class="label">Other</div>
                    </template>
                </el-tab-pane> -->
            </el-tabs>
            <Save @click="saveSetting"></Save>
        </div>
        <!-- <GeneralSetting v-if="activeName === '1'" :general="general"></GeneralSetting> -->
        <AccountSetting v-if="activeName === '2'" :account="userInfo"></AccountSetting>
        <!-- <Notification v-if="activeName === '3'" :notification="notification"></Notification>
        <Other v-if="activeName === '4'"></Other> -->
    </div>
</template>

<script setup>
    import { ref, onMounted } from 'vue';
    import { useRoute } from 'vue-router';
    import { api } from '@/api';
    import { ElMessage, ElMessageBox } from 'element-plus';
    import Save from '@/components/buttons/save.vue';
    import GeneralSetting from '@/components/settings/generalsetting.vue';
    import AccountSetting from '@/components/settings/accountsetting.vue';
    import Notification from '@/components/settings/notification.vue';
    import Other from '@/components/settings/other.vue';

    const route = useRoute()
    const activeName = ref('2')
    const general = ref({
        selectedLanguage: "English",
        selectedZone: "Sydney UTC+8",
        startWeek: "Monday",
        workingHour: "7.5 Hours",
        selectedCurrency:"AUD",
        authentication: false,
        email: false,
        sms: false,
        system: false
    })
    const notification = ref({
        popup: false,
        application: false,
        message: false,
        change: false
    })
    const userInfo = ref({})

    onMounted(() => {
        if (route.query.tab) {
            activeName.value = route.query.tab;
        }
        getProfile()        
    });

    const saveSetting = async () => {
        if (activeName.value === "first") {
            console.log("Current settings:", { ...general.value })
        } else if (activeName.value === "2") {
            const data = {
                email: userInfo.value.email,
                first_name: userInfo.value.first_name,
                last_name: userInfo.value.last_name,
                phone: userInfo.value.phone
            }
            const [err, res] = await api.putUser(userInfo.value.user_id, data)
            if (!err) {
                console.log(res)
            } else {
                ElMessage.error({
                    message: err.message || 'Failed to save',
                    type: 'error'
                });
            }
        } else {
            console.log("Current settings:", { ...notification.value })
        }
    }
    const getProfile = async () => {
        const [err, res] = await api.getProfile()
        if (!err) {
            console.log(res)
            userInfo.value = res
        } else {
            console.log(err)
            ElMessage.error({
                message: err.message || 'Failed to get profile',
                type: 'error'
            });
        }
    }
</script>

<style scoped>
    .setting {
        padding: 20px;
        border-radius: 3px;
        background: #FFF;
    }
    .tabbar {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .tabs {
        --el-color-primary: #2984DE;
    }
    .label {
        color: #949494;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 400;
        line-height: 12px;
    }
    .tabs ::v-deep(.el-tabs__item.is-active .label) {
        color: #2984DE;
    }
</style>