<template>
    <button>
        <img src="/src/assets/icons/create.png" clt="create" />
        {{ action }}
    </button>
</template>

<script setup>
    defineProps({
        action: String
    })
</script>

<style scoped>
    button {
        padding: 7px 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        border-radius: 3px;
        border: none;
        background: #2984DE;
        color: #FFF;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 19px;
    }
    img {
        width: 20px;
        height: 20px;
    }
    button:hover {
        background: #1F63A9;
    }
</style>