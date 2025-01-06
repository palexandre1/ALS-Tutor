import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HangmanService {
  private baseUrl = 'http://127.0.0.1:8080'

  constructor(private http: HttpClient) {}

  startGame(): Observable<any> {
    return this.http.get('/hangman/start', { withCredentials: true })
  }

  getGameState(): Observable<any> {
    return this.http.get(`${this.baseUrl}/hangman/state`, { withCredentials: true })
  }

  submitGuess(guess: string): Observable<any> {
    return this.http.post('/hangman/guess', { guess }, { withCredentials: true })
  }
}
