<template>
    <button>
        <p class="button_txt">Active</p>
    </button>
</template>

<script setup>

</script>

<style scoped>
button {
    height: 32px;
    padding: 0 20px;
    border-radius: 4px;
    background: #1CBB8C;
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 5px;
    border: none;
}
.button_txt {
    color: #FFF;
    font-feature-settings: 'liga' off, 'clig' off;
    font-size: 0.9rem;
    font-style: normal;
    font-weight: 500;
    line-height: normal;
    margin: 0;
}
button:hover {
    background: #169670;
}
</style>