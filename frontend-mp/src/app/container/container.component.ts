import { Component, OnInit } from '@angular/core';
import { UploadService } from '../upload.service';

@Component({
  selector: 'app-container',
  templateUrl: './container.component.html',
  styleUrls: ['./container.component.css']
})
export class ContainerComponent implements OnInit {
  video_file: any
  constructor(private upload: UploadService) { }

  ngOnInit(): void {
  }

  onFileSelected(event: any) {
    if (event.target.files.length > 0) {
      let files: FileList = event.target.files
      this.video_file = files.item(0);
      console.log(this.video_file);
      this.uploadFileToServer()
    }
  }

  uploadFileToServer() {
    this.upload.postFile(this.video_file).subscribe(data => {
      // do something, if upload success
      console.log(data)
    }, error => {
      console.log(error);
    });
  }

}
