import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../_services/auth.service';
import { TokenStorageService } from '../_services/token-storage.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  form: any = {
    username: null,
    password: null
  };
  isLoggedIn = false;
  isLoginFailed = false;
  errorMessage = '';
  role?: string;

  constructor(private router: Router, private authService: AuthService, private tokenStorage: TokenStorageService, private userService: UserService) { }

  ngOnInit(): void {
    if (this.tokenStorage.getToken()) {
      this.userService.getMe().subscribe(
        user => {
          this.role = user.role;
          setTimeout(() => {
            this.router.navigate(['home']);
          }, 2000);
        },
        err => {
          this.tokenStorage.clearToken();
          window.location.reload();
        }
      )
    }
  }

  onSubmit(): void {
    const { username, password } = this.form;

    this.authService.login(username, password).subscribe(
      data => {
        this.isLoggedIn = data.success;
        if (this.isLoggedIn) {
          this.role = data.user.role;
          this.tokenStorage.saveToken(data.msg);
          setTimeout(() => {
            this.router.navigate(['home']);
          }, 2000);
          window.location.reload();
        } else {
          this.errorMessage = data.msg;
        }
      },
      err => {
        this.errorMessage = err.error.message;
        this.isLoginFailed = true;
      }
    );
  }
}
