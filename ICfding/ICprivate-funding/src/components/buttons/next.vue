<template>
    <button :disabled="disabled">
        <span class="arrow">→</span>
        {{ text || 'Next' }}
    </button>
</template>

<script setup>
    const props = defineProps({
        disabled: {
            type: Boolean,
            default: false
        },
        text: {
            type: String,
            default: 'Next'
        }
    })
</script>

<style scoped>
    button {
        padding: 7px 10px;
        border-radius: 3px;
        background: #28a745;
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
        cursor: pointer;
    }
    
    button:disabled {
        background: #6c757d;
        cursor: not-allowed;
        opacity: 0.6;
    }
    
    .arrow {
        font-size: 16px;
        font-weight: bold;
    }
    
    button:hover:not(:disabled) {
        background: #218838;
    }
</style> 