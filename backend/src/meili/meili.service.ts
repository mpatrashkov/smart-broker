import { Injectable, OnModuleInit } from '@nestjs/common';
import { MeiliSearch, Index } from 'meilisearch';

@Injectable()
export class MeiliService implements OnModuleInit {
  client: MeiliSearch;
  listingsIndex: Index<any>;

  onModuleInit() {
    this.client = new MeiliSearch({
      host: 'http://127.0.0.1:7700',
      // apiKey: 'masterKey',
    });

    this.listingsIndex = this.client.index('listings');
  }

  addListings(listings: any[]) {
    return this.listingsIndex.addDocuments(listings);
  }

  search(term: string) {
    return this.listingsIndex.search(term);
  }
}
