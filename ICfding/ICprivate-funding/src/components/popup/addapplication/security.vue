<template>
    <div class="form">
        <div class="long_item">
            <h1>Security Property Details <span class="required">*</span></h1>
            <span class="hint">Information about the property being used as security for the loan</span>
        </div>
        <div v-for="(item, index) in security" :key="index" class="security">
            <div class="address">
                <div class="item">
                    <p>Unit/Suite</p>
                    <el-input v-model="item.address_unit" placeholder="e.g. Unit 5" />
                    <span class="hint">Unit or suite number if applicable</span>
                </div>
                <div class="item">
                    <p>Street No <span class="required">*</span></p>
                    <el-input v-model="item.address_street_no" placeholder="e.g. 123" />
                    <span class="hint">Street number</span>
                </div>
                <div class="item">
                    <p>Street Name <span class="required">*</span></p>
                    <el-input v-model="item.address_street_name" placeholder="e.g. Main Street" />
                    <span class="hint">Street name</span>
                </div>
                <div class="item">
                    <p>Suburb <span class="required">*</span></p>
                    <el-input v-model="item.address_suburb" placeholder="e.g. Richmond" />
                    <span class="hint">Suburb name</span>
                </div>
                <div class="item">
                    <p>State <span class="required">*</span></p>
                    <el-select v-model="item.address_state" placeholder="Select state">
                        <el-option value="NSW" label="NSW" />
                        <el-option value="VIC" label="VIC" />
                        <el-option value="QLD" label="QLD" />
                        <el-option value="SA" label="SA" />
                        <el-option value="WA" label="WA" />
                        <el-option value="TAS" label="TAS" />
                        <el-option value="NT" label="NT" />
                        <el-option value="ACT" label="ACT" />
                    </el-select>
                    <span class="hint">Australian state or territory</span>
                </div>
                <div class="item">
                    <p>Postcode <span class="required">*</span></p>
                    <el-input v-model="item.address_postcode" placeholder="e.g. 3000" maxlength="4" />
                    <span class="hint">4-digit postcode</span>
                </div>
            </div>
            <div class="property">
                <div class="item">
                    <p>Property Type <span class="required">*</span></p>
                    <el-select v-model="item.property_type" placeholder="Select property type">
                        <el-option value="residential" label="Residential" />
                        <el-option value="commercial" label="Commercial" />
                        <el-option value="industrial" label="Industrial" />
                        <el-option value="retail" label="Retail" />
                        <el-option value="land" label="Land" />
                        <el-option value="rural" label="Rural" />
                        <el-option value="other" label="Other" />
                    </el-select>
                    <span class="hint">Type of property</span>
                </div>
                <div class="item" v-if="item.property_type === 'other'">
                    <p>Description (if applicable) <span class="required">*</span></p>
                    <el-input v-model="item.description_if_applicable" placeholder="Please describe the property type" />
                    <span class="hint">Provide a description if property type is 'Other'</span>
                </div>
                <div class="item">
                    <p>Bedrooms</p>
                    <el-input-number v-model="item.bedrooms" :min="0" :max="20" placeholder="e.g. 3" />
                    <span class="hint">Number of bedrooms</span>
                </div>
                <div class="item">
                    <p>Bathrooms</p>
                    <el-input-number v-model="item.bathrooms" :min="0" :max="20" placeholder="e.g. 2" />
                    <span class="hint">Number of bathrooms</span>
                </div>
                <div class="item">
                    <p>Car Spaces</p>
                    <el-input-number v-model="item.car_spaces" :min="0" :max="20" placeholder="e.g. 1" />
                    <span class="hint">Number of car spaces</span>
                </div>
                <div class="item">
                    <p>Building Size (sqm)</p>
                    <el-input v-model="item.building_size" type="number" placeholder="e.g. 150" />
                    <span class="hint">Size in square meters</span>
                </div>
                <div class="item">
                    <p>Land Size (sqm)</p>
                    <el-input v-model="item.land_size" type="number" placeholder="e.g. 500" />
                    <span class="hint">Size in square meters</span>
                </div>
                <div class="item">
                    <p>Features <span class="required">*</span></p>
                    <div class="features">
                        <el-checkbox v-model="item.is_single_story">Single Story</el-checkbox>
                        <el-checkbox v-model="item.has_garage">Garage</el-checkbox>
                        <el-checkbox v-model="item.has_carport">Carport</el-checkbox>
                        <el-checkbox v-model="item.has_off_street_parking">Off-street Parking</el-checkbox>
                    </div>
                    <span class="hint">Select all applicable features</span>
                </div>
                <div class="item">
                    <p>Occupancy <span class="required">*</span></p>
                    <el-select v-model="item.occupancy" placeholder="Select occupancy type">
                        <el-option value="owner_occupied" label="Owner Occupied" />
                        <el-option value="investment" label="Investment Property" />
                    </el-select>
                    <span class="hint">How the property is occupied</span>
                </div>
            </div>
            <div class="finance">
                <div class="item">
                    <p>Current Mortgagee</p>
                    <el-input v-model="item.current_mortgagee" placeholder="e.g. ABC Bank" />
                    <span class="hint">Current mortgage holder</span>
                </div>
                <div class="item">
                    <p>First Mortgage ($)</p>
                    <el-input-number v-model="item.first_mortgage" :min="0" :precision="2" placeholder="e.g. 200000" />
                    <span class="hint">First mortgage amount</span>
                </div>
                <div class="item">
                    <p>Second Mortgage ($)</p>
                    <el-input-number v-model="item.second_mortgage" :min="0" :precision="2" placeholder="e.g. 50000" />
                    <span class="hint">Second mortgage amount (if applicable)</span>
                </div>
                <div class="item">
                    <p>Current Debt Position ($)</p>
                    <el-input v-model="item.current_debt_position" type="number" placeholder="e.g. 250000" />
                    <span class="hint">Current debt on the property</span>
                </div>
                <div class="item">
                    <p>1st Mortgage Debt ($)</p>
                    <el-input v-model="item.first_mortgage_debt" type="number" placeholder="e.g. 150000" />
                    <span class="hint">Outstanding debt for the first mortgage</span>
                </div>
                <div class="item">
                    <p>2nd Mortgage Debt ($)</p>
                    <el-input v-model="item.second_mortgage_debt" type="number" placeholder="e.g. 50000" />
                    <span class="hint">Outstanding debt for the second mortgage (if any)</span>
                </div>
                <div class="item">
                    <p>Estimated Value ($) <span class="required">*</span></p>
                    <el-input v-model="item.estimated_value" type="number" placeholder="e.g. 500000" />
                    <span class="hint">Estimated property value</span>
                </div>
                <div class="item">
                    <p>Purchase Price ($)</p>
                    <el-input v-model="item.purchase_price" type="number" placeholder="e.g. 450000" />
                    <span class="hint">Original purchase price</span>
                </div>
            </div>
            <div class="buttons">
                <el-button type="danger" @click="$emit('remove', index)" :disabled="security.length <= 1">Remove</el-button>
            </div>
        </div>
        <div class="add">
            <el-button type="primary" @click="$emit('add')">Add Security Property</el-button>
        </div>
    </div>
