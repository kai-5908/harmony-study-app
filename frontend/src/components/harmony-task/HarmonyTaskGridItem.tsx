import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, CardContent, Typography, Chip, CardActionArea, Box } from '@mui/material';
import { ChevronRight as ChevronRightIcon } from '@mui/icons-material';
import type { HarmonyTask } from '../../models/harmonyTaskModel';

type DifficultyColor = 'success' | 'warning' | 'error' | undefined;

const getDifficultyColor = (difficulty?: string): DifficultyColor => {
  switch (difficulty) {
    case 'easy':
      return 'success';
    case 'normal':
      return 'warning';
    case 'hard':
      return 'error';
    default:
      return undefined;
  }
};

interface HarmonyTaskGridItemProps {
  task: HarmonyTask;
}

export const HarmonyTaskGridItem: React.FC<HarmonyTaskGridItemProps> = ({ task }) => {
  const navigate = useNavigate();

  return (
    <Card className="w-full sm:w-72 hover:shadow-md transition-shadow">
      <CardActionArea onClick={() => navigate(`/tasks/${task.id}`)}>
        <CardContent>
          <Typography
            variant="h6"
            component="h2"
            className="font-bold mb-2 flex items-center justify-between"
          >
            {task.title || '無題の課題'}
            <ChevronRightIcon className="text-gray-400" />
          </Typography>

          <Box className="flex flex-wrap gap-2 mb-2">
            <Chip
              size="small"
              label={`難易度: ${task.difficulty}`}
              color={getDifficultyColor(task.difficulty)}
              variant="outlined"
            />
            {task.tags?.map((tag) => (
              <Chip key={tag} size="small" label={tag} variant="outlined" color="primary" />
            ))}
          </Box>

          <Typography variant="body2" color="text.secondary" className="line-clamp-2">
            {task.description}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
};
