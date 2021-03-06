angular
    .module('horizon.dashboard.project.vitrage')
    .directive('hzEntitiesActionlist', hzEntitiesActionlist);

function hzEntitiesActionlist() {
    var directive = {
        link: link,
        templateUrl: STATIC_URL + 'dashboard/project/entities/actionlist/entities-actionlist.html',
        restrict: 'E',
        scope: {
            actionItem: '=',
            actionList: '='
        }
    };
    return directive;
    function link(scope) {
        scope.selectedAction ='None';
        scope.showbutton = {'width':'90px'};
        scope.showpanel={'display':'none'};


        scope.$watch('actionItem', function () {
            scope.showpanel.display = scope.actionItem.display;
        });
        scope.$watch('actionList', function () {
            scope.typeArray=[];
            if(scope.actionList.length > 0 ){
                for(var i = 0; i<scope.actionList.length; i++){
                        scope.typeArray.push(scope.actionList[i]);
                }
                if(scope.typeArray.length > 0){
                    scope.selectedAction = scope.typeArray[0];
                }else{
                    scope.selectedAction = 'None';
                }

            }
        });
        scope.setStyle = function(selectedAction){
          if(selectedAction != 'Rally'){
              scope.showbutton['width'] = '182px';
              return scope.showbutton;
          }else{
              scope.showbutton['width'] ='90px';
              return scope.showbutton;
          }
        };

        scope.getComp = function(selectedAction,button_type){
            if (button_type != "Action"){
                return false;
            }else{
                return false;
            }
        };

        scope.onRunClick = function(action_type) {
              scope.$emit('selectedAction',[action_type,scope.actionItem.vitrage_type]);
        };
        scope.onNewtab = function(selectedAction) {
              scope.$emit('newTab',selectedAction);
        };
    }

}
