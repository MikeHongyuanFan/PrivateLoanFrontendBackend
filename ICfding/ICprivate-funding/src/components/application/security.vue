<template>
    <div class="content">
        <div v-if="!detail.security_properties.length">
            <p>No security properties in this application</p>
        </div>
        <div class="form" v-for="(property, index) in detail.security_properties" :key="index">
            <div class="index"><h1>Property {{ index + 1 }}</h1></div>
            
            <!-- Property Address Section -->
            <div class="item">
                <p class="title">Full Address</p>
                <p>{{ formatAddress(property) || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Property Type</p>
                <p>{{ formatPropertyType(property.property_type) || '-' }}</p>
            </div>
            <div class="item" v-if="property.property_type === 'other'">
                <p class="title">Description (if applicable)</p>
                <p>{{ property.description_if_applicable || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Occupancy Type</p>
                <p>{{ formatOccupancy(property.occupancy) || '-' }}</p>
            </div>
            
            <!-- Property Details Section -->
            <div class="item">
                <p class="title">Bedrooms</p>
                <p>{{ formatNumber(property.bedrooms) }}</p>
            </div>
            <div class="item">
                <p class="title">Bathrooms</p>
                <p>{{ formatNumber(property.bathrooms) }}</p>
            </div>
            <div class="item">
                <p class="title">Car Spaces</p>
                <p>{{ formatNumber(property.car_spaces) }}</p>
            </div>
            <div class="item">
                <p class="title">Building Size (sqm)</p>
                <p>{{ property.building_size || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Land Size (sqm)</p>
                <p>{{ property.land_size || '-' }}</p>
            </div>
            
            <!-- Property Features Section -->
            <div class="item">
                <p class="title">Property Features</p>
                <div class="features">
                    <span v-if="property.is_single_story" class="feature">Single Story</span>
                    <span v-if="property.has_garage" class="feature">Garage</span>
                    <span v-if="property.has_carport" class="feature">Carport</span>
                    <span v-if="property.has_off_street_parking" class="feature">Off-street Parking</span>
                    <span v-if="!hasAnyFeatures(property)" class="no-features">No features specified</span>
                </div>
            </div>
            
            <!-- Current Mortgage Section -->
            <div class="index"><h1>Current Mortgage Information</h1></div>
            <div class="item">
                <p class="title">Current Mortgagee</p>
                <p>{{ property.current_mortgagee || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">1st Mortgage</p>
                <p>{{ property.first_mortgage || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">2nd Mortgage</p>
                <p>{{ property.second_mortgage || '-' }}</p>
            </div>
            
            <!-- Financial Information Section -->
            <div class="index"><h1>Financial Information</h1></div>
            <div class="item">
                <p class="title">Current Debt Position</p>
                <p>{{ formatCurrency(property.current_debt_position) || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Estimated Value</p>
                <p>{{ formatCurrency(property.estimated_value) || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Purchase Price</p>
                <p>{{ formatCurrency(property.purchase_price) || '-' }}</p>
            </div>
            <div class="item">
                <p class="title">Net Equity</p>
                <p>{{ calculateNetEquity(property) || '-' }}</p>
            </div>
        </div>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const { detail } = defineProps({
        detail: Object
    });

    // Helper function to format the complete address
    const formatAddress = (property) => {
        const addressParts = [
            property.address_unit,
            property.address_street_no,
            property.address_street_name,
            property.address_suburb,
            property.address_state,
            property.address_postcode
        ].filter(part => part && part.toString().trim() !== '');
        
        return addressParts.length > 0 ? addressParts.join(' ') : null;
    };

    // Helper function to format property type
    const formatPropertyType = (type) => {
        if (!type) return null;
        
        const typeMap = {
            'residential': 'Residential',
            'commercial': 'Commercial',
            'industrial': 'Industrial',
            'retail': 'Retail',
            'land': 'Land',
            'rural': 'Rural',
            'other': 'Other'
        };
        
        return typeMap[type] || type;
    };

    // Helper function to format occupancy type
    const formatOccupancy = (occupancy) => {
        if (!occupancy) return null;
        
        const occupancyMap = {
            'owner_occupied': 'Owner Occupied',
            'investment': 'Investment Property'
        };
        
        return occupancyMap[occupancy] || occupancy;
    };

    // Helper function to format currency
    const formatCurrency = (amount) => {
        if (!amount || amount === 0) return null;
        
        const numAmount = parseFloat(amount);
        if (isNaN(numAmount)) return null;
        
        return new Intl.NumberFormat('en-AU', {
            style: 'currency',
            currency: 'AUD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(numAmount);
    };

    // Helper function to calculate net equity
    const calculateNetEquity = (property) => {
        const estimatedValue = parseFloat(property.estimated_value) || 0;
        const currentDebt = parseFloat(property.current_debt_position) || 0;
        
        if (estimatedValue === 0) return null;
        
        const netEquity = estimatedValue - currentDebt;
        return formatCurrency(netEquity);
    };

    // Helper function to check if property has any features
    const hasAnyFeatures = (property) => {
        return property.is_single_story || 
               property.has_garage || 
               property.has_carport || 
               property.has_off_street_parking;
    };

    // Helper function to format number
    const formatNumber = (value) => {
        if (value === null || value === undefined) return '-';
        return value.toString();
    };
</script>

<style scoped>
    .content {
        display: flex;
        flex-direction: column;
        gap: 20px;        
    }
    .form {
        padding: 20px;
        border-radius: 6px;
        background: #FFF;
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
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
    .index {
        grid-column: 1 / 4;
        margin-bottom: 20px;
    }
    h1 {
        color: #384144;
        font-feature-settings: 'liga' off, 'clig' off;
        font-size: 0.9rem;
        font-style: normal;
        font-weight: 600;
        line-height: normal;
    }
    .features {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }
    .feature {
        background: #e8f5e8;
        color: #2d5a2d;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 500;
    }
    .no-features {
        color: #7A858E;
        font-style: italic;
        font-size: 0.7rem;
    }
</style>