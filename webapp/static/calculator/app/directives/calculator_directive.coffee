app = angular.module('app')

app.directive 'calculator', ->
    scope: {}
    templateUrl: 'app/directives/calculator.html'
    controller: ($scope, $http)->

        $scope.expression = ''
        $scope.resetText = 'AC'

        #######################################################################
        # MODES
        #######################################################################
        EDIT = 'edit'
        ERROR = 'error'
        PRESENTATION = 'presentation'
        $scope.editMode = ->
            if $scope.mode == EDIT
                return

            if $scope.mode == PRESENTATION
                $scope.result = $scope.expression
            $scope.resetText = 'CE'
            $scope.expression = ''
            $scope.mode = EDIT

        $scope.presentationMode = (answer)->
            console.debug 'presentationMode', arguments
            if $scope.mode == PRESENTATION
                return

            $scope.resetText = 'AC'
            $scope.result = $scope.expression
            $scope.expression = answer
            $scope.mode = PRESENTATION

        $scope.errorMode = ->
            if $scope.mode == ERROR
                return

            $scope.resetText = 'AC'
            $scope.mode = ERROR
            $scope.result = $scope.expression
            $scope.expression = 'Error'

        #######################################################################
        # Expression Modification
        #######################################################################
        $scope.digit = (digit)->
            $scope.editMode()
            $scope.expression += digit

        $scope.operator = (operator)->
            $scope.editMode()
            prefix = if operator in ['%', '(', ')'] then '' else ' '
            $scope.expression += prefix + operator

        $scope.reset = ()->
            $scope.editMode()
            $scope.expression = ''

        $scope.isEvaluating = false
        $scope.evaluate = ->
            $scope.isEvaluating = true
            params =
                expression: $scope.expression
            request = $http.get('/calculator/evaluate/', {params: params})
                .success((data, status, headers, config)->
                    $scope.isEvaluating = false
                    $scope.presentationMode(data.answer)
                )
                .error((data, status, headers, config)->
                    $scope.isEvaluating = false
                    $scope.errorMode()
                )

        # Initialize
        $scope.editMode()