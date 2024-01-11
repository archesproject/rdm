define([
    'knockout',
    'knockout-mapping',
    'jquery',
    'uuid',
    'arches',
    'viewmodels/alert',
    'viewmodels/alert-json',
    'templates/views/components/etl_modules/migrate-rdm.htm',
], function(ko, koMapping, $, uuid, arches, AlertViewModel, JsonErrorAlertViewModel, migrateRDMTemplate) {
    const viewModel = function(params) {
        const self = this;

        this.loadDetails = params.load_details;
        this.state = params.state;
        this.loading = params.loading || ko.observable();
        this.alert = params.alert;
        this.moduleId = params.etlmoduleid;
        this.selectedLoadEvent = params.selectedLoadEvent || ko.observable();
        this.formatTime = params.formatTime;
        this.timeDifference = params.timeDifference;

        this.init = function(){
            // this.getGraphs();
            console.log('Hello world');
        };

        this.init();
    };
    ko.components.register('migrate-rdm', {
        viewModel: viewModel,
        template: migrateRDMTemplate,
    });
    return viewModel;
}); 