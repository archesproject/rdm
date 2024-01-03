import ko from 'knockout';
import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import RDMApp from '@/App.vue';
import RDMAppTepmlate from 'templates/views/components/plugins/reference-data-manager.htm';

ko.components.register('reference-data-manager', {
    viewModel: function() {
        const app = createApp(RDMApp);
        app.use(PrimeVue);
        app.mount('#rdm-mounting-point');
    },
    template: RDMAppTepmlate,
});