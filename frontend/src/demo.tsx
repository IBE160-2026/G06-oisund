import { ThemeProvider } from './theme';
import { createRoot } from 'react-dom/client';
import { FictionalAssessment } from './FictionalAssessment';
import './style.css';
createRoot(document.getElementById('root')!).render(<ThemeProvider><FictionalAssessment /></ThemeProvider>);
