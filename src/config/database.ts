// src/config/database.ts
import 'reflect-metadata';
import { ColumnType, DataSource } from 'typeorm';
import { TestEntity } from '../entities/testEntity';

export const AppDataSource = new DataSource({
  type: 'postgres',
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT as string, 10),
  username: process.env.DATABASE_USERNAME,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  synchronize: true,
  logging: false,
  entities: [TestEntity],
  migrations: [],
  subscribers: [],
});

export const connectDB = async () => {
  try {
    await AppDataSource.initialize();
    AppDataSource.driver.supportedDataTypes.push("vector" as ColumnType);
    AppDataSource.driver.withLengthColumnTypes.push("vector" as ColumnType);
    console.log('Connected to the PostgreSQL database with TypeORM');
  } catch (err) {
    console.error('Error connecting to the database', err);
    process.exit(1);
  }
};
