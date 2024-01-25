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
        this.loadId = params.loadId || uuid.generate();
        this.formData = new window.FormData();
        this.graphs = ko.observable();
        this.selectedLoadEvent = params.selectedLoadEvent || ko.observable();
        this.formatTime = params.formatTime;
        this.timeDifference = params.timeDifference;

        this.getGraphs = function(){
            self.loading(true);
            self.submit('get_graphs').then(function(response){
                self.graphs(response.result);
                self.loading(false);
            });
        };
        
        self.runRDMMigration = async function() {
            self.loading(true);            
            const response = await self.submit('run_migrate_rdm');
            self.loading(false);
        };

        this.submit = function(action) {
            self.formData.append('action', action);
            self.formData.append('load_id', self.loadId);
            self.formData.append('module', self.moduleId);
            return $.ajax({
                type: "POST",
                url: arches.urls.etl_manager,
                data: self.formData,
                cache: false,
                processData: false,
                contentType: false,
            });
        };

        this.init = function(){
            this.getGraphs();
        };

        this.init();
    };
    ko.components.register('migrate-rdm', {
        viewModel: viewModel,
        template: migrateRDMTemplate,
    });
    return viewModel;
}); 