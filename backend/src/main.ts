import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ValidationPipe } from '@nestjs/common';
import { BigIntInterceptor } from './common/interceptors/bigint.interceptor';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Включаем валидацию входящих DTO
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));
  
  // Перехватчик для исправления JSON BigInt ошибки от Prisma
  app.useGlobalInterceptors(new BigIntInterceptor());

  app.enableCors();
  
  await app.listen(3000);
}
bootstrap();
