import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { HarmonyTaskList } from './components/harmony-task/HarmonyTaskList';
import HarmonyTaskDetail from './components/harmony-task/HarmonyTaskDetail';
import theme from './theme';
import './App.css';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<HarmonyTaskList />} />
          <Route path="/tasks/:taskId" element={<HarmonyTaskDetail />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
