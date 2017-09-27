import {Component} from '@angular/core';
import {Http, Headers} from '@angular/http';
import {Injectable} from '@angular/core';


import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import {timestamp} from "rxjs/operator/timestamp";
import {forEach} from "@angular/router/src/utils/collection";
import {not} from "rxjs/util/not";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

@Injectable()
export class AppComponent {
  title = 'INES - Mattermost Search';
  mattermost_results: Array<String>;
  newsflash_results: Array<String>;
  query: string;
  http: Http;

  private elasticUrl = 'http://localhost:9200/mm_015/_search?from=0&size=1000&q=';
  //private newsflashUrl = 'http://localhost:9200/newsflash/_search?from=0&size=1000&q=';
  //private elasticUrl = 'http://35.187.72.132:9200/logstash-2017.07.06/_search?from=0&size=1000&q=';

  constructor(http: Http) {
    this.mattermost_results = [];
    this.newsflash_results = [];
    this.http = http;
    this.query = "";
  }

  convert(string) {
    let date = new Date(string);
    return date.toString();
  }

  linkToMattermost(any) {
    return (any.first_name.indexOf("newsflash") < 0);
  }

  getMattermostLink(any) {
    return  "https://mattermost.inovex.de/inovex/pl/" + any.id;
  }

  fitMessage(string) {
    let idx = string.indexOf(this.query.split(" ")[0]);
    return string;
  }

  search() {
    const headerDict = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    const headerObj = {
      headers: new Headers(headerDict),
    };

    this.http
      .get(this.elasticUrl + this.query, headerObj)
      .map(resp => resp.json())
      .subscribe(
        (result) => {
          this.mattermost_results = result.hits.hits;
        },
        (err) => {
          console.debug(err);
        });

    /*this.http
      .get(this.newsflashUrl + this.query, headerObj)
      .map(resp => resp.json())
      .subscribe(
        (result) => {
          this.newsflash_results = result.hits.hits;
        },
        (err) => {
          console.debug(err);
        });*/
  }

}
