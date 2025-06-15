import '@mui/material/Chip';

declare module '@mui/material/Chip' {
  interface ChipPropsColorOverrides {
    default: true;
    primary: true;
    secondary: true;
    info: true;
    success: true;
    warning: true;
    error: true;
  }
}
