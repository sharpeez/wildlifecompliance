<template lang="html">
    <div id="applicationConditionDetail">
        <modal transition="modal fade" @ok="ok()" @cancel="cancel()" title="Condition" large>
            <div class="container-fluid">
                <div class="row">
                    <form class="form-horizontal" name="conditionForm">
                        <alert :show.sync="showError" type="danger"><strong>{{errorString}}</strong></alert>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <label class="radio-inline control-label"><input type="radio" name="conditionType" :value="true" v-model="condition.standard">Standard Condition</label>
                                <label class="radio-inline"><input type="radio" name="conditionType" :value="false" v-model="condition.standard">Free Text Condition</label>
                            </div>
                        </div>
                        <div class="col-sm-12">
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"  for="Name">Purpose</label>
                                    </div>
                                    <div class="col-sm-9" >
                                        <div style="width:70% !important">
                                            <select class="form-control" ref="select_purpose" name="purpose" v-model="condition.licence_purpose" >
                                                <option v-for="p in purposes" :value="p.id" >{{p.short_name}}</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"  for="Name">Condition</label>
                                    </div>
                                    <div class="col-sm-9" v-if="condition.standard">
                                        <div style="width:70% !important">
                                            <select class="form-control" ref="standard_req" name="standard_condition" v-model="condition.standard_condition">
                                                <option v-for="r in conditions" :value="r.id" >{{r.short_description}}</option>
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-sm-9" v-else>
                                        <textarea style="width: 70%;" class="form-control" name="free_condition" v-model="condition.free_condition"></textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <div class="row" v-if="!condition.standard || showDueDate">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"  for="Name">Due Date</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div class="input-group date" ref="due_date" style="width: 70%;">
                                            <input type="text" class="form-control" name="due_date" placeholder="DD/MM/YYYY" v-model="condition.due_date">
                                            <span class="input-group-addon">
                                                <span class="glyphicon glyphicon-calendar"></span>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group" v-if="!condition.standard && validDate">
                                <div class="row">
                                    <div class="col-sm-3">
                                        <label class="control-label pull-left"  for="Name">Return Type</label>
                                    </div>
                                    <div class="col-sm-9">
                                        <div style="width:70% !important">
                                            <select class="form-control" ref="return_types_select" name="return_type" v-model="condition.return_type">
                                                <option v-for="r in return_types" :value="r.id">{{r.name}}</option>
                                            </select>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <template v-if="showDueDate && validDate">
                                <div class="form-group">
                                    <div class="row">
                                        <div class="col-sm-3">
                                            <label class="control-label pull-left"  for="Name">Recurrence</label>
                                        </div>
                                        <div class="col-sm-9">
                                            <label class="checkbox-inline"><input type="checkbox" v-model="condition.recurrence"></label>
                                        </div>
                                    </div>
                                </div>
                                <template v-if="condition.recurrence">
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-3">
                                                <label class="control-label pull-left"  for="Name">Recurrence pattern</label>
                                            </div>
                                            <div class="col-sm-9">
                                                <label class="radio-inline control-label"><input type="radio" name="recurrenceSchedule" value="weekly" v-model="condition.recurrence_pattern">Weekly</label>
                                                <label class="radio-inline control-label"><input type="radio" name="recurrenceSchedule" value="monthly" v-model="condition.recurrence_pattern">Monthly</label>
                                                <label class="radio-inline control-label"><input type="radio" name="recurrenceSchedule" value="yearly" v-model="condition.recurrence_pattern">Yearly</label>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <div class="row">
                                            <div class="col-sm-12">
                                                <label class="control-label"  for="Name">
                                                    <strong class="pull-left">Recur every</strong> 
                                                    <input class="pull-left" style="width:10%; margin-left:10px;" type="number" name="schedule" v-model="condition.recurrence_schedule"/> 
                                                    <strong v-if="condition.recurrence_pattern == 'weekly'" class="pull-left" style="margin-left:10px;">week(s)</strong>
                                                    <strong v-else-if="condition.recurrence_pattern == 'monthly'" class="pull-left" style="margin-left:10px;">month(s)</strong>
                                                    <strong v-else-if="condition.recurrence_pattern == 'yearly'" class="pull-left" style="margin-left:10px;">year(s)</strong>
                                                </label>
                                            </div>
                                        </div>
                                    </div>
                                </template>
                            </template>
                        </div>
                    </form>
                </div>
            </div>
            <div slot="footer">
                <template v-if="condition.id">
                    <button type="button" v-if="updatingCondition" disabled class="btn btn-primary" @click="ok"><i class="fa fa-spinnner fa-spin"></i> Updating</button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Update</button>
                </template>
                <template v-else>
                    <button type="button" v-if="addingCondition" disabled class="btn btn-primary" @click="ok"><i class="fa fa-spinner fa-spin"></i> Adding</button>
                    <button type="button" v-else class="btn btn-primary" @click="ok">Add</button>
                </template>
                <button type="button" class="btn btn-primary" @click="cancel">Cancel</button>
            </div>
        </modal>
    </div>
