import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ListItem, ListItemText, Typography, Chip, IconButton } from '@mui/material';
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

interface HarmonyTaskListItemProps {
  task: HarmonyTask;
}

export const HarmonyTaskListItem: React.FC<HarmonyTaskListItemProps> = ({ task }) => {
  const navigate = useNavigate();

  return (
    <ListItem
      className="border-b border-gray-200 hover:bg-gray-50 transition-colors"
      secondaryAction={
        <IconButton edge="end" onClick={() => navigate(`/tasks/${task.id}`)}>
          <ChevronRightIcon />
        </IconButton>
      }
    >
      <ListItemText
        primary={
          <div className="flex items-center gap-2">
            <Typography variant="subtitle1" className="font-bold">
              {task.title}
            </Typography>
            <Chip
              size="small"
              label={task.difficulty}
              color={getDifficultyColor(task.difficulty)}
              variant="outlined"
            />
          </div>
        }
        secondary={task.description}
      />
    </ListItem>
  );
};
