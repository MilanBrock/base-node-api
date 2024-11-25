// src/controllers/userController.ts
import { Request, Response } from 'express';
import { AppDataSource } from '../config/database';
import { createTestEntity, readTestEntity, updateTestEntity, deleteTestEntity } from '../utils/databaseCRUD';
import { openAIRequest } from '../utils/openai';
import { groqChatCompletion } from '../utils/groq';



export const TestEndpoint = async (req: Request, res: Response) => {
  try {
    res.status(201).json({"message": "Test successful"});
  } catch (err) {
    console.error(err);
    res.status(500).send('Server Error');
  }
};

export const CreateTestEntity = async (req: Request, res: Response) => {
    const { value } = req.body;
    try {
        const succes = await createTestEntity(value);
        if (succes) {
            res.status(201).json({"message": "Test successful"});
        } else {
            res.status(400).json({"message": "Test failed"});
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
};

export const ReadTestEntity = async (req: Request, res: Response) => {
    const { id } = req.body;
    try {
        const testEntity = await readTestEntity(id);
        if (testEntity !== null) {
            res.status(201).json({"message": "Test successful", "data": testEntity});
        } else {
            res.status(400).json({"message": "Test failed"});
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
};

export const UpdateTestEntity = async (req: Request, res: Response) => {
    const { id, value } = req.body;
    try {
        const succes = await updateTestEntity(id, value);
        if (succes) {
            res.status(201).json({"message": "Test successful"});
        } else {
            res.status(400).json({"message": "Test failed"});
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
}

export const DeleteTestEntity = async (req: Request, res: Response) => {
    const { id } = req.body;
    try {
        const succes = await deleteTestEntity(id);
        if (succes) {
            res.status(201).json({"message": "Test successful"});
        } else {
            res.status(400).json({"message": "Test failed"});
        }
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
}

export const OpenAIRequest = async (req: Request, res: Response) => {
    const { prompt, userMessage } = req.body;
    try {
        const response = await openAIRequest(prompt, userMessage);
        res.status(201).json({"message": "Test successful", "data": response});
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
}


// Sends a request to the Groq API
export const GroqRequest = async (req: Request, res: Response) => {
    try {
        const response = await groqChatCompletion(req.body.messages);
        res.status(201).json({"message": "Test successful", "data": response});
    } catch (err) {
        console.error(err);
        res.status(500).send('Server Error');
    }
}











