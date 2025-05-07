'use strict';

customElements.define('compodoc-menu', class extends HTMLElement {
    constructor() {
        super();
        this.isNormalMode = this.getAttribute('mode') === 'normal';
    }

    connectedCallback() {
        this.render(this.isNormalMode);
    }

    render(isNormalMode) {
        let tp = lithtml.html(`
        <nav>
            <ul class="list">
                <li class="title">
                    <a href="index.html" data-type="index-link">scheduler-app documentation</a>
                </li>

                <li class="divider"></li>
                ${ isNormalMode ? `<div id="book-search-input" role="search"><input type="text" placeholder="Type to search"></div>` : '' }
                <li class="chapter">
                    <a data-type="chapter-link" href="index.html"><span class="icon ion-ios-home"></span>Getting started</a>
                    <ul class="links">
                        <li class="link">
                            <a href="overview.html" data-type="chapter-link">
                                <span class="icon ion-ios-keypad"></span>Overview
                            </a>
                        </li>
                        <li class="link">
                            <a href="index.html" data-type="chapter-link">
                                <span class="icon ion-ios-paper"></span>README
                            </a>
                        </li>
                                <li class="link">
                                    <a href="dependencies.html" data-type="chapter-link">
                                        <span class="icon ion-ios-list"></span>Dependencies
                                    </a>
                                </li>
                                <li class="link">
                                    <a href="properties.html" data-type="chapter-link">
                                        <span class="icon ion-ios-apps"></span>Properties
                                    </a>
                                </li>
                    </ul>
                </li>
                    <li class="chapter modules">
                        <a data-type="chapter-link" href="modules.html">
                            <div class="menu-toggler linked" data-bs-toggle="collapse" ${ isNormalMode ?
                                'data-bs-target="#modules-links"' : 'data-bs-target="#xs-modules-links"' }>
                                <span class="icon ion-ios-archive"></span>
                                <span class="link-name">Modules</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                        </a>
                        <ul class="links collapse " ${ isNormalMode ? 'id="modules-links"' : 'id="xs-modules-links"' }>
                            <li class="link">
                                <a href="modules/AppModule.html" data-type="entity-link" >AppModule</a>
                                    <li class="chapter inner">
                                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ?
                                            'data-bs-target="#components-links-module-AppModule-d33d84d2ce6ca1645fc0e44d05236cf56394dd82aec52fe1bd876a61c01177811e681ccbce5fb7a2355a1d673f08eeb1d67ce3ac23f1b36a197dc5449ca4ab5a"' : 'data-bs-target="#xs-components-links-module-AppModule-d33d84d2ce6ca1645fc0e44d05236cf56394dd82aec52fe1bd876a61c01177811e681ccbce5fb7a2355a1d673f08eeb1d67ce3ac23f1b36a197dc5449ca4ab5a"' }>
                                            <span class="icon ion-md-cog"></span>
                                            <span>Components</span>
                                            <span class="icon ion-ios-arrow-down"></span>
                                        </div>
                                        <ul class="links collapse" ${ isNormalMode ? 'id="components-links-module-AppModule-d33d84d2ce6ca1645fc0e44d05236cf56394dd82aec52fe1bd876a61c01177811e681ccbce5fb7a2355a1d673f08eeb1d67ce3ac23f1b36a197dc5449ca4ab5a"' :
                                            'id="xs-components-links-module-AppModule-d33d84d2ce6ca1645fc0e44d05236cf56394dd82aec52fe1bd876a61c01177811e681ccbce5fb7a2355a1d673f08eeb1d67ce3ac23f1b36a197dc5449ca4ab5a"' }>
                                            <li class="link">
                                                <a href="components/AppComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AppComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/DataComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >DataComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/LoginComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >LoginComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/RegistrationComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >RegistrationComponent</a>
                                            </li>
                                        </ul>
                                    </li>
                            </li>
                            <li class="link">
                                <a href="modules/AppRoutingModule.html" data-type="entity-link" >AppRoutingModule</a>
                            </li>
                            <li class="link">
                                <a href="modules/HomeModule.html" data-type="entity-link" >HomeModule</a>
                                    <li class="chapter inner">
                                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ?
                                            'data-bs-target="#components-links-module-HomeModule-d7d0fe2266a556cf08662f966512bef98a6985c503bfd54de206c250673d22dacd3c8eecab3b56e9f642a079c17c51871b3264b4b7a864e0c39b9185d8cbca76"' : 'data-bs-target="#xs-components-links-module-HomeModule-d7d0fe2266a556cf08662f966512bef98a6985c503bfd54de206c250673d22dacd3c8eecab3b56e9f642a079c17c51871b3264b4b7a864e0c39b9185d8cbca76"' }>
                                            <span class="icon ion-md-cog"></span>
                                            <span>Components</span>
                                            <span class="icon ion-ios-arrow-down"></span>
                                        </div>
                                        <ul class="links collapse" ${ isNormalMode ? 'id="components-links-module-HomeModule-d7d0fe2266a556cf08662f966512bef98a6985c503bfd54de206c250673d22dacd3c8eecab3b56e9f642a079c17c51871b3264b4b7a864e0c39b9185d8cbca76"' :
                                            'id="xs-components-links-module-HomeModule-d7d0fe2266a556cf08662f966512bef98a6985c503bfd54de206c250673d22dacd3c8eecab3b56e9f642a079c17c51871b3264b4b7a864e0c39b9185d8cbca76"' }>
                                            <li class="link">
                                                <a href="components/AssignmentLogicDialogComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >AssignmentLogicDialogComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ClassComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ClassComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ColumnSelectorDialogComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ColumnSelectorDialogComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ConflictCardComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ConflictCardComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ConflictManagerComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ConflictManagerComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/DetailsComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >DetailsComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/FileManagerComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >FileManagerComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/HomeComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >HomeComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/ProfileComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >ProfileComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/SectionComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >SectionComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/SectionRowComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >SectionRowComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/TrainingDataDialogComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >TrainingDataDialogComponent</a>
                                            </li>
                                            <li class="link">
                                                <a href="components/UploadComponent.html" data-type="entity-link" data-context="sub-entity" data-context-id="modules" >UploadComponent</a>
                                            </li>
                                        </ul>
                                    </li>
                            </li>
                            <li class="link">
                                <a href="modules/HomeRoutingModule.html" data-type="entity-link" >HomeRoutingModule</a>
                            </li>
                </ul>
                </li>
                        <li class="chapter">
                            <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#injectables-links"' :
                                'data-bs-target="#xs-injectables-links"' }>
                                <span class="icon ion-md-arrow-round-down"></span>
                                <span>Injectables</span>
                                <span class="icon ion-ios-arrow-down"></span>
                            </div>
                            <ul class="links collapse " ${ isNormalMode ? 'id="injectables-links"' : 'id="xs-injectables-links"' }>
                                <li class="link">
                                    <a href="injectables/DataService.html" data-type="entity-link" >DataService</a>
                                </li>
                                <li class="link">
                                    <a href="injectables/TrainingDataService.html" data-type="entity-link" >TrainingDataService</a>
                                </li>
                            </ul>
                        </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interceptors-links"' :
                            'data-bs-target="#xs-interceptors-links"' }>
                            <span class="icon ion-ios-swap"></span>
                            <span>Interceptors</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="interceptors-links"' : 'id="xs-interceptors-links"' }>
                            <li class="link">
                                <a href="interceptors/AuthInterceptor.html" data-type="entity-link" >AuthInterceptor</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#interfaces-links"' :
                            'data-bs-target="#xs-interfaces-links"' }>
                            <span class="icon ion-md-information-circle-outline"></span>
                            <span>Interfaces</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? ' id="interfaces-links"' : 'id="xs-interfaces-links"' }>
                            <li class="link">
                                <a href="interfaces/ClassMeeting.html" data-type="entity-link" >ClassMeeting</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/ConflictView.html" data-type="entity-link" >ConflictView</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/StoredFile.html" data-type="entity-link" >StoredFile</a>
                            </li>
                            <li class="link">
                                <a href="interfaces/TrainingInfo.html" data-type="entity-link" >TrainingInfo</a>
                            </li>
                        </ul>
                    </li>
                    <li class="chapter">
                        <div class="simple menu-toggler" data-bs-toggle="collapse" ${ isNormalMode ? 'data-bs-target="#miscellaneous-links"'
                            : 'data-bs-target="#xs-miscellaneous-links"' }>
                            <span class="icon ion-ios-cube"></span>
                            <span>Miscellaneous</span>
                            <span class="icon ion-ios-arrow-down"></span>
                        </div>
                        <ul class="links collapse " ${ isNormalMode ? 'id="miscellaneous-links"' : 'id="xs-miscellaneous-links"' }>
                            <li class="link">
                                <a href="miscellaneous/variables.html" data-type="entity-link">Variables</a>
                            </li>
                        </ul>
                    </li>
                        <li class="chapter">
                            <a data-type="chapter-link" href="routes.html"><span class="icon ion-ios-git-branch"></span>Routes</a>
                        </li>
                    <li class="chapter">
                        <a data-type="chapter-link" href="coverage.html"><span class="icon ion-ios-stats"></span>Documentation coverage</a>
                    </li>
                    <li class="divider"></li>
                    <li class="copyright">
                        Documentation generated using <a href="https://compodoc.app/" target="_blank" rel="noopener noreferrer">
                            <img data-src="images/compodoc-vectorise.png" class="img-responsive" data-type="compodoc-logo">
                        </a>
                    </li>
            </ul>
        </nav>
        `);
        this.innerHTML = tp.strings;
    }
});