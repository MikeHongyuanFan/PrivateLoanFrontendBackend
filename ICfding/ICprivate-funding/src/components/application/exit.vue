<template>
    <div class="content">
        <div class="item">
            <p class="title">Finance Takeout Method</p>
            <p>{{ formatExitStrategy(detail.exit_strategy) || '-' }}</p>
        </div>
        <div class="item">
            <p class="title">Details (If Other)</p>
            <p>{{ detail.exit_strategy_details || '-' }}</p>
        </div>
    </div>
</template>

<script setup>
    import { computed } from 'vue';

    const props = defineProps({
        detail: {
            type: Object,
            required: true
        }
    });

    // Helper function to format exit strategy for display
    const formatExitStrategy = (strategy) => {
        if (!strategy) return null;
        
        const strategyMap = {
            'sale': 'Sale of Property',
            'refinance': 'Refinance',
            'income': 'Income/Cash Flow',
            'other': 'Other'
        };
        
        return strategyMap[strategy] || strategy;
    };
</script>

<style scoped>
    .content {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
        min-height: 250px;
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
</style>