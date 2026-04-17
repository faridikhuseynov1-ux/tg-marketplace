import { Controller, Get, Post, Body, Param } from '@nestjs/common';
import { ItemsService } from './items.service';
import { CreateItemDto } from './dto/create-item.dto';

@Controller('items')
export class ItemsController {
  constructor(private readonly itemsService: ItemsService) {}

  @Get()
  async findAll() {
    return this.itemsService.findAll();
  }

  @Get(':id')
  async findOne(@Param('id') id: string) {
    return this.itemsService.findOne(id);
  }

  @Post()
  async create(@Body() createItemDto: CreateItemDto) {
    return this.itemsService.create(createItemDto);
  }
}
