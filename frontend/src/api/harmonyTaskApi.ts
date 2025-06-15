import { HarmonyTask } from '../models/harmonyTaskModel';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

interface APIError extends Error {
  status?: number;
}

export class HarmonyTaskAPI {
  private static async handleResponse<T>(response: Response): Promise<T> {
    if (!response.ok) {
      const error: APIError = new Error('API request failed');
      error.status = response.status;
      throw error;
    }
    return response.json();
  }

  static async getTasks(): Promise<HarmonyTask[]> {
    const response = await fetch(`${API_BASE_URL}/tasks`);
    return this.handleResponse<HarmonyTask[]>(response);
  }

  static async getTask(id: string): Promise<HarmonyTask> {
    const response = await fetch(`${API_BASE_URL}/tasks/${id}`);
    return this.handleResponse<HarmonyTask>(response);
  }
}
