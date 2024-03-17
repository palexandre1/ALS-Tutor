import { Component, Inject, Injectable } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { WebcamImage } from 'ngx-webcam';
import { CameraComponent } from './camera/camera.component';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from  '@angular/common/http';
import { HttpHeaders } from '@angular/common/http';


@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, CommonModule, CameraComponent, HttpClientModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})

export class AppComponent {
  public title: string;
  public visible: boolean;
  public webcamImage: WebcamImage | null;
  public imgURL: string;

  constructor(private httpClient: HttpClient) {
    this.title = 'ASL-Tutor';
    this.visible = false;
    this.webcamImage = null;
    this.imgURL = '';
  }

  toggleCamera() {
    this.visible = !this.visible;
  }

  handleImage(webcamImage: WebcamImage) {
    this.webcamImage = webcamImage;
  }

  uploadImage() {
    let url = 'http://127.0.0.1:8080/predict';

    if (this.webcamImage) {
      this.imgURL = this.webcamImage.imageAsDataUrl
    }

    let formData = new FormData();
    formData.append('file', this.imgURL);

    this.httpClient.post(url,formData).subscribe(
      data => {
        console.log(data)
      }
    )
  }
}
