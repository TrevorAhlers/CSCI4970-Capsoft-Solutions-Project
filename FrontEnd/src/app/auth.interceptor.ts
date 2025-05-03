// Makes sure users can't access pages and information without being logged in.

import { Injectable } from '@angular/core';
import { HttpInterceptor, HttpRequest, HttpHandler } from '@angular/common/http';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {
	intercept(req: HttpRequest<any>, next: HttpHandler) {
		const jwt = localStorage.getItem('jwt');
		if (jwt) {
			req = req.clone({ setHeaders: { Authorization: `Bearer ${jwt}` } });
		}
		return next.handle(req);
	}
}

