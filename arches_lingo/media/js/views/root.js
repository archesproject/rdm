import LingoApp from '@/arches_lingo/App.vue';
import createVueApplication from 'arches/arches/app/media/js/utils/create-vue-application';

createVueApplication(LingoApp).then(vueApp => {
    vueApp.mount('#lingo-mounting-point');
});
