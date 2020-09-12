import ax from 'axios'

// insert all your axios logic here

export const axios = ax

export default {
    install (Vue, options) {
        Vue.prototype.$axios = ax
    }
}