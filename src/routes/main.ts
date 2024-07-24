// src/routes/users.ts
import { Router } from 'express';
import { TestEndpoint, CreateTestEntity, ReadTestEntity, UpdateTestEntity, DeleteTestEntity } from '../controllers/mainController';

const router = Router();

router.post("/test", TestEndpoint)
router.post("/create", CreateTestEntity)
router.post("/read", ReadTestEntity)
router.post("/update", UpdateTestEntity)
router.post("/delete", DeleteTestEntity)

export default router;
