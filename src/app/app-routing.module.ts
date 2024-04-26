import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SiteListComponent } from './site-list/site-list.component';
import { ConfigComponent } from './config/config.component';


const routes: Routes = [
  { path: 'sites', component: SiteListComponent },
  { path: 'config/:siteId', component: ConfigComponent }, // Route pour la page de configuration avec le nom du site en paramètre
  { path: '', redirectTo: '/sites', pathMatch: 'full' },
  { path: '**', redirectTo: '/sites', pathMatch: 'full' }, // Gestion de la route par défaut
  
];


@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
