/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_API_URL: string
  readonly VITE_API_TIMEOUT: string
  readonly VITE_ENABLE_GUEST_MODE: string
  readonly VITE_ENABLE_SOCIAL_LOGIN: string
  readonly VITE_GOOGLE_CLIENT_ID: string
  readonly VITE_GITHUB_CLIENT_ID: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
