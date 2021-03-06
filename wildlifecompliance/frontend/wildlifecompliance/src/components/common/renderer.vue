<template lang="html">
    <div>
        <div v-if="withSectionsSelector" class="col-lg-12" >
            <h3>Application {{application.id}}: {{application.licence_type_short_name}}</h3>
        </div>
        <div v-if="withSectionsSelector" class="col-md-3 sections-dropdown">
            <affix class="sections-menu" relative-element-selector="#tabs">
                <div class="panel panel-default fixed">
                <div class="panel-heading">
                    <div class="dropdown">
                        <ul class="list-unstyled">
                            <li class="open">
                                <h5>Sections</span></h5>
                                <ul class="dropdown-menu dropdown-panel">
                                    <li v-for="(tab, tab_idx) in renderer_tabs" class='dropdown-submenu'>
                                        <a tabindex='-1' class='section-menu' v-on:click="sectionClick(tab)">
                                            {{tab.name}}
                                            <span 
                                                :class="`fa fa-caret-${
                                                    tab.id == section_tab_id ? 'up': 'down'
                                                }`"
                                            />
                                        </a>
                                        <div class='dropdown-menu-right section-list' id='section-submenu' >
                                            <div v-for="(section, section_idx) in getSections(tab.id)"
                                                v-on:click="selectTab(tab)"
                                                v-scroll-to="`#${section.name}`"
                                                class="menu-row">
                                                    <div>
                                                        <i class="fa fa-circle"></i>
                                                        <span>{{section.label}}</span>
                                                    </div>
                                            </div>
                                        </div>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </div>
                </div>
                <div class="panel-body" style="padding:0">
                </div>
                </div>
            </affix>
        </div>
    </div>
</template>


<script>
import Vue from 'vue';
import { mapActions, mapGetters } from 'vuex';
import AmendmentRequestDetails from '@/components/forms/amendment_request_details.vue';
import '@/scss/forms/form.scss';

export default {
  name: 'renderer-form',
  components: {
      AmendmentRequestDetails,
  },
  data: function() {
    return {
        section_tab_id: 0,
    }
  },
  props:{
    withSectionsSelector:{
        type: Boolean,
        default: true
    },
    form_width: {
        type: String,
        default: 'col-md-9'
    }
  },
  computed: {
    ...mapGetters([
        'application',
        'selected_activity_tab_id',
        'renderer_tabs',
        'unfinishedActivities',
        'allCurrentActivities',
        'sectionsForTab',
        'allCurrentActivitiesWithAssessor',
    ]),
    listVisibleActivities: function() {
        if (this.$router.currentRoute.name=='complete-assessment'){
            // filtered activity list for application when completing assessments.
            return this.allCurrentActivitiesWithAssessor ? this.allCurrentActivitiesWithAssessor : this.allCurrentActivities;
        }
        return this.application.can_user_edit ? this.unfinishedActivities : this.allCurrentActivities;
    },
  },
  methods: {
    ...mapActions([
        'setRendererTabs',
        'setRendererSections',
        'setActivityTab',
    ]),
    selectTab: function(component) {
        this.section_tab_id = component.id;
        this.setActivityTab({id: component.id, name: component.label});
    },
    getSections: function(tab_id) {
        return tab_id == this.section_tab_id ? this.sectionsForTab(tab_id) : [];
    },
    initRendererTabs: function() {
        let tabs_list = [];
        for(let component of this.listVisibleActivities.filter(
            activity => activity.type == 'tab')) {
                if(!this.selected_activity_tab_id) {
                    this.selectTab(component);
                }
                tabs_list.push({name: component.name,
                                label: component.label,
                                id: component.id
                                });
        }
        this.setRendererTabs(tabs_list);
    },
    initRendererSections: function() {
        let sections = {};
        for(let component of this.listVisibleActivities.filter(
            activity => activity.type == 'tab' && activity.children)) {
                sections[component.id] = [];
                for(let section of component.children) {
                    sections[component.id].push({
                        name: section.name,
                        label: section.label
                    });
                }
        }
        this.setRendererSections(sections);
    },
    sectionClick: function(component) {
        if(this.section_tab_id == component.id) {
            this.section_tab_id = 0;  // Collapse the expanded panel upon double click.
        }
        else {
            this.section_tab_id = component.id;
        }
    },
  },
  mounted: function() {
      this.initRendererTabs();
      this.initRendererSections();
  },
}
</script>
