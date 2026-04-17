import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

@Injectable()
export class ItemsService {
  constructor(private prisma: PrismaService) {}

  async findAll() {
    return this.prisma.item.findMany();
  }

  async findOne(id: string) {
    return this.prisma.item.findUnique({ where: { id } });
  }

  async create(data: any) {
    return this.prisma.item.create({ data });
  }
}
