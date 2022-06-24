import * as moment from 'moment';
import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { isEmpty } from 'lodash';
import { NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-board-cleaners',
  templateUrl: './board-cleaners.component.html',
  styleUrls: ['./board-cleaners.component.css']
})
export class BoardCleanersComponent implements OnInit {
  cleaners: Array<any> = [];
  fetchResult = '';
  tomorrow = moment().add(1, 'day');
  minPickerDate: NgbDateStruct = { year: this.tomorrow.year(), month: this.tomorrow.month() + 1, day: this.tomorrow.date() }
  selectedDate: NgbDateStruct = { year: this.tomorrow.year(), month: this.tomorrow.month() + 1, day: this.tomorrow.date() };
  isUserAdmin = false;

  addCleanerForm = this.formBuilder.group({
    badge: '',
    name: ''
  });
  addResult: string = '';

  bookingResult: string = '';

  constructor(private formBuilder: FormBuilder, private userService: UserService) { }

  ngOnInit(): void {
    this.fetchCleaners();
    this.userService.getMe().subscribe(
      user => {
        this.isUserAdmin = user.role === 'admin';
      }
    );
  }

  numToStr(num: number, digits = 2) {
    return num.toString().padStart(digits, '0');
  }

  selectedToDate() {
    return `${this.numToStr(this.selectedDate.year, 4)}-${this.numToStr(this.selectedDate.month)}-${this.numToStr(this.selectedDate.day)}`;
  }

  fetchCleaners(): void {
    this.userService.getCleaners(this.selectedToDate()).subscribe(
      data => {
        this.cleaners = data.cleaners;
      },
      err => {
        this.fetchResult = JSON.parse(err.error).message;
      }
    );
  }

  closeFetchResult() {
    this.fetchResult = '';
  }

  showFetchResult() {
    return !isEmpty(this.fetchResult);
  }

  onDateSelect(_event: any) {
    this.fetchCleaners();
  }

  // Only for admin
  addCleaner(): void {
    const { badge, name } = this.addCleanerForm.value
    if (!isEmpty(badge) && !isEmpty(name)) {
      this.userService.addCleaner(badge, name).subscribe(
        data => {
          if (data.success) {
            this.addResult = 'Added';
            setTimeout(() => {
              this.addResult = '';
            }, 3000);
            this.addCleanerForm.reset();
            this.fetchCleaners();
          } else {
            this.addResult = data.msg;
          }
        },
        err => {
          this.addResult = JSON.parse(err.error).message;
        }
      )
    } else {
      this.addResult = 'Need values for badge and name';
    }
  }

  showAddResult() {
    return !isEmpty(this.addResult);
  }

  // Only for non-admin
  bookButtonClick(_event: any, cleaner: any): void {
    this.userService.addBooking(cleaner.id, this.selectedToDate()).subscribe(
      data => {
        if (data.success) {
          this.bookingResult = 'Booked';
        } else {
          this.bookingResult = data.msg;
        }
      },
      err => {
        this.bookingResult = JSON.parse(err.error).message;
      }
    )
  }

  closeBookResult() {
    this.bookingResult = '';
  }

  showBookResult() {
    return !isEmpty(this.bookingResult);
  }
}
