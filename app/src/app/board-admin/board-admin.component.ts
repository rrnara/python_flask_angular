import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { isEmpty } from 'lodash';
import { AuthService } from '../_services/auth.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-board-admin',
  templateUrl: './board-admin.component.html',
  styleUrls: ['./board-admin.component.css']
})
export class BoardAdminComponent implements OnInit {
  admins: Array<any> = [];
  fetchResult = '';

  addAdminForm = this.formBuilder.group({
    name: '',
    username: '',
    password: ''
  });
  addResult: string = '';

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private userService: UserService) { }

  ngOnInit(): void {
    this.fetchAdmins()
  }

  fetchAdmins() {
    this.userService.getAdmins().subscribe(
      data => {
        if (data.success) {
          this.admins = data.users;
        } else {
          this.fetchResult = data.msg
        }
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

  onSubmit(): void {
    const { name, username, password } = this.addAdminForm.value
    if (!isEmpty(name) && !isEmpty(username) && !isEmpty(password)) {
      this.authService.addAdmin(name, username, password).subscribe(
        data => {
          if (data.success) {
            this.addResult = 'Added';
            setTimeout(() => {
              this.addResult = '';
            }, 3000);
            this.addAdminForm.reset();
            this.fetchAdmins();
          } else {
            this.addResult = data.msg;
          }
        },
        err => {
          this.addResult = JSON.parse(err.error).message;
        }
      )
    } else {
      this.addResult = 'Need values for name, username and password';
    }
  }

  showAddResult() {
    return !isEmpty(this.addResult);
  }
}
