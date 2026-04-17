import { Injectable, OnModuleInit, Logger } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Telegraf } from 'telegraf';

@Injectable()
export class BotService implements OnModuleInit {
  private bot: Telegraf;
  private readonly logger = new Logger(BotService.name);

  constructor(private configService: ConfigService) {}

  onModuleInit() {
    const token = this.configService.get<string>('TELEGRAM_BOT_TOKEN');
    
    if (!token) {
      this.logger.error('TELEGRAM_BOT_TOKEN is not defined in environment variables! Bot initialization skipped.');
      return;
    }

    this.bot = new Telegraf(token);

    this.bot.start((ctx) => {
      const webAppUrl = this.configService.get<string>('WEB_APP_URL') || 'https://google.com';
      ctx.reply('Привет! Я бот P2P-маркетплейса. Открой Mini App для начала работы!', {
        reply_markup: {
          inline_keyboard: [
            [{ text: 'Открыть маркетплейс', web_app: { url: webAppUrl } }]
          ]
        }
      });
    });

    this.bot.launch().catch(err => this.logger.error('Bot launch error', err));
  }
}
