import { Component, OnInit } from '@angular/core';
import { UploadService } from '../upload.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatDialog } from '@angular/material/dialog';
import { DialogConfirmComponent } from '../dialog-confirm/dialog-confirm.component';

@Component({
  selector: 'app-container',
  templateUrl: './container.component.html',
  styleUrls: ['./container.component.css']
})

export class ContainerComponent implements OnInit {
  public files: any[] = [];
  video_file: any = null;
  constructor(private upload: UploadService, private _snackBar: MatSnackBar, public dialog: MatDialog) { }

  ngOnInit(): void {
  }

  onFileSelected(pFileList: File[]) {


    if (pFileList.length > 0) {

      this.files = Object.keys(pFileList).map((key: any) => pFileList[key]);
      this._snackBar.open("Successfully upload!", 'Close', {
        duration: 2000,
      });
      this.video_file = pFileList[0]
      console.log(this.video_file);
      this.uploadFileToServer()
    }
  }

  openConfirmDialog(pIndex: number): void {
    const dialogRef = this.dialog.open(DialogConfirmComponent, {
      panelClass: 'modal-xs'
    });
    dialogRef.componentInstance.fName = this.files[pIndex].name;
    dialogRef.componentInstance.fIndex = pIndex;


    dialogRef.afterClosed().subscribe(result => {
      if (result !== undefined) {
        this.deleteFromArray(result);
      }
    });
  }

  deleteFromArray(index: number) {
    console.log(this.files);
    this.files.splice(index, 1);
  }


  uploadFileToServer() {
    this.upload.postFile(this.video_file).subscribe(data => {
      this._snackBar.open("Successfully upload!", 'Close', {
        duration: 2000,
      });
      console.log(data)
    }, error => {
      console.log(error);
    });
  }

}
