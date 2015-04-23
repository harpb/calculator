app = angular.module('app')
app.directive 'cell', ->
    require: '^ticTacToe',
    scope:
        model: '=ngModel'
    templateUrl: 'app/directives/cell.html'

    controller: ($scope)->
        $scope.active = false
        $scope.letter = ' '

    link: (scope, element, attrs, ticTacToeCtrl)->

        scope.activate = ->
            if scope.model.active
                return
            ticTacToeCtrl.playerMove(scope.model)
            scope.model.active = true

        scope.rightCorner = ->
            @model.position % ticTacToeCtrl.length == ticTacToeCtrl.length - 1

        scope.color = ->
            if ticTacToeCtrl.isPlayer(@model)
                return 'teal'
            if ticTacToeCtrl.isComputer(@model)
                return 'purple'
