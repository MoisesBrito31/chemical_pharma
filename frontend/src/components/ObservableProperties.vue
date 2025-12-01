<template>
  <div v-if="properties" class="observable-properties">
    <div v-if="properties.flavor" class="property-item">
      <span class="property-icon">👅</span>
      <span class="property-label">Sabor:</span>
      <span class="property-value">{{ properties.flavor }}</span>
    </div>
    
    <div v-if="properties.appearance" class="property-item">
      <span class="property-icon" :style="{ color: properties.appearance.color }">●</span>
      <span class="property-label">Aparência:</span>
      <span class="property-value" :style="{ color: properties.appearance.color }">
        {{ properties.appearance.name }}
      </span>
    </div>
    
    <div v-if="properties.effects && properties.effects.length > 0" class="property-item effects">
      <span class="property-icon">⚡</span>
      <span class="property-label">Efeitos:</span>
      <div class="effects-list">
        <span 
          v-for="effect in properties.effects" 
          :key="effect"
          class="effect-badge"
        >
          {{ effect }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  properties: {
    type: Object,
    default: null
  }
})
</script>

<style scoped>
.observable-properties {
  margin-top: 0.75rem;
  padding-top: 0.75rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.property-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.property-item:last-child {
  margin-bottom: 0;
}

.property-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.property-label {
  color: #aaa;
  font-weight: 500;
  min-width: 80px;
}

.property-value {
  color: #fff;
  font-weight: 600;
}

.property-item.effects {
  flex-direction: column;
  align-items: flex-start;
}

.effects-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.effect-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: rgba(100, 150, 255, 0.2);
  border: 1px solid rgba(100, 150, 255, 0.4);
  border-radius: 4px;
  font-size: 0.8rem;
  color: #64a0ff;
}
</style>

