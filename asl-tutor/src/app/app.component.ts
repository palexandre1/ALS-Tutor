import { Component, Inject, Injectable, ViewChild } from '@angular/core';
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
      const arr = this.webcamImage.imageAsDataUrl.split(",");
      // const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }
      const file: File = new File([u8arr], 'snapshot.jpeg', { type: 'image/jpeg' })
      console.log(file);

      let formData = new FormData();
      formData.append('file', file);

      this.httpClient.post(url,formData).subscribe(
        data => {
          console.log(data)
        })
    }
  }
}
