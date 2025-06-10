<template>
    <div class="form">
        <h1>Finance Takeout Method <span class="required">*</span></h1>
        <div class="item">
            <p>Exit Strategy <span class="required">*</span></p>
            <el-select v-model="exit.exit_strategy" placeholder="Select exit strategy">
                <el-option value="sale" label="Sale of Property" />
                <el-option value="refinance" label="Refinance" />
                <el-option value="income" label="Income/Cash Flow" />
                <el-option value="other" label="Other" />
            </el-select>
            <span class="hint">How the loan will be paid out at the end of the term</span>
        </div>
        
        <div class="item" v-if="exit.exit_strategy === 'other'">
            <p>Other Strategy <span class="required">*</span></p>
            <el-input v-model="otherStrategy" placeholder="Specify other exit strategy" @input="updateOtherStrategy" />
            <span class="hint">Required if 'Other' is selected</span>
        </div>
        
        <h1>Details (If Other)</h1>
        <div class="item">
            <p>Attach copies of supporting documents for your Finance Takeout Method</p>
            <el-input :rows="3" type="textarea" v-model="exit.exit_strategy_details" placeholder="Enter details about your exit strategy" />
            <span class="hint">Provide additional information about your exit strategy</span>
        </div>
    </div>
</template>

<script setup>
    import { ref, watch, onMounted } from 'vue';

    const props = defineProps({
        exit: Object
    });

    // Create a local ref for the other strategy
    const otherStrategy = ref("");

    // Initialize values from props
    onMounted(() => {
        // Check if exit_strategy is already set and is a valid enum value
        const validStrategies = ["sale", "refinance", "income", "other"];
        if (props.exit.exit_strategy && validStrategies.includes(props.exit.exit_strategy)) {
            // If it's a valid enum value, keep it as is
        } else if (props.exit.exit_strategy) {
            // If it's set but not a valid enum, assume it's a custom value
            otherStrategy.value = props.exit.exit_strategy;
            props.exit.exit_strategy = "other";
        } else {
            // Default to refinance if nothing is set
            props.exit.exit_strategy = "refinance";
        }
    });

    // Function to update the exit strategy when "other" is selected
    const updateOtherStrategy = () => {
        if (props.exit.exit_strategy === 'other' && otherStrategy.value) {
            // Store the custom value in a separate field
            props.exit.custom_exit_strategy = otherStrategy.value;
        }
    };

    // Watch for changes in the exit strategy
    watch(() => props.exit.exit_strategy, (newVal) => {
        if (newVal !== 'other') {
            // Reset the other strategy input when a predefined strategy is selected
            otherStrategy.value = "";
        }
    });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 15px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    .group {
        width: 100%;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    p {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.75rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
        margin: 0;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .hint {
        color: #8c8c8c;
        font-size: 0.7rem;
        font-style: italic;
    }
    .required {
        color: #f56c6c;
        margin-left: 2px;
    }
</style>
