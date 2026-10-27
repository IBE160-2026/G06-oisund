import { createRoot } from 'react-dom/client';
import { PrivateAccess } from './PrivateAccess';
import './style.css';

// Dedicated private publication: no fictional demo entry point or API.
createRoot(document.getElementById('root')!).render(<PrivateAccess />);
