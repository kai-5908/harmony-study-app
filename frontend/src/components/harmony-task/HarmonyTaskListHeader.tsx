import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from '@mui/material';
import {
  ViewList as ViewListIcon,
  ViewModule as ViewModuleIcon,
  Sort as SortIcon,
  FilterList as FilterListIcon,
} from '@mui/icons-material';

interface HarmonyTaskListHeaderProps {
  viewMode: 'list' | 'grid';
  onViewModeChange: (mode: 'list' | 'grid') => void;
  onSortChange: (sortBy: string) => void;
  onFilterChange: (filterBy: string) => void;
}

const HarmonyTaskListHeader: React.FC<HarmonyTaskListHeaderProps> = ({
  viewMode,
  onViewModeChange,
  onSortChange,
  onFilterChange,
}) => {
  return (
    <>
      {' '}
      <AppBar position="static" color="primary" elevation={0}>
        <Toolbar sx={{ minHeight: 72, px: 3 }}>
          <Typography
            variant="h5"
            component="h1"
            sx={{
              flexGrow: 1,
              fontWeight: 'bold',
              fontSize: { xs: '1.25rem', sm: '1.5rem' },
            }}
          >
            和声課題一覧
          </Typography>
        </Toolbar>
      </AppBar>{' '}
      <Box
        sx={{
          bgcolor: 'background.paper',
          borderBottom: 1,
          borderColor: 'divider',
          px: 3,
          py: 2,
        }}
        className="flex justify-between items-center"
      >
        <div className="flex items-center gap-4">
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel id="filter-label" className="flex items-center gap-1">
              <FilterListIcon fontSize="small" />
              フィルター
            </InputLabel>
            <Select
              labelId="filter-label"
              value=""
              label="フィルター"
              onChange={(e) => onFilterChange(e.target.value)}
            >
              <MenuItem value="all">すべて</MenuItem>
              <MenuItem value="not-started">未着手</MenuItem>
              <MenuItem value="in-progress">進行中</MenuItem>
              <MenuItem value="completed">完了</MenuItem>
              <MenuItem value="easy">難易度：易</MenuItem>
              <MenuItem value="medium">難易度：中</MenuItem>
              <MenuItem value="hard">難易度：難</MenuItem>
            </Select>
          </FormControl>
          <FormControl size="small" sx={{ minWidth: 120 }}>
            <InputLabel id="sort-label" className="flex items-center gap-1">
              <SortIcon fontSize="small" />
              ソート
            </InputLabel>
            <Select
              labelId="sort-label"
              value=""
              label="ソート"
              onChange={(e) => onSortChange(e.target.value)}
            >
              <MenuItem value="created-desc">作成日（新しい順）</MenuItem>
              <MenuItem value="created-asc">作成日（古い順）</MenuItem>
              <MenuItem value="difficulty-asc">難易度（易→難）</MenuItem>
              <MenuItem value="difficulty-desc">難易度（難→易）</MenuItem>
              <MenuItem value="progress">進捗状況</MenuItem>
            </Select>
          </FormControl>
        </div>
        <div className="flex gap-1">
          <IconButton
            color={viewMode === 'list' ? 'primary' : 'default'}
            onClick={() => onViewModeChange('list')}
          >
            <ViewListIcon />
          </IconButton>
          <IconButton
            color={viewMode === 'grid' ? 'primary' : 'default'}
            onClick={() => onViewModeChange('grid')}
          >
            <ViewModuleIcon />
          </IconButton>
        </div>
      </Box>
    </>
  );
};

export default HarmonyTaskListHeader;
