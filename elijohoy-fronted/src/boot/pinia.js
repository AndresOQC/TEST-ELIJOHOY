import { boot } from 'quasar/wrappers'
import { createPinia } from 'pinia'

/*
 * When adding new properties to stores, you should also
 * extend the `PiniaCustomProperties` interface.
 * @see https://pinia.vuejs.org/core-concepts/plugins.html#typing-new-store-properties
 */

export default boot(({ app }) => {
  const pinia = createPinia()

  // You can add Pinia plugins here
  // pinia.use(SomePiniaPlugin)

  app.use(pinia)
})