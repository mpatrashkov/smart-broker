import { Module } from '@nestjs/common';
import { MeiliModule } from 'src/meili/meili.module';
import { ScraperController } from './scraper.controller';
import { ScraperService } from './scraper.service';

@Module({
  controllers: [ScraperController],
  providers: [ScraperService],
  imports: [MeiliModule],
})
export class ScraperModule {}
1