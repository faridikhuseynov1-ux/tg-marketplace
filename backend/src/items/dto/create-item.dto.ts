import { IsString, IsNumber, IsArray, IsNotEmpty, IsUUID, Min } from 'class-validator';

export class CreateItemDto {
  @IsString()
  @IsNotEmpty()
  title: string;

  @IsString()
  @IsNotEmpty()
  description: string;

  @IsNumber()
  @Min(0)
  price: number;

  @IsUUID()
  @IsNotEmpty()
  seller_id: string;

  @IsUUID()
  @IsNotEmpty()
  category_id: string;

  @IsArray()
  @IsString({ each: true })
  images: string[];
}
