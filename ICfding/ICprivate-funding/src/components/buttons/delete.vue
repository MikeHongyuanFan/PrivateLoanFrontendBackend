<template>
    <button>
        <img src="/src/assets/icons/delete.png" alt="edit" />
        Delete
    </button>
</template>

<script setup>

</script>

<style scoped>
    button {
        height: 32px;
        padding: 0 20px;
        border-radius: 4px;
        background: #2984DE;
        display: flex;
        flex-direction: row;
        align-items: center;
        gap: 5px;
        border: none;
        color: #FFF;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: normal;
    }
    img {
        width: 20px;
        height: 20px;
    }
    button:hover {
        background: #1F63A9;
    }
</style>