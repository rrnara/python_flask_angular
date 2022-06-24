import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardCleanersComponent } from './board-cleaners.component';

describe('BoardCleanersComponent', () => {
  let component: BoardCleanersComponent;
  let fixture: ComponentFixture<BoardCleanersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardCleanersComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardCleanersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
