import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HttpClientModule, HttpClient } from '@angular/common/http';
import { provideHttpClient, withFetch } from '@angular/common/http';
import { SiteListComponent } from './site-list/site-list.component';
import { ConfigComponent } from './config/config.component';
import { FormsModule } from '@angular/forms';
import { DatePipe } from '@angular/common';
import { LoginComponent } from './login/login.component';
import { NavigateComponent } from './navigate/navigate.component';
import { ScrapingDetailsComponent } from './scraping-details/scraping-details.component';

@NgModule({
  declarations: [
    AppComponent,
    SiteListComponent,
    ConfigComponent,
    LoginComponent,
    NavigateComponent,
    ScrapingDetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    provideHttpClient(withFetch()),
    DatePipe

  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
