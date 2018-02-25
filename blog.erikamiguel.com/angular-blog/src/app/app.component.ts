import { Component, OnInit } from '@angular/core';
import { Title }     from '@angular/platform-browser';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
	title = "Erika Miguel's Blog";

	constructor(private titleService: Title){ }

	public setTitle(title: string){
		this.titleService.setTitle(title);
	}

	ngOnInit(){
		this.setTitle(this.title)
	}
}
