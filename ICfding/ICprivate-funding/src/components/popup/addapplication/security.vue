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
                <div class="item">
                    <p>Bedrooms</p>
                    <el-input-number v-model="bedroomsComputed[index]" :min="0" :max="20" placeholder="e.g. 3" />
                    <span class="hint">Number of bedrooms</span>
                </div>
                <div class="item">
                    <p>Bathrooms</p>
                    <el-input-number v-model="bathroomsComputed[index]" :min="0" :max="20" placeholder="e.g. 2" />
                    <span class="hint">Number of bathrooms</span>
                </div>
                <div class="item">
                    <p>Car Spaces</p>
                    <el-input-number v-model="carSpacesComputed[index]" :min="0" :max="20" placeholder="e.g. 1" />
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
                    <p>First Mortgage</p>
                    <el-input v-model="item.first_mortgage" placeholder="e.g. XYZ Bank" />
                    <span class="hint">First mortgage holder</span>
                </div>
                <div class="item">
                    <p>Second Mortgage</p>
                    <el-input v-model="item.second_mortgage" placeholder="e.g. DEF Bank" />
                    <span class="hint">Second mortgage holder (if applicable)</span>
                </div>
                <div class="item">
                    <p>Current Debt Position ($)</p>
                    <el-input v-model="item.current_debt_position" type="number" placeholder="e.g. 250000" />
                    <span class="hint">Current debt on the property</span>
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
    import { ref, computed, onMounted, watch } from 'vue';

    const props = defineProps({
        security: Array
    });

    defineEmits(['add', 'remove']);

    // Create computed properties for numeric fields to handle type conversion
    const bedroomsComputed = ref([]);
    const bathroomsComputed = ref([]);
    const carSpacesComputed = ref([]);

    // Initialize default values and computed properties
    onMounted(() => {
        // Initialize arrays for computed properties
        bedroomsComputed.value = props.security.map(item => Number(item.bedrooms) || 0);
        bathroomsComputed.value = props.security.map(item => Number(item.bathrooms) || 0);
        carSpacesComputed.value = props.security.map(item => Number(item.car_spaces) || 0);
        
        // Initialize default values for required boolean fields
        props.security.forEach((property, index) => {
            if (property.is_single_story === null) property.is_single_story = false;
            if (property.has_garage === null) property.has_garage = false;
            if (property.has_carport === null) property.has_carport = false;
            if (property.has_off_street_parking === null) property.has_off_street_parking = false;
        });
    });

    // Watch for changes in the computed properties and update the original data
    watch(bedroomsComputed, (newVal) => {
        props.security.forEach((item, index) => {
            if (index < newVal.length) {
                item.bedrooms = newVal[index];
            }
        });
    });

    watch(bathroomsComputed, (newVal) => {
        props.security.forEach((item, index) => {
            if (index < newVal.length) {
                item.bathrooms = newVal[index];
            }
        });
    });

    watch(carSpacesComputed, (newVal) => {
        props.security.forEach((item, index) => {
            if (index < newVal.length) {
                item.car_spaces = newVal[index];
            }
        });
    });

    // Watch for changes in the security array (e.g., when adding new items)
    watch(() => props.security.length, (newLength, oldLength) => {
        if (newLength > oldLength) {
            // A new item was added, initialize its computed properties
            for (let i = oldLength; i < newLength; i++) {
                bedroomsComputed.value[i] = Number(props.security[i].bedrooms) || 0;
                bathroomsComputed.value[i] = Number(props.security[i].bathrooms) || 0;
                carSpacesComputed.value[i] = Number(props.security[i].car_spaces) || 0;
                
                // Initialize boolean fields
                if (props.security[i].is_single_story === null) props.security[i].is_single_story = false;
                if (props.security[i].has_garage === null) props.security[i].has_garage = false;
                if (props.security[i].has_carport === null) props.security[i].has_carport = false;
                if (props.security[i].has_off_street_parking === null) props.security[i].has_off_street_parking = false;
            }
        }
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
