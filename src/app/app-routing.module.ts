import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SiteListComponent } from './site-list/site-list.component';
import { ConfigComponent } from './config/config.component';
import { LoginComponent } from './login/login.component';
import { AuthGuard } from './auth-guard.service';


const routes: Routes = [
  { path: 'sites', component: SiteListComponent, canActivate: [AuthGuard] }, // Utilisez le garde d'authentification
  { path: 'config/:siteId', component: ConfigComponent, canActivate: [AuthGuard] },
  { path: 'login', component: LoginComponent },
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: '**', redirectTo: '/sites', pathMatch: 'full' }, // Gestion de la route par défaut
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
  providers: [AuthGuard]
})
export class AppRoutingModule { }
