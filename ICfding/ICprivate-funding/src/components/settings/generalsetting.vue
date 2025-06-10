<template>
    <div class="settings">
        <div class="language">
            <div class="text">
                <h1>Locale</h1>
                <p>Preferred language setting</p>
            </div>
            <el-select v-model="general.selectedLanguage" @change="handleLanguageChange" style="width: 100px">
                <el-option
                    v-for="item in languages"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                />
            </el-select>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Start of week</h1>
                <p>Select the first day of the week for calendar and scheduling purposes.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="selectSunday" 
                    :style="{
                        color: general.startWeek === 'Sunday' ? '#FFF' : '#7A858E',
                        background: general.startWeek === 'Sunday' ? '#2984DE' : '#FFF'
                    }"
                >Sunday</div>
                <div class="action" 
                    @click="selectMonday"
                    :style="{
                        color: general.startWeek === 'Monday' ? '#FFF' : '#7A858E',
                        background: general.startWeek === 'Monday' ? '#2984DE' : '#FFF'
                    }"
                >Monday</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Timezone</h1>
                <p>Select the timezone for calendar and scheduling purposes.</p>
            </div>
            <el-select v-model="general.selectedZone" style="width: 150px">
                <el-option
                    v-for="item in timezone"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                />
            </el-select>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Working Hour</h1>
                <p>Set the default working hour.</p>
            </div>
            <el-input v-model="general.workingHour" placeholder="7.5 Hours" style="width: 90px"/>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Currency Settings</h1>
                <p>Select the currency.</p>
            </div>
            <el-select v-model="general.selectedCurrency" style="width: 80px">
                <el-option
                    v-for="item in currency"
                    :key="item.value"
                    :label="item.label"
                    :value="item.value"
                />
            </el-select>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Two-Factor Authentication</h1>
                <p>Enable Two-Factor authentication.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="general.authentication = true" 
                    :style="{
                        color: general.authentication ? '#FFF' : '#7A858E',
                        background: general.authentication ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="general.authentication = false"
                    :style="{
                        color: !general.authentication ? '#FFF' : '#7A858E',
                        background: !general.authentication ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>Email Notifications</h1>
                <p>Enable Email Notifications.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="general.email = true" 
                    :style="{
                        color: general.email ? '#FFF' : '#7A858E',
                        background: general.email ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="general.email = false"
                    :style="{
                        color: !general.email ? '#FFF' : '#7A858E',
                        background: !general.email ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>SMS Alert</h1>
                <p>Enable SMS alert.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="general.sms = true" 
                    :style="{
                        color: general.sms ? '#FFF' : '#7A858E',
                        background: general.sms ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="general.sms = false"
                    :style="{
                        color: !general.sms ? '#FFF' : '#7A858E',
                        background: !general.sms ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
        <div class="setting">
            <div class="text">
                <h1>System Push Notifications</h1>
                <p>Enable System Push Notifications.</p>
            </div>
            <div class="set">
                <div class="action" 
                    @click="general.system = true" 
                    :style="{
                        color: general.system ? '#FFF' : '#7A858E',
                        background: general.system ? '#2984DE' : '#FFF'
                    }"
                >On</div>
                <div class="action" 
                    @click="general.system = false"
                    :style="{
                        color: !general.system ? '#FFF' : '#7A858E',
                        background: !general.system ? '#2984DE' : '#FFF'
                    }"
                >Off</div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';
    import { useLocale } from '@/hooks/useLocale';

    const { handleLanguageChange } = useLocale()

    const props = defineProps({
        general: Object
    })

    const languages = ref([
        {label: "English", value: "en"},
        {label: "简体中文", value: "zh"}
    ])
    const timezone = ref([
        {label: "Sydney UTC+8", value: "Sydney UTC+8"}
    ])
    const currency = ref([
        {label: "AUD", value: "AUD"},
        {label: "USD", value: "USD"}
    ])

    const selectMonday = () => {
        props.general.startWeek = "Monday"
    }
    const selectSunday = () => {
        props.general.startWeek = "Sunday"
    }
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
    .language {
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