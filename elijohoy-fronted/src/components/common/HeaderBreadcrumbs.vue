<template>
  <div class="breadcrumbs-container">
    <q-breadcrumbs 
      class="custom-breadcrumbs"
      separator="/"
      separator-color="purple-5"
    >
      <template v-slot:separator>
        <q-icon name="chevron_right" size="14px" />
      </template>
      
      <q-breadcrumbs-el 
        v-for="(crumb, index) in breadcrumbs" 
        :key="index"
        :label="crumb.label"
        :icon="crumb.icon"
        :to="crumb.to"
        :class="{ 'current-crumb': index === breadcrumbs.length - 1 }"
        class="breadcrumb-item"
      />
    </q-breadcrumbs>
    
    <div class="breadcrumb-actions" v-if="showActions">
      <q-btn
        flat
        round
        icon="refresh"
        size="sm"
        class="action-btn"
        @click="$emit('refresh')"
      >
        <q-tooltip>Actualizar</q-tooltip>
      </q-btn>
      
      <q-btn
        flat
        round
        icon="more_vert"
        size="sm"
        class="action-btn"
      >
        <q-tooltip>Más opciones</q-tooltip>
        <q-menu>
          <q-list style="min-width: 100px">
            <q-item clickable v-close-popup>
              <q-item-section>Exportar</q-item-section>
            </q-item>
            <q-item clickable v-close-popup>
              <q-item-section>Configurar</q-item-section>
            </q-item>
          </q-list>
        </q-menu>
      </q-btn>
    </div>
  </div>
</template>

<script>
import { defineComponent, computed } from 'vue'
import { useRoute } from 'vue-router'

export default defineComponent({
  name: 'HeaderBreadcrumbs',
  props: {
    customBreadcrumbs: {
      type: Array,
      default: null
    },
    showActions: {
      type: Boolean,
      default: true
    }
  },
  emits: ['refresh'],
  setup(props) {
    const route = useRoute()
    
    const breadcrumbs = computed(() => {
      if (props.customBreadcrumbs) {
        return props.customBreadcrumbs
      }
      
      // Auto-generate breadcrumbs based on route
      const pathSegments = route.path.split('/').filter(segment => segment)
      const crumbs = [
        { label: 'Dashboard', icon: 'dashboard', to: '/dashboard' }
      ]
      
      let currentPath = ''
      pathSegments.forEach((segment, index) => {
        if (index > 0) { // Skip 'dashboard' as it's already added
          currentPath += `/${segment}`
          const label = segment.charAt(0).toUpperCase() + segment.slice(1)
          crumbs.push({
            label: label.replace(/-/g, ' '),
            to: currentPath
          })
        }
      })
      
      return crumbs
    })
    
    return {
      breadcrumbs
    }
  }
})
</script>

<style scoped>
.breadcrumbs-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 12px 16px;
  margin: 16px 24px;
  border: 1px solid rgba(124, 58, 237, 0.1);
  box-shadow: 0 2px 12px rgba(124, 58, 237, 0.08);
}

.custom-breadcrumbs {
  flex: 1;
}

.breadcrumb-item {
  transition: all 0.3s ease;
  border-radius: 6px;
  padding: 4px 8px;
}

.breadcrumb-item:hover {
  background: rgba(124, 58, 237, 0.1);
  color: #7C3AED;
}

.current-crumb {
  color: #7C3AED;
  font-weight: 600;
  background: rgba(124, 58, 237, 0.1);
}

.breadcrumb-actions {
  display: flex;
  gap: 4px;
}

.action-btn {
  color: #64748b;
  transition: all 0.3s ease;
}

.action-btn:hover {
  color: #7C3AED;
  background: rgba(124, 58, 237, 0.1);
}

@media (max-width: 768px) {
  .breadcrumbs-container {
    margin: 12px 16px;
    padding: 10px 12px;
  }
  
  .breadcrumb-actions {
    display: none;
  }
}
</style>