import { Component, OnInit, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HangmanService } from '../hangman.service';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-hangman',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule ],
  templateUrl: './hangman.component.html',
  styleUrl: './hangman.component.css',
  providers: [HangmanService]
})
export class HangmanComponent implements OnInit{
  gameState: any = null;
  @Input() guessedLetter: string = '';
  isGameStarted: boolean = false;

  constructor(private hangmanService: HangmanService) {}

  ngOnInit(): void {}

  startGame(): void {
    this.hangmanService.startGame().subscribe((state: gameState) => {
      this.gameState = state;
      this.isGameStarted = true;
    })
  }

  fetchGameState(): void {
    this.hangmanService.getGameState().subscribe((state: gameState) => {
      this.gameState = state
    })
  }

  onGuess(): void {
    if (this.guessedLetter) {
      this.hangmanService.submitGuess(this.guessedLetter).subscribe((state: gameState) => {
        this.gameState = state;
        this.guessedLetter = '';
      })
    }
  }
}

interface gameState {
  masked_word: string;
  remaining_guesses: number;
  guessed_letters: string[];
  status: string;
}
