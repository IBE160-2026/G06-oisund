import { createContext, useContext, useEffect, useLayoutEffect, useState, type ReactNode } from 'react';

// Persist only this allowlisted presentation value, never application state.
const KEY = 'ibe160-theme';
type Theme = 'day' | 'night';
const ThemeContext = createContext({ night: false, toggle: () => {} });
function initialTheme(): Theme {
  try { return localStorage.getItem(KEY) === 'night' ? 'night' : 'day'; }
  catch { return 'day'; }
}
export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setTheme] = useState<Theme>(initialTheme);
  useLayoutEffect(() => {
    document.documentElement.classList.toggle('night', theme === 'night');
    document.documentElement.dataset.theme = theme;
  }, [theme]);
  useEffect(() => {
    const update = (event: StorageEvent) => {
      if (event.key === KEY || event.key === null) setTheme(event.newValue === 'night' ? 'night' : 'day');
    };
    window.addEventListener('storage', update);
    return () => window.removeEventListener('storage', update);
  }, []);
  return <ThemeContext value={{ night: theme === 'night', toggle: () => setTheme(current => { const next = current === 'day' ? 'night' : 'day'; try { localStorage.setItem(KEY, next); } catch { /* Continue in memory. */ } return next; }) }}>{children}</ThemeContext>;
}
export const useTheme = () => useContext(ThemeContext);
export function ThemeControl({ demo = false }: { demo?: boolean }) {
  const { night, toggle } = useTheme();
  return <div className="theme-control"><button type="button" aria-pressed={night} onClick={toggle}>{demo ? night ? 'Bytt til dagvisning' : 'Bytt til nattvisning' : 'Nattmodus'}</button><span>Visning: {night ? 'Natt' : 'Dag'}</span></div>;
}
