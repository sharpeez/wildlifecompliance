<template lang="html" >
    <div class="container" >
        <div class="row">
            <div class="col-sm-12">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h3 class="panel-title">{{applicationTitle}} for
                            <span v-if="selected_apply_org_id">{{ selected_apply_org_id_details.name }} ({{ selected_apply_org_id_details.abn }})</span>
                            <span v-if="selected_apply_proxy_id">{{ selected_apply_proxy_id_details.first_name }} {{ selected_apply_proxy_id_details.last_name }} ({{ selected_apply_proxy_id_details.email }})</span>
                            <span v-if="!selected_apply_org_id && !selected_apply_proxy_id">yourself</span>
                            <a :href="'#'+pBody" data-toggle="collapse"  data-parent="#userInfo" expanded="true" :aria-controls="pBody">
                                <span class="glyphicon glyphicon-chevron-up pull-right "></span>
                            </a>
                        </h3>
                    </div>

                    <div class="panel-body collapse in" :id="pBody">
                        <form v-if="categoryCount" class="form-horizontal" name="personal_form" method="post">
                          
                            <div class="col-sm-12" v-show='current_user.is_reception' >
                                <div class="row">
                                    <label class="col-sm-3">
                                        Payment method for customer:
                                    </label>
                                    <div class="col-sm-6">
                                        <input type="radio" checked="checked" name="reception" value="card" v-model="customer_pay_method" > Credit Card &nbsp;&nbsp;</input>
                                        <input type="radio" name="reception" id="cash" value="cash" v-model="customer_pay_method" > Cash &nbsp;&nbsp;</input>
                                        <input type="radio" name="reception" id="none" value="none" v-model="customer_pay_method" > No Payment &nbsp;&nbsp;</input>
                                    </div>
                                </div>
                            </div>
                            <br /><br />
                            <div class="col-sm-12">
                                <div class="row">
                                    <label class="col-sm-6">
                                        {{ selectionLabel }}:
                                    </label>
                                </div>

                                <div class="margin-left-20">
                                <div v-for="(category,index) in visibleLicenceCategories" class="radio">
                                    <div class ="row">
                                        <div class="col-sm-9" >  
                                            <input type="radio"  :id="category.id" name="licence_category" v-model="licence_categories.id"  :value="category.id" @change="handleRadioChange($event,index)"> {{category.short_name}}
                                             
                                            <div class="row">


                                                <div  v-if="category.checked" class="col-sm-9">

                                                    <div v-if="!(selected_apply_org_id != '' && type.not_for_organisation == true)" v-for="(type,index1) in category.activity" class="checkbox margin-left-20">
                                                        <input type="checkbox" ref="selected_activity_type" name ="activity" :value="type.id" :id = "type.id" v-model="category.activity[index1].selected" @change="handleActivityCheckboxChange(index,index1)"> {{type.short_name}}

                                                        <div v-if="type.selected">
                                                            <div v-for="(purpose,index2) in type.purpose" class="checkbox purpose-clear-left">

                                                                <div v-if="purpose.is_valid_age" class ="col-sm-12">
                                                                    <input type="checkbox"
                                                                        :value="purpose.id"
                                                                        :id="purpose.id"
                                                                        v-model="type.purpose[index2].selected"
                                                                        @change="handlePurposeCheckboxChange(index,$event)">
                                                                            {{purpose.name}}
                                                                            <span> ({{parseFloat(purpose.base_application_fee) | toCurrency}} + {{parseFloat(purpose.base_licence_fee) | toCurrency}})</span>
                                                                </div>

                                                                <div v-else class ="col-sm-12">
                                                                    <input type="checkbox" disabled :value="purpose.id" :id="purpose.id" v-model="type.purpose[index2].selected" >
                                                                    {{purpose.name}}
                                                                    <span> (Minimum age {{purpose.minimum_age}} years)</span>
                                                                </div>

                                                            </div>
                                                        </div>
                                                    </div>
                                                </div> 
                                                <div v-else="!radio_selected[index]" class="col-sm-4">
                                                    
                                                </div>
                                            </div>
                                        </div>
                                    </div> 
                                </div>
                                </div>
                            </div>
                            <div class="col-sm-12">
                                <button v-if="showSpinner" type="button" class="btn btn-primary pull-right" style="margin-left: 10px;" disabled><i class="fa fa-spinner fa-spin" />Continue</button>
                                <button v-else @click.prevent="submit()" type="button" class="btn btn-primary pull-right" style="margin-left: 10px;">Continue</button>
                                <div class="pull-right" style="font-size: 18px;">
                                    <strong>Estimated application fee: {{application_fee | toCurrency}}</strong><br>
                                    <strong>Estimated licence fee: {{licence_fee | toCurrency}}</strong><br>
                                </div>
                            </div>
                        </form>
                        <div v-else-if="!categoryCount && (isAmendment || isRenewal)">
                            <div class="col-sm-12">
                                <div class="row">
                                    <br/><br/><br/><br/>
                                    <center><i class="fa fa-4x fa-spinner fa-spin"/></center>
                                    <br/><br/><br/><br/>
                                </div>
                            </div>
                        </div>
                        <div v-else >
                            <div class="col-sm-12">
                                <div class="row">
                                    <label>
                                        <!-- No matching licensed activities found. -->
                                    </label>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import {
  api_endpoints,
  helpers
}
from '@/utils/hooks'
import { mapActions, mapGetters } from 'vuex'
import utils from './utils'
import internal_utils from '@/components/internal/utils'
export default {
  data: function() {
    let vm = this;
    return {
        licence_category : this.$route.params.licence_category,
        licence_activity : this.$route.params.licence_activity,
        licence_no : this.$route.params.licence_no,
        select_activity : this.$route.params.select_activity,
        select_purpose : this.$route.params.select_purpose,
        select_licence_purpose : this.$route.params.select_licence_purpose,
        application: null,
        agent: {},
        activity :{
            id:null,
            purpose:[]
        },
        
        radio_selected : [],
        selected_activity:[],
        activity_type_showing : [],
        organisations:null,
        licence_categories : {
            checked:false,
            activity:[
             { 
             	id:null,
                selected:false,
                purpose:[]
             }
            ]
        },
        "loading": [],
        form: null,
        pBody: 'pBody' + vm._uid,
        application_fee: 0,
        licence_fee: 0,
        selected_apply_org_id_details : {},
        selected_apply_proxy_id_details: {},
        customer_pay_method: 'card',
        spinner: false,
    }
  },
  components: {
  },
  computed: {
        ...mapGetters([
            'selected_apply_org_id',
            'selected_apply_proxy_id',
            'selected_apply_licence_select',
            'application_workflow_state',
            'reception_method_id',
            'current_user',
        ]),
        applicationTitle: function() {
            switch(this.selected_apply_licence_select) {
                case 'new_activity':
                    return 'Apply for a new activity';
                break;
                case 'amend_activity':
                    return 'Amend one or more licensed activities';
                break;
                case 'renew_activity':
                    return 'Renew one or more licensed activities';
                break;
                case 'reissue_activity':
                    return 'Reissue one or more licensed activities';
                break;
                default:
                    return 'Apply for a new licence';
                break;
            }
        },
        selectionLabel: function() {
            return this.isAmendment ?
            `Select the licence activity and purposes you wish to amend` :
            this.isRenewal ?
            `Select one or more activities and purposes you wish to renew` :
            this.isReissue ?
            `Select one or more activities and purposes you wish to reissue` :
            `Select the class of licence you wish to apply for`;
        },
        categoryCount: function() {
            return this.visibleLicenceCategories.length;
        },
        visibleLicenceCategories: function() {
            return this.licence_categories;
        },
        isAmendment: function() {
            return this.selected_apply_licence_select && this.selected_apply_licence_select === 'amend_activity'
        },
        isRenewal: function() {
            return this.selected_apply_licence_select && this.selected_apply_licence_select === 'renew_activity'
        },
        isReissue: function() {
            return this.selected_apply_licence_select && this.selected_apply_licence_select === 'reissue_activity'
        },
        showSpinner: function() {
            return this.spinner
        },
  },
  methods: {
    ...mapActions([
        'setApplicationWorkflowState',
        'setReceptionMethodId',
        'loadCurrentUser',
    ]),
    submit: function() {
        let vm = this;
        vm.spinner = true;
        swal({
            title: "Create Application",
            text: "Are you sure you want to create an application?",
            type: "question",
            showCancelButton: true,
            confirmButtonText: 'Accept'
        }).then((result) => {
            if (result.value) {
               vm.createApplication();
            }
        },(error) => {
            vm.spinner = false;
        });
        vm.spinner = false;
    },
    handleRadioChange: function(e,index){
        let vm=this
        for(var i=0,_len=vm.licence_categories.length;i<_len;i++){
            if(i===index){
                vm.licence_categories[i].checked = true;
            }else{
                for(var activity_type_index=0, len1=vm.licence_categories[i].activity.length; activity_type_index<len1; activity_type_index++){
                        if (vm.licence_categories[i].activity[activity_type_index].selected){
                            vm.licence_categories[i].activity[activity_type_index].selected=false;
                            for(var activity_index=0, len2=vm.licence_categories[i].activity[activity_type_index].purpose.length; activity_index<len2; activity_index++){
                                vm.licence_categories[i].activity[activity_type_index].purpose[activity_index].selected = false;
                                vm.application_fee = 0;
                                vm.licence_fee = 0;
                            }    
                        }
                }
                vm.licence_categories[i].checked=false;
            }

        }
    },
    handleActivityCheckboxChange:function(index,index1){
        let vm = this
        var input = $(vm.$refs.selected_activity_type)[0];
        if(vm.licence_categories[index].activity[index1].selected){
            for(var activity_index=0, len2=vm.licence_categories[index].activity[index1].purpose.length; activity_index<len2; activity_index++){
                vm.licence_categories[index].activity[index1].purpose[activity_index].selected = this.isAmendment || this.isRenewal;
                if (this.isAmendment) {
                    this.application_fee = this.application_fee + vm.licence_categories[index].activity[index1].purpose[activity_index].amendment_application_fee
                    this.licence_fee = this.licence_fee + vm.licence_categories[index].activity[index1].purpose[activity_index].base_licence_fee
                }
                if (this.isRenewal) {
                    this.application_fee = this.application_fee + vm.licence_categories[index].activity[index1].purpose[activity_index].renewal_application_fee
                    this.licence_fee = this.licence_fee + vm.licence_categories[index].activity[index1].purpose[activity_index].base_licence_fee
                }
            }
        }
    },
    handlePurposeCheckboxChange:function(index, event){
        const purpose_ids = [].concat.apply([], this.licence_categories[index].activity.map(
            activity => activity.purpose.filter(
                purpose => purpose.selected || (purpose.id == event.target.id && event.target.checked)
            ))).map(purpose => purpose.id);
        this.$http.post('/api/application/estimate_price/', {
                'purpose_ids': purpose_ids,
                'licence_type': this.selected_apply_licence_select,
            }).then(res => {
                this.application_fee = res.body.fees.application;
                this.licence_fee = res.body.fees.licence;

        }, err => {
            console.log(err);
        });
    },
    createApplication:function () {
        let vm = this;
        vm.spinner = true;
        let licence_purposes = [];
        let count_total_licence_categories = 0
        let count_total_activities = 0
        let count_total_purposes = 0
        let count_selected_purposes_this_loop = 0
        let data = new FormData()

        // loop through level 1 and find selected licence class (radio option, only one)
        for(var i=0,_len1=vm.licence_categories.length;i<_len1;i++){

            // if licence class selected
            if(vm.licence_categories[i].checked){

                // loop through level 2 and find selected activity (checkboxes, one or more)
                for(var j=0,_len2=vm.licence_categories[i].activity.length;j<_len2;j++){

                    // if activity selected
                    if(vm.licence_categories[i].activity[j].selected){

                        // reset current loop total of selected purposes for this activity (level 3)
                        count_selected_purposes_this_loop = 0

                        // loop through level 3 and find selected activity (checkboxes, one or more)
                        for(var k=0,_len3=vm.licence_categories[i].activity[j].purpose.length;k<_len3;k++){

                            // if activity selected
                            if(vm.licence_categories[i].activity[j].purpose[k].selected){
                                count_selected_purposes_this_loop++;
                                count_total_purposes++;

                                licence_purposes.push(vm.licence_categories[i].activity[j].purpose[k].id);
                                // end of selected activity loop
                        	}
                        }

                        // only if there is at least one activity selected for this activity
                        if(count_selected_purposes_this_loop > 0){
                            count_total_activities++;
                        }

                        // end of selected activity loop
                    }

                }

                count_total_licence_categories++; // this should always be 1 at end of full loop

                // end of selected licence class loop
            }
        }

        // if no selections, display error do not continue
        if(count_total_purposes == 0){
            swal({
                title: "Create Application",
                text: "Please ensure at least one licence purpose is selected",
                type: "error",
            })
        } else {
            data.organisation_id=vm.selected_apply_org_id;
            data.proxy_id=vm.selected_apply_proxy_id;
            data.application_fee=vm.application_fee;
            data.licence_fee=vm.licence_fee;
            data.licence_purposes=licence_purposes;
            data.application_type = vm.selected_apply_licence_select;
            data.customer_method_id = vm.customer_pay_method;
            data.selected_activity = vm.select_activity;
            data.selected_purpose = vm.select_purpose;
            vm.$http.post('/api/application.json',JSON.stringify(data),{emulateJSON:true}).then(res => {
                vm.setApplicationWorkflowState({bool: false});
                vm.setReceptionMethodId({pay_method: this.customer_pay_method});
                vm.application = res.body;
                vm.spinner = false;
                vm.$router.push({
                    name:"draft_application",
                    params:{application_id:vm.application.id}
                });
            }, err => {
                console.log(err);
                vm.spinner = false;
                swal(
                    'Application Error',
                    helpers.apiVueResourceError(err),
                    'error'
                )
            });
        }
    },
    createSelectedPurposeApplication: function() {
        let vm = this;
        vm.spinner = true;
        let licence_purposes = [vm.select_licence_purpose];
        let data = new FormData()
        data.organisation_id=vm.selected_apply_org_id;
        data.proxy_id=vm.selected_apply_proxy_id;
        data.application_fee=vm.application_fee;
        data.licence_fee=vm.licence_fee;
        data.licence_purposes=licence_purposes;
        data.application_type = vm.selected_apply_licence_select;
        data.customer_method_id = vm.customer_pay_method;
        data.selected_activity = vm.select_activity;
        data.selected_purpose = vm.select_purpose;
        vm.$http.post('/api/application.json',JSON.stringify(data),{emulateJSON:true}).then(res => {
            vm.setApplicationWorkflowState({bool: false});
            vm.setReceptionMethodId({pay_method: this.customer_pay_method});
            vm.application = res.body;
            vm.spinner = false;
            vm.$router.push({
                name:"draft_application",
                params:{application_id:vm.application.id}
            });
        }, err => {
            console.log(err);
            vm.spinner = false;
            swal(
                'Application Error',
                helpers.apiVueResourceError(err),
                'error'
            )
        });
    },
    setupInitialisers: function() {
        let initialisers = [
            utils.fetchLicenceAvailablePurposes({
                "application_type": this.selected_apply_licence_select,
                "licence_category": this.licence_category,
                "licence_activity": this.licence_activity,
                "proxy_id": this.selected_apply_proxy_id,
                "organisation_id": this.selected_apply_org_id,
                "licence_no": this.licence_no,
                "select_activity": this.select_activity,
                "select_purpose": this.select_purpose,
            }),
            this.selected_apply_org_id ? utils.fetchOrganisation(this.selected_apply_org_id) : '',
            this.selected_apply_proxy_id ? internal_utils.fetchUser(this.selected_apply_proxy_id) : '',
        ];

        Promise.all(initialisers).then(data => {
            this.licence_categories = data[0];
            this.selected_apply_org_id_details = data[1];
            this.selected_apply_proxy_id_details = data[2];
        });
    }
  },
  mounted: function() {
      if (['amend_activity','renew_activity'].includes(this.selected_apply_licence_select)) {
          this.createSelectedPurposeApplication();

      } else {
          this.setupInitialisers();
      }

  },
  beforeRouteEnter:function(to,from,next){
    next(vm => {
        vm.loadCurrentUser({ url: `/api/my_user_details` });
        // Sends the user back to the first application workflow screen if licence_select is null
        // or workflow state was interrupted (e.g. lost from page refresh)
        if(vm.selected_apply_licence_select == null || !vm.application_workflow_state) {
            return vm.$router.push({
                name: "apply_application_organisation",
            });
        }
    });
  },
}
</script>

<style lang="css">
div.margin-left-20 {
    margin-left: 20px;
}
div.purpose-clear-left {
    clear: left;
}
</style>
