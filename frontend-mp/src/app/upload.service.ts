import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class UploadService {

  constructor(private httpClient: HttpClient) { }


  postFile(fileToUpload: File) {
    const endpoint = 'http://localhost:5000/upload';
    const formData: FormData = new FormData();
    const yourHeadersConfig = {}

    formData.append('file', fileToUpload, fileToUpload.name);
    return this.httpClient
      .post(endpoint, formData, { headers: yourHeadersConfig })
      .pipe(map((res) => {
        console.log(res)
        return res
      }))
  }


  handleError(e: any) {
    console.log(e);
  }
}
