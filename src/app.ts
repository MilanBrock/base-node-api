// src/app.ts
import 'dotenv/config';
import express from 'express';
import { connectDB } from './config/database';
import mainRoutes from './routes/main';

const app = express();
const port = process.env.PORT || 3000;

// Connect to the database
connectDB();

// Middleware to parse JSON bodies
app.use(express.json());

// Routes
app.use('/api', mainRoutes);

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