</template>

<script setup>
    import { onMounted } from 'vue';

    const props = defineProps({
        security: Array
    });

    defineEmits(['add', 'remove']);

    // Initialize default values for boolean fields
    onMounted(() => {
        props.security.forEach((property) => {
            if (property.is_single_story === null || property.is_single_story === undefined) property.is_single_story = false;
            if (property.has_garage === null || property.has_garage === undefined) property.has_garage = false;
            if (property.has_carport === null || property.has_carport === undefined) property.has_carport = false;
            if (property.has_off_street_parking === null || property.has_off_street_parking === undefined) property.has_off_street_parking = false;
        });
    });
</script>

<style scoped>
    .form {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
    .security {
        display: flex;
        flex-direction: column;
        gap: 15px;
        padding: 15px;
        border: 1px solid #e1e1e1;
        border-radius: 5px;
    }
    .address, .property, .finance {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }
    .item {
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
    }
    .long_item {
        grid-column: 1 / 4;
        display: flex;
        flex-direction: column;
        align-items: start;
        gap: 10px;
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
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 500;
        line-height: 12px;
    }
    .features {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
    }
    .buttons {
        display: flex;
        justify-content: flex-end;
        margin-top: 10px;
    }
    .add {
        display: flex;
        justify-content: center;
        margin-top: 10px;
    }
    :deep(.el-select) {
        width: 100%;
    }
    :deep(.el-input-number) {
        width: 100%;
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
