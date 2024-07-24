import { AppDataSource } from "../config/database";
import { TestEntity } from "../entities/testEntity";


export async function createTestEntity(value: string): Promise<Boolean> {
    !AppDataSource.isInitialized ? await AppDataSource.initialize() : null;
    const testEntity = new TestEntity();
    testEntity.value = value;
    const assignedId = await AppDataSource.getRepository(TestEntity).save(testEntity);

    if (assignedId) {
        return true;
    } else {
        return false;
    }
}

export async function readTestEntity(id: number): Promise<TestEntity | null> {
    !AppDataSource.isInitialized ? await AppDataSource.initialize() : null;
    const testEntity = await AppDataSource.getRepository(TestEntity).findOne({ where: { id } });

    if (testEntity) {
        return testEntity;
    } else {
        return null;
    }
}

export async function updateTestEntity(id: number, value: string): Promise<Boolean> {
    !AppDataSource.isInitialized ? await AppDataSource.initialize() : null;
    const testEntity = await AppDataSource.getRepository(TestEntity).findOne({ where: { id } });

    if (testEntity) {
        testEntity.value = value;
        const assignedId = await AppDataSource.getRepository(TestEntity).save(testEntity);
        if (assignedId) {
            return true;
        }
    }
    return false;
}

export async function deleteTestEntity(id: number): Promise<Boolean> {
    !AppDataSource.isInitialized ? await AppDataSource.initialize() : null;
    const testEntity = await AppDataSource.getRepository(TestEntity).findOne({ where: { id } });

    if (testEntity) {
        const deletedEntity = await AppDataSource.getRepository(TestEntity).delete(id);
        if (deletedEntity) {
            return true;
        }
    }
    return false;
}