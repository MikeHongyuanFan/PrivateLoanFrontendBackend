<template>
    <div class="content">
        <div v-if="!detail.security_properties.length">
            <p>No security properties in this application</p>
        </div>
        <div class="form" v-for="(s, index) in detail.security_properties" :key="index">
            <div class="index"><h1>Property {{ index + 1 }}</h1></div>
            <div class="item">
                <p class="title">Full Address</p>
                <p>{{ s.address || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Property Type</p>
                <p>{{ s.type || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Bedrooms</p>
                <p>{{ s.bedroom || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Bathrooms</p>
                <p>{{ s.bathroom || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Car Spaces</p>
                <p>{{ s.carSpace || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Building Size(sqm)</p>
                <p>{{ s.buildingSize || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Land Size(sqm)</p>
                <p>{{ s.landSize || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Description(If Applicable)</p>
                <p>{{ s.description || '-' }}</p>
            </div>
            <div class="index"><h1>Current Mortgage Name</h1></div>
            <div class="item">
                <p class="title">1st Mortgage</p>
                <p>{{ s.mortgage1 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">2nd Mortgage</p>
                <p>{{ s.mortgage2 || '-' }}</p>
            </div>
            <div class="index"><h1>Current Debt Name</h1></div>
            <div class="item">
                <p class="title">1st Mortgage</p>
                <p>{{ s.debt1 || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">2nd Mortgage</p>
                <p>{{ s.debt2 || '-' }}</p>
            </div>
            <div class="index"><h1>Valuation</h1></div>
            <div class="values">
                <div class="value">
                    <el-checkbox v-model="s.valuation" disabled><p>Est Current Value</p></el-checkbox>
                    <p>Value($) {{ s.est }}</p>
                </div>
                <div class="value">
                    <el-checkbox v-model="s.valuation" disabled><p>Purchase Price</p></el-checkbox>
                    <p>Value($) {{ s.purchase }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const { detail } = defineProps({
        detail: Object
    })
</script>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        gap: 20px;        
    }
    .form {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .item {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 600;
        line-height: 140%;
        margin: 0;
    }
    .title {
        color: #7A858E;
    }
    .index {
        grid-column: 1 / 4;
        margin-bottom: 20px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
    .values {
        grid-column: 1 / 4;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }
    .value {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    :deep(.el-checkbox__input.is-disabled.is-checked .el-checkbox__inner) {
        background-color: #2984DE;
        border-color: #2984DE;
    }
    :deep(.el-checkbox) {
        --el-checkbox-disabled-checked-icon-color: #FFF;
    }
</style>