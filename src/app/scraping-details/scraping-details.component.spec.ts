import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ScrapingDetailsComponent } from './scraping-details.component';

describe('ScrapingDetailsComponent', () => {
  let component: ScrapingDetailsComponent;
  let fixture: ComponentFixture<ScrapingDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ScrapingDetailsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ScrapingDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
