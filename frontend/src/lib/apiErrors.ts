interface ApiErrorResponse {
  error: string;
  messages?: Record<string, string[]>;
}

export function formatApiError(errorData: ApiErrorResponse): string {
  if (!errorData.messages) return errorData.error;
  
  const fieldErrors = Object.entries(errorData.messages)
    .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
    .join('; ');
  
  return `${errorData.error} - ${fieldErrors}`;
}
