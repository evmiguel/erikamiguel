import { Component, OnInit } from '@angular/core';
import { Blog } from '../blog';
import { BLOGS } from '../mock-blogs';

@Component({
  selector: 'app-blog',
  templateUrl: './blog.component.html',
  styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {

  title = "Blog Posts";

  blogs = BLOGS;

  selectedBlog: Blog;

  onSelect(blog: Blog): void {
	  this.selectedBlog = blog;
  }

  constructor() { }

  ngOnInit() {
  }

}
