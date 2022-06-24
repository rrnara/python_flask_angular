import { Component } from '@angular/core';
import { TokenStorageService } from './_services/token-storage.service';
import { UserService } from './_services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  isLoggedIn = false;
  username?: string;
  role?: string
  showAdminBoard = false;

  constructor(private tokenStorageService: TokenStorageService, private userService: UserService) { }

  ngOnInit(): void {
    const isLoggedIn = !!this.tokenStorageService.getToken();
    if (isLoggedIn) {
      this.userService.getMe().subscribe(
        user => {
          this.role = user.role;
          this.username = user.username;
          this.showAdminBoard = user.role === 'admin';
          this.isLoggedIn = true;
        },
        err => {
          this.tokenStorageService.clearToken();
          this.isLoggedIn = false;
        }
      );
    }
  }

  logout(): void {
    this.tokenStorageService.signOut();
    window.location.reload();
  }
}
