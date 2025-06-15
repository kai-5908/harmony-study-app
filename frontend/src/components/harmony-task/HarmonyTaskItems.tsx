import React from 'react';
import { Link } from 'react-router-dom';
import { List, Box } from '@mui/material';
import { HarmonyTask } from '../../models/harmonyTaskModel';
import HarmonyTaskListItem from './HarmonyTaskListItem';
import HarmonyTaskGridItem from './HarmonyTaskGridItem';

interface HarmonyTaskItemsProps {
  tasks: HarmonyTask[];
  viewMode: 'list' | 'grid';
}

const HarmonyTaskItems: React.FC<HarmonyTaskItemsProps> = ({ tasks, viewMode }) => {
  if (viewMode === 'list') {
    return (
      <List>
        {tasks.map((task) => (
          <Link key={task.id} to={`/tasks/${task.id}`} className="no-underline">
            <HarmonyTaskListItem task={task} />
          </Link>
        ))}
      </List>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box
        sx={{
          display: 'grid',
          gridTemplateColumns: {
            xs: '1fr',
            sm: 'repeat(2, minmax(0, 1fr))',
            md: 'repeat(3, minmax(0, 1fr))',
          },
          gap: 3,
          width: '100%',
        }}
      >
        {tasks.map((task) => (
          <Link key={task.id} to={`/tasks/${task.id}`} className="no-underline">
            <Box>
              <HarmonyTaskGridItem task={task} />
            </Box>
          </Link>
        ))}
      </Box>
    </Box>
  );
};

export default HarmonyTaskItems;
