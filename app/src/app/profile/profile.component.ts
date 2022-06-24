import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { isEmpty } from 'lodash';
import { AuthService } from '../_services/auth.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  currentUser: any;
  error: string = 'Loading...';

  updatePasswordForm = this.formBuilder.group({
    password: ''
  });
  updateResult = '';

  constructor(private formBuilder: FormBuilder, private authService: AuthService, private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getMe().subscribe(
      user => {
        this.currentUser = user;
      },
      err => {
        this.error = err.toString();
      }
    )
  }

  onSubmit(): void {
    const { password } = this.updatePasswordForm.value
    if (!isEmpty(password)) {
      this.authService.updatePassword(password).subscribe(
        data => {
          if (data.success) {
            this.updateResult = 'Updated';
            setTimeout(() => {
              this.updateResult = '';
            }, 3000);
            this.updatePasswordForm.reset();
          } else {
            this.updateResult = data.msg;
          }
        },
        err => {
          this.updateResult = JSON.parse(err.error).message;
        }
      )
    } else {
      this.updateResult = 'Need new password value';
    }
  }

  showUpdateResult() {
    return !isEmpty(this.updateResult);
  }
}
