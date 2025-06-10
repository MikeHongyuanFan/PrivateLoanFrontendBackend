<template>
    <button>
        <img src="/src/assets/icons/save.png" alt="save" />
        Save
    </button>
</template>

<script setup>

</script>

<style scoped>
    button {
        padding: 7px 10px;
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
    img {
        width: 20px;
        height: 20px;
    }
    button:hover {
        background: #1F63A9;
    }
</style>