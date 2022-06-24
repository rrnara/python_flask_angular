import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BoardBookingsComponent } from './board-bookings.component';

describe('BoardCleanersComponent', () => {
  let component: BoardBookingsComponent;
  let fixture: ComponentFixture<BoardBookingsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ BoardBookingsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BoardBookingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
