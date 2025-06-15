import React, { useState, useEffect } from 'react';
import { Container, Paper, CircularProgress, Alert } from '@mui/material';
import HarmonyTaskListHeader from './HarmonyTaskListHeader';
import { HarmonyTaskItems } from './HarmonyTaskItems';
import { HarmonyTask } from '../../models/harmonyTaskModel';
import { HarmonyTaskAPI } from '../../api/harmonyTaskApi';

export const HarmonyTaskList: React.FC = () => {
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');
  const [tasks, setTasks] = useState<HarmonyTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await HarmonyTaskAPI.getTasks();
        setTasks(data);
        setError(null);
      } catch (err) {
        setError('課題の読み込みに失敗しました。しばらくしてから再度お試しください。');
        console.error('Failed to fetch tasks:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="xl" className="py-4 flex justify-center items-center min-h-[400px]">
        <CircularProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" className="py-4">
      <Paper elevation={0} className="overflow-hidden rounded-lg shadow-sm">
        <HarmonyTaskListHeader viewMode={viewMode} onViewModeChange={setViewMode} />
        {error ? (
          <Alert severity="error" className="m-4">
            {error}
          </Alert>
        ) : (
          <HarmonyTaskItems tasks={tasks} viewMode={viewMode} />
        )}
      </Paper>
    </Container>
  );
};

export default HarmonyTaskList;
