import { Component, Inject, Injectable } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { WebcamImage } from 'ngx-webcam';
import { Observable, Subject } from 'rxjs';
import { ServiceService } from './service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'fe-app';

  imageId = 1;
  max = 8;
  taken = false;
  preview = false;
  loader: boolean = false;
  previewUrl = "";

  private trigger: Subject<void> = new Subject<void>();
  public webcamImage: WebcamImage = null as any;

  constructor(private service: ServiceService,
    private _sanitizer: DomSanitizer) {}

  public handleImage(webcamImage: WebcamImage): void {
    console.info('received webcam image', webcamImage);
    this.webcamImage = webcamImage;
    this.taken = true;
  }

  previous(): void {
    this.imageId = this.imageId - 1;
    if (this.imageId < 1) {
      this.imageId = this.max;
    }
  }

  next(): void {
    this.imageId = this.imageId + 1;
    if (this.imageId > this.max) {
      this.imageId = 1;
    }
  }

  public get triggerObservable(): Observable<void> {
    return this.trigger.asObservable();
  }

  take(): void {
    this.trigger.next();
  }

  retake(): void {
    this.taken = false;
    this.preview = false;
  }

  personalize(): void {
    this.loader = true;
    this.service
      .process(this.webcamImage.imageAsBase64, this.imageId)
      .subscribe(out => {
        console.log(out);
        this.previewUrl = ' data:image/jpeg;charset=utf-8;base64, '+out.processed;
        this.loader = false;
        this.preview = true;
      }
    );
  }

  sanitizeImg(): SafeUrl{
    return this._sanitizer.bypassSecurityTrustUrl(this.previewUrl);
 }

  buy(): void {
    console.log("buy");
  }
}
