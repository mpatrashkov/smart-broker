import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
// import { AuthModule } from './auth/auth.module';
import { ScraperModule } from './scraper/scraper.module';
import { MeiliModule } from './meili/meili.module';

@Module({
  imports: [
    // AuthModule,
    ScraperModule,
    MeiliModule,
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
