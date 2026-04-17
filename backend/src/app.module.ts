import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { PrismaModule } from './prisma/prisma.module';
import { BotModule } from './bot/bot.module';
import { ItemsModule } from './items/items.module';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    PrismaModule, 
    BotModule, 
    ItemsModule
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
