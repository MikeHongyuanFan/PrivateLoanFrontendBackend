<template>
    <div class="content">
        <div class="line" v-for="(l, index) in detail.loan_requirements" :key=index>
            <p>{{ l.description }}</p>
            <p class="status">{{ l.amount }}</p>
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
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .line {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    p {
        color: #7A858E;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 140%;
        margin: 0;
    }
    .status {
        color: #384144;
        font-weight: 600;
    }
</style>