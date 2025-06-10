<template>
    <div class="settings">
        <div class="email">
            <div class="text">
                <h1>Login Email</h1>
                <p>Set login email.</p>
            </div>
            <el-input v-model="account.email" placeholder="Your email" style="width: 220px"/>
        </div>
        <!-- <div class="setting">
            <div class="text">
                <h1>Password</h1>
                <p>Set login password.</p>
            </div>
            <div class="password">
                <el-input
                    v-model="account.password"
                    type="password"
                    :placeholder=account.password
                    show-password
                    style="width: 150px"
                />
                <button>Change</button>
            </div>
        </div> -->
        <div class="setting">
            <div class="text">
                <h1>Account First Name</h1>
                <p>Set Account Name.</p>
            </div>
            <el-input v-model="account.first_name" :placeholder=account.first_name style="width: 150px"/>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Account Last Name</h1>
                <p>Set Account Name.</p>
            </div>
            <el-input v-model="account.last_name" :placeholder=account.last_name style="width: 150px"/>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Account Phone Number</h1>
                <p>Set Account Contact Number.</p>
            </div>
            <el-input v-model="account.phone" :placeholder=account.phone style="width: 150px"/>
        </div>
        <div class="setting" v-if="account.role !== 'admin'">
            <div class="text">
                <h1>Your Role</h1>
                <p>If your role changes, please contact your admin.</p>
            </div>
            <el-input v-model="account.role" disabled :placeholder=account.role style="width: 150px"/>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        account: Object
    })
</script>

<style scoped>
    .settings {
        width: 100%;
        padding: 20px 0;
    }
    .text {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 1rem;
        font-style: normal;
        font-weight: 500;
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
    .email {
        width: 100%;
        padding: 20px 0;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    .setting {
        width: 100%;
        padding: 20px 0;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
        border-top: 1.5px solid #EAEFF2;
    }
    .password {
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 10px;
    }
    button {
        padding: 6px 20px;
        border-radius: 3px;
        background: #2984DE;
        border: none;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        color: #FFF;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 19px;
    }
</style>