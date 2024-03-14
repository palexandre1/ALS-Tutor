import { Component, Inject, Injectable } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { WebcamImage } from 'ngx-webcam';
import { CameraComponent } from './camera/camera.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, CameraComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  public title: string;
  public visible: boolean;
  public webcamImage: WebcamImage | null;

  constructor() {
    this.title = 'ASL-Tutor';
    this.visible = false;
    this.webcamImage = null;
  }

  toggleCamera() {
    this.visible = !this.visible;
  }

  handleImage(webcamImage: WebcamImage) {
    this.webcamImage = webcamImage;
  }
}
