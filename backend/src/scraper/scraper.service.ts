import { Injectable } from '@nestjs/common';
import { MeiliService } from 'src/meili/meili.service';
import { PythonShell } from 'python-shell';

@Injectable()
export class ScraperService {
  constructor(private meiliService: MeiliService) {}

  scrape() {
    let timeRn = new Date().toLocaleTimeString();
    console.log(`Started Python scraper at ${timeRn}`);
    PythonShell.run('../scraper-python/alobg.py', null, (err, data) => {
      console.log(err);

      const listings = JSON.parse(data[0]);

      this.meiliService.addListings(listings);

      timeRn = new Date().toLocaleTimeString();
      console.log(`Python scraper finished at ${timeRn}`);
    });
  }
}