</template>

<script>
//import $ from 'jquery'
import modal from '@vue-utils/bootstrap-modal.vue'
import alert from '@vue-utils/alert.vue'
import {helpers,api_endpoints} from "@/utils/hooks.js"

var select2 = require('select2');
require("select2/dist/css/select2.min.css");
require("select2-bootstrap-theme/dist/select2-bootstrap.min.css");

export default {
    name:'Condition-Detail',
    components:{
        modal,
        alert
    },
    props:{
            application_id:{
                type:Number,
                required: true
            },
            condition: {
                type: Object,
                required: true
            },
            conditions: {
                type: Array,
                required: true
            },
            licence_activity_tab:{
                type:Number,
                required:true
            },
            purposes: {
                type: Array,
                required: true
            },
    },
    data:function () {
        let vm = this;
        return {
            isModalOpen:false,
            form:null,
            return_types: [],
            addingCondition: false,
            updatingCondition: false,
            validation_form: null,
            type: '1',
            errors: false,
            errorString: '',
            successString: '',
            success:false,
            datepickerOptions:{
                format: 'DD/MM/YYYY',
                showClear:true,
                useCurrent:false,
                keepInvalid:true,
                allowInputToggle:true
            },
            validDate: false,
            showDueDate: false
        }
    },
    computed: {
        showError: function() {
            var vm = this;
            return vm.errors;
        },
        due_date: {
            cache: false,
            get(){
                if (this.condition.due_date == null){
                    return '';
                }
                else{
                    return this.condition.due_date;
                }
            }
        }  
    },
    watch: {
        due_date: function(){
            this.validDate = moment(this.condition.due_date,'DD/MM/YYYY').isValid();
        },
    },
    methods:{
        ok:function () {
            let vm =this;
            if($(vm.form).valid()){
                vm.sendData();
            }
        },
        setShowDueDate: function(val) {
            //Only show the Due Date field for Conditions which require a return.         
            let condition = this.conditions.filter(function(e) {return e.id == val})
            this.showDueDate=condition[0].require_return
        },       
        cancel:function () {
            this.close()
        },
        close:function () {
            this.isModalOpen = false;
            $(this.$refs.standard_req).val(null).trigger('change');
            this.errors = false;
            $('.has-error').removeClass('has-error');
            const datePicker = $(this.$refs.due_date).data('DateTimePicker');
            if(datePicker) {
                datePicker.clear();
            }
            this.showDueDate = false;
            this.validation_form.resetForm();
        },
        fetchContact: function(id){
            let vm = this;
            vm.$http.get(api_endpoints.contact(id)).then((response) => {
                vm.contact = response.body; vm.isModalOpen = true;
            },(error) => {
                console.log(error);
            } );
        },
        fetchReturnTypes() {
            this.$http.get(api_endpoints.return_types).then((response) => {
                this.return_types = response.body;
            },(error) => {
                console.log(error);
            })
        },
        sendData:function(){
            let vm = this;
            vm.errors = false;
            vm.condition.licence_activity=vm.licence_activity_tab;
            let condition = JSON.parse(JSON.stringify(vm.condition));
            if (condition.standard){
                condition.free_condition = '';
            }
            else{
                condition.standard_condition = '';
                $(this.$refs.standard_req).val(null).trigger('change');
            }
            if (!condition.due_date){
                condition.due_date = null;
                condition.return_type = null;
                condition.recurrence = false;
                delete condition.recurrence_pattern;
                condition.recurrence_schedule ? delete condition.recurrence_schedule : '';
            }
            if (vm.condition.id){
                vm.updatingCondition = true;
                vm.$http.post(helpers.add_endpoint_json(api_endpoints.application_conditions,condition.id+'/update_condition'),JSON.stringify(condition),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.updatingCondition = false;
                        vm.$parent.updatedConditions();
                        vm.close();
                    },(error)=>{
                        vm.errors = true;
                        vm.errorString = helpers.apiVueResourceError(error);
                        vm.updatingCondition = false;
                    });
            } else {
                vm.addingCondition = true;
                vm.$http.post(api_endpoints.application_conditions,JSON.stringify(condition),{
                        emulateJSON:true,
                    }).then((response)=>{
                        vm.addingCondition = false;
                        vm.close();
                        vm.$parent.updatedConditions();
                    },(error)=>{
                        vm.errors = true;
                        vm.addingCondition = false;
                        vm.errorString = helpers.apiVueResourceError(error);
                    });
                
            }
        },
        addFormValidations: function() {
            let vm = this;
            vm.validation_form = $(vm.form).validate({
                rules: {
                    standard_condition:{
                        required: {
                            depends: function(el){
                                return vm.condition.standard;
                            }
                        }
                    },
                    free_condition:{
                        required: {
                            depends: function(el){
                                return !vm.condition.standard;
                            }
                        }
                    },
                    schedule:{
                        required: {
                            depends: function(el){
                                return vm.condition.recurrence;
                            }
                        }
                    }
                },
                messages: {
                    arrival:"field is required",
                    departure:"field is required",
                    campground:"field is required",
                    campsite:"field is required"
                },
                showErrors: function(errorMap, errorList) {
                    $.each(this.validElements(), function(index, element) {
                        var $element = $(element);
                        $element.attr("data-original-title", "").parents('.form-group').removeClass('has-error');
                    });
                    // destroy tooltips on valid elements
                    $("." + this.settings.validClass).tooltip("destroy");
                    // add or update tooltips
                    for (var i = 0; i < errorList.length; i++) {
                        var error = errorList[i];
                        $(error.element)
                            .tooltip({
                                trigger: "focus"
                            })
                            .attr("data-original-title", error.message)
                            .parents('.form-group').addClass('has-error');
                    }
                }
            });
       },
       setConditionSelector: function () {
            let vm = this;
            // Intialise select2
            $(vm.$refs.standard_req).select2({
                "theme": "bootstrap",
                allowClear: true,
                minimumInputLength: 2,
                placeholder:"Select Condition..."
            }).
            on("select2:selecting",function (e) {
                var selected = $(e.currentTarget);
                vm.showDueDate = false;
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.condition.standard_condition = selected.val();
                vm.setShowDueDate(selected.val());
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.condition.standard_condition = selected.val();
            });
       },
       setPurposeSelector: function () {
            let vm = this;

            $(vm.$refs.select_purpose).select2({
                "theme": "bootstrap",
                allowClear: true,
                placeholder:"Select Purpose..."
            }).
            on("select2:select",function (e) {
                var selected = $(e.currentTarget);
                vm.condition.licence_purpose = selected.val();
            }).
            on("select2:unselect",function (e) {
                var selected = $(e.currentTarget);
                vm.condition.licence_purpose = selected.val();
            });
       },
       eventListeners:function () {
            let vm = this;
            vm.setConditionSelector();
            vm.setPurposeSelector();
       }
   },
   updated:function () {
       let vm = this;
       vm.setPurposeSelector();
       vm.setConditionSelector();
       if (vm.condition.free_condition || vm.condition.due_date){
            vm.showDueDate=true;
       }
       // Initialise Date Picker
       if (!vm.condition.standard || vm.showDueDate) {
            $(vm.$refs.due_date).datetimepicker(vm.datepickerOptions);
            $(vm.$refs.due_date).on('dp.change', function(e){
                if ($(vm.$refs.due_date).data('DateTimePicker').date()) {
                    vm.condition.due_date =  e.date.format('DD/MM/YYYY');
                }
                else if ($(vm.$refs.due_date).data('date') === "") {
                    vm.condition.due_date = "";
                }
            });       
       }
   },
   mounted:function () {
        let vm =this;
        vm.form = document.forms.conditionForm;
        vm.addFormValidations();
        vm.fetchReturnTypes();
        this.$nextTick(()=>{
            vm.eventListeners();
        });
   }
}
</script>

<style lang="css">
</style>
