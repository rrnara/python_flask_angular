import * as moment from 'moment';
import { Component, OnInit } from '@angular/core';
import { isEmpty } from 'lodash';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-board-bookings',
  templateUrl: './board-bookings.component.html',
  styleUrls: ['./board-bookings.component.css']
})
export class BoardBookingsComponent implements OnInit {
  bookings: Array<any> = [];
  fetchResult = '';
  today = moment();
  selectedDate: NgbDateStruct = { year: this.today.year(), month: this.today.month() + 1, day: this.today.date() };
  isUserAdmin = false;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.fetchBookings();
    this.userService.getMe().subscribe(
      user => {
        this.isUserAdmin = user.role === 'admin';
      }
    );
  }

  numToStr(num: number, digits = 2) {
    return num.toString().padStart(digits, '0');
  }

  closeFetchResult() {
    this.fetchResult = '';
  }

  showFetchResult() {
    return !isEmpty(this.fetchResult);
  }

  fetchBookings(): void {
    const dt = `${this.numToStr(this.selectedDate.year, 4)}-${this.numToStr(this.selectedDate.month)}-${this.numToStr(this.selectedDate.day)}`;
    this.userService.getBookings(dt).subscribe(
      data => {
        this.bookings = data.bookings;
      },
      err => {
        this.fetchResult = JSON.parse(err.error).message;
      }
    );
  }

  onDateSelect(_event: any) {
    this.fetchBookings();
  }
}
