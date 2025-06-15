import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Paper,
  Typography,
  Box,
  Chip,
  CircularProgress,
  Alert,
  IconButton,
  ChipProps,
} from '@mui/material';
import { ArrowBack as ArrowBackIcon, MusicNote as MusicNoteIcon } from '@mui/icons-material';
import { HarmonyTask } from '../../models/harmonyTaskModel';
import { HarmonyTaskAPI } from '../../api/harmonyTaskApi';

type DifficultyColor = NonNullable<ChipProps['color']>;

const getDifficultyColor = (difficulty?: string): DifficultyColor => {
  switch (difficulty) {
    case 'easy':
      return 'success';
    case 'normal':
      return 'warning';
    case 'hard':
      return 'error';
    default:
      return 'default';
  }
};

const HarmonyTaskDetail: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();
  const navigate = useNavigate();
  const [task, setTask] = useState<HarmonyTask | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTask = async () => {
      if (!taskId) return;

      try {
        const data = await HarmonyTaskAPI.getTask(taskId);
        setTask(data);
        setError(null);
      } catch (err) {
        setError('課題の読み込みに失敗しました。しばらくしてから再度お試しください。');
        console.error('Failed to fetch task:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchTask();
  }, [taskId]);

  if (loading) {
    return (
      <Container maxWidth="xl" className="py-4 flex justify-center items-center min-h-[400px]">
        <CircularProgress />
      </Container>
    );
  }

  if (error || !task) {
    return (
      <Container maxWidth="xl" className="py-4">
        <Alert
          severity="error"
          action={
            <IconButton color="inherit" size="small" onClick={() => navigate('/')}>
              <ArrowBackIcon />
            </IconButton>
          }
        >
          {error || '課題が見つかりません'}
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="xl" className="py-4">
      <Paper elevation={0} className="p-6 rounded-lg">
        <Box className="space-y-4">
          <Box className="flex items-center gap-4">
            <IconButton onClick={() => navigate('/')}>
              <ArrowBackIcon />
            </IconButton>
            <Typography variant="h4" component="h1" className="font-bold">
              {task.title}
            </Typography>
          </Box>

          <Box className="flex flex-wrap gap-2">
            <Chip
              label={`難易度: ${task.difficulty}`}
              color={getDifficultyColor(task.difficulty)}
              variant="outlined"
            />
          </Box>

          <Typography variant="body1" className="whitespace-pre-line">
            {task.description}
          </Typography>

          <Box className="mt-8">
            <Typography variant="h5" className="font-bold mb-4">
              課題楽譜
            </Typography>
            <Paper className="p-4 bg-gray-50">
              <Box className="flex items-center gap-2">
                <MusicNoteIcon />
                <Typography>{task.score.data}</Typography>
              </Box>
            </Paper>
          </Box>
        </Box>
      </Paper>
    </Container>
  );
};

export default HarmonyTaskDetail;
