(function () {
  'use strict';

  angular
      .module('horizon.app.core.openstack-service-api')
      .factory('horizon.app.core.openstack-service-api.vitrage', vitrageAPI);

  vitrageAPI.$inject = [
    'horizon.framework.util.http.service',
    'horizon.framework.widgets.toast.service'

  ];

  function vitrageAPI(apiService, toastService) {

    var service = {
      getTopology: getTopology,
      getAlarms: getAlarms,
      getHistoryAlarms: getHistoryAlarms,
      getRca: getRca,
      getTemplates: getTemplates,
      getDetailedActionlist: getDetailedActionlist,
      postAction: postAction,
      getSetting: getSetting
    };

    return service;

    ///////////
    // Topology
    ///////////

    function getTopology(graph_type, config,admin) {
      config = config || {};

      if (graph_type) {
        config.params = config.params || {};
        config.params.graph_type = graph_type;
      }
      if (admin){
        (!config.params) ? config.params = {all_tenants: true} : config.params.all_tenants = true;
      }
      console.info('CONFIG in core - ', config)
      return apiService.get('/api/vitrage/topology/', config)
          .error(function () {
            toastService.add('error', gettext('Unable to fetch the Vitrage Topology service.'));
          });
    }

    function getAlarms(config) {
      config = config || {};
      var url = '/api/vitrage/alarm/';

      return apiService.get(url, config)
        .catch(function() {
          toastService.add('error', gettext('Unable to fetch the Vitrage Alarms service.'));
        });
    }

    function getHistoryAlarms(config) {
      config = config || {};

      var url = '/api/vitrage/history/';
      return apiService.get(url, config)
        .catch(function() {
          toastService.add('error', gettext('Unable to fetch the Vitrage' +
            ' Alarms History service.'));
        });

    }

    function getRca(alarm_id,adminState) {
      return apiService.get('/api/vitrage/rca/'+alarm_id+"/"+adminState)
          .catch(function () {
            toastService.add('error', gettext('Unable to fetch the Vitrage RCA service.'));
          });
    }

    function getTemplates(template_id) {
      return apiService.get('/api/vitrage/template/'+template_id)
          .catch(function () {
            toastService.add('error', gettext('Unable to fetch the Vitrage Templates service.'));
          });
    }

    function getDetailedActionlist(action,nodetype) {
      return apiService.get('/api/vitrage/actions/' + action + "/" + nodetype )
          .catch(function () {
            toastService.add('error', gettext('Unable to fetch the Project action list service.'));
          });
      }

    function postAction(action, requestdict) {
      return apiService.post('/api/vitrage/requests/' + action + "/" + JSON.stringify(requestdict))
          .catch(function () {
            toastService.add('error', gettext('Unable to fetch the Project request action service.'));
          });
      }

    function getSetting() {
      return apiService.get('/api/vitrage/settings')
          .catch(function () {
            toastService.add('error', gettext('Unable to fetch the Vitrage Setting service.'));
          });
      }
  }
}());
