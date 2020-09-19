import Vue from 'vue'
import Router from 'vue-router'
import TextCount from "./components/TextCount.vue"
import UploadImage from "./components/UploadImage.vue"
import Planet from "./components/Planet.vue"
import PopUp from "./components/PopUp.vue"

Vue.use(Router)

export default new Router({
    mode: 'history',
    routes: [
        {
            path: '/text-count',
            name: 'text-count',
            component: TextCount
        },
        {
            path: '/upload-image',
            name: 'upload-image',
            component: UploadImage
        },
        {
            path: '/planet',
            name: 'planet',
            component: Planet
        },
        {
            path: '/pop-up',
            name: 'pop-up',
            component: PopUp
        },
    ]
})

