import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Box,
} from '@mui/material';
import { HarmonyTask } from '../../models/harmonyTaskModel';

interface HarmonyTaskModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (task: Partial<HarmonyTask>) => void;
  task?: HarmonyTask;
  mode: 'create' | 'edit';
}

const HarmonyTaskModal: React.FC<HarmonyTaskModalProps> = ({
  open,
  onClose,
  onSave,
  task,
  mode,
}) => {
  const [formData, setFormData] = React.useState<Partial<HarmonyTask>>({
    title: task?.title || '',
    description: task?.description || '',
    difficulty: task?.difficulty || 'medium',
    status: task?.status || 'not_started',
  });

  const handleChange = (field: keyof HarmonyTask, value: string) => {
    setFormData((prev) => ({
      ...prev,
      [field]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>{mode === 'create' ? '新規和声課題作成' : '和声課題編集'}</DialogTitle>
      <form onSubmit={handleSubmit}>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField
              label="タイトル"
              value={formData.title}
              onChange={(e) => handleChange('title', e.target.value)}
              required
              fullWidth
            />
            <TextField
              label="説明"
              value={formData.description}
              onChange={(e) => handleChange('description', e.target.value)}
              multiline
              rows={4}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel id="difficulty-label">難易度</InputLabel>
              <Select
                labelId="difficulty-label"
                value={formData.difficulty}
                label="難易度"
                onChange={(e) => handleChange('difficulty', e.target.value)}
              >
                <MenuItem value="easy">易</MenuItem>
                <MenuItem value="medium">中</MenuItem>
                <MenuItem value="hard">難</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel id="status-label">状態</InputLabel>
              <Select
                labelId="status-label"
                value={formData.status}
                label="状態"
                onChange={(e) => handleChange('status', e.target.value)}
              >
                <MenuItem value="not_started">未着手</MenuItem>
                <MenuItem value="in_progress">進行中</MenuItem>
                <MenuItem value="completed">完了</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>キャンセル</Button>
          <Button type="submit" variant="contained" color="primary">
            {mode === 'create' ? '作成' : '更新'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default HarmonyTaskModal;
