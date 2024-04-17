const missingVariables = [];

const required = (variable) => {
  const value = process.env[variable];
  if (!value) {
    missingVariables.push(variable);
  }
  return value;
};

export const { REACT_APP_BACKEND_URL = required("REACT_APP_BACKEND_URL") } =
  process.env;

if (missingVariables.length) {
  throw new Error(`Missing environment variables: ${missingVariables}`);
}
