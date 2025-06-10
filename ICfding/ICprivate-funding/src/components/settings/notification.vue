<template>
    <div class="settings">
        <div class="popup_setting">
            <div class="text">
                <h1>Pop up notification on desktop</h1>
                <p>Turn on the notification on desktop as popup.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="notification.popup = true" 
                    :style="{
                        color: notification.popup ? '#FFF' : '#7A858E',
                        background: notification.popup ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="notification.popup = false"
                    :style="{
                        color: !notification.popup ? '#FFF' : '#7A858E',
                        background: !notification.popup ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Turn on all application notifications</h1>
                <p>Turn on the notification of all applications.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="notification.application = true" 
                    :style="{
                        color: notification.application ? '#FFF' : '#7A858E',
                        background: notification.application ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="notification.application = false"
                    :style="{
                        color: !notification.application ? '#FFF' : '#7A858E',
                        background: !notification.application ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Turn on all messages</h1>
                <p>Turn on the notification of all messages.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="notification.message = true" 
                    :style="{
                        color: notification.message ? '#FFF' : '#7A858E',
                        background: notification.message ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="notification.message = false"
                    :style="{
                        color: !notification.message ? '#FFF' : '#7A858E',
                        background: !notification.message ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Turn on all changes</h1>
                <p>Turn on the notification of all changes.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="notification.change = true" 
                    :style="{
                        color: notification.change ? '#FFF' : '#7A858E',
                        background: notification.change ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="notification.change = false"
                    :style="{
                        color: !notification.change ? '#FFF' : '#7A858E',
                        background: !notification.change ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
    </div>
</template>

<script setup>
    const props = defineProps({
        notification: Object
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
    .popup_setting {
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
    .set {
        padding: 5px;
        display: flex;
        flex-direction: row;
        gap: 5px;
        border-radius: 5px;
        border: 1.5px solid #EAEFF2;
        background: #FDFDFD;
    }
    .action {
        padding: 6px 12px;
        border-radius: 3px;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 12px;
        cursor: pointer;
    }
</style>